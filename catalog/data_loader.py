import html
import json
import os
import re
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from catalog.sections import resolve_catalog_section
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

HIDDEN_STATUSES = {"hidden", "draft", "deleted", "sold", "unavailable", "reserved_hidden"}
ROUND_SHAPES = {"round", "круг"}
REPORT_REQUIRED_SECTIONS = {"main", "large"}
SCORE_REQUIRED_SECTIONS = {"main", "large"}


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


def _first(stone: dict, *keys, default=""):
    for key in keys:
        value = stone.get(key)
        if value not in (None, ""):
            return value
    return default


def _safe_float(value, default=0.0):
    try:
        if value in (None, ""):
            return default
        if isinstance(value, str):
            value = value.strip().replace(" ", "").replace(",", ".")
        return float(value)
    except (TypeError, ValueError):
        return default


def _safe_int(value, default=0):
    try:
        if value in (None, ""):
            return default
        if isinstance(value, str):
            value = value.strip().replace(" ", "").replace(",", ".")
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _safe_bool(value, default=False) -> bool:
    if value in (None, ""):
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y", "да"}


def _clean_text(value) -> str:
    if value in (None, ""):
        return ""
    text = str(value).strip()
    if text.lower() in {"nan", "none", "null"}:
        return ""
    return text


def _is_round(shape: str) -> bool:
    return _clean_text(shape).lower() in ROUND_SHAPES


def _score_required(section: str, shape: str) -> bool:
    return section in SCORE_REQUIRED_SECTIONS and _is_round(shape)


def _report_required(section: str) -> bool:
    return section in REPORT_REQUIRED_SECTIONS


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


def _format_decimal_ru(value, digits=2) -> str:
    number = _safe_float(value, None)
    if number is None or number <= 0:
        return ""
    text = f"{number:.{digits}f}".rstrip("0").rstrip(".")
    return text.replace(".", ",")


def _diameter_text(stone: dict) -> str:
    direct = _first(stone, "diameter", "diameter_mm", "Diameter", "DiameterMM", default="")
    direct_text = _clean_text(direct)
    if direct_text:
        if "мм" in direct_text.lower() or "mm" in direct_text.lower():
            return direct_text.replace("mm", "мм").replace("MM", "мм")
        number = _format_decimal_ru(direct_text)
        return f"{number} мм" if number else direct_text

    measurements = _first(stone, "measurements", "Measurements", "measurement", "Measurement", default="")
    measurements_text = _clean_text(measurements)
    if not measurements_text:
        return ""

    # Common formats: 6.55x6.58x4.04, 6.55 - 6.58 x 4.04, 6.55*6.58*4.04
    numbers = re.findall(r"\d+(?:[\.,]\d+)?", measurements_text)
    if not numbers:
        return measurements_text

    if len(numbers) >= 2:
        a = _safe_float(numbers[0])
        b = _safe_float(numbers[1])
        avg = (a + b) / 2 if a > 0 and b > 0 else a
        formatted = _format_decimal_ru(avg)
        return f"{formatted} мм" if formatted else measurements_text

    formatted = _format_decimal_ru(numbers[0])
    return f"{formatted} мм" if formatted else measurements_text


def _finish_text(stone: dict) -> str:
    cut = _clean_text(_first(stone, "cut", "Cut", default=""))
    polish = _clean_text(_first(stone, "polish", "Polish", default=""))
    symmetry = _clean_text(_first(stone, "symmetry", "Symmetry", default=""))
    existing = _clean_text(_first(stone, "finish", "finish_grade", default=""))

    parts = [x.upper() for x in (cut, polish, symmetry) if x]
    if parts:
        return " ".join(parts)
    return existing.upper() if existing else ""


def _fluor_text(stone: dict) -> str:
    fluor = _first(stone, "fluor", "fluorescence", "Fluorescence", "fluorescence_intensity", default="")
    fluor_text = _clean_text(fluor)
    return fluor_text.lower() if fluor_text else ""


