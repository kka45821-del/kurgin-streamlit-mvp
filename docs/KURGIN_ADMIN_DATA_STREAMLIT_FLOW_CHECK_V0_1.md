# KURGIN ADMIN DATA STREAMLIT FLOW CHECK v0.1

Repo: `kka45821-del/kurgin-streamlit-mvp`
Scope: checkpoint / audit document.
Status: source-level flow check / no implementation approval.

This document records the current Admin -> Data -> Streamlit MVP flow checkpoint.

Working repositories reviewed:

- `kurgin-admin-mvp`
- `kurgin-data`
- `kurgin-streamlit-mvp`

Repositories not changed:

- `kurgin-score-analyzer`
- `kurgin-formula-service`

This checkpoint does not add features, does not change code, does not change data, does not change CI, does not change Analyzer, does not change formula/scoring, does not perform cleanup, and does not deploy production.

## 1. Final verdict

```text
RISK
```

Interpretation:

- Source-level flow contract looks coherent.
- Published data files exist in `kurgin-data`.
- Streamlit has a remote data loader for `kurgin-data` and safe fallback behavior.
- Request-price and no-price states are protected from checkout/sellable behavior in both Admin publication rules and Streamlit normalization.
- Tools / Index / Analyzer preview surfaces remain MVP skeleton / public-safe surfaces.

Why not `PASS`:

- This task did not run the live Admin app manually.
- This task did not upload an Excel file through the live UI.
- This task did not execute a real publish operation with `GITHUB_TOKEN`.
- Streamlit/Admin/Data CI status contexts were not visible from the available commit-status queries.

No blocker requiring automatic code changes was found.

## 2. Checked repository snapshot

| Repo | Observed status | Notes |
|---|---|---|
| `kurgin-admin-mvp` | Source-level checked | Admin app and import/preview/publish modules inspected. |
| `kurgin-data` | Source-level checked | `catalog.json`, `data/catalog.json`, `stones.csv`, `upload_batches.csv` exist and match expected publication contract. |
| `kurgin-streamlit-mvp` | Source-level checked | Public app loads catalog state and renders mobile shell from published/fallback stones. |
| `kurgin-score-analyzer` | Not changed | Analyzer changes explicitly out of scope. |
| `kurgin-formula-service` | Not changed | Formula Service changes explicitly out of scope. |

## 3. Admin app checkpoint

### 3.1. Admin app entry

Status:

```text
SOURCE-LEVEL PASS
RUNTIME NOT EXECUTED
```

Findings:

- `kurgin-admin-mvp/app.py` defines the Streamlit admin entrypoint.
- The app sets page config as `KURGIN Admin MVP`.
- The app imports admin modules for auth, batches, IO, logs, menu, settings, pricing, publication rules, publish, upload and validation.
- The app renders dashboard, catalog, settings and controlled stub/future/restricted pages.
- Admin login is required before rendering the main admin page.

Checkpoint limitation:

- The live Admin app was not opened in this task.
- No browser/runtime session was executed.

Result:

```text
RISK: source looks intact, runtime open not verified here.
```

### 3.2. Excel/import flow

Status:

```text
SOURCE-LEVEL PASS
RUNTIME UPLOAD NOT EXECUTED
```

Findings:

- `admin_upload.py` provides an Excel template download.
- It accepts `.xlsx` uploads.
- It diagnoses sheets.
- It detects header rows.
- It reports recognized and unrecognized columns.
- It renders raw Excel preview.
- It normalizes Excel data into the KURGIN stone schema.
- It validates before save.
- It blocks saving if critical errors exist.
- It requires explicit confirmation before saving a batch.

Important boundary:

- The UI warns that import auto-marks stones as available/show_in_catalog/is_mvp_eligible and that Publication Gate and public preview must be checked before publication.

Checkpoint limitation:

- No real Excel upload was executed in this task.

Result:

```text
RISK: import contract is present; live upload not verified.
```

### 3.3. Preview / validation

Status:

```text
SOURCE-LEVEL PASS
```

Findings:

- `admin_validation.py` defines critical fields: `stone_id`, `shape`, `carat`, `color`, `clarity`, `lab`, `report_number`.
- Empty file / wrong sheet becomes a critical error.
- Missing required fields become critical errors.
- Duplicate `stone_id` becomes a critical error.
- `price_rub` and `karo_score` are warnings in base validation.
- Upload flow adds stricter KURGIN Score gate for Round main/large stones.

Result:

```text
PASS at source level.
```

## 4. Publish contract checkpoint

### 4.1. Publish target

Status:

