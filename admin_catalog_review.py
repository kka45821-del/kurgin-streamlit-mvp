import json
from datetime import datetime, timezone
from io import BytesIO

import pandas as pd
import streamlit as st

from catalog.catalog_core import RULE_LIBRARY, admin_section_rules, import_diagnostics, normalize_stone

st.set_page_config(page_title="KURGIN Catalog Admin", page_icon="◇", layout="wide")

RULE_LABELS = {**RULE_LIBRARY, "price_warning": "Цена не заполнена"}

COLUMN_MAP = {
    "SR NO": "source_row", "NO": "source_row", "№": "source_row",
    "Stock #": "stone_id", "Stock": "stone_id", "ID": "stone_id",
    "REPORT NO": "report_number", "Report No": "report_number", "Report #": "report_number", "Report": "report_number", "Certificate": "report_number",
    "DESCRIPTION": "shape", "Description": "shape", "Shape": "shape",
    "LAB": "lab", "Lab": "lab", "TYPE": "growth_method", "Type": "growth_method",
    "COLOR": "color", "Color": "color", "CLARITY": "clarity", "Clarity": "clarity",
    "WEIGHT": "carat", "Weight": "carat", "Carat": "carat",
    "PCS/CTS": "quantity", "PCS": "quantity", "Quantity": "quantity", "Qty": "quantity",
    "RATE": "supplier_rate", "TOTAL AMT": "supplier_total",
    "Availability": "availability", "Status": "availability",
    "Cut": "cut", "Polish": "polish", "Symmetry": "symmetry", "Fluorescence": "fluorescence",
    "Measurements": "measurements", "Diameter": "diameter", "DiameterMM": "diameter_mm", "Size MM": "size_mm",
    "Section": "section", "Catalog Section": "section", "Is Colored": "is_colored",
    "Color Type": "color_type", "Color Hue": "color_hue", "Color Intensity": "color_intensity",
    "Pair ID": "pair_id", "Side Type": "side_type",
    "price_rub": "price_rub", "Price RUB": "price_rub", "Public Price RUB": "public_price_rub",
    "karo_score": "karo_score", "Karo Score": "karo_score", "KARO SCORE": "karo_score",
    "kurgin_score": "karo_score", "Kurgin Score": "karo_score", "KURGIN SCORE": "karo_score", "KURGIN Score": "karo_score",
    "Currency": "currency", "Price Date": "price_date", "Supplier": "supplier_name", "Supplier Name": "supplier_name",
    "Source": "source", "Upload Date": "upload_date", "show_in_catalog": "show_in_catalog", "Show In Catalog": "show_in_catalog",
    "tag1": "tag1", "tag2": "tag2", "tag3": "tag3", "tag4": "tag4", "tag5": "tag5", "tag6": "tag6",
}
NUMERIC_FIELDS = {"carat", "price_rub", "public_price_rub", "karo_score", "diameter", "diameter_mm", "size_mm", "quantity", "supplier_rate", "supplier_total"}
STATUS_OPTIONS = {"Все": "all", "Все проблемные": "problem", "Заблокированные": "blocked", "С предупреждениями": "warning", "Готовые": "ready"}
TEMPLATE_COLUMNS = ["stone_id", "availability", "section", "shape", "carat", "size_mm", "quantity", "color", "clarity", "cut", "polish", "symmetry", "fluorescence", "measurements", "lab", "report_number", "price_rub", "karo_score", "is_colored", "color_type", "pair_id", "side_type", "supplier_name", "upload_date", "show_in_catalog", "tag1", "tag2", "tag3", "tag4", "tag5", "tag6"]


def template_bytes() -> bytes:
    out = BytesIO()
    example = [{"stone_id": "KRG-001", "availability": "available", "section": "main", "shape": "Round", "carat": 1.25, "size_mm": "", "quantity": 1, "color": "F", "clarity": "VS1", "cut": "EX", "polish": "EX", "symmetry": "VG", "fluorescence": "none", "measurements": "6.85x6.88x4.20", "lab": "IGI", "report_number": "LG000000", "price_rub": "", "karo_score": 92, "is_colored": False, "color_type": "", "pair_id": "", "side_type": "", "supplier_name": "", "upload_date": "", "show_in_catalog": True, "tag1": "", "tag2": "", "tag3": "", "tag4": "", "tag5": "", "tag6": ""}]
    rules = pd.DataFrame([
        {"section": "main", "required": "carat, color, clarity, report, Karo Score для Round", "warning": "price, measurements, finish, fluorescence"},
        {"section": "large", "required": "carat, color, clarity, report, Karo Score для Round", "warning": "price, measurements, finish, fluorescence"},
        {"section": "small", "required": "size_mm или carat, quantity", "warning": "price, report, Karo Score"},
        {"section": "colored", "required": "size_mm или carat, color_type", "warning": "price, report, Karo Score"},
        {"section": "pairs", "required": "size_mm или carat, quantity, pair_id", "warning": "price, report, Karo Score"},
        {"section": "side", "required": "size_mm или carat, quantity, side_type", "warning": "price, report, Karo Score"},
    ])
    with pd.ExcelWriter(out, engine="openpyxl") as writer:
        pd.DataFrame(example, columns=TEMPLATE_COLUMNS).to_excel(writer, sheet_name="KURGIN_Template", index=False)
        pd.DataFrame(columns=TEMPLATE_COLUMNS).to_excel(writer, sheet_name="Empty_Template", index=False)
        rules.to_excel(writer, sheet_name="Rules", index=False)
    return out.getvalue()


