import html


DEMO_ROWS = (
    ("1", "Round", "1.00", "E", "VS1", "IGI", "LG-DEMO-001", "ready", "—"),
    ("2", "Round", "1.20", "F", "VS2", "IGI", "LG-DEMO-002", "incomplete", "не заполнены геометрические поля"),
    ("3", "Oval", "1.10", "G", "VS1", "IGI", "LG-DEMO-003", "unsupported_shape", "форма пока не поддерживается"),
    ("4", "Round", "—", "H", "SI1", "IGI", "LG-DEMO-004", "invalid_input", "ошибочное значение веса"),
    ("5", "Round", "1.00", "E", "VS1", "IGI", "LG-DEMO-001", "duplicate", "дубликат report number"),
)

DEMO_RESULTS = (
    ("LG-DEMO-001", "Round", "1.00", "E", "VS1", "Review", "ready", "демо-режим", "не сертификат", "request_professional_review"),
    ("LG-DEMO-002", "Round", "1.20", "F", "VS2", "Review", "incomplete", "не хватает данных", "не оценка цены", "fix_parameters"),
    ("LG-DEMO-003", "Oval", "1.10", "G", "VS1", "Unsupported", "unsupported_shape", "форма не поддерживается", "не геммологическое заключение", "request_professional_review"),
)

ROW_DETAIL = {
    "исходные параметры": "Round · 1.00 ct · E · VS1 · IGI · LG-DEMO-001",
    "статус анализа": "ready",
    "score band": "Review",
    "summary": "Демонстрационная строка готова к будущему безопасному анализу.",
    "warnings": "демо-режим; расчёт не выполнялся",
    "limitations": "не сертификат; не оценка цены; не геммологическое заключение",
    "next_action": "request_professional_review",
}


def _escape(value: object) -> str:
    return html.escape(str(value if value is not None else "—"), quote=True)


def _render_requirements() -> str:
    checks = (
        "формат файла",
        "обязательные колонки",
        "названия колонок",
        "количество строк",
        "дубликаты report number",
        "пустые обязательные поля",
        "неподдерживаемые формы",
        "ошибочные значения",
    )
    return "".join(f"<li>{_escape(check)}</li>" for check in checks)


def _render_preview_rows() -> str:
    rows = []
    for row in DEMO_ROWS:
        rows.append("<tr>" + "".join(f"<td>{_escape(cell)}</td>" for cell in row) + "</tr>")
    return "".join(rows)


def _render_result_rows() -> str:
    rows = []
    for row in DEMO_RESULTS:
        rows.append("<tr>" + "".join(f"<td>{_escape(cell)}</td>" for cell in row) + "</tr>")
    return "".join(rows)


def _render_row_detail() -> str:
    rows = "".join(
        f"<div><span>{_escape(label)}</span><strong>{_escape(value)}</strong></div>"
        for label, value in ROW_DETAIL.items()
    )
    return f"""
<section class="tool-card mass-analyzer-row-detail">
  <div class="tool-kicker">Шаг 7</div>
  <div class="tool-title">Деталь строки</div>
  <div class="tool-text">Skeleton показывает безопасную карточку одной строки результата без внутренних расчётов и технических полей.</div>
  <div class="analyzer-result-grid" aria-label="Mass Analyzer row detail skeleton">
    {rows}
  </div>
  <div class="favoriteActions">
    <button type="button" class="favoriteBtn disabled">Вернуться к таблице — позже</button>
    <button type="button" class="favoriteBtn disabled">Задать вопрос менеджеру — позже</button>
    <button type="button" class="favoriteBtn disabled">Начать анализ одного камня — позже</button>
  </div>
</section>
"""


