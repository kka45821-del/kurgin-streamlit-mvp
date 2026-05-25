import html
import re

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
MANUAL_SECTIONS = {"colored", "side", "pairs", "exclusive"}

SECTION_ALIASES = {
    "мелкие": "small",
    "small": "small",
    "средние": "medium",
    "medium": "medium",
    "основной": "main",
    "основной каталог": "main",
    "main": "main",
    "крупные": "large",
    "large": "large",
    "цветные": "colored",
    "colored": "colored",
    "боковые": "side",
    "side": "side",
    "парные": "pairs",
    "pairs": "pairs",
    "эксклюзив": "exclusive",
    "exclusive": "exclusive",
}


def extract_stones(payload):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("stones", "catalog", "items", "data"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return []


def clean_text(value) -> str:
    if value in (None, ""):
        return ""
    text = str(value).strip()
    if text.lower() in {"nan", "none", "null"}:
        return ""
    return text


def first(stone: dict, *keys, default=""):
    for key in keys:
        value = stone.get(key)
        if value not in (None, ""):
            return value
    return default


def safe_float(value, default=0.0):
    try:
        if value in (None, ""):
            return default
        if isinstance(value, str):
            value = value.strip().replace(" ", "").replace(",", ".")
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_int(value, default=0):
    try:
        if value in (None, ""):
            return default
        if isinstance(value, str):
            value = value.strip().replace(" ", "").replace(",", ".")
        return int(float(value))
    except (TypeError, ValueError):
        return default


def safe_bool(value, default=False) -> bool:
    if value in (None, ""):
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y", "да"}


def is_round(shape: str) -> bool:
    return clean_text(shape).lower() in ROUND_SHAPES


def score_required(section: str, shape: str) -> bool:
    return section in SCORE_REQUIRED_SECTIONS and is_round(shape)


def report_required(section: str) -> bool:
    return section in REPORT_REQUIRED_SECTIONS


def normalize_section_key(value: str) -> str:
    if not value:
        return ""
    return SECTION_ALIASES.get(str(value).strip().lower(), "")


def auto_weight_section(carat: float) -> str:
    if carat < 0.30:
        return "small"
    if carat < 1.00:
        return "medium"
    if carat < 3.00:
        return "main"
    return "large"


def resolve_catalog_section(carat: float, section: str = "", is_colored: bool = False) -> str:
    normalized = normalize_section_key(section)
    if normalized in MANUAL_SECTIONS:
        return normalized
    if is_colored:
        return "colored"
    return auto_weight_section(carat)


def display_tags(stone: dict) -> str:
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


def format_decimal_ru(value, digits=2) -> str:
    number = safe_float(value, None)
    if number is None or number <= 0:
        return ""
    text = f"{number:.{digits}f}".rstrip("0").rstrip(".")
    return text.replace(".", ",")


def diameter_text(stone: dict) -> str:
    direct = first(stone, "diameter", "diameter_mm", "Diameter", "DiameterMM", default="")
    direct_text = clean_text(direct)
    if direct_text:
        if "мм" in direct_text.lower() or "mm" in direct_text.lower():
            return direct_text.replace("mm", "мм").replace("MM", "мм")
        number = format_decimal_ru(direct_text)
        return f"{number} мм" if number else direct_text

    measurements = first(stone, "measurements", "Measurements", "measurement", "Measurement", default="")
    measurements_text = clean_text(measurements)
    if not measurements_text:
        return ""

    numbers = re.findall(r"\d+(?:[\.,]\d+)?", measurements_text)
    if not numbers:
        return measurements_text

    if len(numbers) >= 2:
        a = safe_float(numbers[0])
        b = safe_float(numbers[1])
        avg = (a + b) / 2 if a > 0 and b > 0 else a
        formatted = format_decimal_ru(avg)
        return f"{formatted} мм" if formatted else measurements_text

    formatted = format_decimal_ru(numbers[0])
    return f"{formatted} мм" if formatted else measurements_text


def finish_text(stone: dict) -> str:
    cut = clean_text(first(stone, "cut", "Cut", default=""))
    polish = clean_text(first(stone, "polish", "Polish", default=""))
    symmetry = clean_text(first(stone, "symmetry", "Symmetry", default=""))
    existing = clean_text(first(stone, "finish", "finish_grade", default=""))

    parts = [x.upper() for x in (cut, polish, symmetry) if x]
    if parts:
        return " ".join(parts)
    return existing.upper() if existing else ""


def fluor_text(stone: dict) -> str:
    fluor = first(stone, "fluor", "fluorescence", "Fluorescence", "fluorescence_intensity", default="")
    fluor_text_value = clean_text(fluor)
    return fluor_text_value.lower() if fluor_text_value else ""


def meta_text(stone: dict) -> str:
    existing = clean_text(stone.get("meta"))
    if existing:
        return existing

    chunks = [diameter_text(stone), finish_text(stone), fluor_text(stone)]
    return " · ".join(chunk for chunk in chunks if chunk)


def weight_band(carat: float) -> str:
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


def score_band(score: float) -> str:
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


def normalize_stone(stone: dict) -> dict:
    normalized = dict(stone)

    carat = safe_float(first(normalized, "carat", "weight", "Weight", default=0))
    score = safe_float(first(normalized, "score", "karo_score", "Karo Score", default=0))
    price = safe_int(first(normalized, "price", "price_rub", "Price", "Price RUB", default=0))

    report = clean_text(first(normalized, "report", "report_number", "Report #", "certificate", "certificate_number", default=""))
    stone_id = clean_text(first(normalized, "id", "stone_id", "stock_number", "stock", "Stock #", default=""))
    if not stone_id:
        stone_id = report

    raw_section = first(normalized, "section", "catalog_section", "category", default="")
    is_colored = safe_bool(first(normalized, "is_colored", "colored", default=False))
    section = resolve_catalog_section(carat=carat, section=raw_section, is_colored=is_colored)

    price_text = normalized.get("priceText") or f"{price:,}".replace(",", " ")

    normalized["id"] = stone_id
    normalized["shape"] = clean_text(first(normalized, "shape", "Shape", default="Круг")) or "Круг"
    normalized["carat"] = carat
    normalized["color"] = clean_text(first(normalized, "color", "Color", default=""))
    normalized["clarity"] = clean_text(first(normalized, "clarity", "Clarity", default=""))
    normalized["score"] = score
    normalized["price"] = price
    normalized["priceText"] = price_text
    normalized["diameter"] = diameter_text(normalized)
    normalized["fluor"] = fluor_text(normalized)
    normalized["finish"] = finish_text(normalized)
    normalized["report"] = report
    normalized["meta"] = meta_text(normalized)
    normalized["tags"] = display_tags(normalized)
    normalized["availability"] = clean_text(first(normalized, "status", "current_status", "availability", default="available")) or "available"
    normalized["section"] = section
    normalized["weight"] = weight_band(carat)
    normalized["scoreBand"] = score_band(score)
    normalized["scoreRequired"] = score_required(section, normalized["shape"])
    normalized["reportRequired"] = report_required(section)
    return normalized


def validation_errors(stone: dict) -> list[str]:
    status = clean_text(first(stone, "status", "current_status", "availability", default="available")).lower()
    errors = []

    if status in HIDDEN_STATUSES:
        errors.append("hidden_status")
    if stone.get("show_in_catalog") is False:
        errors.append("show_in_catalog_false")
    if safe_float(stone.get("carat")) <= 0:
        errors.append("missing_carat")
    if safe_int(stone.get("price")) <= 0:
        errors.append("missing_price")
    if score_required(stone.get("section", ""), stone.get("shape", "")) and safe_float(stone.get("score")) <= 0:
        errors.append("missing_required_score")
    if not clean_text(stone.get("color")):
        errors.append("missing_color")
    if not clean_text(stone.get("clarity")):
        errors.append("missing_clarity")
    if report_required(stone.get("section", "")) and not clean_text(stone.get("report")):
        errors.append("missing_report")
    if not (clean_text(stone.get("id")) or clean_text(stone.get("report"))):
        errors.append("missing_id")

    return errors


def is_public_stone(stone: dict) -> bool:
    return not validation_errors(stone)


def normalize_public_stones(items) -> list[dict]:
    stones = [normalize_stone(item) for item in items if isinstance(item, dict)]
    return [stone for stone in stones if is_public_stone(stone)]