def _meta(stone: dict) -> str:
    existing = _clean_text(stone.get("meta"))
    if existing:
        return existing

    chunks = [_diameter_text(stone), _finish_text(stone), _fluor_text(stone)]
    return " · ".join(chunk for chunk in chunks if chunk)


def _normalize_stone(stone: dict) -> dict:
    normalized = dict(stone)

    carat = _safe_float(_first(normalized, "carat", "weight", "Weight", default=0))
    score = _safe_float(_first(normalized, "score", "karo_score", "Karo Score", default=0))
    price = _safe_int(_first(normalized, "price", "price_rub", "Price", "Price RUB", default=0))

    report = _clean_text(_first(normalized, "report", "report_number", "Report #", "certificate", "certificate_number", default=""))
    stone_id = _clean_text(_first(normalized, "id", "stone_id", "stock_number", "stock", "Stock #", default=""))
    if not stone_id:
        stone_id = report

    raw_section = _first(normalized, "section", "catalog_section", "category", default="")
    is_colored = _safe_bool(_first(normalized, "is_colored", "colored", default=False))
    section = resolve_catalog_section(carat=carat, section=raw_section, is_colored=is_colored)

    price_text = normalized.get("priceText") or f"{price:,}".replace(",", " ")

    normalized["id"] = stone_id
    normalized["shape"] = _clean_text(_first(normalized, "shape", "Shape", default="Круг")) or "Круг"
    normalized["carat"] = carat
    normalized["color"] = _clean_text(_first(normalized, "color", "Color", default=""))
    normalized["clarity"] = _clean_text(_first(normalized, "clarity", "Clarity", default=""))
    normalized["score"] = score
    normalized["price"] = price
    normalized["priceText"] = price_text
    normalized["diameter"] = _diameter_text(normalized)
    normalized["fluor"] = _fluor_text(normalized)
    normalized["finish"] = _finish_text(normalized)
    normalized["report"] = report
    normalized["meta"] = _meta(normalized)
    normalized["tags"] = _display_tags(normalized)
    normalized["availability"] = _clean_text(_first(normalized, "status", "current_status", "availability", default="available")) or "available"
    normalized["section"] = section
    normalized["weight"] = _weight_band(carat)
    normalized["scoreBand"] = _score_band(score)
    normalized["scoreRequired"] = _score_required(section, normalized["shape"])
    normalized["reportRequired"] = _report_required(section)
    return normalized


def _is_public_stone(stone: dict) -> bool:
    status = _clean_text(_first(stone, "status", "current_status", "availability", default="available")).lower()
    if status in HIDDEN_STATUSES:
        return False
    if stone.get("show_in_catalog") is False:
        return False
    if _safe_float(stone.get("carat")) <= 0:
        return False
    if _safe_int(stone.get("price")) <= 0:
        return False
    if _score_required(stone.get("section", ""), stone.get("shape", "")) and _safe_float(stone.get("score")) <= 0:
        return False
    if not _clean_text(stone.get("color")):
        return False
    if not _clean_text(stone.get("clarity")):
        return False
    if _report_required(stone.get("section", "")) and not _clean_text(stone.get("report")):
        return False
    if not (_clean_text(stone.get("id")) or _clean_text(stone.get("report"))):
        return False
    return True


def _normalize_public_stones(items) -> list[dict]:
    stones = [_normalize_stone(item) for item in items if isinstance(item, dict)]
    return [stone for stone in stones if _is_public_stone(stone)]


def _weight_band(carat: float) -> str:
    if 1.0 <= carat < 1.5:
        return "1–1.49"
    if 1.5 <= carat < 2.0:
        return "1.5–1.99"
    if 2.0 <= carat < 2.5:
        return "2–2.49"
    if 2.5 <= carat < 3.0:
        return "2.5–2.99"
    if carat >= 3.0:
        return "3+"
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
            stones = _normalize_public_stones(_extract_stones(payload))
            if stones:
                return stones
        except (URLError, HTTPError, TimeoutError, json.JSONDecodeError, OSError):
            continue

    return _normalize_public_stones(LOCAL_STONES)
