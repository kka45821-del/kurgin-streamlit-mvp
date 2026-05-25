import json
from datetime import datetime, timezone

import pandas as pd
import streamlit as st

from catalog.catalog_core import (
    RULE_LIBRARY,
    admin_section_rules,
    import_diagnostics,
    normalize_public_stones,
    normalize_stone,
)

st.set_page_config(
    page_title="KURGIN Catalog Admin",
    page_icon="◇",
    layout="wide",
)

COLUMN_MAP = {
    "Stock #": "stone_id",
    "Stock": "stone_id",
    "ID": "stone_id",
    "Availability": "availability",
    "Status": "availability",
    "Shape": "shape",
    "Weight": "carat",
    "Carat": "carat",
    "Color": "color",
    "Clarity": "clarity",
    "Cut": "cut",
    "Polish": "polish",
    "Symmetry": "symmetry",
    "Fluorescence": "fluorescence",
    "Measurements": "measurements",
    "Diameter": "diameter",
    "DiameterMM": "diameter_mm",
    "Size MM": "size_mm",
    "Quantity": "quantity",
    "Qty": "quantity",
    "Lab": "lab",
    "Report #": "report_number",
    "Report": "report_number",
    "Certificate": "report_number",
    "Section": "section",
    "Catalog Section": "section",
    "Is Colored": "is_colored",
    "Color Type": "color_type",
    "Color Hue": "color_hue",
    "Color Intensity": "color_intensity",
    "Pair ID": "pair_id",
    "Side Type": "side_type",
    "price_rub": "price_rub",
    "Price RUB": "price_rub",
    "Public Price RUB": "public_price_rub",
    "karo_score": "karo_score",
    "Karo Score": "karo_score",
    "Currency": "currency",
    "Price Date": "price_date",
    "Supplier": "supplier_name",
    "Supplier Name": "supplier_name",
    "Source": "source",
    "Upload Date": "upload_date",
    "show_in_catalog": "show_in_catalog",
    "Show In Catalog": "show_in_catalog",
    "tag1": "tag1",
    "tag2": "tag2",
    "tag3": "tag3",
    "tag4": "tag4",
    "tag5": "tag5",
    "tag6": "tag6",
}

NUMERIC_FIELDS = {
    "carat",
    "price_rub",
    "public_price_rub",
    "karo_score",
    "diameter",
    "diameter_mm",
    "size_mm",
    "quantity",
}


def _clean_cell(value):
    if pd.isna(value):
        return None
    if isinstance(value, str):
        text = value.strip()
        return text if text else None
    return value


def _coerce_value(key, value):
    value = _clean_cell(value)
    if key in NUMERIC_FIELDS and value is not None:
        try:
            if isinstance(value, str):
                value = value.replace(" ", "").replace(",", ".")
            return float(value)
        except (TypeError, ValueError):
            return value
    return value


def dataframe_to_raw_stones(df: pd.DataFrame) -> list[dict]:
    stones = []
    for _, row in df.iterrows():
        item = {}
        for column in df.columns:
            target = COLUMN_MAP.get(str(column).strip(), str(column).strip())
            item[target] = _coerce_value(target, row.get(column))
        if any(value not in (None, "") for value in item.values()):
            stones.append(item)
    return stones


def label_rules(rule_keys):
    return ", ".join(RULE_LIBRARY.get(key, key) for key in rule_keys)


def make_review_table(raw_stones: list[dict]) -> pd.DataFrame:
    rows = []
    for item in raw_stones:
        stone = normalize_stone(item)
        rows.append(
            {
                "ID": stone.get("id"),
                "Раздел": stone.get("section"),
                "Статус": stone.get("publication_status"),
                "Форма": stone.get("shape"),
                "Карат": stone.get("carat"),
                "Цвет": stone.get("color"),
                "Чистота": stone.get("clarity"),
                "Цена": stone.get("price"),
                "Karo Score": stone.get("score"),
                "Report": stone.get("report"),
                "Meta": stone.get("meta"),
                "Блокирующие ошибки": label_rules(stone.get("blocking_errors", [])),
                "Предупреждения": label_rules(stone.get("warnings", [])),
            }
        )
    return pd.DataFrame(rows)


