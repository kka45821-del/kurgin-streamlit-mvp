# KURGIN ACTIVE SOURCE INDEX v0.1

Repo: `kka45821-del/kurgin-streamlit-mvp`
Scope: docs-only orientation source.
Status: active source index / MVP stabilization orientation.

This document explains the current active source map for KURGIN after the project split across multiple repositories and after Analyzer stabilization work.

It does not approve production launch, production deployment, new public promises, new Analyzer features, public formula disclosure, payment activation, reserve/sold flows, auth/pro roles, data migration, UI changes, CI changes, or code implementation.

## 1. Purpose

This document exists to:

- explain the current KURGIN source and repository map;
- reduce confusion between strategy, public MVP, future work, staging work, and legacy/review materials;
- give contributors a stable orientation point before changing the public MVP repository;
- preserve the private/public Analyzer boundary;
- prevent staging or prototype files from being mistaken for production launch readiness.

This document does not rewrite Stage 0 or Gate source documents. It is an index and orientation layer only.

## 2. Current KURGIN working definition

KURGIN is a controlled commerce and analysis platform for laboratory diamonds / lab-grown diamonds for the Russian market.

Current implementation status:

```text
MVP prototype / stabilization
not production launch
```

Current KURGIN consists of:

- a public MVP storefront and mobile-first catalog surface;
- an admin data-publication workflow;
- a published data layer;
- a private Analyzer / formula / SDK / API contour;
- a future private formula-service candidate.

## 3. Active strategic sources

The following strategic and gate documents remain active orientation and boundary sources:

- Strategic Foundation;
- Gate 1 Legal / Operations Guardrails;
- Gate 1.5 Decision Register;
- Claims Register;
- Gate 2 SEO Scope and Controlled Semantic SEO Map;
- Gate 3 Content / Meaning Map;
- Gate 4 Page Architecture sources;
- Gate 5 UX Scope, UX Structure, and Interaction Flow sources;
- Gate 6 Design Scope sources;
- Analyzer repository structure / integration planning sources.

Interpretation:

```text
strategic / gate documents control meaning and boundaries;
they are not direct code implementation approval.
```

The gate sources should be used to preserve:

- KURGIN identity as a laboratory-diamond / lab-grown-diamond platform;
- MVP catalog eligibility boundaries;
- Analyzer / KURGIN Score / Index claim boundaries;
- payment / reserve / sold separation;
- supplier and specialist boundaries;
- public/private formula separation;
- Russia-market orientation.

They should not be read as permission to implement new code, connect private engines, publish future features, or launch production flows.

## 4. Active implementation repositories

### 4.1. `kurgin-streamlit-mvp`

Role:

```text
public MVP / mobile-first storefront / catalog / tools / Analyzer preview / Index
```

Current status:

- active public MVP prototype and stabilization repository;
- main working repository for public Streamlit surfaces;
- current repo for this document.

Controls:

- public MVP orientation;
- mobile-first storefront behavior;
- catalog and public product-surface presentation;
- public-safe tools and Analyzer preview/skeleton surfaces;
- KURGIN Index public-safe surface;
- docs that explain safe future integration boundaries.

Must not control:

- private formula/scoring logic;
- private Analyzer internals;
- source-of-truth published catalog data outside the published data contract;
- admin import/publish authority;
- production payment/reserve/sold logic;
- secrets, deployment credentials, or formula-service credentials.

### 4.2. `kurgin-admin-mvp`

Role:

```text
admin / Excel import / validation / preview / publish
```

Current status:

- active admin-side MVP workflow repository;
- separate from the public storefront.

Controls:

- controlled data intake;
- Excel import flow;
- validation and preview before publication;
- admin-side publish workflow to the data layer.

Must not control:

- public UI direction in `kurgin-streamlit-mvp`;
- private formula internals;
- public payment/reserve/sold claims;
- final legal/operations policy wording;
- published-data schema changes without separate approval.

### 4.3. `kurgin-data`

Role:

```text
published catalog / data layer
```

Current status:

- active data repository for published catalog/data output.

Controls:

- published data files used by the public MVP;
- catalog data contract consumed by Streamlit;
- data state that should be stable and reviewable.

Must not control:

- admin import UI;
- public UI components;
- formula/scoring calculations;
- private Analyzer internals;
- unreviewed schema expansion;
- secrets or deployment credentials.

### 4.4. `kurgin-score-analyzer`

Role:

```text
private Analyzer engine / SDK / API / public-safe adapter / Excel output / staging
```

Current status:

- active private Analyzer and stabilization repository;
- not public storefront code;
- source for private scoring, SDK/API behavior, safe adapter contracts, and Excel output logic.

Controls:

- Analyzer core behavior;
- private engine and SDK structure;
- API/staging contracts;
- Excel output behavior;
- public-safe adapter boundary;
- internal scoring-related output contracts.

Must not control:

