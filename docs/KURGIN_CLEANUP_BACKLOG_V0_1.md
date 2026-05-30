# KURGIN CLEANUP BACKLOG v0.1

Repo: `kka45821-del/kurgin-streamlit-mvp`
Scope: docs-only cleanup backlog.
Status: planning backlog only / cleanup not authorized.

This document prepares a future cleanup path for KURGIN legacy, review, staging, raw, duplicate and generated files after creation of the Active Source Index.

It does not delete, move, rename, refactor, rewrite or disable any file.
It does not change code, UI, data, CI, Analyzer, Admin, `kurgin-data`, deployment, formula logic or public behavior.

## 1. Purpose

The purpose of this backlog is to:

- reduce confusion between active source files, legacy materials, staging scaffolds, generated artifacts and raw assets;
- reduce spaghetti risk across multiple KURGIN repositories;
- prepare a controlled future cleanup process;
- document candidate areas for review without acting on them now;
- prevent accidental deletion of protected or active files;
- keep cleanup separate from feature work.

Current related orientation sources:

- `docs/KURGIN_ACTIVE_SOURCE_INDEX_V0_1.md`
- `docs/KURGIN_ACTIVE_SOURCE_INDEX_CHECK_V0_1.md`
- `docs/ANALYZER_REPO_STRUCTURE_MAP_V0_1.md` in `kurgin-score-analyzer`

This backlog is only a planning layer.

```text
cleanup backlog ≠ cleanup approval
candidate for review ≠ delete/move approval
legacy/review classification ≠ safe to delete
```

## 2. Cleanup principles

### 2.1. No cleanup without usage audit

No file may be deleted, moved, renamed or archived until a usage audit proves it is safe.

Usage audit must check at least:

- imports and runtime references;
- Streamlit page routing / navigation references;
- tests and smoke checks;
- GitHub Actions / CI references;
- data-loading paths;
- documentation references;
- external links or deployment references;
- manual operational use.

### 2.2. Classification before action

The correct order is:

```text
docs classification
→ usage audit
→ test / smoke coverage check
→ separate approved delete/move task
```

Classification alone is not enough to remove or move anything.

### 2.3. Tests before move/delete

Before any future deletion or move, the owning repository must have relevant tests or smoke checks.

At minimum, future cleanup should verify:

- public MVP still starts;
- catalog still loads;
- tools still render;
- Analyzer preview/skeleton still behaves as expected;
- request/payment/reserve/sold smoke protections are not weakened;
- Admin publish flow is not broken;
- published data schema is not changed;
- Analyzer contracts remain unchanged.

### 2.4. Protected files are excluded from deletion candidates

Protected / do-not-touch zones are not cleanup targets.

Protected files may be documented, mapped or audited, but not deleted or moved under a generic cleanup task.

### 2.5. No cleanup mixed with feature work

Cleanup must not be mixed with:

- new Analyzer features;
- UI redesign;
- payment/auth/reserve/sold work;
- formula/scoring changes;
- Admin changes;
- data schema changes;
- CI changes;
- production deployment.

Any cleanup task must be narrow, reversible where possible, and separately approved.

## 3. Candidate categories

### 3.1. `LEGACY_OR_REVIEW`

Files that may represent older prototypes, previous UI attempts, outdated plans, abandoned screens, deprecated wrappers or review-only materials.

Handling:

- classify first;
- do not delete now;
- verify whether any active route/import/test references them.

### 3.2. `STAGING_ONLY`

Files used only for staging, experiments, deployment trials or service candidates.

Handling:

- keep separate from production path;
- confirm no production dependency;
- do not treat as launch-ready implementation.

### 3.3. `HISTORICAL_DOCS`

Old docs, old OpenAPI snapshots, previous release notes, sync manifests, old handoff documents, old review notes.

Handling:

- preserve if they explain history;
- do not use as active source unless revalidated;
- archive only after separate approval.

### 3.4. `RAW_ASSETS`

Raw images, logo experiments, SVG duplicates, upload artifacts, generated visual files and non-source media.

Handling:

- usage audit before deletion;
- confirm not used by Streamlit, docs, markdown, static assets or external links;
- never delete current brand/source assets without explicit design/brand approval.

### 3.5. `DUPLICATE_OR_OLD_FILES`

Files with suffixes, duplicates, old versions, renamed copies or equivalent documents.

Handling:

- compare contents;
- identify active canonical file;
- verify references;
- delete/move only through a separate approved cleanup task.

### 3.6. `GENERATED_ARTIFACTS`

Generated reports, exports, cache-like outputs, smoke-test outputs, build artifacts, temporary PDFs, output spreadsheets, package archives.

