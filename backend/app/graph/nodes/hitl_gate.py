"""LangGraph Node: hitl_approval_node (step_4_hitl_gate)."""
from typing import Dict, Any
from backend.app.graph.state import TorobShoppingState


def hitl_approval_node(state: TorobShoppingState) -> Dict[str, Any]:
    return {"current_step": "step_4_hitl_gate"}
