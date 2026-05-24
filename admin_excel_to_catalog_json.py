import json
from pathlib import Path

import pandas as pd

INPUT_FILE = Path("KURGIN_Filled_Test_Import_AllData.xlsx")
OUTPUT_FILE = Path("catalog.json")


COLUMN_MAP = {
    "Stock #": "stone_id",
    "Availability": "availability",
    "Shape": "shape",
    "Weight": "carat",
    "Color": "color",
    "Clarity": "clarity",
    "Cut": "cut",
    "Polish": "polish",
    "Symmetry": "symmetry",
    "Fluorescence": "fluorescence",
    "Measurements": "measurements",
    "Shade": "shade",
    "Milky": "milky",
    "Eye Clean": "eye_clean",
    "Lab": "lab",
    "Report #": "report_number",
    "Location": "location",
    "Treatment": "treatment",
    "DepthPercent": "depth_percent",
    "TablePercent": "table_percent",
    "GirdleThin": "girdle_thin",
    "GirdleThick": "girdle_thick",
    "GirdlePercent": "girdle_percent",
    "GirdleCondition": "girdle_condition",
    "CuletSize": "culet_size",
    "CuletCondition": "culet_condition",
    "CrownPercent": "crown_percent",
    "CrownAngle": "crown_angle",
    "PavilionPercent": "pavilion_percent",
    "PavilionAngle": "pavilion_angle",
    "price_rub": "price_rub",
    "karo_score": "karo_score",
    "tag1": "tag1",
    "tag2": "tag2",
    "tag3": "tag3",
    "tag4": "tag4",
    "tag5": "tag5",
    "tag6": "tag6",
}


NUMERIC_FIELDS = {
    "carat",
    "depth_percent",
    "table_percent",
    "girdle_percent",
    "crown_percent",
    "crown_angle",
    "pavilion_percent",
    "pavilion_angle",
    "price_rub",
    "karo_score",
}


def clean_value(value):
    if pd.isna(value):
        return None
    return value


# Read source workbook.
df = pd.read_excel(INPUT_FILE, sheet_name="All Data")

stones = []

for _, row in df.iterrows():
    stock = row.get("Stock #")
    if pd.isna(stock):
        continue

    stone = {}

    for excel_col, target_key in COLUMN_MAP.items():
        value = clean_value(row.get(excel_col))

        if target_key in NUMERIC_FIELDS and value is not None:
            try:
                value = float(value)
            except (TypeError, ValueError):
                value = None

        stone[target_key] = value

    stones.append(stone)

payload = {
    "updated_at": pd.Timestamp.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "source": "KURGIN Admin",
    "stones": stones,
}

OUTPUT_FILE.write_text(
    json.dumps(payload, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

print(f"Exported {len(stones)} stones -> {OUTPUT_FILE}")
