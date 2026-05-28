# ANALYZER INTEGRATION PLAN v0.1

Repo: `kka45821-del/kurgin-streamlit-mvp`
Scope: public MVP planning only.
Status: architecture plan / no production code change.

This document defines a safe future path for integrating KURGIN Score Analyzer into the public MVP without destabilizing the storefront, catalog, favorites, request flow, filters/sort, or KURGIN Index.

## 1. Baseline assumptions

Current public MVP baseline:

- public storefront is stable;
- catalog renders;
- catalog request flow works;
- favorites flow works;
- catalog filters and sorting work;
- KURGIN Index works;
- checkout / payment / order / reserve / sold logic is inactive;
- auth / login / profile roles are inactive;
- Analyzer engine is not connected to the public MVP.

This plan does not authorize implementation. It prepares a controlled integration path.

## 2. Recommended location in public MVP

### Primary location: Tools → KURGIN Stone Analyzer

The Analyzer should live first inside the existing Tools surface as `KURGIN Stone Analyzer`.

Recommended initial public placement:

- Tools page;
- Stone Analyzer tab;
- inactive skeleton becomes a controlled public preview surface;
- no global navigation change;
- no catalog flow dependency;
- no profile dependency;
- no auth requirement in phase 1.

### Secondary location: Tools → KURGIN Mass Analyzer

Batch / Excel analysis should stay separate from single-stone public preview.

Recommended placement:

- Tools page;
- Mass Analyzer tab;
- disabled / future state in phase 1;
- controlled upload preview only in phase 2 or later;
- no direct connection to live catalog publishing.

### Possible later connection: Catalog detail card

The catalog detail card may later link to an Analyzer preview only as a read-only contextual view.

Allowed later:

- `Analyze similar parameters` or `View KURGIN Score explanation` as a non-blocking information link;
- use existing stone fields already visible in the card;
- no hidden formula disclosure;
- no automatic price or availability impact.

Not allowed in early phases:

- using Analyzer result to create checkout/order/reserve;
- changing catalog price;
- changing public Index values;
- creating a certificate claim;
- exposing internal scoring internals.

### Possible later connection: Profile

Profile should not be required for public preview.

Later professional mode may connect Analyzer to Profile only after auth/roles are designed and reviewed.

Profile-related features are phase 3 or later:

- saved analysis history;
- professional role access;
- paid analysis level;
- business dashboard;
- analyst notes.

## 3. Analyzer modes

### Single stone mode

Purpose:

- public preview for one stone;
- minimal manual parameter input;
- controlled output;
- no formula disclosure.

Potential inputs:

- shape;
- carat;
- color;
- clarity;
- table %;
- depth %;
- crown angle;
- pavilion angle;
- crown height;
- pavilion depth;
- girdle;
- fluorescence;
- report number as optional reference.

Public phase 1 should not require all parameters. Missing data should show a limitation state.

### File upload mode

Purpose:

- future public or semi-professional upload of a single report / file.

Phase 1 state:

- not active;
- may show safe placeholder only.

Phase 2 or later:

- controlled upload adapter;
- strict file type and size limits;
- no permanent storage without explicit backend design;
- no certificate claim.

### Manual input mode

Purpose:

- controlled public form for entering parameters manually.

Recommended for phase 1 because it avoids parsing/upload risk.

Constraints:

- minimal required fields;
- clear missing-data warnings;
- no formula details;
- no official certificate language.

### Batch / Excel mode

Purpose:

- professional or semi-professional analysis of multiple stones.

Recommended phase:

- phase 2 or phase 3;
- not public phase 1.

Constraints:

- should use a separate adapter;
- should not block public storefront;
- should not publish data to catalog;
- should not connect to checkout/payment/order/reserve.

### Public preview mode

Purpose:

- show limited KURGIN Score interpretation;
- demonstrate value without exposing formula;
- avoid legal/quality overclaim.

Public preview can show:

- score band or coefficient;
- simple textual category;
- data completeness warning;
- limitations;
- `not a certificate` disclaimer;
- prompt to request professional review later.

