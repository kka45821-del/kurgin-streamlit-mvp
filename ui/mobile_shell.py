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


def _catalog_section_fix_script() -> str:
    return r"""
// Public catalog section UX:
// - show all published stones by default;
// - keep professional sections available;
// - show section counts so the user does not confuse total catalog count with one section.
(function(){
  if(!document.getElementById('catalogStatsStyle')){
    const style = document.createElement('style');
    style.id = 'catalogStatsStyle';
    style.textContent = `
      .catalogStats{display:grid;grid-template-columns:repeat(3,1fr);gap:.4rem;padding:0 1rem .65rem}
      .catalogStat{border:1px solid #dedede;border-radius:13px;background:#fff;padding:.55rem .55rem;text-align:center;box-shadow:0 8px 18px rgba(0,0,0,.035)}
      .catalogStat strong{display:block;font-size:.98rem;line-height:1;color:#111}
      .catalogStat span{display:block;margin-top:.22rem;font-size:.58rem;letter-spacing:.04em;text-transform:uppercase;color:#777}
      .price.request{font-size:.72rem;line-height:1.1;color:#666;white-space:normal;text-align:right;font-weight:600}
      .detailPrice.request{font-size:.9rem;color:#666;white-space:normal;text-align:right;line-height:1.25}
      .act.disabled,.detailBtn.disabled{opacity:.38;pointer-events:none;filter:grayscale(1)}
    `;
    document.head.appendChild(style);
  }

  if(Array.isArray(sections) && !sections.find(x => x[0] === 'all')){
    sections.unshift(['all', 'Все камни', 'все разделы']);
  }

  function sectionCount(id){
    if(id === 'all') return stones.length;
    return stones.filter(x => x.section === id).length;
  }

  function currentSectionLabel(){
    const section = sections.find(x => x[0] === activeSection) || sections[0];
    return section;
  }

  function isRequestPrice(stone){
    const price = Number(stone.price || stone.price_rub || stone.public_price_rub || 0);
    const status = String(stone.price_status || '').toLowerCase();
    const action = String(stone.public_action || '').toLowerCase();
    const checkoutEnabled = stone.checkout_enabled === true || String(stone.checkout_enabled).toLowerCase() === 'true';
    const publicSellable = stone.public_sellable === true || String(stone.public_sellable).toLowerCase() === 'true';
    return price <= 0 || ['request_price','missing','score_required','future_scope','blocked','needs_review','index_pending','index_suggested'].includes(status) || action === 'request_price' || !checkoutEnabled || !publicSellable;
  }

  function priceHtml(stone, detail=false){
    if(isRequestPrice(stone)){
      return detail ? `<div class='detailPrice request'>Цена<br>по запросу</div>` : `<div class='price request'>по<br>запросу</div>`;
    }
    const price = Number(stone.price || stone.price_rub || stone.public_price_rub || 0);
    const priceText = (stone.priceText && stone.priceText !== '0') ? stone.priceText : String(price);
    return detail ? `<div class=detailPrice>${priceText} ₽</div>` : `<div class=price>${priceText} ₽</div>`;
  }

  function actionHtml(stone){
    const cartClass = isRequestPrice(stone) ? 'act disabled' : 'act';
    return `<button class=act data-stop=1>${icon('message')}</button><button class=act data-stop=1>${icon('reserve')}</button><button class='act infoBtn'>${icon('info')}</button><button class=act data-stop=1>${icon('heart')}</button><button class='${cartClass}' data-stop=1>${icon('shopping')}</button><button class=act data-stop=1>${icon('share')}</button>`;
  }

  window.source = function source(){
    let a = activeSection === 'all' ? stones : stones.filter(x => x.section === activeSection);
    if(sort === 'new') return a;
    let [k, d] = sort.split('_');
    return [...a].sort((x, y) => {
      let xv = Number(x[k] || 0), yv = Number(y[k] || 0);
      return d === 'asc' ? xv - yv : yv - xv;
    });
  };

  window.drawMenu = function drawMenu(){
    catalogMenu.innerHTML=sections.map((s,i)=>`${i===5?'<div class=sep></div>':''}<button class='${s[0]===activeSection?'active':''}' data-id='${s[0]}'><div class=m-title>${s[1]}</div><div class=m-sub>${sectionCount(s[0])} камней${s[2]?` · ${s[2]}`:''}</div></button>`).join('');
    catalogMenu.querySelectorAll('button').forEach(b=>b.onclick=()=>{
      activeSection=b.dataset.id;
      let s=currentSectionLabel();
      sectionTitle.textContent=s[1];
      sectionSub.textContent=`${sectionCount(s[0])} камней${s[2]?` · ${s[2]}`:''}`;
      catalogBox.classList.remove('open');
      drawMenu();
      renderCards();
    });
  };

  window.renderCatalogPage = function renderCatalogPage(){
    if(!activeSection) activeSection='all';
    let s=currentSectionLabel();
    content.innerHTML = pageHeader(pageTitles.catalog, pageSubtitles.catalog) + `
      <div class='top'><div class='catalogBox' id='catalogBox'><button class='select' id='catalogBtn'><div><div class='select-title' id='sectionTitle'>${s[1]}</div><div class='select-sub' id='sectionSub'>${sectionCount(s[0])} камней${s[2]?` · ${s[2]}`:''}</div></div><div class='chev'><svg viewBox='0 0 20 20'><path d='M5 8l5 5 5-5'/></svg></div></button><div class='menu' id='catalogMenu'></div></div><div class='pick'>Индив.<br>подбор</div></div>
      <div class='catalogStats' id='catalogStats'><div class='catalogStat'><strong>${stones.length}</strong><span>всего</span></div><div class='catalogStat'><strong>${sectionCount('main')}</strong><span>основной</span></div><div class='catalogStat'><strong>${sectionCount('large')}</strong><span>крупные</span></div></div>
      <div class='cols'><div>ФОРМА</div><div>КАРАТ</div><div>ЦВЕТ</div><div>ЧИСТОТА</div><div>KURGIN SCORE</div><div>ЦЕНА</div></div>
      <div id='cards'></div><div class='empty' id='empty'>По выбранному разделу и фильтрам камни не найдены</div>`;
    setupCatalog();
    content.scrollTop = 0;
  };

  window.renderCards = function renderCards(){
    if(!document.getElementById('cards')) return;
    sortLabel.textContent=sortLabels[sort];
    document.querySelectorAll('.sort').forEach(b=>b.classList.toggle('on',b.dataset.sort===sort));
    cards.innerHTML=source().map(s=>`<div class=card data-idx='${stones.indexOf(s)}' data-shape='${shapeKey(s)}' data-weight='${s.weight||''}' data-color='${s.color||''}' data-clarity='${s.clarity||''}' data-score='${s.scoreBand||''}' data-fluorescence='${s.fluor||s.fluorescence||''}' data-finish='${s.finish||''}'><div class=main><div>${s.shape||''}</div><div>${Number(s.carat||0).toFixed(2).replace('.00','')}</div><div>${s.color||''}</div><div>${s.clarity||''}</div><div class=scoreValue>${s.score||''}</div>${priceHtml(s)}</div><div class=line></div><div class=meta><div>${s.meta||''}</div><div class=tags>${mkTags(s.score,s.tags)}</div></div><div class=actions>${actionHtml(s)}</div></div>`).join('');
    wireCards();
    filter();
  };

  window.openDetail = function openDetail(i){
    let s=stones[i];
    const cartClass = isRequestPrice(s) ? 'detailBtn dark disabled' : 'detailBtn dark';
    const cartLabel = isRequestPrice(s) ? 'Запросить цену' : 'В корзину';
    detailContent.innerHTML=`<div class=detailTop><div><div class=detailName>${s.shape||''} ${Number(s.carat||0).toFixed(2).replace('.00','')} ct</div><div class=tags style='justify-content:flex-start;margin-top:.55rem'>${mkTags(s.score,s.tags)}</div></div>${priceHtml(s,true)}</div><div class=detailGrid><div class=detailCell><div class=detailLabel>Цвет</div><div class=detailValue>${s.color||''}</div></div><div class=detailCell><div class=detailLabel>Чистота</div><div class=detailValue>${s.clarity||''}</div></div><div class=detailCell><div class=detailLabel>KURGIN Score</div><div class='detailValue scoreBold'>${s.score||''}</div></div><div class=detailCell><div class=detailLabel>Диаметр</div><div class=detailValue>${s.diameter||''} мм</div></div><div class=detailCell><div class=detailLabel>Флюоресценция</div><div class=detailValue>${s.fluor||s.fluorescence||''}</div></div><div class=detailCell><div class=detailLabel>Отделка</div><div class=detailValue>${s.finish||''}</div></div></div><div class=detailNote>Сертификат: ${s.report||''}<br>${s.meta||''}<br>Подробная профессиональная карточка будет расширяться: параметры, пропорции, световое поведение и условия резерва.</div><div class=detailActions><button class='${cartClass}'>${cartLabel}</button><button class=detailBtn>В избранное</button></div>`;
    open('detail');
  };

  if(currentPage === 'catalog'){
    activeSection = activeSection || 'all';
    renderCatalogPage();
  }
})();
"""


def _public_score_label_script() -> str:
    return r"""
function applyPublicScoreLabel(){
  var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  var nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);
  nodes.forEach(function(node){
    if (!node.nodeValue) return;
    node.nodeValue = node.nodeValue
      .replace(/KARO SCORE/g, 'KURGIN SCORE')
      .replace(/Karo Score/g, 'KURGIN Score');
  });
}
applyPublicScoreLabel();
document.addEventListener('click', function(){ setTimeout(applyPublicScoreLabel, 0); }, true);
"""


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
{_catalog_section_fix_script()}
{_public_score_label_script()}
</script>
</body>
</html>
"""
