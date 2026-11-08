# Changelog

All notable changes to the **Torob In-Person Shopping Assistant (`torob-inperson-agent`)** are documented in this file following Semantic Versioning (SemVer).

## [1.0.0] - 2026-10-22
### Added
- **Map-First Visual Shopping Concierge Frontend (Next.js + Shadcn UI + Torob Brand Design System)**:
  - Full RTL Persian layout (`#D73948` Torob Red, `Vazirmatn` font with Persian digits `ss01`).
  - 4-Step Visual Stepper & Chatless Quick-Filter Bar (neighborhood, budget slider, TorobPay/installment, open-now toggle, 112 real-shop live mode).
  - All 11 interactive GenUI components (`SmartRequirementForm`, `ProductComparisonCarousel`, `ProductReviewAndInspectionCard`, `InteractiveTehranMapAndFilterBar`, `StoreComparisonMatrix`, `RealStoreWebInstagramLiveCard`, `OutreachApprovalDialog`, `LiveVerificationTracker`, `AlternativeSwitchBanner`, `TehranBourseLocationWidget`, `PassageIndoorNavigationCard`).
- **EDA-Driven Data Pipeline (`clean_and_index.py` & `hedonic_fair_price.py`)**:
  - Non-destructive cleaning of 17,873 anomalous offers (`15,083` null prices, `2,282` sentinel `<=1,000` Toman, `508` overflow `>2B` Toman including integer division `/10^9` fix on `shop_37befbca4fa26b53e5bae5bf`).
  - Automated 10x Rial/Toman detector (`245` offers) and `seller_title` bulk/roll/meter unit disambiguator (`2,464` offers across `1,721` products).
  - Dual-mode Fair Price Engine (weighted median for `38,899` multi-seller products + Hedonic `log10(price_toman)` spec regression for `187,004` single-offer products).
- **Self-Contained Dual Model Gateway**:
  - `llm_gateway.py`: `deepseek-v4.1-flash` via MetisAI proxy with `cache: {"ttl": "5m"}`.
  - `system_one/gateway.py`: `SystemOneDecisionGateway` supporting `metis_jev`, `local_mizan_4b`, `local_kev`, and `local_laya` (`/v1/systemone` Choice, Score, Noul).
- **O2O Pain-Point Solvers & Governance**:
  - Zero-Awkwardness AI Voice/Message Proxy, 1-Tap Seller Micro-Webhook, Google Pointy Probabilistic Stock Confidence + Waze-style Shopper Check-in, 2-Hour Price-Lock QR Hold Pass, and In-Mall Panic Reroute Button (`🚨 الان جلوی مغازه‌ام و بسته است`).
  - Read-Only SQL enforcement, `<untrusted_content>` prompt-injection breaker, LangGraph `interrupt()` HITL gate, `fallback_retry_count <= 3`, and `scripts/security_audit.py`.
