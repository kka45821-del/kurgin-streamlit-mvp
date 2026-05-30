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
    "report_number": "PREVIEW-MOCK",
}


FORM_FIELDS = (
    ("shape", "Shape", "Round"),
    ("carat", "Carat", "1.00"),
    ("color", "Color", "E"),
    ("clarity", "Clarity", "VS1"),
    ("table_pct", "Table %", "57.0"),
    ("depth_pct", "Depth %", "61.8"),
    ("crown_angle", "Crown angle", "34.7"),
    ("pavilion_angle", "Pavilion angle", "40.8"),
    ("crown_height", "Crown height %", "15.0"),
    ("pavilion_depth", "Pavilion depth %", "43.0"),
    ("girdle", "Girdle %", "3.5"),
    ("fluorescence", "Fluorescence", "None"),
    ("report_number", "Report #", "PREVIEW-MOCK"),
)


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
    return f"""
      <section class="single-next-box analyzer-preview-result" aria-label="KURGIN Stone Analyzer public-safe preview result">
        <div class="result-kicker">Public-safe preview/mock</div>
        <div class="result-title">{_escape(result.get('score_band'))}</div>
        <div class="result-text">{_escape(result.get('summary'))}</div>
        <div class="analyzer-result-grid" aria-label="Analyzer public-safe fields">
          <div><span>Status</span><strong>{_escape(result.get('status'))}</strong></div>
          <div><span>Score band</span><strong>{_escape(result.get('score_band'))}</strong></div>
          <div class="wide"><span>Summary</span><strong>{_escape(result.get('summary'))}</strong></div>
          <div class="wide"><span>Next action</span><strong>{_escape(next_action)}</strong></div>
        </div>
        <div class="analyzer-result-list"><strong>Warnings</strong><ul>{_list_items(warnings)}</ul></div>
        <div class="analyzer-result-list"><strong>Limitations</strong><ul>{_list_items(limitations)}</ul></div>
      </section>
"""


def render_analyzer_preview() -> str:
    preview_result = analyze_public_stone(DEFAULT_PUBLIC_INPUT)
    result_html = _render_public_safe_result(preview_result)
    form_fields = _render_form_fields()
    return f"""
    <div class="single-tool analyzer-preview">
      <div class="tool-section-title">KURGIN Stone Analyzer</div>
      <div class="muted">Public preview/mock для будущей Tools-интеграции. Live backend и Formula Service здесь не подключены.</div>

      <div class="analyzer-mode-row" aria-label="Analyzer modes">
        <div class="analyzer-mode active"><strong>Manual preview</strong><span>mock</span></div>
        <div class="analyzer-mode inactive"><strong>Upload</strong><span>later</span></div>
        <div class="analyzer-mode inactive"><strong>Batch</strong><span>later</span></div>
      </div>

      <section class="single-workspace analyzer-workspace">
        <div class="workspace-title">Manual public input</div>
        <div class="workspace-text">Форма показывает первый безопасный UI слой для ручного ввода. Сейчас это preview/mock: данные не отправляются в backend и не запускают реальный engine.</div>
        <div class="analyzer-preview-notice">Нет checkout, оплаты, заявки, резерва, batch upload или Excel upload. Внутренние поля формулы не показываются.</div>

        <form class="analyzer-form-grid" aria-label="KURGIN Stone Analyzer public preview form">
{form_fields}
        </form>

        <button type="button" class="single-file-button analyzer-mock-cta">Показать public-safe preview</button>
        <div class="analyzer-disabled-note">Результат ниже создан локальным preview/mock adapter и содержит только status, score_band, summary, warnings, limitations и next_action.</div>
      </section>

{result_html}

      <section class="tool-card">
        <div class="tool-kicker">Safety boundary</div>
        <div class="tool-title">Что скрыто</div>
        <div class="tool-text">В public preview не выводятся диагностика, breakdown, внутренние коэффициенты, formula internals, stack traces, price/order/reserve/payment effects.</div>
        <div class="tool-note">Это не production integration и не расчёт Formula Service.</div>
      </section>
    </div>
"""
