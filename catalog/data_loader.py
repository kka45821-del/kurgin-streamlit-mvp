import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from catalog.catalog_core import extract_stones, normalize_public_stones
from catalog.stones import STONES as LOCAL_STONES

DEFAULT_CATALOG_URLS = [
    "https://raw.githubusercontent.com/kka45821-del/kurgin-data/main/catalog.json",
    "https://raw.githubusercontent.com/kka45821-del/kurgin-data/main/stones.json",
    "https://raw.githubusercontent.com/kka45821-del/kurgin-data/main/catalog_published.json",
    "https://raw.githubusercontent.com/kka45821-del/kurgin-data/main/data/catalog.json",
]


def _load_json_url(url: str):
    with urlopen(url, timeout=5) as response:
        raw = response.read().decode("utf-8")
    return json.loads(raw)


def load_catalog_stones():
    urls = []
    env_url = os.getenv("KURGIN_DATA_CATALOG_URL")
    if env_url:
        urls.append(env_url)
    urls.extend(DEFAULT_CATALOG_URLS)

    for url in urls:
        try:
            payload = _load_json_url(url)
            stones = normalize_public_stones(extract_stones(payload))
            if stones:
                return stones
        except (URLError, HTTPError, TimeoutError, json.JSONDecodeError, OSError):
            continue

    return normalize_public_stones(LOCAL_STONES)
