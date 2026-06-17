import csv
import io
import json
import os
import re
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from catalog.catalog_core import extract_stones, normalize_public_stones
from catalog.stones import STONES as LOCAL_STONES

CATALOG_LOADER_VERSION = "state_v2_public_stones_v1"

DEFAULT_CATALOG_URLS = [
    "https://raw.githubusercontent.com/kka45821-del/kurgin-data/main/public_stones_v1.csv",
    "https://raw.githubusercontent.com/kka45821-del/kurgin-data/main/catalog.json",
    "https://raw.githubusercontent.com/kka45821-del/kurgin-data/main/stones.json",
    "https://raw.githubusercontent.com/kka45821-del/kurgin-data/main/catalog_published.json",
    "https://raw.githubusercontent.com/kka45821-del/kurgin-data/main/data/catalog.json",
    "https://raw.githubusercontent.com/kka45821-del/kurgin-data/main/stones.csv",
]


def _read_url(url: str) -> str:
    with urlopen(url, timeout=5) as response:
        return response.read().decode("utf-8-sig")


def _clean(value) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _numeric_price(value: str) -> str:
    text = _clean(value)
    digits = re.sub(r"[^0-9]", "", text)
    return digits


def _avg_diameter(row: dict) -> str:
    raw_min = _clean(row.get("min_diameter"))
    raw_max = _clean(row.get("max_diameter"))
    try:
        min_value = float(raw_min.replace(",", ".")) if raw_min else 0.0
        max_value = float(raw_max.replace(",", ".")) if raw_max else 0.0
    except ValueError:
        return raw_min or raw_max

    if min_value > 0 and max_value > 0:
        return f"{((min_value + max_value) / 2):.2f}"
    if min_value > 0:
        return f"{min_value:.2f}"
    if max_value > 0:
        return f"{max_value:.2f}"
    return ""


def _is_public_stones_v1_row(row: dict) -> bool:
    return any(
        key in row
        for key in (
            "public_card_status",
            "price_display_type",
            "public_price_display",
            "availability_status_public",
        )
    )


def _adapt_public_stones_v1_row(row: dict) -> dict:
    """Map Admin public_stones_v1.csv rows to the current mobile catalog contract.

    The public site must not calculate prices or infer admin-only state. It only
    adapts public-safe export fields into the existing display keys used by the
    MVP shell.
    """
    if not _is_public_stones_v1_row(row):
        return row

    adapted = dict(row)
    price_display_type = _clean(row.get("price_display_type")).lower()
    public_price_display = _clean(row.get("public_price_display"))
    numeric_price = _numeric_price(public_price_display) if price_display_type == "numeric" else ""
    is_numeric = bool(numeric_price)

    stone_id = _clean(row.get("stone_id"))
    report_number = _clean(row.get("report_number"))
    weight = _clean(row.get("weight"))
    score = _clean(row.get("kurgin_score"))
    section = _clean(row.get("catalog_section")) or "main"
    availability = _clean(row.get("availability_status_public")) or "in_stock"

    public_action = "checkout" if is_numeric else "request_price"
    checkout_enabled = "true" if is_numeric else "false"
    public_sellable = "true" if is_numeric else "false"
    price_status = "calculated" if is_numeric else "request_price"

    adapted.update({
        "id": stone_id or report_number,
        "stone_id": stone_id,
        "report": report_number,
        "report_number": report_number,
        "carat": weight,
        "weight": weight,
        "score": score,
        "karo_score": score,
        "kurgin_score": score,
        "price": numeric_price,
        "price_rub": numeric_price,
        "public_price_rub": numeric_price,
        "price_status": price_status,
        "public_action": public_action,
        "checkout_enabled": checkout_enabled,
        "public_sellable": public_sellable,
        "availability": "available" if availability in {"in_stock", "available"} else availability,
        "status": "available" if availability in {"in_stock", "available"} else availability,
        "current_status": "available" if availability in {"in_stock", "available"} else availability,
        "section": section,
        "catalog_section": section,
        "shape": _clean(row.get("shape")),
        "color": _clean(row.get("color")),
        "clarity": _clean(row.get("clarity")),
        "cut": _clean(row.get("cut_grade")) or _clean(row.get("cut")),
        "polish": _clean(row.get("polish")),
        "symmetry": _clean(row.get("symmetry")),
        "fluorescence": _clean(row.get("fluorescence")),
        "diameter_mm": _avg_diameter(row),
        "depth_mm": _clean(row.get("height")) or _clean(row.get("depth_mm")),
        "tags": _clean(row.get("tags")),
        "show_in_catalog": True,
        "public_card_status": _clean(row.get("public_card_status")),
        "public_visibility_reason": _clean(row.get("public_visibility_reason")),
    })
    return adapted


def _load_csv_text(raw: str) -> list[dict]:
    if not raw.strip():
        return []

    reader = csv.DictReader(io.StringIO(raw))
    if not reader.fieldnames:
        return []

    rows = []
    for row in reader:
        normalized_row = {_clean(key): _clean(value) for key, value in row.items() if key is not None}
        if not any(normalized_row.values()):
            continue
        rows.append(_adapt_public_stones_v1_row(normalized_row))
    return rows


def _load_url(url: str):
    raw = _read_url(url)
    lower_url = url.lower().split("?", 1)[0]
    if lower_url.endswith(".csv"):
        return _load_csv_text(raw)
    return json.loads(raw)


def _catalog_state(status: str, stones: list[dict], *, source: str, attempted_remote: int = 0, remote_empty: int = 0, remote_errors: int = 0) -> dict:
    notices = {
        "remote_loaded": "Каталог загружен.",
        "fallback_used": "Показана резервная демо-выборка.",
        "empty": "Каталог пока пуст. Попробуйте проверить публикацию данных позже.",
        "error": "Каталог временно недоступен. Попробуйте открыть страницу позже.",
    }
    return {
        "status": status,
        "source": source,
        "count": len(stones),
        "attempted_remote": attempted_remote,
        "remote_empty": remote_empty,
        "remote_errors": remote_errors,
        "loader_version": CATALOG_LOADER_VERSION,
        "public_notice": notices.get(status, notices["remote_loaded"]),
        "stones": stones,
    }


def load_catalog_state() -> dict:
    urls = []
    env_url = os.getenv("KURGIN_DATA_CATALOG_URL")
    if env_url:
        urls.append(env_url)
    urls.extend(DEFAULT_CATALOG_URLS)

    remote_empty = 0
    remote_errors = 0

    for url in urls:
        try:
            payload = _load_url(url)
            stones = normalize_public_stones(extract_stones(payload))
            if stones:
                return _catalog_state(
                    "remote_loaded",
                    stones,
                    source=url,
                    attempted_remote=len(urls),
                    remote_empty=remote_empty,
                    remote_errors=remote_errors,
                )
            remote_empty += 1
        except (URLError, HTTPError, TimeoutError, json.JSONDecodeError, csv.Error, OSError, UnicodeDecodeError):
            remote_errors += 1
            continue

    fallback_stones = normalize_public_stones(LOCAL_STONES)
    if fallback_stones:
        return _catalog_state(
            "fallback_used",
            fallback_stones,
            source="local_fallback",
            attempted_remote=len(urls),
            remote_empty=remote_empty,
            remote_errors=remote_errors,
        )

    status = "error" if remote_errors else "empty"
    return _catalog_state(
        status,
        [],
        source="none",
        attempted_remote=len(urls),
        remote_empty=remote_empty,
        remote_errors=remote_errors,
    )


def load_catalog_stones():
    return load_catalog_state()["stones"]
