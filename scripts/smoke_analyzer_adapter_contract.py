from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from services.analyzer_adapter import FORBIDDEN_OUTPUT_KEYS, analyze_public_stone


def assert_no_forbidden_keys(value: Any, path: str = "response") -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            assert key not in FORBIDDEN_OUTPUT_KEYS, f"Forbidden key {key!r} found at {path}"
            assert_no_forbidden_keys(nested, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            assert_no_forbidden_keys(item, f"{path}[{index}]")


def assert_contract(response: dict, expected_status: str) -> None:
    required_keys = {"status", "score_band", "coefficient", "summary", "warnings", "limitations", "next_action"}
    assert set(response.keys()) == required_keys, f"Unexpected response keys: {sorted(response.keys())}"
    assert response["status"] == expected_status, response
    assert isinstance(response["warnings"], list), response
    assert isinstance(response["limitations"], list), response
    assert response["summary"], response
    assert response["next_action"], response
    assert_no_forbidden_keys(response)


def complete_round_payload() -> dict:
    return {
        "shape": "Round",
        "carat": 1.25,
        "color": "E",
        "clarity": "VS1",
        "table_pct": 57.0,
        "depth_pct": 61.8,
        "crown_angle": 34.7,
        "pavilion_angle": 40.8,
        "crown_height": 15.0,
        "pavilion_depth": 43.0,
        "girdle": 3.5,
        "fluorescence": "None",
        "report_number": "LG123456789",
    }


def test_complete_round_returns_ok() -> None:
    response = analyze_public_stone(complete_round_payload())
    assert_contract(response, "ok")
    assert response["score_band"] == "preview_ready", response
    assert response["coefficient"] is None, response


def test_missing_geometry_returns_incomplete() -> None:
    payload = complete_round_payload()
    payload.pop("table_pct")
    payload.pop("depth_pct")
    response = analyze_public_stone(payload)
    assert_contract(response, "incomplete")


def test_unsupported_shape_returns_unsupported_shape() -> None:
    payload = complete_round_payload()
    payload["shape"] = "Oval"
    response = analyze_public_stone(payload)
    assert_contract(response, "unsupported_shape")


def test_bad_carat_returns_invalid_input() -> None:
    payload = complete_round_payload()
    payload["carat"] = "bad"
    response = analyze_public_stone(payload)
    assert_contract(response, "invalid_input")


def test_missing_required_fields_returns_invalid_input() -> None:
    payload = complete_round_payload()
    payload.pop("color")
    response = analyze_public_stone(payload)
    assert_contract(response, "invalid_input")


def main() -> None:
    tests = [
        test_complete_round_returns_ok,
        test_missing_geometry_returns_incomplete,
        test_unsupported_shape_returns_unsupported_shape,
        test_bad_carat_returns_invalid_input,
        test_missing_required_fields_returns_invalid_input,
    ]
    for test in tests:
        test()
    print("Analyzer adapter contract smoke checks passed.")


if __name__ == "__main__":
    main()