```text
SOURCE-LEVEL PASS
```

Findings:

- `admin_publish.py` targets `kka45821-del/kurgin-data` on branch `main`.
- Publish requires `GITHUB_TOKEN` from Streamlit secrets or environment.
- If token is missing, the UI falls back to manual download of `catalog.json`.
- The UI caption explicitly says it publishes data only and does not change the public site or design.

### 4.2. Expected files

Publish contract writes these four files:

1. `catalog.json`
2. `data/catalog.json`
3. `stones.csv`
4. `upload_batches.csv`

This matches the expected Admin -> Data publication contract for the current MVP.

### 4.3. Publish execution

Status:

```text
NOT EXECUTED IN THIS TASK
```

Checkpoint limitation:

- This audit did not press the live publish button.
- This audit did not use a real `GITHUB_TOKEN`.
- This audit did not create or update files in `kurgin-data`.

Result:

```text
RISK: publish contract is correct at source level; live publish was not executed here.
```

## 5. kurgin-data checkpoint

### 5.1. Published JSON files

Status:

```text
SOURCE-LEVEL PASS
```

Findings:

- `catalog.json` exists.
- `data/catalog.json` exists.
- Both expose source `KURGIN Admin`.
- Both expose schema version `catalog_mvp_v2`.
- Both expose `count: 174` at the observed snapshot.
- The first observed stone has `price_rub: 0`, `public_sellable: false`, `checkout_enabled: false`, and `public_action: request_price`.

Interpretation:

```text
No-price stones are visible/request-price, not buyable.
```

### 5.2. Published CSV files

Status:

```text
SOURCE-LEVEL PASS
```

Findings:

- `stones.csv` exists.
- `upload_batches.csv` exists.
- `stones.csv` contains the full admin/public schema columns.
- `upload_batches.csv` contains batch metadata including `batch_number`, `upload_date`, `supplier_name`, `stones_count`, `upload_confirmed`, and `notes`.

Result:

```text
PASS at source level.
```

## 6. Streamlit reader checkpoint

### 6.1. App data loading

Status:

```text
SOURCE-LEVEL PASS
RUNTIME NOT EXECUTED
```

Findings:

- `app.py` imports `load_catalog_state` from `catalog.data_loader`.
- `app.py` loads `catalog_state` and passes `stones_json` into `build_mobile_shell`.
- `catalog/data_loader.py` tries remote URLs from `kurgin-data`, including:
  - `catalog.json`
  - `data/catalog.json`
- `catalog/data_loader.py` normalizes public stones through `normalize_public_stones`.
- If remote loading fails or is empty, it uses local fallback stones.

Checkpoint limitation:

- The live Streamlit app was not opened in this task.
- Remote fetch was not executed through a live deployed app runtime here.

Result:

```text
RISK: source-level reader contract is present; live app read not verified here.
```

### 6.2. Catalog display

Status:

```text
SOURCE-LEVEL PASS
```

Findings:

- `mobile_shell.py` renders catalog UI from the `stones` array.
- Catalog stats and cards are generated from published normalized stones.
- Filtering/sorting and section selection are handled in the active shell.
- Favorites are local browser state only.

Result:

```text
PASS at source level.
```

## 7. Request-price / buyable-state checkpoint

### 7.1. Admin publication rules

Status:

```text
PASS
```

Findings:

- `admin_publication_rules.py` separates public visibility from public sellability.
- `public_sellable_mask` requires:
  - base public eligibility;
  - `price_rub > 0`;
  - `price_confirmed` true;
  - `availability_confirmed` true.
- `public_visible_mask` allows request-only visibility where price is missing and status/flag permits it.
- `public_preview` sets:
  - `public_visible = True`;
  - `public_sellable = sellable`;
  - `checkout_enabled = sellable`;
  - `public_action = checkout` if sellable, otherwise `request_price`.

Conclusion:

```text
No-price stones do not become checkout-enabled in Admin publication rules.
```

### 7.2. Streamlit normalization

Status:

```text
PASS
```

Findings:

- `catalog_core.py` treats request-price state as true when price is missing/zero, price status is request-like, `public_action` is `request_price`, `checkout_enabled` is false, or `public_sellable` is false.
- `normalize_stone` sets request-price stones to:
  - `priceText = по запросу`;
  - `priceDisplay = по запросу`;
  - `is_request_price = True`;
  - `checkout_enabled = False`;
  - `public_sellable = False`.

Conclusion:

```text
Streamlit preserves request-price as request-only state.
```

### 7.3. UI action boundary

Status:

```text
PASS
```

Findings:

