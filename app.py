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

if page == 'kurgin':
    render_kurgin_info_page()
    st.stop()

if page != 'catalog':
    icons = {'kurgin': '♢', 'tools': '✦', 'catalog': '◇', 'favorites': '♡', 'cart': '◠', 'profile': '○'}
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
*{box-sizing:border-box}html,body{margin:0;padding:0;background:#fff;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#111;overflow:hidden}.app{width:100%;max-width:430px;height:100dvh;min-height:100svh;margin:0 auto;position:relative;background:#fff;overflow:hidden}.content{position:absolute;inset:0 0 calc(126px + env(safe-area-inset-bottom)) 0;overflow-y:auto;-webkit-overflow-scrolling:touch}.header{display:flex;align-items:center;gap:.82rem;padding:.82rem 1rem .72rem;border-bottom:1px solid #ddd;background:#fff;box-shadow:0 2px 10px rgba(0,0,0,.07)}.logo{width:92px;height:36px;object-fit:contain;filter:drop-shadow(0 2px 3px rgba(0,0,0,.13))}.brand-title,.brand-title span{font-family:'Cinzel','Times New Roman',serif!important;font-size:1.15rem;font-weight:400!important;letter-spacing:.06em;line-height:1.02;white-space:nowrap}.brand-sub{margin-top:.3rem;color:#858585;font-size:.58rem;letter-spacing:.105em;text-transform:uppercase}.top{display:grid;grid-template-columns:2fr 1fr;gap:.55rem;padding:.82rem 1rem .55rem;position:relative}.catalogBox{position:relative}.select,.pick{border:1px solid #aaa;border-radius:13px;min-height:54px;background:#fff;display:flex;align-items:center}.select{width:100%;justify-content:space-between;padding:0 .85rem;text-align:left}.pick{justify-content:center;color:#555;font-size:.88rem;line-height:1.22;text-align:center}.select-title{font-weight:400;font-size:.96rem}.select-sub{color:#777;font-size:.78rem;margin-top:.12rem}.chev{width:18px;height:18px;color:#555;display:flex;align-items:center;justify-content:center;transition:transform .18s ease}.chev svg{width:15px;height:15px;stroke:currentColor;stroke-width:1.55;stroke-linecap:round;stroke-linejoin:round;fill:none}.open .chev{transform:rotate(180deg)}.menu{display:none;position:absolute;left:0;right:0;top:calc(100% + .55rem);z-index:45;background:#fff;border:1px solid #bbb;border-radius:10px;box-shadow:0 8px 22px rgba(0,0,0,.18);overflow:hidden}.open .menu{display:block}.menu button{display:block;width:100%;border:0;background:#fff;text-align:left;padding:.62rem .75rem;border-bottom:1px solid #eee}.menu button.active{background:#edf1f5}.m-title{font-size:.86rem;font-weight:400}.m-sub{font-size:.68rem;color:#666;margin-top:.18rem}.sep{height:1px;background:#ddd}.cols,.main{display:grid;grid-template-columns:.92fr .78fr .62fr .95fr 1.12fr 1.25fr;gap:.18rem}.cols{color:#aaa;font-size:.57rem;line-height:1.05;padding:.45rem 1.85rem .6rem;text-transform:uppercase}.card{margin:0 1rem 1rem;border:1px solid #d0d0d0;border-radius:18px;padding:1.05rem 1rem .75rem;background:#fff;cursor:pointer}.card.hide{display:none}.main{font-size:.98rem}.scoreValue{font-weight:800;color:#111}.price{font-weight:700;text-align:right;white-space:nowrap}.line{border-top:1px solid #e6e6e6;margin:1.05rem 0 .7rem}.meta{display:flex;justify-content:space-between;align-items:center;color:#666;font-size:.86rem;gap:.5rem}.tags{display:flex;gap:.35rem;flex-wrap:wrap;justify-content:flex-end}.tag{border:1px solid #f0c56d;color:#c77c16;border-radius:7px;padding:.08rem .45rem;font-size:.7rem;min-width:1.45rem;text-align:center}.blue{border-color:#8bd7e8;color:#1892ad}.gray{border-color:#ccc;color:#555}.elite{border-color:#111;color:#111;letter-spacing:.04em}.actions{display:grid;grid-template-columns:repeat(6,1fr);gap:.1rem;padding-top:.85rem}.act{border:0;background:transparent;color:#888;display:flex;align-items:center;justify-content:center;min-height:28px}.act svg{width:18px;height:18px;stroke:currentColor;stroke-width:1.55;stroke-linecap:round;stroke-linejoin:round;fill:none}.empty{display:none;margin:0 1rem 1rem;border:1px solid #d0d0d0;border-radius:18px;padding:1rem;color:#666;font-size:.9rem;text-align:center}.empty.show{display:block}.controls{position:fixed;left:50%;transform:translateX(-50%);width:100%;max-width:430px;bottom:calc(64px + env(safe-area-inset-bottom));z-index:30;background:#fff;border-top:1px solid #ddd;padding:.5rem .8rem;display:grid;grid-template-columns:1fr 1fr;gap:.65rem}.ctrl{border:1px solid #c9c9c9;border-radius:14px;min-height:64px;background:#fff;text-align:left;padding:.55rem .8rem;color:#111}.ctrl-l{color:#aaa;font-size:.72rem;letter-spacing:.04em}.ctrl-v{font-weight:700;font-size:.92rem;margin-top:.12rem}.nav{position:fixed;left:50%;transform:translateX(-50%);width:100%;max-width:430px;bottom:0;z-index:31;background:#fff;border-top:1px solid #ddd;padding:.25rem .25rem calc(.45rem + env(safe-area-inset-bottom))}.nav-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:.2rem}.nav a{display:flex;align-items:center;justify-content:center;min-height:52px;border-radius:12px;color:#888;text-decoration:none}.nav .active{background:#f2f5f8;color:#111;border:1px solid #cfd5dc}.ico svg{width:22px;height:22px;display:block;stroke:currentColor;stroke-width:1.35;stroke-linecap:round;stroke-linejoin:round;fill:none}
</style>
</head>
<body><div class='app'><div class='content'>KURGIN CATALOG ACTIVE</div></div></body></html>
'''

CATALOG_HTML = CATALOG_HTML.replace('__STONES_JSON__', stones_json)
components.html(CATALOG_HTML, height=900, scrolling=False)
