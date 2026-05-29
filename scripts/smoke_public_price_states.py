from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from catalog.catalog_core import normalize_public_stones, normalize_stone
from config.request_contacts import REQUEST_CONTACTS
from ui.mobile_shell import build_mobile_shell


REQUEST_STONE = {
    "stone_id": "REQ-1",
    "shape": "Round",
    "carat": 1.2,
    "color": "F",
    "clarity": "VS1",
    "karo_score": 90,
    "report_number": "LG-REQ-1",
    "price_rub": 0,
    "price_status": "request_price",
    "public_action": "request_price",
    "checkout_enabled": False,
    "public_sellable": False,
    "current_status": "available",
    "show_in_catalog": True,
}

SELLABLE_STONE = {
    "stone_id": "SELL-1",
    "shape": "Round",
    "carat": 1.2,
    "color": "F",
    "clarity": "VS1",
    "karo_score": 90,
    "report_number": "LG-SELL-1",
    "price_rub": 120000,
    "price_status": "confirmed",
    "public_action": "checkout",
    "checkout_enabled": True,
    "public_sellable": True,
    "current_status": "available",
    "show_in_catalog": True,
}

ACTIVE_COMMERCE_PATTERNS = (
    "createOrder",
    "paymentSession",
    "startPayment",
    "initPayment",
    "initiatePayment",
    "sberPayment",
    "checkoutPayment",
    "markSold",
    "soldState",
    "reserveStone",
    "createReserve",
)


def run() -> None:
    assert REQUEST_CONTACTS["phone"], REQUEST_CONTACTS
    assert REQUEST_CONTACTS["max_url"].startswith("https://max.ru/"), REQUEST_CONTACTS
    assert REQUEST_CONTACTS["telegram_url"].startswith("https://t.me/"), REQUEST_CONTACTS
    assert REQUEST_CONTACTS["whatsapp_url"].startswith("https://wa.me/"), REQUEST_CONTACTS
    print("OK: request contacts config")

    request_stone = normalize_stone(REQUEST_STONE)
    assert request_stone["priceText"] == "по запросу", request_stone
    assert request_stone["priceDisplay"] == "по запросу", request_stone
    assert request_stone["is_request_price"] is True, request_stone
    assert request_stone["checkout_enabled"] is False, request_stone
    assert request_stone["public_sellable"] is False, request_stone
    assert "0 ₽" not in f"{request_stone.get('priceText', '')} ₽"
    print("OK: request price state")

    sellable_stone = normalize_stone(SELLABLE_STONE)
    assert sellable_stone["priceText"] != "по запросу", sellable_stone
    assert sellable_stone["is_request_price"] is False, sellable_stone
    assert sellable_stone["checkout_enabled"] is True, sellable_stone
    assert sellable_stone["public_sellable"] is True, sellable_stone
    assert sellable_stone["price"] == 120000, sellable_stone
    print("OK: sellable price state")

    public_stones = normalize_public_stones([REQUEST_STONE, SELLABLE_STONE])
    assert len(public_stones) == 2, public_stones
    by_id = {stone["id"]: stone for stone in public_stones}
    assert by_id["REQ-1"]["priceText"] == "по запросу", by_id["REQ-1"]
    assert by_id["SELL-1"]["priceText"] != "по запросу", by_id["SELL-1"]
    print("OK: normalize_public_stones price states")

    shell = build_mobile_shell(page="catalog", stones_json="[]")
    assert "kurginFavoritesV01" in shell
    assert "function getFavorites()" in shell
    assert "function saveFavorites(items)" in shell
    assert "function addFavorite(stone)" in shell
    assert "function removeFavorite(stoneId)" in shell
    assert "function isFavorite(stoneOrId)" in shell
    assert "function toggleFavorite(stone)" in shell
    assert "Избранное помогает сохранить интересные камни в этом браузере" in shell
    assert "Оно не резервирует камни и не фиксирует цену" in shell
    assert "checkout" in shell
    for pattern in ACTIVE_COMMERCE_PATTERNS:
        assert pattern not in shell, f"Active commerce pattern found: {pattern}"
    assert "заявка не является заказом" in shell.lower()
    assert "не фиксирует цену" in shell.lower()
    assert "не резервирует" in shell.lower()
    print("OK: favorites localStorage helpers and safe inactive commerce boundary")

    print("SMOKE_PUBLIC_PRICE_STATES_OK")


if __name__ == "__main__":
    run()
