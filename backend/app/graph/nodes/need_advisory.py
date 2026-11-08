"""LangGraph Node: need_advisory_node (step_1_advisory)."""
from typing import Dict, Any
from backend.app.graph.state import TorobShoppingState


def need_advisory_node(state: TorobShoppingState) -> Dict[str, Any]:
    return {"current_step": "step_1_advisory"}
