import json

import streamlit as st
import streamlit.components.v1 as components

from catalog.data_loader import load_catalog_state
from ui.publication_contract_shell import build_mobile_shell


st.set_page_config(
    page_title="KURGIN MVP",
    page_icon="favicon.png",
    layout="centered",
    initial_sidebar_state="collapsed",
)

PAGES = {
    "kurgin": "KURGIN",
    "tools": "KURGIN Tools",
    "catalog": "KURGIN Diamonds",
    "favorites": "Избранное",
    "cart": "Корзина",
    "profile": "Профиль",
}

if "page" not in st.session_state:
    st.session_state.page = "catalog"

query_page = st.query_params.get("page")
if query_page in PAGES:
    st.session_state.page = query_page

page = st.session_state.page
catalog_state = load_catalog_state()
stones_json = json.dumps(catalog_state.get("stones", []), ensure_ascii=False)

st.markdown(
    """
<style>
header[data-testid="stHeader"], div[data-testid="stToolbar"] {display:none}
.block-container {max-width:430px; padding:0!important}
div[data-testid="stElementContainer"] {margin:0!important}
iframe {display:block!important; width:100%!important; height:100dvh!important; min-height:100svh!important; border:0!important}
.catalog-load-notice {font-size:.72rem; line-height:1.35; color:#666; background:#f7f7f7; border:1px solid #e5e5e5; border-radius:14px; padding:.55rem .7rem; margin:.45rem 0 .55rem}
</style>
""",
    unsafe_allow_html=True,
)

if page == "catalog" and catalog_state.get("status") in {"fallback_used", "empty", "error"}:
    st.markdown(
        f"<div class='catalog-load-notice'>{catalog_state.get('public_notice', 'Каталог временно недоступен.')}</div>",
        unsafe_allow_html=True,
    )

components.html(
    build_mobile_shell(page=page, stones_json=stones_json),
    height=900,
    scrolling=False,
)
