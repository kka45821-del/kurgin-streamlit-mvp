from __future__ import annotations


INDEX_INIT = r"""
(function(){
  if(window.__kurginIndexInitMounted) return;
  window.__kurginIndexInitMounted = true;

  function indexRootFromTarget(target){
    return target && target.closest ? target.closest('.index-shell') : null;
  }

  function syncIndexTableWidth(root){
    if(!root) return;
    const clarityWidth = 82;
    const bandWidth = 84;
    let maxVisibleBandCount = 1;

    root.querySelectorAll('.index-matrix').forEach(table => {
      const visibleHeaders = Array.from(table.querySelectorAll('thead [data-index-band]')).filter(header => !header.hidden);
      const count = Math.max(visibleHeaders.length, 1);
      maxVisibleBandCount = Math.max(maxVisibleBandCount, count);
      const tableWidthPx = (clarityWidth + (count * bandWidth)) + 'px';
      table.style.width = tableWidthPx;
      table.style.minWidth = tableWidthPx;
      table.style.maxWidth = tableWidthPx;
    });

    root.style.setProperty('--index-visible-band-count', String(maxVisibleBandCount));
    root.style.setProperty('--index-table-width', (clarityWidth + (maxVisibleBandCount * bandWidth)) + 'px');
  }

  function applyScoreRange(root, button){
    if(!root || !button) return;
    const card = button.closest('.index-score-card');
    if(!card) return;
    card.querySelectorAll('[data-score-range]').forEach(b => b.setAttribute('aria-selected', 'false'));
    button.setAttribute('aria-selected', 'true');

    const label = button.getAttribute('data-score-label') || '';
    const ru = button.getAttribute('data-score-ru') || '';
    const range = button.getAttribute('data-score-range-label') || '';
    const mode = button.getAttribute('data-score-mode') || '';
    const coeff = Number(button.getAttribute('data-score-coefficient') || 0);
    const coeffLabel = button.getAttribute('data-score-coefficient-label') || '×1.00';
    const selectedText = label + ' / ' + ru + ' · ' + range;

    root.querySelectorAll('.index-score-selected,.index-range-summary-selected').forEach(el => {
      el.textContent = selectedText;
    });
    root.querySelectorAll('.index-score-coefficient,.index-range-summary-coefficient').forEach(el => {
      el.textContent = 'Коэффициент: ' + coeffLabel;
    });

    root.querySelectorAll('.index-cell').forEach(cell => {
      const base = Number(cell.getAttribute('data-index-base') || 0);
      const main = cell.querySelector('.index-cell-main');
      const sub = cell.querySelector('.index-cell-sub');
      if(!main || !sub) return;
      if(!base){
        main.textContent = 'request';
        main.classList.add('muted');
        sub.textContent = '—';
        return;
      }
      if(mode === 'numeric'){
        main.textContent = String(Math.round(base * coeff)) + ' $/ct';
        main.classList.remove('muted');
        sub.textContent = coeffLabel;
      } else {
        main.textContent = 'request';
        main.classList.add('muted');
        sub.textContent = mode === 'request_caution' ? 'caution' : '—';
      }
    });
  }

  function resetPanelMotion(panel){
    if(!panel) return;
    panel.style.transform = '';
    panel.style.transition = '';
  }

  function closeViewPanel(root){
    if(!root) return;
    const panel = root.querySelector('.index-view-panel');
    if(panel){
      panel.hidden = true;
      resetPanelMotion(panel);
    }
    root.querySelectorAll('[data-index-action="view-toggle"]').forEach(button => {
      button.setAttribute('aria-expanded', 'false');
    });
  }

  function ensureViewPanelHandleClose(root){
    if(!root) return;
    const panel = root.querySelector('.index-view-panel');
    const handle = root.querySelector('.index-view-close-handle');
    if(!panel || !handle || handle.dataset.pointerCloseMounted === 'true') return;
    handle.dataset.pointerCloseMounted = 'true';

    let startY = 0;
    let currentY = 0;
    let pointerId = null;
    let dragging = false;
    let moved = false;

    function finishDrag(event, cancelled){
      if(!dragging) return;
      const deltaY = Math.max(currentY - startY, 0);
      const panelHeight = panel.offsetHeight || 0;
      dragging = false;

      if(pointerId !== null && handle.releasePointerCapture){
        try{ handle.releasePointerCapture(pointerId); }catch(e){}
      }
      pointerId = null;

      if(!cancelled && (deltaY > 90 || deltaY > panelHeight * 0.22)){
        closeViewPanel(root);
        return;
      }

      panel.style.transition = 'transform .18s ease';
      panel.style.transform = 'translateX(-50%)';
    }

    handle.addEventListener('pointerdown', event => {
      if(event.button !== undefined && event.button !== 0) return;
      startY = event.clientY;
      currentY = event.clientY;
      pointerId = event.pointerId;
      dragging = true;
      moved = false;
      panel.style.transition = 'none';
      if(handle.setPointerCapture){
        try{ handle.setPointerCapture(pointerId); }catch(e){}
      }
    });

    handle.addEventListener('pointermove', event => {
      if(!dragging || event.pointerId !== pointerId) return;
      currentY = event.clientY;
      const deltaY = currentY - startY;
      if(Math.abs(deltaY) > 3) moved = true;
      if(deltaY > 0){
        event.preventDefault();
        panel.style.transform = 'translate(-50%, ' + deltaY + 'px)';
      } else {
        panel.style.transform = 'translateX(-50%)';
      }
    });

    handle.addEventListener('pointerup', event => {
      if(!dragging || event.pointerId !== pointerId) return;
      currentY = event.clientY;
      const wasTap = !moved || Math.abs(currentY - startY) <= 6;
      if(wasTap){
        dragging = false;
        if(pointerId !== null && handle.releasePointerCapture){
          try{ handle.releasePointerCapture(pointerId); }catch(e){}
        }
        pointerId = null;
        closeViewPanel(root);
        return;
      }
      finishDrag(event, false);
    });

    handle.addEventListener('pointercancel', event => {
      if(!dragging || event.pointerId !== pointerId) return;
      finishDrag(event, true);
    });
  }

  function toggleViewPanel(root, button){
    if(!root || !button) return;
    const panel = root.querySelector('.index-view-panel');
    if(!panel) return;
    const shouldOpen = panel.hidden;
    if(!shouldOpen){
      closeViewPanel(root);
      return;
    }
    panel.hidden = false;
    panel.style.transform = 'translateX(-50%)';
    panel.style.transition = 'transform .18s ease';
    panel.scrollTop = 0;
    button.setAttribute('aria-expanded', 'true');
    ensureViewPanelHandleClose(root);
    syncIndexTableWidth(root);
  }

  function setAllColorSections(root, open){
    if(!root) return;
    root.querySelectorAll('.index-color-section').forEach(section => { section.open = open; });
  }

  function toggleViewOption(root, button){
    if(!root || !button) return;
    const type = button.getAttribute('data-index-view-type');
    const value = button.getAttribute('data-index-view-value');
    const active = button.getAttribute('aria-pressed') !== 'true';
    button.setAttribute('aria-pressed', String(active));

    if(type === 'color'){
      root.querySelectorAll('.index-color-section[data-index-color="' + value + '"]').forEach(el => { el.hidden = !active; });
    }
    if(type === 'clarity'){
      root.querySelectorAll('tr[data-index-clarity="' + value + '"]').forEach(el => { el.hidden = !active; });
    }
    if(type === 'band'){
      root.querySelectorAll('[data-index-band="' + value + '"]').forEach(el => { el.hidden = !active; });
      syncIndexTableWidth(root);
    }
  }

  function showAll(root){
    if(!root) return;
    root.querySelectorAll('.index-view-choice').forEach(button => button.setAttribute('aria-pressed', 'true'));
    root.querySelectorAll('.index-color-section,[data-index-clarity],[data-index-band]').forEach(el => { el.hidden = false; });
    syncIndexTableWidth(root);
  }

  function resetView(root){
    if(!root) return;
    showAll(root);
    root.querySelectorAll('.index-color-section').forEach(section => {
      section.open = section.getAttribute('data-index-color') === 'E';
    });
    syncIndexTableWidth(root);
  }

  document.addEventListener('click', event => {
    const button = event.target.closest('[data-index-action]');
    if(!button) return;
    const root = indexRootFromTarget(button);
    if(!root) return;
    const action = button.getAttribute('data-index-action');
    if(action === 'score-range') applyScoreRange(root, button);
    if(action === 'view-toggle') toggleViewPanel(root, button);
    if(action === 'view-close') closeViewPanel(root);
    if(action === 'expand-all-colors') setAllColorSections(root, true);
    if(action === 'collapse-all-colors') setAllColorSections(root, false);
    if(action === 'view-option') toggleViewOption(root, button);
    if(action === 'show-all') showAll(root);
    if(action === 'reset-view') resetView(root);
  });
})();
"""
