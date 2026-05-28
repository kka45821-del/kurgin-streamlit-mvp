from __future__ import annotations


INDEX_INIT = r"""
(function(){
  if(window.__kurginIndexInitMounted) return;
  window.__kurginIndexInitMounted = true;

  function indexRootFromTarget(target){
    return target && target.closest ? target.closest('.index-shell') : null;
  }

  function shareIndex(button){
    let url;
    try{url=new URL(window.parent.location.href);}catch(e){url=new URL(window.location.href);}
    url.searchParams.set('page','tools');
    url.searchParams.set('tool','kurgin_index');
    url.hash='kurgin-index';
    const shareData={title:'KURGIN Index',text:'KURGIN Index — ориентир для сопоставления лабораторных бриллиантов',url:url.toString()};
    if(navigator.share){navigator.share(shareData).catch(()=>{});return;}
    if(navigator.clipboard){
      navigator.clipboard.writeText(url.toString()).then(()=>{
        const original=button.textContent;
        button.textContent='Ссылка скопирована';
        setTimeout(()=>{button.textContent=original || '↗ Поделиться Index';},1400);
      }).catch(()=>{window.prompt('Скопируйте ссылку',url.toString());});
      return;
    }
    window.prompt('Скопируйте ссылку',url.toString());
  }

  function currentPdfTables(root){
    return Array.from(root.querySelectorAll('.index-color-section'))
      .filter(section=>!section.hidden)
      .map(section=>{
        const color=section.getAttribute('data-index-color') || '';
        const table=section.querySelector('.index-matrix');
        return table ? `<section class="pdf-section"><h2>Color ${color}</h2>${table.outerHTML}</section>` : '';
      }).join('');
  }

  function printPdf(root){
    const selected=(root.querySelector('.index-score-selected')||{}).textContent || 'Standard / Стандартный · 80–89.99';
    const coefficient=(root.querySelector('.index-score-coefficient')||{}).textContent || 'Коэффициент: ×1.00';
    const tables=currentPdfTables(root);
    if(!tables){alert('Нет данных Index для PDF.');return;}
    const html='<!doctype html><html><head><meta charset="utf-8"><title>KURGIN Index PDF</title><style>body{font-family:Arial,sans-serif;color:#111;margin:28px}.pdf-head{display:flex;align-items:center;gap:16px;border-bottom:1px solid #111;padding-bottom:16px;margin-bottom:18px}.pdf-logo{width:84px;height:auto}.pdf-title{font-size:22px;font-weight:700;letter-spacing:.04em}.pdf-meta{font-size:12px;color:#555;margin-top:4px}.pdf-note{font-size:11px;line-height:1.45;border:1px solid #ddd;padding:10px;margin:14px 0}.pdf-section{break-inside:avoid;margin:16px 0}.pdf-section h2{font-size:16px;margin:0 0 8px}.index-matrix{width:100%;border-collapse:collapse;font-size:10px}.index-matrix th,.index-matrix td{border:1px solid #999;padding:5px;text-align:center}.index-matrix th{background:#eee}.index-matrix tbody th{text-align:left;background:#f7f7f7}.index-cell-sub{font-size:9px;color:#555}[hidden]{display:none!important}@media print{body{margin:18mm}.pdf-section{page-break-inside:avoid}}</style></head><body><div class="pdf-head"><img class="pdf-logo" src="https://raw.githubusercontent.com/kka45821-del/kurgin-streamlit-mvp/main/Vectorr-header.svg?v=1" alt="KURGIN"><div><div class="pdf-title">KURGIN Index</div><div class="pdf-meta">Snapshot: public_index_v0_1 · Unit: USD / ct · Period: current</div><div class="pdf-meta">Score range: '+selected+' · '+coefficient+'</div></div></div><div class="pdf-note">KURGIN Index is an indicative benchmark for comparing laboratory-grown diamonds. It is not an offer, not a final price for a specific stone, not a financial index and not an investment recommendation.</div>'+tables+'</body></html>';
    const frame=document.createElement('iframe');
    frame.setAttribute('title','KURGIN Index PDF');
    frame.style.position='fixed';frame.style.right='0';frame.style.bottom='0';frame.style.width='0';frame.style.height='0';frame.style.border='0';frame.style.opacity='0';
    document.body.appendChild(frame);
    const cleanup=()=>{setTimeout(()=>{try{frame.remove();}catch(e){}},1200);};
    try{
      const doc=frame.contentWindow.document;
      doc.open();doc.write(html);doc.close();
      frame.contentWindow.onafterprint=cleanup;
      setTimeout(()=>{try{frame.contentWindow.focus();frame.contentWindow.print();}catch(e){alert('Не удалось открыть PDF preview. Попробуйте ещё раз.');cleanup();}},500);
    }catch(e){alert('Не удалось подготовить PDF preview. Попробуйте ещё раз.');cleanup();}
  }

  function applyScoreRange(root, button){
    const card=button.closest('.index-score-card');
    if(!card) return;
    card.querySelectorAll('[data-score-range]').forEach(b=>b.setAttribute('aria-selected','false'));
    button.setAttribute('aria-selected','true');
    const label=button.getAttribute('data-score-label');
    const ru=button.getAttribute('data-score-ru');
    const range=button.getAttribute('data-score-range-label');
    const mode=button.getAttribute('data-score-mode');
    const coeff=Number(button.getAttribute('data-score-coefficient')||0);
    const coeffLabel=button.getAttribute('data-score-coefficient-label');
    const selectedText=label+' / '+ru+' · '+range;
    root.querySelectorAll('.index-score-selected,.index-range-summary-selected').forEach(el=>el.textContent=selectedText);
    root.querySelectorAll('.index-score-coefficient,.index-range-summary-coefficient').forEach(el=>el.textContent='Коэффициент: '+coeffLabel);
    root.querySelectorAll('.index-cell').forEach(cell=>{
      const base=Number(cell.getAttribute('data-index-base')||0);
      const main=cell.querySelector('.index-cell-main');
      const sub=cell.querySelector('.index-cell-sub');
      if(!main || !sub) return;
      if(!base){main.textContent='request';main.classList.add('muted');sub.textContent='—';return;}
      if(mode==='numeric'){main.textContent=String(Math.round(base*coeff))+' $/ct';main.classList.remove('muted');sub.textContent=coeffLabel;}
      else{main.textContent='request';main.classList.add('muted');sub.textContent=mode==='request_caution'?'caution':'—';}
    });
  }

  function toggleViewPanel(root, button){
    const panel=root.querySelector('.index-view-panel');
    if(!panel)return;
    const shouldOpen=panel.hidden;
    panel.hidden=!shouldOpen;
    button.setAttribute('aria-expanded',String(shouldOpen));
    if(shouldOpen)panel.scrollIntoView({block:'nearest'});
  }

  function setAllColorSections(root, open){
    root.querySelectorAll('.index-color-section').forEach(section=>{section.open=open;});
  }

  function toggleViewOption(root, button){
    const type=button.getAttribute('data-index-view-type');
    const value=button.getAttribute('data-index-view-value');
    const active=button.getAttribute('aria-pressed')!=='true';
    button.setAttribute('aria-pressed',String(active));
    if(type==='color')root.querySelectorAll('.index-color-section[data-index-color="'+value+'"]').forEach(el=>{el.hidden=!active;});
    if(type==='clarity')root.querySelectorAll('tr[data-index-clarity="'+value+'"]').forEach(el=>{el.hidden=!active;});
    if(type==='band')root.querySelectorAll('[data-index-band="'+value+'"]').forEach(el=>{el.hidden=!active;});
  }

  function showAll(root){
    root.querySelectorAll('.index-view-choice').forEach(button=>button.setAttribute('aria-pressed','true'));
    root.querySelectorAll('.index-color-section,[data-index-clarity],[data-index-band]').forEach(el=>{el.hidden=false;});
  }

  function resetView(root){
    showAll(root);
    root.querySelectorAll('.index-color-section').forEach(section=>{section.open=section.getAttribute('data-index-color')==='E';});
  }

  document.addEventListener('click', event=>{
    const button=event.target.closest('[data-index-action]');
    if(!button)return;
    const root=indexRootFromTarget(button);
    if(!root)return;
    const action=button.getAttribute('data-index-action');
    if(action==='share')shareIndex(button);
    if(action==='pdf')printPdf(root);
    if(action==='score-range')applyScoreRange(root, button);
    if(action==='view-toggle')toggleViewPanel(root, button);
    if(action==='expand-all-colors')setAllColorSections(root, true);
    if(action==='collapse-all-colors')setAllColorSections(root, false);
    if(action==='view-option')toggleViewOption(root, button);
    if(action==='show-all')showAll(root);
    if(action==='reset-view')resetView(root);
  });
})();
"""
