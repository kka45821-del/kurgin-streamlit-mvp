from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from catalog.catalog_core import normalize_public_stones, normalize_stone


ACTIVE_STATE_FIELDS = (
    "payment_session",
    "payment_status",
    "payment_id",
    "order_id",
    "sold_at",
    "reserved_at",
    "reserve_until",
)


def _base_stone(**overrides) -> dict:
    stone = {
        "stone_id": "BASE-1",
        "shape": "Round",
        "carat": 1.2,
        "color": "F",
        "clarity": "VS1",
        "karo_score": 90,
        "report_number": "LG-BASE-1",
        "price_rub": 120000,
        "price_status": "confirmed",
        "public_action": "checkout",
        "checkout_enabled": True,
        "public_sellable": True,
        "current_status": "available",
        "show_in_catalog": True,
    }
    stone.update(overrides)
    return stone


def _normalized(stone: dict) -> dict:
    return normalize_stone(stone)


def _public_visible(stone: dict) -> bool:
    normalized_id = _normalized(stone)["id"]
    public_stones = normalize_public_stones([stone])
    return any(public_stone["id"] == normalized_id for public_stone in public_stones)


def _assert_no_active_state_fields(stone: dict) -> None:
    for field in ACTIVE_STATE_FIELDS:
        assert field not in stone, f"Unexpected active state field invented: {field}"


def test_available_price_stone() -> None:
    stone = _base_stone(stone_id="AVAILABLE-PRICE-1")
    normalized = _normalized(stone)
    assert _public_visible(stone) is True, normalized
    assert normalized["public_sellable"] is True, normalized
    assert normalized["checkout_enabled"] is True, normalized
    assert normalized["public_action"] == "checkout", normalized
    assert normalized["is_request_price"] is False, normalized
    _assert_no_active_state_fields(normalized)
    print("OK: available stone with confirmed price")


def test_request_price_stone() -> None:
    stone = _base_stone(
        stone_id="REQUEST-PRICE-1",
        price_rub=0,
        price_status="request_price",
        public_action="request_price",
        checkout_enabled=False,
        public_sellable=False,
    )
    normalized = _normalized(stone)
    assert _public_visible(stone) is True, normalized
    assert normalized["public_sellable"] is False, normalized
    assert normalized["checkout_enabled"] is False, normalized
    assert normalized["public_action"] == "request_price", normalized
    assert normalized["is_request_price"] is True, normalized
    assert normalized["priceText"] == "по запросу", normalized
    _assert_no_active_state_fields(normalized)
    print("OK: request-price stone remains non-buyable")


def test_missing_price_stone() -> None:
    stone = _base_stone(
        stone_id="MISSING-PRICE-1",
        price_rub=0,
        price_status="missing",
        public_action="request_price",
        checkout_enabled=True,
        public_sellable=True,
    )
    normalized = _normalized(stone)
    assert normalized["public_sellable"] is False, normalized
    assert normalized["checkout_enabled"] is False, normalized
    assert normalized["public_action"] == "request_price", normalized
    assert normalized["is_request_price"] is True, normalized
    assert normalized["priceText"] == "по запросу", normalized
    _assert_no_active_state_fields(normalized)
    print("OK: missing price cannot become checkout-enabled")


def test_sold_unavailable_stones() -> None:
    for status in ("sold", "unavailable"):
        stone = _base_stone(
            stone_id=f"STATUS-{status.upper()}-1",
            current_status=status,
            checkout_enabled=False,
            public_sellable=False,
            public_action="request_price",
        )
        normalized = _normalized(stone)
        assert _public_visible(stone) is False, normalized
        assert normalized["public_sellable"] is False, normalized
        assert normalized["checkout_enabled"] is False, normalized
        assert status in normalized["blocking_errors"] or "not_hidden_status" in normalized["blocking_errors"], normalized
        _assert_no_active_state_fields(normalized)
    print("OK: sold/unavailable stones stay non-public and non-buyable")


def test_blocked_operational_states() -> None:
    for status in ("reserved", "payment-blocked", "paid-order-processing"):
        stone = _base_stone(
            stone_id=f"BLOCKED-{status.upper()}-1",
            current_status=status,
            price_status="blocked",
            public_action="request_price",
            checkout_enabled=False,
            public_sellable=False,
        )
        normalized = _normalized(stone)
        assert normalized["public_sellable"] is False, normalized
        assert normalized["checkout_enabled"] is False, normalized
        assert normalized["is_request_price"] is True, normalized
        assert normalized["priceText"] == "по запросу", normalized
        _assert_no_active_state_fields(normalized)
    print("OK: reserved/payment-blocked/paid-order-processing stay non-buyable")


def test_forbidden_drift() -> None:
    request_only = _base_stone(
        stone_id="REQUEST-ONLY-1",
        price_rub=0,
        price_status="request_price",
        public_action="request_price",
        checkout_enabled=True,
        public_sellable=True,
    )
    normalized_request = _normalized(request_only)
    assert normalized_request["public_sellable"] is False, normalized_request
    assert normalized_request["checkout_enabled"] is False, normalized_request
    assert normalized_request["public_action"] == "request_price", normalized_request

    missing_price = _base_stone(
        stone_id="NO-PRICE-DRIFT-1",
        price_rub="",
        price_status="confirmed",
        public_action="checkout",
        checkout_enabled=True,
        public_sellable=True,
    )
    normalized_missing_price = _normalized(missing_price)
    assert normalized_missing_price["public_sellable"] is False, normalized_missing_price
    assert normalized_missing_price["checkout_enabled"] is False, normalized_missing_price
    assert normalized_missing_price["is_request_price"] is True, normalized_missing_price

    _assert_no_active_state_fields(normalized_request)
    _assert_no_active_state_fields(normalized_missing_price)
    print("OK: forbidden drift checks")


def run() -> None:
    test_available_price_stone()
    test_request_price_stone()
    test_missing_price_stone()
    test_sold_unavailable_stones()
    test_blocked_operational_states()
    test_forbidden_drift()
    print("SMOKE_CATALOG_PUBLIC_STATE_CONTRACT_OK")


if __name__ == "__main__":
    run()
