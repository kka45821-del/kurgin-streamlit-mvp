import html
import re

TAG_LABELS = {
    "огонь": "О", "fire": "О",
    "блеск": "Б", "brilliance": "Б",
    "контраст": "К", "contrast": "К",
    "баланс": "БАЛАНС", "balance": "БАЛАНС",
    "цена": "ЦЕНА", "price": "ЦЕНА",
    "крупный": "КРУПНЫЙ", "large": "КРУПНЫЙ",
    "овал": "ОВАЛ", "oval": "ОВАЛ",
    "капля": "PEAR", "pear": "PEAR",
    "кушон": "CUSHION", "cushion": "CUSHION",
    "проверка": "ПРОВЕРКА", "review": "ПРОВЕРКА",
}

HIDDEN_STATUSES = {"hidden", "draft", "deleted", "sold", "unavailable", "reserved_hidden"}
ROUND_SHAPES = {"round", "круг"}
REPORT_REQUIRED_SECTIONS = {"main", "large"}
SCORE_REQUIRED_SECTIONS = {"main", "large"}
INDEX_SECTIONS = {"main", "large"}
INDEX_AVAILABILITY = "available"
MANUAL_SECTIONS = {"colored", "side", "pairs", "exclusive"}

SECTION_ALIASES = {
    "мелкие": "small", "small": "small",
    "средние": "medium", "medium": "medium",
    "основной": "main", "основной каталог": "main", "main": "main",
    "крупные": "large", "large": "large",
    "цветные": "colored", "colored": "colored",
    "боковые": "side", "side": "side",
    "парные": "pairs", "pairs": "pairs",
    "эксклюзив": "exclusive", "exclusive": "exclusive",
}

SHAPE_ALIASES = {
    "round": "Round", "round brilliant": "Round", "round brilliant cut": "Round", "rbc": "Round", "круг": "Round",
    "oval": "Oval", "овал": "Oval",
    "pear": "Pear", "pear shape": "Pear", "капля": "Pear",
    "cushion": "Cushion", "кушон": "Cushion",
}

RULE_LIBRARY = {
    "show_in_catalog": "Публикация включена",
    "not_hidden_status": "Статус не скрывает камень",
    "id_required": "ID / stock number обязателен",
    "availability_required": "Статус наличия обязателен",
    "price_warning": "Цена не заполнена",
    "price_required": "Цена обязательна",
    "carat_required": "Карат обязателен",
    "size_or_carat_required": "Размер в мм или карат обязателен",
    "quantity_required": "Количество обязательно",
    "color_required": "Цвет обязателен",
    "clarity_required": "Чистота обязательна",
    "report_required": "Report / сертификат обязателен",
    "karo_score_required_round": "KURGIN Score обязателен для Round / Круг",
    "color_type_required": "Описание цветного камня обязательно",
    "pair_id_required": "ID пары обязателен",
    "side_type_required": "Тип бокового камня обязателен",
    "measurements_warning": "Желательно заполнить measurements / диаметр",
    "finish_warning": "Желательно заполнить Cut / Polish / Symmetry",
    "fluorescence_warning": "Желательно заполнить fluorescence",
    "report_warning": "Желательно заполнить report / сертификат",
    "karo_score_warning": "KURGIN Score отсутствует или ещё не применим",
}

COMMON_BLOCKING_RULES = ["show_in_catalog", "not_hidden_status", "id_required", "availability_required"]
COMMON_WARNINGS = ["price_warning"]

