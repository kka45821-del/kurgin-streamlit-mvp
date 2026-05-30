# KURGIN ADMIN DATA STREAMLIT FLOW CHECK v0.1

Repo: `kka45821-del/kurgin-streamlit-mvp`
Scope: checkpoint / audit document.
Status: source-level MVP-flow checkpoint / no implementation approval.

This document records the current Admin -> Data -> Streamlit MVP flow checkpoint after source stabilization and the Analyzer Excel template contract.

Working repositories reviewed:

- `kurgin-admin-mvp`
- `kurgin-data`
- `kurgin-streamlit-mvp`

Repositories not changed:

- `kurgin-score-analyzer`
- `kurgin-formula-service`

Context sources:

- `docs/KURGIN_ACTIVE_SOURCE_INDEX_V0_1.md`
- `docs/KURGIN_ACTIVE_SOURCE_INDEX_CHECK_V0_1.md`
- `docs/KURGIN_CLEANUP_BACKLOG_V0_1.md`
- `docs/KURGIN_STABILIZATION_CHECKPOINT_V0_1.md`
- `docs/FINAL_ANALYZER_EXCEL_TEMPLATE_CONTRACT_V0_1.md` in `kurgin-score-analyzer` as read-only context

This checkpoint does not add features, does not change code, does not change UI, does not change data, does not change CI, does not change Analyzer, does not change formula/scoring, does not change the Excel contract, does not perform cleanup, and does not deploy production.

## 1. Final verdict

```text
RISK
```

Interpretation:

- Source-level Admin -> Data -> Streamlit contract is coherent.
- Published data files exist in `kurgin-data`.
- Streamlit has a remote data loader for `kurgin-data` and safe fallback behavior.
- Request-price and no-price states are protected from checkout/sellable behavior in both Admin publication rules and Streamlit normalization.
- Tools / Index / Analyzer preview surfaces remain MVP skeleton / public-safe surfaces.
- No blocker was found that justifies automatic code changes under this task.

Why verdict is not `PASS`:

- The live Admin app was not opened manually in this task.
- Excel upload/import was source-checked, not executed with a real file in a live app.
- Live publish with `GITHUB_TOKEN` was not executed.
- Live deployed Streamlit read was not opened in this task.
- CI/status contexts were not treated as sufficient proof of runtime readiness.

Why verdict is not `BLOCKED`:

- No source-level blocker was found.
- Published files required by the current contract exist.
- No evidence was found that no-price stones become checkout-enabled.
- No evidence was found that request-price becomes order/reserve/payment.
- No evidence was found that Tools / Index / Analyzer preview became production Analyzer, Verify, payment, report or reserve functionality.

## 2. Checked repositories

| Repo | Observed role | Check status | Change status |
|---|---|---|---|
| `kurgin-admin-mvp` | Admin / Excel import / validation / preview / publish | Source-level checked | No change |
| `kurgin-data` | Published catalog/data layer | Source-level checked | No change |
| `kurgin-streamlit-mvp` | Public MVP / catalog / tools / Analyzer preview / Index | Source-level checked and this doc updated | Docs-only change |
| `kurgin-score-analyzer` | Private Analyzer / SDK / API / Excel contract context | Context only | No change |
| `kurgin-formula-service` | Future/staging Formula Service candidate | Out of scope | No change |

## 3. What was checked

Checklist summary:

