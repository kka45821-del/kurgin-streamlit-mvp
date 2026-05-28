# ANALYZER PHASE 1 SMOKE CHECKPOINT v0.1

Repo: `kka45821-del/kurgin-streamlit-mvp`
Scope: public MVP / Tools → KURGIN Stone Analyzer.
Status: Phase 1 public preview skeleton checkpoint.

This checkpoint records the expected state of the KURGIN Stone Analyzer public preview skeleton after the Phase 1 form refinement.

## 1. Current status

KURGIN Stone Analyzer is currently a public preview skeleton.

Current expected state:

- Stone Analyzer is visible inside `Tools → KURGIN Stone Analyzer`.
- Manual preview mode is visible.
- Form-like controls are disabled / read-only.
- The UI shows a preview notice that data is not sent and calculation is not performed.
- CTA is disabled.
- Result block is a placeholder only.
- Limitations are visible.

Current non-active state:

- no Analyzer engine;
- no backend connection;
- no file upload;
- no formula disclosure;
- no PDF generation;
- no report generation;
- no certificate generation;
- no auth/login;
- no payment;
- no checkout;
- no order;
- no reserve;
- no sold logic.

## 2. UI smoke checklist

Use this checklist after any future change touching Tools, Analyzer preview, shared styles, shell navigation, or public MVP layout.

### Tools surface

- [ ] `?page=tools` opens.
- [ ] Tools tabs are visible.
- [ ] Stone Analyzer tab opens.
- [ ] KURGIN Index tab still opens.
- [ ] Verify / Mass Analyzer / Academy remain skeleton states.

### Stone Analyzer Phase 1 preview

- [ ] Manual preview mode is visible.
- [ ] Upload is marked later / inactive.
- [ ] Batch is marked later / inactive.
- [ ] Disabled form-like controls are visible.
- [ ] Shape select-looking field is visible.
- [ ] Carat input-looking field is visible.
- [ ] Color select-looking field is visible.
- [ ] Clarity select-looking field is visible.
- [ ] Optional geometry fields are visible.
- [ ] Preview notice is visible: `Форма показана как preview. Данные не отправляются и расчёт не выполняется.`
- [ ] CTA is visible and disabled: `Получить предварительный результат`.
- [ ] Adapter note is visible: `Engine будет подключён через adapter contract.`
- [ ] Limitations are visible.

### Required limitation wording

The preview must clearly communicate:

- [ ] not a certificate;
- [ ] not a valuation / price assessment;
- [ ] not a gemological conclusion;
- [ ] formula and internal coefficients are not disclosed.

## 3. Regression checklist

The Analyzer preview must not destabilize the already-stable public MVP.

### KURGIN Index

- [ ] Index opens.
- [ ] Index score selector works.
- [ ] Index view panel opens.
- [ ] Index close handle works.
- [ ] Index color filters work.
- [ ] Index clarity filters work.
- [ ] Index carat range filters work.
- [ ] Index share placeholder works or fails safely.
- [ ] Index PDF placeholder remains a placeholder only.

### Catalog

- [ ] Catalog opens.
- [ ] Catalog cards render.
- [ ] Catalog sections work.
- [ ] Catalog filters work.
- [ ] Catalog sorting works.
- [ ] Catalog empty state remains clear.

### Detail request flow

- [ ] Catalog card opens detail card.
- [ ] Request icon opens detail / request path.
- [ ] Request block is visible.
- [ ] MAX / Telegram / WhatsApp links are preserved or safely disabled if not configured.
- [ ] Request remains non-order / non-reserve / non-payment / non-price-lock.

### Favorites

- [ ] Favorite icon adds/removes a stone.
- [ ] Favorites badge updates.
- [ ] Favorites page opens.
- [ ] Saved stone opens detail card.
- [ ] Delete removes saved stone.

### Inactive surfaces

- [ ] Profile still says auth/login is unavailable.
- [ ] Cart / Requests still says checkout is inactive.
- [ ] Verify remains inactive skeleton.
- [ ] Mass Analyzer remains inactive skeleton.
- [ ] Academy remains inactive skeleton.

## 4. Forbidden changes

Do not include these in Analyzer Phase 1 preview work:

- Analyzer engine connection;
- backend connection;
- upload flow;
- real calculation;
- formula disclosure;
- scoring weight disclosure;
- penalty breakdown disclosure;
- internal diagnostics;
- debug trace;
- PDF generation;
- report generation;
- certificate wording;
- appraisal wording;
- catalog data changes;
- `catalog.json` changes;
- `public_index.json` changes;
- Index methodology changes;
- pricing/scoring formula changes;
- checkout logic;
- payment logic;
- order logic;
- reserve logic;
- sold logic;
- auth/login;
- profile roles;
- admin repo changes;
- data repo changes;
- analyzer repo changes.

## 5. Next phase gate

Before Phase 2, complete a separate architecture and code audit of `kurgin-score-analyzer`.

Phase 2 may not start until the following are identified and reviewed:

- pure engine function or stable calculation entrypoint;
- input schema expected by the engine;
- public-safe output mapping;
- unsupported shape behavior;
- missing-field behavior;
- error behavior;
- dependencies and deployment impact;
- whether engine code has Streamlit/UI assumptions;
- whether engine code exposes formula internals;
- whether engine code writes files or requires local state.

Phase 2 must use an adapter boundary.

Required before Phase 2 implementation:

- design adapter file, likely `services/analyzer_adapter.py` or equivalent;
- add tests / smoke checks for adapter states;
- verify no direct UI import of the Analyzer app;
- verify no formula internals are returned to public UI;
- verify no traceback or internal exception reaches public UI;
- verify KURGIN Index, catalog, request flow and favorites still work.

## 6. Checkpoint note

This document is a smoke checkpoint only.

No production code is changed by this document. No Analyzer engine is connected. No backend, upload, formula, PDF/report, auth, payment, checkout, order, reserve or sold logic is added.
