# KURGIN Tools Analyzer Structure Lock V0.1

## 1. Purpose

This document locks the current structure of the KURGIN Tools Analyzer layer.

The purpose is to prevent uncontrolled mixing between:

- KURGIN Stone Analyzer;
- KURGIN Mass Analyzer;
- payment / checkout / reserve flows;
- Admin logic;
- Catalog publishing;
- Formula internals.

This is a structure lock, not a production launch plan. It does not introduce new functionality, claims, backend connections, commercial flows, or formula exposure.

## 2. Current Tools

The current Tools layer contains the following tools:

1. KURGIN Stone Analyzer
2. KURGIN Mass Analyzer
3. KURGIN Index
4. KURGIN Verify
5. KURGIN Academy

Each tool must keep a clear responsibility boundary.

## 3. KURGIN Stone Analyzer Boundary

KURGIN Stone Analyzer is for one-stone analysis only.

Current allowed one-stone modes:

- Фото / camera / later;
- Загрузка / file / later;
- Вручную / active now.

The current active mode is manual parameter entry.

Stone Analyzer must not become:

- Excel analyzer;
- batch analyzer;
- catalog publishing tool;
- checkout tool;
- payment tool;
- reserve tool;
- certificate generator;
- price valuation tool.

Stone Analyzer may provide a public-safe quality interpretation only.

It must not create purchase pressure, financial conclusions, official claims, or ownership states.

## 4. KURGIN Mass Analyzer Boundary

KURGIN Mass Analyzer is for Excel / table / batch workflows only.

Safe skeleton flow:

```text
Upload → Validate → Preview → Confirm → Analyze → Results table → Row detail → Export result
```

Current state:

- no real upload;
- no real Excel processing;
- no real backend call;
- no real batch analysis execution;
- no catalog publishing;
- no order creation;
- no reserve creation;
- no payment flow;
- no PDF reports;
- no paid Analyzer model yet.

Mass Analyzer must remain separate from Stone Analyzer.

Excel / table / batch logic belongs in Mass Analyzer, not in Stone Analyzer.

## 5. Formula / Analyzer Boundary

The public MVP must not import or expose raw formula internals.

The current public UI skeleton must not call Formula Service directly.

Future live integration must go through an approved public-safe adapter or API boundary.

Forbidden public fields / internals:

- diagnostics;
- breakdown;
- triple_score;
- structure_modifier;
- raw_formula;
- weights;
- debug_trace.

Additional internal formula, penalty, trace, or coefficient data must remain outside public UI.

## 6. File Responsibility

Current responsibility map:

- `ui/pages/tools_page.py` — composition and tabs only;
- `ui/pages/tools/analyzer_preview.py` — Stone Analyzer UI skeleton;
- `ui/pages/tools/mass_analyzer_preview.py` — Mass Analyzer UI skeleton;
- `services/analyzer_adapter.py` — public-safe demo/mock adapter for one-stone preview;
- `scripts/smoke_analyzer_preview_ui.py` — public safety smoke check.

Files should not silently expand beyond these responsibilities.

## 7. Spaghetti Prevention Rules

Do not add live backend calls in UI render files.

Do not add payment, access, subscription, or role logic inside:

- `ui/pages/tools/analyzer_preview.py`;
- `ui/pages/tools/mass_analyzer_preview.py`.

Do not add Excel parsing inside UI files.

Do not add catalog writes from Tools UI.

Do not add Formula Service calls directly into public UI components.

Do not mix Admin workflows into Tools UI.

If a file starts exceeding clear responsibility, create a dedicated service / adapter module or a structure issue before extending it.

## 8. Future Stages

Possible future stages, each requiring separate review:

1. Interactive Stone Analyzer manual input.
2. Live Analyzer integration through a public-safe adapter.
3. Batch Analyzer contract.
4. Commercial access model.
5. Profile / history layer.
6. PDF / report layer after separate review.

None of these are approved by this document.

This document only preserves the structural boundary for future work.

## 9. Forbidden Claims / Actions

The Tools Analyzer layer must not expose or imply:

- купить;
- оплатить;
- зарезервировать;
- получить сертификат;
- оценить стоимость;
- официальная оценка;
- инвестиционный рейтинг;
- точная рыночная цена;
- гарантия;
- catalog publish.

These claims/actions require separate legal, product, and implementation review.

## 10. Acceptance Criteria

This structure lock is valid when:

- this document exists;
- no code changes are required by this task;
- no UI changes are required by this task;
- no backend changes are required by this task;
- no test changes are required unless a docs index later needs explicit registration;
- Tools Analyzer boundaries remain clear;
- Stone Analyzer remains one-stone only;
- Mass Analyzer remains Excel / table / batch only;
- Formula internals remain outside public UI.

## 11. Status

Status: locked for current MVP skeleton.

Version: V0.1
