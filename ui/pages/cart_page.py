def render_cart_page() -> str:
    return """
<div class="pageBody">
  <div class="placeholder empty-state">
    <div class="empty-title">Заявки / корзина пока не активны</div>
    <div class="muted">Этот раздел подготовлен для будущего сценария заявок. Онлайн-checkout сейчас не включён.</div>
    <button class="btn light" type="button" data-nav-page="catalog">Перейти в каталог</button>
  </div>

  <div class="placeholder empty-state-info">
    <div class="empty-title">Важно</div>
    <div class="muted">Добавление в будущую корзину не будет означать оплату, резерв или фиксацию цены без отдельного подтверждения.</div>
  </div>
</div>
"""
