from urllib.parse import quote

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="KURGIN MVP",
    page_icon="💎",
    layout="centered",
    initial_sidebar_state="collapsed",
)

PAGES = {
    "kurgin": "О KURGIN",
    "tools": "Инструменты",
    "catalog": "Каталог",
    "favorites": "Избранное",
    "cart": "Корзина",
    "profile": "Профиль",
}

TABS = [
    ("kurgin", "♢", "KURGIN"),
    ("tools", "♢", "Инстр."),
    ("catalog", "◇", "Каталог"),
    ("favorites", "♡", "Избр."),
    ("cart", "◠", "Корзина"),
    ("profile", "○", "Профиль"),
]

FILTER_GROUPS = {
    "shape": ["Round", "Oval", "Pear", "Cushion"],
    "weight": ["1–1.49", "1.5–1.99", "2–2.49", "2.5–2.99"],
    "color": ["D", "E", "F", "G", "H"],
    "clarity": ["IF", "VVS1", "VVS2", "VS1", "VS2"],
    "score": ["0–49", "50–79", "80–89", "90–94.9", "95–98", "99+"],
    "fluorescence": ["None", "Faint", "Medium", "Strong"],
    "finish": ["Ex/Ex/Ex+", "2Ex/1VG+"],
}

DEFAULT_FILTERS = {
    "shape": {"Round"},
    "weight": {"1–1.49"},
    "color": {"D", "E", "F"},
    "clarity": {"VVS1", "VS1"},
    "score": {"80–89"},
    "fluorescence": {"None"},
    "finish": {"Ex/Ex/Ex+"},
}

if "page" not in st.session_state:
    st.session_state.page = "catalog"
if "selected_filters" not in st.session_state:
    st.session_state.selected_filters = {k: set(v) for k, v in DEFAULT_FILTERS.items()}

requested_page = st.query_params.get("page")
if requested_page in PAGES:
    st.session_state.page = requested_page

if st.query_params.get("reset") == "1":
    st.session_state.selected_filters = {k: set() for k in FILTER_GROUPS}
    st.query_params.clear()
    st.query_params["page"] = "catalog"
    st.query_params["filters"] = "1"
    st.rerun()

toggle_value = st.query_params.get("toggle")
if toggle_value and ":" in toggle_value:
    group, value = toggle_value.split(":", 1)
    if group in FILTER_GROUPS and value in FILTER_GROUPS[group]:
        selected = st.session_state.selected_filters.setdefault(group, set())
        if value in selected:
            selected.remove(value)
        else:
            selected.add(value)
    st.query_params.clear()
    st.query_params["page"] = "catalog"
    st.query_params["filters"] = "1"
    st.rerun()

current_page = st.session_state.page
filters_open = current_page == "catalog" and st.query_params.get("filters") == "1"


def open_filters() -> None:
    st.query_params["page"] = "catalog"
    st.query_params["filters"] = "1"


def chip(group: str, value: str) -> str:
    selected = value in st.session_state.selected_filters.get(group, set())
    cls = "chip chip-on" if selected else "chip"
    payload = quote(f"{group}:{value}", safe="")
    return f'<a class="{cls}" href="?page=catalog&filters=1&toggle={payload}" target="_self">{value}</a>'


def chips_html(group: str) -> str:
    return "".join(chip(group, value) for value in FILTER_GROUPS[group])


