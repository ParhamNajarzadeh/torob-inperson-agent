"""LangGraph StateGraph Orchestrator with Real MetisAI LLM Connection & Dynamic 24-Hour Spatial-Temporal Engine."""
import os
import re
import json
import httpx
from typing import Dict, Any, List, Optional
from backend.app.system_one.gateway import SystemOneDecisionGateway
from backend.app.mcp_servers.torob_catalog_mcp import (
    torob_catalog_megatool,
    parse_time_from_query,
    haversine_km,
)
from backend.app.mcp_servers.tehran_spatial_bourse_mcp import tehran_spatial_bourse_megatool
from backend.app.governance.observability import append_trace_event

system_one = SystemOneDecisionGateway()
EPISODIC_MEMORY_STORE: Dict[str, Any] = {}

TEHRAN_BOURSES_INFO = [
    {
        "bourse_id": "bourse_jomhouri_valiasr",
        "short_name": "بورس موبایل و الکترونیک ولیعصر / جمهوری (چارسو و علاءالدین)",
        "lat": 35.7025,
        "lon": 51.4065,
        "categories": ["شارژر گوشی", "گوشی موبایل", "هدفون، هدست و هندزفری", "لپ تاپ و نوت بوک", "تاچ و ال سی دی گوشی و تبلت", "ساعت مچی عقربه‌ای و دیجیتالی"],
    },
    {
        "bourse_id": "bourse_lalehzar",
        "short_name": "بورس برق، کابل و روشنایی لاله‌زار و فردوسی",
        "lat": 35.6935,
        "lon": 51.4215,
        "categories": ["سیم و کابل برق ساختمان", "لوستر و چراغ تزئینی", "سیم سیار و چندراهی برق", "دوربین مدار بسته", "دزدگیر اماکن و لوازم جانبی"],
    },
    {
        "bourse_id": "bourse_baharestan_saadi",
        "short_name": "بورس ابزار صنعتی، موتور برق و پمپ سعدی جنوبی",
        "lat": 35.6870,
        "lon": 51.4255,
        "categories": ["ژنراتور و موتور برق", "پمپ خانگی و صنعتی"],
    },
    {
        "bourse_id": "bourse_moniriyeh",
        "short_name": "بورس تخصصی کالای ورزشی و صوتی-تصویری مرکز شهر",
        "lat": 35.6845,
        "lon": 51.4015,
        "categories": ["اسپیکر و سیستم صوتی", "تلویزیون", "ساندبار", "لنز دوربین", "مبل تخت‌خواب شو"],
    },
]


def _format_price_fa(val: Optional[int]) -> str:
    if not val:
        return "نیازمند استعلام تلفنی"
    return f"{int(val):,} تومان"


def _find_relevant_bourse(cat_name: str, user_lat: float, user_lon: float) -> Dict[str, Any]:
    best = None
    for b in TEHRAN_BOURSES_INFO:
        if cat_name in b["categories"]:
            best = dict(b)
            break
    if not best:
        best = dict(TEHRAN_BOURSES_INFO[0])
    best["distance_km"] = haversine_km(user_lat, user_lon, best["lat"], best["lon"])
    return best


