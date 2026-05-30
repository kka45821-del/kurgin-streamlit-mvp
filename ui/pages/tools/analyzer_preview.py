import html

import streamlit as st

from services.analyzer_adapter import analyze_public_stone


DEFAULT_PUBLIC_INPUT = {
    "shape": "Round",
    "carat": 1.00,
    "color": "E",
    "clarity": "VS1",
    "lab": "IGI",
    "report_number": "PREVIEW-DEMO",
    "table_pct": 57.0,
    "depth_pct": 61.8,
    "crown_angle": 34.7,
    "pavilion_angle": 40.8,
    "crown_height": 15.0,
    "pavilion_depth": 43.0,
    "girdle": 3.5,
    "fluorescence": "None",
    "measurements": "6.43 x 6.47 x 3.97",
}


BASIC_FIELDS = (
    ("shape", "Форма", "Round"),
    ("carat", "Вес", "1.00"),
    ("color", "Цвет", "E"),
    ("clarity", "Чистота", "VS1"),
    ("lab", "Лаборатория", "IGI"),
    ("report_number", "Номер лабораторного документа / отчёта", "PREVIEW-DEMO"),
)

GEOMETRY_FIELDS = (
    ("table_pct", "Table %", "57.0"),
    ("depth_pct", "Depth %", "61.8"),
    ("crown_angle", "Crown angle", "34.7"),
    ("pavilion_angle", "Pavilion angle", "40.8"),
    ("crown_height", "Crown height %", "15.0"),
    ("pavilion_depth", "Pavilion depth %", "43.0"),
    ("girdle", "Girdle", "3.5"),
    ("fluorescence", "Fluorescence", "None"),
    ("measurements", "Measurements", "6.43 x 6.47 x 3.97"),
)

SAFE_STATUS_LABELS = (
    "ok",
    "incomplete",
    "invalid_input",
    "unsupported_shape",
    "engine_unavailable",
)

NEXT_ACTION_LABELS = {
    "request_professional_review": "Запросить профессиональную проверку",
    "fix_parameters": "Исправить параметры",
}


def _escape(value: object) -> str:
    return html.escape(str(value if value is not None else "—"), quote=True)


def _list_items(values: list[object]) -> str:
    if not values:
        return "<li>—</li>"
    return "".join(f"<li>{_escape(value)}</li>" for value in values)


def _next_action_label(value: object) -> str:
    return NEXT_ACTION_LABELS.get(str(value or "request_professional_review"), str(value or "request_professional_review"))


def _render_field_group(fields: tuple[tuple[str, str, str], ...]) -> str:
    rendered = []
    for key, label, placeholder in fields:
        value = DEFAULT_PUBLIC_INPUT.get(key, "")
        rendered.append(
            f"""
          <label class="analyzer-control analyzer-input">
            <span>{_escape(label)}</span>
            <input type="text" name="{_escape(key)}" value="{_escape(value)}" placeholder="{_escape(placeholder)}" aria-label="{_escape(label)}">
          </label>"""
        )
    return "".join(rendered)


def _render_public_safe_result(result: dict[str, object]) -> str:
    warnings = result.get("warnings") if isinstance(result.get("warnings"), list) else []
    limitations = result.get("limitations") if isinstance(result.get("limitations"), list) else []
    next_action_label = _next_action_label(result.get("next_action"))
    return f"""
      <section class="single-next-box analyzer-preview-result" aria-label="Предварительный публичный результат KURGIN Stone Analyzer">
        <div class="result-kicker">Проверка данных</div>
        <div class="result-title">{_escape(result.get('score_band'))}</div>
        <div class="result-text">{_escape(result.get('summary'))}</div>
        <div class="analyzer-result-grid" aria-label="Безопасные поля предварительного результата">
          <div><span>Статус анализа</span><strong>{_escape(result.get('status'))}</strong></div>
          <div><span>Класс результата</span><strong>{_escape(result.get('score_band'))}</strong></div>
          <div class="wide"><span>Краткое резюме</span><strong>{_escape(result.get('summary'))}</strong></div>
          <div class="wide"><span>Следующий шаг</span><strong>{_escape(next_action_label)}</strong></div>
        </div>
        <div class="analyzer-result-list"><strong>Предупреждения</strong><ul>{_list_items(warnings)}</ul></div>
        <div class="analyzer-result-list"><strong>Ограничения</strong><ul>{_list_items(limitations)}</ul></div>
      </section>
"""


def _render_safe_next_actions() -> str:
    actions = (
        "Задать вопрос по результату",
        "Подобрать похожий камень",
        "Сравнить с каталогом",
        "Начать новый анализ",
        "Исправить параметры",
    )
    return "".join(f"<button type='button' class='favoriteBtn'>{_escape(action)}</button>" for action in actions)


