def render_profile_page() -> str:
    return """
<div class="pageBody">
  <div class="profileGrid">
    <div class="profileCard"><div class="profileTitle">Регистрация</div><div class="muted">Создание профиля покупателя или специалиста. Функционал подключим позже.</div><div class="inputFake">Имя</div><div class="inputFake">Телефон / email</div><button class="btn">Зарегистрироваться</button></div>
    <div class="profileCard"><div class="profileTitle">Войти</div><div class="muted">Вход в личный кабинет. Пока без авторизации, только скелет.</div><div class="inputFake">Телефон / email</div><button class="btn light">Войти</button></div>
  </div>
</div>
"""
