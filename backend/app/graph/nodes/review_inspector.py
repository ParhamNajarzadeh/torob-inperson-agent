"""LangGraph Node: product_review_inspector_node (step_1_review)."""
from typing import Dict, Any
from backend.app.graph.state import TorobShoppingState


def product_review_inspector_node(state: TorobShoppingState) -> Dict[str, Any]:
    return {"current_step": "step_1_review"}
