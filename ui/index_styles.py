from __future__ import annotations


INDEX_CSS = r'''
.index-shell{padding-bottom:4.8rem}
.index-info-card,.index-score-card,.index-range-summary,.index-view-panel{border:1px solid #aaa;border-radius:18px;background:#f7f7f7;padding:1rem;margin:0 0 1rem}
.index-title,.index-subtitle,.index-view-title{font-weight:700;font-size:1rem;margin-bottom:.55rem}
.index-info-card div,.index-score-card div,.index-range-summary div,.index-view-panel div{font-size:.82rem;line-height:1.45}
.index-hint,.index-range-disclaimer,.index-view-text,.index-view-hint{font-size:.64rem!important;color:#666}
.index-score-selected,.index-range-summary-selected{font-weight:700;margin:.15rem 0 .35rem}
.index-score-coefficient,.index-range-summary-coefficient{font-size:.72rem!important;color:#555;margin-bottom:.65rem}
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
.index-matrix{min-width:760px;width:max-content;border-collapse:separate;border-spacing:0;table-layout:fixed;font-size:.72rem}
.index-matrix th,.index-matrix td{border-right:1px solid #bcbcbc;border-bottom:1px solid #bcbcbc;text-align:center;padding:.5rem .25rem;vertical-align:middle;min-width:84px;background:#fff}
.index-matrix thead th{background:#dedede;font-weight:400;position:sticky;top:0;z-index:2}
.index-matrix thead th:first-child,.index-matrix tbody th{position:sticky;left:0;z-index:4;min-width:82px;width:82px;background:#f8f8f8;text-align:left;padding-left:.7rem;font-weight:400;box-shadow:2px 0 0 #bcbcbc}
.index-matrix thead th:first-child{background:#dedede;z-index:5}
.index-matrix tbody th{background:#fafafa}
.index-cell-main{font-size:.72rem;line-height:1.15}
.index-cell-sub{font-size:.65rem;line-height:1.15;margin-top:.18rem}
.index-view-actions{display:grid;grid-template-columns:1fr 1fr;gap:.55rem;margin:.75rem 0}
.index-view-action{border:1px solid #aaa;border-radius:13px;background:#fff;min-height:40px;font:inherit;font-size:.72rem;color:#111}
.index-filter-button{position:fixed;left:50%;transform:translateX(-50%);bottom:calc(64px + env(safe-area-inset-bottom));z-index:34;width:100%;max-width:430px;border:1px solid #777;border-radius:20px 20px 0 0;background:#f3f3f3;min-height:58px;font:inherit;font-size:.92rem;color:#111}
'''