def _streamlit_result_block(result: dict[str, object]) -> None:
    warnings = result.get("warnings") if isinstance(result.get("warnings"), list) else []
    limitations = result.get("limitations") if isinstance(result.get("limitations"), list) else []

    st.caption("Проверка данных")
    col_a, col_b = st.columns(2)
    col_a.metric("Статус анализа", str(result.get("status", "—")))
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
    st.caption("Анализ одного камня. Расчётный контур не подключён в этой версии.")

    with st.form("kurgin_stone_analyzer_preview_form"):
        st.write("**Базовые данные**")
        shape = st.selectbox("Форма", ["Round", "Oval"], index=0)
        col_a, col_b = st.columns(2)
        with col_a:
            carat = st.number_input("Вес", min_value=0.0, value=float(DEFAULT_PUBLIC_INPUT["carat"]), step=0.01)
            color = st.text_input("Цвет", value=str(DEFAULT_PUBLIC_INPUT["color"]))
            clarity = st.text_input("Чистота", value=str(DEFAULT_PUBLIC_INPUT["clarity"]))
        with col_b:
            lab = st.text_input("Лаборатория", value=str(DEFAULT_PUBLIC_INPUT["lab"]))
            report_number = st.text_input("Номер лабораторного документа / отчёта", value=str(DEFAULT_PUBLIC_INPUT["report_number"]))

        st.write("**Геометрия**")
        col_c, col_d = st.columns(2)
        with col_c:
            table_pct = st.number_input("Table %", min_value=0.0, value=float(DEFAULT_PUBLIC_INPUT["table_pct"]), step=0.1)
            depth_pct = st.number_input("Depth %", min_value=0.0, value=float(DEFAULT_PUBLIC_INPUT["depth_pct"]), step=0.1)
            crown_angle = st.number_input("Crown angle", min_value=0.0, value=float(DEFAULT_PUBLIC_INPUT["crown_angle"]), step=0.1)
            pavilion_angle = st.number_input("Pavilion angle", min_value=0.0, value=float(DEFAULT_PUBLIC_INPUT["pavilion_angle"]), step=0.1)
        with col_d:
            crown_height = st.number_input("Crown height %", min_value=0.0, value=float(DEFAULT_PUBLIC_INPUT["crown_height"]), step=0.1)
            pavilion_depth = st.number_input("Pavilion depth %", min_value=0.0, value=float(DEFAULT_PUBLIC_INPUT["pavilion_depth"]), step=0.1)
            girdle = st.number_input("Girdle", min_value=0.0, value=float(DEFAULT_PUBLIC_INPUT["girdle"]), step=0.1)
            fluorescence = st.text_input("Fluorescence", value=str(DEFAULT_PUBLIC_INPUT["fluorescence"]))
            measurements = st.text_input("Measurements", value=str(DEFAULT_PUBLIC_INPUT["measurements"]))
        submitted = st.form_submit_button("Показать предварительный результат")

    public_input = {
        "shape": shape,
        "carat": carat,
        "color": color,
        "clarity": clarity,
        "lab": lab,
        "report_number": report_number,
        "table_pct": table_pct,
        "depth_pct": depth_pct,
        "crown_angle": crown_angle,
        "pavilion_angle": pavilion_angle,
        "crown_height": crown_height,
        "pavilion_depth": pavilion_depth,
        "girdle": girdle,
        "fluorescence": fluorescence,
        "measurements": measurements,
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
    basic_fields = _render_field_group(BASIC_FIELDS)
    geometry_fields = _render_field_group(GEOMETRY_FIELDS)
    safe_statuses = "".join(f"<span class='analyzer-status-pill'>{_escape(status)}</span>" for status in SAFE_STATUS_LABELS)
    next_actions = _render_safe_next_actions()
    return f"""
    <div class="single-tool analyzer-preview">
      <div class="tool-section-title">KURGIN Stone Analyzer</div>
      <div class="muted">Анализ одного камня помогает понять качество по параметрам. Он не заменяет лабораторный документ, не оценивает цену и не является сертификатом.</div>

      <div class="analyzer-mode-row" aria-label="Режимы анализа одного камня">
        <div class="analyzer-mode inactive"><strong>Фото</strong><span>камера</span><em>Сфотографировать сертификат · позже</em></div>
        <div class="analyzer-mode inactive"><strong>Загрузка</strong><span>файл</span><em>Загрузить документ · позже</em></div>
        <div class="analyzer-mode active"><strong>Вручную</strong><span>форма</span><em>Активный режим сейчас</em></div>
      </div>

      <section class="single-workspace analyzer-workspace">
        <div class="workspace-title">Анализ одного камня</div>
        <div class="workspace-text">Предварительная проверка качества по параметрам. Не сертификат, не оценка стоимости и не покупательский триггер.</div>
        <div class="analyzer-preview-notice">Расчётный контур не подключён в этой версии. Нет checkout, оплаты, заявки, резерва, пакетной загрузки или Excel-загрузки.</div>

        <div class="workspace-title">Базовые данные</div>
        <form class="analyzer-form-grid" aria-label="Базовые данные одного камня">
{basic_fields}
        </form>

        <div class="workspace-title">Геометрия</div>
        <form class="analyzer-form-grid" aria-label="Геометрия одного камня">
{geometry_fields}
        </form>

        <div class="workspace-title">Проверка данных</div>
        <div class="analyzer-status-row" aria-label="Безопасные статусы проверки данных">{safe_statuses}</div>
        <button type="button" class="single-file-button analyzer-mock-cta">Показать предварительный результат</button>
        <div class="analyzer-disabled-note">Результат ниже показан как пример безопасной публичной интерпретации качества одного камня.</div>
      </section>

{result_html}

      <section class="tool-card">
        <div class="tool-kicker">Дальше</div>
        <div class="tool-title">Безопасные следующие действия</div>
        <div class="favoriteActions">{next_actions}</div>
        <div class="tool-note">Действия показаны как UI skeleton. Они не создают покупку, оплату, резерв, заказ или сертификат.</div>
      </section>

      <section class="tool-card">
        <div class="tool-kicker">Контур безопасности</div>
        <div class="tool-title">Что скрыто</div>
        <div class="tool-text">В предварительном просмотре не выводятся внутренние данные формулы, служебная трассировка, коммерческие эффекты или технические детали расчёта.</div>
        <div class="tool-note">Это демонстрационный режим, не production integration и не расчёт Formula Service.</div>
      </section>
    </div>
"""
