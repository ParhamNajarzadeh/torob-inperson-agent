"""
Dual-Mode Fair Price & Comparison Engine (Insight 2, 7, 10, 15 of Torob EDA Report):
- Mode 1 (Multi-seller products: 38,899 products / 17.22% of catalog): Weighted clean median + min/median savings %.
- Mode 2 (Single-offer products: 187,004 products / 82.78% of catalog): Log10(price_toman) Hedonic Spec Regression.
"""
import math
import re
from typing import Dict, Any, List, Optional


CATEGORY_BASE_LOG10_MEDIANS: Dict[str, float] = {
    "گوشی موبایل": 7.45,
    "لپ تاپ و نوت بوک": 8.16,
    "سیم و کابل برق ساختمان": 6.05,
    "دوربین مدار بسته": 6.84,
    "ژنراتور و موتور برق": 8.19,
    "پمپ خانگی و صنعتی": 7.49,
    "هدفون، هدست و هندزفری": 6.63,
    "ساعت مچی عقربه‌ای و دیجیتالی": 7.31,
    "شارژر گوشی": 6.32,
    "کفش و کتانی ورزشی": 6.83
}


def extract_specs_from_persian_title(persian_title: str) -> Dict[str, Any]:
    """Insight 9 & 10: Compensates for 74.49% missing brand_name, 98.20% missing model, and 35.99% missing specs."""
    title = persian_title or ""
    storage_gb = None
    ram_gb = None

    m_storage = re.search(r"(32|64|128|256|512|1024)\s*(?:GB|گیگابایت|گیگ)", title, re.IGNORECASE)
    if m_storage:
        storage_gb = int(m_storage.group(1))

    m_ram = re.search(r"رم\s*(4|8|12|16|24|32|64)\s*(?:GB|گیگ)?", title, re.IGNORECASE)
    if m_ram:
        ram_gb = int(m_ram.group(1))

    brands = ["سامسونگ", "اپل", "شیائومی", "انکر", "اسیکس", "نایکی", "آدیداس", "ایسوس", "لنوو", "داهوا", "هایک ویژن", "افشارنژاد خراسان"]
    detected_brand = next((b for b in brands if b in title), None)

    return {
        "extracted_brand": detected_brand,
        "storage_gb": storage_gb,
        "ram_gb": ram_gb
    }


def compute_dual_mode_fair_price(
    category_name: str,
    persian_title: str,
    clean_offer_prices: List[int]
) -> Dict[str, Any]:
    """Computes both direct market consensus (if >=2 offers) and Hedonic log10 spec estimate."""
    specs = extract_specs_from_persian_title(persian_title)
    base_log10 = CATEGORY_BASE_LOG10_MEDIANS.get(category_name, 6.56)  # 6.56 = log10(3,650,000 Toman global median)

    # Monotonic spec adjustments proven in EDA Insight 10
    if specs["storage_gb"]:
        if specs["storage_gb"] >= 512:
            base_log10 += 0.38
        elif specs["storage_gb"] >= 256:
            base_log10 += 0.24
        elif specs["storage_gb"] <= 64:
            base_log10 -= 0.22
    if specs["ram_gb"]:
        if specs["ram_gb"] >= 32:
            base_log10 += 0.30
        elif specs["ram_gb"] >= 16:
            base_log10 += 0.18

    hedonic_estimate = int(round((10 ** base_log10) / 10000.0) * 10000)

    if not clean_offer_prices:
        return {
            "mode": "unpriced_hedonic_only",
            "min_clean_price_toman": None,
            "median_clean_price_toman": None,
            "max_clean_price_toman": None,
            "hedonic_fair_price_estimate": hedonic_estimate,
            "max_saving_pct_vs_median": 0.0
        }

    sorted_p = sorted(clean_offer_prices)
    n = len(sorted_p)
    median_p = sorted_p[n // 2] if n % 2 == 1 else int((sorted_p[n // 2 - 1] + sorted_p[n // 2]) / 2)
    min_p = sorted_p[0]
    max_p = sorted_p[-1]
    saving_pct = round(((median_p - min_p) / median_p) * 100.0, 1) if median_p > 0 else 0.0

    return {
        "mode": "multi_seller_consensus" if n >= 2 else "single_offer_hedonic",
        "min_clean_price_toman": min_p,
        "median_clean_price_toman": median_p,
        "max_clean_price_toman": max_p,
        "hedonic_fair_price_estimate": median_p if n >= 3 else int(0.6 * median_p + 0.4 * hedonic_estimate),
        "max_saving_pct_vs_median": saving_pct
    }
