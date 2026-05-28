def render_cart_page() -> str:
    return """
<div class="pageBody">
  <div class="placeholder empty-state">
    <div class="empty-title">Заявки / будущая корзина</div>
    <div class="muted">В текущем public MVP онлайн-checkout не активен. Этот раздел подготовлен только как будущая зона заявок и проверки условий.</div>
    <button class="btn light" type="button" data-nav-page="catalog">Вернуться в каталог</button>
  </div>

  <div class="placeholder empty-state-info">
    <div class="empty-title">Важно</div>
    <div class="muted">Переход в этот раздел, добавление интереса или отправка запроса не являются заказом, оплатой, резервом, фиксацией цены или подтверждением наличия камня.</div>
  </div>
</div>
"""
