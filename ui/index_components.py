from __future__ import annotations

import html

from ui.index_data import INDEX_BANDS, INDEX_CLARITIES, INDEX_COLORS, load_public_index_rows
from ui.index_score_rules import SCORE_INDEX_RULES, SCORE_RANGE_SELECTOR_ORDER
from ui.index_scripts import (
    INDEX_COLLAPSE_ALL_COLORS,
    INDEX_EXPAND_ALL_COLORS,
    INDEX_PDF_PRINT,
    INDEX_VIEW_TOGGLE,
    SCORE_RANGE_CLICK,
    SHARE_CLICK,
)
from ui.score_ranges import KURGIN_SCORE_RANGES, default_score_range_id


LOGO_URL = "https://raw.githubusercontent.com/kka45821-del/kurgin-streamlit-mvp/main/Vectorr-header.svg?v=1"


def _html_attr(value: str) -> str:
    return html.escape(value, quote=True)


def _score_ranges_by_id() -> dict[str, dict[str, object]]:
    return {str(item["id"]): item for item in KURGIN_SCORE_RANGES}


def _index_value_map() -> dict[tuple[str, str, str], int]:
    return {(color, clarity, carat_band): int(value) for color, clarity, carat_band, value in load_public_index_rows() if value > 0}


def _index_cell_html(value: int | None) -> str:
    if value:
        return (
            f"<div class='index-cell' data-index-base='{int(value)}'>"
            f"<div class='index-cell-main'>{int(value)} $/ct</div>"
            "<div class='index-cell-sub'>×1.00</div>"
            "</div>"
        )
    return (
        "<div class='index-cell' data-index-base=''>"
        "<div class='index-cell-main muted'>request</div>"
        "<div class='index-cell-sub'>—</div>"
        "</div>"
    )


def _index_table_for_color(color: str) -> str:
    values = _index_value_map()
    header_cells = "".join(f"<th>{label}</th>" for _, label in INDEX_BANDS)
    body_rows = []
    for clarity in INDEX_CLARITIES:
        cells = []
        for band_key, _ in INDEX_BANDS:
            cells.append(f"<td>{_index_cell_html(values.get((color, clarity, band_key)))}</td>")
        body_rows.append(f"<tr><th>{clarity}</th>{''.join(cells)}</tr>")
    return (
        "<div class='index-matrix-wrap'>"
        "<table class='index-matrix'>"
        f"<thead><tr><th>Clarity</th>{header_cells}</tr></thead>"
        f"<tbody>{''.join(body_rows)}</tbody>"
        "</table>"
        "</div>"
    )


def _plain_index_value(value: int | None) -> str:
    return f"{int(value)} $/ct" if value else "request"


def _pdf_table_for_color(color: str) -> str:
    values = _index_value_map()
    header_cells = "".join(f"<th>{label}</th>" for _, label in INDEX_BANDS)
    body_rows = []
    for clarity in INDEX_CLARITIES:
        cells = []
        for band_key, _ in INDEX_BANDS:
            cells.append(f"<td>{_plain_index_value(values.get((color, clarity, band_key)))}</td>")
        body_rows.append(f"<tr><th>{clarity}</th>{''.join(cells)}</tr>")
    return f"<table class='pdf-table'><thead><tr><th>Clarity</th>{header_cells}</tr></thead><tbody>{''.join(body_rows)}</tbody></table>"


def _index_sections_html() -> str:
    sections = []
    for color in INDEX_COLORS:
        open_attr = " open" if color == "E" else ""
        sections.append(
            f"<details class='index-color-section'{open_attr}>"
            f"<summary>Цвет {color}</summary>"
            f"{_index_table_for_color(color)}"
            "</details>"
        )
    return "".join(sections)


def _pdf_sections_html() -> str:
    sections = []
    for color in INDEX_COLORS:
        sections.append(
            f"<section class='pdf-section'><h2>Color {color}</h2>{_pdf_table_for_color(color)}</section>"
        )
    return "".join(sections)


