from __future__ import annotations


INDEX_CSS = r'''
.index-shell{padding-bottom:7.6rem;--index-clarity-width:82px;--index-band-width:84px;--index-table-width:754px}
.index-info-card,.index-score-card,.index-range-summary,.index-view-panel{border:1px solid #aaa;border-radius:18px;background:#f7f7f7;padding:1rem;margin:0 0 1rem}
.index-title,.index-subtitle,.index-view-title{font-weight:700;font-size:1rem;margin-bottom:.55rem}
.index-info-card div,.index-score-card div,.index-range-summary div,.index-view-panel div{font-size:.82rem;line-height:1.45}
.index-hint,.index-range-disclaimer,.index-view-text,.index-view-hint{font-size:.64rem!important;color:#666}
.index-score-selected,.index-range-summary-selected{font-weight:700;margin:.15rem 0 .35rem}
.index-score-coefficient,.index-range-summary-coefficient{font-size:.72rem!important;color:#555;margin-bottom:.65rem}
.index-action-button{display:block;width:100%;margin:.65rem 0 0;border:1px solid #aaa;border-radius:13px;background:#fff;min-height:40px;font:inherit;font-size:.78rem;color:#111;text-align:center;cursor:pointer}
.index-action-button:active{transform:translateY(1px)}
.index-secondary-action{background:#f3f3f3;color:#555;border-color:#d5d5d5}
.index-action-notice{margin-top:.6rem;border:1px solid #ddd;border-radius:12px;background:#fff;padding:.55rem .65rem;color:#555;font-size:.7rem!important;line-height:1.35!important}
.index-action-notice:empty,.index-action-notice[hidden]{display:none!important}
.score-range-selector{display:flex;gap:.4rem;margin:.65rem 0;overflow-x:auto;-webkit-overflow-scrolling:touch;padding-bottom:.2rem}
.score-range-button{flex:0 0 108px;border:1px solid #c8c8c8;border-radius:13px;background:#fff;padding:.52rem .45rem;text-align:left;font:inherit;color:#111;min-height:58px}
.score-range-button[aria-selected="true"]{border-color:#111;background:#efefef}
.score-range-button strong{display:block;font-size:.75rem;line-height:1.1}
.score-range-button span{display:block;font-size:.64rem;color:#555;margin-top:.12rem}
.score-range-button small{display:block;font-size:.58rem;color:#777;margin-top:.12rem}
.index-color-section{margin:0 0 .9rem}
.index-color-section summary{list-style:none;border:1px solid #aaa;border-radius:13px;background:#f7f7f7;padding:.75rem 1rem;font-weight:700;font-size:1rem;cursor:pointer}
.index-color-section summary::-webkit-details-marker{display:none}
.index-color-section summary:before{content:'▶ ';font-weight:700}
.index-color-section[open] summary{border-color:#555;background:#dedede}
.index-color-section[open] summary:before{content:'▼ '}
.index-matrix-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:.55rem 0 1rem;border:1px solid #bcbcbc;border-radius:10px;background:#fff}
.index-matrix{width:var(--index-table-width,754px);min-width:var(--index-table-width,754px);max-width:var(--index-table-width,754px);border-collapse:separate;border-spacing:0;table-layout:fixed;font-size:.72rem}
.index-matrix th,.index-matrix td{border-right:1px solid #bcbcbc;border-bottom:1px solid #bcbcbc;text-align:center;padding:.5rem .25rem;vertical-align:middle;background:#fff;box-sizing:border-box}
.index-matrix th[data-index-band],.index-matrix td[data-index-band]{width:var(--index-band-width,84px);min-width:var(--index-band-width,84px);max-width:var(--index-band-width,84px)}
.index-matrix thead th{background:#dedede;font-weight:400;position:sticky;top:0;z-index:2}
.index-matrix thead th:first-child,.index-matrix tbody th{position:sticky;left:0;z-index:4;width:var(--index-clarity-width,82px);min-width:var(--index-clarity-width,82px);max-width:var(--index-clarity-width,82px);background:#f8f8f8;text-align:left;padding-left:.7rem;font-weight:400;box-shadow:2px 0 0 #bcbcbc;box-sizing:border-box}
.index-matrix thead th:first-child{background:#dedede;z-index:5}
.index-matrix tbody th{background:#fafafa}
.index-cell-main{font-size:.72rem;line-height:1.15}
.index-cell-sub{font-size:.65rem;line-height:1.15;margin-top:.18rem}
.index-view-panel{position:fixed;left:50%;bottom:calc(122px + env(safe-area-inset-bottom));transform:translateX(-50%);z-index:38;width:100%;max-width:430px;box-sizing:border-box;max-height:min(66vh,540px);overflow:auto;-webkit-overflow-scrolling:touch;overscroll-behavior:contain;box-shadow:0 -12px 38px rgba(0,0,0,.18);border-radius:18px 18px 0 0;margin:0}
.index-view-panel[hidden]{display:none!important}
.index-view-close-handle{display:flex;align-items:center;justify-content:center;width:100%;height:34px;margin:-.45rem 0 .35rem;border:0;background:transparent;padding:0;cursor:grab;touch-action:none;color:inherit}
.index-view-close-handle:active{cursor:grabbing}
.index-view-close-handle span{display:block;width:42px;height:4px;border-radius:999px;background:#c8c8c8}
.index-view-actions{display:grid;grid-template-columns:1fr 1fr;gap:.55rem;margin:.75rem 0}
.index-view-action{border:1px solid #aaa;border-radius:13px;background:#fff;min-height:40px;font:inherit;font-size:.72rem;color:#111}
.index-view-group{border-top:1px solid #ddd;margin-top:.8rem;padding-top:.75rem}
.index-view-group-title{font-weight:700;margin-bottom:.45rem}
.index-view-choice-grid{display:flex;flex-wrap:wrap;gap:.42rem}
.index-view-choice{border:1px solid #aaa;border-radius:999px;background:#fff;min-height:34px;padding:.35rem .65rem;font:inherit;font-size:.68rem;color:#111}
.index-view-choice[aria-pressed="true"]{border-color:#111;background:#efefef;font-weight:700}
.index-view-choice[aria-pressed="false"]{opacity:.42;background:#fafafa}
.index-filter-button{position:fixed;left:50%;transform:translateX(-50%);bottom:calc(64px + env(safe-area-inset-bottom));z-index:39;width:100%;max-width:430px;border:1px solid #777;border-radius:0;background:#f3f3f3;min-height:58px;font:inherit;font-size:.92rem;color:#111}
.index-filter-button[aria-expanded="true"]{background:#111;color:#fff;border-color:#111}
'''
