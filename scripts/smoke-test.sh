#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[1/4] Running Security Audit (Zero Hardcoded Secrets)..."
python3 scripts/security_audit.py

echo "[2/4] Testing EDA Data Pipeline & Dual-Mode Hedonic Fair Price Engine..."
python3 -c "
from backend.app.data_pipeline.clean_and_index import parse_warranty_json, compute_price_freshness, haversine_km
from backend.app.data_pipeline.hedonic_fair_price import compute_dual_mode_fair_price
assert haversine_km(35.7012, 51.4075, 35.6958, 51.4059) < 2.0
fp = compute_dual_mode_fair_price('شارژر گوشی', 'شارژر اپل 20W', [1680000, 1720000, 2150000])
assert fp['mode'] == 'multi_seller_consensus'
print('Data pipeline & Hedonic engine verified: OK')
"

echo "[3/4] Testing System-1 Decision Gateway & Evaluation Matrix..."
python3 eval/eval_router_matrix.py

echo "[4/4] Testing LangGraph Multi-Agent Turn & Governance Trace..."
python3 -c "
from backend.app.graph.workflow import run_torob_agent_turn
state = {'budget_range_toman': {'min': 0, 'max': 50000000}, 'active_filters': {'require_torobpay': True}}
out = run_torob_agent_turn('smoke_thread_01', 'شارژر اصلی اپل ۲۰ وات با ترب‌پی حضوری', state)
assert len(out['product_candidates']) > 0 and len(out['store_candidates']) > 0
print('LangGraph turn & GenUI state verified: OK')
"

echo "ALL SMOKE TESTS PASSED SUCCESSFULLY!"
