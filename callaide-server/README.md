# CallAide Server

A 24/7 AI Voice Receptionist — receives phone calls via Twilio, processes audio through an STT→LLM→TTS pipeline, captures lead data, and delivers instant call summaries.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Fill in your API keys
uvicorn main:app --reload --port 8000
```

## Architecture

See `/home/team/shared/system-architecture.md` for the full architecture design.