st.markdown(
    """
<style>
header[data-testid="stHeader"], div[data-testid="stToolbar"] { display: none; }
.block-container { max-width: 430px; padding: 0 0 8.9rem 0; }
h1, h2, h3, .stCaption { display: none; }

.catalog-header {
    display: flex; align-items: center; gap: 1rem;
    padding: 1.4rem 1rem 1.15rem;
    border-bottom: 1px solid #ddd;
    box-shadow: 0 2px 8px rgba(0,0,0,.12);
    background: #fff;
}
.logo-mark { width: 72px; height: 44px; border: 1.4px solid #111; border-radius: 50%; position: relative; flex: 0 0 auto; }
.logo-mark:after { content: ""; position: absolute; width: 72px; height: 44px; border: 1.4px solid #111; border-radius: 50%; left: 32px; top: -1px; }
.logo-title { font-family: serif; font-size: 1.35rem; letter-spacing: .08em; color: #111; white-space: nowrap; }
.logo-sub { margin-top: .35rem; color: #8b8b8b; font-size: .72rem; letter-spacing: .08em; }

.catalog-top { display: grid; grid-template-columns: 2fr 1fr; gap: .65rem; padding: 1.35rem 1rem .8rem; }
.catalog-select, .catalog-pick { border: 1px solid #aaa; border-radius: 14px; min-height: 70px; display: flex; align-items: center; justify-content: center; background: #fff; }
.catalog-select { justify-content: space-between; padding: 0 1rem; }
.select-title { font-weight: 700; font-size: 1.05rem; color: #111; }
.select-sub { color: #777; font-size: .92rem; margin-top: .25rem; }
.catalog-pick { color: #555; font-size: .98rem; line-height: 1.35; text-align: center; }

.catalog-cols, .stone-main {
    display: grid;
    grid-template-columns: .92fr .78fr .62fr .95fr 1.12fr 1.25fr;
    gap: .18rem;
}
.catalog-cols {
    color: #aaa;
    font-size: .57rem;
    line-height: 1.05;
    padding: .45rem 1.85rem .6rem;
    text-transform: uppercase;
}
.stone-card { margin: 0 1rem 1rem; border: 1px solid #d0d0d0; border-radius: 18px; padding: 1.05rem 1rem .75rem; background: #fff; }
.stone-main { align-items: start; font-size: .98rem; color: #111; }
.price { font-weight: 700; text-align: right; font-size: .98rem; line-height: 1.25; white-space: nowrap; }
.stone-line { border-top: 1px solid #e6e6e6; margin: 1.05rem 0 .7rem; }
.stone-meta { display: flex; justify-content: space-between; align-items: center; color: #666; font-size: .86rem; gap: .5rem; }
.tags { display: flex; gap: .35rem; flex-wrap: wrap; justify-content: flex-end; }
.tag { border: 1px solid #f0c56d; color: #c77c16; border-radius: 7px; padding: .08rem .45rem; font-size: .7rem; }
.tag-blue { border-color: #8bd7e8; color: #1892ad; }
.tag-gray { border-color: #ccc; color: #555; }
.actions { display: grid; grid-template-columns: repeat(6,1fr); color: #888; font-size: 1.25rem; padding-top: .85rem; text-align: center; }

.st-key-sort_button, .st-key-filter_button {
    position: fixed; bottom: 4.35rem; z-index: 999998; width: calc(50% - 1.15rem); max-width: 195px;
}
.st-key-sort_button { left: max(.8rem, calc(50vw - 207px)); }
.st-key-filter_button { right: max(.8rem, calc(50vw - 207px)); }
.st-key-sort_button button, .st-key-filter_button button {
    width: 100%; min-height: 64px; border: 1px solid #c9c9c9; border-radius: 14px; background: #fff;
    color: #111; text-align: left; padding: .55rem .8rem; font-size: .92rem; font-weight: 700; white-space: pre-line;
}
.st-key-sort_button button:before { content: "СОРТИРОВКА"; display: block; color: #aaa; font-size: .72rem; font-weight: 400; letter-spacing: .04em; }
.st-key-filter_button button:before { content: "ФИЛЬТРЫ"; display: block; color: #aaa; font-size: .72rem; font-weight: 400; letter-spacing: .04em; }

.filter-overlay { position: fixed; left: 0; right: 0; top: 0; bottom: 0; z-index: 1000000; background: rgba(0,0,0,.22); }
.filter-sheet {
    position: fixed; left: 0; right: 0; bottom: 0; z-index: 1000001;
    max-width: 430px; max-height: calc(100vh - 70px); overflow-y: auto;
    margin: 0 auto; background: #fff; border: 1px solid #999; border-bottom: 0;
    border-radius: 26px 26px 0 0; padding: 1.4rem 1.35rem 1.2rem;
    box-shadow: 0 -6px 22px rgba(0,0,0,.18);
    touch-action: pan-y;
}
.sheet-handle { display: block; width: 42px; height: 4px; border-radius: 4px; background: #c9c9c9; margin: 0 auto 1rem; }
.sheet-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: .7rem; }
.sheet-title { font-weight: 700; font-size: 1.15rem; color: #111; }
.reset-link { font-size: .78rem; color: #222!important; text-decoration: none!important; }
.filter-group { margin: .85rem 0 1.05rem; }
.filter-name { font-size: .76rem; font-weight: 600; color: #111; margin-bottom: .55rem; }
.chips { display: flex; gap: .55rem; flex-wrap: wrap; }
.chip {
    border: 1px solid #aaa; border-radius: 18px; padding: .45rem .82rem;
    font-size: .67rem; color: #111!important; background: #fff;
    text-decoration: none!important; display: inline-flex; align-items: center; min-height: 34px;
    -webkit-tap-highlight-color: transparent;
}
.chip-on { background: #000; color: #fff!important; border-color: #000; }
.chip-note { font-size: .58rem; color: #222; align-self: center; }

.kurgin-bottom-nav { position: fixed; left: 0; right: 0; bottom: 0; width: 100%; z-index: 999999; background: #fff; border-top: 1px solid rgba(49,51,63,.18); padding: .25rem .25rem calc(.45rem + env(safe-area-inset-bottom)); }
.kurgin-nav-grid { display: grid; grid-template-columns: repeat(6,1fr); gap: .2rem; max-width: 430px; margin: 0 auto; }
.kurgin-tab { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 52px; border-radius: 12px; color: #888!important; text-decoration: none!important; font-size: .68rem; line-height: 1.1; white-space: nowrap; }
.kurgin-tab-active { background: #f2f5f8; color: #111!important; border: 1px solid #cfd5dc; }
.kurgin-icon { font-size: 1.15rem; line-height: 1; margin-bottom: .15rem; }
.page-pad { padding: 1rem; }
</style>
""",
    unsafe_allow_html=True,
)

