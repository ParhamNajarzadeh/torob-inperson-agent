"""LangGraph Node: tehran_bourse_fallback_node (step_2_bourse_fallback)."""
from typing import Dict, Any
from backend.app.graph.state import TorobShoppingState


def tehran_bourse_fallback_node(state: TorobShoppingState) -> Dict[str, Any]:
    return {"current_step": "step_2_bourse_fallback"}
