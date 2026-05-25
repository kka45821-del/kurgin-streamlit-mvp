def render_profile_page() -> str:
    return """
<div class="pageBody">
  <div class="system-state profile-guest">
    <div class="system-title">Гость</div>
    <div class="system-text">Вы пока не вошли. Регистрация и вход показаны как скелет интерфейса; backend, SMS/email и хранение профиля подключим позже.</div>
  </div>

  <div class="profileCard authCard">
    <input class="authRadio" type="radio" name="auth-mode" id="auth-register" checked>
    <input class="authRadio" type="radio" name="auth-mode" id="auth-login">

    <div class="authSwitch">
      <label class="authOption authRegisterLabel" for="auth-register">Регистрация</label>
      <label class="authOption authLoginLabel" for="auth-login">Войти</label>
    </div>

    <div class="authPanel registerPanel">
      <div class="profileTitle">Регистрация</div>
      <div class="muted">Базовая регистрация. По умолчанию создаётся профиль покупателя; тип профиля можно уточнить ниже.</div>

      <div class="inputFake">Имя</div>
      <div class="inputFake">Телефон / email</div>
      <button class="btn">Зарегистрироваться</button>

      <div class="profileRoleAfterButton">
        <input class="roleRadio" type="radio" name="profile-role" id="role-customer" checked>
        <input class="roleRadio" type="radio" name="profile-role" id="role-specialist">

        <div class="muted roleIntro">Тип профиля</div>
        <div class="roleSwitch">
          <label class="roleOption roleCustomerLabel" for="role-customer">
            <div class="roleName">Покупатель</div>
            <div class="roleHint">каталог, избранное, корзина</div>
          </label>
          <label class="roleOption roleSpecialistLabel" for="role-specialist">
            <div class="roleName">Специалист</div>
            <div class="roleHint">ювелир / консультант</div>
          </label>
        </div>

        <div class="roleExplanation">
          <div class="rolePanel customerPanel">
            <div class="rolePanelTitle">Покупатель</div>
            <div class="rolePanelText">Базовый профиль для просмотра каталога, сохранения камней, корзины и запроса индивидуального подбора.</div>
          </div>
          <div class="rolePanel specialistPanel">
            <div class="rolePanelTitle">Специалист / ювелир</div>
            <div class="rolePanelText">Профессиональный сценарий для подбора под клиента, сравнения камней и будущих рабочих инструментов. Доступ будет требовать верификацию.</div>
          </div>
        </div>

        <div class="roleLater">Поставщик / партнёр — отдельный закрытый сценарий. Добавим позже, не как публичную регистрацию.</div>
      </div>
    </div>

    <div class="authPanel loginPanel">
      <div class="profileTitle">Войти</div>
      <div class="muted">Вход в личный кабинет. Авторизация будет подключена отдельным backend-этапом.</div>
      <div class="inputFake">Телефон / email</div>
      <button class="btn light">Войти</button>
    </div>
  </div>
</div>
"""
