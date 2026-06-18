"""System prompt compiler — replaces placeholders with client data."""

from __future__ import annotations

from pathlib import Path
from string import Template

from knowledge_base.client_config import ClientConfig

# Path to the default system prompt template
TEMPLATE_PATH = Path(__file__).resolve().parent.parent / "templates" / "default_system_prompt.md"


def compile_system_prompt(client_config: ClientConfig) -> str:
    """Compile the system prompt template with client-specific data.

    Reads the Jinja-like template containing ``{{placeholders}}`` and
    replaces them with values from the client configuration.

    Parameters
    ----------
    client_config : ClientConfig
        The client's knowledge base configuration.

    Returns
    -------
    str
        The fully compiled system prompt ready for the LLM.
    """
    if not TEMPLATE_PATH.exists():
        return _build_prompt_inline(client_config)

    with open(TEMPLATE_PATH) as f:
        template_str = f.read()

    # Use string.Template for placeholder replacement
    # Convert {{key}} → $key for string.Template
    template_str = template_str.replace("{{", "${").replace("}}", "}")

    # Flatten nested keys like contact_details.phone → contact_details_phone
    flat_data = _flatten_dict(client_config.to_dict())

    template = Template(template_str)
    try:
        result = template.safe_substitute(**flat_data)
    except KeyError as e:
        # Fall back: replace what we can
        result = template.safe_substitute(**flat_data)

    return result


def _flatten_dict(d: dict, parent_key: str = "", sep: str = "_") -> dict:
    """Flatten a nested dict for string.Template substitution.

    ``{"contact": {"phone": "123"}}`` → ``{"contact_phone": "123"}``
    """
    items: dict = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(_flatten_dict(v, new_key, sep=sep))
        else:
            items[new_key] = str(v) if v is not None else ""
    return items


def _build_prompt_inline(client_config: ClientConfig) -> str:
    """Build a minimal system prompt without reading the template file."""
    c = client_config.to_dict()
    return (
        f"You are the professional, friendly AI Voice Receptionist for {c['company_name']}. "
        f"Your goal is to represent the company flawlessly, answer caller inquiries "
        f"using only the provided knowledge base, capture complete lead details, "
        f"and handle booking or callback requests.\n\n"
        f"Tone: {c['tone_of_voice']}\n\n"
        f"Company Info:\n"
        f"- Industry: {c['industry']}\n"
        f"- Location: {c['location']}\n"
        f"- Hours: {c['opening_hours']}\n"
        f"- Services: {c['services']}\n"
        f"- Pricing: {c['prices_or_price_rules']}\n"
        f"- Booking: {c['booking_rules']}\n"
        f"- Staff: {c['staff_members']}\n"
        f"- FAQs: {c['faqs']}\n\n"
        f"Follow the 9-step call flow: Greet → Understand → Answer from Knowledge → "
        f"Ask missing questions → Collect lead details → Offer booking/callback → "
        f"Confirm summary → Close politely → Send summary.\n\n"
        f"Speak in 1-2 sentence turns. Ask one question at a time. "
        f"Never invent prices or availability. "
        f"If missing info, offer a callback. "
        f"Escalate if caller is angry, confused, or has an emergency."
    )