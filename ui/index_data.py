from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PUBLIC_INDEX_ROWS: list[tuple[str, str, str, int]] = [
    ("D", "IF", "1.00–1.49", 250),
    ("D", "IF", "1.50–1.99", 380),
    ("D", "IF", "2.00–2.49", 480),
    ("D", "VVS1", "1.00–1.49", 125),
    ("D", "VVS1", "1.50–1.99", 150),
    ("D", "VVS1", "2.00–2.49", 170),
    ("D", "VVS1", "2.50–2.99", 210),
    ("D", "VVS1", "3.00–3.49", 245),
    ("D", "VVS1", "4.00–4.49", 325),
    ("D", "VVS2", "1.00–1.49", 110),
    ("D", "VVS2", "1.50–1.99", 115),
    ("D", "VVS2", "2.00–2.49", 120),
    ("D", "VVS2", "2.50–2.99", 125),
    ("D", "VVS2", "3.00–3.49", 135),
    ("D", "VVS2", "3.50–3.99", 145),
    ("D", "VVS2", "4.00–4.49", 160),
    ("D", "VVS2", "4.50–4.99", 170),
    ("D", "VS1", "1.00–1.49", 100),
    ("D", "VS1", "1.50–1.99", 100),
    ("D", "VS1", "2.00–2.49", 105),
    ("D", "VS1", "2.50–2.99", 115),
    ("D", "VS1", "3.00–3.49", 125),
    ("D", "VS1", "3.50–3.99", 130),
    ("E", "IF", "1.00–1.49", 185),
    ("E", "VVS1", "1.00–1.49", 120),
    ("E", "VVS1", "1.50–1.99", 145),
    ("E", "VVS1", "2.00–2.49", 150),
    ("E", "VVS1", "2.50–2.99", 160),
    ("E", "VVS1", "3.00–3.49", 165),
    ("E", "VVS2", "1.00–1.49", 105),
    ("E", "VVS2", "1.50–1.99", 110),
    ("E", "VVS2", "2.00–2.49", 105),
    ("E", "VVS2", "2.50–2.99", 100),
    ("E", "VVS2", "3.00–3.49", 100),
    ("E", "VS1", "1.00–1.49", 95),
    ("E", "VS1", "1.50–1.99", 98),
    ("E", "VS1", "2.00–2.49", 98),
    ("E", "VS1", "2.50–2.99", 98),
    ("E", "VS1", "3.00–3.49", 98),
    ("E", "VS1", "3.50–3.99", 100),
    ("E", "VS1", "4.00–4.49", 100),
    ("E", "VS1", "4.50–4.99", 105),
    ("F", "IF", "1.00–1.49", 150),
    ("F", "IF", "1.50–1.99", 150),
    ("F", "VVS1", "1.00–1.49", 115),
    ("F", "VVS1", "1.50–1.99", 135),
    ("F", "VVS1", "2.00–2.49", 145),
    ("F", "VVS1", "2.50–2.99", 155),
    ("F", "VVS1", "3.00–3.49", 155),
    ("F", "VVS1", "4.50–4.99", 175),
    ("F", "VVS2", "1.00–1.49", 100),
    ("F", "VVS2", "1.50–1.99", 100),
    ("F", "VVS2", "2.00–2.49", 100),
    ("F", "VVS2", "2.50–2.99", 100),
    ("F", "VVS2", "3.00–3.49", 100),
    ("F", "VVS2", "3.50–3.99", 100),
    ("F", "VVS2", "4.00–4.49", 105),
    ("F", "VVS2", "4.50–4.99", 105),
    ("F", "VS1", "1.00–1.49", 95),
    ("F", "VS1", "1.50–1.99", 95),
    ("F", "VS1", "2.00–2.49", 95),
    ("F", "VS1", "2.50–2.99", 95),
    ("F", "VS1", "3.00–3.49", 95),
    ("F", "VS1", "3.50–3.99", 98),
    ("F", "VS1", "4.00–4.49", 100),
    ("F", "VS1", "4.50–4.99", 100),
    ("G", "VVS1", "2.00–2.49", 110),
    ("G", "VVS2", "3.00–3.49", 95),
    ("G", "VS1", "1.50–1.99", 95),
    ("G", "VS1", "2.00–2.49", 95),
    ("G", "VS1", "3.00–3.49", 95),
]

INDEX_COLORS = ["D", "E", "F", "G"]
INDEX_CLARITIES = ["IF", "VVS1", "VVS2", "VS1", "VS2", "SI1"]
INDEX_BANDS = [
    ("1.00–1.49", "1–1.49"),
    ("1.50–1.99", "1.5–1.99"),
    ("2.00–2.49", "2–2.49"),
    ("2.50–2.99", "2.5–2.99"),
    ("3.00–3.49", "3–3.49"),
    ("3.50–3.99", "3.5–3.99"),
    ("4.00–4.49", "4–4.49"),
    ("4.50–4.99", "4.5–4.99"),
]

PUBLIC_INDEX_SNAPSHOT_PATHS = (
    Path("public_index.json"),
    Path(__file__).resolve().parents[1] / "public_index.json",
)


def _carat_band_label(carat_band_from: float, carat_band_to: float) -> str:
    return f"{carat_band_from:.2f}–{carat_band_to:.2f}"


def _normalize_public_index_row(row: dict[str, Any]) -> tuple[str, str, str, int] | None:
    status = str(row.get("status", "")).strip().lower()
    if status and status != "ok":
        return None

    color = str(row.get("color", "")).strip().upper()
    clarity = str(row.get("clarity", "")).strip().upper()
    if not color or not clarity:
        return None

    try:
        carat_band_from = float(row.get("carat_band_from"))
        carat_band_to = float(row.get("carat_band_to"))
        index_value = int(float(row.get("index_value_usd_per_ct")))
    except (TypeError, ValueError):
        return None

    if index_value <= 0 or carat_band_to <= carat_band_from:
        return None

    return color, clarity, _carat_band_label(carat_band_from, carat_band_to), index_value


def _load_rows_from_snapshot(path: Path) -> list[tuple[str, str, str, int]]:
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    raw_rows = data.get("rows", []) if isinstance(data, dict) else data
    if not isinstance(raw_rows, list):
        return []

    rows: list[tuple[str, str, str, int]] = []
    for raw_row in raw_rows:
        if not isinstance(raw_row, dict):
            continue
        normalized = _normalize_public_index_row(raw_row)
        if normalized is not None:
            rows.append(normalized)
    return rows


def load_public_index_rows() -> list[tuple[str, str, str, int]]:
    for path in PUBLIC_INDEX_SNAPSHOT_PATHS:
        if not path.exists():
            continue
        try:
            rows = _load_rows_from_snapshot(path)
        except (OSError, json.JSONDecodeError):
            continue
        if rows:
            return rows
    return PUBLIC_INDEX_ROWS
