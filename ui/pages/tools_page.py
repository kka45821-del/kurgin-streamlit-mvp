import html

import streamlit as st

from services.analyzer_adapter import analyze_public_stone
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


def _escape(value: object) -> str:
    return html.escape(str(value if value is not None else "—"), quote=True)


def _preview_payload() -> dict[str, object]:
    return {
        "shape": "Round",
        "carat": 1.00,
        "color": "E",
        "clarity": "VS1",
        "table_pct": 57.0,
        "depth_pct": 61.8,
        "crown_angle": 34.7,
        "pavilion_angle": 40.8,
        "crown_height": 15.0,
        "pavilion_depth": 43.0,
        "girdle": 3.5,
        "fluorescence": "None",
        "report_number": "PREVIEW-STUB",
    }


def _list_items(values: list[object]) -> str:
    if not values:
        return "<li>—</li>"
    return "".join(f"<li>{_escape(value)}</li>" for value in values)


def _render_adapter_mock_result(result: dict[str, object]) -> str:
    warnings = result.get("warnings") if isinstance(result.get("warnings"), list) else []
    limitations = result.get("limitations") if isinstance(result.get("limitations"), list) else []
    return f"""
<details class="analyzer-adapter-preview">
  <summary>Показать mock preview</summary>
  <div class="analyzer-result-grid" aria-label="Analyzer adapter mock result">
    <div><span>Status</span><strong>{_escape(result.get('status'))}</strong></div>
    <div><span>Score band</span><strong>{_escape(result.get('score_band'))}</strong></div>
    <div class="wide"><span>Summary</span><strong>{_escape(result.get('summary'))}</strong></div>
    <div class="wide"><span>Next action</span><strong>{_escape(result.get('next_action'))}</strong></div>
  </div>
  <div class="analyzer-result-list"><strong>Warnings</strong><ul>{_list_items(warnings)}</ul></div>
  <div class="analyzer-result-list"><strong>Limitations</strong><ul>{_list_items(limitations)}</ul></div>
</details>
"""


def render_tools_page() -> str:
    active_tool = _active_tool_from_query()
    tab_click = "const root=this.closest('.tools-page');const active=this.getAttribute('data-tool-tab');root.querySelectorAll('[data-tool-tab]').forEach(t=>t.setAttribute('aria-selected','false'));this.setAttribute('aria-selected','true');root.querySelectorAll('[data-tool-panel]').forEach(p=>p.hidden=p.getAttribute('data-tool-panel')!==active);try{const url=new URL(window.parent.location.href);url.searchParams.set('page','tools');url.searchParams.set('tool',active);window.parent.history.replaceState(null,'',url.toString());}catch(e){}"
    public_index_tool = render_public_index_tool()
    adapter_mock_result = analyze_public_stone(_preview_payload())
    adapter_mock_result_html = _render_adapter_mock_result(adapter_mock_result)
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
      <div class="muted">Это adapter stub preview. Реальная формула не подключена: расчёт, формула, загрузка файлов и отчёты сейчас не выполняются.</div>

      <div class="analyzer-mode-row" aria-label="Analyzer modes">
        <div class="analyzer-mode active"><strong>Manual preview</strong><span>phase 1</span></div>
        <div class="analyzer-mode inactive"><strong>Upload</strong><span>later</span></div>
        <div class="analyzer-mode inactive"><strong>Batch</strong><span>later</span></div>
      </div>

      <section class="single-workspace analyzer-workspace">
        <div class="workspace-title">Manual adapter preview</div>
        <div class="workspace-text">Поля ниже показывают будущую структуру ручного ввода. Данные не отправляются в backend и не запускают реальный engine.</div>
        <div class="analyzer-preview-notice">Форма показана как preview. Данные не отправляются и расчёт не выполняется.</div>

        <div class="analyzer-form-grid" aria-label="KURGIN Stone Analyzer preview form">
          <label class="analyzer-control analyzer-select"><span>Shape</span><select disabled aria-label="Shape preview"><option>Round</option></select></label>
          <label class="analyzer-control analyzer-input"><span>Carat</span><input type="text" value="1.00 ct" disabled readonly aria-label="Carat preview"></label>
          <label class="analyzer-control analyzer-select"><span>Color</span><select disabled aria-label="Color preview"><option>E</option></select></label>
          <label class="analyzer-control analyzer-select"><span>Clarity</span><select disabled aria-label="Clarity preview"><option>VS1</option></select></label>
          <label class="analyzer-control analyzer-input optional"><span>Table %</span><input type="text" value="57.0" disabled readonly aria-label="Table percentage preview"></label>
          <label class="analyzer-control analyzer-input optional"><span>Depth %</span><input type="text" value="61.8" disabled readonly aria-label="Depth percentage preview"></label>
          <label class="analyzer-control analyzer-input optional"><span>Crown angle</span><input type="text" value="34.7" disabled readonly aria-label="Crown angle preview"></label>
          <label class="analyzer-control analyzer-input optional"><span>Pavilion angle</span><input type="text" value="40.8" disabled readonly aria-label="Pavilion angle preview"></label>
        </div>

        <button type="button" class="single-file-button analyzer-mock-cta">Показать mock preview</button>
        <div class="analyzer-disabled-note">Результат ниже создан через public-safe adapter stub. Реальная формула не подключена.</div>
      </section>

      <section class="single-next-box analyzer-preview-result">
        <div class="result-kicker">Adapter stub preview</div>
        <div class="result-title">Mock result по public adapter contract</div>
        <div class="result-text">Это не настоящий расчёт. UI показывает только безопасные поля: status, score_band, summary, warnings, limitations и next_action.</div>
        {adapter_mock_result_html}
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
