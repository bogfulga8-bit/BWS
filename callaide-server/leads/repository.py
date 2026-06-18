"""Lead repository — CRUD operations for lead data storage.

In Phase 1, uses a simple in-memory store. In later phases,
migrates to the team-db SQLite or PostgreSQL.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from leads.models import LeadData, CallSummary

logger = logging.getLogger(__name__)


class LeadRepository:
    """In-memory lead store for development.

    Phase 1: simple dict-based store.
    Phase 3+: migrate to team-db SQLite or PostgreSQL.
    """

    def __init__(self):
        self._leads: dict[str, LeadData] = {}
        self._summaries: dict[str, CallSummary] = {}

    def save_lead(self, lead: LeadData) -> str:
        """Store a lead record and return its call_id."""
        self._leads[lead.call_id] = lead
        logger.info(f"Lead saved — call_id={lead.call_id} caller={lead.caller_name_first}")
        return lead.call_id

    def get_lead(self, call_id: str) -> Optional[LeadData]:
        return self._leads.get(call_id)

    def save_summary(self, summary: CallSummary) -> str:
        self._summaries[summary.call_id] = summary
        logger.info(f"Summary saved — call_id={summary.call_id}")
        return summary.call_id

    def get_summary(self, call_id: str) -> Optional[CallSummary]:
        return self._summaries.get(call_id)

    def create_lead_from_call(
        self,
        caller_phone: str,
        caller_name_first: str = "",
        service_category: str = "General Inquiry",
        caller_notes: str = "",
    ) -> LeadData:
        """Create a LeadData from minimal call info.

        Returns a partially filled lead — will be enriched
        as the conversation progresses.
        """
        return LeadData(
            call_id=str(uuid4()),
            timestamp=datetime.now(timezone.utc),
            caller_phone=caller_phone,
            caller_name_first=caller_name_first or "Unknown",
            service_category=service_category,
            caller_notes=caller_notes,
            is_existing_customer=False,
            is_emergency=False,
            escalated_to_human=False,
        )

    def count(self) -> int:
        return len(self._leads)


# Singleton for development
default_repo = LeadRepository()