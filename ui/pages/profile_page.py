def render_profile_page() -> str:
    return """
<div class="pageBody">
  <div class="system-state profile-guest">
    <div class="system-title">Профиль</div>
    <div class="system-text">Аккаунт, роли и кабинет специалиста будут подключены позже. Сейчас сайт можно использовать как публичную витрину каталога и запросов.</div>
  </div>

  <div class="profileCard authCard">
    <input class="authRadio" type="radio" name="auth-mode" id="auth-register" checked>
    <input class="authRadio" type="radio" name="auth-mode" id="auth-login">

    <div class="authSwitch">
      <label class="authOption authRegisterLabel" for="auth-register">Профиль</label>
      <label class="authOption authLoginLabel" for="auth-login">Вход позже</label>
    </div>

    <div class="authPanel registerPanel">
      <div class="muted">Регистрация пока не активна. В будущем профиль будет использоваться для сохранения сценариев, заявок и профессионального доступа.</div>
      <div class="inputFake">Имя</div>
      <div class="inputFake">Телефон / email</div>
      <button class="btn light" type="button">Недоступно в MVP</button>

      <div class="profileRoleAfterButton">
        <input class="roleRadio" type="radio" name="profile-role" id="role-customer" checked>
        <input class="roleRadio" type="radio" name="profile-role" id="role-specialist">

        <div class="muted roleIntro">Будущие режимы</div>
        <div class="roleSwitch compactRoleSwitch">
          <label class="roleOption compactRoleOption roleCustomerLabel" for="role-customer">
            <div class="roleName">Покупатель</div>
          </label>
          <label class="roleOption compactRoleOption roleSpecialistLabel" for="role-specialist">
            <div class="roleName">Специалист</div>
          </label>
        </div>

        <div class="roleExplanation">
          <div class="rolePanel customerPanel">
            <div class="rolePanelTitle">Покупатель</div>
            <div class="rolePanelText">Будущий режим для сохранения камней, заявок и истории запросов.</div>
          </div>
          <div class="rolePanel specialistPanel">
            <div class="rolePanelTitle">Специалист</div>
            <div class="rolePanelText">Будущий режим для ювелиров, брендов, консультантов и экспертов. Доступ будет подключаться отдельно и может требовать проверки.</div>
          </div>
        </div>

        <div class="roleLater">Профессиональный кабинет не активен в текущем public MVP.</div>
      </div>
    </div>

    <div class="authPanel loginPanel">
      <div class="muted">Вход будет подключён позже. Сейчас на этой странице нет рабочей авторизации.</div>
      <div class="inputFake">Телефон / email</div>
      <button class="btn light" type="button">Вход пока недоступен</button>
    </div>
  </div>
</div>
"""