if current_page == "catalog":
    st.markdown(
        """
<div class="catalog-header"><div class="logo-mark"></div><div><div class="logo-title">KURGIN DIAMONDS</div><div class="logo-sub">ЛАБОРАТОРНЫЕ БРИЛЛИАНТЫ</div></div></div>
<div class="catalog-top"><div class="catalog-select"><div><div class="select-title">Основной каталог</div><div class="select-sub">1.00–2.99 ct</div></div><div>⌄</div></div><div class="catalog-pick">Индив.<br>подбор</div></div>
<div class="catalog-cols"><div>ФОРМА</div><div>КАРАТ</div><div>ЦВЕТ</div><div>ЧИСТОТА</div><div>KARO SCORE</div><div>ЦЕНА</div></div>
<div class="stone-card"><div class="stone-main"><div>Круг</div><div>1.05</div><div>G</div><div>VVS1</div><div>95</div><div class="price">32 200 ₽</div></div><div class="stone-line"></div><div class="stone-meta"><div>6.5 мм · ex ex vg · none</div><div class="tags"><span class="tag">огонь</span><span class="tag tag-blue">блеск</span></div></div><div class="actions"><div>♡</div><div>▣</div><div>ⓘ</div><div>♡</div><div>⌞</div><div>⌯</div></div></div>
<div class="stone-card"><div class="stone-main"><div>Круг</div><div>1.51</div><div>E</div><div>VS1</div><div>86</div><div class="price">58 500 ₽</div></div><div class="stone-line"></div><div class="stone-meta"><div>7.4 мм · ex ex vg · none</div><div class="tags"><span class="tag tag-gray">контраст</span><span class="tag">огонь</span></div></div><div class="actions"><div>♡</div><div>▣</div><div>ⓘ</div><div>♡</div><div>⌞</div><div>⌯</div></div></div>
<div class="stone-card"><div class="stone-main"><div>Круг</div><div>1</div><div>F</div><div>VS2</div><div>77</div><div class="price">34 900 ₽</div></div><div class="stone-line"></div><div class="stone-meta"><div>6.4 мм · ex ex vg · none</div><div class="tags"><span class="tag">БАЛАНС</span></div></div></div>
""",
        unsafe_allow_html=True,
    )

    st.button("по Karo Score ↓", key="sort_button")
    st.button("☷ Параметры", key="filter_button", on_click=open_filters)

    if filters_open:
        st.markdown(
            f"""
<a class="filter-overlay" href="?page=catalog" target="_self"></a>
<div class="filter-sheet">
  <a class="sheet-handle" href="?page=catalog" target="_self"></a>
  <div class="sheet-head"><div class="sheet-title">Фильтры</div><a class="reset-link" href="?page=catalog&filters=1&reset=1" target="_self">Сбросить</a></div>
  <div class="filter-group"><div class="filter-name">1. Форма / огранка</div><div class="chips">{chips_html('shape')}</div></div>
  <div class="filter-group"><div class="filter-name">2. Вес</div><div class="chips">{chips_html('weight')}</div></div>
  <div class="filter-group"><div class="filter-name">3. Цвет</div><div class="chips">{chips_html('color')}</div></div>
  <div class="filter-group"><div class="filter-name">4. Чистота</div><div class="chips">{chips_html('clarity')}</div></div>
  <div class="filter-group"><div class="filter-name">5. Karo Score</div><div class="chips">{chips_html('score')}<span class="chip-note">качество / индекс-коэф.</span></div></div>
  <div class="filter-group"><div class="filter-name">6. Флюоресценция</div><div class="chips">{chips_html('fluorescence')}</div></div>
  <div class="filter-group"><div class="filter-name">7. Качество отделки</div><div class="chips">{chips_html('finish')}</div></div>
</div>
""",
            unsafe_allow_html=True,
        )
        components.html(
            """
<script>
(function () {
  const closeUrl = new URL(window.parent.location.href);
  closeUrl.searchParams.set('page', 'catalog');
  closeUrl.searchParams.delete('filters');
  closeUrl.searchParams.delete('toggle');
  closeUrl.searchParams.delete('reset');

  function attachSwipeClose() {
    try {
      const sheet = window.parent.document.querySelector('.filter-sheet');
      if (!sheet || sheet.dataset.swipeReady === '1') return;
      sheet.dataset.swipeReady = '1';
      let startY = null;
      let startX = null;
      sheet.addEventListener('touchstart', function (event) {
        if (!event.touches || event.touches.length === 0) return;
        startY = event.touches[0].clientY;
        startX = event.touches[0].clientX;
      }, { passive: true });
      sheet.addEventListener('touchend', function (event) {
        if (startY === null || !event.changedTouches || event.changedTouches.length === 0) return;
        const endY = event.changedTouches[0].clientY;
        const endX = event.changedTouches[0].clientX;
        const dy = endY - startY;
        const dx = Math.abs(endX - startX);
        if (dy > 85 && dx < 90) {
          window.parent.location.href = closeUrl.toString();
        }
        startY = null;
        startX = null;
      }, { passive: true });
    } catch (e) {}
  }

  setTimeout(attachSwipeClose, 100);
  setTimeout(attachSwipeClose, 500);
})();
</script>
""",
            height=0,
        )
else:
    st.markdown(f'<div class="page-pad"><h3>{PAGES[current_page]}</h3></div>', unsafe_allow_html=True)

nav_items = []
for page_key, icon, label in TABS:
    active_class = " kurgin-tab-active" if page_key == current_page else ""
    nav_items.append(
        f'<a class="kurgin-tab{active_class}" href="?page={page_key}" target="_self">'
        f'<span class="kurgin-icon">{icon}</span><span>{label}</span></a>'
    )
st.markdown('<nav class="kurgin-bottom-nav"><div class="kurgin-nav-grid">' + ''.join(nav_items) + '</div></nav>', unsafe_allow_html=True)