def _score_range_selector_html() -> str:
    default_id = default_score_range_id()
    ranges = _score_ranges_by_id()
    buttons = []
    score_range_click = _html_attr(SCORE_RANGE_CLICK)
    for range_id in SCORE_RANGE_SELECTOR_ORDER:
        item = ranges[range_id]
        rule = SCORE_INDEX_RULES[range_id]
        selected = "true" if item["id"] == default_id else "false"
        buttons.append(
            "<button type='button' class='score-range-button' role='tab' "
            f"data-score-range='{item['id']}' "
            f"data-score-label='{item['en']}' "
            f"data-score-ru='{item['ru']}' "
            f"data-score-range-label='{item['range_label']}' "
            f"data-score-mode='{rule['mode']}' "
            f"data-score-coefficient='{rule['coefficient']}' "
            f"data-score-coefficient-label='{rule['coefficient_label']}' "
            f"aria-selected='{selected}' onclick=\"{score_range_click}\">"
            f"<strong>{item['en']}</strong><span>{item['range_label']}</span><small>{item['ru']}</small>"
            "</button>"
        )
    return "".join(buttons)


def _pdf_template_html() -> str:
    return f"""
<div id="index-pdf-template" hidden>
  <div class="pdf-head">
    <img class="pdf-logo" src="{LOGO_URL}" alt="KURGIN">
    <div>
      <div class="pdf-title">KURGIN Index</div>
      <div class="pdf-meta">Snapshot: public_index_v0_1 · Unit: USD / ct · Period: current</div>
    </div>
  </div>
  <div class="pdf-note">KURGIN Index is an indicative benchmark for comparing laboratory-grown diamonds. It is not an offer, not a final price for a specific stone, not a financial index and not an investment recommendation.</div>
  {_pdf_sections_html()}
</div>
"""


def _index_view_panel_html() -> str:
    expand_all = _html_attr(INDEX_EXPAND_ALL_COLORS)
    collapse_all = _html_attr(INDEX_COLLAPSE_ALL_COLORS)
    return f"""
<div class="index-view-panel" hidden>
  <div class="index-view-title">Вид таблицы Index</div>
  <div class="index-view-text">Это настройки просмотра таблицы индекса. Они не меняют каталог, цены камней или формулы.</div>
  <div class="index-view-actions">
    <button type="button" class="index-view-action" onclick="{expand_all}">Раскрыть все цвета</button>
    <button type="button" class="index-view-action" onclick="{collapse_all}">Свернуть все цвета</button>
  </div>
  <div class="index-view-hint">Подсказка: двигайте таблицу влево-вправо. Первый столбик “Clarity / чистота” остаётся на месте.</div>
</div>
"""


def render_public_index_tool() -> str:
    index_sections = _index_sections_html()
    score_selector = _score_range_selector_html()
    pdf_template = _pdf_template_html()
    index_view_panel = _index_view_panel_html()
    share_click = _html_attr(SHARE_CLICK)
    index_pdf_print = _html_attr(INDEX_PDF_PRINT)
    index_view_toggle = _html_attr(INDEX_VIEW_TOGGLE)
    return f"""
<section class="index-shell" id="kurgin-index">
  <div class="index-info-card">
    <div class="index-title">KURGIN Index v1.0</div>
    <div>Обновлено: текущий период</div>
    <div>Основные камни: 1.00–4.99 ct</div>
    <button type="button" class="btn light" onclick="{share_click}">↗ Поделиться Index</button>
    <button type="button" class="btn light" onclick="{index_pdf_print}">⬇ Скачать PDF</button>
  </div>
  <div class="index-score-card">
    <div class="index-subtitle">KURGIN Score range</div>
    <div class="index-score-selected">Standard / Стандартный · 80–89.99</div>
    <div class="index-score-coefficient">Коэффициент: ×1.00</div>
    <div class="score-range-selector" role="tablist" aria-label="KURGIN Score ranges">{score_selector}</div>
    <div class="index-hint">Значения индекса меняются по выбранному диапазону KURGIN Score. Это ориентир, не финальная цена конкретного камня. Backend formula и pricing formula не менялись.</div>
  </div>
  {index_sections}
  <div class="index-range-summary">
    <div class="index-range-summary-selected">Standard / Стандартный · 80–89.99</div>
    <div class="index-range-summary-coefficient">Коэффициент: ×1.00</div>
    <div class="index-range-disclaimer">Это индексный ориентир для сопоставления лабораторных бриллиантов. Это не цена конкретного камня, не оферта, не финансовый индекс и не инвестиционная рекомендация.</div>
  </div>
  {index_view_panel}
  <button type="button" class="index-filter-button" aria-expanded="false" onclick="{index_view_toggle}">☰ Вид таблицы Index</button>
  <div class="tool-note">“Вид таблицы Index” — это настройки просмотра самой таблицы индекса, не фильтры каталога. Индекс остаётся ориентиром: не оферта, не финальная цена конкретного камня, не финансовый индекс и не инвестиционная рекомендация.</div>
  {pdf_template}
</section>
"""
