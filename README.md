# kurgin-streamlit-mvp

Mobile-first MVP for KURGIN website and Streamlit functionality.

## SITE-1 — public_stones_v1 catalog input

The public MVP site can now read the Admin-generated public export contract:

```text
kurgin-data/public_stones_v1.csv
```

The catalog loader still keeps the older remote JSON URLs and local fallback behavior, but `public_stones_v1.csv` is now the first preferred public data source.

SITE-1 is read-only:

```text
- does not write to kurgin-data;
- does not create sync;
- does not calculate prices;
- does not read stones_master.csv;
- does not expose admin/internal price fields;
- does not create orders, reserves, payments, PDF or assets.
```

The public site displays only public-safe fields prepared by KURGIN Admin, including `public_price_display` mapped into the existing mobile catalog price display.
