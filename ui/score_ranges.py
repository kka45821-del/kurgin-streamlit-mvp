from __future__ import annotations


KURGIN_SCORE_RANGES: list[dict[str, object]] = [
    {
        "id": "elite",
        "min": 98.5,
        "max": 100.0,
        "range_label": "98.5–100",
        "en": "Elite",
        "ru": "Элитный",
        "comment_ru": "Максимальный уровень построения по KURGIN Score.",
    },
    {
        "id": "premium",
        "min": 95.0,
        "max": 98.49,
        "range_label": "95–98.49",
        "en": "Premium",
        "ru": "Премиальный",
        "comment_ru": "Премиальный ювелирный класс, сильный кандидат для подбора.",
    },
    {
        "id": "high",
        "min": 90.0,
        "max": 94.99,
        "range_label": "90–94.99",
        "en": "High",
        "ru": "Высокое качество",
        "comment_ru": "Хороший уровень построения.",
    },
    {
        "id": "standard",
        "min": 80.0,
        "max": 89.99,
        "range_label": "80–89.99",
        "en": "Standard",
        "ru": "Стандартный",
        "comment_ru": "Коммерческий диапазон; требует учёта цены и визуальных факторов.",
    },
    {
        "id": "fair",
        "min": 70.0,
        "max": 79.99,
        "range_label": "70–79.99",
        "en": "Fair",
        "ru": "Среднее качество",
        "comment_ru": "Умеренный результат; нужна осторожность и сравнение с альтернативами.",
    },
    {
        "id": "poor",
        "min": 50.0,
        "max": 69.99,
        "range_label": "50–69.99",
        "en": "Poor",
        "ru": "Низкое качество",
        "comment_ru": "Слабый уровень построения по текущей модели.",
    },
    {
        "id": "rejected",
        "min": 0.0,
        "max": 49.99,
        "range_label": "0–49.99",
        "en": "Rejected",
        "ru": "Не рекомендуется",
        "comment_ru": "Зона отказа для ювелирного подбора по KURGIN Score.",
    },
]


def default_score_range_id() -> str:
    return "standard"
