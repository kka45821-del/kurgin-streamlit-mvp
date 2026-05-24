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
    .block-container {
        max-width: 430px;
        padding-top: 1rem;
        padding-bottom: 7rem;
    }
    .kurgin-bottom-nav {
        position: fixed;
        left: 50%;
        bottom: 0;
        transform: translateX(-50%);
        width: 100%;
        max-width: 430px;
        z-index: 999999;
        background: white;
        border-top: 1px solid rgba(49, 51, 63, 0.2);
        padding: 0.35rem 0.35rem 0.55rem 0.35rem;
        box-shadow: 0 -4px 18px rgba(0, 0, 0, 0.08);
    }
    .kurgin-bottom-nav div[data-testid="stHorizontalBlock"] {
        gap: 0.25rem;
    }
    .kurgin-bottom-nav .stButton > button {
        min-height: 48px;
        padding: 0.25rem 0.1rem;
        font-size: 0.72rem;
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


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


# --- Fixed bottom navigation ---
st.markdown('<div class="kurgin-bottom-nav">', unsafe_allow_html=True)
cols = st.columns(6)

for col, (page_key, icon, label) in zip(cols, TABS):
    with col:
        active = page_key == current_page
        button_label = f"{icon}\n{label}"
        if st.button(button_label, use_container_width=True, type="primary" if active else "secondary"):
            go(page_key)
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
