import json

from ui.extra_styles import SYSTEM_CSS
from ui.pages.cart_page import render_cart_page
from ui.pages.favorites_page import render_favorites_page
from ui.pages.kurgin_page import render_kurgin_page
from ui.pages.profile_page import render_profile_page
from ui.pages.tools_page import render_tools_page
from ui.scripts import catalog_script
from ui.styles import BASE_CSS

LOGO_URL = "https://raw.githubusercontent.com/kka45821-del/kurgin-streamlit-mvp/main/Vectorr.svg?v=16"

PAGE_TITLES = {
    "kurgin": "KURGIN",
    "tools": "KURGIN Tools",
    "catalog": "KURGIN <span>Diamonds</span>",
    "favorites": "Избранное",
    "cart": "Корзина",
    "profile": "Профиль",
}

PAGE_SUBTITLES = {
    "kurgin": "платформа лабораторных бриллиантов",
    "tools": "инструменты анализа и подбора",
    "catalog": "лабораторные бриллианты",
    "favorites": "сохранённые камни",
    "cart": "выбранные камни",
    "profile": "регистрация и вход",
}


def _page_templates() -> dict[str, str]:
    return {
        "kurgin": render_kurgin_page(LOGO_URL),
        "tools": render_tools_page(),
        "favorites": render_favorites_page(),
        "cart": render_cart_page(),
        "profile": render_profile_page(),
    }


def build_mobile_shell(page: str, stones_json: str) -> str:
    initial_page = page if page in PAGE_TITLES else "catalog"
    pages_json = json.dumps(_page_templates(), ensure_ascii=False)
    titles_json = json.dumps(PAGE_TITLES, ensure_ascii=False)
    subtitles_json = json.dumps(PAGE_SUBTITLES, ensure_ascii=False)

    return f"""
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600&display=swap" rel="stylesheet">
<style>
{BASE_CSS}
{SYSTEM_CSS}
</style>
</head>
<body>
<div class="app" id="app">
  <div class="content" id="content"></div>

  <div class="controls hidden" id="controls">
    <button class="ctrl" id="openSort"><div class="ctrl-l">СОРТИРОВКА</div><div class="ctrl-v" id="sortLabel">по цене ↑</div></button>
    <button class="ctrl" id="openFilters"><div class="ctrl-l">ФИЛЬТРЫ</div><div class="ctrl-v">☷ Параметры</div></button>
  </div>

  <nav class="nav"><div class="nav-grid" id="navGrid"></div></nav>

  <div class="overlay" id="overlay"></div>

  <div class="sortSheet" id="sortSheet">
    <div class="handle" id="sortHandle"></div>
    <div class="head"><div class="title">Сортировка</div></div>
    <div id="sortList"></div>
  </div>

  <div class="detailSheet" id="detailSheet">
    <div class="handle" id="detailHandle"></div>
    <div class="head"><div class="title">Карточка камня</div><button class="closeDetail" id="closeDetail">Закрыть</button></div>
    <div id="detailContent"></div>
  </div>

  <div class="sheet" id="sheet">
    <div class="handle" id="handle"></div>
    <div class="head"><div class="title">Фильтры</div><button class="reset" id="reset">Сбросить</button></div>
    <div id="filterContent"></div>
  </div>
</div>

<script>
{catalog_script(stones_json, initial_page, pages_json, titles_json, subtitles_json, LOGO_URL)}
</script>
</body>
</html>
"""