- public Streamlit UI layout directly;
- catalog publication authority;
- public formula disclosure;
- production public connection to Streamlit without separate approval;
- public paid Analyzer/product flows without legal/privacy/payment readiness.

### 4.5. `kurgin-formula-service`

Role:

```text
future private formula service / staging candidate
```

Current status:

- future / staging candidate;
- not production deployment;
- not public MVP dependency unless separately approved.

Controls:

- candidate private service wrapper around formula/analyzer behavior;
- future API service staging experiments;
- future private deployment planning.

Must not control:

- current public MVP behavior;
- public Streamlit production dependency;
- public formula disclosure;
- production API claims;
- production deploy or credentials.

## 5. Current MVP scope

Current public MVP scope is limited to:

- public MVP catalog / mobile-first site;
- public-safe catalog display using published data;
- Admin -> Data -> Streamlit publication flow;
- Analyzer preview/skeleton only in the public MVP;
- KURGIN Index and tools as controlled public-safe surfaces;
- documentation that clarifies future integration and boundary rules.

Current MVP explicitly excludes:

- production payment flow;
- production reserve flow;
- production sold-state automation;
- public formula disclosure;
- private Analyzer engine connection to the public Streamlit app;
- public paid Analyzer/report/Verify flows;
- auth/pro role activation.

## 6. Future / not current MVP

The following are future or not-current-MVP items unless a separate approval, spec, review, and implementation task explicitly authorizes them:

- paid Analyzer;
- 30-day access;
- auto-renewal;
- saved card;
- PDF/report generation;
- KURGIN Verify UI;
- result history storage;
- auth/pro roles;
- payment;
- reserve/sold;
- real engine connection to public Streamlit;
- production Formula Service deployment.

These items may exist in strategy, planning docs, private Analyzer staging, or skeleton UI language, but they are not active public MVP launch scope.

## 7. Legacy / review zones

The following should be treated as legacy, staging, or review-only unless a current task explicitly reactivates them:

- old UI/prototype files;
- old OpenAPI docs;
- staging scaffolds;
- raw visual assets;
- duplicate docs;
- release notes;
- sync manifests;
- obsolete screenshots and generated artifacts;
- experimental Analyzer wrappers;
- any files that describe a possible future flow but are not connected to current MVP execution.

Legacy/review material must not be used as automatic proof that a feature is approved, production-ready, legally approved, public-safe, or active in the MVP.

## 8. Protected / do-not-touch zones

The following areas are protected and must not be changed without separate explicit approval:

- formula/scoring;
- core Analyzer internals;
- public-safe output contracts;
- catalog price/request state logic;
- admin publish flow;
- `kurgin-data` published schema;
- API response contracts;
- Excel/PDF output schema;
- secrets, env names, deployment credentials, tokens, and private service keys.

For public MVP tasks, assume these areas are read-only unless the task explicitly says otherwise.

## 9. Main current risks

Current practical risks:

- Analyzer feature-growth before backend/legal/privacy readiness;
- private formula logic leaking into public surfaces;
- Streamlit becoming overloaded with backend, admin, payment, auth, Analyzer, and service responsibilities;
- request-price / request-help states being confused with buyable catalog items;
- staging being mistaken for production;
- legacy files being mistaken for active paths;
- public Analyzer preview being mistaken for full private engine connection;
- future commercial access models being mistaken for current MVP scope.

## 10. Safe next actions

Safe next actions:

- stabilization;
- documentation clarification;
- smoke tests;
- contract tests;
- public/private boundary hardening;
- CI green checks;
- repository maps;
- cleanup backlog creation;
- review notes that do not delete, move, or rewrite active code/data.

These actions should preserve existing behavior and clarify boundaries.

## 11. Blocked without separate approval

The following are blocked without separate approval:

- new Analyzer features;
- real engine connection to public Streamlit;
- PDF/report/Verify/payment/auth/storage implementation;
- formula/scoring changes;
- file deletion cleanup;
- file move cleanup;
- production deploy;
- production Formula Service deployment;
- public paid Analyzer access;
- public reserve/sold/payment activation;
- changes to published data schema;
- changes to API/Excel/PDF output contracts.

## 12. Repository handling rule

Current task boundary:

```text
Only `kka45821-del/kurgin-streamlit-mvp` may be changed.
All other repositories are reference-only for this source index.
```

Do not change:

- `kurgin-admin-mvp`;
- `kurgin-data`;
- `kurgin-score-analyzer`;
- `kurgin-formula-service`.

## 13. Acceptance checklist

This document satisfies the active-source-index task if:

- only `docs/KURGIN_ACTIVE_SOURCE_INDEX_V0_1.md` is created;
- no code changes are made;
- no UI changes are made;
- no data changes are made;
- no CI changes are made;
- no files are deleted or moved;
- no repository other than `kurgin-streamlit-mvp` is touched;
- active strategy, active implementation, current MVP, future/not-MVP, legacy/review, and protected/do-not-touch zones are separated;
- current implementation is described as MVP prototype / stabilization, not production launch.
