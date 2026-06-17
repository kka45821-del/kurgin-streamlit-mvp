# Checkpoint SITE-1 — public_stones_v1 catalog input

Stable input before this checkpoint:

```text
Admin Checkpoint 33 — Stage 8A manual publish package completed
Manual pilot with real public rows is pending
```

What SITE-1 adds:

```text
- public site loader can read kurgin-data/public_stones_v1.csv;
- CSV rows are adapted to the existing mobile catalog display contract;
- only public_card_status values public_numeric_price / public_price_on_request are accepted from public_stones_v1.csv;
- public_price_display is used as prepared public price display;
- price_on_request rows remain request-price rows;
- if public_stones_v1.csv exists but has no public rows, the public catalog is empty and demo fallback is not used;
- legacy JSON fallback remains available only when public_stones_v1.csv is unavailable.
```

What SITE-1 does not do:

```text
- no writes to kurgin-data;
- no sync;
- no Admin changes;
- no DB;
- no PDF/assets;
- no orders/reserves/payments;
- no direct stones_master.csv read;
- no hidden/admin price fields exposed;
- no silent replacement of legacy stones.csv.
```

Next recommended stage:

```text
DATA-1 — manually place a small public_stones_v1.csv dry-run file into kurgin-data and verify the public site renders real cards.
```