| Area | Check | Result |
|---|---|---:|
| Admin app entry | `app.py` imports and renders Admin MVP surfaces | SOURCE-LEVEL PASS |
| Admin auth boundary | Admin login is required before main app rendering | SOURCE-LEVEL PASS |
| Excel/import flow | Template, `.xlsx` uploader, sheet diagnostics, column recognition and normalization are present | SOURCE-LEVEL PASS / runtime not executed |
| Validation/preview | Critical/warning validation and upload preview are present | SOURCE-LEVEL PASS |
| Publish flow | Contract targets `kurgin-data` and expected files | SOURCE-LEVEL PASS / live publish not executed |
| Data files | `catalog.json`, `data/catalog.json`, `stones.csv`, `upload_batches.csv` exist | SOURCE-LEVEL PASS |
| Data structure | Published JSON exposes `catalog_mvp_v2` and full catalog fields | SOURCE-LEVEL PASS |
| Request-price/no-price | No-price observed stone is `request_price`, not checkout-enabled | PASS at source/data level |
| Streamlit read | Streamlit reads remote `kurgin-data` URLs and uses fallback | SOURCE-LEVEL PASS / live app not opened |
| Catalog display | Mobile shell renders cards from normalized stones | SOURCE-LEVEL PASS |
| Tools / Index / Analyzer preview | Skeleton/public-safe surfaces remain present | SOURCE-LEVEL PASS |
| Prohibited features | No payment/reserve/sold/auth/PDF/Verify/real-engine approval added | PASS |

## 4. kurgin-admin-mvp checkpoint

### 4.1. Admin app opens

Status:

```text
RISK: source-level pass, runtime not executed
```

Findings:

- `app.py` is the Streamlit Admin entrypoint.
- The page config is `KURGIN Admin MVP`.
- The app imports the expected admin modules for auth, batches, IO, logging, menu, settings, pricing, publication rules, publish, upload and validation.
- The app renders dashboard, catalog, settings and controlled active/stub/future/restricted sections.
- The app requires admin login before the main admin page renders.

Not confirmed:

- live browser/runtime open;
- Streamlit Cloud availability;
- secrets availability;
- manual login success.

### 4.2. Excel/import or current test-data flow

Status:

```text
RISK: source-level pass, live upload not executed
```

Findings:

- `admin_upload.py` provides a downloadable Excel template.
- It accepts `.xlsx` uploads.
- It performs sheet diagnostics.
- It attempts header-row detection.
- It reports recognized and unrecognized columns.
- It displays raw Excel preview.
- It normalizes Excel data into the internal stone schema.
- It runs validation before save.
- It blocks saving when critical errors exist.
- It requires explicit confirmation before saving a batch.

Important risk note:

- The import UI warns that imported stones are automatically marked as available/show_in_catalog/is_mvp_eligible and must be checked through Publication Gate and public preview before publication.

Not confirmed:

- live `.xlsx` upload;
- actual save through the running Admin app;
- real fixture round-trip.

### 4.3. Validation / preview

Status:

```text
SOURCE-LEVEL PASS
```

Findings:

- `admin_validation.py` defines critical fields:
  - `stone_id`
  - `shape`
  - `carat`
  - `color`
  - `clarity`
  - `lab`
  - `report_number`
- Empty file / wrong sheet is a critical error.
- Missing required fields become critical errors.
- Duplicate `stone_id` becomes a critical error.
- `price_rub` and `karo_score` are base warnings.
- Upload flow adds a stricter KURGIN Score gate for Round main/large rows.

Interpretation:

```text
Validation/preview path exists and preserves blocking/warning separation.
```

### 4.4. Publish flow

Status:

```text
RISK: source-level pass, live publish not executed
```

Findings:

- `admin_publish.py` targets `kka45821-del/kurgin-data` on `main`.
- It requires `GITHUB_TOKEN` from Streamlit secrets or environment for auto-publish.
- If token is missing, the UI provides manual download of `catalog.json`.
- The publish UI states that it publishes data only and does not change the public site or design.
- The publish contract writes four expected files:
  1. `catalog.json`
  2. `data/catalog.json`
  3. `stones.csv`
  4. `upload_batches.csv`

Not confirmed:

- actual live publish button execution;
- token presence;
- 409 retry behavior in a live operation.

### 4.5. Publish does not unexpectedly change schema

Status:

```text
SOURCE-LEVEL PASS
```

Findings:

- Publish payload declares schema version `catalog_mvp_v2`.
- It includes full catalog fields and computed public fields.
- It does not change code or UI during publish.
- This checkpoint does not alter schema.

Risk:

- Any future schema change must be separately approved and tested against Streamlit reader assumptions.

## 5. kurgin-data checkpoint

### 5.1. Expected files exist

Status:

```text
SOURCE-LEVEL PASS
```

Observed required files:

