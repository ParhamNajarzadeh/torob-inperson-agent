"""LangGraph Node: outreach_and_indoor_nav_node (step_4_outreach_and_nav)."""
from typing import Dict, Any
from backend.app.graph.state import TorobShoppingState


def outreach_and_indoor_nav_node(state: TorobShoppingState) -> Dict[str, Any]:
    return {"current_step": "step_4_outreach_and_nav"}
