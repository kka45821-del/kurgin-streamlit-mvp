def render_profile_page() -> str:
    return """
<div class="pageBody">
  <div class="system-state profile-guest">
    <div class="system-title">Гость</div>
    <div class="system-text">Вы пока не вошли. Регистрация и вход показаны как скелет интерфейса; backend, SMS/email и хранение профиля подключим позже.</div>
  </div>

  <div class="profileGrid profileAuthGrid">
    <div class="profileCard">
      <div class="profileTitle">Регистрация</div>
      <div class="muted">Выберите тип профиля. По умолчанию выбран покупатель.</div>

      <div class="roleSwitch" data-role-switch>
        <button class="roleOption selected" type="button" data-role="customer">
          <div class="roleName">Покупатель</div>
          <div class="roleHint">каталог, избранное, корзина</div>
        </button>
        <button class="roleOption" type="button" data-role="specialist">
          <div class="roleName">Специалист</div>
          <div class="roleHint">ювелир / консультант</div>
        </button>
      </div>

      <div class="roleExplanation">
        <div class="rolePanel active" data-role-panel="customer">
          <div class="rolePanelTitle">Покупатель</div>
          <div class="rolePanelText">Базовый профиль для просмотра каталога, сохранения камней, корзины и запроса индивидуального подбора.</div>
        </div>
        <div class="rolePanel" data-role-panel="specialist">
          <div class="rolePanelTitle">Специалист / ювелир</div>
          <div class="rolePanelText">Профессиональный сценарий для подбора под клиента, сравнения камней и будущих рабочих инструментов. Доступ будет требовать верификацию.</div>
        </div>
      </div>

      <div class="roleLater">Поставщик / партнёр — отдельный закрытый сценарий. Добавим позже, не как публичную регистрацию.</div>

      <div class="inputFake">Имя</div>
      <div class="inputFake">Телефон / email</div>
      <button class="btn">Зарегистрироваться</button>
    </div>
    <div class="profileCard">
      <div class="profileTitle">Войти</div>
      <div class="muted">Вход в личный кабинет. Авторизация будет подключена отдельным backend-этапом.</div>
      <div class="inputFake">Телефон / email</div>
      <button class="btn light">Войти</button>
    </div>
  </div>
</div>
"""
