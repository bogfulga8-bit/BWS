"""Webhook notification — dispatches structured JSON to CRM endpoints.

Phase 1: stub. Phase 3: full implementation with retry logic.
"""

from __future__ import annotations

import json
import logging
from typing import Optional

import httpx

from leads.models import CallSummary

logger = logging.getLogger(__name__)


async def dispatch_webhook(
    summary: CallSummary,
    webhook_url: str,
    secret: Optional[str] = None,
) -> bool:
    """POST a structured JSON payload to the client's CRM webhook.

    Parameters
    ----------
    summary : CallSummary
        The structured call summary.
    webhook_url : str
        The target webhook URL (Zapier, Make, CRM).
    secret : str | None
        Optional HMAC secret to sign the payload.

    Returns
    -------
    bool
        True if the webhook responded 2xx.
    """
    payload = {
        "event": "call.completed",
        "call_id": summary.call_id,
        "timestamp": summary.timestamp.isoformat(),
        "duration_seconds": summary.duration_seconds,
        "lead": summary.lead.model_dump(mode="json"),
        "transcript": summary.transcript,
    }

    headers = {"Content-Type": "application/json"}
    if secret:
        headers["X-Webhook-Signature"] = secret

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                webhook_url,
                json=payload,
                headers=headers,
                timeout=10.0,
            )
            response.raise_for_status()
            logger.info(f"Webhook dispatched — status={response.status_code}")
            return True
        except Exception as e:
            logger.error(f"Webhook failed: {e}")
            return False