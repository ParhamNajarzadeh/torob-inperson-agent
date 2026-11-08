---
name: tehran-bourses-and-passages
description: "Use when parsing indoor mall/passage floor and unit numbers from textual addresses or recommending specialized Tehran commercial bourses for out-of-dataset products."
allowed-tools: ["tehran_spatial_bourse_mcp"]
---

# Instructions
1. Use `scripts/parse_passage_address.py` to deterministically extract `passage_name`, `floor`, `corridor`, and `unit_number` from `shops.address`.
2. When a product is not in `products.csv` or has 0 nearby offers, match the product category against `references/tehran_commercial_bourses.json` and render `TehranBourseLocationWidget` with the bourse polygon and same-category shops from the `2,684` zero-offer directory shops in `shops.csv`.
