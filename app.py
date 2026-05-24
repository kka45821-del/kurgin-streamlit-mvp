import html

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

if "page" not in st.session_state:
    st.session_state.page = "catalog"

requested_page = st.query_params.get("page")
if requested_page in PAGES:
    st.session_state.page = requested_page

current_page = st.session_state.page

st.markdown(
    """
<style>
header[data-testid="stHeader"], div[data-testid="stToolbar"] { display: none; }
.block-container { max-width: 430px; padding: 0 !important; }
div[data-testid="stElementContainer"] { margin: 0 !important; }
iframe { display: block !important; width: 100% !important; height: 100dvh !important; min-height: 100svh !important; border: 0 !important; }
.page-pad { padding: 1rem; }
.kurgin-bottom-nav { position: fixed; left: 0; right: 0; bottom: 0; width: 100%; z-index: 999999; background: #fff; border-top: 1px solid rgba(49,51,63,.18); padding: .25rem .25rem calc(.45rem + env(safe-area-inset-bottom)); }
.kurgin-nav-grid { display: grid; grid-template-columns: repeat(6,1fr); gap: .2rem; max-width: 430px; margin: 0 auto; }
.kurgin-tab { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 52px; border-radius: 12px; color: #888!important; text-decoration: none!important; font-size: .68rem; line-height: 1.1; white-space: nowrap; }
.kurgin-tab-active { background: #f2f5f8; color: #111!important; border: 1px solid #cfd5dc; }
.kurgin-icon { font-size: 1.15rem; line-height: 1; margin-bottom: .15rem; }
</style>
""",
    unsafe_allow_html=True,
)


def weight_group(carat: float) -> str:
    if carat < 1.5:
        return "1–1.49"
    if carat < 2.0:
        return "1.5–1.99"
    if carat < 2.5:
        return "2–2.49"
    return "2.5–2.99"


def score_group(score: float) -> str:
    if score < 50:
        return "0–49"
    if score < 80:
        return "50–79"
    if score < 90:
        return "80–89"
    if score < 95:
        return "90–94.9"
    if score < 99:
        return "95–98"
    return "99+"


def stone_card(stone: dict) -> str:
    tags = "".join(
        f'<span class="tag {html.escape(cls)}">{html.escape(label)}</span>'
        for label, cls in stone["tags"]
    )
    data = {
        "shape": stone["shape_filter"],
        "weight": weight_group(float(stone["carat"])),
        "color": stone["color"],
        "clarity": stone["clarity"],
        "score": score_group(float(stone["score"])),
        "fluorescence": stone["fluorescence"],
        "finish": stone["finish"],
    }
    data_attrs = " ".join(f'data-{key}="{html.escape(value)}"' for key, value in data.items())
    return f"""
    <div class="stone-card" {data_attrs}>
      <div class="stone-main">
        <div>{html.escape(stone['shape'])}</div>
        <div>{html.escape(str(stone['carat']))}</div>
        <div>{html.escape(stone['color'])}</div>
        <div>{html.escape(stone['clarity'])}</div>
        <div>{html.escape(str(stone['score']))}</div>
        <div class="price">{html.escape(stone['price'])} ₽</div>
      </div>
      <div class="stone-line"></div>
      <div class="stone-meta"><div>{html.escape(stone['meta'])}</div><div class="tags">{tags}</div></div>
      <div class="actions"><div>♡</div><div>▣</div><div>ⓘ</div><div>♡</div><div>⌞</div><div>⌯</div></div>
    </div>
    """


