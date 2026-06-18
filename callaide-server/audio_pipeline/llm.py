"""LLM — Conversation manager for the AI receptionist.

Handles system prompt compilation, conversation history, and
response generation through OpenAI or Anthropic APIs.
"""

from __future__ import annotations

import logging
from typing import AsyncIterator

from openai import AsyncOpenAI
from anthropic import AsyncAnthropic

logger = logging.getLogger(__name__)


class LLMConversation:
    """Manages the conversation with the LLM for a single call session.

    Maintains message history and generates responses using
    the compiled system prompt for the client's business.
    """

    def __init__(
        self,
        provider: str = "openai",
        model_live: str = "gpt-4o-mini",
        model_setup: str = "gpt-4o",
        openai_api_key: str = "",
        anthropic_api_key: str = "",
    ):
        self.provider = provider
        self.model_live = model_live
        self.model_setup = model_setup
        self._messages: list[dict] = []

        # Initialize clients
        self._openai = AsyncOpenAI(api_key=openai_api_key) if openai_api_key else None
        self._anthropic = AsyncAnthropic(api_key=anthropic_api_key) if anthropic_api_key else None

    def set_system_prompt(self, prompt: str):
        """Set the compiled system prompt for this call session."""
        self._messages = [{"role": "system", "content": prompt}]

    def add_user_message(self, text: str):
        """Add a user (caller) message to the history."""
        self._messages.append({"role": "user", "content": text})

    def add_assistant_message(self, text: str):
        """Add an assistant (AI) message to the history."""
        self._messages.append({"role": "assistant", "content": text})

    @property
    def message_count(self) -> int:
        return len(self._messages) - 1  # exclude system prompt

    async def generate_response(self, is_setup: bool = False) -> str:
        """Generate a response to the current conversation.

        Parameters
        ----------
        is_setup : bool
            If True, uses the stronger setup model for testing/onboarding.

        Returns
        -------
        str
            The model's response text.
        """
        model = self.model_setup if is_setup else self.model_live

        if self.provider == "openai" and self._openai:
            return await self._generate_openai(model)
        elif self.provider == "anthropic" and self._anthropic:
            return await self._generate_anthropic(model)
        else:
            return self._generate_mock()

    async def _generate_openai(self, model: str) -> str:
        """Generate a response using OpenAI."""
        response = await self._openai.chat.completions.create(
            model=model,
            messages=self._messages,
            temperature=0.3,
            max_tokens=200,
            stream=False,
        )
        text = response.choices[0].message.content or ""
        self.add_assistant_message(text)
        logger.debug(f"LLM (OpenAI {model}): {text[:80]}…")
        return text

    async def _generate_anthropic(self, model: str) -> str:
        """Generate a response using Anthropic Claude."""
        # Convert OpenAI-style messages to Anthropic format
        system_msg = ""
        anthropic_messages = []
        for msg in self._messages:
            if msg["role"] == "system":
                system_msg = msg["content"]
            else:
                anthropic_messages.append({
                    "role": msg["role"],
                    "content": msg["content"],
                })

        response = await self._anthropic.messages.create(
            model=model,
            system=system_msg,
            messages=anthropic_messages,
            temperature=0.3,
            max_tokens=200,
        )
        text = response.content[0].text if response.content else ""
        self.add_assistant_message(text)
        logger.debug(f"LLM (Anthropic {model}): {text[:80]}…")
        return text

    def _generate_mock(self) -> str:
        """Generate a mock response for development without API keys.

        Follows the 9-step call flow logic in a simplified way.
        """
        msg_count = self.message_count
        if msg_count <= 1:
            text = (
                "Thanks for calling! I'd be happy to help you with that. "
                "Could I start with your name, please?"
            )
        elif msg_count <= 2:
            text = (
                "Thank you! And what's the best phone number "
                "to reach you at?"
            )
        elif msg_count <= 3:
            text = (
                "Great, thanks! And what service are you looking for today?"
            )
        elif msg_count <= 4:
            text = (
                "Perfect! Do you have a preferred date and time "
                "for that service?"
            )
        else:
            text = (
                "Excellent! I've logged all your details. "
                "Our team will review and confirm your appointment "
                "shortly. Thank you for calling!"
            )

        self.add_assistant_message(text)
        logger.debug(f"LLM (mock): {text[:80]}…")
        return text

    def get_history(self) -> list[dict]:
        """Return the full conversation history (for transcript storage)."""
        return self._messages.copy()

    def reset(self):
        """Reset the conversation for a new call."""
        self._messages = []