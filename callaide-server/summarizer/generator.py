"""Call summary generator — produces structured summaries from transcript data.

Phase 1: stub implementation. Phase 3: full implementation with
SMS, Email, and Webhook delivery.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from leads.models import LeadData, CallSummary

logger = logging.getLogger(__name__)


def generate_summary(
    lead: LeadData,
    transcript: list[dict],
    duration_seconds: int,
) -> CallSummary:
    """Generate a structured call summary from lead data and transcript.

    Parameters
    ----------
    lead : LeadData
        Captured lead information.
    transcript : list[dict]
        Conversation turns (role + content).
    duration_seconds : int
        Duration of the call.

    Returns
    -------
    CallSummary
        Structured summary ready for notification delivery.
    """
    summary = CallSummary(
        call_id=lead.call_id,
        timestamp=lead.timestamp,
        duration_seconds=duration_seconds,
        transcript=transcript,
        lead=lead,
    )
    logger.info(f"Summary generated — call_id={lead.call_id} duration={duration_seconds}s")
    return summary