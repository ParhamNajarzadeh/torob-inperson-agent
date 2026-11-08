---
name: torob-catalog-disambiguation
description: "Use when querying products.csv and offers.csv to filter out null/sentinel/overflow prices, detect 10x Rial/Toman errors, and disambiguate bulk/roll/meter seller_title units from single items."
allowed-tools: ["torob_catalog_mcp"]
---

# Instructions
1. Always enforce the Dataset-First Invariant: search the 225,903 `BaseProduct` records and 331,506 `ProductInStore` offers first.
2. Quarantine offers where `price_toman IS NULL` (`UNPRICED_NEEDS_INQUIRY`), `price_toman <= 1000` (`SENTINEL_PLACEHOLDER`), or `price_toman > 2000000000` (apply `// 10**9` overflow recovery if trailing 9 digits match concatenation).
3. Compare `offers.seller_title` against `products.persian_title` using `scripts/clean_price_and_units.py` to flag bulk/pack/roll/meter mismatches (`unit_mismatch_flag = True`).

# Examples
- Input: `product_df1dfb162403cf73df70fdf3` (شارژر اپل ۲۰ وات) -> Flag extreme dispersion (`480,000` to `29,800,000` Toman) as high-copy vs original authenticity risk.
- Input: `product_9b36205cbdc7ee5304fc85b6` (سیم افشان ۲.۵) -> Separate 1-meter offers (`39,000` Toman) from 100-meter roll (`کلاف ۱۰۰ متری`) in `seller_title`.

# Constraints
- Never merge category-only shops (`2,684` zero-offer shops in `shops.csv`) into confirmed product offers.
