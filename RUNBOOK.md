# دستورالعمل عملیات، پایداری و چک‌لیست داوری (`RUNBOOK.md`)

## ۱. راه‌اندازی سریع ۱ دستوری برای داوران
```bash
cp .env.example .env
# کلید METIS_API_KEY خود را در فایل .env قرار دهید
bash scripts/smoke-test.sh
docker compose up --build -d
```
- **رابط کاربری رادار خرید حضوری (Next.js):** `http://localhost:3000`
- **بک‌اند ایجنتیک و مستندات OpenAPI (FastAPI + LangGraph):** `http://localhost:8000/docs`
- **تست سلامت سرویس:** `curl http://localhost:8000/health`

## ۲. کلید توقف اضطراری (AI Governance Kill-Switch — فصل ۱۶ کوئرا)
طبق گزارش CSA 2026 (نبود فرآیند بازنشستگی در ۷۹٪ سازمان‌ها)، این ایجنت دارای هویت مستقل مجازی (`service_account:torob-inperson-agent-v1`)، تاریخ انقضای توکن (`AGENT_TOKEN_EXPIRES_AT`) و اندپوینت بازنشستگی آنی است:
```bash
curl -X POST http://localhost:8000/admin/agent/retire \
  -H "X-Admin-Secret: ${AGENT_KILL_SWITCH_SECRET}" \
  -H "Content-Type: application/json" \
  -d '{"reason": "Hackathon judging period completed"}'
```
پس از فراخوانی این دستور، تمام فراخوانی‌های بیرونی و استعلام‌های فروشندگان متوقف شده و سیستم در حالت ایمن Read-Only قفل می‌شود.

## ۳. چک‌لیست امنیتی پیش از Public کردن مخزن (بازهٔ پایان مهلت تا ۱ ساعت پس از آن)
1. اجرای اسکنر امنیتی خودکار جهت اطمینان از نبود هیچ کلید API در کدها:
   ```bash
   python3 scripts/security_audit.py
   ```
   *(خروجی باید دقیقاً `PASS: 0 hardcoded secrets found across all files` باشد).*
2. اطمینان از وجود `.env` در `.gitignore` و تمیز بودن `.env.example`.
3. اجرای تست سلامت سرتاسری:
   ```bash
   bash scripts/smoke-test.sh
   ```

## ۴. کارگردانی ویدیوی دموی ۵ دقیقه‌ای برای کسب کامل ۳۰۰ امتیاز
- **دقیقه ۰:۰۰ تا ۱:۰۰ (فلو متفاوت Map-First و گام ۱ + موتور نقد و بررسی):** نمایش رابط کاربری با دیزاین‌سیستم ترب (`#D73948`، وزیرمتن)، انتخاب نیاز با فرم بدون چت `SmartRequirementForm`، مشاهدهٔ کاروسل محصولات `ProductComparisonCarousel`، قیمت منصفانهٔ هدونیک و باز کردن `ProductReviewAndInspectionCard` (رادار ریسک کالای های‌کپی/تفاوت واحد فروش `seller_title` + چک‌لیست تعاملی تست فیزیکی در مغازه).
- **دقیقه ۱:۰۰ تا ۲:۱۵ (گام ۲ و ۳ — نقشهٔ بورس‌ها، تفکیک ۳ سطح قیمت و رادار موجودی):** تغییر بدون چت (Chatless) فیلتر محله و «ترب‌پی حضوری / قسطی» روی نقشهٔ تعاملی `InteractiveTehranMapAndFilterBar`، نمایش تفکیک قیمت ثبت‌شده، سن قیمت و قیمت تأییدشده در `StoreComparisonMatrix` به همراه درصد اطمینان موجودی (Pointy Score) و تأیید جمعی خریداران (Waze Check-in).
- **دقیقه ۲:۱۵ تا ۳:۳۰ (گام ۴ — وکیل صوتی ضدخجالت، میکرو-لینک ۱ کلیکی و ۱۱۲ فروشگاه واقعی):** کلیک روی «به‌جای من از مغازه‌دار بپرس»، نمایش دیالوگ HITL (`OutreachApprovalDialog`)، مشاهدهٔ موج صوتی و شبیه‌ساز میکرو-لینک ۱ کلیکی فروشنده در `LiveVerificationTracker`، و بررسی زندهٔ یکی از ۱۱۲ فروشگاه دارای سایت/اینستاگرام واقعی در `RealStoreWebInstagramLiveCard`.
- **دقیقه ۳:۳۰ تا ۴:۳۰ (دکمهٔ نجات فوری در پاساژ، بورس‌یاب تهران و کارت رزرو QR):** فشردن دکمهٔ بحران `🚨 الان جلوی مغازه‌ام و بسته است!` در `AlternativeSwitchBanner` و جایگزینیابی زیر ۲ ثانیه در همان پاساژ + نمایش کارت مسیریابی درون‌پاساژی `PassageIndoorNavigationCard` (طبقه، راهرو، پلاک و QR رزرو ۲ ساعته) + نمایش ویجت `TehranBourseLocationWidget` برای کالای خارج از دیتاست.
- **دقیقه ۴:۳۰ تا ۵:۰۰ (معماری فنی کوئرا، دروازهٔ System-1 و دیپلوی لیارا):** نمایش پنل تله‌متری `SystemOneDecisionGateway` (`Jev / Mizan-4B / Kev / Laya` با تأخیر ~۴۰ میلی‌ثانیه)، کش پرامپت `deepseek-v4.1-flash` و لاگ `trace.jsonl`.
