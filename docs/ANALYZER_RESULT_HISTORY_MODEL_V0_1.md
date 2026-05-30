# KURGIN Analyzer Result and History Model V0.1

## 1. Purpose

This document describes the future model for Analyzer results, Analyzer history, and KURGIN Verify.

The purpose is to:

- describe future Analyzer result records;
- describe future analysis history in Profile;
- describe KURGIN Verify as the public authenticity base for issued Full one-stone analysis reports;
- separate one-stone results from batch results;
- separate Profile history from KURGIN Verify;
- avoid implementing storage, history, Verify, PDF, or report generation in the current MVP.

This is a planning document only. It does not authorize current MVP storage, profile, history, payment, PDF, report, Verify, or backend implementation.

## 2. Current MVP Lock

Current Tools Analyzer remains a skeleton / public preview.

Current MVP status:

- demo / public preview / mock results are not stored;
- results are not saved;
- history is not implemented;
- profile is not implemented;
- PDF / report generation is not implemented;
- KURGIN Verify database is not implemented;
- storage / database is not implemented;
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
- `pdf_report_result_later`;
- `verify_record_later`.

`verify_record_later` applies only to issued Full one-stone analysis reports.

It is a planning concept only and is not implemented in the current MVP.

## 4. Storage Rule

Do not store in the current MVP:

- demo result;
- public preview / mock result;
- unfinished form input;
- raw mock result.

May be stored later after backend, access, and privacy review:

- paid Score Only result;
- paid Full one-stone analysis result;
- admin-granted / free-granted Score Only result;
- admin-granted / free-granted Full one-stone analysis result;
- Mass Analyzer result after real batch analysis.

Public UI must not be the source of truth for stored results.

## 5. One-Stone Score Result

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

Score Only does not have to include PDF.

## 6. Full One-Stone Result

A Full one-stone result may include a richer public-safe interpretation.

Potential fields:

- `result_id`;
- `user_id` later;
- `entitlement_id` later;
- `KURGIN Analyzer Report Number`;
- `verification_code`;
- `QR code` later;
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
- `pdf_report_available` later;
- `pdf_download_available` later.

Important boundaries:

- Full one-stone analysis may later produce a PDF / report;
- PDF / report is the output of Full one-stone analysis;
- PDF / report is not implemented in the current MVP;
- Full one-stone analysis is not a certificate;
- Full one-stone analysis is not price valuation;
- Full one-stone analysis is not an investment recommendation.

## 7. KURGIN Analyzer Report Number

Each issued Full one-stone analysis must have its own unique KURGIN Analyzer Report Number.

Example format:

```text
KURGIN-ANL-2026-8F4K29QX
```

Rules:

- KURGIN Analyzer Report Number is the number of the issued KURGIN Analyzer report;
- the number must appear in the PDF / report;
- the number is used to find the report in KURGIN Verify;
- the number should be suitable for QR verification later;
- KURGIN Analyzer Report Number is separate from a laboratory report number;
- laboratory report numbers such as IGI / GIA report numbers must not be the only key for downloading a KURGIN PDF;
- KURGIN Analyzer Report Number and / or `verification_code` is the key for KURGIN Verify.

## 8. KURGIN Verify

KURGIN Verify is the future public verification database for issued Full one-stone analysis reports.

KURGIN Verify is:

- available to anyone;
- applied to issued KURGIN Analyzer reports;
- not the same as personal Profile history;
- not a public search of all laboratory certificates.

Verify input may include:

- KURGIN Analyzer Report Number;
- `verification_code`;
- QR code later.

Verify may show:

- `verification_status`;
- KURGIN Analyzer Report Number;
- `analysis_type`;
- `created_at`;
- `score_band`;
- short public summary;
- limitations;
- PDF download link for the issued Full one-stone analysis report.

Verify must not show:

- user personal data;
- payment data;
- internal admin notes;
- formula internals;
- diagnostics;
- breakdown;
- triple_score;
- structure_modifier;
- raw_formula;
- weights;
- debug_trace;
- entitlement_id.

## 9. PDF Download Through Verify

A PDF of the Full one-stone analysis report may later be downloadable through KURGIN Verify.

Rules:

- PDF download through Verify is available only for issued Full one-stone analysis reports;
- PDF download should use KURGIN Analyzer Report Number and / or `verification_code`;
- Score Only does not have to include PDF;
- Batch result must not automatically create PDFs for all rows;
- PDF must not be called a KURGIN certificate;
- PDF download link must be backend-controlled;
- public UI must not generate or expose raw PDF storage paths.

PDF / report storage requires separate storage and privacy review before implementation.

## 10. Verify Statuses

Potential Verify statuses:

- `valid`;
- `revoked`;
- `under_review`;
- `not_found`;
- `expired_if_applicable`.

Status meanings:

- `valid` means the report exists and is available for verification;
- `revoked` means an admin has revoked public verification for the report;
- `under_review` means the report exists but is temporarily limited;
- `not_found` means no public Verify record exists for the submitted code;
- `expired_if_applicable` may be used if future reports have validity periods.

