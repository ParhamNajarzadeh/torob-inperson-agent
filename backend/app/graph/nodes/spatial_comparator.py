"""LangGraph Node: spatial_comparator_node (step_2_3_spatial_comparison)."""
from typing import Dict, Any
from backend.app.graph.state import TorobShoppingState


def spatial_comparator_node(state: TorobShoppingState) -> Dict[str, Any]:
    return {"current_step": "step_2_3_spatial_comparison"}
