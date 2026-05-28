import json

from config.request_contacts import REQUEST_CONTACTS
from ui.extra_styles import SYSTEM_CSS
from ui.pages.cart_page import render_cart_page
from ui.pages.favorites_page import render_favorites_page
from ui.pages.kurgin_page import render_kurgin_page
from ui.pages.profile_page import render_profile_page
from ui.pages.tools_page import render_tools_page
from ui.scripts import catalog_script
from ui.styles import BASE_CSS

LOGO_URL = "https://raw.githubusercontent.com/kka45821-del/kurgin-streamlit-mvp/main/Vectorr-header.svg?v=1"

PAGE_TITLES = {
    "kurgin": "KURGIN",
    "tools": "KURGIN Tools",
    "catalog": "KURGIN <span>Diamonds</span>",
    "favorites": "Избранное",
    "cart": "Заявки / Корзина",
    "profile": "Профиль",
}

PAGE_SUBTITLES = {
    "kurgin": "платформа лабораторных бриллиантов",
    "tools": "инструменты анализа и подбора",
    "catalog": "лабораторные бриллианты",
    "favorites": "сохранённые камни",
    "cart": "будущий checkout не активен",
    "profile": "аккаунт и профессиональный доступ позже",
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
// - keep favorites as a browser-only saved-stone flow;
// - keep filters and sorting stable in the active mobile shell layer;
// - never create checkout, payment, order, reserve or ownership states.
(function(){
  const requestContactConfig = __REQUEST_CONTACTS_JSON__;
  const requestContact = {
    phone: requestContactConfig.phone || '',
    maxUrl: requestContactConfig.max_url || '',
    telegramUrl: requestContactConfig.telegram_url || '',
    whatsappUrl: requestContactConfig.whatsapp_url || ''
  };
  const favoritesStorageKey = 'kurginFavoritesV01';

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
      .act.favoriteToggle.on{color:#111;border-color:#111;background:#f7f4ee}
      .act.requestDetailBtn{color:#111}
      .detailBtn.favoriteOn{border-color:#111;background:#f7f4ee;color:#111}
      .nav a{position:relative}
      .favBadge{position:absolute;top:.12rem;right:.22rem;min-width:15px;height:15px;border-radius:999px;background:#111;color:#fff;font-size:.55rem;line-height:15px;text-align:center;font-weight:700}
      .requestBox{margin:1rem 0 .75rem;border:1px solid #e4e0d8;border-radius:18px;background:#fff;padding:.85rem;box-shadow:0 10px 24px rgba(0,0,0,.045)}
      .requestTitle{font-size:.78rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#111;margin-bottom:.35rem}
      .requestHint{font-size:.72rem;line-height:1.35;color:#666;margin-bottom:.75rem}
      .requestChannels{display:grid;grid-template-columns:1.2fr 1fr 1fr;gap:.45rem}
      .requestBtn{display:flex;align-items:center;justify-content:center;min-height:38px;border:1px solid #d9d4ca;border-radius:13px;background:#fff;color:#111;text-decoration:none;font-size:.76rem;font-weight:700}
      .requestBtn.primary{background:#111;color:#fff;border-color:#111}
      .requestBtn.disabled{opacity:.45;pointer-events:none;color:#777;background:#f4f3f1}
      .favoritesInfo{margin:0 1rem .75rem;padding:.8rem;border:1px solid #e5e0d8;border-radius:16px;background:#fff;font-size:.75rem;line-height:1.35;color:#666}
      .favoriteList{display:grid;gap:.7rem;padding:0 1rem 1rem}
      .favoriteCard{border:1px solid #ddd8ce;border-radius:18px;background:#fff;padding:.85rem;box-shadow:0 10px 24px rgba(0,0,0,.035)}
      .favoriteTop{display:flex;justify-content:space-between;gap:.75rem;align-items:flex-start}
      .favoriteName{font-size:.95rem;font-weight:700;color:#111}
      .favoriteMeta{font-size:.72rem;color:#666;margin-top:.3rem;line-height:1.35}
      .favoritePrice{font-size:.78rem;font-weight:700;text-align:right;color:#111;white-space:nowrap}
      .favoriteGrid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:.45rem;margin-top:.75rem}
      .favoriteCell{border:1px solid #eee;border-radius:12px;background:#fafafa;padding:.5rem .55rem;min-height:46px}
      .favoriteCell span{display:block;font-size:.58rem;letter-spacing:.04em;text-transform:uppercase;color:#888;margin-bottom:.18rem}
      .favoriteCell strong{display:block;font-size:.78rem;line-height:1.2;color:#111;font-weight:700;word-break:break-word}
      .favoriteSafety{margin-top:.65rem;font-size:.68rem;line-height:1.35;color:#666;background:#f7f7f7;border-radius:12px;padding:.55rem}
      .favoriteUnavailable{margin-top:.65rem;font-size:.72rem;line-height:1.35;color:#8a5b00;background:#fff7df;border-radius:12px;padding:.55rem}
      .favoriteActions{display:grid;grid-template-columns:1fr 1fr;gap:.45rem;margin-top:.75rem}
      .favoriteBtn{border:1px solid #d9d4ca;border-radius:13px;background:#fff;color:#111;font-size:.75rem;font-weight:700;min-height:36px}
      .favoriteBtn.dark{background:#111;color:#fff;border-color:#111}.favoriteBtn.danger{color:#8a1c1c}
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

  function escapeHtml(value){
    return String(value ?? '').replace(/[&<>'"]/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));
  }

  window.catalogNormalizeFilterValue = window.catalogNormalizeFilterValue || function catalogNormalizeFilterValue(group, value){
    const raw = String(value || '').trim();
    const v = raw.toLowerCase().replace(/ё/g,'е').replace(/,/g,'.').replace(/\s+/g,' ');
    if(group === 'shape'){
      if(['round','круг','круглый'].includes(v)) return 'round';
      if(v.includes('oval') || v.includes('овал')) return 'oval';
      if(v.includes('pear') || v.includes('капля')) return 'pear';
      if(v.includes('cushion') || v.includes('кушон')) return 'cushion';
    }
    if(group === 'color' || group === 'clarity') return raw.toUpperCase();
    if(group === 'fluorescence'){
      if(!v || v === 'none' || v === 'no' || v === 'нет') return 'none';
      if(v.includes('faint')) return 'faint';
      if(v.includes('medium')) return 'medium';
      if(v.includes('strong')) return 'strong';
    }
    if(group === 'finish') return v.toUpperCase().replace(/[\/\-+\s]/g,'');
    return raw;
  };

  window.finishMatches = window.finishMatches || function finishMatches(actual, selected){
    const normalizedActual = window.catalogNormalizeFilterValue('finish', actual);
    const normalizedSelected = window.catalogNormalizeFilterValue('finish', selected);
    if(!normalizedSelected) return true;
    if(normalizedActual === normalizedSelected) return true;
    const text = String(actual || '').toUpperCase();
    const exCount = (text.match(/EX/g) || []).length;
    const vgCount = (text.match(/VG/g) || []).length;
    if(normalizedSelected === 'EXEXEX' || normalizedSelected === '3EX') return exCount >= 3;
    if(normalizedSelected === '2EX1VG') return exCount >= 2 && (vgCount >= 1 || exCount >= 3);
    return false;
  };

  window.filterMatches = window.filterMatches || function filterMatches(group, actual, selected){
    if(group === 'finish') return window.finishMatches(actual, selected);
    return window.catalogNormalizeFilterValue(group, actual) === window.catalogNormalizeFilterValue(group, selected);
  };

  window.catalogSortNumber = function catalogSortNumber(stone, key, direction){
    let value = stone ? stone[key] : '';
    if(key === 'diameter'){
      const match = String(value || '').replace(',', '.').match(/\d+(?:\.\d+)?/);
      value = match ? match[0] : '';
    }
    const number = Number(value || 0);
    if(Number.isFinite(number) && number > 0) return number;
    return direction === 'asc' ? Number.POSITIVE_INFINITY : Number.NEGATIVE_INFINITY;
  };

  function stoneKey(stone){
    return String((stone && (stone.id || stone.stone_id || stone.report)) || '');
  }

  function getFavorites(){
    try{
      const raw = window.localStorage.getItem(favoritesStorageKey);
      const parsed = raw ? JSON.parse(raw) : [];
      return Array.isArray(parsed) ? parsed : [];
    }catch(e){ return []; }
  }

  function saveFavorites(items){
    const safeItems = Array.isArray(items) ? items : [];
    window.localStorage.setItem(favoritesStorageKey, JSON.stringify(safeItems));
  }

  function favoriteSnapshot(stone){
    return {
      shape: stone.shape || '',
      carat: stone.carat || '',
      color: stone.color || '',
      clarity: stone.clarity || '',
      score: stone.score || stone.karo_score || '',
      priceText: stone.priceText || stone.priceDisplay || (isRequestPrice(stone) ? 'по запросу' : ''),
      price_status: stone.price_status || '',
      public_action: stone.public_action || 'request_price',
      diameter: stone.diameter || '',
      fluor: stone.fluor || stone.fluorescence || '',
      finish: stone.finish || '',
      report: stone.report || ''
    };
  }

  function addFavorite(stone){
    const id = stoneKey(stone);
    if(!id) return;
    const items = getFavorites().filter(x => String(x.stone_id) !== id);
    items.unshift({stone_id:id, added_at:new Date().toISOString(), snapshot:favoriteSnapshot(stone)});
    saveFavorites(items);
  }

  function removeFavorite(stoneId){
    const id = String(stoneId || '');
    saveFavorites(getFavorites().filter(x => String(x.stone_id) !== id));
  }

  function isFavorite(stoneOrId){
    const id = typeof stoneOrId === 'object' ? stoneKey(stoneOrId) : String(stoneOrId || '');
    return !!id && getFavorites().some(x => String(x.stone_id) === id);
  }

  function toggleFavorite(stone){
    const id = stoneKey(stone);
    if(!id) return false;
    if(isFavorite(id)){
      removeFavorite(id);
      return false;
    }
    addFavorite(stone);
    return true;
  }

  window.getFavorites = getFavorites;
  window.saveFavorites = saveFavorites;
  window.addFavorite = addFavorite;
  window.removeFavorite = removeFavorite;
  window.isFavorite = isFavorite;
  window.toggleFavorite = toggleFavorite;

  function favoritesCount(){ return getFavorites().length; }

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

  function displayPriceText(stone){
    if(!stone) return 'по запросу';
    if(isRequestPrice(stone)) return 'по запросу';
    const price = Number(stone.price || stone.price_rub || stone.public_price_rub || 0);
    const priceText = (stone.priceText && stone.priceText !== '0') ? stone.priceText : String(price || '');
    return priceText ? `${priceText} ₽` : 'по запросу';
  }

  function requestMessage(stone, requestType){
    const parts = [
      'Здравствуйте. Хочу уточнить информацию по камню KURGIN.',
      `Тип заявки: ${requestType || 'request_price'}`,
      `ID: ${stone.id || stone.stone_id || ''}`,
      `Камень: ${stone.shape || ''} ${stone.carat || ''} ct / ${stone.color || ''} / ${stone.clarity || ''}`,
      `KURGIN Score: ${stone.score || stone.karo_score || ''}`,
      `Статус цены: ${stone.price_status || 'request_price'}`,
      '',
      'Понимаю, что это не заказ, не резерв и не фиксация цены.'
    ];
    return parts.join('\n');
  }

  function channelLink(channel, stone){
    const message = encodeURIComponent(requestMessage(stone, 'request_price'));
    if(channel === 'max') return requestContact.maxUrl || '';
    if(channel === 'telegram'){
      if(!requestContact.telegramUrl) return '';
      return requestContact.telegramUrl + (requestContact.telegramUrl.includes('?') ? '&' : '?') + 'text=' + message;
    }
    if(channel === 'whatsapp') return requestContact.whatsappUrl ? `${requestContact.whatsappUrl}?text=${message}` : '';
    return '';
  }

  function requestButton(channel, label, stone, primary=false){
    const href = channelLink(channel, stone);
    const cls = `requestBtn${primary ? ' primary' : ''}${href ? '' : ' disabled'}`;
    if(!href) return `<span class='${cls}'>${label}</span>`;
    return `<a class='${cls}' href='${href}' target='_blank' rel='noopener noreferrer'>${label}</a>`;
  }

  function requestChannelsHtml(stone){
    return `<div class='requestBox'><div class='requestTitle'>Запросить условия</div><div class='requestHint'>Заявка не является заказом, резервом, оплатой или фиксацией цены. Менеджер уточнит наличие, цену и условия. Контакт: ${requestContact.phone}</div><div class='requestChannels'>${requestButton('max','MAX',stone,true)}${requestButton('telegram','Telegram',stone,false)}${requestButton('whatsapp','WhatsApp',stone,false)}</div></div>`;
  }

  function actionHtml(stone){
    const favClass = isFavorite(stone) ? 'act favoriteToggle on' : 'act favoriteToggle';
    return `<button class='act requestDetailBtn' data-stop=1 title='Запросить условия'>${icon('message')}</button><button class='act disabled' data-stop=1 title='Действие недоступно в MVP'>${icon('reserve')}</button><button class='act infoBtn'>${icon('info')}</button><button class='${favClass}' data-stop=1 data-favorite-id='${stoneKey(stone)}'>${icon('heart')}</button><button class='act disabled' data-stop=1 title='Checkout недоступен в MVP'>${icon('shopping')}</button><button class='act disabled' data-stop=1 title='Share недоступен в MVP'>${icon('share')}</button>`;
  }

  window.renderNav = function renderNav(){
    const items=[['kurgin','menu'],['tools','tools'],['catalog','catalog'],['favorites','favorites'],['cart','cart'],['profile','profile']];
    const count = favoritesCount();
    navGrid.innerHTML=items.map(i=>`<a class='${i[0]===currentPage?'active':''}' href='?page=${i[0]}' data-nav-page='${i[0]}'><span class='ico'>${icon(i[1])}</span>${i[0]==='favorites'&&count>0?`<span class='favBadge'>${count}</span>`:''}</a>`).join('');
  };

  window.source = function source(){
    let a = activeSection === 'all' ? stones : stones.filter(x => x.section === activeSection);
    if(sort === 'new') return a;
    let [k, d] = sort.split('_');
    return [...a].sort((x, y) => {
      let xv = window.catalogSortNumber(x, k, d), yv = window.catalogSortNumber(y, k, d);
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
      <div id='cards'></div><div class='empty' id='empty'>По выбранным фильтрам камни не найдены.<br><button class='btn light' type='button' data-reset-filters>Сбросить фильтры</button></div>`;
    setupCatalog();
    content.scrollTop = 0;
  };

  window.renderCards = function renderCards(){
    if(!document.getElementById('cards')) return;
    sortLabel.textContent=sortLabels[sort];
    document.querySelectorAll('.sort').forEach(b=>b.classList.toggle('on',b.dataset.sort===sort));
    cards.innerHTML=source().map(s=>`<div class=card data-idx='${stones.indexOf(s)}' data-shape='${shapeKey(s)}' data-weight='${s.weight||''}' data-color='${s.color||''}' data-clarity='${s.clarity||''}' data-score='${s.scoreBand||''}' data-fluorescence='${s.fluor||s.fluorescence||''}' data-finish='${s.finish||''}'><div class=main><div>${s.shape||''}</div><div>${Number(s.carat||0).toFixed(2).replace('.00','')}</div><div>${s.color||''}</div><div>${s.clarity||''}</div><div class=scoreValue>${s.score||''}</div>${priceHtml(s)}</div><div class=line></div><div class=meta><div>${s.meta||''}</div><div class=tags>${mkTags(s.score,s.tags)}</div></div><div class=actions>${actionHtml(s)}</div></div>`).join('');
    wireCards();
    wireFavoriteButtons();
    wireRequestButtons();
    filter();
  };

  function wireFavoriteButtons(){
    document.querySelectorAll('.favoriteToggle').forEach(button=>{
      button.onclick = event => {
        event.stopPropagation();
        const card = button.closest('.card');
        const stone = card ? stones[Number(card.dataset.idx)] : stones.find(x => stoneKey(x) === button.dataset.favoriteId);
        if(!stone) return;
        toggleFavorite(stone);
        syncFavoriteUI();
      };
    });
  }

  function wireRequestButtons(){
    document.querySelectorAll('.requestDetailBtn').forEach(button=>{
      button.onclick = event => {
        event.stopPropagation();
        const card = button.closest('.card');
        if(!card) return;
        openDetail(Number(card.dataset.idx));
      };
    });
  }

  function syncFavoriteUI(){
    document.querySelectorAll('.favoriteToggle').forEach(button=>{
      button.classList.toggle('on', isFavorite(button.dataset.favoriteId));
    });
    renderNav();
    if(currentPage === 'favorites') renderFavoritesPage();
  }

  window.openDetail = function openDetail(i){
    let s=stones[i];
    const requestBlock = requestChannelsHtml(s);
    const mainLabel = isRequestPrice(s) ? 'Запросить условия' : 'Уточнить условия';
    const favLabel = isFavorite(s) ? 'В избранном' : 'В избранное';
    const favClass = isFavorite(s) ? 'detailBtn detailFavoriteBtn favoriteOn' : 'detailBtn detailFavoriteBtn';
    detailContent.innerHTML=`<div class=detailTop><div><div class=detailName>${s.shape||''} ${Number(s.carat||0).toFixed(2).replace('.00','')} ct</div><div class=tags style='justify-content:flex-start;margin-top:.55rem'>${mkTags(s.score,s.tags)}</div></div>${priceHtml(s,true)}</div>${requestBlock}<div class=detailGrid><div class=detailCell><div class=detailLabel>Цвет</div><div class=detailValue>${s.color||''}</div></div><div class=detailCell><div class=detailLabel>Чистота</div><div class=detailValue>${s.clarity||''}</div></div><div class=detailCell><div class=detailLabel>KURGIN Score</div><div class='detailValue scoreBold'>${s.score||''}</div></div><div class=detailCell><div class=detailLabel>Диаметр</div><div class=detailValue>${s.diameter||''} мм</div></div><div class=detailCell><div class=detailLabel>Флюоресценция</div><div class=detailValue>${s.fluor||s.fluorescence||''}</div></div><div class=detailCell><div class=detailLabel>Отделка</div><div class=detailValue>${s.finish||''}</div></div></div><div class=detailNote>Документ / report: ${s.report||'—'}<br>${s.meta||''}<br>Параметры карточки будут уточняться: пропорции, световое поведение и условия запроса.</div><div class=detailActions><button class='detailBtn dark disabled' type='button' disabled>${mainLabel}</button><button class='${favClass}' data-favorite-id='${stoneKey(s)}'>${favLabel}</button></div>`;
    const favoriteButton = detailContent.querySelector('.detailFavoriteBtn');
    if(favoriteButton){
      favoriteButton.onclick = () => {
        toggleFavorite(s);
        favoriteButton.textContent = isFavorite(s) ? 'В избранном' : 'В избранное';
        favoriteButton.classList.toggle('favoriteOn', isFavorite(s));
        syncFavoriteUI();
      };
    }
    open('detail');
  };

  function currentStoneById(stoneId){
    return stones.find(stone => stoneKey(stone) === String(stoneId || ''));
  }

  function formattedCarat(value){
    const number = Number(value || 0);
    if(!number) return '—';
    return number.toFixed(2).replace('.00','') + ' ct';
  }

  function favoriteCell(label, value){
    const safeValue = value !== undefined && value !== null && String(value).trim() ? value : '—';
    return `<div class='favoriteCell'><span>${escapeHtml(label)}</span><strong>${escapeHtml(safeValue)}</strong></div>`;
  }

  function favoriteCardHtml(item){
    const current = currentStoneById(item.stone_id);
    const snapshot = item.snapshot || {};
    const stone = current || {id:item.stone_id, stone_id:item.stone_id, shape:snapshot.shape, carat:snapshot.carat, color:snapshot.color, clarity:snapshot.clarity, score:snapshot.score, priceText:snapshot.priceText, public_action:snapshot.public_action, diameter:snapshot.diameter, fluor:snapshot.fluor, finish:snapshot.finish, report:snapshot.report};
    const unavailable = !current;
    const shape = stone.shape || snapshot.shape || '';
    const carat = stone.carat || snapshot.carat || '';
    const color = stone.color || snapshot.color || '';
    const clarity = stone.clarity || snapshot.clarity || '';
    const score = stone.score || snapshot.score || '';
    const price = unavailable ? (snapshot.priceText && snapshot.priceText !== '0' ? snapshot.priceText : 'по запросу') : displayPriceText(stone);
    const name = `${shape || 'Камень'} ${formattedCarat(carat)}`.trim();
    const detailAction = current ? `<button class='favoriteBtn dark' data-open-favorite='${escapeHtml(stoneKey(stone))}'>Открыть карточку</button>` : `<button class='favoriteBtn dark' data-nav-page='catalog'>В каталог</button>`;
    return `<div class='favoriteCard'><div class='favoriteTop'><div><div class='favoriteName'>${escapeHtml(name)}</div><div class='favoriteMeta'>ID: ${escapeHtml(item.stone_id || '')}</div></div><div class='favoritePrice'>${escapeHtml(price)}</div></div><div class='favoriteGrid'>${favoriteCell('Форма', shape)}${favoriteCell('Карат', formattedCarat(carat))}${favoriteCell('Цвет', color)}${favoriteCell('Чистота', clarity)}${favoriteCell('KURGIN Score', score)}${favoriteCell('Цена', price)}</div>${unavailable?`<div class='favoriteUnavailable'>Камень больше не доступен в текущем каталоге.</div>`:''}<div class='favoriteSafety'>Избранное хранится только в этом браузере. Оно не резервирует камень, не фиксирует цену и не создаёт заказ.</div><div class='favoriteActions'>${detailAction}<button class='favoriteBtn danger' data-remove-favorite='${escapeHtml(item.stone_id)}'>Удалить</button></div></div>`;
  }

  window.renderFavoritesPage = function renderFavoritesPage(){
    const favorites = getFavorites();
    if(!favorites.length){
      content.innerHTML = pageHeader(pageTitles.favorites, pageSubtitles.favorites) + `<div class='pageBody'><div class='placeholder empty-state'><div class='empty-title'>Вы пока не добавили камни в избранное.</div><div class='muted'>Сохраняйте интересные камни из каталога, чтобы вернуться к ним позже. Избранное хранится только в этом браузере.</div><button class='btn light' type='button' data-nav-page='catalog'>Перейти в каталог</button></div><div class='favoritesInfo'>Избранное не резервирует камни, не фиксирует цену и не создаёт заказ.</div></div>`;
    } else {
      content.innerHTML = pageHeader(pageTitles.favorites, pageSubtitles.favorites) + `<div class='favoritesInfo'>Избранное хранится только в этом браузере. Оно не резервирует камни, не фиксирует цену, не создаёт заказ и не подтверждает наличие.</div><div class='favoriteList'>${favorites.map(favoriteCardHtml).join('')}</div>`;
    }
    content.scrollTop = 0;
    wireFavoritePageActions();
  };

  function wireFavoritePageActions(){
    document.querySelectorAll('[data-remove-favorite]').forEach(button=>{
      button.onclick = event => {
        event.stopPropagation();
        removeFavorite(button.dataset.removeFavorite);
        renderFavoritesPage();
        renderNav();
        if(document.getElementById('cards')) syncFavoriteUI();
      };
    });
    document.querySelectorAll('[data-open-favorite]').forEach(button=>{
      button.onclick = event => {
        event.stopPropagation();
        const stone = currentStoneById(button.dataset.openFavorite);
        if(!stone) return;
        openDetail(stones.indexOf(stone));
      };
    });
  }

  setPage = function(page){
    if(!pageTemplates[page] && page !== 'catalog') page='catalog';
    currentPage = page;
    renderNav();
    controls.classList.toggle('hidden', page !== 'catalog');
    content.classList.toggle('catalog', page === 'catalog');

    if(page === 'catalog'){
      renderCatalogPage();
    } else if(page === 'favorites'){
      renderFavoritesPage();
    } else {
      content.innerHTML = pageHeader(pageTitles[page] || 'KURGIN', pageSubtitles[page] || '') + pageTemplates[page];
      if(page === 'profile' && typeof initProfilePage === 'function') initProfilePage();
      content.scrollTop = 0;
    }

    try {
      const url = new URL(window.parent.location.href);
      url.searchParams.set('page', page);
      window.parent.history.replaceState(null, '', url.toString());
    } catch(e) {}
  };

  if(currentPage === 'catalog'){
    activeSection = activeSection || 'all';
  }
  setPage(currentPage);
})();
""".replace("__REQUEST_CONTACTS_JSON__", json.dumps(REQUEST_CONTACTS, ensure_ascii=False))


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
