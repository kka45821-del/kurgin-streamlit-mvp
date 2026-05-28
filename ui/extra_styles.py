# TODO: Index styles should move to ui/index_styles.py later.
SYSTEM_CSS = r'''
.system-state{border:1px solid #d7d7d7;border-radius:18px;background:#fff;padding:1rem;margin-bottom:1rem;box-shadow:0 10px 24px rgba(0,0,0,.04)}
.system-title,.empty-title{font-weight:700;margin-bottom:.35rem}
.system-text{color:#666;font-size:.86rem;line-height:1.45}
.authCard{margin-top:.75rem;border:0;background:transparent;box-shadow:none;padding:0}
.authRadio,.roleRadio{position:absolute;opacity:0;pointer-events:none}
.authSwitch{display:grid;grid-template-columns:1fr 1fr;gap:0;margin:0 0 -1px 0;padding:0;position:relative;z-index:2}
.authOption{border:1px solid #d7d7d7;border-bottom-color:#111;border-radius:12px 12px 0 0;background:#f7f7f7;padding:.62rem .9rem;text-align:center;font-weight:700;font-size:.88rem;cursor:pointer;min-width:0;color:#666}
.authOption+ .authOption{margin-left:-1px}
#auth-register:checked ~ .authSwitch .authRegisterLabel,#auth-login:checked ~ .authSwitch .authLoginLabel{border-color:#111;border-bottom-color:#fff;background:#fff;color:#111;position:relative;z-index:3}
.authPanel{display:none;border:1px solid #111;background:#fff;border-radius:0 0 16px 16px;padding:1rem;box-shadow:0 10px 24px rgba(0,0,0,.04)}
#auth-register:checked ~ .registerPanel,#auth-login:checked ~ .loginPanel{display:block}
.profile-section-title{padding:0 0 .5rem;margin-top:.25rem}
.profileRoleAfterButton{margin-top:1rem;border-top:1px solid #eee;padding-top:.9rem}
.roleIntro{margin-bottom:.35rem}
.roleSwitch{display:grid;grid-template-columns:1fr 1fr;gap:.5rem;margin:.55rem 0}
.roleOption{border:1px solid #d7d7d7;border-radius:14px;background:#fff;padding:.75rem;text-align:left;font:inherit;color:#111;display:block;cursor:pointer}
.compactRoleSwitch{gap:.4rem;margin:.45rem 0 .55rem}
.compactRoleOption{padding:.55rem .65rem;text-align:center;border-radius:12px}
.compactRoleOption .roleName{font-size:.82rem}
#role-customer:checked ~ .roleSwitch .roleCustomerLabel,#role-specialist:checked ~ .roleSwitch .roleSpecialistLabel{border-color:#111;background:#fafafa}
.roleName{font-weight:700;font-size:.9rem}
.roleHint{font-size:.72rem;color:#777;margin-top:.25rem;line-height:1.3}
.roleExplanation{border:1px solid #e0e0e0;border-radius:14px;background:#fff;padding:.85rem;margin:.55rem 0 .8rem}
.rolePanel{display:none}
#role-customer:checked ~ .roleExplanation .customerPanel,#role-specialist:checked ~ .roleExplanation .specialistPanel{display:block}
.rolePanelTitle{font-weight:700;margin-bottom:.25rem}
.rolePanelText{font-size:.84rem;color:#666;line-height:1.4}
.specialistRolesTitle{font-weight:700;font-size:.82rem;margin-top:.8rem;margin-bottom:.35rem}
.specialistRoleList{margin:.25rem 0 0;padding-left:1.1rem;color:#666;font-size:.82rem;line-height:1.45}
.specialistRoleList li{margin:.18rem 0}
.roleLater{border:1px dashed #ddd;border-radius:14px;padding:.75rem;color:#777;font-size:.82rem;line-height:1.35;margin-bottom:0}
.profileAuthGrid{margin-top:.75rem}
.catalog-state{margin:1rem}
.catalog-loading{display:block}
.catalog-ready .catalog-loading{display:none}
.catalog-empty-message,.catalog-error-message{display:none}
.catalog-empty .catalog-empty-message,.catalog-error .catalog-error-message{display:block}
.catalog-empty #cards,.catalog-error #cards{display:none}
.catalog-empty .controls,.catalog-error .controls{display:none}
.logo{width:72px!important;height:42px!important;filter:none!important;object-fit:contain!important;image-rendering:auto!important}
.header{gap:.72rem!important}
.logo-orb img{filter:none!important}
.tools-current-title{font-family:'Cinzel','Times New Roman',serif;font-size:.95rem;letter-spacing:.055em;margin:0 0 .6rem;color:#111}
.tools-tabs{display:grid;grid-template-columns:repeat(5,1fr);gap:0;padding:0;margin:0 0 1rem;border-bottom:1px solid #111}
.tools-tab{border:1px solid #d7d7d7;border-bottom:0;background:#fff;border-radius:10px 10px 0 0;min-height:38px;padding:.35rem .15rem;font:inherit;font-size:.67rem;color:#111;white-space:nowrap;margin:0 0 -1px -1px}
.tools-tab:first-child{margin-left:0}
.tools-tab[aria-selected="true"]{border-color:#111;background:#fff;position:relative;z-index:2;font-weight:700}
.tool-section-title{font-weight:700;margin:.1rem 0 .75rem}
.single-mode-tabs{display:grid;grid-template-columns:repeat(3,1fr);gap:.65rem;margin-bottom:1rem}
.single-mode-tab{border:1px solid #aaa;border-radius:14px;background:#f5f5f5;min-height:58px;font:inherit;color:#111;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.15rem}
.single-mode-tab[aria-selected="true"]{border-color:#111;background:#eee}
.single-mode-tab strong{font-size:.82rem}.single-mode-tab span{font-size:.65rem;color:#555}
.single-workspace{border:1px solid #aaa;border-radius:18px;background:#f3f3f3;padding:1rem;margin-bottom:1.6rem;min-height:150px}
.workspace-title{font-weight:700;margin-bottom:.65rem;font-size:.88rem}.workspace-text{font-size:.78rem;line-height:1.45;color:#111;margin-bottom:1.05rem}
.single-file-button{display:block;width:72%;margin:.25rem auto 0;border:1px solid #bbb;border-radius:13px;background:#fff;min-height:42px;font:inherit;font-size:.72rem;color:#111}
.single-next-box{border:1px solid #d0d0d0;border-radius:16px;background:#fff;padding:1rem;font-size:.72rem;line-height:1.45;color:#111}
.index-shell{padding-bottom:4.8rem}.index-info-card,.index-score-card,.index-range-summary{border:1px solid #aaa;border-radius:18px;background:#f7f7f7;padding:1rem;margin:0 0 1rem}.index-title,.index-subtitle{font-weight:700;font-size:1rem;margin-bottom:.55rem}.index-info-card div,.index-score-card div,.index-range-summary div{font-size:.82rem;line-height:1.45}.index-hint,.index-range-disclaimer{font-size:.64rem!important;color:#666}.index-score-selected,.index-range-summary-selected{font-weight:700;margin:.15rem 0 .35rem}.index-score-coefficient,.index-range-summary-coefficient{font-size:.72rem!important;color:#555;margin-bottom:.65rem}.score-range-selector{display:flex;gap:.4rem;margin:.65rem 0;overflow-x:auto;-webkit-overflow-scrolling:touch;padding-bottom:.2rem}.score-range-button{flex:0 0 108px;border:1px solid #c8c8c8;border-radius:13px;background:#fff;padding:.52rem .45rem;text-align:left;font:inherit;color:#111;min-height:58px}.score-range-button[aria-selected="true"]{border-color:#111;background:#efefef}.score-range-button strong{display:block;font-size:.75rem;line-height:1.1}.score-range-button span{display:block;font-size:.64rem;color:#555;margin-top:.12rem}.score-range-button small{display:block;font-size:.58rem;color:#777;margin-top:.12rem}.index-color-section{margin:0 0 .9rem}.index-color-section summary{list-style:none;border:1px solid #aaa;border-radius:13px;background:#f7f7f7;padding:.75rem 1rem;font-weight:700;font-size:1rem;cursor:pointer}.index-color-section summary::-webkit-details-marker{display:none}.index-color-section summary:before{content:'▶ ';font-weight:700}.index-color-section[open] summary{border-color:#555;background:#dedede}.index-color-section[open] summary:before{content:'▼ '}.index-matrix-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:.55rem 0 1rem;border:1px solid #bcbcbc;border-radius:10px;background:#fff}.index-matrix{min-width:760px;width:max-content;border-collapse:separate;border-spacing:0;table-layout:fixed;font-size:.72rem}.index-matrix th,.index-matrix td{border-right:1px solid #bcbcbc;border-bottom:1px solid #bcbcbc;text-align:center;padding:.5rem .25rem;vertical-align:middle;min-width:84px;background:#fff}.index-matrix thead th{background:#dedede;font-weight:400;position:sticky;top:0;z-index:2}.index-matrix thead th:first-child,.index-matrix tbody th{position:sticky;left:0;z-index:4;min-width:82px;width:82px;background:#f8f8f8;text-align:left;padding-left:.7rem;font-weight:400;box-shadow:2px 0 0 #bcbcbc}.index-matrix thead th:first-child{background:#dedede;z-index:5}.index-matrix tbody th{background:#fafafa}.index-cell-main{font-size:.72rem;line-height:1.15}.index-cell-sub{font-size:.65rem;line-height:1.15;margin-top:.18rem}.index-filter-button{position:fixed;left:50%;transform:translateX(-50%);bottom:calc(64px + env(safe-area-inset-bottom));z-index:34;width:100%;max-width:430px;border:1px solid #777;border-radius:20px 20px 0 0;background:#f3f3f3;min-height:58px;font:inherit;font-size:.92rem;color:#111}
'''
