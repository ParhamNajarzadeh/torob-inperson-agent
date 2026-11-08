# راهنمای تحویل سیستم و اجرای تست‌های سلامت (`docs/ONBOARDING.md`)

## ۱. ساختار معماری ۴ لایهٔ قطعیت رفتار (فصل ۱۲ کوئرا)
1. **لایهٔ ۱ (Always-On):** فایل `CLAUDE.md` و سیستم‌پرامپت کش‌شده با `extra_body={"cache": {"ttl": "5m"}}`.
2. **لایهٔ ۲ (Progressive Disclosure Skills):** پوشهٔ `.claude/skills/` شامل ۵ مهارت تخصصی که متادیتای آن‌ها در استارت‌آپ خوانده شده و بدنهٔ کامل فقط به صورت Just-in-Time توسط `skill_selector_gate` بارگذاری می‌شود.
3. **لایهٔ ۳ (Context-Isolated Subagents):** پوشهٔ `.claude/agents/` شامل ۶ ساب‌ایجنت تخصصی که خروجی آن‌ها حداکثر ۳۰۰ توکن JSON تایپ‌شده است.
4. **لایهٔ ۴ (Deterministic Hooks & Stage Guards):** فایل `.claude/settings.json` و `backend/app/graph/stage_guard.py`.

## ۲. اجرای تست سلامت و ارزیابی
```bash
# ۱. ممیزی امنیتی کد (تضمین ۰ کلید هاردکدشده)
python3 scripts/security_audit.py

# ۲. اجرای پایپ‌لاین نمونه و تست سلامت بک‌اند و فرانت‌اند
bash scripts/smoke-test.sh

# ۳. ارزیابی ماتریس مسیریاب System-1 و LLM-as-Judge
python3 eval/eval_router_matrix.py
python3 eval/rubric_judge.py
```
