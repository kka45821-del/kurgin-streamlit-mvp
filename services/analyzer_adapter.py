from __future__ import annotations

from typing import Any

STATUS_OK = "ok"
STATUS_INCOMPLETE = "incomplete"
STATUS_UNSUPPORTED_SHAPE = "unsupported_shape"
STATUS_INVALID_INPUT = "invalid_input"
STATUS_ENGINE_UNAVAILABLE = "engine_unavailable"

REQUIRED_FIELDS = ("shape", "carat", "color", "clarity")
IMPORTANT_GEOMETRY_FIELDS = ("table_pct", "depth_pct", "crown_angle", "pavilion_angle")
OPTIONAL_GEOMETRY_FIELDS = ("crown_height", "pavilion_depth", "girdle")
OPTIONAL_PUBLIC_FIELDS = ("fluorescence", "report_number")
SUPPORTED_SHAPES = {"round", "round brilliant", "круг", "круглый"}

FORBIDDEN_OUTPUT_KEYS = {
    "raw_formula",
    "weights",
    "penalty_breakdown",
    "penalty_breakdown_internal",
    "internal_diagnostics",
    "debug_trace",
    "traceback",
    "exception",
    "stack",
    "raw_engine_output",
    "formula_source",
    "coefficient_formula",
    "certificate_claim",
    "appraisal_claim",
    "price_effect",
    "order_effect",
    "reserve_effect",
    "payment_effect",
}

BASE_LIMITATIONS = [
    "Не является сертификатом.",
    "Не является оценкой стоимости.",
    "Не является геммологическим заключением.",
    "Формула и внутренние коэффициенты не раскрываются.",
]


def _clean_text(value: Any) -> str:
    return str(value or "").strip()


def _normalize_shape(value: Any) -> str:
    return _clean_text(value).lower().replace("ё", "е")


def _is_missing(value: Any) -> bool:
    if value is None:
        return True
    text = str(value).strip()
    return text == "" or text.lower() in {"none", "nan", "null"}


def _to_positive_float(value: Any, field_name: str) -> tuple[float | None, str | None]:
    if _is_missing(value):
        return None, f"{field_name}: missing"
    try:
        number = float(str(value).replace(",", "."))
    except (TypeError, ValueError):
        return None, f"{field_name}: invalid number"
    if number <= 0:
        return None, f"{field_name}: must be positive"
    return number, None


def _response(
    *,
    status: str,
    summary: str,
    warnings: list[str] | None = None,
    next_action: str,
    score_band: str | None = None,
    coefficient: None = None,
) -> dict[str, Any]:
    response: dict[str, Any] = {
        "status": status,
        "score_band": score_band,
        "coefficient": coefficient,
        "summary": summary,
        "warnings": warnings or [],
        "limitations": list(BASE_LIMITATIONS),
        "next_action": next_action,
    }
    for forbidden_key in FORBIDDEN_OUTPUT_KEYS:
        response.pop(forbidden_key, None)
    return response


def analyze_public_stone(payload: dict) -> dict:
    """Return a public-safe Analyzer preview response.

    This is a Phase 2 boundary stub. It intentionally performs no formula
    calculation and imports no KURGIN Score Analyzer engine modules.
    """
    if not isinstance(payload, dict):
        return _response(
            status=STATUS_INVALID_INPUT,
            summary="Некорректный запрос Analyzer preview.",
            warnings=["Payload must be an object."],
            next_action="fix_input",
        )

    missing_required = [field for field in REQUIRED_FIELDS if _is_missing(payload.get(field))]
    if missing_required:
        return _response(
            status=STATUS_INVALID_INPUT,
            summary="Не хватает обязательных параметров для Analyzer preview.",
            warnings=[f"Missing required fields: {', '.join(missing_required)}."],
            next_action="fix_input",
        )

    shape = _normalize_shape(payload.get("shape"))
    if shape not in SUPPORTED_SHAPES:
        return _response(
            status=STATUS_UNSUPPORTED_SHAPE,
            summary="Эта огранка пока не поддерживается в public preview.",
            warnings=["Текущий public MVP adapter stub поддерживает только Round."],
            next_action="request_professional_review",
        )

    _, carat_error = _to_positive_float(payload.get("carat"), "carat")
    if carat_error:
        return _response(
            status=STATUS_INVALID_INPUT,
            summary="Некорректное значение carat.",
            warnings=[carat_error],
            next_action="fix_input",
        )

    numeric_errors: list[str] = []
    missing_geometry: list[str] = []
    for field in IMPORTANT_GEOMETRY_FIELDS:
        value = payload.get(field)
        if _is_missing(value):
            missing_geometry.append(field)
            continue
        _, error = _to_positive_float(value, field)
        if error:
            numeric_errors.append(error)

    for field in OPTIONAL_GEOMETRY_FIELDS:
        value = payload.get(field)
        if _is_missing(value):
            continue
        _, error = _to_positive_float(value, field)
        if error:
            numeric_errors.append(error)

    if numeric_errors:
        return _response(
            status=STATUS_INVALID_INPUT,
            summary="Некоторые числовые параметры заполнены некорректно.",
            warnings=numeric_errors,
            next_action="fix_input",
        )

    if missing_geometry:
        return _response(
            status=STATUS_INCOMPLETE,
            summary="Недостаточно геометрических параметров для предварительной интерпретации.",
            warnings=[
                "Missing geometry fields: " + ", ".join(missing_geometry) + ".",
                "Engine не подключён; это contract-safe preview response.",
            ],
            next_action="add_missing_parameters",
        )

    return _response(
        status=STATUS_OK,
        score_band="preview_ready",
        summary="Public-safe Analyzer adapter stub принял полный Round input. Реальный расчёт формулы не выполнялся.",
        warnings=["Engine не подключён; результат является mock response для проверки adapter contract."],
        next_action="connect_engine_adapter_later",
    )
