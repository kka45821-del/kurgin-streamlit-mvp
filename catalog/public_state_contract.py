from catalog import catalog_core as core


def has_value(stone: dict, key: str) -> bool:
    return stone.get(key) not in (None, "")


def request_price_state(stone: dict, price: int | None = None) -> bool:
    if has_value(stone, "is_request_price"):
        return core.safe_bool(stone.get("is_request_price"))

    action = core.clean_text(core.first(stone, "public_action", default="")).lower()
    if action:
        return action == "request_price"

    state = core.clean_text(core.first(stone, "public_state", default="")).lower()
    if state:
        return state != "checkout"

    if has_value(stone, "checkout_enabled"):
        return not core.safe_bool(stone.get("checkout_enabled"))

    return core.is_request_price_state(stone, price)


def is_public_stone(stone: dict) -> bool:
    if has_value(stone, "public_visible"):
        return core.safe_bool(stone.get("public_visible"))
    return core.is_public_stone(stone)


def normalize_stone(stone: dict) -> dict:
    normalized = core.normalize_stone(stone)
    price = core.safe_int(core.first(normalized, "price", "price_rub", "public_price_rub", default=0))
    request = request_price_state(stone, price)

    action = core.clean_text(core.first(stone, "public_action", default="")).lower()
    state = core.clean_text(core.first(stone, "public_state", default="")).lower()
    reason = core.clean_text(core.first(stone, "public_reason", default=""))

    checkout_enabled = False if request else core.safe_bool(core.first(stone, "checkout_enabled", default=normalized.get("checkout_enabled", False)))
    public_sellable = False if request else core.safe_bool(core.first(stone, "public_sellable", default=normalized.get("public_sellable", False)))

    if not action:
        action = "request_price" if request else "checkout"
    if not state:
        state = "checkout" if checkout_enabled else "sellable_contact" if public_sellable else "request_price"

    carat = normalized.get("carat", 0) or 0
    price_text = "по запросу" if request else f"{price:,}".replace(",", " ")
    price_per_ct = round(price / carat, 2) if not request and price > 0 and carat > 0 else 0

    normalized.update({
        "public_action": action,
        "checkout_enabled": checkout_enabled,
        "public_sellable": public_sellable,
        "is_request_price": request,
        "public_state": state,
        "public_reason": reason or normalized.get("public_reason", ""),
        "price_per_ct": price_per_ct,
        "priceText": price_text,
        "priceDisplay": price_text,
    })
    return normalized


def normalize_public_stones(items) -> list[dict]:
    normalized = [normalize_stone(item) for item in items if isinstance(item, dict)]
    return [stone for stone in normalized if is_public_stone(stone)]
