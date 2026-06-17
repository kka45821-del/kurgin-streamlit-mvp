# Public Stones V1 Site Integration

Status: SITE-1 read-only integration foundation.

## Purpose

The public site should be able to consume the Admin-generated export file:

```text
public_stones_v1.csv
```

The file is expected to live in:

```text
kurgin-data/public_stones_v1.csv
```

## Source of truth for SITE-1

The public site is a display layer. It does not decide which stones are public.

The public eligibility decision remains in KURGIN Admin:

```text
Admin public layer audit
→ public_stones_v1.csv
→ kurgin-data
→ public site display
```

## Loader behavior

The site attempts remote public data in this order:

```text
1. KURGIN_DATA_CATALOG_URL environment override, if set
2. kurgin-data/public_stones_v1.csv
3. legacy JSON URLs
4. legacy kurgin-data/stones.csv
5. local fallback stones
```

If `public_stones_v1.csv` does not exist or contains only headers, the site continues trying fallback sources.

## Public-safe price behavior

The site does not calculate prices.

For numeric rows:

```text
price_display_type = numeric
public_price_display = prepared numeric display
```

The loader maps the prepared public display into the existing mobile catalog price keys.

For request-price rows:

```text
price_display_type = price_on_request
public_price_display = Цена по запросу
```

The card remains a request-price card.

## Forbidden in SITE-1

```text
write to kurgin-data
sync with Admin
read stones_master.csv directly
calculate prices
show supplier/internal/start/working prices
show margins
show price_source / admin price metadata
create orders / reserves / payments
create PDF / assets
replace legacy stones.csv silently
```

## Future stages

```text
SITE-2 — refine public card detail view for public_stones_v1 fields
DATA-1 — manual dry-run of public_stones_v1.csv in kurgin-data
V2 — Timeweb database source of truth
```
