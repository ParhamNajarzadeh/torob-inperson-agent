#!/usr/bin/env python3
"""Deterministic price anomaly cleaner and seller_title unit disambiguator based on Torob EDA."""
import re
from typing import Dict, Any, Optional

BULK_UNIT_REGEX = re.compile(
    r"(کلاف|حلقه|قرقره|رول|کارتن|پک|بسته\s*\d+\s*عددی|\d+\s*متری|\b\d+m\b)",
    re.UNICODE | re.IGNORECASE
)

def inspect_offer_price_and_unit(
    price_toman: Optional[float],
    product_median_price: Optional[float],
    persian_title: str,
    seller_title: str
) -> Dict[str, Any]:
    status = "CLEAN"
    cleaned_price: Optional[int] = None
    suspected_rial_toman = False

    if price_toman is None:
        status = "UNPRICED_NEEDS_INQUIRY"
    elif price_toman <= 1000:
        status = "SENTINEL_QUARANATINED"
    elif price_toman > 2_000_000_000:
        # Check string concatenation overflow (e.g. shop_37befbca4fa26b53e5bae5bf)
        recovered = int(price_toman // 1_000_000_000)
        if 1000 < recovered <= 2_000_000_000:
            status = "OVERFLOW_RECOVERED"
            cleaned_price = recovered
        else:
            status = "OVERFLOW_QUARANTINED"
    else:
        cleaned_price = int(price_toman)

    if cleaned_price and product_median_price and product_median_price > 0:
        ratio = cleaned_price / product_median_price
        if 8.5 <= ratio <= 11.5:
            suspected_rial_toman = True
            cleaned_price = int(round(cleaned_price / 10.0))
        elif 0.085 <= ratio <= 0.115:
            suspected_rial_toman = True
            cleaned_price = int(round(cleaned_price * 10.0))

    seller_matches = set(BULK_UNIT_REGEX.findall(seller_title or ""))
    product_matches = set(BULK_UNIT_REGEX.findall(persian_title or ""))
    unit_mismatch_flag = bool(seller_matches - product_matches)

    return {
        "price_status": status,
        "cleaned_price_toman": cleaned_price,
        "suspected_rial_toman_flag": suspected_rial_toman,
        "unit_mismatch_flag": unit_mismatch_flag
    }
