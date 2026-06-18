"""Text-to-Speech — ElevenLabs / Cartesia streaming client."""

from __future__ import annotations

import logging
from typing import AsyncIterator

import httpx

logger = logging.getLogger(__name__)


class ElevenLabsTTS:
    """Streaming TTS client using ElevenLabs Turbo v2.5.

    Converts response text to μ-law 8000Hz audio chunks
    suitable for Twilio Media Streams.
    """

    BASE_URL = "https://api.elevenlabs.io/v1"

    def __init__(self, api_key: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM"):
        self.api_key = api_key
        self.voice_id = voice_id
        self._client = httpx.AsyncClient()

    async def synthesize(self, text: str) -> AsyncIterator[bytes]:
        """Stream TTS audio for the given text.

        Yields μ-law 8000Hz audio chunks.
        """
        url = f"{self.BASE_URL}/text-to-speech/{self.voice_id}/stream"
        headers = {
            "Accept": "audio/x-mulaw",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key,
        }
        payload = {
            "text": text,
            "model_id": "eleven_turbo_v2_5",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5,
            },
            "optimize_streaming_latency": 4,
            "output_format": "ulaw_8000",
        }

        async with self._client.stream(
            "POST", url, json=payload, headers=headers
        ) as response:
            response.raise_for_status()
            async for chunk in response.aiter_bytes():
                yield chunk

    async def close(self):
        await self._client.aclose()


class MockTTS:
    """Mock TTS for development without API keys.

    Returns small silent μ-law audio chunks to keep the
    pipeline flowing during testing.
    """

    def __init__(self):
        # A short silent μ-law frame (8000Hz, 20ms = 160 bytes)
        self._silent_frame = b"\xff" * 160

    async def synthesize(self, text: str) -> AsyncIterator[bytes]:
        """Yield silent audio chunks as placeholder."""
        # Yield enough frames to simulate speaking duration
        words = len(text.split())
        frame_count = max(2, words)  # ~20ms per frame, ~5 words/sec
        for _ in range(frame_count):
            yield self._silent_frame

    async def close(self):
        pass