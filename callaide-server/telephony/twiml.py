"""TwiML response builders for Twilio telephony."""

from __future__ import annotations

from twilio.twiml.voice_response import (
    VoiceResponse,
    Connect,
    Stream,
    Dial,
    Say,
    Gather,
)


def build_media_stream_twiml(
    websocket_url: str,
    call_sid: str,
    from_number: str = "",
) -> str:
    """Build a TwiML response that connects a call to a Media Stream.

    Parameters
    ----------
    websocket_url : str
        The full WS(S) URL of the Media Stream endpoint
        (e.g. ``wss://example.com/twilio/media-stream``).
    call_sid : str
        Call SID to forward as a parameter.
    from_number : str
        Caller's phone number to forward as a parameter.

    Returns
    -------
    str
        The rendered TwiML string.
    """
    resp = VoiceResponse()
    connect = Connect()
    stream = Stream(url=websocket_url)
    stream.parameter(name="callSid", value=call_sid)
    stream.parameter(name="fromNumber", value=from_number)
    connect.append(stream)
    resp.append(connect)
    return str(resp)


def build_transfer_twiml(transfer_number: str, message: str = "") -> str:
    """Build a TwiML response that warm-transfers to a human.

    Parameters
    ----------
    transfer_number : str
        Phone number to dial (E.164 format).
    message : str
        Optional message to say before dialing.

    Returns
    -------
    str
        The rendered TwiML string.
    """
    resp = VoiceResponse()
    if message:
        resp.say(message, voice="alice")
    resp.dial(transfer_number)
    return str(resp)


def build_hangup_twiml() -> str:
    """Build a simple TwiML response that hangs up."""
    resp = VoiceResponse()
    resp.hangup()
    return str(resp)