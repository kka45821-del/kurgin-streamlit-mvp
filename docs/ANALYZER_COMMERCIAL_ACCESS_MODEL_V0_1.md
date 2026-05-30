# KURGIN Analyzer Commercial Access Model V0.1

## 1. Purpose

This document describes the future commercial access model for KURGIN Analyzer.

It does not approve implementation in the current MVP.

It separates future commercial access from the current public-safe Tools skeleton.

Current Tools Analyzer remains a public-safe preview / skeleton layer until separate implementation review.

## 2. Commercial Access Modes

Future commercial access may include:

1. Free / admin-granted access.
2. One-time paid one-stone analysis.
3. 30-day paid access.

These modes are planning concepts only. They do not create live payment, entitlement, profile, role, or report logic in the current MVP.

## 3. Free / Admin-Granted Access

Free / admin-granted access means access is issued by an administrator.

It may be granted to any user.

It may be limited by:

- time period;
- usage limit;
- analysis level;
- analysis type.

Admin-granted access does not mean that Analyzer is publicly free for all users.

## 4. One-Time Paid Analysis

One-time paid analysis may be available to any user.

It should not be rigidly tied to a professional role.

Future one-time paid analysis may have two levels:

### A. KURGIN Score Only

A fast one-stone result.

Public-safe output may include:

- status;
- score / score_band;
- short summary;
- warnings;
- limitations;
- next_action.

KURGIN Score Only must not expose formula internals.

It is not a certificate.

It is not a price valuation.

### B. Full One-Stone Analysis

A more detailed one-stone analysis result.

It may include an automatic expanded result plus the ability to ask a manager a question.

Potential content may include:

- KURGIN Score;
- score band;
- summary;
- geometry interpretation;
- risk flags;
- strengths;
- warnings;
- limitations;
- manager-assisted next action.

A PDF / report may later become an output of Full one-stone analysis.

PDF / report is not included in the current MVP.

## 5. 30-Day Paid Access

30-day paid access may be available to any user.

It must not be called unlimited.

It should use fair-use limits.

Initial constraints:

- no auto-renewal initially;
- no saved card initially;
- no recurring payment initially.

30-day access may later include:

- one-stone Analyzer;
- Mass Analyzer;
- other limited Analyzer capabilities.

Exact limits must be defined separately before implementation.

## 6. Mass Analyzer Commercial Boundary

Mass Analyzer may later be available through:

- admin-granted access;
- 30-day paid access;
- future commercial package.

Mass Analyzer must not automatically publish catalog data.

Mass Analyzer must not create orders, reserves, or payments.

Mass Analyzer must not issue certificates.

Mass Analyzer must not expose formula internals.

Batch output must remain public-safe unless a separate internal/professional surface is approved.

## 7. Entitlement Concept

A future entitlement entity may be named `AnalyzerEntitlement`.

Potential fields:

- `user_id`;
- `access_type`;
- `level`;
- `valid_from`;
- `valid_until`;
- `monthly_limit`;
- `used_count`;
- `fair_use_limit`;
- `one_stone_score_enabled`;
- `one_stone_full_enabled`;
- `batch_enabled`;
- `created_by_admin`;
- `revoked_at`;
- `status`.

Potential statuses:

- `active`;
- `expired`;
- `revoked`;
- `pending_payment`;
- `payment_failed`;
- `used`.

This entity is a planning concept only. It is not implemented in the current MVP.

## 8. Payment States

### One-Time Paid Analysis

Potential payment / processing states:

```text
submitted → validation → eligible_for_payment → payment_pending → payment_success → analysis_processing → result_ready
```

### 30-Day Access

Potential 30-day access states:

```text
payment_pending → payment_success → entitlement_active → expires_after_30_days
```

These states are not implemented in the current MVP.

They require payment provider review, legal review, user account design, and entitlement design before implementation.

## 9. Forbidden Commercial Claims

Analyzer commercial copy must not claim or imply:

- сертификат KURGIN;
- оценка стоимости;
- рыночная стоимость;
- точная цена;
- инвестиционный рейтинг;
- гарантия ликвидности;
- гарантия перепродажи;
- официальная оценка;
- автоматическая покупка;
- автоматический резерв;
- цена зафиксирована.

Any claim near certification, pricing, investment quality, liquidity, resale, or official appraisal requires separate legal and product review.

## 10. Current MVP Status

Current Tools Analyzer remains a skeleton / public preview.

Current MVP has:

- no payment UI;
- no paid access logic;
- no auth / profile / history;
- no PDF / report;
- no production commercial launch.

Current MVP must remain public-safe until a separate commercial implementation is approved.

## 11. Future Implementation Order

Recommended future order:

1. Commercial model docs.
2. Entitlement model docs.
3. Payment provider / legal review.
4. Auth / profile / history design.
5. One-time paid one-stone analysis.
6. 30-day access without auto-renewal.
7. PDF / report after separate review.

Each stage should be reviewed separately.

## 12. Non-Implementation Lock

This document does not authorize:

- payment implementation;
- checkout implementation;
- subscription UI;
- auth / profile / role implementation;
- PDF / report UI;
- live Analyzer backend integration;
- Formula Service integration;
- production commercial launch.

## 13. Acceptance Criteria

This planning document is valid when:

- this document exists;
- no code changes are made by this task;
- no UI changes are made by this task;
- no backend changes are made by this task;
- no payment implementation is added;
- no auth implementation is added.

## 14. Status

Status: planning lock only.

Version: V0.1
