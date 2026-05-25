def render_profile_page() -> str:
    return """
<div class="pageBody">
  <div class="system-state profile-guest">
    <div class="system-title">Гость</div>
    <div class="system-text">Вы пока не вошли. Регистрация и вход показаны как скелет интерфейса; backend, SMS/email и хранение профиля подключим позже.</div>
  </div>

  <div class="section-title profile-section-title">Тип профиля</div>
  <div class="roleGrid">
    <button class="roleCard selected" type="button">
      <div class="roleHeader">Покупатель</div>
      <div class="roleMeta">Каталог, избранное, корзина, запрос подбора.</div>
      <div class="roleStatus">MVP</div>
    </button>
    <button class="roleCard" type="button">
      <div class="roleHeader">Специалист / ювелир</div>
      <div class="roleMeta">Подбор под клиента, сравнение, будущие профессиональные возможности.</div>
      <div class="roleStatus">после верификации</div>
    </button>
    <button class="roleCard disabled" type="button" disabled>
      <div class="roleHeader">Поставщик / партнёр</div>
      <div class="roleMeta">Закрытый операционный сценарий. Не публичный продавец и не публикация камней.</div>
      <div class="roleStatus">позже</div>
    </button>
  </div>

  <div class="profileGrid profileAuthGrid">
    <div class="profileCard">
      <div class="profileTitle">Регистрация</div>
      <div class="muted">Создание профиля покупателя или специалиста. Пока без сохранения данных.</div>
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
