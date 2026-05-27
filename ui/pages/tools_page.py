def render_tools_page() -> str:
    return """
<div class="tools-page">
  <div class="tools-intro">Раздел «Инструменты» собирает аналитические и сервисные сценарии KURGIN. KURGIN Score здесь не отдельный инструмент: это коэффициент 0–100 внутри результата KURGIN Analyzer.</div>

  <div class="tools-tabs" role="tablist" aria-label="Инструменты KURGIN">
    <button type="button" class="tools-tab" role="tab" data-tool-tab="single_stone_analyzer" aria-selected="true">Анализ одного камня</button>
    <button type="button" class="tools-tab" role="tab" data-tool-tab="kurgin_index" aria-selected="false">KURGIN Index</button>
    <button type="button" class="tools-tab" role="tab" data-tool-tab="database_analysis" aria-selected="false">Анализ по базе</button>
    <button type="button" class="tools-tab" role="tab" data-tool-tab="excel_analyzer" aria-selected="false">Excel Analyzer</button>
    <button type="button" class="tools-tab" role="tab" data-tool-tab="kurgin_academy" aria-selected="false">KURGIN Academy</button>
  </div>

  <div class="tools-tab-content" data-tool-panel="single_stone_analyzer">
    <section class="tool-card"><div class="tool-kicker">Analyzer</div><div class="tool-title">KURGIN Analyzer</div><div class="tool-text">Полный анализ одного лабораторного бриллианта: KURGIN Score 0–100, теги, риски, сильные стороны, интерпретации и подробный анализ.</div><div class="tool-meta"><span class="tool-pill">один камень</span><span class="tool-pill">quality analysis</span><span class="tool-pill">KURGIN Score внутри</span></div><div class="tool-note">Не оценка цены, не сертификат, не инвестиционная рекомендация.</div></section>
  </div>

  <div class="tools-tab-content" data-tool-panel="kurgin_index" hidden>
    <section class="tool-card"><div class="tool-kicker">Index</div><div class="tool-title">KURGIN Index</div><div class="tool-text">Рыночный ориентир / market benchmark для сопоставимости лабораторных бриллиантов. Позже подключим параметры и дату обновления.</div><div class="tool-meta"><span class="tool-pill">benchmark</span><span class="tool-pill">без прогноза</span></div><div class="tool-note">Не финансовый индекс и не точная цена конкретного камня.</div></section>
  </div>

  <div class="tools-tab-content" data-tool-panel="database_analysis" hidden>
    <section class="tool-card"><div class="tool-kicker">Database</div><div class="tool-title">Анализ по базе</div><div class="tool-text">Manager-assisted сценарии для анализа базы, похожих вариантов, bulk-запросов и задач специалиста.</div><div class="tool-meta"><span class="tool-pill">база</span><span class="tool-pill">bulk</span><span class="tool-pill">специалисты</span></div><div class="tool-note">Не публичный каталог и не гарантия наличия.</div></section>
  </div>

  <div class="tools-tab-content" data-tool-panel="excel_analyzer" hidden>
    <section class="tool-card"><div class="tool-kicker">Excel</div><div class="tool-title">Excel Analyzer</div><div class="tool-text">Сценарий анализа Excel-файла для пакетной обработки данных. Логика Excel Analyzer не изменялась.</div><div class="tool-meta"><span class="tool-pill">Excel</span><span class="tool-pill">batch</span></div><div class="tool-note">Preview-структура. Не публикация, не checkout и не изменение каталога.</div></section>
  </div>

  <div class="tools-tab-content" data-tool-panel="kurgin_academy" hidden>
    <section class="tool-card"><div class="tool-kicker">Academy</div><div class="tool-title">KURGIN Academy</div><div class="tool-text">Образовательный раздел KURGIN: базовые материалы о лабораторных бриллиантах, параметрах, анализе и интерпретации результатов.</div><div class="tool-meta"><span class="tool-pill">education</span><span class="tool-pill">guide</span></div><div class="tool-note">UX-скелет. Не публичная статья, не сертификат и не инвестиционная рекомендация.</div></section>
  </div>
</div>

<script>
(function(){
  const root = document.currentScript.closest('.tools-page') || document.querySelector('.tools-page');
  if(!root) return;

  const defaultTool = 'single_stone_analyzer';
  let activeTool = defaultTool;
  const tabs = Array.from(root.querySelectorAll('[data-tool-tab]'));
  const panels = Array.from(root.querySelectorAll('[data-tool-panel]'));

  function setActiveTool(toolId){
    activeTool = toolId || defaultTool;
    tabs.forEach(tab => {
      const selected = tab.getAttribute('data-tool-tab') === activeTool;
      tab.setAttribute('aria-selected', selected ? 'true' : 'false');
    });
    panels.forEach(panel => {
      const selected = panel.getAttribute('data-tool-panel') === activeTool;
      panel.hidden = !selected;
    });
  }

  tabs.forEach(tab => {
    tab.addEventListener('click', function(){
      setActiveTool(tab.getAttribute('data-tool-tab'));
    });
  });

  setActiveTool(defaultTool);
})();
</script>
"""
