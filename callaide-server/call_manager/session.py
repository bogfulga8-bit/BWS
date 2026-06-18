"""Call session — per-call state management.

Tracks the state of a single phone call: SIDs, transcript
fragments, and any structured data extracted so far.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Callable, Awaitable, Optional

logger = logging.getLogger(__name__)

OnTranscript = Callable[[str, bool], Awaitable[None]]


class CallSession:
    """Holds state for one phone call session.

    Attributes
    ----------
    call_sid : str | None
        Twilio Call SID.
    stream_sid : str | None
        Twilio Media Stream SID.
    start_time : datetime | None
        When the call started.
    transcript_fragments : list[dict]
        In-progress transcript pieces from STT.
    """

    def __init__(self):
        self.call_sid: Optional[str] = None
        self.stream_sid: Optional[str] = None
        self.start_time: Optional[datetime] = None
        self.transcript_fragments: list[dict] = []
        self._on_transcript: Optional[OnTranscript] = None

    def set_call_sid(self, sid: str):
        self.call_sid = sid
        self.start_time = datetime.now(timezone.utc)

    def set_stream_sid(self, sid: str):
        self.stream_sid = sid

    def set_on_transcript(self, callback: OnTranscript):
        """Set the callback invoked when a transcript arrives."""
        self._on_transcript = callback

    async def on_transcript(self, text: str, is_final: bool):
        """Callback for STT transcript events.

        Records the transcript and forwards to the pipeline.
        """
        entry = {
            "text": text,
            "is_final": is_final,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.transcript_fragments.append(entry)

        if is_final:
            logger.info(f"Final transcript: {text}")

        if self._on_transcript:
            await self._on_transcript(text, is_final)

    def get_transcript_summary(self) -> str:
        """Return a one-line summary of the call transcript."""
        finals = [f["text"] for f in self.transcript_fragments if f["is_final"]]
        if not finals:
            return "(no transcript)"
        return " | ".join(finals[:3])  # first 3 utterances

    def get_duration_seconds(self) -> float:
        """Return call duration in seconds (or 0 if not started)."""
        if self.start_time:
            return (datetime.now(timezone.utc) - self.start_time).total_seconds()
        return 0.0