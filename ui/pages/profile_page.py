def render_profile_page() -> str:
    return """
<div class="pageBody">
  <div class="system-state profile-guest">
    <div class="system-title">Гость</div>
    <div class="system-text">Вы пока не вошли. В профиле будут доступны сохранённые камни, корзина и персональные сценарии подбора.</div>
  </div>

  <div class="profileCard authCard">
    <input class="authRadio" type="radio" name="auth-mode" id="auth-register" checked>
    <input class="authRadio" type="radio" name="auth-mode" id="auth-login">

    <div class="authSwitch">
      <label class="authOption authRegisterLabel" for="auth-register">Регистрация</label>
      <label class="authOption authLoginLabel" for="auth-login">Войти</label>
    </div>

    <div class="authPanel registerPanel">
      <div class="muted">Создайте стандартный профиль или выберите сценарий для специалистов ниже.</div>

      <div class="inputFake">Имя</div>
      <div class="inputFake">Телефон / email</div>
      <button class="btn">Зарегистрироваться</button>

      <div class="profileRoleAfterButton">
        <input class="roleRadio" type="radio" name="profile-role" id="role-customer" checked>
        <input class="roleRadio" type="radio" name="profile-role" id="role-specialist">

        <div class="muted roleIntro">Тип профиля</div>
        <div class="roleSwitch compactRoleSwitch">
          <label class="roleOption compactRoleOption roleCustomerLabel" for="role-customer">
            <div class="roleName">Стандартный</div>
          </label>
          <label class="roleOption compactRoleOption roleSpecialistLabel" for="role-specialist">
            <div class="roleName">Для специалистов</div>
          </label>
        </div>

        <div class="roleExplanation">
          <div class="rolePanel customerPanel">
            <div class="rolePanelTitle">Стандартный профиль</div>
            <div class="rolePanelText">Базовый сценарий для просмотра каталога, сохранения камней, корзины и запроса индивидуального подбора.</div>
          </div>
          <div class="rolePanel specialistPanel">
            <div class="rolePanelTitle">Профиль для специалистов</div>
            <div class="rolePanelText">Профессиональный сценарий для подбора под клиента, сравнения камней и будущих рабочих инструментов. Доступ будет требовать верификацию.</div>
            <div class="specialistRolesTitle">Возможные роли специалиста</div>
            <ul class="specialistRoleList">
              <li>Ювелир</li>
              <li>Ювелирная мастерская</li>
              <li>Геммолог / эксперт</li>
              <li>Консультант по подбору</li>
              <li>Дизайнер украшений</li>
              <li>Закупщик / байер</li>
            </ul>
          </div>
        </div>

        <div class="roleLater">Партнёрский доступ будет оформляться отдельно.</div>
      </div>
    </div>

    <div class="authPanel loginPanel">
      <div class="muted">Для входа будет использоваться код или ссылка, отправленные на телефон / email.</div>
      <div class="inputFake">Телефон / email</div>
      <button class="btn light">Получить код / ссылку входа</button>
    </div>
  </div>
</div>
"""