def render_mass_analyzer_preview() -> str:
    return f"""
<section class="tool-card mass-analyzer-preview">
  <div class="tool-kicker">Mass Analyzer · Excel skeleton</div>
  <div class="tool-title">KURGIN Mass Analyzer</div>
  <div class="tool-text">Массовый анализ Excel: анализ группы камней по таблице. Это не сертификат, не оценка цены и не публикация в каталог.</div>
  <div class="tool-note">Загрузка Excel будет позже. Сейчас раздел не выполняет расчёт, не публикует данные, не меняет каталог. Не создаёт заказ, резерв или оплату.</div>
  <div class="favoriteActions">
    <button type="button" class="favoriteBtn disabled">Загрузить Excel — позже</button>
    <button type="button" class="favoriteBtn disabled">Скачать шаблон — позже</button>
    <button type="button" class="favoriteBtn">Посмотреть требования к файлу</button>
    <button type="button" class="favoriteBtn">Посмотреть пример результата</button>
  </div>
</section>

<section class="tool-card mass-analyzer-upload">
  <div class="tool-kicker">Шаг 1 · Upload</div>
  <div class="tool-title">Загрузка файла</div>
  <div class="tool-text">Excel-файл будет проверяться до запуска анализа. В текущем MVP реальная загрузка и обработка файла не выполняются.</div>
  <div class="analyzer-form-grid" aria-label="Mass Analyzer upload skeleton">
    <label class="analyzer-control analyzer-input"><span>Excel-файл</span><input type="text" value="Файл не выбран" disabled readonly></label>
    <label class="analyzer-control analyzer-input"><span>Язык результата</span><input type="text" value="RU / EN" disabled readonly></label>
    <label class="analyzer-control analyzer-input"><span>Тип анализа</span><input type="text" value="предварительный / полный — позже" disabled readonly></label>
  </div>
  <div class="favoriteActions">
    <button type="button" class="favoriteBtn disabled">Проверить файл — позже</button>
    <button type="button" class="favoriteBtn disabled">Скачать шаблон — позже</button>
  </div>
</section>

<section class="tool-card mass-analyzer-validation">
  <div class="tool-kicker">Шаг 2 · Validate</div>
  <div class="tool-title">Проверка шаблона</div>
  <div class="tool-text">Будущие проверки перед анализом:</div>
  <ul class="analyzer-limitations">{_render_requirements()}</ul>
</section>

<section class="tool-card mass-analyzer-preview-table">
  <div class="tool-kicker">Шаг 3 · Preview</div>
  <div class="tool-title">Предпросмотр данных</div>
  <div class="tool-text">Demo table показывает будущие статусы строк без запуска анализа.</div>
  <div class="mass-table-wrap">
    <table class="mass-table">
      <thead><tr><th>строка</th><th>форма</th><th>вес</th><th>цвет</th><th>чистота</th><th>лаборатория</th><th>report number</th><th>статус данных</th><th>ошибки / предупреждения</th></tr></thead>
      <tbody>{_render_preview_rows()}</tbody>
    </table>
  </div>
</section>

<section class="tool-card mass-analyzer-confirm">
  <div class="tool-kicker">Шаг 4 · Confirm</div>
  <div class="tool-title">Подтверждение запуска</div>
  <div class="tool-text">Анализ не запускается в текущем MVP. Запуск будет доступен после утверждения batch Analyzer contract.</div>
  <div class="analyzer-result-grid" aria-label="Mass Analyzer confirm summary">
    <div><span>всего строк</span><strong>5</strong></div>
    <div><span>готово к анализу</span><strong>1</strong></div>
    <div><span>пропущено</span><strong>3</strong></div>
    <div><span>ошибки</span><strong>1</strong></div>
  </div>
  <div class="favoriteActions">
    <button type="button" class="favoriteBtn disabled">Подтвердить запуск — позже</button>
    <button type="button" class="favoriteBtn disabled">Назад к предпросмотру — позже</button>
    <button type="button" class="favoriteBtn disabled">Отменить — позже</button>
  </div>
</section>

<section class="tool-card mass-analyzer-run">
  <div class="tool-kicker">Шаг 5 · Analyze</div>
  <div class="tool-title">Процесс анализа</div>
  <div class="tool-text">Future process block. Прогресс ниже является skeleton и не связан с реальным расчётом.</div>
  <div class="analyzer-result-grid" aria-label="Mass Analyzer future progress">
    <div><span>обработано</span><strong>0 из 1</strong></div>
    <div><span>успешно</span><strong>0</strong></div>
    <div><span>ошибки</span><strong>0</strong></div>
    <div><span>пропущено</span><strong>0</strong></div>
  </div>
  <button type="button" class="single-file-button disabled">Запустить массовый анализ — позже</button>
  <div class="tool-note">Массовый анализ будет подключён после утверждения batch Analyzer contract.</div>
</section>

<section class="tool-card mass-analyzer-results">
  <div class="tool-kicker">Шаг 6 · Results table</div>
  <div class="tool-title">Таблица результатов</div>
  <div class="tool-text">Demo result table показывает только безопасные публичные поля будущего результата.</div>
  <div class="mass-table-wrap">
    <table class="mass-table">
      <thead><tr><th>report number</th><th>shape</th><th>carat</th><th>color</th><th>clarity</th><th>score band</th><th>status</th><th>warnings</th><th>limitations</th><th>next_action</th></tr></thead>
      <tbody>{_render_result_rows()}</tbody>
    </table>
  </div>
  <div class="favoriteActions">
    <button type="button" class="favoriteBtn disabled">Скачать результат Excel — позже</button>
    <button type="button" class="favoriteBtn disabled">Новый анализ — позже</button>
  </div>
</section>

{_render_row_detail()}

<section class="tool-card mass-analyzer-export">
  <div class="tool-kicker">Шаг 8 · Export result</div>
  <div class="tool-title">Экспорт результата</div>
  <div class="tool-text">Экспорт Excel будет доступен позже после утверждения безопасного batch-result contract.</div>
  <button type="button" class="single-file-button disabled">Скачать результат Excel — позже</button>
</section>
"""
