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


def _normalize_stone(stone: dict) -> dict:
    normalized = dict(stone)

    carat = normalized.get("carat", normalized.get("weight", 0))
    try:
        carat = float(carat)
    except (TypeError, ValueError):
        carat = 0.0

    score = normalized.get("score", normalized.get("karo_score", 0))
    try:
        score = float(score)
    except (TypeError, ValueError):
        score = 0.0

    price = normalized.get("price", normalized.get("price_rub", 0))
    try:
        price = int(float(price))
    except (TypeError, ValueError):
        price = 0

    price_text = normalized.get("priceText") or f"{price:,}".replace(",", " ")

    normalized.setdefault("shape", "Круг")
    normalized["carat"] = carat
    normalized.setdefault("color", "")
    normalized.setdefault("clarity", "")
    normalized["score"] = score
    normalized["price"] = price
    normalized["priceText"] = price_text
    normalized.setdefault("diameter", "")
    normalized.setdefault("meta", "")
    normalized.setdefault("fluor", normalized.get("fluorescence", ""))
    normalized.setdefault("finish", "")
    normalized.setdefault("report", normalized.get("report_number", ""))
    normalized.setdefault("tags", "")
    normalized.setdefault("section", _section_by_carat(carat))
    normalized.setdefault("weight", _weight_band(carat))
    normalized.setdefault("scoreBand", _score_band(score))
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