SECTION_RULE_MATRIX = {
    "main": {
        "blocking": COMMON_BLOCKING_RULES + ["carat_required", "color_required", "clarity_required", "report_required", "karo_score_required_round"],
        "warnings": COMMON_WARNINGS + ["measurements_warning", "finish_warning", "fluorescence_warning"],
    },
    "large": {
        "blocking": COMMON_BLOCKING_RULES + ["carat_required", "color_required", "clarity_required", "report_required", "karo_score_required_round"],
        "warnings": COMMON_WARNINGS + ["measurements_warning", "finish_warning", "fluorescence_warning"],
    },
    "medium": {
        "blocking": COMMON_BLOCKING_RULES + ["carat_required", "color_required", "clarity_required"],
        "warnings": COMMON_WARNINGS + ["report_warning", "karo_score_warning", "measurements_warning", "fluorescence_warning"],
    },
    "small": {
        "blocking": COMMON_BLOCKING_RULES + ["size_or_carat_required", "quantity_required"],
        "warnings": COMMON_WARNINGS + ["report_warning", "karo_score_warning"],
    },
    "colored": {
        "blocking": COMMON_BLOCKING_RULES + ["size_or_carat_required", "color_type_required"],
        "warnings": COMMON_WARNINGS + ["report_warning", "karo_score_warning", "measurements_warning"],
    },
    "side": {
        "blocking": COMMON_BLOCKING_RULES + ["size_or_carat_required", "quantity_required", "side_type_required"],
        "warnings": COMMON_WARNINGS + ["report_warning", "karo_score_warning"],
    },
    "pairs": {
        "blocking": COMMON_BLOCKING_RULES + ["size_or_carat_required", "quantity_required", "pair_id_required"],
        "warnings": COMMON_WARNINGS + ["report_warning", "karo_score_warning"],
    },
    "exclusive": {
        "blocking": COMMON_BLOCKING_RULES + ["size_or_carat_required"],
        "warnings": COMMON_WARNINGS + ["report_warning", "karo_score_warning", "measurements_warning"],
    },
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


def clean_text_keep_none(value) -> str:
    if value in (None, ""):
        return ""
    text = str(value).strip()
    if text.lower() in {"nan", "null"}:
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
        if isinstance(value, str):
            match = re.search(r"\d+(?:[\.,]\d+)?", value)
            if match:
                try:
                    return float(match.group(0).replace(",", "."))
                except ValueError:
                    pass
        return default


def safe_int(value, default=0):
    try:
        if value in (None, ""):
            return default
        if isinstance(value, str):
            value = value.strip().replace(" ", "").replace(",", ".")
        return int(float(value))
    except (TypeError, ValueError):
        if isinstance(value, str):
            match = re.search(r"\d+", value)
            if match:
                try:
                    return int(match.group(0))
                except ValueError:
                    pass
        return default


def safe_bool(value, default=False) -> bool:
    if value in (None, ""):
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y", "да"}


def normalize_shape(value: str) -> str:
    raw = clean_text(value)
    if not raw:
        return "Круг"
    key = raw.lower().strip()
    return SHAPE_ALIASES.get(key, raw.title() if raw.isupper() else raw)


def is_round(shape: str) -> bool:
    return normalize_shape(shape).lower() == "round"


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
    direct = first(stone, "diameter", "diameter_mm", "size_mm", "Diameter", "DiameterMM", default="")
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
    fluor_text_value = clean_text_keep_none(fluor)
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


def has_size_or_carat(stone: dict) -> bool:
    return safe_float(stone.get("carat")) > 0 or bool(diameter_text(stone))


def quantity_value(stone: dict) -> int:
    return safe_int(first(stone, "quantity", "qty", "count", "pcs", "pieces", "PCS/CTS", "шт", default=0))


def color_type_value(stone: dict) -> str:
    return clean_text(first(stone, "color_type", "color_hue", "color_intensity", "fancy_color", "color_description", default=""))


def side_type_value(stone: dict) -> str:
    return clean_text(first(stone, "side_type", "side_shape", "side_stone_type", default=""))


def pair_id_value(stone: dict) -> str:
    return clean_text(first(stone, "pair_id", "pair_number", "pair", default=""))


def rule_failed(rule_key: str, stone: dict) -> bool:
    status = clean_text(first(stone, "status", "current_status", "availability", default=stone.get("availability") or "available")).lower()
    checks = {
        "show_in_catalog": lambda: stone.get("show_in_catalog") is False,
        "not_hidden_status": lambda: status in HIDDEN_STATUSES,
        "id_required": lambda: not (clean_text(stone.get("id")) or clean_text(stone.get("report"))),
        "availability_required": lambda: not clean_text(stone.get("availability")),
        "price_required": lambda: safe_int(stone.get("price")) <= 0,
        "price_warning": lambda: safe_int(stone.get("price")) <= 0,
        "carat_required": lambda: safe_float(stone.get("carat")) <= 0,
        "size_or_carat_required": lambda: not has_size_or_carat(stone),
        "quantity_required": lambda: quantity_value(stone) <= 0,
        "color_required": lambda: not clean_text(stone.get("color")),
        "clarity_required": lambda: not clean_text(stone.get("clarity")),
        "report_required": lambda: not clean_text(stone.get("report")),
        "karo_score_required_round": lambda: is_round(stone.get("shape")) and safe_float(stone.get("score")) <= 0,
        "color_type_required": lambda: not color_type_value(stone),
        "pair_id_required": lambda: not pair_id_value(stone),
        "side_type_required": lambda: not side_type_value(stone),
        "measurements_warning": lambda: not diameter_text(stone),
        "finish_warning": lambda: not finish_text(stone),
        "fluorescence_warning": lambda: not fluor_text(stone),
        "report_warning": lambda: not clean_text(stone.get("report")),
        "karo_score_warning": lambda: safe_float(stone.get("score")) <= 0,
    }
    return checks.get(rule_key, lambda: False)()


def section_rules(section: str) -> dict:
    return SECTION_RULE_MATRIX.get(section, SECTION_RULE_MATRIX["main"])


def admin_section_rules() -> dict:
    return {
        section: {
            "blocking": [{"key": key, "label": RULE_LIBRARY[key]} for key in rules["blocking"]],
            "warnings": [{"key": key, "label": RULE_LIBRARY[key]} for key in rules["warnings"]],
        }
        for section, rules in SECTION_RULE_MATRIX.items()
    }


def validation_errors(stone: dict) -> list[str]:
    rules = section_rules(stone.get("section", "main"))
    return [rule for rule in rules["blocking"] if rule_failed(rule, stone)]


def validation_warnings(stone: dict) -> list[str]:
    rules = section_rules(stone.get("section", "main"))
    return [rule for rule in rules["warnings"] if rule_failed(rule, stone)]


def publication_status(stone: dict) -> str:
    if validation_errors(stone):
        return "blocked"
    if validation_warnings(stone):
        return "warning"
    return "ready"


def index_exclusion_reason(stone: dict) -> str:
    availability = clean_text(stone.get("availability")).lower()
    if availability != INDEX_AVAILABILITY:
        return "not_available"
    if stone.get("section") not in INDEX_SECTIONS:
        return "wrong_section"
    if not is_round(stone.get("shape")):
        return "not_round"
    if safe_float(stone.get("carat")) <= 0:
        return "missing_carat"
    if safe_int(stone.get("price")) <= 0:
        return "missing_public_price"
    if not clean_text(stone.get("color")):
        return "missing_color"
    if not clean_text(stone.get("clarity")):
        return "missing_clarity"
    if safe_float(stone.get("score")) <= 0:
        return "missing_karo_score"
    return ""


def index_eligible(stone: dict) -> bool:
    return index_exclusion_reason(stone) == ""


def index_bucket(stone: dict) -> str:
    if not index_eligible(stone):
        return ""
    shape = "round"
    carat_group = stone.get("weight") or weight_band(stone.get("carat", 0))
    color = clean_text(stone.get("color")).upper()
    clarity = clean_text(stone.get("clarity")).upper()
    score_group = stone.get("scoreBand") or score_band(safe_float(stone.get("score")))
    return f"{shape}|{carat_group}|{color}|{clarity}|{score_group}"


def normalize_stone(stone: dict) -> dict:
    normalized = dict(stone)
    carat = safe_float(first(normalized, "carat", "weight", "Weight", default=0))
    score = safe_float(first(normalized, "score", "karo_score", "kurgin_score", "Karo Score", "KURGIN Score", "KURGIN SCORE", default=0))
    price = safe_int(first(normalized, "price", "price_rub", "public_price_rub", "Price", "Price RUB", default=0))
    report = clean_text(first(normalized, "report", "report_number", "Report #", "certificate", "certificate_number", default=""))
    stone_id = clean_text(first(normalized, "id", "stone_id", "stock_number", "stock", "Stock #", default="")) or report
    raw_section = first(normalized, "section", "catalog_section", "category", default="")
    is_colored = safe_bool(first(normalized, "is_colored", "colored", default=False))
    section = resolve_catalog_section(carat=carat, section=raw_section, is_colored=is_colored)
    shape = normalize_shape(first(normalized, "shape", "Shape", "description", "DESCRIPTION", default="Круг"))
    price_text = normalized.get("priceText") or f"{price:,}".replace(",", " ")
    price_per_ct = round(price / carat, 2) if price > 0 and carat > 0 else 0

    normalized.update({
        "id": stone_id,
        "shape": shape,
        "carat": carat,
        "color": clean_text(first(normalized, "color", "Color", default="")),
        "clarity": clean_text(first(normalized, "clarity", "Clarity", default="")),
        "score": score,
        "price": price,
        "public_price_rub": price,
        "currency": clean_text(first(normalized, "currency", default="RUB")) or "RUB",
        "price_date": clean_text(first(normalized, "price_date", "upload_date", "updated_at", default="")),
        "price_source": clean_text(first(normalized, "price_source", "source", "supplier_name", default="admin_upload")) or "admin_upload",
        "price_per_ct": price_per_ct,
        "priceText": price_text,
        "diameter": diameter_text(normalized),
        "fluor": fluor_text(normalized),
        "finish": finish_text(normalized),
        "report": report,
        "meta": meta_text(normalized),
        "tags": display_tags(normalized),
        "availability": clean_text(first(normalized, "status", "current_status", "availability", default="available")) or "available",
        "section": section,
        "quantity": quantity_value(normalized),
        "color_type": color_type_value(normalized),
        "pair_id": pair_id_value(normalized),
        "side_type": side_type_value(normalized),
        "weight": weight_band(carat),
        "scoreBand": score_band(score),
    })
    normalized["scoreRequired"] = score_required(section, normalized["shape"])
    normalized["reportRequired"] = report_required(section)
    normalized["blocking_errors"] = validation_errors(normalized)
    normalized["warnings"] = validation_warnings(normalized)
    normalized["publication_status"] = publication_status(normalized)
    normalized["index_eligible"] = index_eligible(normalized)
    normalized["index_exclusion_reason"] = index_exclusion_reason(normalized)
    normalized["index_bucket"] = index_bucket(normalized)
    return normalized


def is_public_stone(stone: dict) -> bool:
    return not validation_errors(stone)


def normalize_public_stones(items) -> list[dict]:
    stones = [normalize_stone(item) for item in items if isinstance(item, dict)]
    return [stone for stone in stones if is_public_stone(stone)]


def import_diagnostics(items) -> dict:
    normalized = [normalize_stone(item) for item in items if isinstance(item, dict)]
    summary = {"total": len(normalized), "ready": 0, "warning": 0, "blocked": 0, "by_section": {}, "blocking_rules": {}, "warning_rules": {}, "stones": []}
    for stone in normalized:
        status = stone.get("publication_status")
        section = stone.get("section") or "unknown"
        summary[status] += 1
        summary["by_section"].setdefault(section, {"total": 0, "ready": 0, "warning": 0, "blocked": 0})
        summary["by_section"][section]["total"] += 1
        summary["by_section"][section][status] += 1
        for rule in stone.get("blocking_errors", []):
            summary["blocking_rules"][rule] = summary["blocking_rules"].get(rule, 0) + 1
        for rule in stone.get("warnings", []):
            summary["warning_rules"][rule] = summary["warning_rules"].get(rule, 0) + 1
        summary["stones"].append({"id": stone.get("id"), "title": stone.get("title", ""), "section": section, "status": status, "blocking_errors": stone.get("blocking_errors", []), "warnings": stone.get("warnings", [])})
    return summary