STONES = [
    {"shape": "Круг", "shape_filter": "Round", "carat": "1.05", "color": "G", "clarity": "VVS1", "score": "95", "price": "32 200", "meta": "6.5 мм · ex ex vg · none", "fluorescence": "None", "finish": "2Ex/1VG+", "tags": [("огонь", ""), ("блеск", "tag-blue")]},
    {"shape": "Круг", "shape_filter": "Round", "carat": "1.51", "color": "E", "clarity": "VS1", "score": "86", "price": "58 500", "meta": "7.4 мм · ex ex vg · none", "fluorescence": "None", "finish": "2Ex/1VG+", "tags": [("контраст", "tag-gray"), ("огонь", "")]},
    {"shape": "Круг", "shape_filter": "Round", "carat": "1.00", "color": "F", "clarity": "VS2", "score": "77", "price": "34 900", "meta": "6.4 мм · ex ex vg · none", "fluorescence": "None", "finish": "2Ex/1VG+", "tags": [("БАЛАНС", "")]},
    {"shape": "Круг", "shape_filter": "Round", "carat": "1.22", "color": "D", "clarity": "VVS2", "score": "92", "price": "41 800", "meta": "6.9 мм · ex ex ex · none", "fluorescence": "None", "finish": "Ex/Ex/Ex+", "tags": [("блеск", "tag-blue"), ("огонь", "")]},
    {"shape": "Круг", "shape_filter": "Round", "carat": "1.74", "color": "F", "clarity": "VS1", "score": "89", "price": "67 900", "meta": "7.8 мм · ex ex vg · faint", "fluorescence": "Faint", "finish": "2Ex/1VG+", "tags": [("контраст", "tag-gray"), ("блеск", "tag-blue")]},
    {"shape": "Круг", "shape_filter": "Round", "carat": "2.03", "color": "G", "clarity": "VS2", "score": "84", "price": "88 400", "meta": "8.1 мм · ex vg vg · none", "fluorescence": "None", "finish": "2Ex/1VG+", "tags": [("БАЛАНС", "")]},
    {"shape": "Круг", "shape_filter": "Round", "carat": "2.41", "color": "E", "clarity": "VVS1", "score": "96", "price": "126 300", "meta": "8.7 мм · ex ex ex · none", "fluorescence": "None", "finish": "Ex/Ex/Ex+", "tags": [("огонь", ""), ("блеск", "tag-blue")]},
]

cards_html = "".join(stone_card(stone) for stone in STONES)

