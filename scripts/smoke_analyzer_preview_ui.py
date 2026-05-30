from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ui.pages.tools_page import render_tools_page


REQUIRED_FRAGMENTS = [
    "KURGIN Stone Analyzer",
    "Предварительная проверка параметров",
    "Расчётный контур не подключён в этой версии.",
    "Ручной ввод параметров",
    "Форма предварительной проверки KURGIN Stone Analyzer",
    "Огранка",
    "Каратность",
    "Цвет",
    "Чистота",
    "Площадка, %",
    "Глубина, %",
    "Угол короны",
    "Угол павильона",
    "Высота короны, %",
    "Глубина павильона, %",
    "Рундист, %",
    "Флуоресценция",
    "Номер отчёта",
    "Демонстрационный режим",
    "Состояние",
    "Класс результата",
    "Пояснение",
    "Предупреждения",
    "Ограничения",
    "Следующий шаг",
    "Запросить профессиональную проверку",
    "Не является сертификатом.",
    "Не является оценкой стоимости.",
    "Не является геммологическим заключением.",
    "Это демонстрационный режим, не production integration и не расчёт Formula Service.",
]

FORBIDDEN_FRAGMENTS = [
    "Public preview/mock",
    "Manual public input",
    "Score band",
    "Next action",
    "raw_formula",
    "weights",
    "penalty_breakdown",
    "internal_diagnostics",
    "debug_trace",
    "traceback",
    "raw_engine_output",
    "formula_source",
    "coefficient_formula",
    "certificate_claim",
    "appraisal_claim",
    "price_effect",
    "order_effect",
    "reserve_effect",
    "payment_effect",
    "diagnostics",
    "breakdown",
    "triple_score",
    "structure_modifier",
    "raw JSON",
    "kurgin-score-analyzer",
]


def main() -> None:
    html = render_tools_page()
    for fragment in REQUIRED_FRAGMENTS:
        assert fragment in html, f"Missing Analyzer preview UI fragment: {fragment}"
    for fragment in FORBIDDEN_FRAGMENTS:
        assert fragment not in html, f"Forbidden Analyzer preview UI fragment found: {fragment}"
    print("Analyzer preview UI smoke checks passed.")


if __name__ == "__main__":
    main()