- `catalog.json`
- `data/catalog.json`
- `stones.csv`
- `upload_batches.csv`

Findings:

- `catalog.json` exists and exposes source `KURGIN Admin`.
- `data/catalog.json` exists and mirrors the expected published JSON structure.
- `stones.csv` exists and includes the full admin/public catalog schema columns.
- `upload_batches.csv` exists and contains batch metadata.

### 5.2. Structure not broken

Status:

```text
SOURCE-LEVEL PASS
```

Findings:

- Published JSON exposes `schema.version = catalog_mvp_v2`.
- Published JSON exposes `score_public_name = KURGIN Score`.
- Published JSON exposes `score_field = karo_score`.
- Published JSON exposes `includes_full_catalog_fields = true`.
- Published JSON exposes `section_autofill = true`.
- Published JSON contains a `stones` list.
- Observed count is `174` in the current published snapshot.

### 5.3. No accidental extra production meanings

Status:

```text
SOURCE-LEVEL PASS
```

Findings:

- Published data is data only.
- Published data does not by itself activate payment, reserve, sold, auth, PDF/report, Verify, or real Analyzer engine behavior.
- Public meaning remains controlled by Streamlit reader and UI logic.

### 5.4. Request-price / no-price states do not become buyable

Status:

```text
PASS
```

Observed data example:

- first observed published stone has `price_rub: 0`;
- `public_sellable: false`;
- `checkout_enabled: false`;
- `public_action: request_price`.

Interpretation:

```text
No-price published stones remain request-price, not buyable.
```

## 6. kurgin-streamlit-mvp checkpoint

### 6.1. App reads published data

Status:

```text
RISK: source-level pass, live app not opened
```

Findings:

- `app.py` imports `load_catalog_state` from `catalog.data_loader`.
- `app.py` loads `catalog_state` and passes `stones_json` into `build_mobile_shell`.
- `catalog/data_loader.py` tries remote URLs from `kurgin-data`, including:
  - `catalog.json`
  - `data/catalog.json`
- Remote payload is normalized through `normalize_public_stones`.
- If remote loading fails or is empty, Streamlit uses local fallback stones and shows a notice.

Not confirmed:

- live deployed app read;
- live remote request from the deployed environment;
- end-user browser rendering.

### 6.2. Catalog displays data

Status:

```text
SOURCE-LEVEL PASS
```

Findings:

- `mobile_shell.py` renders catalog UI from the `stones` array.
- The catalog renders stats, sections, filters/sorting and cards.
- The shell keeps favorites as browser local state.
- The catalog source logic reads from normalized stones, not from arbitrary raw data directly.

### 6.3. Stone without price does not become buyable

Status:

```text
PASS
```

Findings:

- `catalog_core.py` treats request-price as true when price is missing/zero, price status is request-like, `public_action` is request_price, checkout is disabled, or public sellable is false.
- `normalize_stone` sets request-price stones to:
  - `priceText = по запросу`;
  - `priceDisplay = по запросу`;
  - `is_request_price = True`;
  - `checkout_enabled = False`;
  - `public_sellable = False`.

Interpretation:

```text
A no-price stone remains a request-price stone, not a checkout-enabled stone.
```

### 6.4. Request-price does not become order/reserve/payment

Status:

```text
PASS
```

Findings:

- Request message explicitly says the request is not an order, reserve or price lock.
- Request box says request is not order, reserve, payment or price fixing.
- Checkout/reserve/share actions are rendered disabled in the current shell.
- Smoke script `smoke_public_price_states.py` asserts request-price/favorites/inactive commerce boundaries at source level.

Interpretation:

```text
request_price ≠ order
request_price ≠ reserve
request_price ≠ payment
favorite ≠ reserve
```

### 6.5. Tools / Index / Analyzer preview

Status:

```text
SOURCE-LEVEL PASS
```

Findings:

