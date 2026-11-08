"""
AI Governance & Security Guards (Chapter 16 Quera & 9-Second Pacto Lesson):
1. Breaks Simon Willison's Lethal Trifecta by wrapping external web/Instagram text in <untrusted_content>
   and parsing outputs strictly into numeric/boolean Pydantic fields.
2. Masks PII (phone numbers, national IDs) before external logging.
3. Enforces Virtual User Identity (service_account:torob-inperson-agent-v1) and Kill-Switch state.
"""
import os
import re
from typing import Dict, Any
from pydantic import BaseModel, ConfigDict

AGENT_RETIRED_KILL_SWITCH = False


class SanitizedWebStoreExtraction(BaseModel):
    model_config = ConfigDict(extra="forbid")
    in_stock: bool
    live_price_toman: int
    has_torob_pay: bool
    floor_number: int


def wrap_untrusted_external_content(raw_html_or_bio: str) -> str:
    """Strips script tags and wraps external store content in <untrusted_content> tags."""
    cleaned = re.sub(r"<script.*?>.*?</script>", "", raw_html_or_bio or "", flags=re.DOTALL | re.IGNORECASE)
    return f"<untrusted_content>\n{cleaned[:1200]}\n</untrusted_content>"


def mask_pii(text: str) -> str:
    """Masks Iranian mobile numbers before writing to trace logs."""
    return re.sub(r"\b(09\d{2})\d{3}(\d{4})\b", r"\1***\2", text or "")


def check_agent_active() -> Dict[str, Any]:
    if AGENT_RETIRED_KILL_SWITCH:
        raise RuntimeError("Agent is retired via Governance Kill-Switch (/admin/agent/retire).")
    return {
        "virtual_user_id": os.getenv("AGENT_VIRTUAL_USER_ID", "service_account:torob-inperson-agent-v1"),
        "token_expires_at": os.getenv("AGENT_TOKEN_EXPIRES_AT", "2026-11-01T23:59:59+03:30"),
        "retired": AGENT_RETIRED_KILL_SWITCH
    }
