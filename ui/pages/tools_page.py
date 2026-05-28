import streamlit as st

from ui.index_components import render_public_index_tool


TOOLS = (
    "single_stone_analyzer",
    "kurgin_index",
    "database_analysis",
    "excel_analyzer",
    "kurgin_academy",
)


def _active_tool_from_query() -> str:
    tool = st.query_params.get("tool")
    return tool if tool in TOOLS else "single_stone_analyzer"


def _selected(active_tool: str, tool: str) -> str:
    return "true" if active_tool == tool else "false"


def _hidden(active_tool: str, tool: str) -> str:
    return "" if active_tool == tool else " hidden"


def render_tools_page() -> str:
    active_tool = _active_tool_from_query()
    tab_click = "const root=this.closest('.tools-page');const active=this.getAttribute('data-tool-tab');root.querySelectorAll('[data-tool-tab]').forEach(t=>t.setAttribute('aria-selected','false'));this.setAttribute('aria-selected','true');root.querySelectorAll('[data-tool-panel]').forEach(p=>p.hidden=p.getAttribute('data-tool-panel')!==active);try{const url=new URL(window.parent.location.href);url.searchParams.set('page','tools');url.searchParams.set('tool',active);window.parent.history.replaceState(null,'',url.toString());}catch(e){}"
    public_index_tool = render_public_index_tool()
    return f"""
<div class="tools-page">
  <div class="tools-tabs" role="tablist" aria-label="Инструменты KURGIN">
    <button type="button" class="tools-tab" role="tab" data-tool-tab="single_stone_analyzer" aria-selected="{_selected(active_tool, 'single_stone_analyzer')}" onclick="{tab_click}">KURGIN<br>Stone Analyzer</button>
    <button type="button" class="tools-tab" role="tab" data-tool-tab="kurgin_index" aria-selected="{_selected(active_tool, 'kurgin_index')}" onclick="{tab_click}">KURGIN<br>Index</button>
    <button type="button" class="tools-tab" role="tab" data-tool-tab="database_analysis" aria-selected="{_selected(active_tool, 'database_analysis')}" onclick="{tab_click}">KURGIN<br>Verify</button>
    <button type="button" class="tools-tab" role="tab" data-tool-tab="excel_analyzer" aria-selected="{_selected(active_tool, 'excel_analyzer')}" onclick="{tab_click}">KURGIN<br>Mass Analyzer</button>
    <button type="button" class="tools-tab" role="tab" data-tool-tab="kurgin_academy" aria-selected="{_selected(active_tool, 'kurgin_academy')}" onclick="{tab_click}">KURGIN<br>Academy</button>
  </div>

  <div class="tools-tab-content" data-tool-panel="single_stone_analyzer"{_hidden(active_tool, 'single_stone_analyzer')}>
    <div class="single-tool analyzer-preview">
      <div class="tool-section-title">KURGIN Stone Analyzer</div>
      <div class="muted">Public preview skeleton. Engine не подключён: расчёт, формула, загрузка файлов и отчёты сейчас не выполняются.</div>

      <div class="analyzer-mode-row" aria-label="Analyzer modes">
        <div class="analyzer-mode active"><strong>Manual preview</strong><span>phase 1</span></div>
        <div class="analyzer-mode inactive"><strong>Upload</strong><span>later</span></div>
        <div class="analyzer-mode inactive"><strong>Batch</strong><span>later</span></div>
      </div>

      <section class="single-workspace analyzer-workspace">
        <div class="workspace-title">Manual input preview</div>
        <div class="workspace-text">Поля ниже показывают будущую структуру ручного ввода. Они не запускают backend calculation и не отправляют данные.</div>
        <div class="analyzer-preview-notice">Форма показана как preview. Данные не отправляются и расчёт не выполняется.</div>

        <div class="analyzer-form-grid" aria-label="KURGIN Stone Analyzer preview form">
          <label class="analyzer-control analyzer-select"><span>Shape</span><select disabled aria-label="Shape preview"><option>Round</option></select></label>
          <label class="analyzer-control analyzer-input"><span>Carat</span><input type="text" value="1.00 ct" disabled readonly aria-label="Carat preview"></label>
          <label class="analyzer-control analyzer-select"><span>Color</span><select disabled aria-label="Color preview"><option>D / E / F</option></select></label>
          <label class="analyzer-control analyzer-select"><span>Clarity</span><select disabled aria-label="Clarity preview"><option>VVS / VS</option></select></label>
          <label class="analyzer-control analyzer-input optional"><span>Table %</span><input type="text" value="optional" disabled readonly aria-label="Table percentage preview"></label>
          <label class="analyzer-control analyzer-input optional"><span>Depth %</span><input type="text" value="optional" disabled readonly aria-label="Depth percentage preview"></label>
          <label class="analyzer-control analyzer-input optional"><span>Crown angle</span><input type="text" value="optional" disabled readonly aria-label="Crown angle preview"></label>
          <label class="analyzer-control analyzer-input optional"><span>Pavilion angle</span><input type="text" value="optional" disabled readonly aria-label="Pavilion angle preview"></label>
        </div>

        <button type="button" class="single-file-button analyzer-disabled-cta" disabled>Получить предварительный результат</button>
        <div class="analyzer-disabled-note">Engine будет подключён через adapter contract.</div>
      </section>

      <section class="single-next-box analyzer-preview-result">
        <div class="result-kicker">Предварительный режим</div>
        <div class="result-title">Расчёт будет подключён через adapter layer</div>
        <div class="result-text">Этот блок показывает будущий public-safe результат без раскрытия формулы и внутренних коэффициентов.</div>
        <ul class="analyzer-limitations">
          <li>Не является сертификатом.</li>
          <li>Не является оценкой стоимости.</li>
          <li>Не является геммологическим заключением.</li>
          <li>Формула и внутренние коэффициенты не раскрываются.</li>
        </ul>
      </section>
    </div>
  </div>

  <div class="tools-tab-content" data-tool-panel="kurgin_index"{_hidden(active_tool, 'kurgin_index')}>
    {public_index_tool}
  </div>

  <div class="tools-tab-content" data-tool-panel="database_analysis"{_hidden(active_tool, 'database_analysis')}>
    <section class="tool-card"><div class="tool-kicker">Verify · MVP skeleton</div><div class="tool-title">KURGIN Verify</div><div class="tool-text">Будущий раздел проверки и сверки данных. Сейчас не выполняет проверку, не создаёт заключение и не подтверждает наличие.</div><div class="tool-note">Не сертификат, не гарантия и не рабочий сервис в public MVP.</div></section>
  </div>

  <div class="tools-tab-content" data-tool-panel="excel_analyzer"{_hidden(active_tool, 'excel_analyzer')}>
    <section class="tool-card"><div class="tool-kicker">Mass Analyzer · MVP skeleton</div><div class="tool-title">KURGIN Mass Analyzer</div><div class="tool-text">Будущий Excel / batch-анализ списка камней. Загрузка файлов и расчёты сейчас не подключены в public MVP.</div><div class="tool-note">Не публикация, не checkout, не изменение каталога и не рабочий Analyzer.</div></section>
  </div>

  <div class="tools-tab-content" data-tool-panel="kurgin_academy"{_hidden(active_tool, 'kurgin_academy')}>
    <section class="tool-card"><div class="tool-kicker">Academy · MVP skeleton</div><div class="tool-title">KURGIN Academy</div><div class="tool-text">Будущий образовательный раздел о лабораторных бриллиантах, параметрах и интерпретации результатов.</div><div class="tool-note">Материалы и обучение не запущены как рабочий продукт в текущей public-версии.</div></section>
  </div>
</div>
"""
