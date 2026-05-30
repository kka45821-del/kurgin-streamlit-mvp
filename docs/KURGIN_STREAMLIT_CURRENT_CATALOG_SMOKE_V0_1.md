# KURGIN STREAMLIT CURRENT CATALOG SMOKE v0.1

Repo: `kka45821-del/kurgin-streamlit-mvp`
Scope: manual Streamlit current catalog smoke checkpoint.
Status: current public catalog smoke recorded / no data change.

This document records a manual smoke check of the current public Streamlit MVP storefront on already published catalog data.

Repositories not changed:

- `kurgin-admin-mvp`
- `kurgin-data`
- `kurgin-score-analyzer`
- `kurgin-formula-service`

This checkpoint did not change code, did not change UI, did not change data, did not change CI, did not publish, did not save Admin data, did not change Analyzer, did not change formula/scoring, did not change schema, and did not deploy production.

## 1. Final verdict

```text
PASS for current Streamlit catalog / public-safe surfaces
RISK for full Admin -> Data -> Streamlit publish flow because save/publish were not tested
```

Operational verdict:

```text
RISK
```

Interpretation:

- Current public catalog opens.
- Stones are displayed.
- Request-price / no-price stones do not become buyable.
- No checkout/payment/reserve/sold behavior appears.
- Tools / Index / Analyzer preview are not broken.
- Current public-safe Streamlit surfaces are usable at smoke level.

The remaining risk is the full Admin -> Data -> Streamlit flow, because Admin save and production publish were not tested in this Streamlit-only smoke.

## 2. What was checked

Manual current-catalog smoke result:

| Check | Result |
|---|---:|
| Catalog opens | PASS |
| Stones are displayed | PASS |
| Request-price / no-price stones do not become buyable | PASS |
| No checkout behavior appears | PASS |
| No payment behavior appears | PASS |
| No reserve behavior appears | PASS |
| No sold behavior appears | PASS |
| Tools are not broken | PASS |
| Index is not broken | PASS |
| Analyzer preview is not broken | PASS |
| Admin save tested | NOT TESTED |
| Production publish tested | NOT TESTED |
| `kurgin-data` changed | NO |

## 3. Current catalog smoke result

### 3.1. Catalog opens

Runtime status:

```text
PASS
```

Confirmed:

- public catalog opened;
- current published/fallback data path allowed the public catalog to render;
- there was no observed hard failure blocking catalog access.

### 3.2. Stones are displayed

Runtime status:

```text
PASS
```

Confirmed:

- stones are displayed in the public catalog;
- the current storefront can present catalog cards from the current data path.

Interpretation:

```text
Current public catalog display is operational at manual smoke level.
```

### 3.3. Request-price / no-price stones do not become buyable

Runtime status:

```text
PASS
```

Confirmed:

- request-price / no-price stones remained request-price / non-buyable;
- no active buy button or checkout-enabled behavior appeared for no-price stones.

Interpretation:

```text
request-price/no-price state remains non-buyable in the current public catalog smoke.
```

## 4. Commerce boundary smoke

Runtime status:

```text
PASS
```

Confirmed not observed:

- checkout activation;
- payment flow;
- reserve flow;
- sold-state automation;
- order creation;
- ownership claim;
- price lock.

Boundary preserved:

```text
request-price ≠ order
request-price ≠ reserve
request-price ≠ payment
favorite ≠ reserve
payment ≠ sold
```

This smoke does not approve adding any commerce functionality.

## 5. Tools / Index / Analyzer preview smoke

Runtime status:

```text
PASS
```

Confirmed:

- Tools surface is not broken;
- Index surface is not broken;
- Analyzer preview surface is not broken.

Boundary preserved:

```text
Analyzer preview ≠ production Analyzer
Analyzer preview ≠ certificate
Analyzer preview ≠ price valuation
Index ≠ exact price
Verify skeleton ≠ active verification service
```

This smoke does not approve:

- real Analyzer engine connection;
- Formula Service connection;
- PDF/report generation;
- paid Analyzer;
- Verify activation;
- result history/storage;
- auth/pro roles.

## 6. Full publish flow limitation

The following were not tested in this smoke:

- Admin save batch;
- Admin production publish;
- `kurgin-data` file update;
- Streamlit refresh after a new publish;
- post-publish catalog regression;
- rollback after publish.

