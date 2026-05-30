# KURGIN Analyzer Result and History Model V0.1

## 1. Purpose

This document describes the future model for Analyzer results and Analyzer history.

The purpose is to:

- describe future Analyzer result records;
- describe future analysis history;
- separate one-stone results from batch results;
- avoid implementing storage or history in the current MVP.

This is a planning document only. It does not authorize current MVP storage, profile, history, payment, PDF, report, or backend implementation.

## 2. Current MVP Lock

Current Tools Analyzer remains a skeleton / public preview.

Current MVP status:

- results are not saved;
- history is not implemented;
- profile is not implemented;
- PDF / report is not implemented;
- payment is not implemented;
- access / entitlement checks are not implemented;
- this is planning only.

The current Analyzer skeleton and mock flows must remain public-safe.

## 3. Result Types

Future result types may include:

- `one_stone_score_result`;
- `one_stone_full_result`;
- `batch_result`;
- `batch_row_result`;
- `manager_question_result`;
- `pdf_report_result_later`.

These types are planning concepts only.

## 4. One-Stone Score Result

A one-stone Score result is a fast public-safe result for one stone.

Public-safe fields:

- `result_id`;
- `user_id` later;
- `entitlement_id` later;
- `created_at`;
- `input_reference`;
- `status`;
- `score`;
- `score_band`;
- `short_summary`;
- `warnings`;
- `limitations`;
- `next_action`.

Must not include:

- `diagnostics`;
- `breakdown`;
- `triple_score`;
- `structure_modifier`;
- `raw_formula`;
- `weights`;
- `debug_trace`;
- `formula_source`;
- `certificate_claim`;
- `appraisal_claim`;
- `price_effect`;
- `payment_effect`;
- `reserve_effect`.

One-stone Score result is not a certificate and is not a price valuation.

## 5. Full One-Stone Result

A Full one-stone result may include a richer public-safe interpretation.

Potential fields:

- `result_id`;
- `user_id` later;
- `entitlement_id` later;
- `created_at`;
- `input_reference`;
- `status`;
- `KURGIN Score`;
- `score_band`;
- `summary`;
- `geometry_interpretation`;
- `risk_flags`;
- `strengths`;
- `warnings`;
- `limitations`;
- `manager_assisted_next_action`;
- `pdf_report_available` later.

Important boundaries:

- PDF / report may later become an output of Full one-stone analysis;
- PDF / report is not implemented in the current MVP;
- Full one-stone analysis is not a certificate;
- Full one-stone analysis is not price valuation.

## 6. Batch Result

A batch result represents an Excel / table analysis session.

Batch-level fields:

- `batch_result_id`;
- `user_id` later;
- `entitlement_id` later;
- `created_at`;
- `source_file_name`;
- `total_rows`;
- `ready_rows`;
- `skipped_rows`;
- `error_rows`;
- `status`;
- `result_excel_available` later.

Batch row fields:

- `row_id`;
- `report_number`;
- `shape`;
- `carat`;
- `color`;
- `clarity`;
- `status`;
- `score_band`;
- `warnings`;
- `limitations`;
- `next_action`.

Batch must not:

- publish catalog automatically;
- create order / reserve / payment;
- issue certificates;
- expose formula internals;
- write to `kurgin-data` directly.

## 7. Input Reference

Future stored results may reference input through a safe `input_reference`.

Allowed reference fields may include:

- `manual_input_summary`;
- `report_number`;
- `lab`;
- `source_mode`: `manual | photo_later | upload_later | batch_later`;
- `original_file_name` later.

Do not store in the current MVP:

- uploaded certificate image;
- uploaded PDF;
- uploaded Excel;
- raw OCR text;
- raw file content.

These may only be stored after a separate storage and privacy review.

## 8. History Model

Future Analyzer history may show:

- date;
- type of analysis;
- status;
- score_band;
- short summary;
- available actions;
- remaining access / entitlement status.

History must not show:

- formula internals;
- raw diagnostics;
- hidden penalty data;
- payment card data;
- internal admin notes.

History is not implemented in the current MVP.

## 9. Data Retention

Planning rules:

- uploaded files require a separate retention policy;
- report numbers and analysis results require privacy review;
- user should later have a way to request deletion;
- public UI must not be source of truth for stored results;
- storage must be backend-controlled.

No storage or database changes are approved by this document.

## 10. Manager-Assisted Questions

Future manager-assisted question records may include:

- `question_id`;
- `result_id`;
- `user_id`;
- `message`;
- `contact_method`;
- `status`;
- `created_at`;
- `manager_response` later.

Manager-assisted questions must not imply:

- order created;
- reserve created;
- price fixed;
- certification completed.

## 11. Relationship to Entitlement

Future results may reference `entitlement_id`.

Relationship rules:

- one-time entitlement becomes `used` after `result_ready`;
- 30-day access increments `used_count` through backend;
- public UI must not update entitlement usage directly.

Entitlement usage changes must be handled by a future backend / access service.

## 12. Relationship to Commercial Model

Relationship rules:

- Score Only produces `one_stone_score_result`;
- Full One-Stone Analysis produces `one_stone_full_result`;
- PDF / report may be attached only to Full analysis later;
- Batch access produces `batch_result` and `batch_row_result`.

Related documents:

- `docs/ANALYZER_COMMERCIAL_ACCESS_MODEL_V0_1.md`;
- `docs/ANALYZER_ENTITLEMENT_MODEL_V0_1.md`.

## 13. Forbidden Claims / Actions

Analyzer result and history layers must not claim or trigger:

- certificate;
- official appraisal;
- price valuation;
- exact market price;
- investment rating;
- guaranteed resale;
- automatic purchase;
- automatic reserve;
- catalog publish;
- payment / order creation.

Any claim near certification, pricing, investment quality, resale, catalog publication, payment, order, or reserve requires separate review.

## 14. Future Implementation Order

Recommended future order:

1. Result / history model docs.
2. Privacy / data retention review.
3. Backend storage design.
4. Profile / history UX design.
5. Entitlement integration.
6. Payment integration.
7. PDF / report after separate review.

Each stage requires separate approval.

## 15. Acceptance Criteria

This planning document is valid when:

- this document exists;
- this is docs-only;
- no code changes are made by this task;
- no UI changes are made by this task;
- no backend changes are made by this task;
- no storage / database changes are made by this task;
- no auth implementation is added;
- no payment implementation is added;
- no changes outside docs are required unless strictly necessary.

## 16. Status

Status: planning lock only.

Version: V0.1
