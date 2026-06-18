"""Lead data models — Pydantic schemas matching lead-data-fields.md."""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class ServiceAddress(BaseModel):
    street_address: Optional[str] = None
    city: Optional[str] = None
    state_province: Optional[str] = None
    postal_code: Optional[str] = None


class SchedulingPreference(BaseModel):
    preferred_date: Optional[date] = None
    preferred_time_slot: Optional[str] = None  # Morning, Afternoon, Evening, Anytime


class LeadData(BaseModel):
    """Structured lead captured during a call.

    Matches the schema defined in lead-data-fields.md.
    """

    # Call metadata
    call_id: str = Field(description="Unique UUID for the call session")
    timestamp: datetime = Field(description="ISO 8601 timestamp when call ended")
    caller_phone: str = Field(description="E.164 formatted phone number")

    # Caller info
    caller_name_first: str = Field(min_length=1, description="Caller's first name")
    caller_name_last: Optional[str] = Field(None, description="Caller's last name")
    caller_email: Optional[str] = Field(None, description="Caller's email address")

    # Service address (for trades/home services)
    service_address: Optional[ServiceAddress] = None

    # Customer type
    is_existing_customer: bool = Field(
        default=False,
        description="True if caller has prior relationship with business",
    )

    # Service details
    service_category: str = Field(description="Broad classification of intent")
    caller_notes: str = Field(description="Summary of caller's request / issue")

    # Scheduling
    scheduling_preference: Optional[SchedulingPreference] = None

    # Flags
    is_emergency: bool = Field(default=False)
    escalated_to_human: bool = Field(default=False)


class CallSummary(BaseModel):
    """Full call summary delivered to the business owner."""

    call_id: str
    timestamp: datetime
    duration_seconds: int
    transcript: list[dict] = Field(default_factory=list)

    # Lead data
    lead: LeadData

    # Notification delivery tracking
    sms_sent: bool = False
    email_sent: bool = False
    webhook_sent: bool = False