### Professional / paid mode later

Professional mode should not be implemented until auth/roles and paid-service boundaries exist.

Possible future output:

- deeper analysis;
- batch results;
- downloadable report;
- analyst review;
- professional dashboard.

Not part of public MVP phase 1.

## 4. What can be shown publicly

Allowed public output:

- KURGIN Score band or coefficient;
- short result summary;
- confidence / completeness indicator;
- missing-data warning;
- limitations;
- recommendation to verify with source document;
- explanation that result is informational;
- note that result is not a certificate and not an appraisal.

Allowed public wording examples:

- `Предварительный результат`;
- `Ориентировочная интерпретация`;
- `Расчёт зависит от полноты введённых параметров`;
- `Не является сертификатом, оценкой стоимости или официальным геммологическим заключением`.

## 5. What must not be shown publicly

Forbidden public output:

- internal formula;
- scoring weights;
- penalty logic details;
- proprietary thresholds beyond approved public bands;
- exact commercial methodology;
- official certificate claim;
- official appraisal claim;
- investment claim;
- guaranteed price effect;
- automatic reserve/order/payment state;
- professional-only interpretation.

Do not expose:

- source code of formula engine;
- internal debug metrics;
- hidden penalty names if not approved for public copy;
- backend tracebacks;
- raw uploaded file content after processing unless explicitly designed.

## 6. Formula protection approach

The public MVP must not import or expose formula internals directly in UI copy.

Recommended approach:

- use an adapter layer;
- adapter returns only approved public fields;
- formula engine remains behind a stable interface;
- public UI never calls internal formula blocks directly;
- public response schema strips internal diagnostics;
- public UI uses labels and ranges, not formula details.

Recommended public result shape:

```json
{
  "status": "ok | incomplete | unsupported | error",
  "score_band": "Standard | High | Premium | ...",
  "coefficient": "optional approved public value",
  "summary": "short public explanation",
  "warnings": ["missing pavilion angle", "not enough data"],
  "limitations": ["not a certificate", "not an appraisal"]
}
```

Forbidden result shape:

```json
{
  "raw_formula": "...",
  "penalty_breakdown_internal": {},
  "weights": {},
  "debug_trace": []
}
```

## 7. Adapter / API layer

Analyzer should not be wired directly into `ui/pages/tools_page.py`.

Recommended future adapter:

- new file, for example `analyzer_adapter.py` or `services/analyzer_adapter.py`;
- adapter imports or calls the Analyzer engine;
- adapter normalizes inputs;
- adapter sanitizes outputs;
- adapter handles errors without traceback;
- adapter returns public-safe response schema.

Possible adapter responsibilities:

- validate shape support;
- normalize numeric fields;
- handle missing parameters;
- call engine;
- map internal score to public label;
- attach warnings;
- block internal formula output;
- return safe fallback state if engine unavailable.

If `kurgin-score-analyzer` remains a separate repository, integration options should be reviewed before implementation:

1. package dependency;
2. copied stable adapter subset;
3. internal API endpoint;
4. separate service call.

Preferred long-term direction: adapter/API boundary, not direct UI-level imports.

## 8. Relationship with `kurgin-score-analyzer` repository

Before implementation, audit the Analyzer repository for:

- available engine functions;
- current input schema;
- output schema;
- dependency list;
- Streamlit-specific assumptions;
- file upload assumptions;
- formula module boundaries;
- public-safe vs internal-only outputs.

Do not import the whole Analyzer app into the public MVP.

Likely safe import target later:

- pure calculation engine function;
- no Streamlit UI dependency;
- no file-system side effects;
- no admin settings dependency;
- no uncontrolled PDF/report generation.

Likely unsafe to import directly:

- Analyzer Streamlit app entrypoint;
- admin/config UI;
- PDF/report generator;
- upload parser with broad file assumptions;
- modules that expose formula internals to UI;
- code that writes files or mutates state.

## 9. Phased integration path

### Phase 1 — Public preview skeleton with manual input

