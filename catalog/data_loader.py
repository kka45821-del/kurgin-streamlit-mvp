import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from catalog.catalog_core import extract_stones
from catalog.public_state_contract import normalize_public_stones
from catalog.stones import STONES as LOCAL_STONES

CATALOG_LOADER_VERSION = "state_v2_public_contract"

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


def _catalog_state(status: str, stones: list[dict], *, source: str, attempted_remote: int = 0, remote_empty: int = 0, remote_errors: int = 0) -> dict:
    notices = {
        "remote_loaded": "Каталог загружен.",
        "fallback_used": "Показана резервная демо-выборка.",
        "empty": "Каталог пока пуст. Попробуйте проверить публикацию данных позже.",
        "error": "Каталог временно недоступен. Попробуйте открыть страницу позже.",
    }
    return {
        "status": status,
        "source": source,
        "count": len(stones),
        "attempted_remote": attempted_remote,
        "remote_empty": remote_empty,
        "remote_errors": remote_errors,
        "public_notice": notices.get(status, notices["remote_loaded"]),
        "stones": stones,
    }


def load_catalog_state() -> dict:
    urls = []
    env_url = os.getenv("KURGIN_DATA_CATALOG_URL")
    if env_url:
        urls.append(env_url)
    urls.extend(DEFAULT_CATALOG_URLS)

    remote_empty = 0
    remote_errors = 0

    for url in urls:
        try:
            payload = _load_json_url(url)
            stones = normalize_public_stones(extract_stones(payload))
            if stones:
                return _catalog_state(
                    "remote_loaded",
                    stones,
                    source="remote",
                    attempted_remote=len(urls),
                    remote_empty=remote_empty,
                    remote_errors=remote_errors,
                )
            remote_empty += 1
        except (URLError, HTTPError, TimeoutError, json.JSONDecodeError, OSError):
            remote_errors += 1
            continue

    fallback_stones = normalize_public_stones(LOCAL_STONES)
    if fallback_stones:
        return _catalog_state(
            "fallback_used",
            fallback_stones,
            source="local_fallback",
            attempted_remote=len(urls),
            remote_empty=remote_empty,
            remote_errors=remote_errors,
        )

    status = "error" if remote_errors else "empty"
    return _catalog_state(
        status,
        [],
        source="none",
        attempted_remote=len(urls),
        remote_empty=remote_empty,
        remote_errors=remote_errors,
    )


def load_catalog_stones():
    return load_catalog_state()["stones"]
