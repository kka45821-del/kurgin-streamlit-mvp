from catalog import catalog_core as core


def _has_key(stone: dict, key: str) -> bool:
    value = stone.get(key)
    return value not in (None, "")


def is_request_price_state(stone: dict, price: int | None = None) -> bool:
    """Trust Admin-published public state first, then fall back to legacy rules.

    New catalog_mvp_v3 payloads already contain the final commercial display
    decision. The public site should display that decision, not recalculate it
    from price_status or other internal workflow flags.
    """
    if _has_key(stone, "is_request_price"):
        return core.safe_bool(stone.get("is_request_price"))

    public_action = core.clean_text(core.first(stone, "public_action", default="")).lower()
    if public_action:
        return public_action == "request_price"

    public_state = core.clean_text(core.first(stone, "public_state", default="")).lower()
    if public_state:
        return public_state != "checkout"

    if _has_key(stone, "checkout_enabled"):
        return not core.safe_bool(stone.get("checkout_enabled"))

    return core.is_request_price_state(stone, price)


def is_public_stone(stone: dict) -> bool:
    if _has_key(stone, "public_visible"):
        return core.safe_bool(stone.get("public_visible"))
    return core.is_public_stone(stone)


def normalize_stone(stone: dict) -> dict:
    normalized = core.normalize_stone(stone)
    price = core.safe_int(core.first(normalized, "price", "price_rub", "public_price_rub", default=0))
    request_price = is_request_price_state(stone, price)

    raw_action = core.clean_text(core.first(stone, "public_action", default="")).lower()
    raw_state = core.clean_text(core.first(stone, "public_state", default="")).lower()
    raw_reason = core.clean_text(core.first(stone, "public_reason", default=""))

    public_action = raw_action or ("request_price" if request_price else "checkout")
    checkout_enabled = False if request_price else core.safe_bool(core.first(stone, "checkout_enabled", default=normalized.get("checkout_enabled", False)))
    public_sellable = False if request_price else core.safe_bool(core.first(stone, "public_sellable", default=normalized.get("public_sellable", False)))

    if raw_state:
        public_state = raw_state
    elif checkout_enabled:
        public_state = "checkout"
    elif public_sellable:
        public_state = "sellable_contact"
    else:
        public_state = "request_price"

    price_text = "по запросу" if request_price else f"{price:,}".replace(",", " ")
    price_per_ct = round(price / normalized.get("carat", 0), 2) if not request_price and price > 0 and normalized.get("carat", 0) > 0 else 0

    normalized.update({
        "public_action": public_action,
        "checkout_enabled": checkout_enabled,
        "public_sellable": public_sellable,
        "is_request_price": request_price,
        "public_state": public_state,
        "public_reason": raw_reason or normalized.get("public_reason", ""),
        "price_per_ct": price_per_ct,
        "priceText": price_text,
        "priceDisplay": price_text,
    })
    return normalized


def normalize_public_stones(items) -> list[dict]:
    stones = [normalize_stone(item) for item in items if isinstance(item, dict)]
    return [stone for stone in stones if is_public_stone(stone)]
