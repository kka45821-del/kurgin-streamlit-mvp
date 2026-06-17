# kurgin-streamlit-mvp

Mobile-first MVP for KURGIN website and Streamlit functionality.

## SITE-1 — public_stones_v1 catalog input

The public MVP site can now read the Admin-generated public export contract:

```text
kurgin-data/public_stones_v1.csv
```

The catalog loader uses `public_stones_v1.csv` as the first preferred public data source.

Loader rules:

```text
- if public_stones_v1.csv contains public rows, the site renders those rows;
- if public_stones_v1.csv exists but contains no public rows, the public catalog is empty;
- legacy JSON fallback is used only when public_stones_v1.csv is unavailable;
- legacy stones.csv is not used as a public fallback source.
```

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
