def render_tools_page() -> str:
    tab_click = "const root=this.closest('.tools-page');const active=this.getAttribute('data-tool-tab');const title=this.getAttribute('data-tool-title');const subtitle=this.getAttribute('data-tool-subtitle');root.querySelectorAll('[data-tool-tab]').forEach(t=>t.setAttribute('aria-selected','false'));this.setAttribute('aria-selected','true');const intro=root.querySelector('[data-tools-intro]');if(intro)intro.hidden=true;root.querySelectorAll('[data-tool-panel]').forEach(p=>p.hidden=p.getAttribute('data-tool-panel')!==active);const headerTitle=document.querySelector('.brand-title');const headerSub=document.querySelector('.brand-sub');if(headerTitle&&title)headerTitle.textContent=title;if(headerSub&&subtitle)headerSub.textContent=subtitle;"
    mode_click = "const root=this.closest('.single-tool');const active=this.getAttribute('data-mode');root.querySelectorAll('[data-mode]').forEach(t=>t.setAttribute('aria-selected','false'));this.setAttribute('aria-selected','true');root.querySelectorAll('[data-mode-panel]').forEach(p=>p.hidden=p.getAttribute('data-mode-panel')!==active);"
    return f"""
<div class="tools-page">
  <div class="tools-tabs" role="tablist" aria-label="Инструменты KURGIN">
    <button type="button" class="tools-tab" role="tab" data-tool-tab="single_stone_analyzer" data-tool-title="KURGIN Analyzer One" data-tool-subtitle="анализ одного камня" aria-selected="false" onclick="{tab_click}">Анализ</button>
    <button type="button" class="tools-tab" role="tab" data-tool-tab="kurgin_index" data-tool-title="KURGIN Index" data-tool-subtitle="рыночный ориентир" aria-selected="false" onclick="{tab_click}">Индекс</button>
    <button type="button" class="tools-tab" role="tab" data-tool-tab="database_analysis" data-tool-title="KURGIN Verify" data-tool-subtitle="проверка данных" aria-selected="false" onclick="{tab_click}">Проверить</button>
    <button type="button" class="tools-tab" role="tab" data-tool-tab="excel_analyzer" data-tool-title="KURGIN Analyzer Excel" data-tool-subtitle="массовый анализ" aria-selected="false" onclick="{tab_click}">Массовый</button>
    <button type="button" class="tools-tab" role="tab" data-tool-tab="kurgin_academy" data-tool-title="KURGIN Academy" data-tool-subtitle="обучение и база знаний" aria-selected="false" onclick="{tab_click}">Обучение</button>
  </div>

  <div class="tools-intro" data-tools-intro>
    <div>Выберите инструмент: анализ одного камня, индекс, проверка данных, массовый анализ или обучение.</div>
    <div class="tools-description-list">
      <div><strong>Анализ</strong> — проверка одного камня по фото, файлу или ручному вводу.</div>
      <div><strong>Индекс</strong> — ориентир рынка для сравнения лабораторных бриллиантов.</div>
      <div><strong>Проверить</strong> — базовая проверка данных перед анализом или подбором.</div>
      <div><strong>Массовый</strong> — пакетная обработка списка камней через Excel.</div>
      <div><strong>Обучение</strong> — материалы KURGIN Academy для понимания параметров.</div>
    </div>
  </div>

  <div class="tools-tab-content" data-tool-panel="single_stone_analyzer" hidden>
    <div class="single-tool">
      <div class="tool-section-title">Анализ одного камня</div>
      <div class="single-mode-tabs" role="tablist" aria-label="Способ ввода">
        <button type="button" class="single-mode-tab" data-mode="photo" aria-selected="false" onclick="{mode_click}"><strong>Фото</strong><span>камера</span></button>
        <button type="button" class="single-mode-tab" data-mode="upload" aria-selected="true" onclick="{mode_click}"><strong>Загрузка</strong><span>файл</span></button>
        <button type="button" class="single-mode-tab" data-mode="manual" aria-selected="false" onclick="{mode_click}"><strong>Вручную</strong><span>форма</span></button>
      </div>

      <section class="single-workspace" data-mode-panel="upload">
        <div class="workspace-title">Рабочая зона: Загрузка</div>
        <div class="workspace-text">Загрузите PDF / JPG / PNG<br>документа или сертификата</div>
        <button type="button" class="single-file-button">[ выбрать файл ]</button>
      </section>

      <section class="single-workspace" data-mode-panel="photo" hidden>
        <div class="workspace-title">Рабочая зона: Фото</div>
        <div class="workspace-text">Сделайте фото документа или сертификата.</div>
        <button type="button" class="single-file-button">[ открыть камеру ]</button>
      </section>

      <section class="single-workspace" data-mode-panel="manual" hidden>
        <div class="workspace-title">Рабочая зона: Вручную</div>
        <div class="workspace-text">Введите параметры камня вручную.</div>
        <button type="button" class="single-file-button">[ открыть форму ]</button>
      </section>

      <section class="single-next-box">
        <div>Дальше: распознавание → проверка данных</div>
        <div>→ Karo Score → PDF-отчёт KURGIN Analyzer</div>
      </section>
    </div>
  </div>

  <div class="tools-tab-content" data-tool-panel="kurgin_index" hidden>
    <section class="tool-card"><div class="tool-kicker">Index</div><div class="tool-title">KURGIN Index</div><div class="tool-text">Рыночный ориентир / market benchmark для сопоставимости лабораторных бриллиантов. Позже подключим параметры и дату обновления.</div><div class="tool-meta"><span class="tool-pill">benchmark</span><span class="tool-pill">без прогноза</span></div><div class="tool-note">Не финансовый индекс и не точная цена конкретного камня.</div></section>
  </div>

  <div class="tools-tab-content" data-tool-panel="database_analysis" hidden>
    <section class="tool-card"><div class="tool-kicker">Verify</div><div class="tool-title">KURGIN Verify</div><div class="tool-text">Проверка данных и базовая верификация параметров перед анализом или подбором.</div><div class="tool-meta"><span class="tool-pill">проверка</span><span class="tool-pill">данные</span></div><div class="tool-note">UX-скелет. Не сертификат и не гарантия наличия.</div></section>
  </div>

  <div class="tools-tab-content" data-tool-panel="excel_analyzer" hidden>
    <section class="tool-card"><div class="tool-kicker">Excel</div><div class="tool-title">KURGIN Analyzer Excel</div><div class="tool-text">Сценарий анализа Excel-файла для пакетной обработки данных. Логика Excel Analyzer не изменялась.</div><div class="tool-meta"><span class="tool-pill">Excel</span><span class="tool-pill">batch</span></div><div class="tool-note">Preview-структура. Не публикация, не checkout и не изменение каталога.</div></section>
  </div>

  <div class="tools-tab-content" data-tool-panel="kurgin_academy" hidden>
    <section class="tool-card"><div class="tool-kicker">Academy</div><div class="tool-title">KURGIN Academy</div><div class="tool-text">Образовательный раздел KURGIN: базовые материалы о лабораторных бриллиантах, параметрах, анализе и интерпретации результатов.</div><div class="tool-meta"><span class="tool-pill">education</span><span class="tool-pill">guide</span></div><div class="tool-note">UX-скелет. Не публичная статья, не сертификат и не инвестиционная рекомендация.</div></section>
  </div>
</div>
"""
