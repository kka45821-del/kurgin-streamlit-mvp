# KURGIN Analyzer Entitlement Model V0.1

## 1. Purpose

This document describes the future access-rights model for KURGIN Analyzer.

The purpose is to:

- describe a future entitlement model for Analyzer access;
- separate user role from actual access rights;
- avoid implementing entitlement in the current MVP;
- prepare a future foundation for free / admin-granted access, one-time paid access, and 30-day access.

This document is planning only. It does not authorize implementation in the current MVP.

## 2. Core Principle

```text
role != entitlement
```

A user role is not the same as Analyzer access.

Principles:

- any user may potentially buy or receive access;
- a role must not automatically grant Analyzer access;
- access is granted through an entitlement;
- an entitlement may be granted by an administrator;
- an entitlement may be created after a one-time purchase;
- an entitlement may be created after a 30-day access purchase;
- an entitlement may be created as a manual exception.

Roles may help with UI context or workflow routing later, but roles must not bypass entitlement checks.

## 3. AnalyzerEntitlement Entity

A future access entity may be named `AnalyzerEntitlement`.

Potential fields:

- `entitlement_id`;
- `user_id`;
- `access_type`;
- `level`;
- `valid_from`;
- `valid_until`;
- `monthly_limit`;
- `fair_use_limit`;
- `used_count`;
- `one_stone_score_enabled`;
- `one_stone_full_enabled`;
- `batch_enabled`;
- `pdf_report_enabled`;
- `manager_question_enabled`;
- `created_by_admin`;
- `source`;
- `revoked_at`;
- `status`;
- `notes_internal`.

This entity is not implemented in the current MVP.

## 4. Access Type Values

Potential `access_type` values:

- `free_granted`;
- `one_time_paid`;
- `thirty_day_access`;
- `manual_exception`;
- `partner_access`;
- `test_access`.

These values describe how access was created. They do not directly describe the scope of what the user may do.

## 5. Level Values

Potential `level` values:

- `score_only`;
- `full_one_stone`;
- `batch`;
- `mixed_access`.

The level defines the scope of analysis access.

## 6. Status Values

Potential `status` values:

- `pending`;
- `active`;
- `expired`;
- `revoked`;
- `pending_payment`;
- `payment_failed`;
- `used`;
- `exhausted`.

Status controls whether the entitlement can be used.

## 7. Usage Tracking

Usage tracking rules:

- one-time access becomes `used` after the result is ready;
- 30-day access tracks `used_count`;
- batch access counts rows or files, not only sessions;
- fair-use limits must exist before public 30-day access;
- `used_count` must not be updated by public UI directly;
- usage tracking must happen through a future backend / access service.

The public UI must not be the source of truth for access usage.

## 8. Access Examples

Examples:

- private buyer buys one-time Score Only;
- jeweler buys Full One-Stone Analysis;
- company buys 30-day access;
- admin grants temporary test access;
- partner receives batch access by agreement.

These examples are not current MVP features.

## 9. What Entitlement Must Not Do

An entitlement must not:

- change the formula;
- publish catalog data;
- create payment by itself;
- create order or reserve;
- expose formula internals;
- bypass the public-safe adapter;
- imply certification;
- imply price valuation;
- imply investment rating;
- imply guaranteed resale.

Entitlement is an access-control concept only.

## 10. Future Integration Points

Future integration points may include:

- Profile / history;
- payment provider;
- Admin access management;
- Analyzer result storage;
- Mass Analyzer limits;
- PDF / report access;
- manager-assisted questions;
- audit log;
- revoke / expire flow.

Each integration point requires separate design and implementation review.

## 11. Current MVP Lock

Current MVP status:

- no entitlement implementation now;
- no user access checks in UI now;
- no payment UI now;
- no auth / profile now;
- no storage / database changes now;
- this is planning only.

The current Analyzer skeleton and mock flows must remain public-safe.

## 12. Relationship to Commercial Model

Related document:

- `docs/ANALYZER_COMMERCIAL_ACCESS_MODEL_V0_1.md`

Relationship:

- commercial access model describes future products;
- entitlement model describes future access rights and limits;
- entitlement is the future permission layer behind commercial access;
- commercial product selection must not directly bypass entitlement checks.

## 13. Acceptance Criteria

This planning document is valid when:

- this document exists;
- this is docs-only;
- no code changes are made by this task;
- no UI changes are made by this task;
- no backend changes are made by this task;
- no auth implementation is added;
- no payment implementation is added;
- no changes outside docs are required unless strictly necessary.

## 14. Status

Status: planning lock only.

Version: V0.1
