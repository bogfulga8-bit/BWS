"""Speech-to-Text — Deepgram real-time streaming client."""

from __future__ import annotations

import json
import logging
from typing import AsyncIterator, Callable, Awaitable

import httpx

logger = logging.getLogger(__name__)

# Deepgram real-time transcription WebSocket URL
DEEPGRAM_WS_URL = "wss://api.deepgram.com/v1/listen"

OnTranscript = Callable[[str, bool], Awaitable[None]]  # text, is_final


class DeepgramSTT:
    """Streaming STT client using Deepgram Nova-2.

    Connects to Deepgram's WebSocket and forwards transcribed
    text to a callback as chunks arrive.
    """

    def __init__(self, api_key: str, *, on_transcript: OnTranscript | None = None):
        self.api_key = api_key
        self.on_transcript = on_transcript
        self._ws = None

    @property
    def connection_params(self) -> dict:
        return {
            "model": "nova-2-general",
            "encoding": "mulaw",
            "sample_rate": 8000,
            "interim_results": True,
            "utterance_end_ms": 1000,
            "vad_events": True,
        }

    async def connect(self):
        """Open the Deepgram WebSocket connection."""
        params = self.connection_params
        query = "&".join(f"{k}={v}" for k, v in params.items())
        url = f"{DEEPGRAM_WS_URL}?{query}"

        headers = {
            "Authorization": f"Token {self.api_key}",
        }

        async with httpx.AsyncClient() as client:
            # Use httpx to upgrade to WebSocket
            import anyio
            from anyio import connect_tcp
            import ssl

            # We'll use websockets library for the actual WebSocket
            import websockets as ws

            self._ws = await ws.connect(
                url,
                extra_headers=headers,
            )
            logger.info("Deepgram STT connected")

    async def send_audio(self, audio_chunk: bytes):
        """Send a μ-law audio chunk to Deepgram for transcription."""
        if self._ws:
            await self._ws.send(audio_chunk)

    async def receive_loop(self):
        """Receive transcription results and dispatch to callback."""
        if not self._ws:
            raise RuntimeError("WebSocket not connected")

        async for message in self._ws:
            data = json.loads(message)
            if "channel" not in data:
                continue

            alternatives = data["channel"].get("alternatives", [])
            if not alternatives:
                continue

            transcript = alternatives[0].get("transcript", "").strip()
            if not transcript:
                continue

            is_final = data.get("is_final", False)
            logger.debug(f"STT: {'[FINAL]' if is_final else '[interim]'} {transcript}")

            if self.on_transcript:
                await self.on_transcript(transcript, is_final)

    async def close(self):
        """Close the Deepgram WebSocket."""
        if self._ws:
            await self._ws.close()
            self._ws = None
            logger.info("Deepgram STT disconnected")


class MockSTT:
    """Mock STT for development without API keys.

    Reads simulated transcripts from a queue for testing.
    """

    def __init__(self, *, on_transcript: OnTranscript | None = None):
        self.on_transcript = on_transcript
        self._queue: list[tuple[str, bool]] = []

    async def connect(self):
        logger.info("MockSTT connected (no API key required)")

    async def send_audio(self, audio_chunk: bytes):
        pass  # Mock — audio is ignored

    async def receive_loop(self):
        """Yield queued transcripts for testing."""
        if not self._queue:
            # Default test transcripts
            self._queue = [
                ("Hi, I'd like to book a plumbing service.", True),
                ("My kitchen sink is leaking badly.", True),
                ("Tomorrow morning would be great if possible.", True),
                ("My name is John Smith and my number is 555-0123.", True),
            ]
        for text, is_final in self._queue:
            if self.on_transcript:
                await self.on_transcript(text, is_final)

    async def close(self):
        logger.info("MockSTT disconnected")

    def add_transcript(self, text: str, is_final: bool = True):
        """Add a test transcript to the queue."""
        self._queue.append((text, is_final))