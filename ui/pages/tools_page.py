PUBLIC_INDEX_ROWS = [
    ("D", "IF", "1.00–1.49", 250),
    ("D", "IF", "1.50–1.99", 380),
    ("D", "IF", "2.00–2.49", 480),
    ("D", "VVS1", "1.00–1.49", 125),
    ("D", "VVS1", "1.50–1.99", 150),
    ("D", "VVS1", "2.00–2.49", 170),
    ("D", "VVS1", "2.50–2.99", 210),
    ("D", "VVS1", "3.00–3.49", 245),
    ("D", "VVS1", "4.00–4.49", 325),
    ("D", "VVS2", "1.00–1.49", 110),
    ("D", "VVS2", "1.50–1.99", 115),
    ("D", "VVS2", "2.00–2.49", 120),
    ("D", "VVS2", "2.50–2.99", 125),
    ("D", "VVS2", "3.00–3.49", 135),
    ("D", "VVS2", "3.50–3.99", 145),
    ("D", "VVS2", "4.00–4.49", 160),
    ("D", "VVS2", "4.50–4.99", 170),
    ("D", "VS1", "1.00–1.49", 100),
    ("D", "VS1", "1.50–1.99", 100),
    ("D", "VS1", "2.00–2.49", 105),
    ("D", "VS1", "2.50–2.99", 115),
    ("D", "VS1", "3.00–3.49", 125),
    ("D", "VS1", "3.50–3.99", 130),
    ("E", "IF", "1.00–1.49", 185),
    ("E", "VVS1", "1.00–1.49", 120),
    ("E", "VVS1", "1.50–1.99", 145),
    ("E", "VVS1", "2.00–2.49", 150),
    ("E", "VVS1", "2.50–2.99", 160),
    ("E", "VVS1", "3.00–3.49", 165),
    ("E", "VVS2", "1.00–1.49", 105),
    ("E", "VVS2", "1.50–1.99", 110),
    ("E", "VVS2", "2.00–2.49", 105),
    ("E", "VVS2", "2.50–2.99", 100),
    ("E", "VVS2", "3.00–3.49", 100),
    ("E", "VS1", "1.00–1.49", 95),
    ("E", "VS1", "1.50–1.99", 98),
    ("E", "VS1", "2.00–2.49", 98),
    ("E", "VS1", "2.50–2.99", 98),
    ("E", "VS1", "3.00–3.49", 98),
    ("E", "VS1", "3.50–3.99", 100),
    ("E", "VS1", "4.00–4.49", 100),
    ("E", "VS1", "4.50–4.99", 105),
    ("F", "IF", "1.00–1.49", 150),
    ("F", "IF", "1.50–1.99", 150),
    ("F", "VVS1", "1.00–1.49", 115),
    ("F", "VVS1", "1.50–1.99", 135),
    ("F", "VVS1", "2.00–2.49", 145),
    ("F", "VVS1", "2.50–2.99", 155),
    ("F", "VVS1", "3.00–3.49", 155),
    ("F", "VVS1", "4.50–4.99", 175),
    ("F", "VVS2", "1.00–1.49", 100),
    ("F", "VVS2", "1.50–1.99", 100),
    ("F", "VVS2", "2.00–2.49", 100),
    ("F", "VVS2", "2.50–2.99", 100),
    ("F", "VVS2", "3.00–3.49", 100),
    ("F", "VVS2", "3.50–3.99", 100),
    ("F", "VVS2", "4.00–4.49", 105),
    ("F", "VVS2", "4.50–4.99", 105),
    ("F", "VS1", "1.00–1.49", 95),
    ("F", "VS1", "1.50–1.99", 95),
    ("F", "VS1", "2.00–2.49", 95),
    ("F", "VS1", "2.50–2.99", 95),
    ("F", "VS1", "3.00–3.49", 95),
    ("F", "VS1", "3.50–3.99", 98),
    ("F", "VS1", "4.00–4.49", 100),
    ("F", "VS1", "4.50–4.99", 100),
    ("G", "VVS1", "2.00–2.49", 110),
    ("G", "VVS2", "3.00–3.49", 95),
    ("G", "VS1", "1.50–1.99", 95),
    ("G", "VS1", "2.00–2.49", 95),
    ("G", "VS1", "3.00–3.49", 95),
]

