# ANALYZER ADAPTER CONTRACT v0.1

Repo: `kka45821-del/kurgin-streamlit-mvp`
Scope: public MVP adapter contract only.
Status: docs-only contract / no production code change.

This document defines the safe contract for a future Analyzer adapter between the public MVP UI and any KURGIN Score Analyzer engine.

It is based on `docs/ANALYZER_INTEGRATION_PLAN_V0_1.md` and must be followed before any future engine integration.

## 1. Purpose

The Analyzer adapter must protect the public MVP from unstable engine behavior, formula disclosure, unsafe legal wording, and accidental checkout/payment/order/reserve logic.

The adapter is responsible for:

- accepting only approved public input fields;
- validating input safely;
- calling the future Analyzer engine only through a controlled boundary;
- returning only public-safe output;
- hiding formula internals;
- converting errors into safe user-facing states;
- preventing traceback, debug data, and internal exception text from reaching the UI.

## 2. Public input schema

The public MVP may send only this input shape to the adapter.

```json
{
  "shape": "Round",
  "carat": 1.0,
  "color": "D",
  "clarity": "VVS1",
  "table_pct": 58.0,
  "depth_pct": 61.5,
  "crown_angle": 34.5,
  "pavilion_angle": 40.8,
  "crown_height": 15.0,
  "pavilion_depth": 43.0,
  "girdle": "Medium",
  "fluorescence": "None",
  "report_number": "optional-public-reference"
}
```

### Required fields

Required for a basic request:

- `shape`
- `carat`
- `color`
- `clarity`

### Optional fields

Optional fields improve completeness but must not be required for the public preview:

- `table_pct`
- `depth_pct`
- `crown_angle`
- `pavilion_angle`
- `crown_height`
- `pavilion_depth`
- `girdle`
- `fluorescence`
- `report_number`

### Field notes

`shape` must be normalized by the adapter. Phase 1 should support only approved shapes. Unsupported shapes must return `unsupported_shape`, not crash.

`carat` must be numeric and positive.

`color` and `clarity` must be normalized to known public labels.

Optional numeric fields must be validated as numeric values if present. Invalid optional values should return `invalid_input` or field-level warnings, depending on severity.

`report_number` is a reference only. It must not be used as proof of certification or authenticity in the public MVP.

## 3. Validation states

The adapter must return one of the following public validation states.

### `ok`

Use when input is complete enough for a public-safe result.

### `incomplete`

Use when the adapter can show a limited preview but key parameters are missing.

Example causes:

- no table percentage;
- no depth percentage;
- no crown angle;
- no pavilion angle;
- limited geometry data.

### `unsupported_shape`

Use when shape is outside the approved public MVP scope.

Example message:

`Эта огранка пока не поддерживается в public preview.`

### `invalid_input`

Use when input is malformed or impossible.

Example causes:

- negative carat;
- non-numeric numeric field;
- invalid color label;
- invalid clarity label.

### `engine_unavailable`

Use when the future engine is unavailable, not installed, not reachable, or returns an unsafe/unexpected error.

The UI must show a safe user-facing message only.

## 4. Public output schema

The adapter may return only this public-safe output shape.

```json
{
  "status": "ok",
  "score_band": "Standard",
  "coefficient": "optional-approved-value",
  "summary": "Предварительная public-safe интерпретация результата.",
  "warnings": [],
  "limitations": [
    "Не является сертификатом.",
    "Не является оценкой стоимости.",
    "Не является геммологическим заключением."
  ],
  "next_action": "request_professional_review"
}
```

### Required output fields

- `status`
- `summary`
- `warnings`
- `limitations`
- `next_action`

### Optional output fields

- `score_band`
- `coefficient`

`coefficient` may be returned only if explicitly approved for public display. If not approved, it must be omitted or set to `null`.

## 5. Forbidden output

The adapter must never return these fields to the public MVP UI:

- `raw_formula`
- `weights`
- `penalty_breakdown`
- `penalty_breakdown_internal`
- `internal_diagnostics`
- `debug_trace`
- `traceback`
- `exception`
- `stack`
- `raw_engine_output`
- `formula_source`
- `coefficient_formula`
- `certificate_claim`
- `appraisal_claim`
- `price_effect`
- `order_effect`
- `reserve_effect`
- `payment_effect`

