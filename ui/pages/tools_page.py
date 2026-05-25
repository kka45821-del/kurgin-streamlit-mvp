def render_tools_page() -> str:
    return """
<div class="tools-page">
  <div class="tools-intro">Раздел «Инструменты» собирает аналитические и сервисные сценарии KURGIN. KURGIN Score здесь не отдельный инструмент: это коэффициент 0–100 внутри результата KURGIN Analyzer.</div>
  <div class="tool-grid">
    <section class="tool-card"><div class="tool-kicker">Analyzer</div><div class="tool-title">KURGIN Analyzer</div><div class="tool-text">Полный анализ одного лабораторного бриллианта: KURGIN Score 0–100, теги, риски, сильные стороны, интерпретации и подробный анализ.</div><div class="tool-meta"><span class="tool-pill">один камень</span><span class="tool-pill">quality analysis</span><span class="tool-pill">KURGIN Score внутри</span></div><div class="tool-note">Не оценка цены, не сертификат, не инвестиционная рекомендация.</div></section>
    <section class="tool-card"><div class="tool-kicker">Index</div><div class="tool-title">KURGIN Index</div><div class="tool-text">Рыночный ориентир / market benchmark для сопоставимости лабораторных бриллиантов. Позже подключим параметры и дату обновления.</div><div class="tool-meta"><span class="tool-pill">benchmark</span><span class="tool-pill">без прогноза</span></div><div class="tool-note">Не финансовый индекс и не точная цена конкретного камня.</div></section>
    <section class="tool-card"><div class="tool-kicker">Request</div><div class="tool-title">Подбор и matching</div><div class="tool-text">Manager-assisted сценарии для подбора одного камня, похожих вариантов, bulk-запросов и задач специалиста.</div><div class="tool-meta"><span class="tool-pill">подбор</span><span class="tool-pill">bulk</span><span class="tool-pill">специалисты</span></div><div class="tool-note">Не публичный каталог и не гарантия наличия.</div></section>
  </div>
</div>
"""
