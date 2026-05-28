# PUBLIC MVP Smoke Checkpoint v0.1

Date: 2026-05-28
Repo: `kka45821-del/kurgin-streamlit-mvp`
Scope: public Streamlit MVP only.

This checkpoint fixes the current expected public MVP state after stabilization work on KURGIN Index, catalog request flow, favorites, catalog filters/sort, and inactive feature states.

## 1. Current public MVP status

The public MVP is a storefront / public showcase for KURGIN. It is not a checkout product, not a payment product, not an order-management product, and not an authenticated professional cabinet.

The current public MVP should allow a user to:

- open the public app;
- browse the public catalog;
- switch catalog sections;
- filter and sort catalog cards;
- open a stone detail card;
- request conditions through the safe request block;
- save stones to browser-local favorites;
- open saved stones from Favorites;
- use the basic KURGIN Index interactions;
- understand that inactive Tools/Profile/Cart areas are not live product functions yet.

## 2. Working public MVP surfaces

### Catalog

Expected working state:

- Catalog renders.
- Catalog sections are available.
- Catalog cards render.
- Catalog cards open the detail card.
- Request icon opens the detail/request path.
- Info icon opens the detail card.
- Favorite icon toggles saved state.
- Disabled actions do not represent active checkout, reserve, payment, order, sold or share logic.

### Catalog filters

Expected working state:

- Filter panel opens.
- Filter chips toggle.
- Supported groups:
  - shape;
  - weight;
  - color;
  - clarity;
  - score;
  - fluorescence;
  - finish.
- Empty state is understandable: `По выбранным фильтрам камни не найдены`.
- Empty state includes a reset filters action.
- Reset filters works from the filter header and from empty state.

### Catalog sort

Expected working state:

- Sort panel opens.
- Sort options work for:
  - price ascending / descending;
  - carat ascending / descending;
  - score ascending / descending;
  - diameter ascending / descending;
  - new.
- Missing numeric values should not break rendering or sorting.

### Stone detail card

Expected working state:

- Detail card opens from catalog card.
- Detail card opens from Favorites.
- Detail card shows understandable public fields:
  - shape / carat;
  - color;
  - clarity;
  - KURGIN Score;
  - diameter;
  - fluorescence;
  - finish;
  - document / report number, if present.
- Main CTA is safe: request conditions / request price language.
- No active cart / checkout / payment / reserve path is exposed.

### Request block

Expected working state:

- Request block is visible in the detail card.
- Request block uses safe language: request is not an order, not a reserve, not a payment, and not a price lock.
- Contact channels are present when configured:
  - MAX;
  - Telegram;
  - WhatsApp.

### Favorites

Expected working state:

- User can add a catalog stone to Favorites.
- Repeated favorite action can remove / toggle saved state.
- Bottom navigation badge updates.
- Favorites page shows saved stones.
- Saved stone card shows:
  - shape;
  - carat;
  - color;
  - clarity;
  - KURGIN Score;
  - price or `по запросу`.
- `Открыть карточку` opens the detail card when the stone still exists in the current catalog.
- `Удалить` removes the saved stone.
- If a saved stone is no longer present in the current catalog, the UI shows: `Камень больше не доступен в текущем каталоге`.
- Favorites are browser-local only and do not reserve, lock price, create an order, or confirm availability.

### KURGIN Index

Expected working state:

- KURGIN Index basic table is visible.
- Score selector works.
- View panel / bottom sheet opens.
- View panel close handle works.
- D / E / F / G filters work.
- Clarity filters work.
- Carat range filters work.
- One / two / all carat range cases should not stretch columns incorrectly.
- Show all / reset view works.
- Horizontal table scroll remains available when needed.

### Tools

Expected working state:

- KURGIN Index is the active basic tool.
- Other tools are shown as inactive / skeleton / future MVP surfaces:
  - KURGIN Stone Analyzer;
  - KURGIN Verify;
  - KURGIN Mass Analyzer;
  - KURGIN Academy.
- Inactive tools must not look like working upload, camera, calculation, verification, report or analysis engines.

### Profile

Expected working state:

- Profile opens.
- Profile clearly states login / registration / roles are unavailable in the current public MVP.
- No active auth backend is implied.
- No professional cabinet is active.

### Cart / Requests

Expected working state:

- Cart / Requests page opens.
- Page clearly states checkout is inactive.
- Page language must remain safe: no order, no payment, no reserve, no price lock.

## 3. Explicitly inactive / not active in this public MVP

The following are not active public MVP functions:

- checkout;
- payment;
- order creation;
- reserve;
- sold logic;
- price lock;
- ownership transfer;
- auth / login / registration;
- professional cabinet;
- Analyzer engine;
- certificate generation;
- PDF generation;
- Share flow;
- admin operations;
- data publishing from public app;
- formula editing;
- pricing or scoring formula changes.

These items must remain inactive until they are intentionally designed, implemented, reviewed and released.

## 4. Manual smoke checklist

Use this checklist after every deploy touching public MVP shell, catalog, favorites, filters/sort, request flow or Index.

### Load and routing

- [ ] `/` opens without white screen.
- [ ] `?page=catalog` opens.
- [ ] `?page=tools` opens.
- [ ] `?page=tools&tool=kurgin_index` opens.
- [ ] `?page=favorites` opens.
- [ ] `?page=profile` opens.
- [ ] No traceback.
- [ ] No visible JS text.

### Bottom navigation

- [ ] KURGIN opens.
- [ ] Tools opens.
- [ ] Catalog opens.
- [ ] Favorites opens.
- [ ] Cart / Requests opens.
- [ ] Profile opens.

### Catalog

- [ ] Catalog cards render.
- [ ] Catalog sections switch.
- [ ] Card tap opens detail card.
- [ ] Info icon opens detail card.
- [ ] Request icon opens detail / request path.
- [ ] Disabled reserve/cart/share actions do not behave as active purchase actions.

### Filters

- [ ] Filter panel opens.
- [ ] Shape chips toggle.
- [ ] Weight chips toggle.
- [ ] Color chips toggle.
- [ ] Clarity chips toggle.
- [ ] Score chips toggle.
- [ ] Fluorescence chips toggle.
- [ ] Finish chips toggle.
- [ ] Empty state appears when no cards match.
- [ ] Empty state reset button works.
- [ ] Header reset button works.

### Sort

- [ ] Price ascending works.
- [ ] Price descending works.
- [ ] Carat ascending works.
- [ ] Carat descending works.
- [ ] Score ascending works.
- [ ] Score descending works.
- [ ] Diameter ascending works.
- [ ] Diameter descending works.
- [ ] New sort does not break card rendering.

### Detail and request

- [ ] Detail card opens from catalog.
- [ ] Detail card opens from Favorites.
- [ ] Detail card uses `Документ / report`, not risky certificate wording as an active claim.
- [ ] Request block is visible.
- [ ] MAX link is present or safely disabled if not configured.
- [ ] Telegram link is present or safely disabled if not configured.
- [ ] WhatsApp link is present or safely disabled if not configured.
- [ ] Request copy says request is not order / reserve / payment / price lock.

### Favorites

- [ ] Favorite icon adds a stone.
- [ ] Favorite icon toggles / removes saved state where applicable.
- [ ] Favorites badge updates.
- [ ] Favorites page shows saved stones.
- [ ] Saved stone card shows shape / carat / color / clarity / score / price or request state.
- [ ] `Открыть карточку` opens detail card.
- [ ] `Удалить` removes the saved stone.
- [ ] Empty Favorites state is understandable.

### KURGIN Index regression

- [ ] Index table is visible.
- [ ] Score selector works.
- [ ] View panel opens.
- [ ] View panel close handle works.
- [ ] D / E / F / G filters work.
- [ ] Clarity filters work.
- [ ] One carat range does not stretch columns.
- [ ] Two carat ranges do not stretch columns.
- [ ] All carat ranges render normally.
- [ ] Show all works.
- [ ] Reset view works.
- [ ] Horizontal scroll works when needed.

### Inactive surfaces

- [ ] Stone Analyzer is clearly inactive / skeleton.
- [ ] Verify is clearly inactive / skeleton.
- [ ] Mass Analyzer is clearly inactive / skeleton.
- [ ] Academy is clearly inactive / skeleton.
- [ ] Profile clearly says auth is unavailable.
- [ ] Cart / Requests clearly says checkout is inactive.

## 5. Release guardrails

Do not change these areas as part of public MVP smoke cleanup unless there is a separate approved task:

- data files;
- `catalog.json`;
- `public_index.json`;
- pricing formula;
- scoring formula;
- Analyzer engine;
- admin repo;
- data repo;
- checkout/payment/order/reserve/sold logic;
- auth/login;
- PDF/Share.

## 6. Checkpoint note

This document is a release checkpoint, not a feature specification. It records the current expected public MVP behavior and the smoke checklist required before treating a deploy as stable.