def build_catalog_payload(public_stones: list[dict]) -> dict:
    return {
        "source": "KURGIN Admin Review",
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "count": len(public_stones),
        "stones": public_stones,
    }


st.title("KURGIN Catalog Admin")
st.caption("Предпубликационная проверка Excel / JSON перед отправкой в catalog.json")

with st.expander("Правила публикации по разделам", expanded=False):
    rules = admin_section_rules()
    for section, section_rules in rules.items():
        st.markdown(f"### {section}")
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Блокирующие правила**")
            for rule in section_rules["blocking"]:
                st.write(f"- {rule['label']}")
        with col_b:
            st.markdown("**Предупреждения**")
            for rule in section_rules["warnings"]:
                st.write(f"- {rule['label']}")

uploaded = st.file_uploader("Загрузите Excel или JSON каталога", type=["xlsx", "xls", "json"])

if not uploaded:
    st.info("Загрузите файл, чтобы увидеть готовые к публикации камни, ошибки и предупреждения.")
    st.stop()

raw_stones = []

try:
    if uploaded.name.lower().endswith(".json"):
        payload = json.loads(uploaded.getvalue().decode("utf-8"))
        if isinstance(payload, dict):
            raw_stones = payload.get("stones") or payload.get("catalog") or payload.get("items") or payload.get("data") or []
        elif isinstance(payload, list):
            raw_stones = payload
    else:
        xls = pd.ExcelFile(uploaded)
        sheet = st.selectbox("Лист Excel", xls.sheet_names)
        df = pd.read_excel(uploaded, sheet_name=sheet)
        raw_stones = dataframe_to_raw_stones(df)
except Exception as exc:
    st.error(f"Не удалось прочитать файл: {exc}")
    st.stop()

if not raw_stones:
    st.warning("В файле не найдено строк камней.")
    st.stop()

diagnostics = import_diagnostics(raw_stones)
public_stones = normalize_public_stones(raw_stones)
review_df = make_review_table(raw_stones)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Всего строк", diagnostics["total"])
col2.metric("Готово", diagnostics["ready"])
col3.metric("С предупреждениями", diagnostics["warning"])
col4.metric("Заблокировано", diagnostics["blocked"])

st.subheader("По разделам")
section_rows = []
for section, values in diagnostics["by_section"].items():
    section_rows.append({"Раздел": section, **values})
st.dataframe(pd.DataFrame(section_rows), use_container_width=True)

st.subheader("Проверка камней")
st.dataframe(review_df, use_container_width=True)

if diagnostics["blocking_rules"]:
    st.subheader("Частые блокирующие ошибки")
    st.dataframe(
        pd.DataFrame(
            [
                {"Правило": RULE_LIBRARY.get(key, key), "Количество": count}
                for key, count in diagnostics["blocking_rules"].items()
            ]
        ),
        use_container_width=True,
    )

if diagnostics["warning_rules"]:
    st.subheader("Частые предупреждения")
    st.dataframe(
        pd.DataFrame(
            [
                {"Правило": RULE_LIBRARY.get(key, key), "Количество": count}
                for key, count in diagnostics["warning_rules"].items()
            ]
        ),
        use_container_width=True,
    )

catalog_payload = build_catalog_payload(public_stones)
json_bytes = json.dumps(catalog_payload, ensure_ascii=False, indent=2).encode("utf-8")

st.download_button(
    "Скачать catalog.json для публикации",
    data=json_bytes,
    file_name="catalog.json",
    mime="application/json",
    disabled=not public_stones,
)

if diagnostics["blocked"]:
    st.warning("Есть заблокированные строки. В скачиваемый catalog.json они не попадут.")
else:
    st.success("Блокирующих ошибок нет. Каталог можно публиковать.")
