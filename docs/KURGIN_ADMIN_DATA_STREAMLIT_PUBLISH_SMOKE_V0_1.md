# KURGIN ADMIN DATA STREAMLIT PUBLISH SMOKE v0.1

Repo: `kka45821-del/kurgin-streamlit-mvp`
Scope: cross-repo dev publish smoke checkpoint.
Status: dev publish/read smoke completed / not production launch.

Working repositories checked:

- `kurgin-admin-mvp`
- `kurgin-data`
- `kurgin-streamlit-mvp`

Repositories not changed:

- `kurgin-score-analyzer`
- `kurgin-formula-service`

This document records the completed controlled Admin -> Data -> Streamlit dev publish smoke.

This is a dev publish smoke, not a production launch. Temporary test stones are allowed in the dev catalog for this smoke. Real inventory launch requires cleanup of all `KRG-RICH-*`, `SMOKE`, `TEST`, and other temporary rows before launch.

This task does not change Analyzer, does not change formula/scoring, does not add payment/reserve/sold, does not add auth/pro roles, does not add PDF/report/Verify, does not redesign UI, and does not make production claims.

## 1. Final verdict

```text
PASS for Admin -> Data -> Streamlit publish/read smoke
RISK for price display semantics because public UI currently shows `по запросу` even for priced stones, unless request-only MVP behavior is intentional
```

Operational verdict:

```text
RISK
```

Interpretation:

- Live Admin publish was executed.
- Publication completed.
- `4/4` expected files were published to `kurgin-data`:
  - `catalog.json`
  - `data/catalog.json`
  - `stones.csv`
  - `upload_batches.csv`
- `kurgin-data` was updated through the Admin publish flow.
- `catalog.json` count is `32`.
- Schema remains `catalog_mvp_v2`.
- `KRG-RICH-*` stones are present in published data.
- Public Streamlit opened after publish.
- Public catalog displays `32` stones.
- Public catalog shows `main = 8` and `large = 8`.
- Stones display correctly.
- KURGIN Score displays.
- Tags display.
- `price_rub = 0` remains request-price / not buyable.
- No payment / reserve / sold behavior was observed.
- Tools / Index / Analyzer preview are not broken.

The remaining risk is price display semantics: public UI currently shows `по запросу` even for priced stones unless this is intentional request-only MVP behavior.

## 2. Dev publish smoke scope

This smoke allowed temporary dev/test stones:

- `KRG-RICH-*`
- possible other `SMOKE` / `TEST` / `DEV` rows if included in the Admin dev catalog

Boundary:

```text
dev publish smoke ≠ production launch
```

Before real inventory launch:

- remove or isolate all `KRG-RICH-*` rows;
- remove or isolate all `KRG-ML-*` rows if present anywhere;
- remove or isolate all `SMOKE` / `TEST` / `DEV` rows;
- re-run Admin -> Data -> Streamlit publish/read smoke on real inventory only.

## 3. Pre-publish result

Confirmed before publish:

- live Admin was opened;
- Admin runtime catalog / publish flow was used;
- publish was intentionally treated as dev smoke, not production launch;
- test stones were temporarily allowed because real inventory does not exist yet.

The exact Admin runtime payload was validated by the resulting published `kurgin-data` files.

## 4. Publish execution result

Publish status:

```text
PASS
```

Confirmed:

- live Admin publish executed;
- publication completed;
- `4/4` expected files published:
  - `catalog.json`
  - `data/catalog.json`
  - `stones.csv`
  - `upload_batches.csv`;
- `kurgin-data` updated.

Important:

```text
kurgin-data was updated through Admin publish, not by direct manual file editing in this task.
```

## 5. kurgin-data post-publish result

Post-publish status:

```text
PASS
```

Confirmed:

- `catalog.json` updated;
- `data/catalog.json` updated;
- `stones.csv` updated;
- `upload_batches.csv` updated;
- `catalog.json` count is `32`;
- schema remains `catalog_mvp_v2`;
- `KRG-RICH-*` stones are present in published data.

Expected published-file checklist:

| File | Result |
|---|---:|
| `catalog.json` | PASS |
| `data/catalog.json` | PASS |
| `stones.csv` | PASS |
| `upload_batches.csv` | PASS |
| schema `catalog_mvp_v2` | PASS |
| count `32` | PASS |
| `KRG-RICH-*` present | PASS |

