def render_kurgin_page(logo_url: str) -> str:
    return f"""
<div class="k-info-page">
  <section class="hero">
    <div class="logo-orb"><img src="{logo_url}" alt="KURGIN"></div>
    <div class="hero-label">информационная страница платформы</div>
    <div class="hero-text">KURGIN помогает покупать, подбирать и анализировать лабораторные бриллианты через каталог, Analyzer, Index, отчёты и инструменты для специалистов.</div>
    <div class="trust-row"><span class="pill">лабораторные бриллианты</span><span class="pill">документная основа</span><span class="pill">quality analysis</span></div>
  </section>
  <div class="section-title">Направления платформы</div>
  <div class="carousel">
    <button class="k-info-card" type="button" data-nav-page="catalog"><div><div class="card-kicker">Catalog</div><div class="card-title">Каталог KURGIN</div><div class="card-text">Лабораторные бриллианты из подтверждённого наличия KURGIN.</div></div><div class="card-link">Открыть каталог →</div></button>
    <button class="k-info-card" type="button" data-nav-page="tools"><div><div class="card-kicker">Analyzer</div><div class="card-title">Полный анализ одного камня</div><div class="card-text">Karo Score 0–100, теги, риски, сильные стороны и интерпретации внутри KURGIN Analyzer.</div></div><div class="card-link">Открыть инструменты →</div></button>
    <button class="k-info-card" type="button" data-nav-page="tools"><div><div class="card-kicker">Index</div><div class="card-title">KURGIN Index</div><div class="card-text">Рыночный ориентир / market benchmark для сопоставимости лабораторных бриллиантов.</div></div><div class="card-link">Открыть инструменты →</div></button>
    <button class="k-info-card" type="button" data-nav-page="profile"><div><div class="card-kicker">Specialists</div><div class="card-title">Для специалистов</div><div class="card-text">Рабочие сценарии для ювелиров, мастерских и консультантов через верификацию и назначенные возможности.</div></div><div class="card-link">Перейти в профиль →</div></button>
  </div>
  <div class="section-title">Информация</div>
  <div class="accordion">
    <details><summary>О KURGIN</summary><p>KURGIN — информационная, коммерческая и аналитическая платформа для лабораторных бриллиантов. Каталог, анализ, документы, отчёты и запросы разделены по смыслу и состояниям.</p></details>
    <details><summary>Как работает платформа</summary><p>Пользователь может изучить каталог, открыть карточку камня, посмотреть документную основу, использовать Analyzer / Karo Score там, где результат есть, и обращаться за подбором или сложным запросом.</p></details>
    <details><summary>Что такое KURGIN Analyzer</summary><p>Analyzer — полный анализ качества одного лабораторного бриллианта: Karo Score 0–100, теги, риски, сильные стороны и интерпретации. Analyzer не является сертификатом и не оценивает цену.</p></details>
    <details><summary>Что такое Karo Score</summary><p>Karo Score — числовой коэффициент внутри результата KURGIN Analyzer. Он помогает понимать качество, но не является отдельным инструментом, финансовым рейтингом или гарантией.</p></details>
    <details><summary>Что такое KURGIN Index</summary><p>KURGIN Index / рыночный ориентир / market benchmark помогает с рыночной сопоставимостью. Это не точная цена конкретного камня и не финансовый индекс.</p></details>
    <details><summary>Документы</summary><div class="doc-box">Здесь позже будут материалы, документы, PDF, методологии, условия и FAQ, управляемые из админки.</div></details>
    <details><summary>Контакты</summary><p>Блок контактов используется для вопросов, подбора, документов, обращений по платформе и manager-assisted сценариев.</p></details>
  </div>
</div>
"""
