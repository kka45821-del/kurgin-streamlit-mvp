from __future__ import annotations


INDEX_INIT = r"""
(function(){
  if(window.__kurginIndexInitMounted) return;
  window.__kurginIndexInitMounted = true;

  function indexRootFromTarget(target){
    return target && target.closest ? target.closest('.index-shell') : null;
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

  function closeViewPanel(root){
    if(!root) return;
    const panel = root.querySelector('.index-view-panel');
    if(panel) panel.hidden = true;
    root.querySelectorAll('[data-index-action="view-toggle"]').forEach(button => {
      button.setAttribute('aria-expanded', 'false');
    });
  }

  function ensureViewPanelSwipeClose(root){
    if(!root) return;
    const panel = root.querySelector('.index-view-panel');
    if(!panel || panel.dataset.swipeCloseMounted === 'true') return;
    panel.dataset.swipeCloseMounted = 'true';

    let startY = 0;
    let startX = 0;
    let tracking = false;

    panel.addEventListener('touchstart', event => {
      if(!event.touches || !event.touches.length) return;
      startY = event.touches[0].clientY;
      startX = event.touches[0].clientX;
      tracking = true;
    }, {passive: true});

    panel.addEventListener('touchend', event => {
      if(!tracking || !event.changedTouches || !event.changedTouches.length) return;
      tracking = false;
      const touch = event.changedTouches[0];
      const deltaY = touch.clientY - startY;
      const deltaX = Math.abs(touch.clientX - startX);
      if(deltaY > 42 && deltaX < 130 && panel.scrollTop <= 18){
        closeViewPanel(root);
      }
    }, {passive: true});
  }

  function toggleViewPanel(root, button){
    if(!root || !button) return;
    const panel = root.querySelector('.index-view-panel');
    if(!panel) return;
    const shouldOpen = panel.hidden;
    panel.hidden = !shouldOpen;
    button.setAttribute('aria-expanded', String(shouldOpen));
    if(shouldOpen){
      ensureViewPanelSwipeClose(root);
    }
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
    }
  }

  function showAll(root){
    if(!root) return;
    root.querySelectorAll('.index-view-choice').forEach(button => button.setAttribute('aria-pressed', 'true'));
    root.querySelectorAll('.index-color-section,[data-index-clarity],[data-index-band]').forEach(el => { el.hidden = false; });
  }

  function resetView(root){
    if(!root) return;
    showAll(root);
    root.querySelectorAll('.index-color-section').forEach(section => {
      section.open = section.getAttribute('data-index-color') === 'E';
    });
  }

  document.addEventListener('click', event => {
    const button = event.target.closest('[data-index-action]');
    if(!button) return;
    const root = indexRootFromTarget(button);
    if(!root) return;
    const action = button.getAttribute('data-index-action');
    if(action === 'score-range') applyScoreRange(root, button);
    if(action === 'view-toggle') toggleViewPanel(root, button);
    if(action === 'expand-all-colors') setAllColorSections(root, true);
    if(action === 'collapse-all-colors') setAllColorSections(root, false);
    if(action === 'view-option') toggleViewOption(root, button);
    if(action === 'show-all') showAll(root);
    if(action === 'reset-view') resetView(root);
  });
})();
"""
