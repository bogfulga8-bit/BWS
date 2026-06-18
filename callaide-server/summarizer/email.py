"""Email notification — sends detailed lead records via SendGrid.

Phase 1: stub. Phase 3: full implementation.
"""

from __future__ import annotations

import logging

from leads.models import CallSummary

logger = logging.getLogger(__name__)


async def send_email_notification(summary: CallSummary, to_email: str) -> bool:
    """Send a detailed email notification to the business owner.

    Parameters
    ----------
    summary : CallSummary
        The structured call summary.
    to_email : str
        Business owner's email address.

    Returns
    -------
    bool
        True if sent successfully.
    """
    lead = summary.lead
    subject = (
        f"📞 CallAide: New Lead — "
        f"{lead.caller_name_first} {lead.caller_name_last or ''} — "
        f"{lead.service_category}"
    )

    # TODO (Phase 3): Build HTML email from call-summary-format.md template
    logger.info(f"Email notification (stub): to={to_email} subject='{subject}'")
    return True