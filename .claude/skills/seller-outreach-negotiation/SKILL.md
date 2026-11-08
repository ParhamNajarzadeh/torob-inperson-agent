---
name: seller-outreach-negotiation
description: "Use when executing the Zero-Awkwardness AI Voice/Message Proxy or generating 1-Tap Seller Micro-Webhook links after HITL approval."
allowed-tools: ["outreach_and_real_shops_mcp"]
---

# Instructions
1. Never initiate external outreach before `hitl_decision == "approved"`.
2. Generate both an automated polite Persian voice/message script AND a 1-Tap Seller Micro-Webhook payload with 3 instant response actions (`[✅ موجوده با همین قیمت]`, `[🔄 موجوده ولی قیمت امروز تغییر کرده]`, `[❌ فعلاً تمام شده / مغازه بسته است]`).
3. Persist the seller's response in `("shops_episodic_memory", shop_id)` with `ttl_minutes = 120` so subsequent shoppers immediately benefit.
