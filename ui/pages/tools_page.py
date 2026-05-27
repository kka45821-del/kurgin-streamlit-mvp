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


def _index_rows_html() -> str:
    rows = []
    for color, clarity, carat_band, value in PUBLIC_INDEX_ROWS:
        rows.append(
            "<tr>"
            f"<td>{carat_band}</td>"
            f"<td>{color}</td>"
            f"<td>{clarity}</td>"
            f"<td>{value}</td>"
            "<td>active</td>"
            "</tr>"
        )
    return "".join(rows)


def render_tools_page() -> str:
    tab_click = "const root=this.closest('.tools-page');const active=this.getAttribute('data-tool-tab');root.querySelectorAll('[data-tool-tab]').forEach(t=>t.setAttribute('aria-selected','false'));this.setAttribute('aria-selected','true');root.querySelectorAll('[data-tool-panel]').forEach(p=>p.hidden=p.getAttribute('data-tool-panel')!==active);"
    mode_click = "const root=this.closest('.single-tool');const active=this.getAttribute('data-mode');root.querySelectorAll('[data-mode]').forEach(t=>t.setAttribute('aria-selected','false'));this.setAttribute('aria-selected','true');root.querySelectorAll('[data-mode-panel]').forEach(p=>p.hidden=p.getAttribute('data-mode-panel')!==active);"
    index_rows = _index_rows_html()
    return f"""
<div class="tools-page">
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
    <section class="tool-card index-card">
      <div class="tool-kicker">Index</div>
      <div class="tool-title">KURGIN Index</div>
      <div class="tool-text">Публичный индексный ориентир для сопоставления лабораторных бриллиантов по диапазону карат, цвету и чистоте.</div>
      <div class="tool-note">Не является офертой, финальной ценой конкретного камня, финансовым индексом или инвестиционной рекомендацией.</div>
      <div class="index-meta">Snapshot: Admin Price Table v0.1 · values: USD / ct · zeros скрыты как request</div>
      <div class="index-table-wrap">
        <table class="index-table">
          <thead><tr><th>Carat</th><th>Color</th><th>Clarity</th><th>USD/ct</th><th>Status</th></tr></thead>
          <tbody>{index_rows}</tbody>
        </table>
      </div>
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
