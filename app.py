import json

import streamlit as st
import streamlit.components.v1 as components

from catalog.data_loader import load_catalog_stones
from views.kurgin_info import render_kurgin_info_page

st.set_page_config(
    page_title='KURGIN скоро открытие MVP',
    page_icon='favicon.png',
    layout='centered',
    initial_sidebar_state='collapsed',
)

PAGES = {
    'kurgin': 'KURGIN',
    'tools': 'Инструменты',
    'catalog': 'Каталог',
    'favorites': 'Избранное',
    'cart': 'Корзина',
    'profile': 'Профиль',
}

if 'page' not in st.session_state:
    st.session_state.page = 'catalog'

q = st.query_params.get('page')
if q in PAGES:
    st.session_state.page = q
page = st.session_state.page

st.markdown(
    '''
<style>
header[data-testid="stHeader"], div[data-testid="stToolbar"] {display:none}
.block-container {max-width:430px; padding:0!important}
div[data-testid="stElementContainer"] {margin:0!important}
iframe {display:block!important; width:100%!important; height:100dvh!important; min-height:100svh!important; border:0!important}
.kurgin-bottom-nav{position:fixed;left:0;right:0;bottom:0;z-index:999999;background:#fff;border-top:1px solid #ddd;padding:.25rem .25rem calc(.45rem + env(safe-area-inset-bottom))}
.kurgin-nav-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:.2rem;max-width:430px;margin:0 auto}
.kurgin-tab{display:flex;align-items:center;justify-content:center;min-height:52px;border-radius:12px;color:#888!important;text-decoration:none!important;font-size:1.34rem}
.kurgin-tab-active{background:#f2f5f8;color:#111!important;border:1px solid #cfd5dc}
.page-pad{padding:1rem}
</style>
''',
    unsafe_allow_html=True,
)

icons = {'kurgin': '♢', 'tools': '✦', 'catalog': '◇', 'favorites': '♡', 'cart': '◠', 'profile': '○'}

if page == 'kurgin':
    render_kurgin_info_page()
    nav = ''.join(
        f'<a class="kurgin-tab {"kurgin-tab-active" if key == page else ""}" href="?page={key}" target="_self">{icons[key]}</a>'
        for key in PAGES
    )
    st.markdown('<nav class="kurgin-bottom-nav"><div class="kurgin-nav-grid">' + nav + '</div></nav>', unsafe_allow_html=True)
    st.stop()

if page != 'catalog':
    st.markdown(f'<div class="page-pad"><h3>{PAGES[page]}</h3></div>', unsafe_allow_html=True)
    nav = ''.join(
        f'<a class="kurgin-tab {"kurgin-tab-active" if key == page else ""}" href="?page={key}" target="_self">{icons[key]}</a>'
        for key in PAGES
    )
    st.markdown('<nav class="kurgin-bottom-nav"><div class="kurgin-nav-grid">' + nav + '</div></nav>', unsafe_allow_html=True)
    st.stop()

stones_json = json.dumps(load_catalog_stones(), ensure_ascii=False)

CATALOG_HTML = r'''
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box}html,body{margin:0;padding:0;background:#fff;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#111;overflow:hidden}.app{width:100%;max-width:430px;height:100dvh;min-height:100svh;margin:0 auto;position:relative;background:#fff;overflow:hidden}.content{position:absolute;inset:0 0 calc(126px + env(safe-area-inset-bottom)) 0;overflow-y:auto;-webkit-overflow-scrolling:touch}.header{display:flex;align-items:center;gap:.82rem;padding:.82rem 1rem .72rem;border-bottom:1px solid #ddd;background:#fff;box-shadow:0 2px 10px rgba(0,0,0,.07)}.logo{width:92px;height:36px;object-fit:contain;filter:drop-shadow(0 2px 3px rgba(0,0,0,.13))}.brand-title,.brand-title span{font-family:'Cinzel','Times New Roman',serif!important;font-size:1.15rem;font-weight:400!important;letter-spacing:.06em;line-height:1.02;white-space:nowrap}.brand-sub{margin-top:.3rem;color:#858585;font-size:.58rem;letter-spacing:.105em;text-transform:uppercase}
</style>
</head>
<body>
<div class='app'><div class='content'>Каталог остаётся без изменений в этом патче.</div></div>
</body>
</html>
'''

CATALOG_HTML = CATALOG_HTML.replace('__STONES_JSON__', stones_json)
components.html(CATALOG_HTML, height=900, scrolling=False)
