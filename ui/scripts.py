from ui.index_scripts import INDEX_INIT


def catalog_script(stones_json: str, initial_page: str, pages_json: str, titles_json: str, subtitles_json: str, logo_url: str) -> str:
    template = r"""
const stones = __STONES_JSON__;
const pageTemplates = __PAGES_JSON__;
const pageTitles = __TITLES_JSON__;
const pageSubtitles = __SUBTITLES_JSON__;
const logoUrl = "__LOGO_URL__";
let currentPage = "__INITIAL_PAGE__";

function icon(n){
  const s='stroke=currentColor fill=none';
  const m={
    menu:`<svg viewBox='0 0 20 20' ${s}><path d='M10 3C6.1 3 3 6.1 3 10s3.1 7 7 7 7-3.1 7-7-3.1-7-7-7Z'/><path d='M8.2 10 10 7l1.8 3-1.8 3.5Z'/></svg>`,
    tools:`<svg viewBox='0 0 20 20' ${s}><path d='M7 3Q5 10 10 16'/><path d='M13 3q2 7-3 13'/><path d='M7 5.5h6'/></svg>`,
    catalog:`<svg viewBox='0 0 20 20' ${s}><path d='M5 4h10l3.5 4L10 18 1.5 8Z'/><path d='M5 4l5 14 5-14M1.5 8h17'/></svg>`,
    favorites:`<svg viewBox='0 0 20 20' ${s}><path d='M10 16S3 11 3 6.5C3 4.5 4.8 3 6.8 3 8.3 3 10 4.8 10 4.8S11.7 3 13.2 3C15.2 3 17 4.5 17 6.5 17 11 10 16 10 16Z'/></svg>`,
    cart:`<svg viewBox='0 0 20 20' ${s}><path d='M5.5 8.2h9l1 8H4.5l1-8Z'/><path d='M7.8 8.2V6.1a2.2 2.2 0 0 1 4.4 0v2.1'/></svg>`,
    profile:`<svg viewBox='0 0 20 20' ${s}><path d='M10 3a4 4 0 1 0 0 8 4 4 0 0 0 0-8Z'/><path d='M3 18c0-3.5 3-5.5 7-5.5s7 2 7 5.5'/></svg>`,
    info:`<svg viewBox='0 0 24 24' ${s}><circle cx='12' cy='12' r='9'/><path d='M12 10v7M12 7h.01'/></svg>`,
    heart:`<svg viewBox='0 0 24 24' ${s}><path d='M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.6l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21l7.8-7.6 1-1a5.5 5.5 0 0 0 0-7.8Z'/></svg>`,
    shopping:`<svg viewBox='0 0 24 24' ${s}><circle cx='9' cy='21' r='1'/><circle cx='20' cy='21' r='1'/><path d='M1 1h4l2.7 13.4a2 2 0 0 0 2 1.6h8.7a2 2 0 0 0 2-1.6L22 6H6'/></svg>`,
    share:`<svg viewBox='0 0 24 24' ${s}><circle cx='18' cy='5' r='3'/><circle cx='6' cy='12' r='3'/><circle cx='18' cy='19' r='3'/><path d='M8.6 10.6 15.4 6.4M8.6 13.4l6.8 4.2'/></svg>`,
    message:`<svg viewBox='0 0 24 24' ${s}><path d='M21 15a4 4 0 0 1-4 4H8l-5 3V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4Z'/></svg>`,
    reserve:`<svg viewBox='0 0 24 24' ${s}><rect x='3' y='4' width='18' height='17' rx='2'/><path d='M8 2v4M16 2v4M3 10h18M8.5 15l2.2 2.2 4.8-5'/></svg>`
  };
  return m[n]||'';
}

function pageHeader(title, subtitle){
  return `<div class='header'><img class='logo' src='${logoUrl}'><div><div class='brand-title'>${title}</div><div class='brand-sub'>${subtitle}</div></div></div>`;
}

function renderNav(){
  const items=[['kurgin','menu'],['tools','tools'],['catalog','catalog'],['favorites','favorites'],['cart','cart'],['profile','profile']];
  navGrid.innerHTML=items.map(i=>`<a class='${i[0]===currentPage?'active':''}' href='?page=${i[0]}' data-nav-page='${i[0]}'><span class='ico'>${icon(i[1])}</span></a>`).join('');
}

function initProfilePage(){
  document.querySelectorAll('.roleOption[data-role]').forEach(button=>{
    button.onclick = () => {
      const role = button.dataset.role;
      document.querySelectorAll('.roleOption[data-role]').forEach(x=>x.classList.toggle('selected', x.dataset.role === role));
      document.querySelectorAll('.rolePanel[data-role-panel]').forEach(x=>x.classList.toggle('active', x.dataset.rolePanel === role));
    };
  });
}

function setPage(page){
  if(!pageTemplates[page] && page !== 'catalog') page='catalog';
  currentPage = page;
  renderNav();
  controls.classList.toggle('hidden', page !== 'catalog');
  content.classList.toggle('catalog', page === 'catalog');

  if(page === 'catalog'){
    renderCatalogPage();
  } else {
    content.innerHTML = pageHeader(pageTitles[page] || 'KURGIN', pageSubtitles[page] || '') + pageTemplates[page];
    if(page === 'profile') initProfilePage();
    content.scrollTop = 0;
  }

  try {
    const url = new URL(window.parent.location.href);
    url.searchParams.set('page', page);
    window.parent.history.replaceState(null, '', url.toString());
  } catch(e) {}
}

document.addEventListener('click', (event) => {
  const nav = event.target.closest('[data-nav-page]');
  if(nav){
    event.preventDefault();
    event.stopPropagation();
    setPage(nav.dataset.navPage);
  }
});

const sections=[['small','Мелкие','0–0.29 ct'],['medium','Средние','0.30–0.99 ct'],['main','Основной каталог','1.00–2.99 ct'],['large','Крупные','3.00+ ct'],['colored','Цветные',''],['side','Боковые',''],['pairs','Парные',''],['exclusive','Эксклюзив','']];
let activeSection='main';
let sort='price_asc';
const sortLabels={score_desc:'по Karo Score ↓',score_asc:'по Karo Score ↑',price_asc:'по цене ↑',price_desc:'по цене ↓',carat_asc:'по весу ↑',carat_desc:'по весу ↓',diameter_asc:'по диаметру ↑',diameter_desc:'по диаметру ↓',new:'по новизне'};
const groups=['shape','weight','color','clarity','score','fluorescence','finish'];

function renderCatalogPage(){
  content.innerHTML = pageHeader(pageTitles.catalog, pageSubtitles.catalog) + `
    <div class='top'><div class='catalogBox' id='catalogBox'><button class='select' id='catalogBtn'><div><div class='select-title' id='sectionTitle'>Основной каталог</div><div class='select-sub' id='sectionSub'>1.00–2.99 ct</div></div><div class='chev'><svg viewBox='0 0 20 20'><path d='M5 8l5 5 5-5'/></svg></div></button><div class='menu' id='catalogMenu'></div></div><div class='pick'>Индив.<br>подбор</div></div>
    <div class='cols'><div>ФОРМА</div><div>КАРАТ</div><div>ЦВЕТ</div><div>ЧИСТОТА</div><div>KARO SCORE</div><div>ЦЕНА</div></div>
    <div id='cards'></div><div class='empty' id='empty'>По выбранному разделу и фильтрам камни не найдены</div>`;
  setupCatalog();
  content.scrollTop = 0;
}

function setupCatalog(){
  drawMenu();
  catalogBtn.onclick=e=>{e.stopPropagation();catalogBox.classList.toggle('open')};
  document.addEventListener('click',e=>{if(document.getElementById('catalogBox') && !catalogBox.contains(e.target)) catalogBox.classList.remove('open')});
  renderCards();
}

function drawMenu(){
  catalogMenu.innerHTML=sections.map((s,i)=>`${i===4?'<div class=sep></div>':''}<button class='${s[0]===activeSection?'active':''}' data-id='${s[0]}'><div class=m-title>${s[1]}</div>${s[2]?`<div class=m-sub>${s[2]}</div>`:''}</button>`).join('');
  catalogMenu.querySelectorAll('button').forEach(b=>b.onclick=()=>{
    activeSection=b.dataset.id;
    let s=sections.find(x=>x[0]===activeSection);
    sectionTitle.textContent=s[1];
    sectionSub.textContent=s[2];
    catalogBox.classList.remove('open');
    drawMenu();
    renderCards();
  });
}

function mkTags(score,base){return (base||'')+(Number(score)>=98.5?'<span class="tag elite">ELITE</span>':'')}
function shapeKey(s){return (s.shape==='Круг'||s.shape==='Round')?'Round':(s.shape||'')}

sortList.innerHTML=`<div class=group><div class=g-name>Karo Score</div><div class=sorts><button class=sort data-sort=score_desc>по Karo Score ↓</button><button class=sort data-sort=score_asc>по Karo Score ↑</button></div></div><div class=group><div class=g-name>Цена</div><div class=sorts><button class='sort on' data-sort=price_asc>по цене ↑</button><button class=sort data-sort=price_desc>по цене ↓</button></div></div><div class=group><div class=g-name>Вес</div><div class=sorts><button class=sort data-sort=carat_asc>по весу ↑</button><button class=sort data-sort=carat_desc>по весу ↓</button></div></div><div class=group><div class=g-name>Диаметр</div><div class=sorts><button class=sort data-sort=diameter_asc>по диаметру ↑</button><button class=sort data-sort=diameter_desc>по диаметру ↓</button></div></div><div class=group><div class=g-name>Прочее</div><div class=sorts><button class=sort data-sort=new>по новизне</button></div></div>`;

filterContent.innerHTML=[['shape','1. Форма / огранка',['Round','Oval','Pear','Cushion']],['weight','2. Вес',['1–1.49','1.5–1.99','2–2.49','2.5–2.99']],['color','3. Цвет',['D','E','F','G','H']],['clarity','4. Чистота',['IF','VVS1','VVS2','VS1','VS2']],['score','5. Karo Score',['0–49','50–79','80–89','90–94.9','95–98','99+']],['fluorescence','6. Флюоресценция',['None','Faint','Medium','Strong']],['finish','7. Качество отделки',['Ex/Ex/Ex+','2Ex/1VG+']]].map(g=>`<div class=group><div class=g-name>${g[1]}</div><div class=chips>${g[2].map((v,i)=>`<button class='chip ${g[0]=='shape'&&i==0?'on':''}' data-group='${g[0]}' data-value='${v}'>${v}</button>`).join('')}</div></div>`).join('');

const actions=`<button class=act data-stop=1>${icon('message')}</button><button class=act data-stop=1>${icon('reserve')}</button><button class='act infoBtn'>${icon('info')}</button><button class=act data-stop=1>${icon('heart')}</button><button class=act data-stop=1>${icon('shopping')}</button><button class=act data-stop=1>${icon('share')}</button>`;

function source(){
  let a=activeSection==='main'?stones:stones.filter(x=>x.section===activeSection);
  if(sort==='new') return a;
  let [k,d]=sort.split('_');
  return [...a].sort((x,y)=>{let xv=Number(x[k]||0),yv=Number(y[k]||0);return d==='asc'?xv-yv:yv-xv});
}

function renderCards(){
  if(!document.getElementById('cards')) return;
  sortLabel.textContent=sortLabels[sort];
  document.querySelectorAll('.sort').forEach(b=>b.classList.toggle('on',b.dataset.sort===sort));
  cards.innerHTML=source().map(s=>`<div class=card data-idx='${stones.indexOf(s)}' data-shape='${shapeKey(s)}' data-weight='${s.weight||''}' data-color='${s.color||''}' data-clarity='${s.clarity||''}' data-score='${s.scoreBand||''}' data-fluorescence='${s.fluor||s.fluorescence||''}' data-finish='${s.finish||''}'><div class=main><div>${s.shape||''}</div><div>${Number(s.carat||0).toFixed(2).replace('.00','')}</div><div>${s.color||''}</div><div>${s.clarity||''}</div><div class=scoreValue>${s.score||''}</div><div class=price>${s.priceText||''} ₽</div></div><div class=line></div><div class=meta><div>${s.meta||''}</div><div class=tags>${mkTags(s.score,s.tags)}</div></div><div class=actions>${actions}</div></div>`).join('');
  wireCards();
  filter();
}

function activeFilters(){
  let f={};
  groups.forEach(g=>f[g]=[]);
  document.querySelectorAll('.chip').forEach(c=>{if(c.classList.contains('on'))f[c.dataset.group].push(c.dataset.value)});
  return f;
}

function filter(){
  if(!document.getElementById('cards')) return;
  let f=activeFilters(),n=0;
  document.querySelectorAll('.card').forEach(card=>{
    let v=true;
    groups.forEach(g=>{if(f[g].length&&!f[g].includes(card.dataset[g]))v=false});
    card.classList.toggle('hide',!v);
    if(v)n++;
  });
  empty.classList.toggle('show',n===0);
}

function open(t){
  app.classList.add(t==='sort'?'sortOpen':t==='detail'?'detailOpen':'filterOpen');
  (t==='sort'?sortSheet:t==='detail'?detailSheet:sheet).style.transform='translate(-50%,0)';
}

function close(){
  [sheet,sortSheet,detailSheet].forEach(s=>s.style.transform='translate(-50%,110%)');
  setTimeout(()=>app.classList.remove('filterOpen','sortOpen','detailOpen'),160);
}

function openDetail(i){
  let s=stones[i];
  detailContent.innerHTML=`<div class=detailTop><div><div class=detailName>${s.shape||''} ${Number(s.carat||0).toFixed(2).replace('.00','')} ct</div><div class=tags style='justify-content:flex-start;margin-top:.55rem'>${mkTags(s.score,s.tags)}</div></div><div class=detailPrice>${s.priceText||''} ₽</div></div><div class=detailGrid><div class=detailCell><div class=detailLabel>Цвет</div><div class=detailValue>${s.color||''}</div></div><div class=detailCell><div class=detailLabel>Чистота</div><div class=detailValue>${s.clarity||''}</div></div><div class=detailCell><div class=detailLabel>Karo Score</div><div class='detailValue scoreBold'>${s.score||''}</div></div><div class=detailCell><div class=detailLabel>Диаметр</div><div class=detailValue>${s.diameter||''} мм</div></div><div class=detailCell><div class=detailLabel>Флюоресценция</div><div class=detailValue>${s.fluor||s.fluorescence||''}</div></div><div class=detailCell><div class=detailLabel>Отделка</div><div class=detailValue>${s.finish||''}</div></div></div><div class=detailNote>Сертификат: ${s.report||''}<br>${s.meta||''}<br>Подробная профессиональная карточка будет расширяться: параметры, пропорции, световое поведение и условия резерва.</div><div class=detailActions><button class='detailBtn dark'>В корзину</button><button class=detailBtn>В избранное</button></div>`;
  open('detail');
}

function wireCards(){
  document.querySelectorAll('.card').forEach(c=>{
    c.onclick=e=>{if(e.target.closest('[data-stop]'))return;openDetail(c.dataset.idx)};
    c.querySelector('.infoBtn').onclick=e=>{e.stopPropagation();openDetail(c.dataset.idx)};
  });
}

openFilters.onclick=()=>open('filter');
openSort.onclick=()=>open('sort');
overlay.onclick=close;
handle.onclick=close;
sortHandle.onclick=close;
detailHandle.onclick=close;
closeDetail.onclick=close;
document.querySelectorAll('.sort').forEach(b=>b.onclick=()=>{sort=b.dataset.sort;renderCards();close()});
document.addEventListener('click',e=>{if(e.target.classList.contains('chip')){e.target.classList.toggle('on');filter()}});
reset.onclick=()=>{document.querySelectorAll('.chip').forEach(c=>c.classList.remove('on'));filter()};

function addSwipe(el){
  let sy=0,sx=0,drag=false;
  el.addEventListener('touchstart',e=>{if(!e.touches.length)return;sy=e.touches[0].clientY;sx=e.touches[0].clientX;drag=true;el.style.transition='none'},{passive:true});
  el.addEventListener('touchmove',e=>{if(!drag||!e.touches.length)return;let dy=e.touches[0].clientY-sy;if(dy>0&&el.scrollTop<=0){e.preventDefault();el.style.transform=`translate(-50%,${Math.min(dy,260)}px)`}},{passive:false});
  el.addEventListener('touchend',e=>{if(!drag)return;drag=false;let t=e.changedTouches[0],dy=t.clientY-sy,dx=Math.abs(t.clientX-sx);if(dy>70&&dx<110&&el.scrollTop<=5)close();else{el.style.transition='transform .18s ease';el.style.transform='translate(-50%,0)'}},{passive:true});
}

addSwipe(sheet);
addSwipe(sortSheet);
addSwipe(detailSheet);
setPage(currentPage);
"""
    return (
        template
        .replace("__STONES_JSON__", stones_json)
        .replace("__INITIAL_PAGE__", initial_page)
        .replace("__PAGES_JSON__", pages_json)
        .replace("__TITLES_JSON__", titles_json)
        .replace("__SUBTITLES_JSON__", subtitles_json)
        .replace("__LOGO_URL__", logo_url)
        + "\n"
        + INDEX_INIT
    )
