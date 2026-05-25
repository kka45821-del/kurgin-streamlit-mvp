SYSTEM_CSS = r'''
.system-state{border:1px solid #d7d7d7;border-radius:18px;background:#fff;padding:1rem;margin-bottom:1rem;box-shadow:0 10px 24px rgba(0,0,0,.04)}
.system-title,.empty-title{font-weight:700;margin-bottom:.35rem}
.system-text{color:#666;font-size:.86rem;line-height:1.45}
.authCard{margin-top:.75rem}
.authRadio,.roleRadio{position:absolute;opacity:0;pointer-events:none}
.authSwitch{display:grid;grid-template-columns:1fr 1fr;gap:.5rem;margin-bottom:1rem}
.authOption{border:1px solid #d7d7d7;border-radius:14px;background:#fff;padding:.75rem;text-align:center;font-weight:700;font-size:.9rem;cursor:pointer}
#auth-register:checked ~ .authSwitch .authRegisterLabel,#auth-login:checked ~ .authSwitch .authLoginLabel{border-color:#111;background:#fafafa}
.authPanel{display:none}
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
'''