- `mobile_shell.py` renders request contact channels for request-price / clarification flow.
- Request message explicitly says it is not an order, reserve or price lock.
- The request box says the request is not an order, reserve, payment or price fixing.
- Checkout/reserve/share actions are rendered disabled in the active shell.

Conclusion:

```text
Request-price state does not become order, reserve, payment or checkout in the current shell.
```

## 8. Tools / Index / Analyzer preview checkpoint

Status:

```text
SOURCE-LEVEL PASS
```

Findings:

- `tools_page.py` renders tabs for Stone Analyzer, Index, Verify skeleton, Mass Analyzer skeleton and Academy skeleton.
- Verify is described as an MVP skeleton, not a working verification service.
- Analyzer preview uses `services.analyzer_adapter.analyze_public_stone`.
- `services/analyzer_adapter.py` states the preview performs no live backend call, no Formula Service call, no file upload and imports no Analyzer engine modules.
- Analyzer preview explicitly says it is not a certificate, not a price valuation and not a purchase trigger.
- Analyzer preview says no checkout, payment, request or reserve is created.

Conclusion:

```text
Tools / Index / Analyzer preview are not converted into production Analyzer, Verify, payment, report or reserve features.
```

## 9. Prohibited feature check

Current source-level check found no evidence that this checkpoint adds or requires:

- payment;
- reserve automation;
- sold automation;
- auth/pro roles;
- PDF/report generation;
- KURGIN Verify activation;
- real Analyzer engine connection to public Streamlit;
- formula/scoring changes;
- cleanup deletion/move;
- production deploy.

This document does not authorize any of those features.

## 10. Blockers and risks

### 10.1. Blocking issues

```text
No code-fix blocker found in this checkpoint.
```

No automatic fix is required because no source-level blocker was found that would justify changing code under this task.

### 10.2. Verification gaps / risk items

| ID | Risk | Severity | Required future action |
|---|---|---:|---|
| RISK-001 | Admin app opening was not live-tested in browser/runtime. | Medium | Run manual Admin open check or CI smoke command in a separate stabilization task. |
| RISK-002 | Excel upload/import was source-checked but not executed with a real file. | Medium | Run a controlled upload smoke using a small fixture in a separate task. |
| RISK-003 | Publish contract exists, but live publish with `GITHUB_TOKEN` was not executed. | Medium | Run controlled publish smoke only with explicit approval. |
| RISK-004 | Streamlit app source reads remote data, but live deployed app was not opened in this task. | Medium | Run Streamlit live/read smoke separately. |
| RISK-005 | CI status contexts were not visible for Admin/Data and Streamlit status visibility has been inconsistent/absent. | Low-medium | Create CI/status visibility note or CI smoke map separately. |

## 11. Recommended next step

Recommended next step:

```text
targeted stabilization or usage audit
```

Allowed next steps:

1. Manual Admin open smoke check.
2. Small fixture Excel upload/import smoke check.
3. Publish dry-run/manual download validation.
4. Controlled publish smoke with `GITHUB_TOKEN`, only after explicit approval.
5. Streamlit remote catalog read smoke check.
6. Catalog request-price smoke check.
7. Tools/Index/Analyzer preview smoke check.
8. CI/status visibility documentation.
9. Usage audit planning for cleanup candidates.

Not recommended now:

- feature growth;
- cleanup deletion/move;
- Analyzer connection;
- formula/scoring changes;
- payment/reserve/sold/auth/PDF/Verify implementation;
- production deploy.

## 12. Blocked actions

Blocked by this checkpoint:

- new functions;
- code refactor;
- UI redesign;
- cleanup deletion/move;
- Analyzer changes;
- formula/scoring changes;
- payment;
- reserve automation;
- sold automation;
- auth/pro roles;
- PDF/report generation;
- KURGIN Verify activation;
- real engine connection to public Streamlit;
- production deploy;
- data schema changes;
- CI changes without separate task;
- `kurgin-score-analyzer` changes;
- `kurgin-formula-service` changes.

## 13. Acceptance checklist

This checkpoint satisfies the task if:

- flow check document is created;
- verdict is included: `RISK`;
- checked repositories are listed;
- blockers are listed;
- unnecessary code changes are not made;
- no new features are added;
- no cleanup is performed;
- next step is limited to targeted stabilization or usage audit.

## 14. Closure

Final verdict:

```text
RISK
```

The Admin -> Data -> Streamlit MVP flow looks structurally coherent at source level.

No blocker requiring code changes was found.

The remaining risk is runtime verification: Admin open, Excel upload, real publish and live Streamlit read were not executed in this checkpoint.
