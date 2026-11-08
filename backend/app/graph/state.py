"""Strict Pydantic v2 Contracts & TorobShoppingState Schema (Section 7)."""
from typing import TypedDict, List, Dict, Optional, Literal, Annotated, Any
from pydantic import BaseModel, Field, ConfigDict
from langgraph.graph.message import add_messages


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class SystemOneDecisionTrace(StrictModel):
    provider: Literal["metis_jev", "local_mizan_4b", "local_kev", "local_laya"]
    latency_ms: float
    intent_choice: str
    intent_confidence: float
    nouls: Dict[str, float]
    scores: Dict[str, float]


class ProductReviewSummary(StrictModel):
    product_id: str
    overall_verdict: str
    value_for_money_score: float = Field(ge=0.0, le=10.0)
    pros: List[str]
    cons: List[str]
    price_dispersion_alert: Optional[str] = None
    authenticity_and_unit_trap_warning: Optional[str] = None
    in_store_inspection_checklist: List[str]
    external_sources_cited: List[str]


class ProductCandidate(StrictModel):
    product_id: str
    persian_title: str
    category_name: str
    extracted_brand: Optional[str]
    extracted_model: Optional[str]
    clean_offer_count: int
    distinct_shop_count: int
    min_clean_price_toman: Optional[int]
    median_clean_price_toman: Optional[int]
    max_clean_price_toman: Optional[int]
    hedonic_fair_price_estimate: Optional[int]
    key_specs: Dict[str, str]
    image_urls: List[str]
    match_reason_badge: str
    review_summary: Optional[ProductReviewSummary] = None


class StoreOfferCandidate(StrictModel):
    offer_id: str
    product_id: str
    shop_id: str
    shop_name: str
    is_real_entity: bool  # True for the 112 shops with real website_url (90) or instagram (22)
    seller_title: str     # Seller's specific item title (pack/roll/warranty details)
    store_photo_or_product_image_url: Optional[str]
    unit_mismatch_flag: bool
    suspected_rial_toman_flag: bool
    registered_price_toman: Optional[int]
    last_price_changed_at: Optional[str]
    price_age_days: Optional[float]
    freshness_tier: Literal["fresh_under_7d", "moderate_7_to_30d", "stale_over_30d", "unpriced"]
    probabilistic_stock_confidence_pct: int = Field(ge=0, le=100)  # Google Pointy-style confidence
    crowdsourced_last_checkin_note: Optional[str] = None           # Waze-style shopper check-in
    warranty_tier: Literal["corporate", "local_shop", "none_or_unknown"]
    warranty_details: Optional[Dict[str, Any]]
    shop_median_price_ratio: Optional[float]  # Store Price Tier Badge (<0.90 cheap, >1.30 expensive)
    is_single_category_specialist: bool
    location_label: str
    lat: float
    lon: float
    distance_km: float
    passage_indoor_info: Dict[str, Optional[str]]  # passage_name, floor, corridor, unit_number
    weekly_hours_status: Literal["open_at_visit", "closed_at_visit", "unknown_needs_inquiry"]
    today_hours_label: str
    payment_capabilities: List[str]  # torob_pay, snapp_pay, digi_pay, tara, azki_vam
    supports_fast_delivery: Optional[bool]
    contact_channels: Dict[str, Optional[str]]  # phone, website_url, instagram
    verification_state: Literal[
        "unverified_dataset_only",
        "pending_hitl_approval",
        "verified_available_live",
        "verified_by_1tap_seller_webhook",
        "verified_web_instagram_live",
        "rejected_out_of_stock",
        "rejected_closed_or_no_answer"
    ]
    verified_live_price_toman: Optional[int] = None
    verification_evidence_note: Optional[str] = None
    composite_store_score: float
    why_recommended_badge: str


class TehranBourseRecommendation(StrictModel):
    bourse_name: str
    neighborhood: str
    center_lat: float
    center_lon: float
    bounding_polygon: List[List[float]]
    specialty_description: str
    famous_passages: List[str]
    nearest_metro_and_brt: str
    best_visit_hours: str
    in_person_buying_tips: List[str]
    directory_shops_in_bourse: List[Dict[str, Any]]  # From the 2,684 zero-offer shops in shops.csv


class GenUIComponentPayload(StrictModel):
    component_id: str
    component_type: Literal[
        "SmartRequirementForm",
        "ProductComparisonCarousel",
        "ProductReviewAndInspectionCard",
        "InteractiveTehranMapAndFilterBar",
        "StoreComparisonMatrix",
        "RealStoreWebInstagramLiveCard",
        "OutreachApprovalDialog",
        "LiveVerificationTracker",
        "AlternativeSwitchBanner",
        "TehranBourseLocationWidget",
        "PassageIndoorNavigationCard"
    ]
    props: Dict[str, Any]


class TorobShoppingState(TypedDict):
    # 1. Conversation & System-1 Routing
    messages: Annotated[list, add_messages]
    thread_id: str
    user_id: str
    current_step: str
    last_system_one_trace: Optional[Dict[str, Any]]
    active_skills_loaded: List[str]

    # 2. Pinned State Anchors (Never dropped during Context Compaction)
    user_location: Dict[str, Any]         # {"lat": 35.701, "lon": 51.409, "label": "میدان ولیعصر"}
    planned_visit_datetime: str           # ISO datetime in IRST (UTC+03:30)
    budget_range_toman: Dict[str, Optional[int]]
    active_filters: Dict[str, Any]        # max_radius_km, require_installment, require_torobpay, open_now_only, real_shops_demo_mode
    user_preferences: Dict[str, Any]

    # 3. Shopping Funnel Entities
    search_query_normalized: Optional[str]
    selected_product_id: Optional[str]
    product_candidates: List[Dict[str, Any]]
    store_candidates: List[Dict[str, Any]]
    rejected_shop_ids: List[str]
    active_target_shop_id: Optional[str]
    bourse_recommendation: Optional[Dict[str, Any]]

    # 4. Resilience, HITL & Loop Controls
    fallback_retry_count: int             # Hard cap: max 3
    hitl_pending_action: Optional[Dict[str, Any]]
    hitl_decision: Optional[Literal["approved", "edited", "cancelled"]]

    # 5. Generative UI Canvas State
    active_ui_components: List[Dict[str, Any]]
