"""SMS notification — sends urgent lead alerts via Twilio.

Phase 1: stub. Phase 3: full implementation.
"""

from __future__ import annotations

import logging

from leads.models import CallSummary

logger = logging.getLogger(__name__)


async def send_sms_notification(summary: CallSummary, to_number: str) -> bool:
    """Send an SMS notification to the business owner.

    Parameters
    ----------
    summary : CallSummary
        The structured call summary.
    to_number : str
        Business owner's phone number (E.164).

    Returns
    -------
    bool
        True if sent successfully.
    """
    lead = summary.lead
    message = (
        f"📞 CallAide Alert — New Lead!\n"
        f"👤 {lead.caller_name_first} {lead.caller_name_last or ''}\n"
        f"📱 {lead.caller_phone}\n"
        f"🛠️ {lead.service_category}: {lead.caller_notes[:80]}\n"
        f"📅 {lead.scheduling_preference.preferred_date or 'TBD'}\n"
        f"⏱️ Duration: {summary.duration_seconds}s"
    )

    # TODO (Phase 3): Use Twilio SMS API
    logger.info(f"SMS notification (stub): to={to_number} msg='{message[:60]}…'")
    return True