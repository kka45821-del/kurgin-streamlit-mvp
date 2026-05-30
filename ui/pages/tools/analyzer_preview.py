import html

from services.analyzer_adapter import analyze_public_stone


DEFAULT_PUBLIC_INPUT = {
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
    "report_number": "PREVIEW-DEMO",
}


FORM_FIELDS = (
    ("shape", "Огранка", "Round"),
    ("carat", "Каратность", "1.00"),
    ("color", "Цвет", "E"),
    ("clarity", "Чистота", "VS1"),
    ("table_pct", "Площадка, %", "57.0"),
    ("depth_pct", "Глубина, %", "61.8"),
    ("crown_angle", "Угол короны", "34.7"),
    ("pavilion_angle", "Угол павильона", "40.8"),
    ("crown_height", "Высота короны, %", "15.0"),
    ("pavilion_depth", "Глубина павильона, %", "43.0"),
    ("girdle", "Рундист, %", "3.5"),
    ("fluorescence", "Флуоресценция", "None"),
    ("report_number", "Номер отчёта", "PREVIEW-DEMO"),
)

NEXT_ACTION_LABELS = {
    "request_professional_review": "Запросить профессиональную проверку",
}


def _escape(value: object) -> str:
    return html.escape(str(value if value is not None else "—"), quote=True)


def _list_items(values: list[object]) -> str:
    if not values:
        return "<li>—</li>"
    return "".join(f"<li>{_escape(value)}</li>" for value in values)


def _render_form_fields() -> str:
    fields = []
    for key, label, placeholder in FORM_FIELDS:
        value = DEFAULT_PUBLIC_INPUT.get(key, "")
        fields.append(
            f"""
          <label class="analyzer-control analyzer-input">
            <span>{_escape(label)}</span>
            <input type="text" name="{_escape(key)}" value="{_escape(value)}" placeholder="{_escape(placeholder)}" aria-label="{_escape(label)}">
          </label>"""
        )
    return "".join(fields)


def _render_public_safe_result(result: dict[str, object]) -> str:
    warnings = result.get("warnings") if isinstance(result.get("warnings"), list) else []
    limitations = result.get("limitations") if isinstance(result.get("limitations"), list) else []
    next_action = result.get("next_action") or "request_professional_review"
    next_action_label = NEXT_ACTION_LABELS.get(str(next_action), str(next_action))
    return f"""
      <section class="single-next-box analyzer-preview-result" aria-label="Предварительный публичный результат KURGIN Stone Analyzer">
        <div class="result-kicker">Демонстрационный режим</div>
        <div class="result-title">{_escape(result.get('score_band'))}</div>
        <div class="result-text">{_escape(result.get('summary'))}</div>
        <div class="analyzer-result-grid" aria-label="Безопасные поля предварительного результата">
          <div><span>Состояние</span><strong>{_escape(result.get('status'))}</strong></div>
          <div><span>Класс результата</span><strong>{_escape(result.get('score_band'))}</strong></div>
          <div class="wide"><span>Пояснение</span><strong>{_escape(result.get('summary'))}</strong></div>
          <div class="wide"><span>Следующий шаг</span><strong>{_escape(next_action_label)}</strong></div>
        </div>
        <div class="analyzer-result-list"><strong>Предупреждения</strong><ul>{_list_items(warnings)}</ul></div>
        <div class="analyzer-result-list"><strong>Ограничения</strong><ul>{_list_items(limitations)}</ul></div>
      </section>
"""


def render_analyzer_preview() -> str:
    preview_result = analyze_public_stone(DEFAULT_PUBLIC_INPUT)
    result_html = _render_public_safe_result(preview_result)
    form_fields = _render_form_fields()
    return f"""
    <div class="single-tool analyzer-preview">
      <div class="tool-section-title">KURGIN Stone Analyzer</div>
      <div class="muted">Предварительная проверка параметров для будущей Tools-интеграции. Расчётный контур не подключён в этой версии.</div>

      <div class="analyzer-mode-row" aria-label="Режимы Analyzer">
        <div class="analyzer-mode active"><strong>Ручной ввод</strong><span>демо</span></div>
        <div class="analyzer-mode inactive"><strong>Загрузка файла</strong><span>позже</span></div>
        <div class="analyzer-mode inactive"><strong>Пакетный анализ</strong><span>позже</span></div>
      </div>

      <section class="single-workspace analyzer-workspace">
        <div class="workspace-title">Ручной ввод параметров</div>
        <div class="workspace-text">Форма показывает первый безопасный слой ручной проверки. Сейчас это демонстрационный режим: данные не отправляются в backend и не запускают реальный engine.</div>
        <div class="analyzer-preview-notice">Нет checkout, оплаты, заявки, резерва, пакетной загрузки или Excel-загрузки. Служебные поля анализа не показываются.</div>

        <form class="analyzer-form-grid" aria-label="Форма предварительной проверки KURGIN Stone Analyzer">
{form_fields}
        </form>

        <button type="button" class="single-file-button analyzer-mock-cta">Показать предварительную проверку</button>
        <div class="analyzer-disabled-note">Результат ниже показан как пример безопасного публичного вывода: состояние, класс результата, пояснение, предупреждения, ограничения и следующий шаг.</div>
      </section>

{result_html}

      <section class="tool-card">
        <div class="tool-kicker">Контур безопасности</div>
        <div class="tool-title">Что скрыто</div>
        <div class="tool-text">В предварительном просмотре не выводятся внутренние данные формулы, служебная трассировка, коммерческие эффекты или технические детали расчёта.</div>
        <div class="tool-note">Это демонстрационный режим, не production integration и не расчёт Formula Service.</div>
      </section>
    </div>
"""