def clean_cell(value):
    if pd.isna(value):
        return None
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return value


def coerce_value(key, value):
    value = clean_cell(value)
    if key in NUMERIC_FIELDS and value is not None:
        try:
            return float(str(value).replace(" ", "").replace(",", "."))
        except (TypeError, ValueError):
            return value
    return value


def normalize_header(value):
    return " ".join(str(value).strip().upper().split()) if value not in (None, "") and not pd.isna(value) else ""


def resolve_column(column) -> str:
    raw_col = str(column).strip()
    return COLUMN_MAP.get(raw_col) or COLUMN_MAP.get(normalize_header(raw_col)) or raw_col


def column_mapping_report(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    for column in df.columns:
        raw_col = str(column).strip()
        normalized_col = normalize_header(raw_col)
        mapped = COLUMN_MAP.get(raw_col) or COLUMN_MAP.get(normalized_col)
        rows.append({
            "Excel column": raw_col,
            "Normalized": normalized_col,
            "Mapped field": mapped or "",
            "Recognized": bool(mapped),
        })
    report = pd.DataFrame(rows)
    return report[report["Recognized"]].copy(), report[~report["Recognized"]].copy()


def detect_header_row(df: pd.DataFrame) -> int | None:
    known = {normalize_header(k) for k in COLUMN_MAP.keys()}
    for idx, row in df.head(80).iterrows():
        hits = sum(1 for cell in row.tolist() if normalize_header(cell) in known)
        if hits >= 4:
            return idx
    return None


def read_excel_smart(uploaded, sheet_name: str) -> pd.DataFrame:
    uploaded.seek(0)
    raw = pd.read_excel(uploaded, sheet_name=sheet_name, header=None)
    header_row = detect_header_row(raw)
    uploaded.seek(0)
    if header_row is None:
        return pd.read_excel(uploaded, sheet_name=sheet_name)
    df = pd.read_excel(uploaded, sheet_name=sheet_name, header=header_row)
    df = df.dropna(how="all").dropna(axis=1, how="all")
    return df


def dataframe_to_raw_stones(df: pd.DataFrame) -> list[dict]:
    rows = []
    for _, row in df.iterrows():
        item = {}
        for col in df.columns:
            target = resolve_column(col)
            item[target] = coerce_value(target, row.get(col))
        if any(v not in (None, "") for v in item.values()) and not str(item.get("source_row", "")).lower().startswith("total"):
            rows.append(item)
    return rows


def review_normalize(raw: dict) -> dict:
    s = normalize_stone(raw)
    errors = list(s.get("blocking_errors", []))
    warnings = list(s.get("warnings", []))
    if "price_required" in errors:
        errors.remove("price_required")
        if "price_warning" not in warnings:
            warnings.insert(0, "price_warning")
    s["blocking_errors"] = errors
    s["warnings"] = warnings
    s["publication_status"] = "blocked" if errors else "warning" if warnings else "ready"
    return s


def labels(keys):
    return ", ".join(RULE_LABELS.get(k, k) for k in keys)


def review_table(raw_stones):
    data = []
    for raw in raw_stones:
        s = review_normalize(raw)
        data.append({"ID": s.get("id"), "Раздел": s.get("section"), "Статус": s.get("publication_status"), "Форма": s.get("shape"), "Карат": s.get("carat"), "Цвет": s.get("color"), "Чистота": s.get("clarity"), "Цена": s.get("price"), "KURGIN Score": s.get("score"), "Report": s.get("report"), "Meta": s.get("meta"), "Блокирующие ошибки": labels(s.get("blocking_errors", [])), "Предупреждения": labels(s.get("warnings", []))})
    return pd.DataFrame(data)


def diagnostics_from_review(df: pd.DataFrame):
    return {"total": len(df), "ready": int((df["Статус"] == "ready").sum()), "warning": int((df["Статус"] == "warning").sum()), "blocked": int((df["Статус"] == "blocked").sum())}


def filtered_review(df, status, section, query):
    view = df.copy()
    if status == "problem":
        view = view[view["Статус"].isin(["blocked", "warning"])]
    elif status != "all":
        view = view[view["Статус"] == status]
    if section != "Все разделы":
        view = view[view["Раздел"] == section]
    query = (query or "").strip().lower()
    if query:
        text = view.fillna("").astype(str).agg(" ".join, axis=1).str.lower()
        view = view[text.str.contains(query, regex=False)]
    return view


def public_review_stones(raw_stones):
    return [s for s in (review_normalize(x) for x in raw_stones if isinstance(x, dict)) if not s.get("blocking_errors")]


st.title("KURGIN Catalog Admin")
st.caption("Предпубликационная проверка Excel / JSON перед отправкой в catalog.json")
st.download_button("Скачать пустой Excel-шаблон", data=template_bytes(), file_name="KURGIN_catalog_template.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

with st.expander("Правила публикации по разделам", expanded=False):
    for section, rules in admin_section_rules().items():
        st.markdown(f"### {section}")
        left, right = st.columns(2)
        left.write("Блокирующие правила")
        for rule in rules["blocking"]:
            left.write(f"- {rule['label']}")
        right.write("Предупреждения")
        for rule in rules["warnings"]:
            right.write(f"- {rule['label']}")

uploaded = st.file_uploader("Загрузите Excel или JSON каталога", type=["xlsx", "xls", "json"])
if not uploaded:
    st.info("Загрузите файл, чтобы увидеть готовые к публикации камни, ошибки и предупреждения.")
    st.stop()

recognized_columns = pd.DataFrame()
unrecognized_columns = pd.DataFrame()

try:
    if uploaded.name.lower().endswith(".json"):
        payload = json.loads(uploaded.getvalue().decode("utf-8"))
        raw_stones = payload if isinstance(payload, list) else payload.get("stones") or payload.get("catalog") or payload.get("items") or payload.get("data") or []
    else:
        xls = pd.ExcelFile(uploaded)
        sheet = st.selectbox("Лист Excel", xls.sheet_names, index=min(1, len(xls.sheet_names)-1))
        source_df = read_excel_smart(uploaded, sheet)
        recognized_columns, unrecognized_columns = column_mapping_report(source_df)
        raw_stones = dataframe_to_raw_stones(source_df)
except Exception as exc:
    st.error(f"Не удалось прочитать файл: {exc}")
    st.stop()

if not raw_stones:
    st.warning("В файле не найдено строк камней.")
    st.stop()

if not recognized_columns.empty or not unrecognized_columns.empty:
    with st.expander("Контроль колонок импорта", expanded=True):
        c1, c2 = st.columns(2)
        c1.metric("Распознано колонок", len(recognized_columns))
        c2.metric("Не распознано колонок", len(unrecognized_columns))
        if not unrecognized_columns.empty:
            st.warning("Есть нераспознанные колонки. Проверь, не потерялись ли важные данные поставщика.")
            st.dataframe(unrecognized_columns[["Excel column", "Normalized"]], use_container_width=True)
        with st.expander("Распознанные колонки", expanded=False):
            st.dataframe(recognized_columns[["Excel column", "Mapped field"]], use_container_width=True)

df = review_table(raw_stones)
public_stones = public_review_stones(raw_stones)
summary = diagnostics_from_review(df)
section_df = df.groupby("Раздел")["Статус"].value_counts().unstack(fill_value=0).reset_index()
for col in ["ready", "warning", "blocked"]:
    if col not in section_df.columns:
        section_df[col] = 0
section_df["total"] = section_df[["ready", "warning", "blocked"]].sum(axis=1)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Всего строк", summary["total"])
c2.metric("Готово", summary["ready"])
c3.metric("С предупреждениями", summary["warning"])
c4.metric("Заблокировано", summary["blocked"])

st.subheader("По разделам")
st.dataframe(section_df[["Раздел", "total", "ready", "warning", "blocked"]], use_container_width=True)
st.subheader("Проверка камней")
f1, f2, f3 = st.columns([1.2, 1.2, 2])
status_label = f1.selectbox("Статус", list(STATUS_OPTIONS.keys()), index=1)
section_filter = f2.selectbox("Раздел", ["Все разделы"] + sorted(df["Раздел"].dropna().unique().tolist()))
search = f3.text_input("Поиск по ID / Report / ошибкам", "")
view = filtered_review(df, STATUS_OPTIONS[status_label], section_filter, search)
st.caption(f"Показано строк: {len(view)} из {len(df)}")
st.dataframe(view, use_container_width=True)

blocked, warning, ready = st.tabs(["Заблокированные", "Предупреждения", "Готовые"])
blocked.dataframe(df[df["Статус"] == "blocked"], use_container_width=True)
warning.dataframe(df[df["Статус"] == "warning"], use_container_width=True)
ready.dataframe(df[df["Статус"] == "ready"], use_container_width=True)

catalog_payload = {"source": "KURGIN Admin Review", "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "count": len(public_stones), "stones": public_stones}
st.download_button("Скачать catalog.json для публикации", data=json.dumps(catalog_payload, ensure_ascii=False, indent=2).encode("utf-8"), file_name="catalog.json", mime="application/json", disabled=not public_stones)

if summary["blocked"]:
    st.warning("Есть заблокированные строки. В скачиваемый catalog.json они не попадут.")
else:
    st.success("Блокирующих ошибок нет. Каталог можно публиковать.")