def synthesize_dynamic_inperson_response(
    user_query: str,
    matched_products: List[Dict[str, Any]],
    visit_time_str: str,
    is_holiday: bool,
    user_loc: Dict[str, Any],
) -> Dict[str, Any]:
    """Generates a 100% query-specific, time-specific analytical response grounded in the matched products and stores."""
    if not matched_products:
        return {
            "live_summary": f"بر اساس جستجوی شما («{user_query}») در ساعت {visit_time_str}، کالای دقیقی در لیست فعلی یافت نشد؛ نزدیک‌ترین بورس‌های تخصصی تهران روی نقشه مشخص شدند.",
            "review": None,
        }

    top_prod = matched_products[0]
    p_title = top_prod.get("persian_title", "")
    p_cat = top_prod.get("category_name", "کالای دیجیتال")
    min_p = _format_price_fa(top_prod.get("min_clean_price_toman"))
    med_p = _format_price_fa(top_prod.get("median_clean_price_toman"))
    max_p = _format_price_fa(top_prod.get("max_clean_price_toman"))
    stores = top_prod.get("stores", [])

    open_stores = [s for s in stores if s.get("is_open_now")]
    closed_stores = [s for s in stores if not s.get("is_open_now")]
    u_lat = float(user_loc.get("lat", 35.7165))
    u_lon = float(user_loc.get("lon", 51.4045))
    rel_bourse = _find_relevant_bourse(p_cat, u_lat, u_lon)

    day_label = "روز جمعه/تعطیل" if is_holiday else "روز عادی"

    if open_stores:
        best_open = open_stores[0]
        cheapest_open = min(
            open_stores, key=lambda x: x.get("registered_price_toman") or 999_999_999_999
        )
        summary = (
            f"پاسخ به درخواست شما («{user_query}») برای ساعت {visit_time_str} ({day_label}): "
            f"کالای «{p_title}» در {len(stores)} مغازه منتخب تهران بررسی شد. "
            f"در ساعت {visit_time_str}، تعداد {len(open_stores)} مغازه باز و {len(closed_stores)} مغازه بسته هستند. "
            f"نزدیک‌ترین مغازه باز به شما «{best_open.get('shop_name')}» در محله {best_open.get('location_label')} "
            f"({best_open.get('passage_name')}، {best_open.get('unit_number')}) در فاصله {best_open.get('distance_km')} کیلومتری است "
            f"(ساعت کاری: {best_open.get('open_hours_label')}، قیمت: {_format_price_fa(best_open.get('registered_price_toman'))})."
        )
        if cheapest_open.get("shop_id") != best_open.get("shop_id"):
            summary += (
                f" همچنین ارزان‌ترین مغازه باز در این ساعت «{cheapest_open.get('shop_name')}» با قیمت "
                f"{_format_price_fa(cheapest_open.get('registered_price_toman'))} در فاصله {cheapest_open.get('distance_km')} کیلومتری است."
            )
        if closed_stores:
            summary += (
                f" توجه کنید که {len(closed_stores)} مغازه دیگر (مانند «{closed_stores[0].get('shop_name')}» با ساعت کاری "
                f"{closed_stores[0].get('open_hours_label')}) در ساعت {visit_time_str} بسته هستند."
            )
    else:
        nearest_closed = closed_stores[0] if closed_stores else {}
        summary = (
            f"پاسخ به درخواست شما («{user_query}») برای ساعت {visit_time_str} ({day_label}): "
            f"در ساعت {visit_time_str}، تمام {len(stores)} فروشگاه ثبت‌شده در ترب برای «{p_title}» "
            f"(از جمله «{nearest_closed.get('shop_name', 'فروشگاه‌های مرکز شهر')}» با ساعت کاری {nearest_closed.get('open_hours_label', '۱۰ تا ۲۰')}) بسته هستند! "
            f"پیشنهاد دستیار ترب: ۱) ساعت مراجعه خود را به بازه کاری مغازه‌ها (مثلاً ۱۰:۳۰ تا ۲۰:۰۰) تغییر دهید تا از قیمت {min_p} خرید کنید، "
            f"یا ۲) اگر خرید شما فوری است، به «{rel_bourse['short_name']}» در فاصله {rel_bourse['distance_km']} کیلومتری مراجعه کنید."
        )

    review_obj = {
        "title": p_title,
        "score": "۹.۴ از ۱۰",
        "verdict": (
            f"برای خرید حضوری «{p_title}» (دسته: {p_cat}) در ساعت {visit_time_str}، "
            f"{len(open_stores)} فروشگاه فعال و باز در تهران شناسایی شد. کمترین قیمت بازار {min_p} و میانه قیمت {med_p} است."
        ),
        "dispersion_alert": (
            f"دامنه قیمت این کالا در مغازه‌های تهران از {min_p} تا {max_p} متغیر است. "
            f"نزدیک‌ترین بورس تخصصی این کالا «{rel_bourse['short_name']}» در فاصله {rel_bourse['distance_km']} کیلومتری شماست."
        ),
        "pros": [
            f"بررسی لحظه‌ای ساعت کاری مغازه‌ها در ساعت {visit_time_str} ({len(open_stores)} مغازه باز و {len(closed_stores)} مغازه بسته)",
            f"امکان مقایسه حضوری در {rel_bourse['short_name']}",
            "پشتیبانی از پرداخت قسطی حضوری (ترب‌پی / اسنپ‌پی) در فروشگاه‌های منتخب",
        ],
        "cons": [
            "تفاوت قیمت بین واحدهای طبقات مختلف پاساژ که استعلام پیش از حرکت را ضروری می‌کند",
            f"بسته بودن {len(closed_stores)} مغازه در ساعت {visit_time_str} بر اساس شیفت کاری ثبت‌شده",
        ],
        "checklist": [
            f"تطبیق مدل دقیق «{p_title[:40]}» و مشخصات فنی با فاکتور مغازه",
            "تست فیزیکی سلامت کالا و بررسی هولوگرام گارانتی پیش از پرداخت",
            "دریافت فاکتور مهرشده فروشگاه همراه با قید مهلت تست",
        ],
    }
    return {"live_summary": summary, "review": review_obj}


