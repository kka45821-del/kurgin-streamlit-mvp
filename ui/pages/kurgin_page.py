HERO_VIDEO_URL = "https://raw.githubusercontent.com/kka45821-del/kurgin-streamlit-mvp/main/video.mp4?v=2"


HERO_VIDEO_WRAP_STYLE = (
    "width:min(100%,360px);"
    "margin:0 auto 1rem;"
    "border:1px solid #e6e0d8;"
    "border-radius:24px;"
    "overflow:hidden;"
    "background:#f7f7f7;"
    "box-shadow:0 14px 34px rgba(0,0,0,.06);"
)

HERO_VIDEO_STYLE = (
    "display:block;"
    "width:100%;"
    "aspect-ratio:16/10;"
    "object-fit:cover;"
)

HERO_VIDEO_ON_ENDED = "this.pause();this.currentTime=0;"

HERO_SIGNATURE_STYLE = (
    "max-width:360px;"
    "margin:.1rem auto 1rem;"
    "text-align:center;"
    "color:#111;"
)

HERO_TAGLINE_STYLE = (
    "font-family:'Cinzel','Times New Roman',serif;"
    "font-size:.82rem;"
    "letter-spacing:.08em;"
    "text-transform:none;"
    "margin-bottom:.58rem;"
)

HERO_POEM_STYLE = (
    "font-family:'Adine Kirnberg','Monotype Corsiva','Segoe Script','Brush Script MT',cursive;"
    "font-size:1.12rem;"
    "line-height:1.38;"
    "font-style:italic;"
    "letter-spacing:.01em;"
    "color:#333;"
)


def render_kurgin_page(logo_url: str) -> str:
    return f"""
<div class="k-info-page">
  <section class="hero">
    <div class="k-hero-video-wrap" style="{HERO_VIDEO_WRAP_STYLE}" aria-label="KURGIN visual introduction">
      <video class="k-hero-video" style="{HERO_VIDEO_STYLE}" autoplay muted playsinline preload="metadata" poster="{logo_url}" onended="{HERO_VIDEO_ON_ENDED}">
        <source src="{HERO_VIDEO_URL}" type="video/mp4">
        KURGIN visual introduction
      </video>
    </div>
    <div class="k-hero-signature" style="{HERO_SIGNATURE_STYLE}">
      <div class="k-hero-tagline" style="{HERO_TAGLINE_STYLE}">Luxury, measured in geometry.</div>
      <div class="k-hero-poem" style="{HERO_POEM_STYLE}">
        Не вымыслом красота живет<br>
        Ей мера строгая дана.<br>
        Где свет по граням ровно льет<br>
        Там гармония одна.
      </div>
    </div>
    <div class="hero-label">public MVP / витрина KURGIN</div>
    <div class="hero-text">KURGIN сейчас работает как публичная витрина лабораторных бриллиантов: можно смотреть каталог, сохранять интересные камни и отправлять запрос на уточнение условий.</div>
    <div class="trust-row"><span class="pill">каталог</span><span class="pill">избранное</span><span class="pill">запрос менеджеру</span></div>
  </section>

  <div class="section-title">Основные разделы</div>
  <div class="carousel">
    <button class="k-info-card" type="button" data-nav-page="catalog"><div><div class="card-kicker">Catalog</div><div class="card-title">KURGIN Diamonds</div><div class="card-text">Публичный каталог лабораторных бриллиантов. Доступность, цена и условия подтверждаются отдельно перед любым решением.</div></div><div class="card-link">Открыть каталог →</div></button>
    <button class="k-info-card" type="button" data-nav-page="tools"><div><div class="card-kicker">Tools</div><div class="card-title">KURGIN Tools</div><div class="card-text">KURGIN Index работает как базовый ориентир. Остальные инструменты показаны как MVP-скелет и подключаются отдельно.</div></div><div class="card-link">Открыть инструменты →</div></button>
    <button class="k-info-card" type="button" data-nav-page="favorites"><div><div class="card-kicker">Favorites</div><div class="card-title">Избранное</div><div class="card-text">Сохранённые в этом браузере камни. Это не резерв, не заказ и не фиксация цены.</div></div><div class="card-link">Открыть избранное →</div></button>
  </div>

  <div class="section-title">Важно</div>
  <div class="accordion">
    <details><summary>Статус MVP</summary><p>Публичный сайт сейчас работает как витрина и интерфейс запроса. Онлайн-покупка, оплата и checkout не активны.</p></details>
    <details><summary>Каталог и цены</summary><p>Если цена не показана, камень отображается как “по запросу”. Заявка не является заказом, резервом, оплатой или фиксацией цены.</p></details>
    <details><summary>Инструменты</summary><p>KURGIN Index доступен как базовый инструмент просмотра. Analyzer, Verify, Mass Analyzer и Academy остаются MVP-разделами без запуска расчётов.</p></details>
  </div>
</div>
"""
