"""CallAide — Application Configuration

Loads environment variables and provides typed access to
all configuration values needed by the server.
"""

from __future__ import annotations

import os
from pathlib import Path
from functools import lru_cache

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env from the project root
env_path = Path(__file__).resolve().parent / ".env"
if env_path.exists():
    load_dotenv(env_path)


class Settings(BaseSettings):
    # ── Server ──────────────────────────────────────────────
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "info"

    # ── Twilio ──────────────────────────────────────────────
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_phone_number: str = ""

    # ── Deepgram (STT) ──────────────────────────────────────
    deepgram_api_key: str = ""

    # ── LLM Provider ────────────────────────────────────────
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    llm_provider: str = "openai"          # "openai" | "anthropic"
    llm_model_live: str = "gpt-4o-mini"   # fast model for live calls
    llm_model_setup: str = "gpt-4o"       # stronger model for setup/testing

    # ── TTS ─────────────────────────────────────────────────
    elevenlabs_api_key: str = ""
    cartesia_api_key: str = ""
    tts_provider: str = "elevenlabs"      # "elevenlabs" | "cartesia"
    tts_voice_id: str = "21m00Tcm4TlvDq8ikWAM"  # ElevenLabs Rachel

    # ── Database ────────────────────────────────────────────
    database_url: str = "sqlite:///./callaide.db"

    # ── Notifications ───────────────────────────────────────
    sendgrid_api_key: str = ""
    from_email: str = "noreply@callaide.com"

    # ── Webhook ─────────────────────────────────────────────
    webhook_secret: str = ""

    model_config = {"env_file": ".env", "case_sensitive": False}


@lru_cache()
def get_settings() -> Settings:
    """Return a cached singleton Settings object."""
    return Settings()