import json
from datetime import datetime, timezone

import pandas as pd
import streamlit as st

from catalog.catalog_core import RULE_LIBRARY, admin_section_rules, import_diagnostics, normalize_public_stones, normalize_stone

st.set_page_config(page_title="KURGIN Catalog Admin", page_icon="◇", layout="wide")

COLUMN_MAP = {
    "Stock #": "stone_id", "Stock": "stone_id", "ID": "stone_id",
    "Availability": "availability", "Status": "availability",
    "Shape": "shape", "Weight": "carat", "Carat": "carat",
    "Color": "color", "Clarity": "clarity", "Cut": "cut", "Polish": "polish", "Symmetry": "symmetry",
    "Fluorescence": "fluorescence", "Measurements": "measurements", "Diameter": "diameter", "DiameterMM": "diameter_mm",
    "Size MM": "size_mm", "Quantity": "quantity", "Qty": "quantity",
    "Lab": "lab", "Report #": "report_number", "Report": "report_number", "Certificate": "report_number",
    "Section": "section", "Catalog Section": "section", "Is Colored": "is_colored",
    "Color Type": "color_type", "Color Hue": "color_hue", "Color Intensity": "color_intensity",
    "Pair ID": "pair_id", "Side Type": "side_type",
    "price_rub": "price_rub", "Price RUB": "price_rub", "Public Price RUB": "public_price_rub",
    "karo_score": "karo_score", "Karo Score": "karo_score",
    "Currency": "currency", "Price Date": "price_date", "Supplier": "supplier_name", "Supplier Name": "supplier_name",
    "Source": "source", "Upload Date": "upload_date", "show_in_catalog": "show_in_catalog", "Show In Catalog": "show_in_catalog",
    "tag1": "tag1", "tag2": "tag2", "tag3": "tag3", "tag4": "tag4", "tag5": "tag5", "tag6": "tag6",
}
NUMERIC_FIELDS = {"carat", "price_rub", "public_price_rub", "karo_score", "diameter", "diameter_mm", "size_mm", "quantity"}
STATUS_OPTIONS = {"Все": "all", "Все проблемные": "problem", "Заблокированные": "blocked", "С предупреждениями": "warning", "Готовые": "ready"}


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


def dataframe_to_raw_stones(df: pd.DataFrame) -> list[dict]:
    rows = []
    for _, row in df.iterrows():
        item = {COLUMN_MAP.get(str(col).strip(), str(col).strip()): coerce_value(COLUMN_MAP.get(str(col).strip(), str(col).strip()), row.get(col)) for col in df.columns}
        if any(value not in (None, "") for value in item.values()):
            rows.append(item)
    return rows


def labels(keys):
    return ", ".join(RULE_LIBRARY.get(key, key) for key in keys)


def review_table(raw_stones: list[dict]) -> pd.DataFrame:
    result = []
    for raw in raw_stones:
        s = normalize_stone(raw)
        result.append({
            "ID": s.get("id"), "Раздел": s.get("section"), "Статус": s.get("publication_status"),
            "Форма": s.get("shape"), "Карат": s.get("carat"), "Цвет": s.get("color"), "Чистота": s.get("clarity"),
            "Цена": s.get("price"), "Karo Score": s.get("score"), "Report": s.get("report"), "Meta": s.get("meta"),
            "Блокирующие ошибки": labels(s.get("blocking_errors", [])), "Предупреждения": labels(s.get("warnings", [])),
        })
    return pd.DataFrame(result)


def filtered_review(df: pd.DataFrame, status: str, section: str, query: str) -> pd.DataFrame:
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


def count_table(counts: dict) -> pd.DataFrame:
    return pd.DataFrame([{"Правило": RULE_LIBRARY.get(key, key), "Количество": value} for key, value in counts.items()])


st.title("KURGIN Catalog Admin")
st.caption("Предпубликационная проверка Excel / JSON перед отправкой в catalog.json")

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

try:
    if uploaded.name.lower().endswith(".json"):
        payload = json.loads(uploaded.getvalue().decode("utf-8"))
        raw_stones = payload if isinstance(payload, list) else payload.get("stones") or payload.get("catalog") or payload.get("items") or payload.get("data") or []
    else:
        xls = pd.ExcelFile(uploaded)
        sheet = st.selectbox("Лист Excel", xls.sheet_names)
        raw_stones = dataframe_to_raw_stones(pd.read_excel(uploaded, sheet_name=sheet))
except Exception as exc:
    st.error(f"Не удалось прочитать файл: {exc}")
    st.stop()

if not raw_stones:
    st.warning("В файле не найдено строк камней.")
    st.stop()

diagnostics = import_diagnostics(raw_stones)
public_stones = normalize_public_stones(raw_stones)
df = review_table(raw_stones)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Всего строк", diagnostics["total"])
c2.metric("Готово", diagnostics["ready"])
c3.metric("С предупреждениями", diagnostics["warning"])
c4.metric("Заблокировано", diagnostics["blocked"])

st.subheader("По разделам")
section_rows = [{"Раздел": section, **values} for section, values in diagnostics["by_section"].items()]
st.dataframe(pd.DataFrame(section_rows), use_container_width=True)

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

if diagnostics["blocking_rules"]:
    st.subheader("Частые блокирующие ошибки")
    st.dataframe(count_table(diagnostics["blocking_rules"]), use_container_width=True)
if diagnostics["warning_rules"]:
    st.subheader("Частые предупреждения")
    st.dataframe(count_table(diagnostics["warning_rules"]), use_container_width=True)

catalog_payload = {"source": "KURGIN Admin Review", "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "count": len(public_stones), "stones": public_stones}
st.download_button("Скачать catalog.json для публикации", data=json.dumps(catalog_payload, ensure_ascii=False, indent=2).encode("utf-8"), file_name="catalog.json", mime="application/json", disabled=not public_stones)

if diagnostics["blocked"]:
    st.warning("Есть заблокированные строки. В скачиваемый catalog.json они не попадут.")
else:
    st.success("Блокирующих ошибок нет. Каталог можно публиковать.")