## 11. User History vs Verify Base

A user may later hide a result from personal Profile history.

Rules:

- hiding / removing a result from Profile does not delete the Verify / base record;
- hiding / removing a result from Profile does not invalidate the issued KURGIN Analyzer Report Number;
- only an admin can revoke or delete a Verify / base record;
- future UI should use wording like `Скрыть из моей истории`;
- future UI should not use hard wording like `Удалить навсегда` unless real hard delete is implemented and reviewed.

Profile history and KURGIN Verify are different surfaces.

Profile history is personal user history.

KURGIN Verify is a public authenticity base for issued reports.

## 12. Batch Result

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

## 13. Input Reference

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

These may only be stored after a separate storage, privacy, and data-retention review.

## 14. Uploaded Files / OCR

Future photo / upload modes:

- Фото means a user photographs a laboratory document to recognize data for one-stone analysis;
- Загрузка means a user uploads a laboratory document file to recognize data for one-stone analysis.

Rules:

- temporary processing only at first;
- no permanent storage of uploaded files until privacy / storage policy exists;
- OCR raw text must not be exposed publicly;
- recognized parameters should be reviewed before analysis.

## 15. History Model

Future Profile history may show:

- date;
- type of analysis;
- result status;
- score_band;
- short summary;
- PDF / report download for Full one-stone analysis;
- available actions;
- entitlement / access status.

Profile history may include:

- paid Score Only result;
- paid Full one-stone analysis;
- admin-granted / free-granted result;
- Mass Analyzer result summary and result Excel later.

History must not show:

- formula internals;
- raw diagnostics;
- hidden penalty data;
- payment card data;
- internal admin notes.

History is not implemented in the current MVP.

## 16. Workspace History

Future Workspace may later show:

- professional / team history;
- company / partner batch results;
- Mass Analyzer result summaries;
- team limits;
- professional workflow states.

Workspace history is not implemented in the current MVP.

## 17. Data Retention

Planning rules:

- uploaded files require a separate retention policy;
- report numbers and analysis results require privacy review;
- PDF / report storage requires separate storage and privacy review;
- user should later have a way to request deletion;
- public UI must not be source of truth for stored results;
- storage must be backend-controlled;
- public UI must not generate or expose raw storage paths.

No storage or database changes are approved by this document.

## 18. Manager-Assisted Questions

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
- certification completed;
- purchase confirmed.

## 19. Relationship to Entitlement

Future results may reference `entitlement_id`.

Relationship rules:

- one-time Full one-stone entitlement becomes `used` after report / `result_ready`;
- 30-day access increments `used_count` through backend;
- Mass Analyzer usage counts rows or files through backend;
- Verify record may reference `result_id` and KURGIN Analyzer Report Number;
- public Verify must not expose `entitlement_id`;
- public UI must not update entitlement usage directly.

Entitlement usage changes must be handled by a future backend / access service.

## 20. Relationship to Commercial Model

Relationship rules:

- Score Only produces `one_stone_score_result`;
- Full One-Stone Analysis produces `one_stone_full_result`;
- PDF / report belongs to Full one-stone analysis;
- Batch access produces `batch_result` and `batch_row_result`;
- KURGIN Verify applies to issued Full one-stone analysis reports.

Related documents:

- `docs/ANALYZER_COMMERCIAL_ACCESS_MODEL_V0_1.md`;
- `docs/ANALYZER_ENTITLEMENT_MODEL_V0_1.md`.

## 21. Forbidden Claims / Actions

Analyzer result, history, and Verify layers must not claim or trigger:

- certificate;
- KURGIN certificate;
- official appraisal;
- price valuation;
- exact market price;
- investment rating;
- guaranteed resale;
- automatic purchase;
- automatic reserve;
- catalog publish;
- payment / order creation;
- price fixed.

Any claim near certification, pricing, investment quality, resale, catalog publication, payment, order, reserve, or fixed price requires separate review.

## 22. Future Implementation Order

Recommended future order:

1. Result / history / Verify model docs.
2. Privacy / data retention review.
3. Backend storage design.
4. Verify record design.
5. Profile / history UX design.
6. Entitlement integration.
7. Payment integration.
8. PDF / report generation after separate review.
9. KURGIN Verify UI after separate review.

Each stage requires separate approval.

## 23. Acceptance Criteria

This planning document is valid when:

- this document exists;
- this is docs-only;
- no code changes are made by this task;
- no UI changes are made by this task;
- no backend changes are made by this task;
- no storage / database changes are made by this task;
- no auth implementation is added;
- no payment implementation is added;
- no PDF implementation is added;
- no Verify UI implementation is added;
- no changes outside docs are required unless strictly necessary;
- the document covers result model;
- the document covers history model;
- the document covers KURGIN Verify model;
- the document covers KURGIN Analyzer Report Number;
- the document covers PDF download through Verify as future planning.

## 24. Status

Status: planning lock only.

Version: V0.1
