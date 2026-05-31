# KURGIN PUBLICATION RULES CONTRACT v0.1

Repo: `kka45821-del/kurgin-streamlit-mvp`  
Scope: publication rules contract / stabilization boundary.  
Status: active contract lock.  

This document locks the public catalog publication semantics between the Admin repository and the public Streamlit repository.

It does not change data, Admin behavior, `kurgin-data`, Analyzer, formula, scoring, publication payload, payment, reserve, order, checkout or sold automation.

---

## 1. Problem

After Admin Product Management stabilization, a publication-logic risk exists:

```text
business / publication logic is partially duplicated
```

Current logic appears in several places:

- `kurgin-admin-mvp/admin_publication_rules.py`
- `kurgin-admin-mvp/admin_publish.py`
- `kurgin-streamlit-mvp/catalog/catalog_core.py`
- `kurgin-streamlit-mvp/ui/mobile_shell.py`

The risk is that Admin and public frontend may interpret the same stone differently.

Potential divergence areas:

- `public_visible`
- `public_sellable`
- `checkout_enabled`
- `public_action`
- request-price state
- `section`
- hidden states
- removed states
- unavailable states
- archived / removed-from-sale states

This is an architecture risk. Refactor must be phased and tested.

---

## 2. Source of truth

Locked principle:

```text
Admin decides.
Frontend displays.
```

The Admin publication layer is the primary source of truth for public catalog semantics.

Admin publication layer decides:

- `public_visible`
- `public_sellable`
- `checkout_enabled`
- `public_action`
- `section`
- public price state
- request-price vs sellable state
- visibility after `removed_from_sale`
- visibility after archived batch states
- whether a stone is included in published public catalog output

The public frontend must not become a second business-rule authority.

---

## 3. Public frontend responsibility

Public Streamlit responsibility:

- read published computed fields;
- display published computed fields;
- use fallback logic only when computed fields are absent;
- keep public UI consistent with Admin-published semantics;
- avoid independent business decisions when Admin-published fields exist.

Public Streamlit must not:

- override Admin-computed sellable state;
- override Admin-computed request-price state;
- override Admin-computed visibility state;
- independently turn non-sellable stones into sellable stones;
- independently turn request-price stones into checkout stones;
- create order states;
- create reserve states;
- create payment states;
- create sold states.

---

## 4. Required published fields contract

Published catalog output should contain these fields:

| Field | Contract role |
|---|---|
| `stone_id` | Stable public/admin stone identifier. |
| `section` | Final Admin-resolved public section. |
| `price_rub` | Base price field where present. |
| `public_price_rub` | Admin-computed public price if available. |
| `price_status` | Price state / fallback support. |
| `public_visible` | Admin-computed public visibility. |
| `public_sellable` | Admin-computed sellable state. |
| `checkout_enabled` | Admin-computed checkout eligibility flag. |
| `public_action` | Admin-computed public action. |
| `priceText` | Admin/public display price text where available. |
| `current_status` | Operational stone status. |
| `show_in_catalog` | Admin visibility input. |
| `is_mvp_eligible` | Admin MVP eligibility input. |

If a field is missing in legacy or transitional payloads, frontend may use fallback logic. Fallback must be treated as compatibility logic only, not the primary rule system.

---

## 5. Allowed `public_action` values

Allowed MVP values:

```text
request_price
checkout
```

MVP rules:

- even if `checkout_enabled = true`, public checkout UI may remain disabled;
- `request_price` must never create order, reserve, payment or sold state;
- favorite must never equal reserve;
- payment must never equal sold;
- checkout availability in payload does not approve client payment automation by itself.

---

## 6. Request-price rule

Primary interpretation:

```text
if public_action == request_price → frontend shows request-price
if checkout_enabled == false → frontend shows request-price
if public_sellable == false → frontend shows request-price
if price_rub <= 0 → frontend shows request-price
```

Frontend may use `price_status` fallback only if computed fields are missing.

Frontend must not override Admin-computed sellable state.

Examples:

| Admin-computed state | Frontend behavior |
|---|---|
| `public_action = request_price` | Show request-price. |
| `checkout_enabled = false` | Show request-price or non-checkout action. |
| `public_sellable = false` | Do not show as active checkout item. |
| `price_rub <= 0` and no computed public price | Show request-price. |
| Computed fields missing | Use compatibility fallback only. |

---

## 7. Section rule

Admin publish must resolve final `section`.

Frontend may:

- filter by `section`;
- display `section`;
- group by `section`.

Frontend must not:

- recalculate section business meaning;
- decide publish eligibility based on its own section matrix;
- turn section aliases into independent commercial rules;
- make hidden / archived / removed stones visible because of section fallback.

---

## 8. Removed / archived states

Admin-side `removed_from_sale` / archived status means after publish:

```text
not public visible
not sellable
not checkout enabled
```

The resulting public behavior should be one of:

```text
public_action = request_price
```

or:

```text
hidden / absent from published catalog
```

depending on the Admin publish rule.

Frontend must not show removed / archived stones as active if Admin-computed visibility says false.

Frontend must not revive removed / archived stones via fallback rules.

---

## 9. Current known duplication locations

### 9.1 `kurgin-admin-mvp/admin_publication_rules.py`

Known duplicated / related responsibilities:

- public masks;
- sellable masks;
- public preview;
- `public_action`.

### 9.2 `kurgin-admin-mvp/admin_publish.py`

Known duplicated / related responsibilities:

- payload creation;
- section normalization;
- `section_for_row`;
- computed field export.

### 9.3 `kurgin-streamlit-mvp/catalog/catalog_core.py`

Known duplicated / related responsibilities:

- hidden statuses;
- request-price statuses;
- section aliases;
- validation matrix;
- section resolving.

### 9.4 `kurgin-streamlit-mvp/ui/mobile_shell.py`

Known duplicated / related responsibilities:

- `isRequestPrice()`;
- `priceHtml()`;
- `displayPriceText()`.

These locations are documented to guide future stabilization. This contract does not remove them.

---

## 10. Implementation status v0.1

Status after stabilization pass:

- frontend request-price interpretation now prefers Admin-computed fields first;
- fallback remains only for missing legacy fields;
- contract smoke script added at `scripts/smoke_publication_rules_contract.py`;
- no checkout behavior was added;
- no payment behavior was added;
- no reserve behavior was added;
- no sold behavior was added;
- no `kurgin-data` changes were made;
- no Analyzer / formula / scoring changes were made.

Current implementation note:

```text
Public frontend must prefer public_action, checkout_enabled and public_sellable before legacy price_status fallback.
```

The MVP UI may still keep checkout disabled even when the data contract marks a stone as sellable.

---

## 11. Future implementation order

### Phase 1 — Contract lock

Create this document and keep it as the source contract.

Status:

```text
complete
```

### Phase 2 — Contract tests / smoke tests

Add tests comparing:

- Admin-published output;
- frontend assumptions;
- request-price behavior;
- hidden / removed / unavailable handling;
- section handling.

Status:

```text
initial smoke added
```

### Phase 3 — Frontend prefers Admin-computed fields

Change frontend request-price logic so it reads Admin-computed fields first:

- `public_visible`
- `public_sellable`
- `checkout_enabled`
- `public_action`
- `priceText`
- `section`

Fallback logic remains only for missing legacy fields.

Status:

```text
initial frontend preference added for request-price interpretation
```

### Phase 4 — Reduce duplicated frontend business rules

After tests pass, reduce duplicated frontend logic around:

- request-price decisions;
- hidden statuses;
- section business meaning;
- sellable / visible decisions.

Frontend should stay a display layer, not a business-rule layer.

Status:

```text
future
```

### Phase 5 — Optional shared pure module

Only if still needed, introduce a shared pure module such as:

```text
domain/publication_rules.py
```

This must be considered only after contract tests and field-preference stabilization.

Do not start with shared-module refactor.

Status:

```text
future / not started
```

---

## 12. Forbidden in this stabilization task

Do not:

- change `kurgin-data`;
- change Analyzer / formula / scoring;
- implement shared module;
- remove JS fallback;
- change publish payload;
- add payment logic;
- add reserve logic;
- add sold logic;
- make a large refactor;
- cleanup files;
- delete files.

---

## 13. Acceptance lock

This stabilization step is complete only if:

1. `scripts/smoke_publication_rules_contract.py` exists.
2. Frontend request-price interpretation prefers Admin-computed fields first.
3. Fallback remains only for missing legacy fields.
4. UI visual design is not changed.
5. Checkout / payment / reserve / sold behavior is not added.
6. This document includes `Implementation status v0.1`.
7. Admin remains the publication authority.
8. Frontend remains the display layer.

---

## 14. Final lock statement

This contract locks the publication semantic boundary:

```text
Admin publication layer computes public catalog meaning.
Public frontend displays published meaning.
Frontend fallback exists only for legacy / missing fields.
```

Any future implementation must preserve this boundary unless an explicit architecture decision supersedes it.
