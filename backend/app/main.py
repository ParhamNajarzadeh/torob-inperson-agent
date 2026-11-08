"""FastAPI Server + Real MetisAI Connection + Multi-Page Torob In-Person Shopping Assistant."""
import os
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import backend.app.governance.security_guards as sec_guards
from backend.app.graph.workflow import run_torob_agent_turn, call_metis_llm, EPISODIC_MEMORY_STORE
from backend.app.mcp_servers.outreach_and_real_shops_mcp import execute_seller_outreach_megatool
from backend.app.mcp_servers.torob_catalog_mcp import ALL_CATALOG_PRODUCTS

app = FastAPI(
    title="Torob In-Person Shopping Assistant API (LangGraph + MetisAI + Dynamic Multi-Page UI)",
    version="2.0.0",
)


@app.get("/", response_class=HTMLResponse)
def serve_full_ui() -> HTMLResponse:
    """Serves the Multi-Page Torob In-Person Shopping Assistant UI."""
    candidates = [
        os.path.join(os.path.dirname(__file__), "torob_inperson_concierge.html"),
        os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "public", "torob_inperson_concierge.html"),
    ]
    for html_file in candidates:
        if os.path.exists(html_file):
            with open(html_file, "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Torob In-Person Assistant</h1>")


@app.get("/app", response_class=HTMLResponse)
def serve_app_alias() -> HTMLResponse:
    return serve_full_ui()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AgentTurnRequest(BaseModel):
    thread_id: str = "thread_demo_01"
    user_query: str = ""
    state: Dict[str, Any] = {}


class MetisKeyTestRequest(BaseModel):
    metis_api_key: str = ""
    metis_model: str = "gpt-4o-mini"


class RetireRequest(BaseModel):
    reason: str


@app.get("/health")
def health_check() -> Dict[str, Any]:
    env_key = os.getenv("METIS_API_KEY", "").strip()
    has_env_key = bool(env_key and env_key not in ("your_metis_api_key_here", "CHANGE_ME"))
    return {
        "status": "healthy",
        "service": "torob-inperson-agent-backend",
        "llm_model": os.getenv("LLM_MODEL_NAME", "gpt-4o-mini"),
        "metis_env_configured": has_env_key,
        "catalog_products_count": len(ALL_CATALOG_PRODUCTS),
        "catalog_db_readonly": True,
        "agent_retired": sec_guards.AGENT_RETIRED_KILL_SWITCH,
    }


@app.post("/api/v1/metis/test")
def test_metis_connection(req: MetisKeyTestRequest) -> Dict[str, Any]:
    """Tests Metis AI API key and returns live status."""
    sample_prods = ALL_CATALOG_PRODUCTS[:1] if ALL_CATALOG_PRODUCTS else []
    res = call_metis_llm(
        user_query="سلام، لطفا در یک جمله کوتاه معرفی کن که چطور به خرید حضوری در تهران کمک می‌کنی.",
        matched_products=sample_prods,
        state={"metis_api_key": req.metis_api_key, "metis_model": req.metis_model},
        visit_time_str="14:30",
        is_holiday=False,
    )
    return res


@app.post("/api/v1/agent/turn")
def agent_turn(req: AgentTurnRequest) -> Dict[str, Any]:
    sec_guards.check_agent_active()
    return run_torob_agent_turn(req.thread_id, req.user_query, req.state)


@app.post("/api/v1/seller/1tap-webhook")
def seller_micro_webhook(
    thread_id: str,
    shop_id: str,
    shop_name: str,
    product_id: str,
    response_code: str = "confirmed_in_stock",
) -> Dict[str, Any]:
    sec_guards.check_agent_active()
    res = execute_seller_outreach_megatool(
        thread_id=thread_id,
        shop_id=shop_id,
        shop_name=shop_name,
        product_id=product_id,
        channel="seller_1tap_webhook",
        custom_question="استعلام ۱ کلیکی موجودی و قیمت روز",
        simulated_seller_response=response_code,
    )
    EPISODIC_MEMORY_STORE[shop_id] = res["episodic_memory_record"]
    return res


@app.post("/admin/agent/retire")
def retire_agent_kill_switch(
    req: RetireRequest,
    x_admin_secret: Optional[str] = Header(default=None),
) -> Dict[str, Any]:
    expected = os.getenv("AGENT_KILL_SWITCH_SECRET", "change_me_in_production_admin_secret")
    if x_admin_secret != expected:
        raise HTTPException(status_code=403, detail="Invalid Kill-Switch admin secret")
    sec_guards.AGENT_RETIRED_KILL_SWITCH = True
    return {"status": "retired", "reason": req.reason}
