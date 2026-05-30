import streamlit as st

from ui.pages.tools.analyzer_preview import render_analyzer_preview
from ui.pages.tools.index_panel import render_index_panel
from ui.pages.tools.mass_analyzer_preview import render_mass_analyzer_preview


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
    analyzer_preview = render_analyzer_preview()
    index_panel = render_index_panel()
    mass_analyzer_preview = render_mass_analyzer_preview()
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
{analyzer_preview}
  </div>

  <div class="tools-tab-content" data-tool-panel="kurgin_index"{_hidden(active_tool, 'kurgin_index')}>
    {index_panel}
  </div>

  <div class="tools-tab-content" data-tool-panel="database_analysis"{_hidden(active_tool, 'database_analysis')}>
    <section class="tool-card"><div class="tool-kicker">Verify · MVP skeleton</div><div class="tool-title">KURGIN Verify</div><div class="tool-text">Будущий раздел проверки и сверки данных. Сейчас не выполняет проверку, не создаёт заключение и не подтверждает наличие.</div><div class="tool-note">Не сертификат, не гарантия и не рабочий сервис в public MVP.</div></section>
  </div>

  <div class="tools-tab-content" data-tool-panel="excel_analyzer"{_hidden(active_tool, 'excel_analyzer')}>
{mass_analyzer_preview}
  </div>

  <div class="tools-tab-content" data-tool-panel="kurgin_academy"{_hidden(active_tool, 'kurgin_academy')}>
    <section class="tool-card"><div class="tool-kicker">Academy · MVP skeleton</div><div class="tool-title">KURGIN Academy</div><div class="tool-text">Будущий образовательный раздел о лабораторных бриллиантах, параметрах и интерпретации результатов.</div><div class="tool-note">Материалы и обучение не запущены как рабочий продукт в текущей public-версии.</div></section>
  </div>
</div>
"""
