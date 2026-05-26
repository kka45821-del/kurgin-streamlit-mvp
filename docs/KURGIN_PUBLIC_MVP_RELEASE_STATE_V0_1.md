# KURGIN Public MVP Release State v0.1

## 1. Что сейчас работает

Текущее состояние публичного MVP после публикации `catalog.json` и включения Request Flow v0.1:

- публичный каталог открывается;
- `catalog.json` читается из `kurgin-data`;
- карточки камней отображаются;
- `request_price` / no-price состояние показывается как **«по запросу»**;
- `0 ₽` не показывается;
- detail sheet открывается;
- detail sheet показывает **«Цена / по запросу»**;
- request-flow через **MAX / Telegram / WhatsApp** отображается;
- используется safe warning:

> Заявка не является заказом, резервом, оплатой или фиксацией цены.

- 6 кнопок карточки визуально сохранены;
- public CI smoke-check зелёный.

## 2. Что работает только визуально / stub

Следующие элементы сейчас являются визуальными или stub-слоями и не являются полноценной рабочей backend-функцией:

- избранное;
- корзина;
- резерв;
- share;
- профиль;
- регистрация;
- checkout;
- order flow;
- payment.

Эти элементы могут присутствовать в интерфейсе как часть MVP-скелета, но не должны трактоваться как production-функции.

## 3. Что request-flow НЕ означает

Request Flow v0.1 **не означает**:

- заказ;
- резерв;
- оплату;
- фиксацию цены;
- checkout;
- sold;
- ownership transfer;
- backend-заявку.

Переход в MAX / Telegram / WhatsApp — это только контактное действие пользователя.

## 4. Связь с админкой

Текущая схема связи:

```text
kurgin-admin-mvp
→ publication gate
→ kurgin-data/catalog.json
→ kurgin-streamlit-mvp
```

Фиксация правил:

- admin публикует `catalog.json` в `kurgin-data`;
- public site читает `catalog.json` из `kurgin-data`;
- public site не пишет обратно в admin;
- public site не меняет статус камня;
- public site не меняет цену;
- public site не публикует данные.

## 5. Что нельзя делать без отдельного утверждения

Без отдельного утверждения нельзя добавлять или включать:

- реальный checkout;
- оплату;
- настоящий reserve;
- `sold`;
- roles / registration;
- Analyzer integration;
- Index UI;
- backend requests;
- `requests.csv`;
- CRM / webhook.

Любой из этих слоёв требует отдельного scope, проверки последствий и controlled implementation.

## 6. Следующий возможный слой

Следующий слой нужно выбирать отдельно. Возможные направления:

1. **Request Flow v0.2 с backend-заявками**
   - `request_id`;
   - `request_type`;
   - `stone_id`;
   - `stone_snapshot`;
   - user contacts;
   - status lifecycle;
   - admin requests panel.

2. **Безопасное избранное**
   - local/session MVP;
   - без backend-аккаунта;
   - без обещания сохранения между устройствами.

3. **Безопасная корзина без checkout**
   - visual selection list;
   - без оплаты;
   - без резерва;
   - без price lock;
   - без sold.

Важно: не делать всё сразу.

## 7. Current release state

```text
Public MVP v0.1 = catalog + request-price display + visual/contact request-flow.
```

Текущая версия является публичной витриной и контактным слоем. Она не является полноценной e-commerce системой, CRM, payment system или backend request system.

## 8. Контрольное правило

```text
Catalog first. Contact intent second. Transaction later.
```

До отдельного утверждения KURGIN public MVP не должен превращать визуальный interest/request-flow в покупку, оплату, резерв, sold или фиксацию цены.
