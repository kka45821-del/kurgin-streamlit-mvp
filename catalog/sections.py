CATALOG_SECTIONS = [
    {
        "key": "small",
        "title": "Мелкие",
        "subtitle": "0.00–0.29 ct",
        "enabled": True,
        "order": 1,
        "mode": "auto_weight",
        "min_carat": 0.00,
        "max_carat": 0.30,
    },
    {
        "key": "medium",
        "title": "Средние",
        "subtitle": "0.30–0.99 ct",
        "enabled": True,
        "order": 2,
        "mode": "auto_weight",
        "min_carat": 0.30,
        "max_carat": 1.00,
    },
    {
        "key": "main",
        "title": "Основной каталог",
        "subtitle": "1.00–2.99 ct",
        "enabled": True,
        "order": 3,
        "mode": "auto_weight",
        "min_carat": 1.00,
        "max_carat": 3.00,
    },
    {
        "key": "large",
        "title": "Крупные",
        "subtitle": "3.00+ ct",
        "enabled": True,
        "order": 4,
        "mode": "auto_weight",
        "min_carat": 3.00,
        "max_carat": None,
    },
    {
        "key": "colored",
        "title": "Цветные",
        "subtitle": "",
        "enabled": True,
        "order": 5,
        "mode": "manual",
    },
    {
        "key": "side",
        "title": "Боковые",
        "subtitle": "",
        "enabled": True,
        "order": 6,
        "mode": "manual",
    },
    {
        "key": "pairs",
        "title": "Парные",
        "subtitle": "",
        "enabled": True,
        "order": 7,
        "mode": "manual",
    },
    {
        "key": "exclusive",
        "title": "Эксклюзив",
        "subtitle": "",
        "enabled": True,
        "order": 8,
        "mode": "manual",
    },
]

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

MANUAL_SECTIONS = {"colored", "side", "pairs", "exclusive"}
AUTO_WEIGHT_SECTIONS = {"small", "medium", "main", "large"}


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

    # Special manual sections always have priority over carat-based sections.
    if normalized in MANUAL_SECTIONS:
        return normalized

    if is_colored:
        return "colored"

    # Weight sections are always recalculated from carat to avoid misplaced stones,
    # for example 3.00+ ct accidentally appearing in the main catalog.
    return auto_weight_section(carat)


def enabled_sections() -> list[dict]:
    return sorted(
        [section for section in CATALOG_SECTIONS if section.get("enabled")],
        key=lambda item: item.get("order", 999),
    )
