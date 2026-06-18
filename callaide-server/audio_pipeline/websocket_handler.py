"""WebSocket handler for Twilio Media Streams.

Orchestrates the real-time STT→LLM→TTS pipeline during a call.
Receives caller audio over WebSocket, sends it to Deepgram,
feeds transcripts to the LLM conversation manager, and streams
TTS audio back to Twilio.
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Optional

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from config import get_settings
from audio_pipeline.stt import DeepgramSTT, MockSTT
from audio_pipeline.llm import LLMConversation
from audio_pipeline.tts import ElevenLabsTTS, MockTTS
from call_manager.session import CallSession

logger = logging.getLogger(__name__)

router = APIRouter()


class MediaStreamHandler:
    """Manages a single call's audio pipeline.

    Coordinates:
    1. Receiving caller audio from Twilio WebSocket
    2. Sending audio to Deepgram STT
    3. Receiving transcripts from Deepgram
    4. Generating LLM responses
    5. Streaming TTS audio back to Twilio
    """

    def __init__(self, websocket: WebSocket, settings):
        self.ws = websocket
        self.settings = settings
        self.stream_sid: Optional[str] = None
        self.call_sid: Optional[str] = None
        self._caller_greeted = False

        # Pipeline components
        self.session = CallSession()
        self.llm = self._init_llm()
        self.stt = self._init_stt()
        self.tts = self._init_tts()

    def _init_llm(self) -> LLMConversation:
        return LLMConversation(
            provider=self.settings.llm_provider,
            model_live=self.settings.llm_model_live,
            model_setup=self.settings.llm_model_setup,
            openai_api_key=self.settings.openai_api_key,
            anthropic_api_key=self.settings.anthropic_api_key,
        )

    def _init_stt(self):
        if self.settings.deepgram_api_key:
            return DeepgramSTT(
                api_key=self.settings.deepgram_api_key,
                on_transcript=self._on_transcript,
            )
        logger.warning("No DEEPGRAM_API_KEY — using MockSTT")
        return MockSTT(on_transcript=self._on_transcript)

    def _init_tts(self):
        if self.settings.elevenlabs_api_key:
            return ElevenLabsTTS(
                api_key=self.settings.elevenlabs_api_key,
                voice_id=self.settings.tts_voice_id,
            )
        logger.warning("No ELEVENLABS_API_KEY — using MockTTS")
        return MockTTS()

    async def _on_transcript(self, text: str, is_final: bool):
        """Called by STT when a transcript chunk is ready."""
        if not is_final:
            return

        logger.info(f"Caller said: {text}")

        # Add to conversation
        self.llm.add_user_message(text)

        # Generate AI response
        response_text = await self.llm.generate_response()
        logger.info(f"AI responds: {response_text[:100]}…")

        # Stream TTS audio back to Twilio
        async for audio_chunk in self.tts.synthesize(response_text):
            if self.stream_sid:
                await self._send_media(audio_chunk)

    async def _send_media(self, audio_chunk: bytes):
        """Send an audio chunk to Twilio via the Media Stream."""
        message = {
            "event": "media",
            "streamSid": self.stream_sid,
            "media": {
                "payload": audio_chunk.hex(),
            },
        }
        await self.ws.send_json(message)

    async def _send_greeting(self):
        """Send the initial greeting to the caller."""
        # Prime the conversation with a system prompt extract
        # The LLM will respond as the AI receptionist
        greeting_text = (
            "Thanks for calling! My name is Amy. "
            "How can I help you today?"
        )
        self.llm.add_assistant_message(greeting_text)

        logger.info(f"AI greeting: {greeting_text}")

        async for audio_chunk in self.tts.synthesize(greeting_text):
            await self._send_media(audio_chunk)

        self._caller_greeted = True

    async def run(self):
        """Main run loop for the call session."""
        try:
            # Connect STT
            await self.stt.connect()

            # Start STT receive loop as background task
            stt_task = asyncio.create_task(self.stt.receive_loop())

            # Process incoming Twilio messages
            async for raw_message in self.ws.iter_text():
                data = json.loads(raw_message)
                event_type = data.get("event")

                if event_type == "connected":
                    logger.debug(f"Twilio connected event")

                elif event_type == "start":
                    self.stream_sid = data.get("streamSid")
                    start_data = data.get("start", {})
                    self.call_sid = start_data.get("callSid")
                    from_number = start_data.get("from", "unknown")
                    logger.info(
                        f"Call started — SID={self.call_sid} "
                        f"streamSid={self.stream_sid} from={from_number}"
                    )
                    self.session.set_call_sid(self.call_sid)
                    self.session.set_stream_sid(self.stream_sid)

                    # Send greeting
                    await self._send_greeting()

                elif event_type == "media":
                    payload = data.get("media", {}).get("payload", "")
                    if payload:
                        audio_bytes = bytes.fromhex(payload)
                        await self.stt.send_audio(audio_bytes)

                elif event_type == "stop":
                    logger.info(f"Stream stopped — SID={self.stream_sid}")
                    break

            # Wait for STT to finish
            await stt_task

        except WebSocketDisconnect:
            logger.info("WebSocket disconnected by client")
        except Exception as e:
            logger.error(f"Pipeline error: {e}", exc_info=True)
        finally:
            # Cleanup
            await self.stt.close()
            await self.tts.close()
            logger.info(
                f"Call ended — "
                f"SID={self.call_sid} "
                f"messages={self.llm.message_count} "
                f"transcript={self.session.get_transcript_summary()}"
            )


@router.websocket("/media-stream")
async def handle_media_stream(websocket: WebSocket):
    """Handle a Twilio Media Stream WebSocket connection."""
    await websocket.accept()
    settings = get_settings()
    handler = MediaStreamHandler(websocket, settings)
    await handler.run()