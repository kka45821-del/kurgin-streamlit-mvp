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
.block-container { max-width: 430px; padding: 0; }
iframe { display: block; }
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

CATALOG_HTML = r"""
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<style>
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: #fff; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: #111; }
body { overflow: hidden; }
.app { max-width: 430px; height: 820px; margin: 0 auto; position: relative; overflow: hidden; background: #fff; }
.content { position: absolute; inset: 0 0 126px 0; overflow-y: auto; -webkit-overflow-scrolling: touch; padding-bottom: 20px; }
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
.stone-main { align-items:start; font-size:.98rem; color:#111; }
.price { font-weight:700; text-align:right; font-size:.98rem; line-height:1.25; white-space:nowrap; }
.stone-line { border-top:1px solid #e6e6e6; margin:1.05rem 0 .7rem; }
.stone-meta { display:flex; justify-content:space-between; align-items:center; color:#666; font-size:.86rem; gap:.5rem; }
.tags { display:flex; gap:.35rem; flex-wrap:wrap; justify-content:flex-end; }
.tag { border:1px solid #f0c56d; color:#c77c16; border-radius:7px; padding:.08rem .45rem; font-size:.7rem; }
.tag-blue { border-color:#8bd7e8; color:#1892ad; }
.tag-gray { border-color:#ccc; color:#555; }
.actions { display:grid; grid-template-columns:repeat(6,1fr); color:#888; font-size:1.25rem; padding-top:.85rem; text-align:center; }
.bottom-controls { position:absolute; left:0; right:0; bottom:64px; z-index:30; background:#fff; border-top:1px solid #ddd; padding:.5rem .8rem; display:grid; grid-template-columns:1fr 1fr; gap:.65rem; }
.control-box { border:1px solid #c9c9c9; border-radius:14px; min-height:64px; background:#fff; text-align:left; padding:.55rem .8rem; color:#111; }
.control-label { color:#aaa; font-size:.72rem; letter-spacing:.04em; }
.control-value { font-weight:700; font-size:.92rem; margin-top:.12rem; }
.bottom-nav { position:absolute; left:0; right:0; bottom:0; z-index:30; background:#fff; border-top:1px solid rgba(49,51,63,.18); padding:.25rem .25rem calc(.45rem + env(safe-area-inset-bottom)); }
.nav-grid { display:grid; grid-template-columns:repeat(6,1fr); gap:.2rem; }
.nav-tab { display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:52px; border-radius:12px; color:#888; text-decoration:none; font-size:.68rem; line-height:1.1; white-space:nowrap; }
.nav-active { background:#f2f5f8; color:#111; border:1px solid #cfd5dc; }
.nav-icon { font-size:1.15rem; line-height:1; margin-bottom:.15rem; }
.overlay { display:none; position:absolute; inset:0; z-index:50; background:rgba(0,0,0,.22); }
.sheet { position:absolute; left:0; right:0; bottom:0; z-index:60; max-height:calc(100% - 70px); overflow-y:auto; -webkit-overflow-scrolling:touch; background:#fff; border:1px solid #999; border-bottom:0; border-radius:26px 26px 0 0; padding:1.4rem 1.35rem 1.2rem; box-shadow:0 -6px 22px rgba(0,0,0,.18); transform:translateY(110%); transition:transform .22s ease; touch-action:pan-y; }
.sheet-open .overlay { display:block; }
.sheet-open .sheet { transform:translateY(0); }
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
  <div class="content">
    <div class="catalog-header"><div class="logo-mark"></div><div><div class="logo-title">KURGIN DIAMONDS</div><div class="logo-sub">ЛАБОРАТОРНЫЕ БРИЛЛИАНТЫ</div></div></div>
    <div class="catalog-top"><div class="catalog-select"><div><div class="select-title">Основной каталог</div><div class="select-sub">1.00–2.99 ct</div></div><div>⌄</div></div><div class="catalog-pick">Индив.<br>подбор</div></div>
    <div class="catalog-cols"><div>ФОРМА</div><div>КАРАТ</div><div>ЦВЕТ</div><div>ЧИСТОТА</div><div>KARO SCORE</div><div>ЦЕНА</div></div>
    <div class="stone-card"><div class="stone-main"><div>Круг</div><div>1.05</div><div>G</div><div>VVS1</div><div>95</div><div class="price">32 200 ₽</div></div><div class="stone-line"></div><div class="stone-meta"><div>6.5 мм · ex ex vg · none</div><div class="tags"><span class="tag">огонь</span><span class="tag tag-blue">блеск</span></div></div><div class="actions"><div>♡</div><div>▣</div><div>ⓘ</div><div>♡</div><div>⌞</div><div>⌯</div></div></div>
    <div class="stone-card"><div class="stone-main"><div>Круг</div><div>1.51</div><div>E</div><div>VS1</div><div>86</div><div class="price">58 500 ₽</div></div><div class="stone-line"></div><div class="stone-meta"><div>7.4 мм · ex ex vg · none</div><div class="tags"><span class="tag tag-gray">контраст</span><span class="tag">огонь</span></div></div><div class="actions"><div>♡</div><div>▣</div><div>ⓘ</div><div>♡</div><div>⌞</div><div>⌯</div></div></div>
    <div class="stone-card"><div class="stone-main"><div>Круг</div><div>1</div><div>F</div><div>VS2</div><div>77</div><div class="price">34 900 ₽</div></div><div class="stone-line"></div><div class="stone-meta"><div>6.4 мм · ex ex vg · none</div><div class="tags"><span class="tag">БАЛАНС</span></div></div><div class="actions"><div>♡</div><div>▣</div><div>ⓘ</div><div>♡</div><div>⌞</div><div>⌯</div></div></div>
    <div class="stone-card"><div class="stone-main"><div>Круг</div><div>1.22</div><div>D</div><div>VVS2</div><div>92</div><div class="price">41 800 ₽</div></div><div class="stone-line"></div><div class="stone-meta"><div>6.9 мм · ex ex ex · none</div><div class="tags"><span class="tag tag-blue">блеск</span><span class="tag">огонь</span></div></div><div class="actions"><div>♡</div><div>▣</div><div>ⓘ</div><div>♡</div><div>⌞</div><div>⌯</div></div></div>
    <div class="stone-card"><div class="stone-main"><div>Круг</div><div>1.74</div><div>F</div><div>VS1</div><div>89</div><div class="price">67 900 ₽</div></div><div class="stone-line"></div><div class="stone-meta"><div>7.8 мм · ex ex vg · faint</div><div class="tags"><span class="tag tag-gray">контраст</span><span class="tag tag-blue">блеск</span></div></div><div class="actions"><div>♡</div><div>▣</div><div>ⓘ</div><div>♡</div><div>⌞</div><div>⌯</div></div></div>
    <div class="stone-card"><div class="stone-main"><div>Круг</div><div>2.03</div><div>G</div><div>VS2</div><div>84</div><div class="price">88 400 ₽</div></div><div class="stone-line"></div><div class="stone-meta"><div>8.1 мм · ex vg vg · none</div><div class="tags"><span class="tag">БАЛАНС</span></div></div><div class="actions"><div>♡</div><div>▣</div><div>ⓘ</div><div>♡</div><div>⌞</div><div>⌯</div></div></div>
    <div class="stone-card"><div class="stone-main"><div>Круг</div><div>2.41</div><div>E</div><div>VVS1</div><div>96</div><div class="price">126 300 ₽</div></div><div class="stone-line"></div><div class="stone-meta"><div>8.7 мм · ex ex ex · none</div><div class="tags"><span class="tag">огонь</span><span class="tag tag-blue">блеск</span></div></div><div class="actions"><div>♡</div><div>▣</div><div>ⓘ</div><div>♡</div><div>⌞</div><div>⌯</div></div></div>
  </div>
  <div class="bottom-controls"><button class="control-box"><div class="control-label">СОРТИРОВКА</div><div class="control-value">по Karo Score ↓</div></button><button class="control-box" id="openFilters"><div class="control-label">ФИЛЬТРЫ</div><div class="control-value">☷ Параметры</div></button></div>
  <nav class="bottom-nav"><div class="nav-grid"><a class="nav-tab" href="?page=kurgin" target="_parent"><span class="nav-icon">♢</span><span>KURGIN</span></a><a class="nav-tab" href="?page=tools" target="_parent"><span class="nav-icon">♢</span><span>Инстр.</span></a><a class="nav-tab nav-active" href="?page=catalog" target="_parent"><span class="nav-icon">◇</span><span>Каталог</span></a><a class="nav-tab" href="?page=favorites" target="_parent"><span class="nav-icon">♡</span><span>Избр.</span></a><a class="nav-tab" href="?page=cart" target="_parent"><span class="nav-icon">◠</span><span>Корзина</span></a><a class="nav-tab" href="?page=profile" target="_parent"><span class="nav-icon">○</span><span>Профиль</span></a></div></nav>
  <div class="overlay" id="overlay"></div>
  <div class="sheet" id="sheet">
    <div class="sheet-handle" id="handle"></div>
    <div class="sheet-head"><div class="sheet-title">Фильтры</div><button class="reset" id="resetFilters">Сбросить</button></div>
    <div class="filter-group"><div class="filter-name">1. Форма / огранка</div><div class="chips"><button class="chip chip-on">Round</button><button class="chip">Oval</button><button class="chip">Pear</button><button class="chip">Cushion</button></div></div>
    <div class="filter-group"><div class="filter-name">2. Вес</div><div class="chips"><button class="chip chip-on">1–1.49</button><button class="chip">1.5–1.99</button><button class="chip">2–2.49</button><button class="chip">2.5–2.99</button></div></div>
    <div class="filter-group"><div class="filter-name">3. Цвет</div><div class="chips"><button class="chip chip-on">D</button><button class="chip chip-on">E</button><button class="chip chip-on">F</button><button class="chip">G</button><button class="chip">H</button></div></div>
    <div class="filter-group"><div class="filter-name">4. Чистота</div><div class="chips"><button class="chip">IF</button><button class="chip chip-on">VVS1</button><button class="chip">VVS2</button><button class="chip chip-on">VS1</button><button class="chip">VS2</button></div></div>
    <div class="filter-group"><div class="filter-name">5. Karo Score</div><div class="chips"><button class="chip">0–49</button><button class="chip">50–79</button><button class="chip chip-on">80–89</button><button class="chip">90–94.9</button><button class="chip">95–98</button><button class="chip">99+</button><span class="chip-note">качество / индекс-коэф.</span></div></div>
    <div class="filter-group"><div class="filter-name">6. Флюоресценция</div><div class="chips"><button class="chip chip-on">None</button><button class="chip">Faint</button><button class="chip">Medium</button><button class="chip">Strong</button></div></div>
    <div class="filter-group"><div class="filter-name">7. Качество отделки</div><div class="chips"><button class="chip chip-on">Ex/Ex/Ex+</button><button class="chip">2Ex/1VG+</button></div></div>
  </div>
</div>
<script>
const app = document.getElementById('app');
const sheet = document.getElementById('sheet');
const overlay = document.getElementById('overlay');
const openFilters = document.getElementById('openFilters');
const resetFilters = document.getElementById('resetFilters');
const handle = document.getElementById('handle');
function openSheet(){ app.classList.add('sheet-open'); sheet.style.transition='transform .22s ease'; sheet.style.transform='translateY(0)'; }
function closeSheet(){ sheet.style.transition='transform .22s ease'; sheet.style.transform='translateY(110%)'; setTimeout(()=>app.classList.remove('sheet-open'),180); }
openFilters.addEventListener('click', openSheet);
overlay.addEventListener('click', closeSheet);
handle.addEventListener('click', closeSheet);
document.querySelectorAll('.chip').forEach(chip => chip.addEventListener('click', () => chip.classList.toggle('chip-on')));
resetFilters.addEventListener('click', () => document.querySelectorAll('.chip').forEach(chip => chip.classList.remove('chip-on')));
let startY = 0, startX = 0, dragging = false;
sheet.addEventListener('touchstart', e => { if(!e.touches.length) return; startY=e.touches[0].clientY; startX=e.touches[0].clientX; dragging=true; sheet.style.transition='none'; }, {passive:true});
sheet.addEventListener('touchmove', e => { if(!dragging || !e.touches.length) return; const dy=e.touches[0].clientY-startY; if(dy>0){ sheet.style.transform=`translateY(${Math.min(dy,260)}px)`; } }, {passive:true});
sheet.addEventListener('touchend', e => { if(!dragging) return; dragging=false; const touch=e.changedTouches[0]; const dy=touch.clientY-startY; const dx=Math.abs(touch.clientX-startX); if(dy>80 && dx<100){ closeSheet(); } else { sheet.style.transition='transform .18s ease'; sheet.style.transform='translateY(0)'; } }, {passive:true});
</script>
</body>
</html>
"""

if current_page == "catalog":
    components.html(CATALOG_HTML, height=820, scrolling=False)
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