Therefore the full Admin -> Data -> Streamlit publish flow remains:

```text
RISK: not fully tested
```

This is not a blocker for the current catalog smoke result. It only prevents marking the full publish chain as PASS.

## 7. Data / repo boundary

Explicitly not done:

- no Admin save;
- no publish to `kurgin-data`;
- no `catalog.json` update;
- no `data/catalog.json` update;
- no `stones.csv` update;
- no `upload_batches.csv` update;
- no Streamlit code update;
- no Streamlit UI update;
- no CI change;
- no Analyzer change;
- no formula/scoring change;
- no production deploy.

## 8. Blockers

Runtime blockers for current catalog smoke:

```text
None observed.
```

Remaining blockers / limitations for broader flow:

| ID | Limitation | Impact | Required future action |
|---|---|---|---|
| LIM-001 | Admin save was not tested in this smoke | Cannot mark save path PASS | Run separate clean save smoke only after rollback plan approval |
| LIM-002 | Production publish was not tested in this smoke | Cannot mark publish flow PASS | Run controlled publish smoke only after explicit approval |
| LIM-003 | Post-publish Streamlit refresh was not tested | Cannot mark full Admin -> Data -> Streamlit chain PASS | Run full flow smoke after save/publish approval |

## 9. Risk items

| ID | Risk | Severity | Handling |
|---|---|---:|---|
| RISK-001 | Full Admin -> Data -> Streamlit publish flow remains untested. | Medium | Keep full-flow verdict at RISK until save/publish smoke is complete. |
| RISK-002 | Request-price semantics must remain clear as catalog evolves. | Medium | Keep request/order/reserve/payment boundary smoke checks active. |
| RISK-003 | Tools/Index/Analyzer preview can be mistaken for production features. | Medium | Continue labeling them as public-safe MVP preview/skeleton surfaces. |
| RISK-004 | Published data changes may affect catalog display after future publish. | Medium | Re-run catalog smoke after any publish. |

## 10. Allowed next actions

Allowed next actions:

1. Keep this smoke result as manual evidence that the current public catalog opens and displays stones.
2. Re-run catalog smoke after any future `kurgin-data` publish.
3. Run clean save smoke only after rollback plan confirmation.
4. Run controlled publish smoke only after explicit approval.
5. Run full Admin -> Data -> Streamlit post-publish smoke only after save/publish are approved and executed.
6. Keep request-price / no-price commerce-boundary checks active.
7. Keep Tools / Index / Analyzer preview public-safe boundary checks active.

## 11. Blocked actions

Blocked by this smoke task:

- code changes;
- UI changes;
- data changes;
- CI changes;
- Admin save;
- publish to `kurgin-data`;
- changing `catalog.json`;
- changing `data/catalog.json`;
- changing `stones.csv`;
- changing `upload_batches.csv`;
- Analyzer changes;
- formula/scoring changes;
- production deploy;
- payment/reserve/sold;
- auth/pro roles;
- PDF/report/Verify;
- real Analyzer engine connection;
- Formula Service connection;
- cleanup deletion/move;
- file deletion;
- file moving.

## 12. Acceptance checklist

This document satisfies the current-catalog smoke documentation task if:

- `docs/KURGIN_STREAMLIT_CURRENT_CATALOG_SMOKE_V0_1.md` exists;
- catalog open result is recorded;
- stones displayed result is recorded;
- request-price / no-price non-buyable behavior is recorded;
- no checkout/payment/reserve/sold behavior is recorded;
- Tools / Index / Analyzer preview not-broken result is recorded;
- verdict is included;
- no code changes are made;
- no UI changes are made;
- no data changes are made;
- no CI changes are made;
- no publish is performed;
- Analyzer/formula/scoring are not touched;
- payment/reserve/sold/auth/PDF/Verify are not added.

## 13. Closure

Final runtime result:

```text
PASS for current Streamlit catalog / public-safe surfaces
RISK for full Admin -> Data -> Streamlit publish flow because save/publish were not tested
```

Operational document verdict remains:

```text
RISK
```

The current public Streamlit catalog smoke confirms that the existing catalog opens, displays stones, preserves request-price/no-price non-buyable behavior, and keeps Tools / Index / Analyzer preview surfaces available.

The full save/publish flow remains a separate untested path.