INDEX_COLORS = ["D", "E", "F", "G"]
INDEX_CLARITIES = ["IF", "VVS1", "VVS2", "VS1", "VS2", "SI1"]
INDEX_BANDS = [
    ("1.00–1.49", "1–1.49"),
    ("1.50–1.99", "1.5–1.99"),
    ("2.00–2.49", "2–2.49"),
    ("2.50–2.99", "2.5–2.99"),
    ("3.00–3.49", "3–3.49"),
    ("3.50–3.99", "3.5–3.99"),
    ("4.00–4.49", "4–4.49"),
    ("4.50–4.99", "4.5–4.99"),
]


def _index_value_map() -> dict[tuple[str, str, str], int]:
    return {(color, clarity, carat_band): int(value) for color, clarity, carat_band, value in PUBLIC_INDEX_ROWS if value > 0}


def _index_cell_html(value: int | None) -> str:
    if value:
        return f"<div class='index-cell-main'>{value} $/ct</div><div class='index-cell-sub'>Δ%</div>"
    return "<div class='index-cell-main muted'>request</div><div class='index-cell-sub'>—</div>"


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


def render_tools_page() -> str:
    tab_click = "const root=this.closest('.tools-page');const active=this.getAttribute('data-tool-tab');root.querySelectorAll('[data-tool-tab]').forEach(t=>t.setAttribute('aria-selected','false'));this.setAttribute('aria-selected','true');root.querySelectorAll('[data-tool-panel]').forEach(p=>p.hidden=p.getAttribute('data-tool-panel')!==active);try{const url=new URL(window.parent.location.href);url.searchParams.set('page','tools');url.searchParams.set('tool',active);window.parent.history.replaceState(null,'',url.toString());}catch(e){}"
    mode_click = "const root=this.closest('.single-tool');const active=this.getAttribute('data-mode');root.querySelectorAll('[data-mode]').forEach(t=>t.setAttribute('aria-selected','false'));this.setAttribute('aria-selected','true');root.querySelectorAll('[data-mode-panel]').forEach(p=>p.hidden=p.getAttribute('data-mode-panel')!==active);"
    share_click = "const url=new URL(window.parent.location.href);url.searchParams.set('page','tools');url.searchParams.set('tool','kurgin_index');url.hash='kurgin-index';const shareData={title:'KURGIN Index',text:'KURGIN Index — ориентир для сопоставления лабораторных бриллиантов',url:url.toString()};if(navigator.share){navigator.share(shareData).catch(()=>{});}else if(navigator.clipboard){navigator.clipboard.writeText(url.toString()).then(()=>{this.textContent='Ссылка скопирована';setTimeout(()=>{this.textContent='↗ Поделиться Index';},1400);});}else{window.prompt('Скопируйте ссылку',url.toString());}"
    deep_link_init = "const trigger=this;setTimeout(()=>{const allowed=['single_stone_analyzer','kurgin_index','database_analysis','excel_analyzer','kurgin_academy'];try{const url=new URL(window.parent.location.href);const tool=url.searchParams.get('tool');if(!allowed.includes(tool))return;const root=trigger.closest('.tools-page');const tab=root&&root.querySelector('[data-tool-tab=\\\"'+tool+'\\\"]');if(tab){tab.click();}if(url.hash){const target=root&&root.querySelector(url.hash);if(target)target.scrollIntoView({block:'start'});}}catch(e){}},0);"
    index_sections = _index_sections_html()
    return f"""
<div class="tools-page">
  <img src="x" alt="" hidden onerror="{deep_link_init}">
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
    <section class="index-shell" id="kurgin-index">
      <div class="index-info-card">
        <div class="index-title">KURGIN Index v1.0</div>
        <div>Обновлено: текущий период</div>
        <div>Основные камни: 1.00–4.99 ct</div>
        <button type="button" class="btn light" onclick="{share_click}">↗ Поделиться Index</button>
      </div>
      <div class="index-score-card">
        <div class="index-subtitle">KURGIN Score range</div>
        <div>Выбрано: 80–89 · коэффициент ×1</div>
        <div class="index-hint">selector влияет на значения таблицы, это не фильтр</div>
      </div>
      {index_sections}
      <button type="button" class="index-filter-button">☰ Фильтры Index</button>
      <div class="tool-note">Индекс — ориентир для сопоставления. Не оферта, не финальная цена конкретного камня, не финансовый индекс и не инвестиционная рекомендация.</div>
    </section>
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
