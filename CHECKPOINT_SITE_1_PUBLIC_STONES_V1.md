# Checkpoint SITE-1 — public_stones_v1 catalog input

Stable input before this checkpoint:

```text
Admin Checkpoint 33 — Stage 8A manual publish package completed
Manual pilot passed with real public rows
```

What SITE-1 adds:

```text
- public site loader can read kurgin-data/public_stones_v1.csv;
- CSV rows are adapted to the existing mobile catalog display contract;
- public_price_display is used as prepared public price display;
- price_on_request rows remain request-price rows;
- legacy JSON / fallback behavior remains available.
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
- no hidden/admin price fields exposed.
```

Next recommended stage:

```text
DATA-1 — manually place a small public_stones_v1.csv dry-run file into kurgin-data and verify the public site renders real cards.
```