The adapter must not return anything implying:

- official certificate;
- official appraisal;
- guaranteed quality;
- guaranteed price;
- checkout readiness;
- payment readiness;
- reserve or ownership state;
- investment recommendation.

## 6. Error behavior

The public MVP must never show internal technical errors.

Forbidden error behavior:

- Python traceback;
- raw exception text;
- file path;
- module name that exposes internals;
- formula block name;
- debug payload;
- stack trace;
- engine internals.

Required error behavior:

```json
{
  "status": "engine_unavailable",
  "score_band": null,
  "coefficient": null,
  "summary": "Analyzer temporarily unavailable in public preview.",
  "warnings": ["Попробуйте позже или запросите профессиональный обзор."],
  "limitations": ["Не является сертификатом.", "Не является оценкой стоимости."],
  "next_action": "request_professional_review"
}
```

## 7. Example request JSON

```json
{
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
  "girdle": "Medium - Slightly Thick",
  "fluorescence": "None",
  "report_number": "LG123456789"
}
```

## 8. Example public response JSON

```json
{
  "status": "ok",
  "score_band": "High",
  "coefficient": null,
  "summary": "Предварительный public preview показывает сильный профиль при введённых параметрах.",
  "warnings": [],
  "limitations": [
    "Результат зависит от полноты и точности введённых параметров.",
    "Не является сертификатом.",
    "Не является оценкой стоимости.",
    "Не является геммологическим заключением."
  ],
  "next_action": "request_professional_review"
}
```

## 9. Example incomplete response JSON

```json
{
  "status": "incomplete",
  "score_band": null,
  "coefficient": null,
  "summary": "Недостаточно параметров для предварительной интерпретации.",
  "warnings": [
    "Добавьте table_pct и depth_pct.",
    "Для более точного preview нужны crown_angle и pavilion_angle."
  ],
  "limitations": [
    "Без геометрических параметров результат ограничен.",
    "Не является сертификатом.",
    "Не является оценкой стоимости.",
    "Формула и внутренние коэффициенты не раскрываются."
  ],
  "next_action": "add_missing_parameters"
}
```

## 10. Example unsupported shape response JSON

```json
{
  "status": "unsupported_shape",
  "score_band": null,
  "coefficient": null,
  "summary": "Эта огранка пока не поддерживается в public preview.",
  "warnings": ["Текущий public MVP может ограничиваться Round."],
  "limitations": ["Не является сертификатом.", "Не является геммологическим заключением."],
  "next_action": "request_professional_review"
}
```

## 11. Future implementation acceptance criteria

A future implementation task connecting the adapter must pass these criteria:

- production app loads without white screen;
- Tools page opens;
- KURGIN Stone Analyzer preview remains mobile-safe;
- KURGIN Index still works;
- catalog still renders;
- request flow still works;
- favorites still work;
- no checkout/payment/order/reserve/sold logic is added;
- no auth/login is added;
- no upload is enabled unless separately approved;
- no PDF/report generation is enabled unless separately approved;
- adapter validates all public inputs;
- invalid input returns `invalid_input` safely;
- missing fields return `incomplete` safely;
- unsupported shape returns `unsupported_shape` safely;
- engine errors return `engine_unavailable` safely;
- no traceback is visible;
- no internal exception text is visible;
- no formula internals are visible;
- no raw formula, weights, penalty breakdown, diagnostics or debug trace are returned;
- no certificate/appraisal/price/order/reserve/payment claim is returned;
- CI `py_compile` passes;
- CI forbidden-pattern check passes.

## 12. Implementation guardrails

Future adapter implementation must not touch these areas unless a separate approved task allows it:

- `catalog.json`;
- `public_index.json`;
- catalog data source;
- Index methodology;
- checkout/payment/order/reserve/sold logic;
- auth/login/profile roles;
- admin repo;
- data repo;
- analyzer repo mutation;
- pricing/scoring formulas;
- PDF/report generation;
- certificate wording.

## 13. Contract status

This is a documentation contract only.

No production code is changed by this document. No Analyzer engine is connected. No formulas are exposed. No data, Index, catalog, checkout, payment, auth, admin, data, or analyzer repository behavior is changed.
