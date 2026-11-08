---
name: product-review-and-inspection
description: "Use when generating ProductReviewAndInspectionCard with statistical price dispersion alerts, fake/high-copy warnings, and physical in-store testing checklists."
allowed-tools: ["torob_catalog_mcp"]
---

# Instructions
1. Combine Torob dataset metrics (`max/min` price ratio, corporate vs shop warranty share, `seller_title` unit traps) with category-specific physical inspection checklists from `references/category_inspection_checklists.json`.
2. Format output strictly according to `assets/review_card_schema.json`.
