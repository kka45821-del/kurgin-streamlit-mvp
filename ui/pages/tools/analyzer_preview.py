import html

from services.analyzer_adapter import analyze_public_stone


def _escape(value: object) -> str:
    return html.escape(str(value if value is not None else "—"), quote=True)


def _preview_payload() -> dict[str, object]:
    return {
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
        "report_number": "PREVIEW-STUB",
    }


def _list_items(values: list[object]) -> str:
    if not values:
        return "<li>—</li>"
    return "".join(f"<li>{_escape(value)}</li>" for value in values)


def _render_adapter_mock_result(result: dict[str, object]) -> str:
    warnings = result.get("warnings") if isinstance(result.get("warnings"), list) else []
    limitations = result.get("limitations") if isinstance(result.get("limitations"), list) else []
    return f"""
<details class="analyzer-adapter-preview">
  <summary>Показать mock preview</summary>
  <div class="analyzer-result-grid" aria-label="Analyzer adapter mock result">
    <div><span>Status</span><strong>{_escape(result.get('status'))}</strong></div>
    <div><span>Score band</span><strong>{_escape(result.get('score_band'))}</strong></div>
    <div class="wide"><span>Summary</span><strong>{_escape(result.get('summary'))}</strong></div>
    <div class="wide"><span>Next action</span><strong>{_escape(result.get('next_action'))}</strong></div>
  </div>
  <div class="analyzer-result-list"><strong>Warnings</strong><ul>{_list_items(warnings)}</ul></div>
  <div class="analyzer-result-list"><strong>Limitations</strong><ul>{_list_items(limitations)}</ul></div>
</details>
"""


def render_analyzer_preview() -> str:
    adapter_mock_result = analyze_public_stone(_preview_payload())
    adapter_mock_result_html = _render_adapter_mock_result(adapter_mock_result)
    return f"""
    <div class="single-tool analyzer-preview">
      <div class="tool-section-title">KURGIN Stone Analyzer</div>
      <div class="muted">Это adapter stub preview. Реальная формула не подключена: расчёт, формула, загрузка файлов и отчёты сейчас не выполняются.</div>

      <div class="analyzer-mode-row" aria-label="Analyzer modes">
        <div class="analyzer-mode active"><strong>Manual preview</strong><span>phase 1</span></div>
        <div class="analyzer-mode inactive"><strong>Upload</strong><span>later</span></div>
        <div class="analyzer-mode inactive"><strong>Batch</strong><span>later</span></div>
      </div>

      <section class="single-workspace analyzer-workspace">
        <div class="workspace-title">Manual adapter preview</div>
        <div class="workspace-text">Поля ниже показывают будущую структуру ручного ввода. Данные не отправляются в backend и не запускают реальный engine.</div>
        <div class="analyzer-preview-notice">Форма показана как preview. Данные не отправляются и расчёт не выполняется.</div>

        <div class="analyzer-form-grid" aria-label="KURGIN Stone Analyzer preview form">
          <label class="analyzer-control analyzer-select"><span>Shape</span><select disabled aria-label="Shape preview"><option>Round</option></select></label>
          <label class="analyzer-control analyzer-input"><span>Carat</span><input type="text" value="1.00 ct" disabled readonly aria-label="Carat preview"></label>
          <label class="analyzer-control analyzer-select"><span>Color</span><select disabled aria-label="Color preview"><option>E</option></select></label>
          <label class="analyzer-control analyzer-select"><span>Clarity</span><select disabled aria-label="Clarity preview"><option>VS1</option></select></label>
          <label class="analyzer-control analyzer-input optional"><span>Table %</span><input type="text" value="57.0" disabled readonly aria-label="Table percentage preview"></label>
          <label class="analyzer-control analyzer-input optional"><span>Depth %</span><input type="text" value="61.8" disabled readonly aria-label="Depth percentage preview"></label>
          <label class="analyzer-control analyzer-input optional"><span>Crown angle</span><input type="text" value="34.7" disabled readonly aria-label="Crown angle preview"></label>
          <label class="analyzer-control analyzer-input optional"><span>Pavilion angle</span><input type="text" value="40.8" disabled readonly aria-label="Pavilion angle preview"></label>
        </div>

        <button type="button" class="single-file-button analyzer-mock-cta">Показать mock preview</button>
        <div class="analyzer-disabled-note">Результат ниже создан через public-safe adapter stub. Реальная формула не подключена.</div>
      </section>

      <section class="single-next-box analyzer-preview-result">
        <div class="result-kicker">Adapter stub preview</div>
        <div class="result-title">Mock result по public adapter contract</div>
        <div class="result-text">Это не настоящий расчёт. UI показывает только безопасные поля: status, score_band, summary, warnings, limitations и next_action.</div>
        {adapter_mock_result_html}
        <ul class="analyzer-limitations">
          <li>Не является сертификатом.</li>
          <li>Не является оценкой стоимости.</li>
          <li>Не является геммологическим заключением.</li>
          <li>Формула и внутренние коэффициенты не раскрываются.</li>
        </ul>
      </section>
    </div>
"""
