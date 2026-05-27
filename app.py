import json

import streamlit as st
import streamlit.components.v1 as components

from catalog.data_loader import load_catalog_stones
from ui.mobile_shell import build_mobile_shell


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
stones_json = json.dumps(load_catalog_stones(), ensure_ascii=False)

st.markdown(
    """
<style>
header[data-testid="stHeader"], div[data-testid="stToolbar"] {display:none}
.block-container {max-width:430px; padding:0!important}
div[data-testid="stElementContainer"] {margin:0!important}
iframe {display:block!important; width:100%!important; height:100dvh!important; min-height:100svh!important; border:0!important}
</style>
""",
    unsafe_allow_html=True,
)

shell_html = build_mobile_shell(page=page, stones_json=stones_json)
shell_html = shell_html.replace(
    """  if(currentPage === 'catalog'){
    activeSection = activeSection || 'all';
    renderCatalogPage();
  } else if(currentPage === 'favorites'){
    renderFavoritesPage();
  }
  renderNav();""",
    """  if(currentPage === 'catalog'){
    activeSection = activeSection || 'all';
  }
  setPage(currentPage);""",
)

components.html(
    shell_html,
    height=900,
    scrolling=False,
)
