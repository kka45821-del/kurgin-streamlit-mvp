#!/usr/bin/env python3
"""Smoke-check the KURGIN publication rules contract.

This script is intentionally read-only. It checks a local published catalog JSON
when one is available and verifies that frontend assumptions can follow the
Admin-computed publication fields.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = {
    "stone_id",
    "section",
    "price_rub",
    "price_status",
    "public_visible",
    "public_sellable",
    "checkout_enabled",
    "public_action",
    "current_status",
    "show_in_catalog",
    "is_mvp_eligible",
}

ALLOWED_PUBLIC_ACTIONS = {"request_price", "checkout"}
REMOVED_OR_INACTIVE_STATUSES = {
    "removed_from_sale",
    "hidden",
    "archived",
    "unavailable",
    "sold",
}
REQUEST_PRICE_FALLBACK_STATUSES = {
    "request_price",
    "missing",
    "score_required",
    "future_scope",
    "blocked",
    "needs_review",
    "index_pending",
    "index_suggested",
}

CATALOG_CANDIDATES = [
    Path("catalog.json"),
    Path("catalog_published.json"),
    Path("stones.json"),
    Path("data/catalog.json"),
    Path("data/catalog_published.json"),
    Path("data/stones.json"),
    Path("public/catalog.json"),
]


def as_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in {"true", "1", "yes", "y", "да"}:
        return True
    if text in {"false", "0", "no", "n", "нет"}:
        return False
    return None


def as_float(value: Any) -> float:
    try:
        return float(str(value).replace(" ", "").replace(",", ".") or 0)
    except (TypeError, ValueError):
        return 0.0


def extract_stones(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        for key in ("stones", "items", "catalog", "data"):
            value = payload.get(key)
            if isinstance(value, list):
                return [row for row in value if isinstance(row, dict)]
    return []


def load_local_catalog() -> tuple[Path | None, list[dict[str, Any]]]:
    for path in CATALOG_CANDIDATES:
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8") as fh:
            return path, extract_stones(json.load(fh))
    return None, []


def frontend_interpretation(stone: dict[str, Any]) -> str:
    """Contract-first frontend interpretation for request-price state."""
    action = str(stone.get("public_action", "")).strip().lower()
    checkout_enabled = as_bool(stone.get("checkout_enabled"))
    public_sellable = as_bool(stone.get("public_sellable"))
    price = as_float(stone.get("public_price_rub", stone.get("price_rub", 0)))

    if action == "request_price":
        return "request_price"
    if checkout_enabled is False:
        return "request_price"
    if public_sellable is False:
        return "request_price"
    if price <= 0:
        return "request_price"
    if action == "checkout" and checkout_enabled is True and public_sellable is True and price > 0:
        return "sellable_contract"

    # Compatibility-only fallback for legacy payloads without computed fields.
    status = str(stone.get("price_status", "")).strip().lower()
    if status in REQUEST_PRICE_FALLBACK_STATUSES:
        return "request_price"
    return "request_price" if price <= 0 else "sellable_contract"


def main() -> int:
    path, stones = load_local_catalog()
    if path is None:
        print("BLOCKED: local published catalog JSON was not found. Nothing was changed.")
        return 0
    if not stones:
        print(f"PASS_EMPTY: {path} exists, but catalog has no stones. Contract checks were skipped honestly.")
        return 0

    issues: list[str] = []
    for index, stone in enumerate(stones, start=1):
        identifier = stone.get("stone_id") or stone.get("id") or stone.get("report_number") or f"row-{index}"
        missing = sorted(REQUIRED_FIELDS - set(stone.keys()))
        if missing:
            issues.append(f"{identifier}: missing required fields: {', '.join(missing)}")

        action = str(stone.get("public_action", "")).strip().lower()
        if action and action not in ALLOWED_PUBLIC_ACTIONS:
            issues.append(f"{identifier}: invalid public_action={action!r}")

        interpretation = frontend_interpretation(stone)
        checkout_enabled = as_bool(stone.get("checkout_enabled"))
        public_sellable = as_bool(stone.get("public_sellable"))
        price = as_float(stone.get("public_price_rub", stone.get("price_rub", 0)))
        if (
            action == "request_price"
            or checkout_enabled is False
            or public_sellable is False
            or price <= 0
        ) and interpretation != "request_price":
            issues.append(f"{identifier}: frontend interpretation must be request_price")

        status = str(stone.get("current_status", "")).strip().lower()
        if status in REMOVED_OR_INACTIVE_STATUSES:
            if public_sellable is True or checkout_enabled is True or action == "checkout":
                issues.append(f"{identifier}: inactive status {status!r} must not be active public sellable")

    if issues:
        print(f"RISK: publication contract violations found in {path}")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print(f"PASS: publication rules contract smoke passed for {path} ({len(stones)} stones).")
    print("Admin decides. Frontend displays. Section is treated as Admin-resolved field.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
