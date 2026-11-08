#!/usr/bin/env python3
"""Deterministic Persian address parser for Tehran passages, floors, corridors, and units."""
import re
from typing import Dict, Optional

PASSAGE_RE = re.compile(r"(?:پاساژ|مرکز\s*خرید|مجتمع\s*تجاری|بازار)\s+([آ-یA-Za-z0-9\s]{2,25}?)(?:،|,|-|طبقه|واحد|پلاک|$)")
FLOOR_RE = re.compile(r"(?:طبقه|ط)\s*(همکف|زیرهمکف|اول|دوم|سوم|چهارم|پنجم|ششم|منفی\s*یک|[+-]?\d+)")
CORRIDOR_RE = re.compile(r"(?:راهرو|لاین|بلوک)\s*([آ-یA-Za-z0-9]+)")
UNIT_RE = re.compile(r"(?:واحد|پلاک|غرفه|شماره)\s*([0-9۰-۹A-Za-z/-]+)")

def parse_tehran_passage_address(address: str) -> Dict[str, Optional[str]]:
    if not address:
        return {
            "passage_name": "نامشخص — نیازمند استعلام",
            "floor": "نامشخص — نیازمند استعلام",
            "corridor": "اصلی",
            "unit_number": "نامشخص — نیازمند استعلام"
        }
    p_m = PASSAGE_RE.search(address)
    f_m = FLOOR_RE.search(address)
    c_m = CORRIDOR_RE.search(address)
    u_m = UNIT_RE.search(address)
    return {
        "passage_name": f"پاساژ {p_m.group(1).strip()}" if p_m else "راسته خیابان اصلی (خارج از پاساژ)",
        "floor": f"طبقه {f_m.group(1).strip()}" if f_m else "همکف / نامشخص در آدرس",
        "corridor": f"راهرو {c_m.group(1).strip()}" if c_m else "راهرو اصلی",
        "unit_number": f"واحد/پلاک {u_m.group(1).strip()}" if u_m else "نامشخص — نیازمند استعلام"
    }
