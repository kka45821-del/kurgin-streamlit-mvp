import streamlit as st

st.set_page_config(
    page_title="KURGIN MVP",
    page_icon="💎",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- Basic mobile-first state ---
if "page" not in st.session_state:
    st.session_state.page = "kurgin"


def go(page: str) -> None:
    st.session_state.page = page


PAGES = {
    "kurgin": "О KURGIN",
    "tools": "Инструменты",
    "catalog": "Каталог",
    "favorites": "Избранное",
    "cart": "Корзина",
    "profile": "Профиль",
}

TABS = [
    ("kurgin", "💎", "KURGIN"),
    ("tools", "🛠", "Инстр."),
    ("catalog", "🔍", "Каталог"),
    ("favorites", "🤍", "Избр."),
    ("cart", "🛒", "Корзина"),
    ("profile", "👤", "Профиль"),
]


# --- Temporary mobile CSS for functional skeleton ---
st.markdown(
    """
    <style>
    header[data-testid="stHeader"] {
        display: none;
    }
    div[data-testid="stToolbar"] {
        display: none;
    }
    .block-container {
        max-width: 430px;
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
        padding-bottom: 7rem;
    }
    .kurgin-bottom-nav {
        position: fixed;
        left: 0;
        right: 0;
        bottom: 0;
        width: 100%;
        z-index: 999999;
        background: white;
        border-top: 1px solid rgba(49, 51, 63, 0.18);
        padding: 0.25rem 0.25rem calc(0.45rem + env(safe-area-inset-bottom));
        box-shadow: 0 -4px 18px rgba(0, 0, 0, 0.08);
    }
    .kurgin-nav-grid {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 0.2rem;
        max-width: 430px;
        margin: 0 auto;
    }
    .kurgin-tab {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 48px;
        border-radius: 12px;
        border: 1px solid rgba(49, 51, 63, 0.18);
        background: #ffffff;
        color: #31333f !important;
        text-decoration: none !important;
        font-size: 0.68rem;
        line-height: 1.1;
        white-space: nowrap;
    }
    .kurgin-tab-active {
        background: #ff4b4b;
        border-color: #ff4b4b;
        color: #ffffff !important;
    }
    .kurgin-icon {
        font-size: 1rem;
        line-height: 1;
        margin-bottom: 0.15rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --- Navigation from query param ---
query_params = st.query_params
requested_page = query_params.get("page")
if requested_page in PAGES and requested_page != st.session_state.page:
    st.session_state.page = requested_page
    st.rerun()


# --- Page content ---
st.title("KURGIN")
st.caption("Черновой mobile-first MVP без финального дизайна")

current_page = st.session_state.page
st.subheader(PAGES[current_page])
st.divider()

if current_page == "kurgin":
    st.write("Публичная витрина KURGIN: лабораторные бриллианты, инструменты анализа, индекс цен и доверительная информация.")

elif current_page == "tools":
    st.write("Здесь будут инструменты KURGIN.")
    st.button("KURGIN Score Analyzer", use_container_width=True)
    st.button("Сравнение камней", use_container_width=True)
    st.button("Индекс цен", use_container_width=True)

elif current_page == "catalog":
    st.write("Каталог лабораторных бриллиантов. На первом этапе — фильтры и карточки-заглушки.")
    with st.expander("Фильтры"):
        st.selectbox("Форма", ["Round", "Oval", "Emerald", "Princess", "Cushion"])
        st.slider("Карат", 0.3, 5.0, (1.0, 2.0))
        st.selectbox("Цвет", ["D", "E", "F", "G", "H", "I"])
    for i in range(1, 4):
        st.container(border=True).write(f"Камень #{i} · Round · 1.{i} ct · IGI · добавить в избранное / корзину")

elif current_page == "favorites":
    st.write("Избранные камни пользователя. Пока пусто.")

elif current_page == "cart":
    st.write("Корзина / резерв. Пока пусто.")

elif current_page == "profile":
    st.write("Профиль, вход, регистрация и выбор роли.")
    st.selectbox("Роль", ["Гость", "Покупатель", "Ювелир", "Геммолог", "Партнёр"])


# --- Fixed bottom navigation as real HTML links ---
nav_items = []
for page_key, icon, label in TABS:
    active_class = " kurgin-tab-active" if page_key == current_page else ""
    nav_items.append(
        f'<a class="kurgin-tab{active_class}" href="?page={page_key}" target="_self">'
        f'<span class="kurgin-icon">{icon}</span><span>{label}</span></a>'
    )

st.markdown(
    '<nav class="kurgin-bottom-nav"><div class="kurgin-nav-grid">'
    + "".join(nav_items)
    + '</div></nav>',
    unsafe_allow_html=True,
)
