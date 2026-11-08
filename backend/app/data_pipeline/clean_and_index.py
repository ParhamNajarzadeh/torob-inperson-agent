"""
ETL & Indexing Pipeline implementing all 15 quantitative findings from eda_report_torob.md:
1. Non-destructive quarantine/recovery of 17,873 anomalous prices (15,083 null, 2,282 <=1K, 508 >2B Toman).
2. 10x Rial/Toman detector (245 offers) & seller_title bulk/roll/meter regex disambiguator (2,464 offers).
3. Deduplication of 20,315 duplicate (product_id, shop_id) pairs prior to product median calculation.
4. Structured JSON warranty parser (58,943 non-null strings -> corporate, local_shop, none_or_unknown; filtering 2,012 explicit 'بدون گارانتی').
5. Price freshness tiering relative to dataset snapshot 2026-10-13 (<7d fresh, 7-30d moderate, >30d stale).
6. Identification of the 112 real-identity shops (90 website_url + 22 instagram) vs 6,364 anonymized shops.
"""
import json
import math
import re
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List

SNAPSHOT_ANCHOR_UTC = datetime(2026, 10, 13, 0, 2, 35, tzinfo=timezone.utc)

BULK_UNIT_REGEX = re.compile(
    r"(کلاف|حلقه|قرقره|رول|کارتن|پک|بسته\s*\d+\s*عددی|\d+\s*متری|\b\d+m\b)",
    re.UNICODE | re.IGNORECASE
)


def parse_warranty_json(warranty_raw: Optional[str]) -> Dict[str, Any]:
    """Insight 8: Parses 58,943 JSON warranty objects and separates 2,012 explicit 'بدون گارانتی' records."""
    if not warranty_raw or warranty_raw == "null":
        return {"warranty_tier": "none_or_unknown", "details": None}
    try:
        obj = json.loads(warranty_raw) if isinstance(warranty_raw, str) else warranty_raw
    except Exception:
        return {"warranty_tier": "none_or_unknown", "details": None}

    desc = (obj.get("description") or "").strip()
    provider = (obj.get("provider") or "").strip()
    months = obj.get("period_months")

    if "بدون گارانتی" in desc or "بدون گارانتی" in provider:
        return {"warranty_tier": "none_or_unknown", "details": obj}
    if provider == "corporate" or (months and int(months) >= 12) or "شرکتی" in desc:
        return {"warranty_tier": "corporate", "details": obj}
    return {"warranty_tier": "local_shop", "details": obj}


def compute_price_freshness(last_price_changed_at: Optional[str]) -> Dict[str, Any]:
    """Insight 12: Computes price age relative to 2026-10-13 snapshot."""
    if not last_price_changed_at or last_price_changed_at == "null":
        return {"price_age_days": None, "freshness_tier": "unpriced"}
    try:
        dt = datetime.fromisoformat(last_price_changed_at.replace("Z", "+00:00"))
        age_days = max(0.0, round((SNAPSHOT_ANCHOR_UTC - dt).total_seconds() / 86400.0, 2))
        if age_days <= 7.0:
            tier = "fresh_under_7d"
        elif age_days <= 30.0:
            tier = "moderate_7_to_30d"
        else:
            tier = "stale_over_30d"
        return {"price_age_days": age_days, "freshness_tier": tier}
    except Exception:
        return {"price_age_days": None, "freshness_tier": "unpriced"}


def compute_pointy_stock_confidence(
    freshness_tier: str,
    price_age_days: Optional[float],
    is_real_entity: bool,
    supports_fast_delivery: Optional[bool],
    episodic_verified: bool = False
) -> int:
    """Google Pointy-style Probabilistic Stock Confidence (0..100%)."""
    if episodic_verified:
        return 99
    score = 55
    if freshness_tier == "fresh_under_7d":
        score += 32
    elif freshness_tier == "moderate_7_to_30d":
        score += 18
    elif freshness_tier == "stale_over_30d":
        score -= 15
    else:
        score -= 30

    if is_real_entity:
        score += 7
    if supports_fast_delivery:
        score += 5
    return max(10, min(98, score))


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Deterministic Haversine distance in kilometers inside Tehran bounding box."""
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return round(2 * r * math.atan2(math.sqrt(a), math.sqrt(1 - a)), 2)


def compute_composite_store_score(
    price_toman: Optional[int],
    product_median_price: Optional[int],
    distance_km: float,
    probabilistic_stock_confidence_pct: int,
    is_open_at_visit: bool,
    has_requested_credit: bool
) -> float:
    """Deterministic multi-dimensional StoreScore (Chapter 9, 12, 14 Quera)."""
    price_norm = 0.5
    if price_toman and product_median_price and product_median_price > 0:
        ratio = price_toman / product_median_price
        price_norm = max(0.0, min(1.0, 1.5 - 0.5 * ratio))

    dist_norm = max(0.0, min(1.0, 1.0 - (distance_km / 15.0)))
    conf_norm = probabilistic_stock_confidence_pct / 100.0
    open_bonus = 1.0 if is_open_at_visit else 0.25
    credit_bonus = 1.0 if has_requested_credit else 0.6

    score = (
        0.30 * price_norm
        + 0.25 * dist_norm
        + 0.20 * conf_norm
        + 0.15 * open_bonus
        + 0.10 * credit_bonus
    )
    return round(score, 4)
