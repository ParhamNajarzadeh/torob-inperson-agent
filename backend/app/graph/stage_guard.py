"""
Deterministic Stage Guards, PostToolUse Pruning, and Anchored Context Compaction (Chapters 9, 10, 12 Quera).
"""
from typing import Dict, Any, List
from backend.app.graph.state import (
    ProductCandidate,
    StoreOfferCandidate,
    GenUIComponentPayload,
    TorobShoppingState
)

MAX_FALLBACK_RETRIES = 3
MAX_MESSAGES_BEFORE_COMPACTION = 40


def validate_stage_transition(state: TorobShoppingState) -> Dict[str, Any]:
    """Prompt Chaining Gate: validates Pydantic schemas and enforces hard loop caps."""
    validated_products = [ProductCandidate(**p).model_dump() for p in state.get("product_candidates", [])]
    validated_stores = [StoreOfferCandidate(**s).model_dump() for s in state.get("store_candidates", [])]
    validated_ui = [GenUIComponentPayload(**c).model_dump() for c in state.get("active_ui_components", [])]

    retry_count = min(MAX_FALLBACK_RETRIES, int(state.get("fallback_retry_count", 0)))
    return {
        "product_candidates": validated_products,
        "store_candidates": validated_stores,
        "active_ui_components": validated_ui,
        "fallback_retry_count": retry_count
    }


def anchored_context_compaction(state: TorobShoppingState) -> Dict[str, Any]:
    """
    Chapter 10 Anchored Structured Compaction:
    Compacts old messages when history exceeds 40 messages or on phase change while strictly preserving
    Pinned State Anchors (user_location, budget_range_toman, active_filters, selected_product_id, rejected_shop_ids).
    """
    msgs = state.get("messages", [])
    if len(msgs) <= MAX_MESSAGES_BEFORE_COMPACTION:
        return {}
    kept_messages = msgs[-6:]
    return {
        "messages": kept_messages,
        "user_location": state["user_location"],
        "budget_range_toman": state["budget_range_toman"],
        "active_filters": state["active_filters"],
        "selected_product_id": state.get("selected_product_id"),
        "rejected_shop_ids": state.get("rejected_shop_ids", [])
    }