CATALOG_TEMPLATE = r"""
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<style>
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: #fff; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: #111; overflow: hidden; }
.app { width: 100%; max-width: 430px; height: 100dvh; min-height: 100svh; margin: 0 auto; position: relative; overflow: hidden; background: #fff; }
.content { position: absolute; inset: 0 0 calc(126px + env(safe-area-inset-bottom)) 0; overflow-y: auto; -webkit-overflow-scrolling: touch; padding-bottom: 20px; }
.catalog-header { display:flex; align-items:center; gap:1rem; padding:1.4rem 1rem 1.15rem; border-bottom:1px solid #ddd; box-shadow:0 2px 8px rgba(0,0,0,.12); background:#fff; }
.logo-mark { width:72px; height:44px; border:1.4px solid #111; border-radius:50%; position:relative; flex:0 0 auto; }
.logo-mark:after { content:""; position:absolute; width:72px; height:44px; border:1.4px solid #111; border-radius:50%; left:32px; top:-1px; }
.logo-title { font-family:serif; font-size:1.35rem; letter-spacing:.08em; color:#111; white-space:nowrap; }
.logo-sub { margin-top:.35rem; color:#8b8b8b; font-size:.72rem; letter-spacing:.08em; }
.catalog-top { display:grid; grid-template-columns:2fr 1fr; gap:.65rem; padding:1.35rem 1rem .8rem; }
.catalog-select, .catalog-pick { border:1px solid #aaa; border-radius:14px; min-height:70px; display:flex; align-items:center; justify-content:center; background:#fff; }
.catalog-select { justify-content:space-between; padding:0 1rem; }
.select-title { font-weight:700; font-size:1.05rem; color:#111; }
.select-sub { color:#777; font-size:.92rem; margin-top:.25rem; }
.catalog-pick { color:#555; font-size:.98rem; line-height:1.35; text-align:center; }
.catalog-cols, .stone-main { display:grid; grid-template-columns:.92fr .78fr .62fr .95fr 1.12fr 1.25fr; gap:.18rem; }
.catalog-cols { color:#aaa; font-size:.57rem; line-height:1.05; padding:.45rem 1.85rem .6rem; text-transform:uppercase; }
.stone-card { margin:0 1rem 1rem; border:1px solid #d0d0d0; border-radius:18px; padding:1.05rem 1rem .75rem; background:#fff; }
.stone-card.is-hidden { display:none; }
.stone-main { align-items:start; font-size:.98rem; color:#111; }
.price { font-weight:700; text-align:right; font-size:.98rem; line-height:1.25; white-space:nowrap; }
.stone-line { border-top:1px solid #e6e6e6; margin:1.05rem 0 .7rem; }
.stone-meta { display:flex; justify-content:space-between; align-items:center; color:#666; font-size:.86rem; gap:.5rem; }
.tags { display:flex; gap:.35rem; flex-wrap:wrap; justify-content:flex-end; }
.tag { border:1px solid #f0c56d; color:#c77c16; border-radius:7px; padding:.08rem .45rem; font-size:.7rem; }
.tag-blue { border-color:#8bd7e8; color:#1892ad; }
.tag-gray { border-color:#ccc; color:#555; }
.actions { display:grid; grid-template-columns:repeat(6,1fr); color:#888; font-size:1.25rem; padding-top:.85rem; text-align:center; }
.empty-state { display:none; margin: 0 1rem 1rem; border:1px solid #d0d0d0; border-radius:18px; padding:1rem; color:#666; font-size:.9rem; text-align:center; }
.empty-state.is-visible { display:block; }
.bottom-controls { position: fixed; left: 50%; transform: translateX(-50%); width: 100%; max-width: 430px; bottom: calc(64px + env(safe-area-inset-bottom)); z-index: 30; background:#fff; border-top:1px solid #ddd; padding:.5rem .8rem; display:grid; grid-template-columns:1fr 1fr; gap:.65rem; }
.control-box { border:1px solid #c9c9c9; border-radius:14px; min-height:64px; background:#fff; text-align:left; padding:.55rem .8rem; color:#111; }
.control-label { color:#aaa; font-size:.72rem; letter-spacing:.04em; }
.control-value { font-weight:700; font-size:.92rem; margin-top:.12rem; }
.bottom-nav { position: fixed; left: 50%; transform: translateX(-50%); width: 100%; max-width: 430px; bottom: 0; z-index: 31; background:#fff; border-top:1px solid rgba(49,51,63,.18); padding:.25rem .25rem calc(.45rem + env(safe-area-inset-bottom)); }
.nav-grid { display:grid; grid-template-columns:repeat(6,1fr); gap:.2rem; }
.nav-tab { display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:52px; border-radius:12px; color:#888; text-decoration:none; font-size:.68rem; line-height:1.1; white-space:nowrap; }
.nav-active { background:#f2f5f8; color:#111; border:1px solid #cfd5dc; }
.nav-icon { font-size:1.15rem; line-height:1; margin-bottom:.15rem; }
.overlay { display:none; position: fixed; left: 0; right: 0; top: 0; bottom: 0; z-index:50; background:rgba(0,0,0,.22); }
.sheet { position: fixed; left: 50%; right: auto; bottom: 0; transform: translate(-50%, 110%); width: 100%; max-width: 430px; z-index:60; max-height:calc(100dvh - 70px); overflow-y:auto; -webkit-overflow-scrolling:touch; background:#fff; border:1px solid #999; border-bottom:0; border-radius:26px 26px 0 0; padding:1.4rem 1.35rem 1.2rem; box-shadow:0 -6px 22px rgba(0,0,0,.18); transition:transform .22s ease; touch-action:pan-y; }
.sheet-open .overlay { display:block; }
.sheet-open .sheet { transform: translate(-50%, 0); }
.sheet-handle { width:42px; height:4px; border-radius:4px; background:#c9c9c9; margin:0 auto 1rem; }
.sheet-head { display:flex; justify-content:space-between; align-items:center; margin-bottom:.7rem; }
.sheet-title { font-weight:700; font-size:1.15rem; color:#111; }
.reset { border:0; background:transparent; padding:0; font-size:.78rem; color:#222; }
.filter-group { margin:.85rem 0 1.05rem; }
.filter-name { font-size:.76rem; font-weight:600; color:#111; margin-bottom:.55rem; }
.chips { display:flex; gap:.55rem; flex-wrap:wrap; }
.chip { border:1px solid #aaa; border-radius:18px; padding:.45rem .82rem; font-size:.67rem; color:#111; background:#fff; min-height:34px; -webkit-tap-highlight-color:transparent; }
.chip-on { background:#000; color:#fff; border-color:#000; }
.chip-note { font-size:.58rem; color:#222; align-self:center; }
</style>
</head>
<body>
<div class="app" id="app">
  <div class="content" id="content">
    <div class="catalog-header"><div class="logo-mark"></div><div><div class="logo-title">KURGIN DIAMONDS</div><div class="logo-sub">ЛАБОРАТОРНЫЕ БРИЛЛИАНТЫ</div></div></div>
    <div class="catalog-top"><div class="catalog-select"><div><div class="select-title">Основной каталог</div><div class="select-sub">1.00–2.99 ct</div></div><div>⌄</div></div><div class="catalog-pick">Индив.<br>подбор</div></div>
    <div class="catalog-cols"><div>ФОРМА</div><div>КАРАТ</div><div>ЦВЕТ</div><div>ЧИСТОТА</div><div>KARO SCORE</div><div>ЦЕНА</div></div>
    __CARDS__
    <div class="empty-state" id="emptyState">По выбранным фильтрам камни не найдены</div>
  </div>
  <div class="bottom-controls"><button class="control-box"><div class="control-label">СОРТИРОВКА</div><div class="control-value">по Karo Score ↓</div></button><button class="control-box" id="openFilters"><div class="control-label">ФИЛЬТРЫ</div><div class="control-value">☷ Параметры</div></button></div>
  <nav class="bottom-nav"><div class="nav-grid"><a class="nav-tab" href="?page=kurgin" target="_parent"><span class="nav-icon">♢</span><span>KURGIN</span></a><a class="nav-tab" href="?page=tools" target="_parent"><span class="nav-icon">♢</span><span>Инстр.</span></a><a class="nav-tab nav-active" href="?page=catalog" target="_parent"><span class="nav-icon">◇</span><span>Каталог</span></a><a class="nav-tab" href="?page=favorites" target="_parent"><span class="nav-icon">♡</span><span>Избр.</span></a><a class="nav-tab" href="?page=cart" target="_parent"><span class="nav-icon">◠</span><span>Корзина</span></a><a class="nav-tab" href="?page=profile" target="_parent"><span class="nav-icon">○</span><span>Профиль</span></a></div></nav>
  <div class="overlay" id="overlay"></div>
  <div class="sheet" id="sheet">
    <div class="sheet-handle" id="handle"></div>
    <div class="sheet-head"><div class="sheet-title">Фильтры</div><button class="reset" id="resetFilters">Сбросить</button></div>
    <div class="filter-group"><div class="filter-name">1. Форма / огранка</div><div class="chips"><button class="chip chip-on" data-group="shape" data-value="Round">Round</button><button class="chip" data-group="shape" data-value="Oval">Oval</button><button class="chip" data-group="shape" data-value="Pear">Pear</button><button class="chip" data-group="shape" data-value="Cushion">Cushion</button></div></div>
    <div class="filter-group"><div class="filter-name">2. Вес</div><div class="chips"><button class="chip" data-group="weight" data-value="1–1.49">1–1.49</button><button class="chip" data-group="weight" data-value="1.5–1.99">1.5–1.99</button><button class="chip" data-group="weight" data-value="2–2.49">2–2.49</button><button class="chip" data-group="weight" data-value="2.5–2.99">2.5–2.99</button></div></div>
    <div class="filter-group"><div class="filter-name">3. Цвет</div><div class="chips"><button class="chip" data-group="color" data-value="D">D</button><button class="chip" data-group="color" data-value="E">E</button><button class="chip" data-group="color" data-value="F">F</button><button class="chip" data-group="color" data-value="G">G</button><button class="chip" data-group="color" data-value="H">H</button></div></div>
    <div class="filter-group"><div class="filter-name">4. Чистота</div><div class="chips"><button class="chip" data-group="clarity" data-value="IF">IF</button><button class="chip" data-group="clarity" data-value="VVS1">VVS1</button><button class="chip" data-group="clarity" data-value="VVS2">VVS2</button><button class="chip" data-group="clarity" data-value="VS1">VS1</button><button class="chip" data-group="clarity" data-value="VS2">VS2</button></div></div>
    <div class="filter-group"><div class="filter-name">5. Karo Score</div><div class="chips"><button class="chip" data-group="score" data-value="0–49">0–49</button><button class="chip" data-group="score" data-value="50–79">50–79</button><button class="chip" data-group="score" data-value="80–89">80–89</button><button class="chip" data-group="score" data-value="90–94.9">90–94.9</button><button class="chip" data-group="score" data-value="95–98">95–98</button><button class="chip" data-group="score" data-value="99+">99+</button><span class="chip-note">качество / индекс-коэф.</span></div></div>
    <div class="filter-group"><div class="filter-name">6. Флюоресценция</div><div class="chips"><button class="chip" data-group="fluorescence" data-value="None">None</button><button class="chip" data-group="fluorescence" data-value="Faint">Faint</button><button class="chip" data-group="fluorescence" data-value="Medium">Medium</button><button class="chip" data-group="fluorescence" data-value="Strong">Strong</button></div></div>
    <div class="filter-group"><div class="filter-name">7. Качество отделки</div><div class="chips"><button class="chip" data-group="finish" data-value="Ex/Ex/Ex+">Ex/Ex/Ex+</button><button class="chip" data-group="finish" data-value="2Ex/1VG+">2Ex/1VG+</button></div></div>
  </div>
</div>
<script>
const app = document.getElementById('app');
const sheet = document.getElementById('sheet');
const overlay = document.getElementById('overlay');
const openFilters = document.getElementById('openFilters');
const resetFilters = document.getElementById('resetFilters');
const handle = document.getElementById('handle');
const emptyState = document.getElementById('emptyState');
const cards = Array.from(document.querySelectorAll('.stone-card'));
const chips = Array.from(document.querySelectorAll('.chip'));
const filterGroups = ['shape', 'weight', 'color', 'clarity', 'score', 'fluorescence', 'finish'];

function activeFilters() {
  const filters = {};
  filterGroups.forEach(group => filters[group] = []);
  chips.forEach(chip => {
    if (chip.classList.contains('chip-on')) {
      filters[chip.dataset.group].push(chip.dataset.value);
    }
  });
  return filters;
}

function applyFilters() {
  const filters = activeFilters();
  let visibleCount = 0;
  cards.forEach(card => {
    let visible = true;
    filterGroups.forEach(group => {
      const values = filters[group];
      if (values.length > 0 && !values.includes(card.dataset[group])) {
        visible = false;
      }
    });
    card.classList.toggle('is-hidden', !visible);
    if (visible) visibleCount += 1;
  });
  emptyState.classList.toggle('is-visible', visibleCount === 0);
}

function openSheet(){
  app.classList.add('sheet-open');
  sheet.style.transition='transform .22s ease';
  sheet.style.transform='translate(-50%, 0)';
}

function closeSheet(){
  sheet.style.transition='transform .22s ease';
  sheet.style.transform='translate(-50%, 110%)';
  setTimeout(() => app.classList.remove('sheet-open'), 180);
}

openFilters.addEventListener('click', openSheet);
overlay.addEventListener('click', closeSheet);
handle.addEventListener('click', closeSheet);

chips.forEach(chip => chip.addEventListener('click', () => {
  chip.classList.toggle('chip-on');
  applyFilters();
}));

resetFilters.addEventListener('click', () => {
  chips.forEach(chip => chip.classList.remove('chip-on'));
  applyFilters();
});

let startY = 0, startX = 0, dragging = false;
sheet.addEventListener('touchstart', e => {
  if(!e.touches.length) return;
  startY=e.touches[0].clientY;
  startX=e.touches[0].clientX;
  dragging=true;
  sheet.style.transition='none';
}, {passive:true});
sheet.addEventListener('touchmove', e => {
  if(!dragging || !e.touches.length) return;
  const dy=e.touches[0].clientY-startY;
  if(dy>0 && sheet.scrollTop <= 0){
    e.preventDefault();
    sheet.style.transform=`translate(-50%, ${Math.min(dy,260)}px)`;
  }
}, {passive:false});
sheet.addEventListener('touchend', e => {
  if(!dragging) return;
  dragging=false;
  const touch=e.changedTouches[0];
  const dy=touch.clientY-startY;
  const dx=Math.abs(touch.clientX-startX);
  if(dy>70 && dx<100 && sheet.scrollTop <= 5){
    closeSheet();
  } else {
    sheet.style.transition='transform .18s ease';
    sheet.style.transform='translate(-50%, 0)';
  }
}, {passive:true});

applyFilters();
</script>
</body>
</html>
"""

CATALOG_HTML = CATALOG_TEMPLATE.replace("__CARDS__", cards_html)

if current_page == "catalog":
    components.html(CATALOG_HTML, height=900, scrolling=False)
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
