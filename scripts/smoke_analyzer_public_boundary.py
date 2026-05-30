from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ui.pages.tools_page import render_tools_page


FORBIDDEN_PUBLIC_FRAGMENTS = [
    "raw_formula",
    "weights",
    "penalty_breakdown",
    "internal_diagnostics",
    "debug_trace",
    "traceback",
    "raw_engine_output",
    "formula_source",
    "certificate_claim",
    "appraisal_claim",
    "price_effect",
    "payment_effect",
    "reserve_effect",
    "order_effect",
    "diagnostics",
    "breakdown",
    "triple_score",
    "structure_modifier",
]

FORBIDDEN_IMPORT_ROOTS = {
    "core_formula",
    "formula_client",
    "formula_modules",
    "kurgin_core",
    "excel_tools",
    "kurgin_score_analyzer",
}

SCAN_TARGETS = [
    ROOT / "app.py",
    ROOT / "catalog",
    ROOT / "config",
    ROOT / "services",
    ROOT / "scripts",
    ROOT / "ui",
]


def _python_files() -> list[Path]:
    files: list[Path] = []
    for target in SCAN_TARGETS:
        if target.is_file() and target.suffix == ".py":
            files.append(target)
        elif target.is_dir():
            files.extend(sorted(target.rglob("*.py")))
    return files


def _module_root(module_name: str | None) -> str:
    return (module_name or "").split(".", 1)[0]


def _check_forbidden_imports() -> None:
    violations: list[str] = []
    for file_path in _python_files():
        tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=str(file_path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = _module_root(alias.name)
                    if root in FORBIDDEN_IMPORT_ROOTS:
                        violations.append(f"{file_path.relative_to(ROOT)}:{node.lineno}: import {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                root = _module_root(node.module)
                if root in FORBIDDEN_IMPORT_ROOTS:
                    violations.append(f"{file_path.relative_to(ROOT)}:{node.lineno}: from {node.module} import ...")
    assert not violations, "Forbidden private Analyzer/formula imports found:\n" + "\n".join(violations)


def _check_public_html_boundary() -> None:
    html = render_tools_page()
    for fragment in FORBIDDEN_PUBLIC_FRAGMENTS:
        assert fragment not in html, f"Forbidden public Analyzer fragment leaked into Tools HTML: {fragment}"


def main() -> None:
    _check_forbidden_imports()
    _check_public_html_boundary()
    print("Analyzer public boundary smoke checks passed.")


if __name__ == "__main__":
    main()
