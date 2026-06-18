"""Telephony — Twilio webhook handlers."""

from __future__ import annotations

import logging

from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse, HTMLResponse
from twilio.request_validator import RequestValidator
from twilio.twiml.voice_response import VoiceResponse, Connect, Stream

from config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter()

# ── WebSocket endpoint that Media Streams connects to ────────

MEDIA_STREAM_URL = "/twilio/media-stream"  # relative WS path on this server


@router.post("/incoming")
async def handle_incoming_call(request: Request):
    """Entry point for an inbound call from Twilio.

    Returns TwiML that connects the call to a bidirectional
    Media Stream WebSocket.
    """
    # (Optional) Validate Twilio signature
    settings = get_settings()
    validator = RequestValidator(settings.twilio_auth_token)
    form_data = await request.form()
    signature = request.headers.get("X-Twilio-Signature", "")

    if settings.twilio_auth_token and signature:
        url = str(request.url)
        is_valid = validator.validate(url, dict(form_data), signature)
        if not is_valid:
            logger.warning("Invalid Twilio signature — rejecting")
            return PlainTextResponse("Invalid signature", status_code=403)

    # Build the TwiML response with a Media Stream
    call_sid = form_data.get("CallSid", "unknown")
    from_number = form_data.get("From", "unknown")
    logger.info(f"Inbound call — SID={call_sid} From={from_number}")

    resp = VoiceResponse()

    # Optional: say a greeting while the WS connects
    # (The AI voice handles all speaking, so we connect immediately)
    connect = Connect()
    stream = Stream(url=f"wss://{request.url.hostname}{MEDIA_STREAM_URL}")
    stream.parameter(name="callSid", value=call_sid)
    stream.parameter(name="fromNumber", value=from_number)
    connect.append(stream)
    resp.append(connect)

    return HTMLResponse(str(resp), media_type="application/xml")


@router.post("/status")
async def handle_call_status(request: Request):
    """Receives call status callbacks from Twilio.

    Triggered when a call ends, is answered, or fails.
    Used to trigger post-call summary generation.
    """
    form_data = await request.form()
    call_sid = form_data.get("CallSid", "unknown")
    call_status = form_data.get("CallStatus", "unknown")
    logger.info(f"Call status — SID={call_sid} Status={call_status}")

    # TODO (Phase 3): trigger summary generation worker here
    return PlainTextResponse("OK")