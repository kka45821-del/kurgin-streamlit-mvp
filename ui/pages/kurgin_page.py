def render_kurgin_page(logo_url: str) -> str:
    return f"""
<div class="k-info-page">
  <section class="hero">
    <div class="logo-orb"><img src="{logo_url}" alt="KURGIN"></div>
    <div class="hero-label">публичная витрина KURGIN</div>
    <div class="hero-text">KURGIN помогает смотреть каталог лабораторных бриллиантов, сохранять интересные камни и отправлять запрос на уточнение условий.</div>
    <div class="trust-row"><span class="pill">каталог</span><span class="pill">избранное</span><span class="pill">запрос</span></div>
  </section>

  <div class="section-title">Основные разделы</div>
  <div class="carousel">
    <button class="k-info-card" type="button" data-nav-page="catalog"><div><div class="card-kicker">Catalog</div><div class="card-title">KURGIN Diamonds</div><div class="card-text">Публичный каталог лабораторных бриллиантов. Доступность и условия уточняются по запросу.</div></div><div class="card-link">Открыть каталог →</div></button>
    <button class="k-info-card" type="button" data-nav-page="tools"><div><div class="card-kicker">Tools</div><div class="card-title">KURGIN Tools</div><div class="card-text">Скелет инструментов анализа, проверки, индекса и обучения. Расчёты подключаются отдельно.</div></div><div class="card-link">Открыть инструменты →</div></button>
    <button class="k-info-card" type="button" data-nav-page="favorites"><div><div class="card-kicker">Favorites</div><div class="card-title">Избранное</div><div class="card-text">Сохранённые в этом браузере камни. Это не резерв и не фиксация цены.</div></div><div class="card-link">Открыть избранное →</div></button>
  </div>

  <div class="section-title">Важно</div>
  <div class="accordion">
    <details><summary>Статус платформы</summary><p>Публичный сайт сейчас работает как витрина и интерфейс запроса. Онлайн-покупка и checkout не активны.</p></details>
    <details><summary>Каталог и цены</summary><p>Если цена не показана, камень отображается как “по запросу”. Заявка не является заказом, резервом или фиксацией цены.</p></details>
    <details><summary>Инструменты</summary><p>KURGIN Tools представлены как UX-скелет. Подключение расчётов, индекса и массового анализа выполняется отдельными этапами.</p></details>
  </div>
</div>
"""
