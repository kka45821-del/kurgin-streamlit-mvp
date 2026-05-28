from ui.index_components import render_public_index_tool
from ui.index_scripts import DEEP_LINK_INIT


def render_tools_page() -> str:
    tab_click = "const root=this.closest('.tools-page');const active=this.getAttribute('data-tool-tab');root.querySelectorAll('[data-tool-tab]').forEach(t=>t.setAttribute('aria-selected','false'));this.setAttribute('aria-selected','true');root.querySelectorAll('[data-tool-panel]').forEach(p=>p.hidden=p.getAttribute('data-tool-panel')!==active);try{const url=new URL(window.parent.location.href);url.searchParams.set('page','tools');url.searchParams.set('tool',active);window.parent.history.replaceState(null,'',url.toString());}catch(e){}"
    mode_click = "const root=this.closest('.single-tool');const active=this.getAttribute('data-mode');root.querySelectorAll('[data-mode]').forEach(t=>t.setAttribute('aria-selected','false'));this.setAttribute('aria-selected','true');root.querySelectorAll('[data-mode-panel]').forEach(p=>p.hidden=p.getAttribute('data-mode-panel')!==active);"
    public_index_tool = render_public_index_tool()
    return f"""
<div class="tools-page">
  <img src="x" alt="" hidden onerror="{DEEP_LINK_INIT}">
  <div class="tools-tabs" role="tablist" aria-label="Инструменты KURGIN">
    <button type="button" class="tools-tab" role="tab" data-tool-tab="single_stone_analyzer" aria-selected="true" onclick="{tab_click}">KURGIN<br>Stone Analyzer</button>
    <button type="button" class="tools-tab" role="tab" data-tool-tab="kurgin_index" aria-selected="false" onclick="{tab_click}">KURGIN<br>Index</button>
    <button type="button" class="tools-tab" role="tab" data-tool-tab="database_analysis" aria-selected="false" onclick="{tab_click}">KURGIN<br>Verify</button>
    <button type="button" class="tools-tab" role="tab" data-tool-tab="excel_analyzer" aria-selected="false" onclick="{tab_click}">KURGIN<br>Mass Analyzer</button>
    <button type="button" class="tools-tab" role="tab" data-tool-tab="kurgin_academy" aria-selected="false" onclick="{tab_click}">KURGIN<br>Academy</button>
  </div>

  <div class="tools-tab-content" data-tool-panel="single_stone_analyzer">
    <div class="single-tool">
      <div class="tool-section-title">KURGIN Stone Analyzer</div>
      <div class="muted">Анализ одного камня по фото, файлу или ручному вводу. Сейчас это UX-скелет без запуска расчёта.</div>
      <div class="single-mode-tabs" role="tablist" aria-label="Способ ввода">
        <button type="button" class="single-mode-tab" data-mode="photo" aria-selected="false" onclick="{mode_click}"><strong>Фото</strong><span>камера</span></button>
        <button type="button" class="single-mode-tab" data-mode="upload" aria-selected="true" onclick="{mode_click}"><strong>Загрузка</strong><span>файл</span></button>
        <button type="button" class="single-mode-tab" data-mode="manual" aria-selected="false" onclick="{mode_click}"><strong>Вручную</strong><span>форма</span></button>
      </div>

      <section class="single-workspace" data-mode-panel="upload">
        <div class="workspace-title">Рабочая зона: Загрузка</div>
        <div class="workspace-text">PDF / JPG / PNG документа или сертификата.</div>
        <button type="button" class="single-file-button">[ выбрать файл ]</button>
      </section>

      <section class="single-workspace" data-mode-panel="photo" hidden>
        <div class="workspace-title">Рабочая зона: Фото</div>
        <div class="workspace-text">Фото документа или сертификата.</div>
        <button type="button" class="single-file-button">[ открыть камеру ]</button>
      </section>

      <section class="single-workspace" data-mode-panel="manual" hidden>
        <div class="workspace-title">Рабочая зона: Вручную</div>
        <div class="workspace-text">Ручной ввод параметров камня.</div>
        <button type="button" class="single-file-button">[ открыть форму ]</button>
      </section>

      <section class="single-next-box">
        <div>Дальше: распознавание → проверка данных</div>
        <div>→ KURGIN Score → отчёт KURGIN Analyzer</div>
      </section>
    </div>
  </div>

  <div class="tools-tab-content" data-tool-panel="kurgin_index" hidden>
    {public_index_tool}
  </div>

  <div class="tools-tab-content" data-tool-panel="database_analysis" hidden>
    <section class="tool-card"><div class="tool-kicker">Verify</div><div class="tool-title">KURGIN Verify</div><div class="tool-text">Проверка, сверка и базовый анализ данных по камню или базе перед подбором.</div><div class="tool-note">UX-скелет. Не сертификат и не гарантия наличия.</div></section>
  </div>

  <div class="tools-tab-content" data-tool-panel="excel_analyzer" hidden>
    <section class="tool-card"><div class="tool-kicker">Mass Analyzer</div><div class="tool-title">KURGIN Mass Analyzer</div><div class="tool-text">Excel / batch / массовый анализ списка камней. Реальная логика Excel Analyzer не подключена в этом public-скелете.</div><div class="tool-note">Не публикация, не checkout и не изменение каталога.</div></section>
  </div>

  <div class="tools-tab-content" data-tool-panel="kurgin_academy" hidden>
    <section class="tool-card"><div class="tool-kicker">Academy</div><div class="tool-title">KURGIN Academy</div><div class="tool-text">Обучение и объяснения по лабораторным бриллиантам, параметрам, анализу и интерпретации результатов.</div><div class="tool-note">UX-скелет. Материалы будут расширяться отдельно.</div></section>
  </div>
</div>
"""
