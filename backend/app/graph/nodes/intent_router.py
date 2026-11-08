"""LangGraph Node: intent_router_node (step_0_routing)."""
from typing import Dict, Any
from backend.app.graph.state import TorobShoppingState


def intent_router_node(state: TorobShoppingState) -> Dict[str, Any]:
    return {"current_step": "step_0_routing"}