## 6. Streamlit post-publish result

Post-publish public Streamlit status:

```text
PASS
```

Confirmed:

- public Streamlit opened after publish;
- catalog opens;
- catalog displays `32` stones;
- `main = 8`;
- `large = 8`;
- stones display correctly;
- KURGIN Score displays;
- tags display;
- Tools surface is not broken;
- Index surface is not broken;
- Analyzer preview is not broken.

## 7. Commerce and product-scope boundaries

Commerce-boundary status:

```text
PASS
```

Confirmed:

- `price_rub = 0` remains request-price / not buyable;
- no checkout behavior observed;
- no payment behavior observed;
- no reserve behavior observed;
- no sold behavior observed.

Active boundaries:

```text
price_rub = 0 -> request-price / not buyable
request ≠ order
favorite ≠ reserve
payment ≠ sold
Analyzer preview ≠ production Analyzer
Index ≠ exact price
Verify skeleton ≠ active verification service
dev publish smoke ≠ production launch
```

This smoke does not approve:

- payment;
- reserve automation;
- sold automation;
- auth/pro roles;
- PDF/report generation;
- KURGIN Verify activation;
- real Analyzer engine connection;
- Formula Service connection;
- production claims.

## 8. Price display semantics risk

Risk status:

```text
RISK
```

Observed:

```text
public UI currently shows `по запросу` even for priced stones
```

Interpretation:

- If the current MVP is intentionally request-only, this may be acceptable.
- If priced stones should display actual prices, this requires a separate UI/data-state review.
- This smoke does not approve a UI change.
- This smoke does not approve checkout/payment/reserve behavior.

Required follow-up before real inventory launch:

1. Decide whether public MVP is request-only.
2. If request-only: document that priced stones still show `по запросу` intentionally.
3. If prices should display: create a separate UI/data-state task.
4. Keep `price_rub = 0` request-price / not-buyable behavior protected.

## 9. Changed files / commits from this task

This documentation update changed only:

```text
docs/KURGIN_ADMIN_DATA_STREAMLIT_PUBLISH_SMOKE_V0_1.md
```

The live Admin publish updated `kurgin-data` through the Admin publish flow. Exact `kurgin-data` commit SHA should be recorded separately if available from the Admin publish output or GitHub history.

No Streamlit code was changed.
No Analyzer/formula/scoring code was changed.
No payment/reserve/sold/auth/PDF/Verify code was added.

Commit message for this documentation update:

```text
Update Admin Data Streamlit publish smoke result
```

## 10. Acceptance status

| Acceptance item | Status |
|---|---:|
| Publish executed or blocker recorded | PASS — publish executed |
| `kurgin-data` status checked | PASS — `4/4` files updated, count `32`, schema `catalog_mvp_v2` |
| Streamlit read checked | PASS — public Streamlit opened and displayed catalog |
| request-price/no-price not buyable | PASS |
| no payment/reserve/sold drift | PASS |
| changed files / commits listed | RISK — docs commit listed; exact `kurgin-data` commit should be recorded if available |
| final verdict included | PASS |

## 11. Required cleanup before real inventory launch

Before real inventory launch, execute a separate cleanup / rollback task:

- remove or isolate all `KRG-RICH-*` rows;
- remove or isolate all `KRG-ML-*` rows if present;
- remove or isolate all `SMOKE` / `TEST` / `DEV` rows;
- republish clean real inventory only;
- re-run Streamlit catalog smoke;
- verify no test rows appear publicly;
- verify price/request semantics are intended and documented.

## 12. Closure

Final runtime result:

```text
PASS for Admin -> Data -> Streamlit publish/read smoke
RISK for price display semantics because public UI currently shows `по запросу` even for priced stones, unless request-only MVP behavior is intentional
```

Operational document verdict remains:

```text
RISK
```

The full dev MVP publish/read path is confirmed: Admin publish updated `kurgin-data`, Streamlit read the updated catalog, public catalog displayed `32` stones safely, request-price/no-price stones remained not buyable, and Tools / Index / Analyzer preview remained available.

This is not production launch. Temporary test stones are allowed only for this dev smoke and must be removed or isolated before real inventory launch.
