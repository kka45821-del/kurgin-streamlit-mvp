from __future__ import annotations

from ui.index_data import INDEX_BANDS, INDEX_CLARITIES, INDEX_COLORS, load_public_index_rows
from ui.index_score_rules import SCORE_INDEX_RULES, SCORE_RANGE_SELECTOR_ORDER
from ui.index_scripts import SCORE_RANGE_CLICK, SHARE_CLICK
from ui.score_ranges import KURGIN_SCORE_RANGES, default_score_range_id


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


def _score_range_selector_html() -> str:
    default_id = default_score_range_id()
    ranges = _score_ranges_by_id()
    buttons = []
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
            f"aria-selected='{selected}' onclick=\"{SCORE_RANGE_CLICK}\">"
            f"<strong>{item['en']}</strong><span>{item['range_label']}</span><small>{item['ru']}</small>"
            "</button>"
        )
    return "".join(buttons)


def render_public_index_tool() -> str:
    index_sections = _index_sections_html()
    score_selector = _score_range_selector_html()
    return f"""
<section class="index-shell" id="kurgin-index">
  <div class="index-info-card">
    <div class="index-title">KURGIN Index v1.0</div>
    <div>Обновлено: текущий период</div>
    <div>Основные камни: 1.00–4.99 ct</div>
    <button type="button" class="btn light" onclick="{SHARE_CLICK}">↗ Поделиться Index</button>
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
  <button type="button" class="index-filter-button">☰ Фильтры Index</button>
  <div class="tool-note">Индекс — ориентир для сопоставления. Не оферта, не финальная цена конкретного камня, не финансовый индекс и не инвестиционная рекомендация.</div>
</section>
"""
