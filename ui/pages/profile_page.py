def render_profile_page() -> str:
    return """
<div class="pageBody">
  <div class="system-state profile-guest">
    <div class="system-title">Профиль будет подключён позже</div>
    <div class="system-text">Сейчас сайт работает как публичная витрина каталога, избранного и запросов. Регистрация, вход, роли и кабинет специалиста не активны в public MVP.</div>
  </div>

  <div class="profileCard authCard inactiveProfileCard">
    <div class="authPanel registerPanel" style="display:block">
      <div class="muted">Аккаунт пока не создаётся. В будущем профиль может использоваться для сохранения заявок, истории запросов и профессионального доступа.</div>
      <button class="btn light disabledStaticButton" type="button" disabled>Профиль недоступен в MVP</button>

      <div class="profileRoleAfterButton">
        <div class="muted roleIntro">Будущие режимы без активации</div>
        <div class="roleExplanation">
          <div class="rolePanel customerPanel" style="display:block">
            <div class="rolePanelTitle">Покупатель</div>
            <div class="rolePanelText">Будущий режим для сохранения камней, заявок и истории запросов. Сейчас не создаёт аккаунт.</div>
          </div>
          <div class="rolePanel specialistPanel" style="display:block;margin-top:.75rem">
            <div class="rolePanelTitle">Специалист</div>
            <div class="rolePanelText">Будущий режим для ювелиров, брендов, консультантов и экспертов. Доступ будет подключаться отдельно и может требовать проверки.</div>
          </div>
        </div>
        <div class="roleLater">Профессиональный кабинет, роли и привилегии не активны в текущем public MVP.</div>
      </div>
    </div>
  </div>
</div>
"""
