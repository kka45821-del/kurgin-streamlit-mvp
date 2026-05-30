from __future__ import annotations

from typing import Any

STATUS_OK = "ok"
STATUS_INCOMPLETE = "incomplete"
STATUS_UNSUPPORTED = "unsupported"
STATUS_ERROR = "error"

REQUIRED_GEOMETRY_FIELDS = (
    "table_pct",
    "depth_pct",
    "crown_angle",
    "pavilion_angle",
    "crown_height",
    "pavilion_depth",
    "girdle",
)
OPTIONAL_PUBLIC_FIELDS = ("carat", "color", "clarity", "fluorescence", "report_number")
SUPPORTED_SHAPES = {"round", "round brilliant", "круг", "круглый"}

FORBIDDEN_OUTPUT_KEYS = {
    "diagnostics",
    "breakdown",
    "triple_score",
    "structure_modifier",
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
]

ALLOWED_PUBLIC_KEYS = {
    "status",
    "score_band",
    "summary",
    "warnings",
    "limitations",
    "next_action",
}


def _clean_text(value: Any) -> str:
    return str(value or "").strip()


def _normalize_shape(value: Any) -> str:
    return _clean_text(value).lower().replace("ё", "е")


def _is_missing(value: Any) -> bool:
    if value is None:
        return True
    text = str(value).strip()
    return text == "" or text.lower() in {"none", "nan", "null", "—", "-"}


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
    score_band: str,
    summary: str,
    warnings: list[str] | None = None,
    next_action: str = "request_professional_review",
) -> dict[str, Any]:
    response: dict[str, Any] = {
        "status": status,
        "score_band": score_band,
        "summary": summary,
        "warnings": warnings or [],
        "limitations": list(BASE_LIMITATIONS),
        "next_action": next_action,
    }
    return {key: response[key] for key in ALLOWED_PUBLIC_KEYS}


def analyze_public_stone(payload: dict) -> dict:
    """Return a public-safe Analyzer preview response.

    This is a UI-only preview/mock boundary. It performs no live backend call,
    no Formula Service call, and imports no Analyzer engine modules.
    """
    if not isinstance(payload, dict):
        return _response(
            status=STATUS_ERROR,
            score_band="Unavailable",
            summary="Некорректный запрос Analyzer public preview.",
            warnings=["Public preview input must be an object."],
        )

    shape = _normalize_shape(payload.get("shape") or "Round")
    if shape not in SUPPORTED_SHAPES:
        return _response(
            status=STATUS_UNSUPPORTED,
            score_band="Unsupported",
            summary="Эта огранка пока не поддерживается в public preview.",
            warnings=["Текущий public preview поддерживает только Round."],
        )

    numeric_errors: list[str] = []
    missing_geometry: list[str] = []

    if not _is_missing(payload.get("carat")):
        _, carat_error = _to_positive_float(payload.get("carat"), "carat")
        if carat_error:
            numeric_errors.append(carat_error)

    for field in REQUIRED_GEOMETRY_FIELDS:
        value = payload.get(field)
        if _is_missing(value):
            missing_geometry.append(field)
            continue
        _, error = _to_positive_float(value, field)
        if error:
            numeric_errors.append(error)

    if numeric_errors:
        return _response(
            status=STATUS_ERROR,
            score_band="Unavailable",
            summary="Некоторые числовые параметры заполнены некорректно.",
            warnings=numeric_errors,
        )

    if missing_geometry:
        return _response(
            status=STATUS_INCOMPLETE,
            score_band="Review",
            summary="Недостаточно геометрических параметров для предварительной интерпретации.",
            warnings=[
                "Missing geometry fields: " + ", ".join(missing_geometry) + ".",
                "Это preview/mock; реальный расчёт формулы не выполняется.",
            ],
        )

    return _response(
        status=STATUS_OK,
        score_band="Review",
        summary="Public-safe Analyzer preview принял полный Round input. Реальный расчёт формулы не выполнялся.",
        warnings=["Preview/mock mode: результат не является расчётом Formula Service."],
        next_action="request_professional_review",
    )
