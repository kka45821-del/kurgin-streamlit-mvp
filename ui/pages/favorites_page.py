def render_favorites_page() -> str:
    return """
<div class="pageBody">
  <div class="placeholder empty-state">
    <div class="empty-title">Избранное пока пусто</div>
    <div class="muted">Сохраняйте интересные камни из каталога, чтобы вернуться к ним позже. Избранное хранится только в этом браузере.</div>
    <button class="btn light" type="button" data-nav-page="catalog">Перейти в каталог</button>
  </div>

  <div class="placeholder empty-state-info">
    <div class="empty-title">Важно</div>
    <div class="muted">Избранное не резервирует камни, не фиксирует цену, не создаёт заказ и не подтверждает наличие. Перед любым решением условия нужно уточнить отдельно.</div>
  </div>
</div>
"""
