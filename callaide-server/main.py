"""CallAide — FastAPI Application Entry Point

Serves the Twilio telephony webhooks and WebSocket endpoint for
Twilio Media Streams. The audio pipeline (STT→LLM→TTS) runs
inside the WebSocket handler.
"""

from __future__ import annotations

import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings

# ── App factory ──────────────────────────────────────────────

def create_app() -> FastAPI:
    """Build and return the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title="CallAide — AI Voice Receptionist",
        version="0.1.0",
        docs_url="/docs",
    )

    # CORS — allow Twilio webhooks and frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Register routers ────────────────────────────────────
    from telephony.router import router as telephony_router
    app.include_router(telephony_router, prefix="/twilio")

    # ── Health check ────────────────────────────────────────
    @app.get("/health")
    async def health():
        return {"status": "ok", "service": "callaide-server"}

    # ── Startup / Shutdown ──────────────────────────────────
    @app.on_event("startup")
    async def startup():
        logging.info("CallAide server starting up …")

    @app.on_event("shutdown")
    async def shutdown():
        logging.info("CallAide server shutting down …")

    return app


# ── Entry point ──────────────────────────────────────────────

app = create_app()

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level,
        reload=True,
    )