Handling:

- verify whether needed for tests, demos or documentation;
- move/delete only with separate approval;
- never delete schema reference examples or golden fixtures unless replaced and tested.

### 3.7. `DO_NOT_TOUCH`

Protected files and paths that must not be changed by cleanup.

Includes at minimum:

- formula/scoring;
- core Analyzer internals;
- public-safe adapter / public-safe output contracts;
- API contracts;
- Excel/PDF output schema;
- admin publish flow;
- catalog price/request state logic;
- published data schema;
- smoke checks protecting request/payment/reserve/sold boundaries;
- secrets, env names and deployment credentials.

## 4. Repo-level cleanup backlog

## 4.1. `kurgin-streamlit-mvp`

Role:

```text
public MVP / mobile-first storefront / catalog / tools / Analyzer preview / Index
```

Candidate for review:

- old uploads;
- raw visual assets;
- duplicate SVGs / logo experiments;
- old prototype files;
- unused generated artifacts;
- old docs that predate Active Source Index;
- obsolete temporary files;
- duplicate screenshots or exported assets.

Do not touch:

- active public MVP code;
- catalog loading and rendering;
- tools page and Analyzer preview/skeleton;
- KURGIN Index public-safe surface;
- request/payment/reserve/sold smoke checks;
- active docs:
  - `docs/KURGIN_ACTIVE_SOURCE_INDEX_V0_1.md`;
  - `docs/KURGIN_ACTIVE_SOURCE_INDEX_CHECK_V0_1.md`;
  - `docs/KURGIN_CLEANUP_BACKLOG_V0_1.md`;
- public-safe integration docs;
- data-loading contract with `kurgin-data`;
- deployment configuration unless a separate deployment task authorizes it.

Risk:

- deleting a raw asset that is still referenced by Streamlit or docs;
- deleting a smoke check that protects state separation;
- confusing Analyzer preview/skeleton with inactive legacy UI;
- accidentally changing public MVP behavior while doing cleanup.

Future action needed:

1. Create a file inventory for candidate assets and old docs.
2. Run usage audit for each candidate path.
3. Verify public MVP smoke checks.
4. Create a separate delete/move task only for proven unused files.

## 4.2. `kurgin-admin-mvp`

Role:

```text
admin / Excel import / validation / preview / publish
```

Candidate for review:

- old import experiments;
- staging upload samples;
- old admin UI drafts;
- generated previews;
- obsolete local test artifacts;
- duplicate docs or notes from early admin planning.

Do not touch:

- Excel import logic;
- validation logic;
- preview logic;
- publish workflow;
- admin-side state handling;
- publish contract to `kurgin-data`;
- any file that affects data quality or publication gates;
- secrets/env names.

Risk:

- breaking Admin -> Data -> Streamlit flow;
- weakening validation before publication;
- changing data output shape;
- deleting a sample fixture that is still used for manual validation.

Future action needed:

1. Map current admin publish flow.
2. Identify generated vs fixture vs source files.
3. Confirm which samples are still used for validation.
4. Create a separate admin cleanup task only after publish-flow tests exist.

## 4.3. `kurgin-data`

Role:

```text
published catalog / data layer
```

Candidate for review:

- obsolete exported snapshots;
- old sample data;
- duplicate generated files;
- historical backups not used by current MVP;
- old sync manifests.

Do not touch:

- published schema;
- current catalog data files;
- data files consumed by `kurgin-streamlit-mvp`;
- identifiers used by public MVP cards;
- any source-of-truth data layer file;
- generated data required for reproducibility or rollback unless replaced by an approved backup process.

Risk:

- breaking public catalog loading;
- changing published schema;
- removing data needed for rollback or audit;
- desynchronizing Admin -> Data -> Streamlit assumptions.

Future action needed:

1. Document current published data schema.
2. Identify files consumed by Streamlit.
3. Separate active published data from snapshots/backups.
4. Create a separate data cleanup task only after data contract tests are green.

## 4.4. `kurgin-score-analyzer`

Role:

```text
private Analyzer engine / SDK / API / public-safe adapter / Excel output / staging
```

Candidate for review:

- `ui_pages/` legacy/review pages unless proven active;
- old `api_docs/` / OpenAPI snapshots unless regenerated and approved;
- staging scaffolds;
- historical deployment notes;
- generated reports and temporary exports;
- old sync manifests;
- duplicate docs or release notes;
- obsolete smoke output artifacts.

Do not touch:

