import html

import streamlit as st

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


def _next_action_label(value: object) -> str:
    return NEXT_ACTION_LABELS.get(str(value or "request_professional_review"), str(value or "request_professional_review"))


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
    next_action_label = _next_action_label(result.get("next_action"))
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


def _streamlit_result_block(result: dict[str, object]) -> None:
    warnings = result.get("warnings") if isinstance(result.get("warnings"), list) else []
    limitations = result.get("limitations") if isinstance(result.get("limitations"), list) else []

    st.caption("Демонстрационный режим")
    col_a, col_b = st.columns(2)
    col_a.metric("Состояние", str(result.get("status", "—")))
    col_b.metric("Класс результата", str(result.get("score_band", "—")))
    st.write(str(result.get("summary", "—")))
    st.write("**Следующий шаг:** " + _next_action_label(result.get("next_action")))

    st.write("**Предупреждения**")
    if warnings:
        for warning in warnings:
            st.write(f"- {warning}")
    else:
        st.write("- —")

    st.write("**Ограничения**")
    for limitation in limitations:
        st.write(f"- {limitation}")


def render_analyzer_preview_controls() -> dict[str, object]:
    """Optional Streamlit-controls wrapper for a future non-iframe Tools page.

    The current MVP shell renders Tools as an HTML iframe via components.html,
    so this function is intentionally not called by the active shell yet. It is
    ready for a future Streamlit-native Tools layer and uses the same local
    preview adapter without live backend calls.
    """
    st.subheader("KURGIN Stone Analyzer")
    st.caption("Демонстрационный режим. Расчётный контур не подключён в этой версии.")

    with st.form("kurgin_stone_analyzer_preview_form"):
        shape = st.selectbox("Огранка", ["Round", "Oval"], index=0)
        col_a, col_b = st.columns(2)
        with col_a:
            carat = st.number_input("Каратность", min_value=0.0, value=float(DEFAULT_PUBLIC_INPUT["carat"]), step=0.01)
            color = st.text_input("Цвет", value=str(DEFAULT_PUBLIC_INPUT["color"]))
            clarity = st.text_input("Чистота", value=str(DEFAULT_PUBLIC_INPUT["clarity"]))
            table_pct = st.number_input("Площадка, %", min_value=0.0, value=float(DEFAULT_PUBLIC_INPUT["table_pct"]), step=0.1)
            depth_pct = st.number_input("Глубина, %", min_value=0.0, value=float(DEFAULT_PUBLIC_INPUT["depth_pct"]), step=0.1)
            crown_angle = st.number_input("Угол короны", min_value=0.0, value=float(DEFAULT_PUBLIC_INPUT["crown_angle"]), step=0.1)
        with col_b:
            pavilion_angle = st.number_input("Угол павильона", min_value=0.0, value=float(DEFAULT_PUBLIC_INPUT["pavilion_angle"]), step=0.1)
            crown_height = st.number_input("Высота короны, %", min_value=0.0, value=float(DEFAULT_PUBLIC_INPUT["crown_height"]), step=0.1)
            pavilion_depth = st.number_input("Глубина павильона, %", min_value=0.0, value=float(DEFAULT_PUBLIC_INPUT["pavilion_depth"]), step=0.1)
            girdle = st.number_input("Рундист, %", min_value=0.0, value=float(DEFAULT_PUBLIC_INPUT["girdle"]), step=0.1)
            fluorescence = st.text_input("Флуоресценция", value=str(DEFAULT_PUBLIC_INPUT["fluorescence"]))
            report_number = st.text_input("Номер отчёта", value=str(DEFAULT_PUBLIC_INPUT["report_number"]))
        submitted = st.form_submit_button("Показать предварительную проверку")

    public_input = {
        "shape": shape,
        "carat": carat,
        "color": color,
        "clarity": clarity,
        "table_pct": table_pct,
        "depth_pct": depth_pct,
        "crown_angle": crown_angle,
        "pavilion_angle": pavilion_angle,
        "crown_height": crown_height,
        "pavilion_depth": pavilion_depth,
        "girdle": girdle,
        "fluorescence": fluorescence,
        "report_number": report_number,
    }
    result = analyze_public_stone(public_input)
    if submitted:
        _streamlit_result_block(result)
    else:
        st.info("Заполните параметры и нажмите кнопку предварительной проверки.")
    return result


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
