def render_favorites_page() -> str:
    return """
<div class="pageBody">
  <div class="placeholder empty-state">
    <div class="empty-title">Избранное пока пусто</div>
    <div class="muted">Сохраняйте интересные камни из каталога, чтобы позже быстро вернуться к сравнению, запросу подбора или оформлению.</div>
    <button class="btn light" type="button" data-nav-page="catalog">Перейти в каталог</button>
  </div>

  <div class="placeholder empty-state-info">
    <div class="empty-title">Что будет здесь</div>
    <div class="muted">Позже появятся сохранённые камни, сравнение параметров, быстрый переход в карточку камня и синхронизация с профилем после входа.</div>
  </div>
</div>
"""
