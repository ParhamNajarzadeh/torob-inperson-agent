"""Append-only Trace Memory Logger (memory/trace/trace.jsonl) + Langfuse Compatibility."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any
from backend.app.governance.security_guards import mask_pii


def append_trace_event(event_type: str, thread_id: str, payload: Dict[str, Any]) -> None:
    trace_path = Path(os.getenv("TRACE_LOG_PATH", "./memory/trace/trace.jsonl"))
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "virtual_agent_id": os.getenv("AGENT_VIRTUAL_USER_ID", "service_account:torob-inperson-agent-v1"),
        "thread_id": thread_id,
        "event_type": event_type,
        "payload_masked": json.loads(mask_pii(json.dumps(payload, ensure_ascii=False)))
    }
    with trace_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
