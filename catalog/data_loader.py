import html
import json
import os
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

from catalog.stones import STONES as LOCAL_STONES

DEFAULT_CATALOG_URLS = [
    "https://raw.githubusercontent.com/kka45821-del/kurgin-data/main/catalog.json",
    "https://raw.githubusercontent.com/kka45821-del/kurgin-data/main/stones.json",
    "https://raw.githubusercontent.com/kka45821-del/kurgin-data/main/catalog_published.json",
    "https://raw.githubusercontent.com/kka45821-del/kurgin-data/main/data/catalog.json",
]

TAG_LABELS = {
    "огонь": "О",
    "fire": "О",
    "блеск": "Б",
    "brilliance": "Б",
    "контраст": "К",
    "contrast": "К",
    "баланс": "БАЛАНС",
    "balance": "БАЛАНС",
    "цена": "ЦЕНА",
    "price": "ЦЕНА",
    "крупный": "КРУПНЫЙ",
    "large": "КРУПНЫЙ",
    "овал": "ОВАЛ",
    "oval": "ОВАЛ",
    "капля": "PEAR",
    "pear": "PEAR",
    "кушон": "CUSHION",
    "cushion": "CUSHION",
    "проверка": "ПРОВЕРКА",
    "review": "ПРОВЕРКА",
}


def _load_json_url(url: str):
    with urlopen(url, timeout=5) as response:
        raw = response.read().decode("utf-8")
    return json.loads(raw)


def _extract_stones(payload):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("stones", "catalog", "items", "data"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return []


def _safe_float(value, default=0.0):
    try:
        if value in (None, ""):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _safe_int(value, default=0):
    try:
        if value in (None, ""):
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _display_tags(stone: dict) -> str:
    existing = stone.get("tags")
    if existing:
        return existing

    parts = []
    for key in ("tag1", "tag2", "tag3", "tag4", "tag5", "tag6"):
        raw = stone.get(key)
        if raw in (None, ""):
            continue
        raw_text = str(raw).strip()
        mapped = TAG_LABELS.get(raw_text.lower(), raw_text.upper())
        if mapped in ("ЭЛИТ", "ELITE"):
            # ELITE is displayed automatically by Karo Score >= 98.5.
            continue
        label = html.escape(mapped)
        css_class = "tag blue" if label == "Б" else "tag gray" if label == "К" else "tag"
        parts.append(f'<span class="{css_class}">{label}</span>')
    return "".join(parts)


def _meta(stone: dict) -> str:
    if stone.get("meta"):
        return stone["meta"]
    measurements = stone.get("measurements") or stone.get("Measurements") or ""
    cut = stone.get("cut") or stone.get("Cut") or ""
    polish = stone.get("polish") or stone.get("Polish") or ""
    symmetry = stone.get("symmetry") or stone.get("Symmetry") or ""
    fluor = stone.get("fluor") or stone.get("fluorescence") or ""
    finish = " ".join(str(x).lower() for x in (cut, polish, symmetry) if x not in (None, ""))
    chunks = [str(x) for x in (measurements, finish, fluor) if x not in (None, "")]
    return " · ".join(chunks)


def _normalize_stone(stone: dict) -> dict:
    normalized = dict(stone)

    carat = _safe_float(normalized.get("carat", normalized.get("weight", normalized.get("Weight", 0))))
    score = _safe_float(normalized.get("score", normalized.get("karo_score", 0)))
    price = _safe_int(normalized.get("price", normalized.get("price_rub", 0)))

    price_text = normalized.get("priceText") or f"{price:,}".replace(",", " ")

    normalized.setdefault("id", normalized.get("stone_id") or normalized.get("stock_number") or normalized.get("stock") or normalized.get("Stock #") or normalized.get("report_number") or "")
    normalized.setdefault("shape", normalized.get("Shape", "Круг"))
    normalized["carat"] = carat
    normalized.setdefault("color", normalized.get("Color", ""))
    normalized.setdefault("clarity", normalized.get("Clarity", ""))
    normalized["score"] = score
    normalized["price"] = price
    normalized["priceText"] = price_text
    normalized.setdefault("diameter", normalized.get("diameter_mm", ""))
    normalized["meta"] = _meta(normalized)
    normalized.setdefault("fluor", normalized.get("fluorescence", normalized.get("Fluorescence", "")))
    normalized.setdefault("finish", normalized.get("finish_grade", ""))
    normalized.setdefault("report", normalized.get("report_number", normalized.get("Report #", "")))
    normalized["tags"] = _display_tags(normalized)
    normalized.setdefault("section", _section_by_carat(carat))
    normalized["weight"] = _weight_band(carat)
    normalized["scoreBand"] = _score_band(score)
    return normalized


def _section_by_carat(carat: float) -> str:
    if carat < 0.30:
        return "small"
    if carat < 1.00:
        return "medium"
    if carat < 3.00:
        return "main"
    return "large"


def _weight_band(carat: float) -> str:
    if 1.0 <= carat < 1.5:
        return "1–1.49"
    if 1.5 <= carat < 2.0:
        return "1.5–1.99"
    if 2.0 <= carat < 2.5:
        return "2–2.49"
    if 2.5 <= carat < 3.0:
        return "2.5–2.99"
    return ""


def _score_band(score: float) -> str:
    if score >= 99:
        return "99+"
    if score >= 95:
        return "95–98"
    if score >= 90:
        return "90–94.9"
    if score >= 80:
        return "80–89"
    if score >= 50:
        return "50–79"
    return "0–49"


def load_catalog_stones():
    urls = []
    env_url = os.getenv("KURGIN_DATA_CATALOG_URL")
    if env_url:
        urls.append(env_url)
    urls.extend(DEFAULT_CATALOG_URLS)

    for url in urls:
        try:
            payload = _load_json_url(url)
            stones = [_normalize_stone(item) for item in _extract_stones(payload) if isinstance(item, dict)]
            if stones:
                return stones
        except (URLError, HTTPError, TimeoutError, json.JSONDecodeError, OSError):
            continue

    return [_normalize_stone(item) for item in LOCAL_STONES]