Goal:

- convert Stone Analyzer skeleton into a controlled public preview surface.

Allowed:

- manual input UI only;
- no file upload;
- no real engine if not separately approved;
- static validation states;
- public-safe preview result container;
- clear limitations and disclaimers.

Possible implementation files later:

- `ui/pages/tools_page.py`;
- `ui/extra_styles.py`;
- optional `docs` update.

Acceptance for phase 1:

- Tools page still opens;
- Index still works;
- Analyzer preview does not break catalog/favorites/request flow;
- no checkout/payment/auth;
- no formula disclosure;
- no certificate claim;
- no backend file processing.

### Phase 2 — Adapter-connected single stone calculation

Goal:

- connect a safe adapter to a pure Analyzer calculation function.

Allowed:

- manual input;
- adapter validation;
- public-safe result schema;
- incomplete-data warnings;
- unsupported-shape state;
- error state without traceback.

Possible implementation files later:

- `services/analyzer_adapter.py` or equivalent;
- `ui/pages/tools_page.py`;
- `ui/extra_styles.py`;
- tests / smoke script;
- docs update.

Acceptance for phase 2:

- adapter returns safe schema;
- public UI never sees internal formula;
- bad input does not crash app;
- unsupported input shows safe message;
- no report/PDF/certificate;
- no checkout/payment/auth.

### Phase 3 — Professional / batch / paid expansion

Goal:

- add controlled professional functionality after public MVP remains stable.

Possible features:

- Excel / batch mode;
- professional detail view;
- saved analysis history;
- analyst review;
- paid report flow;
- controlled PDF/report generation.

Prerequisites:

- auth/roles design;
- payment/service policy;
- legal wording review;
- report/certificate language lock;
- backend storage decision;
- separate smoke/CI coverage.

Not allowed before prerequisites:

- paid service;
- official certificate claim;
- professional cabinet;
- batch upload for public users;
- storing user files;
- automatic catalog mutation.

## 10. Files likely affected later

Likely future public MVP files:

- `ui/pages/tools_page.py` — Analyzer UI surface;
- `ui/extra_styles.py` — mobile styles;
- `ui/mobile_shell.py` — only if navigation or shell-level event handling is needed;
- `docs/*` — release notes and smoke checkpoints;
- `scripts/*` — smoke checks;
- `services/analyzer_adapter.py` — future adapter layer, if created.

Files that should not be touched for early Analyzer preview:

- `ui/index_components.py`;
- `ui/index_scripts.py`;
- `ui/index_styles.py`;
- `catalog/*`;
- `config/request_contacts.py`;
- data files;
- pricing/scoring formula files unless a separate formula task is approved.

## 11. Forbidden changes for future implementation tasks

Do not include in Analyzer public MVP integration unless a separate approved task explicitly allows it:

- checkout;
- payment;
- order;
- reserve;
- sold logic;
- auth/login;
- professional cabinet;
- catalog data mutation;
- Index methodology changes;
- public_index changes;
- catalog.json changes;
- formula disclosure;
- PDF/report generation;
- certificate wording;
- admin repo changes;
- data repo changes;
- Analyzer repo mutation from public MVP task.

## 12. Future implementation acceptance criteria

A future implementation task should pass these criteria:

- public MVP loads without white screen;
- Tools page opens;
- KURGIN Index still works;
- Stone Analyzer surface is clearly marked as preview if not fully connected;
- no active checkout/payment/order/reserve/sold/auth logic;
- no formula internals visible;
- no certificate claim;
- bad input shows safe validation;
- missing data shows limitation warning;
- unsupported shapes show controlled message;
- request/favorites/catalog flows still work;
- mobile layout remains usable;
- CI py_compile passes;
- forbidden-pattern check passes;
- docs updated with smoke checklist.

## 13. Release and safety note

This document is planning only.

No production code is changed by this plan. No Analyzer engine is connected. No formula is changed or exposed. No data, catalog, Index, checkout, payment, auth, admin, or analyzer repository behavior is changed.
