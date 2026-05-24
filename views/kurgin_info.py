import streamlit as st


def render_kurgin_info_page():
    st.markdown(
        '''
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600&display=swap');
.kurgin-info-page{
    min-height:calc(100vh - 76px);
    padding:0 1rem 5.8rem;
    background:
        radial-gradient(circle at 50% 7%, rgba(255,255,255,.36) 0, rgba(245,245,245,.22) 18%, rgba(255,255,255,0) 44%),
        linear-gradient(180deg,#ffffff 0%,#f8f8f8 48%,#ffffff 100%);
    color:#111;
}
.kurgin-info-header{
    position:sticky;
    top:0;
    z-index:10;
    margin:0 -1rem;
    padding:.82rem 1rem .76rem;
    background:rgba(255,255,255,.94);
    border-bottom:1px solid #ddd;
    text-align:center;
    backdrop-filter:blur(10px);
}
.kurgin-platform-title{
    font-family:'Cinzel','Times New Roman',serif!important;
    font-size:1.2rem;
    line-height:1.05;
    font-weight:500;
    letter-spacing:.075em;
}
.kurgin-platform-subtitle{
    margin-top:.28rem;
    color:#6f6f6f;
    font-size:.72rem;
    letter-spacing:.09em;
}
.kurgin-hero{
    padding:1.3rem 0 1rem;
    text-align:center;
}
.kurgin-logo-orb{
    width:188px;
    height:188px;
    margin:0 auto .85rem;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    background:
        radial-gradient(circle, rgba(255,255,255,.98) 0%, rgba(247,247,247,.86) 42%, rgba(231,231,231,.42) 67%, rgba(255,255,255,0) 78%);
    box-shadow:
        0 0 34px rgba(0,0,0,.08),
        inset 0 0 34px rgba(255,255,255,.9);
}
.kurgin-logo-orb img{
    width:128px;
    height:128px;
    object-fit:contain;
    filter:drop-shadow(0 8px 14px rgba(0,0,0,.16));
}
.kurgin-hero-text{
    color:#555;
    font-size:.9rem;
    line-height:1.45;
    max-width:330px;
    margin:.65rem auto 0;
}
.kurgin-trust-row{
    display:flex;
    gap:.35rem;
    justify-content:center;
    flex-wrap:wrap;
    margin:1rem 0 .2rem;
}
.kurgin-trust-pill{
    border:1px solid #ddd;
    border-radius:999px;
    padding:.32rem .62rem;
    background:rgba(255,255,255,.72);
    font-size:.68rem;
    color:#555;
}
.kurgin-section-title{
    margin:1.05rem 0 .62rem;
    font-size:.82rem;
    color:#777;
    letter-spacing:.08em;
    text-transform:uppercase;
}
.kurgin-carousel{
    display:flex;
    gap:.72rem;
    margin:0 -1rem;
    padding:.1rem 1rem .85rem;
    overflow-x:auto;
    scroll-snap-type:x mandatory;
    -webkit-overflow-scrolling:touch;
}
.kurgin-card{
    flex:0 0 78%;
    min-height:148px;
    scroll-snap-align:center;
    border:1px solid #d7d7d7;
    border-radius:20px;
    background:#fff;
    color:#111!important;
    text-decoration:none!important;
    padding:1rem;
    box-shadow:0 10px 24px rgba(0,0,0,.045);
    display:flex;
    flex-direction:column;
    justify-content:space-between;
}
.kurgin-card-kicker{
    font-size:.68rem;
    color:#777;
    letter-spacing:.06em;
    text-transform:uppercase;
}
.kurgin-card-title{
    margin-top:.28rem;
    font-size:1.02rem;
    font-weight:700;
}
.kurgin-card-text{
    margin-top:.45rem;
    color:#555;
    font-size:.82rem;
    line-height:1.35;
}
.kurgin-card-link{
    margin-top:.75rem;
    font-size:.78rem;
    color:#222;
}
.kurgin-accordion{
    margin-top:.2rem;
}
.kurgin-accordion details{
    border:1px solid #ddd;
    border-radius:16px;
    background:#fff;
    margin-bottom:.55rem;
    padding:.72rem .82rem;
}
.kurgin-accordion summary{
    cursor:pointer;
    font-size:.92rem;
    font-weight:600;
}
.kurgin-accordion p{
    color:#555;
    font-size:.82rem;
    line-height:1.45;
}
.kurgin-doc-box{
    border:1px dashed #bbb;
    border-radius:16px;
    padding:.8rem;
    background:#fff;
    color:#555;
    font-size:.82rem;
    line-height:1.45;
}
</style>
''',
        unsafe_allow_html=True,
    )

    st.markdown(
        '''
<div class="kurgin-info-page">
  <div class="kurgin-info-header">
    <div class="kurgin-platform-title">KURGIN Platform</div>
    <div class="kurgin-platform-subtitle">Совершенство создаётся</div>
  </div>

  <section class="kurgin-hero">
    <div class="kurgin-logo-orb">
      <img src="https://raw.githubusercontent.com/kka45821-del/kurgin-streamlit-mvp/main/Vectorr.svg?v=16" alt="KURGIN">
    </div>
    <div class="kurgin-hero-text">
      Платформа для покупки, подбора и анализа лабораторных бриллиантов: каталог, Analyzer, Karo Score, Index и инструменты для специалистов.
    </div>
    <div class="kurgin-trust-row">
      <span class="kurgin-trust-pill">лабораторные бриллианты</span>
      <span class="kurgin-trust-pill">документная основа</span>
      <span class="kurgin-trust-pill">quality analysis</span>
    </div>
  </section>

  <div class="kurgin-section-title">Возможности платформы</div>
  <div class="kurgin-carousel">
    <a class="kurgin-card" href="?page=catalog" target="_self">
      <div>
        <div class="kurgin-card-kicker">Catalog</div>
        <div class="kurgin-card-title">Каталог KURGIN</div>
        <div class="kurgin-card-text">Лабораторные бриллианты из подтверждённого наличия KURGIN.</div>
      </div>
      <div class="kurgin-card-link">Открыть каталог →</div>
    </a>
    <a class="kurgin-card" href="?page=tools" target="_self">
      <div>
        <div class="kurgin-card-kicker">Analyzer</div>
        <div class="kurgin-card-title">KURGIN Analyzer</div>
        <div class="kurgin-card-text">Интерпретация качества и параметров лабораторного бриллианта.</div>
      </div>
      <div class="kurgin-card-link">Открыть инструменты →</div>
    </a>
    <a class="kurgin-card" href="?page=tools" target="_self">
      <div>
        <div class="kurgin-card-kicker">Karo Score</div>
        <div class="kurgin-card-title">Karo Score</div>
        <div class="kurgin-card-text">Показатель внутри результата KURGIN Analyzer, не отдельная финансовая оценка.</div>
      </div>
      <div class="kurgin-card-link">Смотреть объяснение →</div>
    </a>
    <a class="kurgin-card" href="?page=tools" target="_self">
      <div>
        <div class="kurgin-card-kicker">Index</div>
        <div class="kurgin-card-title">KURGIN Index</div>
        <div class="kurgin-card-text">Рыночный ориентир / market benchmark для сопоставимости лабораторных бриллиантов.</div>
      </div>
      <div class="kurgin-card-link">Открыть инструменты →</div>
    </a>
    <a class="kurgin-card" href="?page=profile" target="_self">
      <div>
        <div class="kurgin-card-kicker">Specialists</div>
        <div class="kurgin-card-title">Для специалистов</div>
        <div class="kurgin-card-text">Рабочие сценарии для ювелиров, мастерских и консультантов через верификацию и назначенные возможности.</div>
      </div>
      <div class="kurgin-card-link">Перейти в профиль →</div>
    </a>
  </div>

  <div class="kurgin-section-title">Информация</div>
  <div class="kurgin-accordion">
    <details>
      <summary>О KURGIN</summary>
      <p>KURGIN — платформа для лабораторных бриллиантов. Здесь разделяются покупка, подбор, анализ качества, документы и сервисные состояния.</p>
    </details>
    <details>
      <summary>Что такое KURGIN Analyzer</summary>
      <p>Analyzer помогает интерпретировать качество лабораторного бриллианта по доступным параметрам. Он не заменяет лабораторный документ и не является оценкой цены.</p>
    </details>
    <details>
      <summary>Что такое Karo Score</summary>
      <p>Karo Score — часть результата KURGIN Analyzer. Он помогает сравнивать качество, но не является инвестиционным рейтингом и не должен быть единственным критерием выбора.</p>
    </details>
    <details>
      <summary>Что такое KURGIN Index</summary>
      <p>KURGIN Index / рыночный ориентир / market benchmark помогает с рыночной сопоставимостью. Это не точная цена конкретного камня и не финансовый индекс.</p>
    </details>
    <details>
      <summary>Документы</summary>
      <div class="kurgin-doc-box">Здесь позже будут материалы, документы, PDF, методологии, условия и FAQ, управляемые из админки.</div>
    </details>
    <details>
      <summary>Контакты</summary>
      <p>Блок контактов будет использоваться для вопросов, подбора, документов и обращений по платформе.</p>
    </details>
  </div>
</div>
''',
        unsafe_allow_html=True,
    )