def _extract_json_or_text(raw_text: str) -> Dict[str, Any]:
    """Robustly extracts JSON if present, or uses natural conversational text from LLM directly."""
    cleaned = raw_text.strip()
    # Try finding a JSON block inside markdown or braces
    json_match = re.search(r"\{[\s\S]*\}", cleaned)
    if json_match:
        try:
            parsed = json.loads(json_match.group(0))
            if isinstance(parsed, dict) and (parsed.get("live_summary") or parsed.get("response")):
                return {
                    "live_summary": parsed.get("live_summary") or parsed.get("response"),
                    "review": parsed.get("review"),
                }
        except Exception:
            pass
    # If LLM returned plain text or markdown, strip code fences and return directly as live_summary
    plain = re.sub(r"```(?:json)?", "", cleaned).replace("```", "").strip()
    return {"live_summary": plain, "review": None}


def call_metis_llm(
    user_query: str,
    matched_products: List[Dict[str, Any]],
    state: Dict[str, Any],
    visit_time_str: str,
    is_holiday: bool,
) -> Dict[str, Any]:
    """Calls Metis AI LLM (supporting UI-provided key or .env key, and multiple Metis endpoints/models)."""
    ui_key = (state.get("metis_api_key") or "").strip()
    env_key = os.getenv("METIS_API_KEY", "").strip()
    api_key = ui_key if ui_key else env_key

    user_loc = state.get("user_location", {"label": "میدان ولیعصر", "lat": 35.7165, "lon": 51.4045})
    dynamic_fallback = synthesize_dynamic_inperson_response(
        user_query, matched_products, visit_time_str, is_holiday, user_loc
    )

    if not api_key or api_key in ("your_metis_api_key_here", "CHANGE_ME"):
        return {
            "live_summary": dynamic_fallback["live_summary"],
            "rag_guide": dynamic_fallback["review"],
            "status": "missing_api_key",
            "model_used": "local-dynamic-engine",
            "message": "کلید METIS_API_KEY تنظیم نشده است (از دکمه «⚙️ تنظیم کلید API متیس» در بالای صفحه یا فایل .env وارد کنید).",
        }

    # Build grounded catalog context with exact open/closed state at visit_time_str
    prod_summaries = []
    for p in matched_products[:4]:
        stores_info = []
        for s in (p.get("stores") or [])[:5]:
            open_lbl = f"باز در ساعت {visit_time_str}" if s.get("is_open_now") else f"بسته در ساعت {visit_time_str}"
            stores_info.append(
                f"  * مغازه «{s.get('shop_name')}» ({s.get('location_label')} - {s.get('passage_name')} {s.get('unit_number')}): "
                f"فاصله {s.get('distance_km')}km | قیمت: {_format_price_fa(s.get('registered_price_toman'))} | "
                f"ساعت کاری: {s.get('open_hours_label')} -> [{open_lbl}] | اقساط ترب‌پی: {'دارد' if s.get('torob_pay') else 'ندارد'}"
            )
        stores_str = "\n".join(stores_info)
        prod_summaries.append(
            f"- کالا: {p.get('persian_title')} (دسته: {p.get('category_name')})\n"
            f"  کمترین قیمت: {_format_price_fa(p.get('min_clean_price_toman'))} | میانه بازار: {_format_price_fa(p.get('median_clean_price_toman'))}\n"
            f"  مغازه‌ها در ساعت {visit_time_str}:\n{stores_str}"
        )

    catalog_context = "\n\n".join(prod_summaries)
    day_type = "جمعه / تعطیل" if is_holiday else "روز عادی"

    system_prompt = f"""شما «ترب‌چت حضوری» هستید؛ دستیار هوشمند خرید حضوری ترب در تهران.
اطلاعات لحظه‌ای کاربر:
- پیام کاربر: «{user_query}»
- ساعت دقیق مراجعه کاربر: ساعت {visit_time_str} ({day_type})
- موقعیت فعلی کاربر روی نقشه: {user_loc.get('label', 'تهران')} (مختصات {user_loc.get('lat')}, {user_loc.get('lon')})

کاتالوگ واقعی ترب و وضعیت باز/بسته بودن مغازه‌ها در ساعت {visit_time_str}:
{catalog_context}

دستورالعمل:
۱. مستقیماً به پیام کاربر («{user_query}») و ساعت دقیق مراجعه ({visit_time_str}) پاسخ بده.
۲. دقیقاً مشخص کن کدام مغازه‌ها در ساعت {visit_time_str} باز هستند و کدام‌ها بسته‌اند، چقدر فاصله دارند و قیمتشان چقدر است.
۳. پاسخ را در قالب JSON زیر برگردان:
{{
  "live_summary": "پاسخ کامل، صمیمی، دقیق و پویا به سوال کاربر بر اساس ساعت {visit_time_str} و مغازه‌های باز و بسته",
  "review": {{
    "title": "عنوان کالای پیشنهادی",
    "score": "امتیاز ارزش خرید حضوری از ۱۰",
    "verdict": "تحلیل جامع خرید حضوری این کالا در ساعت {visit_time_str}",
    "dispersion_alert": "تحلیل اختلاف قیمت مغازه‌ها و بورس تخصصی مرتبط",
    "pros": ["مزیت ۱", "مزیت ۲", "مزیت ۳"],
    "cons": ["نکته یا ریسک ۱", "نکته ۲"],
    "checklist": ["مورد تست ۱ در مغازه", "مورد تست ۲", "مورد تست ۳"]
  }}
}}"""

    preferred_model = (state.get("metis_model") or os.getenv("LLM_MODEL_NAME") or "gpt-4o-mini").strip()
    candidate_models = []
    for m in [preferred_model, "gpt-4o-mini", "deepseek-chat", "deepseek-v4.1-flash", "gemini-2.0-flash"]:
        if m and m not in candidate_models:
            candidate_models.append(m)

    base_urls = [
        os.getenv("METIS_OPENAI_COMPAT_URL", "https://api.metisai.ir/openai/v1").rstrip("/"),
        "https://api.metisai.ir/api/v1/wrapper/openai_chat_completion",
        os.getenv("METIS_BASE_URL", "https://api.metisai.ir/deepseek/v1").rstrip("/"),
    ]

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    last_error = ""
    try:
        with httpx.Client(timeout=20.0) as client:
            for b_url in base_urls:
                for mdl in candidate_models[:3]:
                    payload = {
                        "model": mdl,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_query},
                        ],
                        "temperature": 0.25,
                        "max_tokens": 1100,
                    }
                    try:
                        resp = client.post(f"{b_url}/chat/completions", headers=headers, json=payload)
                        if resp.status_code == 200:
                            data = resp.json()
                            raw_text = data["choices"][0]["message"]["content"]
                            extracted = _extract_json_or_text(raw_text)
                            return {
                                "live_summary": extracted.get("live_summary") or dynamic_fallback["live_summary"],
                                "rag_guide": extracted.get("review") or dynamic_fallback["review"],
                                "status": "success",
                                "model_used": mdl,
                            }
                        else:
                            last_error = f"HTTP {resp.status_code}: {resp.text[:160]}"
                    except Exception as inner_e:
                        last_error = str(inner_e)
    except Exception as e:
        last_error = str(e)

    return {
        "live_summary": dynamic_fallback["live_summary"],
        "rag_guide": dynamic_fallback["review"],
        "status": "error_fallback",
        "model_used": "local-dynamic-fallback",
        "message": f"خطا در اتصال به API متیس ({last_error})؛ پاسخ پویا توسط موتور تحلیلی محلی تولید شد.",
    }


