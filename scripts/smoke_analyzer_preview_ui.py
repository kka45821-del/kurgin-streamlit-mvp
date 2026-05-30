from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ui.pages.tools.analyzer_preview import render_analyzer_preview_controls
from ui.pages.tools_page import render_tools_page


REQUIRED_FRAGMENTS = [
    "KURGIN Stone Analyzer",
    "Фото",
    "камера",
    "Сфотографировать сертификат",
    "Загрузка",
    "файл",
    "Загрузить документ",
    "Вручную",
    "форма",
    "Анализ одного камня",
    "Базовые данные",
    "Геометрия",
    "Проверка данных",
    "Показать предварительный результат",
    "Статус анализа",
    "Класс результата",
    "Краткое резюме",
    "Предупреждения",
    "Ограничения",
    "Следующий шаг",
    "Задать вопрос по результату",
    "Подобрать похожий камень",
    "Сравнить с каталогом",
    "KURGIN Mass Analyzer",
    "Массовый анализ Excel",
    "Загрузить Excel",
    "Скачать шаблон",
    "Проверить файл",
    "Проверка шаблона",
    "Предпросмотр данных",
    "Запустить массовый анализ",
    "Таблица результатов",
    "Скачать результат Excel",
    "ready",
    "incomplete",
    "unsupported_shape",
    "invalid_input",
    "duplicate",
    "не выполняет расчёт",
    "не публикует данные",
    "не меняет каталог",
    "Не создаёт заказ, резерв или оплату",
    "ok",
    "engine_unavailable",
    "Не является сертификатом.",
    "Не является оценкой стоимости.",
    "Не является геммологическим заключением.",
]

FORBIDDEN_FRAGMENTS = [
    "Public preview/mock",
    "Manual public input",
    "Score band",
    "Next action",
    "Пакетный анализ",
    "Batch",
    "Excel upload",
    "PDF reports",
    "paid Analyzer",
    "subscription",
    "auth/pro roles",
    "payment",
    "reserve",
    "sold",
    "catalog publish",
    "supplier upload",
    "formula disclosure",
    "raw diagnostics",
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
    "payment_effect",
    "reserve_effect",
    "diagnostics",
    "breakdown",
    "triple_score",
    "structure_modifier",
    "raw JSON",
    "Купить по результату анализа",
    "Оплатить",
    "Зарезервировать",
    "Получить сертификат",
    "Оценить стоимость",
    "kurgin-score-analyzer",
]


def main() -> None:
    html = render_tools_page()
    stone_panel = html.split('data-tool-panel="kurgin_index"', 1)[0]
    for fragment in REQUIRED_FRAGMENTS:
        assert fragment in html, f"Missing Analyzer preview UI fragment: {fragment}"
    for fragment in FORBIDDEN_FRAGMENTS:
        if fragment in {"Пакетный анализ", "Batch", "Excel upload"}:
            assert fragment not in stone_panel, f"Forbidden Stone Analyzer fragment found: {fragment}"
        else:
            assert fragment not in html, f"Forbidden Analyzer preview UI fragment found: {fragment}"

    assert callable(render_analyzer_preview_controls), "Streamlit controls wrapper must be callable"
    assert render_analyzer_preview_controls.__name__ == "render_analyzer_preview_controls"
    print("Analyzer preview UI smoke checks passed.")


if __name__ == "__main__":
    main()