- `tools_page.py` renders tabs for Stone Analyzer, Index, Verify skeleton, Mass Analyzer skeleton and Academy skeleton.
- Verify is described as MVP skeleton, not a working verification service.
- Stone Analyzer preview uses `services.analyzer_adapter.analyze_public_stone`.
- `services/analyzer_adapter.py` states it performs no live backend call, no Formula Service call, no file upload and imports no Analyzer engine modules.
- Analyzer preview states it is not a certificate, not a price valuation and not a purchase trigger.
- Analyzer preview says no checkout, payment, request or reserve is created.

Interpretation:

```text
Tools / Index / Analyzer preview are not production Analyzer, Verify, payment, report, reserve, PDF or storage features.
```

### 6.6. No prohibited features added

Status:

```text
PASS
```

Current source-level check did not find this checkpoint requiring or approving:

- payment;
- reserve automation;
- sold automation;
- auth/pro roles;
- PDF/report generation;
- KURGIN Verify activation;
- real Analyzer engine connection;
- Formula Service integration;
- formula/scoring change;
- Excel contract change;
- kurgin-data schema change;
- production deploy;
- cleanup deletion/move.

## 7. Blockers

```text
No source-level blocker found.
```

No automatic fix was made.

If a live runtime blocker is later found, it must be documented first and fixed only through a separate approved task.

## 8. Risk items

| ID | Risk | Severity | Required next action |
|---|---|---:|---|
| RISK-001 | Admin app opening was not live-tested. | Medium | Run manual Admin open smoke check. |
| RISK-002 | Excel/import was source-checked but not executed with a real fixture. | Medium | Run controlled `.xlsx` fixture upload/import smoke. |
| RISK-003 | Publish contract exists, but live publish with `GITHUB_TOKEN` was not executed. | Medium | Run controlled publish smoke only after explicit approval. |
| RISK-004 | Streamlit source reads remote data, but live deployed app read was not opened here. | Medium | Run Streamlit live remote-catalog read smoke. |
| RISK-005 | CI/status visibility is not treated as runtime proof in this audit. | Low-medium | Create CI/status visibility note or CI smoke map. |
| RISK-006 | Admin import auto-marks MVP flags and depends on Publication Gate review. | Medium | Add/verify fixture tests around Publication Gate before any broader upload use. |

## 9. Next actions

Allowed next actions:

1. Manual Admin open smoke check.
2. Controlled `.xlsx` fixture upload/import smoke check.
3. Publish dry-run/manual download validation.
4. Controlled publish smoke with `GITHUB_TOKEN`, only after explicit approval.
5. Streamlit remote catalog read smoke check.
6. Catalog request-price/no-price smoke check.
7. Tools / Index / Analyzer preview smoke check.
8. CI/status visibility documentation.
9. Usage audit planning for cleanup candidates.
10. Admin -> Data -> Streamlit contract checklist if more formal verification is needed.

Blocked next actions without separate approval:

- new functions;
- code refactor;
- UI redesign;
- cleanup deletion/move;
- Analyzer changes;
- formula/scoring changes;
- real engine connection;
- payment;
- reserve automation;
- sold automation;
- auth/pro roles;
- PDF/report generation;
- KURGIN Verify activation;
- Excel contract changes;
- kurgin-data schema changes;
- production deploy.

## 10. Acceptance checklist

This checkpoint satisfies the task if:

- `docs/KURGIN_ADMIN_DATA_STREAMLIT_FLOW_CHECK_V0_1.md` exists at the requested path;
- verdict is included: `RISK`;
- checked repositories are listed;
- what was checked is listed;
- what works is listed;
- what is not confirmed is listed;
- blockers are listed;
- risk items are listed;
- concrete next actions are listed;
- no unnecessary code changes are made;
- no UI changes are made;
- no data schema changes are made;
- no CI changes are made;
- no cleanup deletion/move is performed;
- no Analyzer/formula/scoring changes are made;
- no real engine/payment/reserve/sold/auth/PDF/Verify features are added.

## 11. Closure

Final verdict:

```text
RISK
```

The Admin -> Data -> Streamlit MVP flow is coherent at source level.

No source-level blocker requiring code changes was found.

The remaining gap is runtime verification: Admin open, real Excel upload, real publish and live Streamlit read must be checked separately before this flow can be marked `PASS`.
