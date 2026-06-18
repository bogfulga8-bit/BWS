"""Client configuration — loading and caching per-client knowledge bases."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Default client config path (development fallback)
DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "templates" / "default_client_config.json"


class ClientConfig:
    """Holds a single client's configuration for the AI receptionist.

    All fields map to the ``{{placeholders}}`` in the system prompt.
    """

    def __init__(self, data: dict):
        self.raw = data

    @classmethod
    def from_dict(cls, data: dict) -> "ClientConfig":
        return cls(data)

    @classmethod
    def from_json(cls, path: str | Path) -> "ClientConfig":
        with open(path) as f:
            data = json.load(f)
        return cls(data)

    @classmethod
    def default(cls) -> "ClientConfig":
        """Return a development/default client config."""
        return cls({
            "company_name": "Your Business Name",
            "industry": "General Services",
            "location": "Your City, State",
            "areas_served": "Your local area",
            "opening_hours": "Monday–Friday 9am–5pm",
            "contact_details": {
                "phone": "+1-555-0000",
                "transfer_phone": "+1-555-0001",
                "email": "info@example.com",
            },
            "services": "General professional services",
            "prices_or_price_rules": "Please contact us for a custom quote",
            "booking_rules": "Collect caller's preferred time and submit as a request",
            "staff_members": "Our professional team",
            "faqs": "We are licensed and insured. We accept major credit cards.",
            "emergency_rules": "Call 911 for life-threatening emergencies",
            "when_to_transfer_to_human": "Angry callers, emergency situations, complex requests",
            "tone_of_voice": "Warm, professional, helpful, polite, and confident",
        })

    def to_dict(self) -> dict:
        return self.raw


class ClientConfigStore:
    """In-memory store for client configurations.

    In production this would load from a database. For Phase 1
    it provides a simple dict-based cache.
    """

    def __init__(self):
        self._cache: dict[str, ClientConfig] = {}

    def get(self, client_id: str) -> Optional[ClientConfig]:
        return self._cache.get(client_id)

    def set(self, client_id: str, config: ClientConfig):
        self._cache[client_id] = config

    def get_or_default(self, client_id: str) -> ClientConfig:
        config = self.get(client_id)
        if config is None:
            logger.warning(f"No config for client '{client_id}' — using default")
            config = ClientConfig.default()
            self.set(client_id, config)
        return config