def run_torob_agent_turn(
    thread_id: str,
    user_query: str,
    current_state: Dict[str, Any],
) -> Dict[str, Any]:
    """Executes full turn: Natural Language Time Parsing + 70-Product Catalog Search + Real MetisAI LLM."""
    # 1. Parse time from query or use state's visit_hour_float
    parsed_time = parse_time_from_query(user_query)
    if parsed_time["found"]:
        visit_hour_float = float(parsed_time["hour_float"])
        visit_time_str = str(parsed_time["time_str"])
        is_holiday = bool(parsed_time["is_holiday"]) or bool(current_state.get("is_holiday", False))
    else:
        visit_hour_float = float(current_state.get("visit_hour_float", 14.5))
        h_int = int(visit_hour_float)
        m_int = int(round((visit_hour_float - h_int) * 60))
        visit_time_str = current_state.get("visit_time_str") or f"{h_int:02d}:{m_int:02d}"
        is_holiday = bool(parsed_time["is_holiday"]) or bool(current_state.get("is_holiday", False))

    user_loc = current_state.get("user_location", {"lat": 35.7165, "lon": 51.4045, "label": "میدان ولیعصر"})
    u_lat = float(user_loc.get("lat", 35.7165))
    u_lon = float(user_loc.get("lon", 51.4045))

    s1_trace = system_one.route_intent_and_gates(user_query, current_state)

    catalog_res = torob_catalog_megatool(
        action="search_products",
        query=user_query,
        max_budget_toman=current_state.get("budget_range_toman", {}).get("max"),
        visit_hour_float=visit_hour_float,
        is_holiday=is_holiday,
        user_lat=u_lat,
        user_lon=u_lon,
    )

    matched_products = catalog_res.get("products", [])
    top_stores = matched_products[0].get("stores", []) if matched_products else []

    # Call Metis LLM (or dynamic query-specific synthesizer if no key)
    llm_output = call_metis_llm(
        user_query=user_query,
        matched_products=matched_products,
        state=current_state,
        visit_time_str=visit_time_str,
        is_holiday=is_holiday,
    )

    updated = dict(current_state)
    updated["visit_hour_float"] = visit_hour_float
    updated["visit_time_str"] = visit_time_str
    updated["is_holiday"] = is_holiday
    updated["parsed_time_from_query"] = parsed_time
    updated["last_system_one_trace"] = s1_trace
    updated["active_skills_loaded"] = s1_trace["selected_skills_jit"]
    updated["product_candidates"] = matched_products
    updated["store_candidates"] = top_stores
    updated["llm_live_summary"] = llm_output.get("live_summary")
    if llm_output.get("rag_guide"):
        updated["llm_rag_guide"] = {"review": llm_output["rag_guide"]}
    updated["llm_status"] = llm_output.get("status")
    updated["llm_model_used"] = llm_output.get("model_used")
    updated["llm_message"] = llm_output.get("message")

    append_trace_event(
        "agent_turn_completed",
        thread_id,
        {
            "intent_choice": s1_trace["intent_choice"],
            "visit_time_str": visit_time_str,
            "products_found": len(matched_products),
            "stores_found": len(top_stores),
            "llm_status": llm_output.get("status"),
            "llm_model_used": llm_output.get("model_used"),
        },
    )
    return updated
