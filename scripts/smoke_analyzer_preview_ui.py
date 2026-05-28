from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ui.pages.tools_page import render_tools_page


REQUIRED_FRAGMENTS = [
    "Это adapter stub preview",
    "Реальная формула не подключена",
    "Показать mock preview",
    "Adapter stub preview",
    "Mock result по public adapter contract",
    "Status",
    "Score band",
    "Summary",
    "Warnings",
    "Limitations",
    "Next action",
    "Не является сертификатом.",
    "Не является оценкой стоимости.",
    "Не является геммологическим заключением.",
]

FORBIDDEN_FRAGMENTS = [
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