- formula/scoring;
- core engine;
- SDK internals;
- API response contracts;
- `public_safe_analyzer_adapter`;
- Excel output schema;
- PDF output schema;
- golden datasets / regression fixtures;
- regression runner behavior;
- secrets/env names;
- docs that define active Analyzer repository structure and public-safe boundary.

Risk:

- formula/scoring regression;
- breaking SDK/API behavior;
- changing public-safe output contract;
- breaking Excel/PDF outputs;
- deleting regression fixtures;
- confusing staging Selectel deployment with production Formula Service;
- exposing private formula logic through cleanup mistakes.

Future action needed:

1. Use `docs/ANALYZER_REPO_STRUCTURE_MAP_V0_1.md` as the initial Analyzer repo orientation source.
2. Audit `ui_pages/` for active imports/routes before classification.
3. Regenerate or mark old OpenAPI docs as historical only after current API docs are confirmed.
4. Classify `deployment/selectel_staging` as staging-only unless separately approved for production.
5. Create a separate Analyzer cleanup task only after regression, API, Excel and PDF tests are green.

## 4.5. `kurgin-formula-service`

Role:

```text
future private formula service / staging candidate
```

Candidate for review:

- staging deployment files;
- old API experiment files;
- old smoke responses;
- obsolete local deployment notes;
- duplicate OpenAPI snapshots;
- temporary logs or generated outputs.

Do not touch:

- current FastAPI app behavior;
- auth / HTTPBearer behavior if already stabilized;
- formula-service endpoint contracts;
- environment variable names;
- private keys/secrets;
- any code that affects formula result behavior;
- deployment configs unless a separate staging/deploy task authorizes it.

Risk:

- breaking private API staging candidate;
- changing auth behavior;
- accidentally exposing or rotating secrets;
- confusing staging candidate with production deployment;
- changing formula behavior indirectly.

Future action needed:

1. Confirm current service role: staging candidate, not production dependency.
2. Audit OpenAPI and smoke artifacts.
3. Separate staging files from production-candidate specs.
4. Create a separate cleanup task only after service contract checks pass.

## 5. Analyzer special notes

Analyzer cleanup must be especially conservative.

### 5.1. `ui_pages/`

Default classification:

```text
LEGACY_OR_REVIEW unless proven active
```

Do not delete or move until:

- active imports/routes are checked;
- manual use is checked;
- current app entry points are verified;
- regression/smoke checks pass.

### 5.2. Old `api_docs/` / OpenAPI docs

Default classification:

```text
HISTORICAL_DOCS unless regenerated / approved as current
```

Do not treat old OpenAPI docs as active contracts unless they match the current API and are explicitly approved.

### 5.3. `deployment/selectel_staging`

Default classification:

```text
STAGING_ONLY
not production
```

This path must not be treated as production Formula Service deployment.

### 5.4. `public_safe_analyzer_adapter`

Default classification:

```text
DO_NOT_TOUCH
```

This is a protected public/private boundary area.

### 5.5. Formula / scoring / core engine

Default classification:

```text
DO_NOT_TOUCH
```

Formula, scoring and core engine files are excluded from generic cleanup.

They must not be deleted, moved, simplified or refactored under cleanup backlog work.

## 6. Streamlit special notes

### 6.1. Active Streamlit scope

The following are active public MVP areas:

- public MVP storefront;
- catalog;
- tools;
- Analyzer preview/skeleton;
- KURGIN Index;
- active docs created after Active Source Index.

These are not cleanup candidates by default.

### 6.2. Active source index docs

The following docs are active orientation/control docs in `kurgin-streamlit-mvp`:

- `docs/KURGIN_ACTIVE_SOURCE_INDEX_V0_1.md`
- `docs/KURGIN_ACTIVE_SOURCE_INDEX_CHECK_V0_1.md`
- `docs/KURGIN_CLEANUP_BACKLOG_V0_1.md`

Do not delete or move them under cleanup.

### 6.3. Request/payment/reserve/sold smoke checks

Smoke checks or tests that protect these distinctions are protected:

```text
request ≠ order
favorite ≠ reserve
payment ≠ sold
Analyzer ≠ certificate
Analyzer ≠ price valuation
Index ≠ exact price
```

Do not remove them during cleanup.

### 6.4. Old uploads / raw assets / duplicate SVGs

Default classification:

```text
RAW_ASSETS or DUPLICATE_OR_OLD_FILES
```

Future deletion requires:

- reference scan;
- Streamlit static usage check;
- markdown/docs usage check;
- current brand/design usage check;
- confirmation that the asset is not part of active MVP or brand source.

## 7. Cleanup phases

### Phase 1 — create backlog only

Status:

```text
current phase
```

Allowed:

- create this backlog;
- classify cleanup categories;
- list candidate areas;
- record protected zones;
- identify future audit needs.

Not allowed:

- deletion;
- moving files;
- refactor;
- code changes;
- UI changes;
- data or CI changes.

### Phase 2 — usage audit per candidate

Future phase only.

Allowed after separate approval:

- scan candidate files;
- check imports/routes/references;
- check docs links;
- check CI/test references;
- mark files as active / unused / historical / protected / unknown.

Output should be a usage-audit document, not deletion.

### Phase 3 — add/verify tests before moving/deleting

Future phase only.

Required before move/delete:

- relevant smoke checks are present;
- repository tests pass;
- data contracts are verified;
- Analyzer regression and output contracts are protected where relevant;
- public MVP behavior remains unchanged.

### Phase 4 — delete/move only with separate approved task

Future phase only.

Allowed only if:

- specific files are named;
- usage audit is complete;
- tests are green;
- rollback path is clear;
- task explicitly approves delete/move;
- no protected files are included.

## 8. Blocked actions

Blocked by this backlog:

- no deletion;
- no file moving;
- no renaming;
- no code refactor;
- no UI changes;
- no data schema changes;
- no CI changes;
- no Analyzer changes;
- no Admin changes;
- no `kurgin-data` changes;
- no formula/scoring changes;
- no API contract changes;
- no Excel/PDF output schema changes;
- no production deploy;
- no production Formula Service deployment;
- no source-index rewrite;
- no Gate document rewrite;
- no new product scope.

## 9. Immediate backlog items

| ID | Repo | Candidate area | Category | Current action | Future required action |
|---|---|---|---|---|---|
| CLN-001 | `kurgin-streamlit-mvp` | old uploads / raw assets / duplicate SVGs | RAW_ASSETS / DUPLICATE_OR_OLD_FILES | classify only | usage audit before deletion |
| CLN-002 | `kurgin-streamlit-mvp` | old prototype files | LEGACY_OR_REVIEW | classify only | route/import/reference audit |
| CLN-003 | `kurgin-streamlit-mvp` | generated artifacts | GENERATED_ARTIFACTS | classify only | confirm not needed for docs/tests |
| CLN-004 | `kurgin-admin-mvp` | old import/admin samples | LEGACY_OR_REVIEW | reference only | audit after admin publish-flow map |
| CLN-005 | `kurgin-data` | old snapshots/backups | HISTORICAL_DOCS / GENERATED_ARTIFACTS | reference only | data contract audit |
| CLN-006 | `kurgin-score-analyzer` | `ui_pages/` | LEGACY_OR_REVIEW | reference only | prove active/inactive before action |
| CLN-007 | `kurgin-score-analyzer` | old `api_docs/` / OpenAPI docs | HISTORICAL_DOCS | reference only | compare with current API docs |
| CLN-008 | `kurgin-score-analyzer` | `deployment/selectel_staging` | STAGING_ONLY | reference only | keep staging/prod separated |
| CLN-009 | `kurgin-score-analyzer` | generated reports / exports | GENERATED_ARTIFACTS | reference only | verify tests/docs dependency |
| CLN-010 | `kurgin-formula-service` | old smoke/OpenAPI/deploy artifacts | STAGING_ONLY / HISTORICAL_DOCS | reference only | service contract audit |

## 10. Do-not-touch summary

Do not include these in generic cleanup:

- formula/scoring;
- core Analyzer engine;
- public-safe analyzer adapter;
- public-safe output contracts;
- API response contracts;
- Excel output schema;
- PDF output schema;
- regression fixtures / golden datasets;
- catalog price/request state logic;
- request/payment/reserve/sold smoke checks;
- Admin publish flow;
- `kurgin-data` published schema;
- secrets/env/deployment credentials;
- active source index and validation docs;
- active public MVP catalog/tools/Index/Analyzer preview surfaces.

## 11. Acceptance checklist

This document satisfies the cleanup-backlog task if:

- only `docs/KURGIN_CLEANUP_BACKLOG_V0_1.md` is created;
- no code changes are made;
- no UI changes are made;
- no data changes are made;
- no CI changes are made;
- no files are deleted or moved;
- cleanup is explicitly not authorized yet;
- repo-level sections are included;
- do-not-touch zones are included;
- all non-Streamlit repositories remain reference-only in this backlog.

## 12. Closure

Final status:

```text
BACKLOG CREATED
CLEANUP NOT AUTHORIZED
```

This backlog prepares future cleanup discipline.
It does not perform cleanup.
It does not approve cleanup.
It does not change current MVP scope or repository behavior.
