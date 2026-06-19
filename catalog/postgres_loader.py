from __future__ import annotations

import os
from typing import Any

import streamlit as st

from catalog.data_loader import _adapt_public_stones_v1_row

KURGIN_SCHEMA_NAME = "kurgin_admin"


def _secret_get(key: str, default: str = "") -> str:
    try:
        value = st.secrets.get(key, default)
    except Exception:
        value = default
    return str(value) if value is not None else default


def _database_url() -> str:
    return _secret_get("DATABASE_URL", "").strip() or os.environ.get("DATABASE_URL", "").strip()


def has_postgres_config() -> bool:
    return bool(_database_url())


def _payload_text(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key, "") if isinstance(payload, dict) else ""
    return "" if value is None else str(value)


def _float_or_none(value):
    try:
        return float(str(value).replace(" ", "").replace(",", "."))
    except Exception:
        return None


def _carat_label(value) -> str:
    number = _float_or_none(value)
    if number is None:
        text = str(value or "").strip()
        return f"{text} ct" if text else ""
    return f"{number:.2f} ct"


def _score_range_label(shape: str, score_value: str) -> str:
    score = _float_or_none(score_value)
    if score is None:
        return "" if str(shape).upper().strip() == "ROUND" else "Не применяется к форме"
    if score < 60:
        return "<60"
    if score < 70:
        return "60–69.99"
    if score < 80:
        return "70–79.99"
    if score < 90:
        return "80–89.99"
    if score < 95:
        return "90–94.99"
    return "95+"


def _normalize_fluorescence(value) -> str:
    text = str(value or "").strip()
    if text.lower() in {"", "nan", "none", "<na>"}:
        return "None"
    return text


def _price_type(payload: dict[str, Any]) -> tuple[str, str]:
    price_display = _payload_text(payload, "public_price_display")
    price_status = _payload_text(payload, "price_status")
    allow_por = _payload_text(payload, "allow_price_on_request").lower() == "true"
    total_rub = _payload_text(payload, "public_price_total_rub")
    if price_status == "calculated" and price_display and _float_or_none(total_rub):
        return "numeric", price_display
    if allow_por and price_display == "Цена по запросу":
        return "price_on_request", price_display
    return "", ""


def _public_row_from_db(stone_id, status, availability, section, report_number, stock_number, payload) -> dict:
    payload = payload or {}
    price_display_type, price_display = _price_type(payload)
    if not price_display_type:
        return {}

    shape = _payload_text(payload, "shape")
    score = _payload_text(payload, "kurgin_score")
    depth_mm = _payload_text(payload, "depth_mm")
    public_card_status = "public_numeric_price" if price_display_type == "numeric" else "public_price_on_request"
    reason = "published / in_stock / public section / numeric price" if price_display_type == "numeric" else "published / in_stock / public section / price on request"
    row = {
        "schema_version": "public_stones_v1",
        "exported_at": "postgresql_live",
        "stone_id": str(stone_id or ""),
        "report_number": str(report_number or _payload_text(payload, "report_number")),
        "lab": _payload_text(payload, "lab"),
        "catalog_section": str(section or ""),
        "section_name": "Основной каталог" if section == "main" else "Крупные камни" if section == "large" else "",
        "public_card_status": public_card_status,
        "public_visibility_reason": reason,
        "shape": shape,
        "weight": _payload_text(payload, "weight"),
        "carat_label": _carat_label(_payload_text(payload, "weight")),
        "color": _payload_text(payload, "color"),
        "clarity": _payload_text(payload, "clarity"),
        "kurgin_score": score,
        "kurgin_score_range_label": _score_range_label(shape, score),
        "public_price_display": price_display,
        "price_display_type": price_display_type,
        "min_diameter": _payload_text(payload, "min_diameter"),
        "max_diameter": _payload_text(payload, "max_diameter"),
        "height": _payload_text(payload, "height") or depth_mm,
        "depth_mm": depth_mm,
        "cut_grade": _payload_text(payload, "cut"),
        "symmetry": _payload_text(payload, "symmetry"),
        "polish": _payload_text(payload, "polish"),
        "fluorescence": _normalize_fluorescence(_payload_text(payload, "fluorescence")),
        "tags": _payload_text(payload, "tags"),
        "availability_status_public": str(availability or ""),
        "detail_available": "false",
        "kurgin_report_available": "false",
        "lab_report_available": "false",
        "main_image_available": "false",
    }
    return _adapt_public_stones_v1_row(row)


def load_postgres_catalog(limit: int = 5000) -> list[dict]:
    url = _database_url()
    if not url:
        return []

    import psycopg

    with psycopg.connect(url, connect_timeout=10) as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                select stone_id, status, availability_status, catalog_section,
                       report_number, stock_number, payload
                from {KURGIN_SCHEMA_NAME}.stones
                where status = 'published'
                  and availability_status = 'in_stock'
                order by stone_id
                limit %s
                """,
                (int(limit),),
            )
            rows = cur.fetchall()

    stones = []
    for row in rows:
        adapted = _public_row_from_db(*row)
        if adapted:
            stones.append(adapted)
    return stones
