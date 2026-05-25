def render_cart_page() -> str:
    return """
<div class="pageBody">
  <div class="placeholder empty-state">
    <div class="empty-title">Корзина пока пуста</div>
    <div class="muted">Добавляйте камни из каталога, чтобы позже проверить доступность, запросить резерв или перейти к оформлению.</div>
    <button class="btn light" type="button" data-nav-page="catalog">Перейти в каталог</button>
  </div>

  <div class="placeholder empty-state-info">
    <div class="empty-title">Что будет здесь</div>
    <div class="muted">Позже появятся выбранные камни, количество, предварительная сумма, статус доступности, резерв и оформление заявки.</div>
  </div>
</div>
"""
