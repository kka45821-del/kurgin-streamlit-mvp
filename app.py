import html

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="KURGIN MVP",
    page_icon="💎",
    layout="centered",
    initial_sidebar_state="collapsed",
)

PAGES = {
    "kurgin": "О KURGIN",
    "tools": "Инструменты",
    "catalog": "Каталог",
    "favorites": "Избранное",
    "cart": "Корзина",
    "profile": "Профиль",
}

TABS = [
    ("kurgin", "♢", "KURGIN"),
    ("tools", "♢", "Инстр."),
    ("catalog", "◇", "Каталог"),
    ("favorites", "♡", "Избр."),
    ("cart", "◠", "Корзина"),
    ("profile", "○", "Профиль"),
]

if "page" not in st.session_state:
    st.session_state.page = "catalog"

requested_page = st.query_params.get("page")
if requested_page in PAGES:
    st.session_state.page = requested_page

current_page = st.session_state.page

st.markdown(
    """
<style>
header[data-testid="stHeader"], div[data-testid="stToolbar"] { display: none; }
.block-container { max-width: 430px; padding: 0 !important; }
div[data-testid="stElementContainer"] { margin: 0 !important; }
iframe {
    display: block !important;
    width: 100% !important;
    height: 100dvh !important;
    min-height: 100svh !important;
    border: 0 !important;
}
.page-pad { padding: 1rem; }
.kurgin-bottom-nav { position: fixed; left: 0; right: 0; bottom: 0; width: 100%; z-index: 999999; background: #fff; border-top: 1px solid rgba(49,51,63,.18); padding: .25rem .25rem calc(.45rem + env(safe-area-inset-bottom)); }
.kurgin-nav-grid { display: grid; grid-template-columns: repeat(6,1fr); gap: .2rem; max-width: 430px; margin: 0 auto; }
.kurgin-tab { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 52px; border-radius: 12px; color: #888!important; text-decoration: none!important; font-size: .68rem; line-height: 1.1; white-space: nowrap; }
.kurgin-tab-active { background: #f2f5f8; color: #111!important; border: 1px solid #cfd5dc; }
.kurgin-icon { font-size: 1.15rem; line-height: 1; margin-bottom: .15rem; }
</style>
""",
    unsafe_allow_html=True,
)


def weight_group(carat: float) -> str:
    if carat < 1.5:
        return "1–1.49"
    if carat < 2.0:
        return "1.5–1.99"
    if carat < 2.5:
        return "2–2.49"
    return "2.5–2.99"


def score_group(score: float) -> str:
    if score < 50:
        return "0–49"
    if score < 80:
        return "50–79"
    if score < 90:
        return "80–89"
    if score < 95:
        return "90–94.9"
    if score < 99:
        return "95–98"
    return "99+"


def stone_card(stone: dict) -> str:
    tags = "".join(
        f'<span class="tag {html.escape(cls)}">{html.escape(label)}</span>'
        for label, cls in stone["tags"]
    )
    data = {
        "shape": stone["shape_filter"],
        "weight": weight_group(float(stone["carat"])),
        "color": stone["color"],
        "clarity": stone["clarity"],
        "score": score_group(float(stone["score"])),
        "fluorescence": stone["fluorescence"],
        "finish": stone["finish"],
    }
    data_attrs = " ".join(f'data-{key}="{html.escape(value)}"' for key, value in data.items())
    return f"""
    <div class="stone-card" {data_attrs}>
      <div class="stone-main">
        <div>{html.escape(stone['shape'])}</div>
        <div>{html.escape(str(stone['carat']))}</div>
        <div>{html.escape(stone['color'])}</div>
        <div>{html.escape(stone['clarity'])}</div>
        <div>{html.escape(str(stone['score']))}</div>
        <div class="price">{html.escape(stone['price'])} ₽</div>
      </div>
      <div class="stone-line"></div>
      <div class="stone-meta"><div>{html.escape(stone['meta'])}</div><div class="tags">{tags}</div></div>
      <div class="actions"><div>♡</div><div>▣</div><div>ⓘ</div><div>♡</div><div>⌞</div><div>⌯</div></div>
    </div>
    """


STONES = [
    {"shape": "Круг", "shape_filter": "Round", "carat": "1.05", "color": "G", "clarity": "VVS1", "score": "95", "price": "32 200", "meta": "6.5 мм · ex ex vg · none", "fluorescence": "None", "finish": "2Ex/1VG+", "tags": [("огонь", ""), ("блеск", "tag-blue")]},
    {"shape": "Круг", "shape_filter": "Round", "carat": "1.51", "color": "E", "clarity": "VS1", "score": "86", "price": "58 500", "meta": "7.4 мм · ex ex vg · none", "fluorescence": "None", "finish": "2Ex/1VG+", "tags": [("контраст", "tag-gray"), ("огонь", "")]},
    {"shape": "Круг", "shape_filter": "Round", "carat": "1.00", "color": "F", "clarity": "VS2", "score": "77", "price": "34 900", "meta": "6.4 мм · ex ex vg · none", "fluorescence": "None", "finish": "2Ex/1VG+", "tags": [("БАЛАНС", "")]},
    {"shape": "Круг", "shape_filter": "Round", "carat": "1.22", "color": "D", "clarity": "VVS2", "score": "92", "price": "41 800", "meta": "6.9 мм · ex ex ex · none", "fluorescence": "None", "finish": "Ex/Ex/Ex+", "tags": [("блеск", "tag-blue"), ("огонь", "")]},
    {"shape": "Круг", "shape_filter": "Round", "carat": "1.74", "color": "F", "clarity": "VS1", "score": "89", "price": "67 900", "meta": "7.8 мм · ex ex vg · faint", "fluorescence": "Faint", "finish": "2Ex/1VG+", "tags": [("контраст", "tag-gray"), ("блеск", "tag-blue")]},
    {"shape": "Круг", "shape_filter": "Round", "carat": "2.03", "color": "G", "clarity": "VS2", "score": "84", "price": "88 400", "meta": "8.1 мм · ex vg vg · none", "fluorescence": "None", "finish": "2Ex/1VG+", "tags": [("БАЛАНС", "")]},
    {"shape": "Круг", "shape_filter": "Round", "carat": "2.41", "color": "E", "clarity": "VVS1", "score": "96", "price": "126 300", "meta": "8.7 мм · ex ex ex · none", "fluorescence": "None", "finish": "Ex/Ex/Ex+", "tags": [("огонь", ""), ("блеск", "tag-blue")]},
]

cards_html = "".join(stone_card(stone) for stone in STONES)

LOGO_SVG = '<svg width="107" height="59" viewBox="0 0 107 59" fill="none" xmlns="http://www.w3.org/2000/svg">\n<path d="M43.4502 29.0975C45.578 29.0193 42.6297 29.0008 40.2223 29.0008C38.5002 29.0008 37.0666 29.025 37.0395 29.0653C37.0215 29.0975 37.3731 29.5807 37.824 30.1446C39.0592 31.6668 40.8985 33.914 43.0805 36.572C44.1444 37.8768 45.2715 39.2541 45.578 39.6326C45.8846 40.0031 46.6149 40.8891 47.201 41.606C48.2469 42.8786 48.4993 43.1927 50.1313 45.1902C50.9698 46.2292 52.5928 48.6133 52.5207 48.4039M61.716 29.4599C62.3382 28.0746 61.8706 29.1216 61.8706 29.0814C61.8706 28.9928 44.5412 28.9686 44.442 29.0492C44.4149 29.0814 44.442 29.1941 44.5051 29.315C44.6223 29.5083 45.0912 30.5392 46.678 34.0348C47.0387 34.8322 47.6969 36.282 48.1477 37.2566C48.5895 38.2312 49.392 39.987 49.9239 41.163C51.592 44.8438 52.7551 47.389 52.9895 47.8884C53.1067 48.122 53.1608 48.1703 53.2149 48.0898C53.287 47.9609 60.3906 32.3595 61.716 29.4599ZM61.716 29.4599C61.5988 29.7016 61.9865 28.8639 61.716 29.4599ZM52.9895 49.1127C53.4223 48.5892 56.8125 44.4733 57.1911 44.0304C57.5608 43.5793 58.2821 42.7094 58.778 42.0892C59.5715 41.0905 63.151 36.6847 64.5936 34.9208C65.6575 33.6241 66.6493 32.3917 67.6862 31.095C68.2633 30.362 68.8674 29.6291 69.0116 29.4599C69.1559 29.2988 69.246 29.1216 69.219 29.0814C69.1288 28.9525 62.9977 28.9767 62.8895 29.0975M62.8895 29.0975C62.9436 29.0411 62.8354 29.1539 62.8895 29.0975C62.4567 28.6464 62.7813 29.2183 62.8895 29.0975ZM62.8895 29.0975C63.4395 27.8974 62.7813 29.2183 62.8895 29.0975ZM29.7272 0.649311C23.0731 1.06008 17.2576 3.10591 12.1904 6.80288C11.1264 7.5761 8.77317 9.70247 7.8535 10.7173C2.14613 16.9997 -0.423543 25.4328 0.973997 33.3099C1.92973 38.7144 4.21989 43.3538 8.02481 47.5662C8.89038 48.5247 11.0092 50.4336 12.1273 51.2552C16.392 54.4125 21.2609 56.41 26.6617 57.2235C31.269 57.9242 35.9936 57.6423 40.592 56.418C44.6674 55.3226 49.1034 53.0271 52.4395 50.2886C52.7821 50.0067 53.0797 49.7812 53.1157 49.7812C53.1518 49.7812 53.5936 50.1114 54.1166 50.5142C59.0756 54.3883 64.7108 56.6758 71.2477 57.449C72.3928 57.5859 77.0542 57.5859 78.1903 57.449C83.1132 56.861 87.2698 55.4918 91.3091 53.1238C92.8509 52.2217 93.8968 51.4968 95.1501 50.4578C100.614 45.9393 104.067 40.0998 105.23 33.4308C105.519 31.7796 105.591 30.8856 105.6 29.0411C105.6 27.1564 105.51 26.0368 105.23 24.5065C103.716 16.0977 98.414 8.91312 90.5337 4.57181C85.8632 2.00246 80.4714 0.641257 74.8993 0.625148C67.046 0.600985 59.7157 3.27506 54.0985 8.20434L53.1338 9.05812L51.9887 8.06742C48.7608 5.2806 45.1002 3.27504 40.8174 1.95412C37.5264 0.947327 33.1985 0.431842 29.7272 0.649311ZM35.1371 1.65611C38.3018 2.05078 41.2502 2.84817 44.0633 4.08049C46.7953 5.27254 49.0403 6.69012 51.628 8.88092L52.5207 9.62998L51.042 11.2892C50.2305 12.2074 48.5534 14.0841 47.3092 15.4775C43.6485 19.5852 42.1248 21.2847 40.9256 22.5976C40.6371 22.9036 39.4469 24.2326 38.2748 25.5374C37.1026 26.8422 36.0026 28.0504 35.8403 28.2195C35.6781 28.3806 35.5428 28.5659 35.5428 28.6223C35.5428 28.7109 36.1108 29.4277 37.5625 31.1755C38.4821 32.287 39.2215 33.1891 42.0526 36.6525C42.7198 37.4741 44.1264 39.1897 45.1723 40.4784C46.2272 41.759 47.4174 43.2249 47.8231 43.7323C49.5813 45.899 51.2493 47.8481 51.8084 48.4039C52.133 48.7261 52.4034 49.0402 52.4034 49.0885C52.4034 49.1932 50.8616 50.4417 49.8789 51.1263C46.2723 53.6554 41.9625 55.4354 37.4272 56.2569C35.5879 56.5952 34.001 56.7241 31.7108 56.7241C29.4567 56.7241 28.4108 56.6516 26.4813 56.3375C21.8559 55.5965 17.474 53.8809 13.7773 51.3679C10.8469 49.3785 8.133 46.6722 6.19448 43.8209C3.18301 39.3991 1.55105 34.1637 1.55105 28.9203C1.55105 25.8999 2.02891 23.3064 3.13793 20.2215C6.05022 12.1349 12.8666 5.7719 21.6215 2.98509C24.0289 2.21992 25.8592 1.86553 29.3215 1.50308C30.1059 1.42253 34.1092 1.52724 35.1371 1.65611ZM77.6583 1.57557C84.9977 2.26825 91.4444 5.17591 96.5116 10.073C99.1263 12.594 101.281 15.7352 102.616 18.965C104.635 23.846 105.167 28.4048 104.284 33.4146C103.761 36.3867 102.877 38.8997 101.353 41.6865C99.9017 44.3525 97.8911 46.8575 95.4657 49.016C92.2559 51.8673 88.5591 53.9695 84.4927 55.2421C80.7509 56.418 77.1805 56.8852 73.2944 56.708C71.428 56.6194 70.7157 56.5469 69.0387 56.2569C63.6649 55.3226 58.6969 53.0835 54.5043 49.7087C54.1436 49.4188 53.8461 49.153 53.8461 49.1127C53.8461 49.0805 54.1977 48.6939 54.6215 48.267C55.4059 47.4696 55.9649 46.8252 58.0928 44.2478C59.3911 42.6772 59.4452 42.6128 61.4649 40.1159C63.5297 37.5707 64.278 36.6445 65.4772 35.1625C67.3256 32.8992 67.9837 32.0776 68.9395 30.8936C69.4354 30.2734 70.0395 29.5405 70.2739 29.2586C70.5083 28.9767 70.7067 28.7028 70.7067 28.6464C70.7067 28.5901 70.4903 28.3162 70.2288 28.0262C69.9674 27.7443 68.8493 26.512 67.7583 25.2958C66.6583 24.0796 65.1346 22.3882 64.3772 21.5505C63.0969 20.141 60.2116 16.9031 55.6764 11.7805C54.6666 10.6529 53.8461 9.6783 53.8461 9.62998C53.8461 9.51722 55.6584 7.99493 56.6862 7.23782C61.0772 4.04023 66.2165 2.13132 71.969 1.58362C73.4928 1.43864 76.1616 1.43059 77.6583 1.57557ZM53.8911 11.0556C54.2608 11.4664 55.3879 12.7309 56.3887 13.8585C57.3895 14.9862 58.4985 16.2346 58.8502 16.6373C59.2018 17.032 59.6526 17.5475 59.851 17.773C60.1846 18.1596 62.3665 20.584 63.5747 21.9129C63.8723 22.2432 64.1247 22.5412 64.1247 22.5734C64.1247 22.6137 59.1747 22.6378 53.1248 22.6378C47.0748 22.6378 42.1248 22.6137 42.1248 22.5815C42.1248 22.5573 42.3592 22.2754 42.6477 21.9613C43.6846 20.8256 51.6551 11.9094 52.7551 10.6529C52.9174 10.4676 53.0887 10.3146 53.1338 10.3146C53.1789 10.3146 53.5215 10.6529 53.8911 11.0556ZM46.9666 23.556C47.0116 23.5883 46.1551 24.732 44.3157 27.108L43.5043 28.1551L40.2854 28.1793L37.0666 28.1954L37.2018 28.0262C37.274 27.9296 38.1936 26.8825 39.2576 25.6985L41.178 23.5399L42.1248 23.4997C43.2338 23.4594 46.9125 23.4997 46.9666 23.556ZM58.6698 24.1682C58.9764 24.5467 59.5264 25.2475 59.8961 25.7388C60.2747 26.2221 60.8518 26.9792 61.1854 27.4061L61.7895 28.1954H53.1698H44.5502L45.7674 26.6006C46.4346 25.7307 47.2371 24.6837 47.5526 24.2729C47.8953 23.8299 48.1928 23.5158 48.301 23.4997C48.4002 23.4836 50.6452 23.4755 53.2961 23.4755L58.1108 23.4836L58.6698 24.1682ZM64.9993 23.548C65.0534 23.5802 65.6485 24.2165 66.3157 24.9575C66.9829 25.6985 67.9026 26.7134 68.3534 27.2047C68.8042 27.7041 69.1739 28.131 69.1739 28.1551C69.1739 28.1793 67.7493 28.1873 66.0092 28.1793L62.8354 28.1551L62.4567 27.6719C60.8067 25.5616 59.3461 23.6205 59.3461 23.5319C59.3461 23.4352 64.819 23.4513 64.9993 23.548Z" stroke="black" stroke-width="1.2" stroke-linejoin="round"/>\n<path d="M43.4502 29.0975C45.578 29.0193 42.6297 29.0008 40.2223 29.0008C38.5002 29.0008 37.0666 29.025 37.0395 29.0653C37.0215 29.0975 37.3731 29.5807 37.824 30.1446C39.0592 31.6668 40.8985 33.914 43.0805 36.572C44.1444 37.8768 45.2715 39.2541 45.578 39.6326C45.8846 40.0031 46.6149 40.8891 47.201 41.606C48.2469 42.8786 48.4993 43.1927 50.1313 45.1902C50.9698 46.2292 52.5928 48.6133 52.5207 48.4039M61.716 29.4599C62.3382 28.0746 61.8706 29.1216 61.8706 29.0814C61.8706 28.9928 44.5412 28.9686 44.442 29.0492C44.4149 29.0814 44.442 29.1941 44.5051 29.315C44.6223 29.5083 45.0912 30.5392 46.678 34.0348C47.0387 34.8322 47.6969 36.282 48.1477 37.2566C48.5895 38.2312 49.392 39.987 49.9239 41.163C51.592 44.8438 52.7551 47.389 52.9895 47.8884C53.1067 48.122 53.1608 48.1703 53.2149 48.0898C53.287 47.9609 60.3906 32.3595 61.716 29.4599ZM61.716 29.4599C61.5988 29.7016 61.9865 28.8639 61.716 29.4599ZM52.9895 49.1127C53.4223 48.5892 56.8125 44.4733 57.1911 44.0304C57.5608 43.5793 58.2821 42.7094 58.778 42.0892C59.5715 41.0905 63.151 36.6847 64.5936 34.9208C65.6575 33.6241 66.6493 32.3917 67.6862 31.095C68.2633 30.362 68.8674 29.6291 69.0116 29.4599C69.1559 29.2988 69.246 29.1216 69.219 29.0814C69.1288 28.9525 62.9977 28.9767 62.8895 29.0975M62.8895 29.0975C62.9436 29.0411 62.8354 29.1539 62.8895 29.0975C62.4567 28.6464 62.7813 29.2183 62.8895 29.0975ZM62.8895 29.0975C63.4395 27.8974 62.7813 29.2183 62.8895 29.0975ZM29.7272 0.649311C23.0731 1.06008 17.2576 3.10591 12.1904 6.80288C11.1264 7.5761 8.77317 9.70247 7.8535 10.7173C2.14613 16.9997 -0.423543 25.4328 0.973997 33.3099C1.92973 38.7144 4.21989 43.3538 8.02481 47.5662C8.89038 48.5247 11.0092 50.4336 12.1273 51.2552C16.392 54.4125 21.2609 56.41 26.6617 57.2235C31.269 57.9242 35.9936 57.6423 40.592 56.418C44.6674 55.3226 49.1034 53.0271 52.4395 50.2886C52.7821 50.0067 53.0797 49.7812 53.1157 49.7812C53.1518 49.7812 53.5936 50.1114 54.1166 50.5142C59.0756 54.3883 64.7108 56.6758 71.2477 57.449C72.3928 57.5859 77.0542 57.5859 78.1903 57.449C83.1132 56.861 87.2698 55.4918 91.3091 53.1238C92.8509 52.2217 93.8968 51.4968 95.1501 50.4578C100.614 45.9393 104.067 40.0998 105.23 33.4308C105.519 31.7796 105.591 30.8856 105.6 29.0411C105.6 27.1564 105.51 26.0368 105.23 24.5065C103.716 16.0977 98.414 8.91312 90.5337 4.57181C85.8632 2.00246 80.4714 0.641257 74.8993 0.625148C67.046 0.600985 59.7157 3.27506 54.0985 8.20434L53.1338 9.05812L51.9887 8.06742C48.7608 5.2806 45.1002 3.27504 40.8174 1.95412C37.5264 0.947327 33.1985 0.431842 29.7272 0.649311ZM35.1371 1.65611C38.3018 2.05078 41.2502 2.84817 44.0633 4.08049C46.7953 5.27254 49.0403 6.69012 51.628 8.88092L52.5207 9.62998L51.042 11.2892C50.2305 12.2074 48.5534 14.0841 47.3092 15.4775C43.6485 19.5852 42.1248 21.2847 40.9256 22.5976C40.6371 22.9036 39.4469 24.2326 38.2748 25.5374C37.1026 26.8422 36.0026 28.0504 35.8403 28.2195C35.6781 28.3806 35.5428 28.5659 35.5428 28.6223C35.5428 28.7109 36.1108 29.4277 37.5625 31.1755C38.4821 32.287 39.2215 33.1891 42.0526 36.6525C42.7198 37.4741 44.1264 39.1897 45.1723 40.4784C46.2272 41.759 47.4174 43.2249 47.8231 43.7323C49.5813 45.899 51.2493 47.8481 51.8084 48.4039C52.133 48.7261 52.4034 49.0402 52.4034 49.0885C52.4034 49.1932 50.8616 50.4417 49.8789 51.1263C46.2723 53.6554 41.9625 55.4354 37.4272 56.2569C35.5879 56.5952 34.001 56.7241 31.7108 56.7241C29.4567 56.7241 28.4108 56.6516 26.4813 56.3375C21.8559 55.5965 17.474 53.8809 13.7773 51.3679C10.8469 49.3785 8.133 46.6722 6.19448 43.8209C3.18301 39.3991 1.55105 34.1637 1.55105 28.9203C1.55105 25.8999 2.02891 23.3064 3.13793 20.2215C6.05022 12.1349 12.8666 5.7719 21.6215 2.98509C24.0289 2.21992 25.8592 1.86553 29.3215 1.50308C30.1059 1.42253 34.1092 1.52724 35.1371 1.65611ZM77.6583 1.57557C84.9977 2.26825 91.4444 5.17591 96.5116 10.073C99.1263 12.594 101.281 15.7352 102.616 18.965C104.635 23.846 105.167 28.4048 104.284 33.4146C103.761 36.3867 102.877 38.8997 101.353 41.6865C99.9017 44.3525 97.8911 46.8575 95.4657 49.016C92.2559 51.8673 88.5591 53.9695 84.4927 55.2421C80.7509 56.418 77.1805 56.8852 73.2944 56.708C71.428 56.6194 70.7157 56.5469 69.0387 56.2569C63.6649 55.3226 58.6969 53.0835 54.5043 49.7087C54.1436 49.4188 53.8461 49.153 53.8461 49.1127C53.8461 49.0805 54.1977 48.6939 54.6215 48.267C55.4059 47.4696 55.9649 46.8252 58.0928 44.2478C59.3911 42.6772 59.4452 42.6128 61.4649 40.1159C63.5297 37.5707 64.278 36.6445 65.4772 35.1625C67.3256 32.8992 67.9837 32.0776 68.9395 30.8936C69.4354 30.2734 70.0395 29.5405 70.2739 29.2586C70.5083 28.9767 70.7067 28.7028 70.7067 28.6464C70.7067 28.5901 70.4903 28.3162 70.2288 28.0262C69.9674 27.7443 68.8493 26.512 67.7583 25.2958C66.6583 24.0796 65.1346 22.3882 64.3772 21.5505C63.0969 20.141 60.2116 16.9031 55.6764 11.7805C54.6666 10.6529 53.8461 9.6783 53.8461 9.62998C53.8461 9.51722 55.6584 7.99493 56.6862 7.23782C61.0772 4.04023 66.2165 2.13132 71.969 1.58362C73.4928 1.43864 76.1616 1.43059 77.6583 1.57557ZM53.8911 11.0556C54.2608 11.4664 55.3879 12.7309 56.3887 13.8585C57.3895 14.9862 58.4985 16.2346 58.8502 16.6373C59.2018 17.032 59.6526 17.5475 59.851 17.773C60.1846 18.1596 62.3665 20.584 63.5747 21.9129C63.8723 22.2432 64.1247 22.5412 64.1247 22.5734C64.1247 22.6137 59.1747 22.6378 53.1248 22.6378C47.0748 22.6378 42.1248 22.6137 42.1248 22.5815C42.1248 22.5573 42.3592 22.2754 42.6477 21.9613C43.6846 20.8256 51.6551 11.9094 52.7551 10.6529C52.9174 10.4676 53.0887 10.3146 53.1338 10.3146C53.1789 10.3146 53.5215 10.6529 53.8911 11.0556ZM46.9666 23.556C47.0116 23.5883 46.1551 24.732 44.3157 27.108L43.5043 28.1551L40.2854 28.1793L37.0666 28.1954L37.2018 28.0262C37.274 27.9296 38.1936 26.8825 39.2576 25.6985L41.178 23.5399L42.1248 23.4997C43.2338 23.4594 46.9125 23.4997 46.9666 23.556ZM58.6698 24.1682C58.9764 24.5467 59.5264 25.2475 59.8961 25.7388C60.2747 26.2221 60.8518 26.9792 61.1854 27.4061L61.7895 28.1954H53.1698H44.5502L45.7674 26.6006C46.4346 25.7307 47.2371 24.6837 47.5526 24.2729C47.8953 23.8299 48.1928 23.5158 48.301 23.4997C48.4002 23.4836 50.6452 23.4755 53.2961 23.4755L58.1108 23.4836L58.6698 24.1682ZM64.9993 23.548C65.0534 23.5802 65.6485 24.2165 66.3157 24.9575C66.9829 25.6985 67.9026 26.7134 68.3534 27.2047C68.8042 27.7041 69.1739 28.131 69.1739 28.1551C69.1739 28.1793 67.7493 28.1873 66.0092 28.1793L62.8354 28.1551L62.4567 27.6719C60.8067 25.5616 59.3461 23.6205 59.3461 23.5319C59.3461 23.4352 64.819 23.4513 64.9993 23.548Z" stroke="black" stroke-width="1.2" stroke-linejoin="round"/>\n</svg>'

CATALOG_TEMPLATE = r"""
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<style>
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: #fff; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: #111; overflow: hidden; }
.app { width: 100%; max-width: 430px; height: 100dvh; min-height: 100svh; margin: 0 auto; position: relative; overflow: hidden; background: #fff; }
.content { position: absolute; inset: 0 0 calc(126px + env(safe-area-inset-bottom)) 0; overflow-y: auto; -webkit-overflow-scrolling: touch; padding-bottom: 20px; }
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600&display=swap');
.catalog-header {
  display:flex;
  align-items:center;
  gap:.78rem;
  padding:1rem 1rem .88rem;
  border-bottom:1px solid rgba(17,17,17,.10);
  background:linear-gradient(180deg,#fff 0%,#fbfbfb 100%);
  box-shadow:0 2px 10px rgba(0,0,0,.08);
}
.logo-svg {
  width:78px;
  min-width:78px;
  height:43px;
  display:flex;
  align-items:center;
  justify-content:center;
  overflow:hidden;
  position:relative;
  filter:drop-shadow(0 2px 4px rgba(0,0,0,.12));
}
.logo-svg svg {
  width:76px;
  height:auto;
  display:block;
  transition:transform .28s ease, filter .28s ease;
}
.logo-svg:hover svg {
  transform:scale(1.055);
  filter:contrast(1.08);
}
.logo-svg::after {
  content:"";
  position:absolute;
  inset:0;
  background:linear-gradient(115deg,transparent 38%,rgba(255,255,255,.22) 50%,transparent 62%);
  transform:translateX(-120%);
  transition:transform .75s ease;
  pointer-events:none;
}
.logo-svg:hover::after {
  transform:translateX(120%);
}
.logo-title {
  font-family:'Cinzel','Times New Roman',serif;
  font-size:1.08rem;
  font-weight:500;
  letter-spacing:.055em;
  line-height:1.05;
  color:#111;
  white-space:nowrap;
  text-rendering:geometricPrecision;
}
.logo-sub {
  margin-top:.28rem;
  color:#8b8b8b;
  font-size:.58rem;
  letter-spacing:.095em;
  text-transform:uppercase;
}
.catalog-top { display:grid; grid-template-columns:2fr 1fr; gap:.65rem; padding:1.35rem 1rem .8rem; }
.catalog-select, .catalog-pick { border:1px solid #aaa; border-radius:14px; min-height:70px; display:flex; align-items:center; justify-content:center; background:#fff; }
.catalog-select { justify-content:space-between; padding:0 1rem; }
.select-title { font-weight:700; font-size:1.05rem; color:#111; }
.select-sub { color:#777; font-size:.92rem; margin-top:.25rem; }
.catalog-pick { color:#555; font-size:.98rem; line-height:1.35; text-align:center; }
.catalog-cols, .stone-main { display:grid; grid-template-columns:.92fr .78fr .62fr .95fr 1.12fr 1.25fr; gap:.18rem; }
.catalog-cols { color:#aaa; font-size:.57rem; line-height:1.05; padding:.45rem 1.85rem .6rem; text-transform:uppercase; }
.stone-card { margin:0 1rem 1rem; border:1px solid #d0d0d0; border-radius:18px; padding:1.05rem 1rem .75rem; background:#fff; }
.stone-card.is-hidden { display:none; }
.stone-main { align-items:start; font-size:.98rem; color:#111; }
.price { font-weight:700; text-align:right; font-size:.98rem; line-height:1.25; white-space:nowrap; }
.stone-line { border-top:1px solid #e6e6e6; margin:1.05rem 0 .7rem; }
.stone-meta { display:flex; justify-content:space-between; align-items:center; color:#666; font-size:.86rem; gap:.5rem; }
.tags { display:flex; gap:.35rem; flex-wrap:wrap; justify-content:flex-end; }
.tag { border:1px solid #f0c56d; color:#c77c16; border-radius:7px; padding:.08rem .45rem; font-size:.7rem; }
.tag-blue { border-color:#8bd7e8; color:#1892ad; }
.tag-gray { border-color:#ccc; color:#555; }
.actions { display:grid; grid-template-columns:repeat(6,1fr); color:#888; font-size:1.25rem; padding-top:.85rem; text-align:center; }
.empty-state { display:none; margin:0 1rem 1rem; border:1px solid #d0d0d0; border-radius:18px; padding:1rem; color:#666; font-size:.9rem; text-align:center; }
.empty-state.is-visible { display:block; }
.bottom-controls { position:fixed; left:50%; transform:translateX(-50%); width:100%; max-width:430px; bottom:calc(64px + env(safe-area-inset-bottom)); z-index:30; background:#fff; border-top:1px solid #ddd; padding:.5rem .8rem; display:grid; grid-template-columns:1fr 1fr; gap:.65rem; }
.control-box { border:1px solid #c9c9c9; border-radius:14px; min-height:64px; background:#fff; text-align:left; padding:.55rem .8rem; color:#111; }
.control-label { color:#aaa; font-size:.72rem; letter-spacing:.04em; }
.control-value { font-weight:700; font-size:.92rem; margin-top:.12rem; }
.bottom-nav { position:fixed; left:50%; transform:translateX(-50%); width:100%; max-width:430px; bottom:0; z-index:31; background:#fff; border-top:1px solid rgba(49,51,63,.18); padding:.25rem .25rem calc(.45rem + env(safe-area-inset-bottom)); }
.nav-grid { display:grid; grid-template-columns:repeat(6,1fr); gap:.2rem; }
.nav-tab { display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:52px; border-radius:12px; color:#888; text-decoration:none; font-size:.68rem; line-height:1.1; white-space:nowrap; }
.nav-active { background:#f2f5f8; color:#111; border:1px solid #cfd5dc; }
.nav-icon { font-size:1.15rem; line-height:1; margin-bottom:.15rem; }
.overlay { display:none; position:fixed; left:0; right:0; top:0; bottom:0; z-index:50; background:rgba(0,0,0,.22); }
.sheet { position:fixed; left:50%; bottom:0; transform:translate(-50%,110%); width:100%; max-width:430px; z-index:60; max-height:calc(100dvh - 70px); overflow-y:auto; -webkit-overflow-scrolling:touch; background:#fff; border:1px solid #999; border-bottom:0; border-radius:26px 26px 0 0; padding:1.4rem 1.35rem 1.2rem; box-shadow:0 -6px 22px rgba(0,0,0,.18); transition:transform .22s ease; touch-action:pan-y; }
.sheet-open .overlay { display:block; }
.sheet-open .sheet { transform:translate(-50%,0); }
.sheet-handle { width:42px; height:4px; border-radius:4px; background:#c9c9c9; margin:0 auto 1rem; }
.sheet-head { display:flex; justify-content:space-between; align-items:center; margin-bottom:.7rem; }
.sheet-title { font-weight:700; font-size:1.15rem; color:#111; }
.reset { border:0; background:transparent; padding:0; font-size:.78rem; color:#222; }
.filter-group { margin:.85rem 0 1.05rem; }
.filter-name { font-size:.76rem; font-weight:600; color:#111; margin-bottom:.55rem; }
.chips { display:flex; gap:.55rem; flex-wrap:wrap; }
.chip { border:1px solid #aaa; border-radius:18px; padding:.45rem .82rem; font-size:.67rem; color:#111; background:#fff; min-height:34px; -webkit-tap-highlight-color:transparent; }
.chip-on { background:#000; color:#fff; border-color:#000; }
.chip-note { font-size:.58rem; color:#222; align-self:center; }
</style>
</head>
<body>
<div class="app" id="app">
  <div class="content" id="content">
    <div class="catalog-header"><div class="logo-svg">__LOGO__</div><div><div class="logo-title">KURGIN Diamonds</div><div class="logo-sub">лабораторные бриллианты</div></div></div>
    <div class="catalog-top"><div class="catalog-select"><div><div class="select-title">Основной каталог</div><div class="select-sub">1.00–2.99 ct</div></div><div>⌄</div></div><div class="catalog-pick">Индив.<br>подбор</div></div>
    <div class="catalog-cols"><div>ФОРМА</div><div>КАРАТ</div><div>ЦВЕТ</div><div>ЧИСТОТА</div><div>KARO SCORE</div><div>ЦЕНА</div></div>
    __CARDS__
    <div class="empty-state" id="emptyState">По выбранным фильтрам камни не найдены</div>
  </div>
  <div class="bottom-controls"><button class="control-box"><div class="control-label">СОРТИРОВКА</div><div class="control-value">по Karo Score ↓</div></button><button class="control-box" id="openFilters"><div class="control-label">ФИЛЬТРЫ</div><div class="control-value">☷ Параметры</div></button></div>
  <nav class="bottom-nav"><div class="nav-grid"><a class="nav-tab" href="?page=kurgin" target="_parent"><span class="nav-icon">♢</span><span>KURGIN</span></a><a class="nav-tab" href="?page=tools" target="_parent"><span class="nav-icon">♢</span><span>Инстр.</span></a><a class="nav-tab nav-active" href="?page=catalog" target="_parent"><span class="nav-icon">◇</span><span>Каталог</span></a><a class="nav-tab" href="?page=favorites" target="_parent"><span class="nav-icon">♡</span><span>Избр.</span></a><a class="nav-tab" href="?page=cart" target="_parent"><span class="nav-icon">◠</span><span>Корзина</span></a><a class="nav-tab" href="?page=profile" target="_parent"><span class="nav-icon">○</span><span>Профиль</span></a></div></nav>
  <div class="overlay" id="overlay"></div>
  <div class="sheet" id="sheet">
    <div class="sheet-handle" id="handle"></div>
    <div class="sheet-head"><div class="sheet-title">Фильтры</div><button class="reset" id="resetFilters">Сбросить</button></div>
    <div class="filter-group"><div class="filter-name">1. Форма / огранка</div><div class="chips"><button class="chip chip-on" data-group="shape" data-value="Round">Round</button><button class="chip" data-group="shape" data-value="Oval">Oval</button><button class="chip" data-group="shape" data-value="Pear">Pear</button><button class="chip" data-group="shape" data-value="Cushion">Cushion</button></div></div>
    <div class="filter-group"><div class="filter-name">2. Вес</div><div class="chips"><button class="chip" data-group="weight" data-value="1–1.49">1–1.49</button><button class="chip" data-group="weight" data-value="1.5–1.99">1.5–1.99</button><button class="chip" data-group="weight" data-value="2–2.49">2–2.49</button><button class="chip" data-group="weight" data-value="2.5–2.99">2.5–2.99</button></div></div>
    <div class="filter-group"><div class="filter-name">3. Цвет</div><div class="chips"><button class="chip" data-group="color" data-value="D">D</button><button class="chip" data-group="color" data-value="E">E</button><button class="chip" data-group="color" data-value="F">F</button><button class="chip" data-group="color" data-value="G">G</button><button class="chip" data-group="color" data-value="H">H</button></div></div>
    <div class="filter-group"><div class="filter-name">4. Чистота</div><div class="chips"><button class="chip" data-group="clarity" data-value="IF">IF</button><button class="chip" data-group="clarity" data-value="VVS1">VVS1</button><button class="chip" data-group="clarity" data-value="VVS2">VVS2</button><button class="chip" data-group="clarity" data-value="VS1">VS1</button><button class="chip" data-group="clarity" data-value="VS2">VS2</button></div></div>
    <div class="filter-group"><div class="filter-name">5. Karo Score</div><div class="chips"><button class="chip" data-group="score" data-value="0–49">0–49</button><button class="chip" data-group="score" data-value="50–79">50–79</button><button class="chip" data-group="score" data-value="80–89">80–89</button><button class="chip" data-group="score" data-value="90–94.9">90–94.9</button><button class="chip" data-group="score" data-value="95–98">95–98</button><button class="chip" data-group="score" data-value="99+">99+</button><span class="chip-note">качество / индекс-коэф.</span></div></div>
    <div class="filter-group"><div class="filter-name">6. Флюоресценция</div><div class="chips"><button class="chip" data-group="fluorescence" data-value="None">None</button><button class="chip" data-group="fluorescence" data-value="Faint">Faint</button><button class="chip" data-group="fluorescence" data-value="Medium">Medium</button><button class="chip" data-group="fluorescence" data-value="Strong">Strong</button></div></div>
    <div class="filter-group"><div class="filter-name">7. Качество отделки</div><div class="chips"><button class="chip" data-group="finish" data-value="Ex/Ex/Ex+">Ex/Ex/Ex+</button><button class="chip" data-group="finish" data-value="2Ex/1VG+">2Ex/1VG+</button></div></div>
  </div>
</div>
<script>
const app = document.getElementById('app');
const sheet = document.getElementById('sheet');
const overlay = document.getElementById('overlay');
const openFilters = document.getElementById('openFilters');
const resetFilters = document.getElementById('resetFilters');
const handle = document.getElementById('handle');
const emptyState = document.getElementById('emptyState');
const cards = Array.from(document.querySelectorAll('.stone-card'));
const chips = Array.from(document.querySelectorAll('.chip'));
const filterGroups = ['shape', 'weight', 'color', 'clarity', 'score', 'fluorescence', 'finish'];

function activeFilters() {
  const filters = {};
  filterGroups.forEach(group => filters[group] = []);
  chips.forEach(chip => {
    if (chip.classList.contains('chip-on')) filters[chip.dataset.group].push(chip.dataset.value);
  });
  return filters;
}
function applyFilters() {
  const filters = activeFilters();
  let visibleCount = 0;
  cards.forEach(card => {
    let visible = true;
    filterGroups.forEach(group => {
      const values = filters[group];
      if (values.length > 0 && !values.includes(card.dataset[group])) visible = false;
    });
    card.classList.toggle('is-hidden', !visible);
    if (visible) visibleCount += 1;
  });
  emptyState.classList.toggle('is-visible', visibleCount === 0);
}
function openSheet(){
  app.classList.add('sheet-open');
  sheet.style.transition='transform .22s ease';
  sheet.style.transform='translate(-50%, 0)';
}
function closeSheet(){
  sheet.style.transition='transform .22s ease';
  sheet.style.transform='translate(-50%, 110%)';
  setTimeout(() => app.classList.remove('sheet-open'), 180);
}
openFilters.addEventListener('click', openSheet);
overlay.addEventListener('click', closeSheet);
handle.addEventListener('click', closeSheet);
chips.forEach(chip => chip.addEventListener('click', () => { chip.classList.toggle('chip-on'); applyFilters(); }));
resetFilters.addEventListener('click', () => { chips.forEach(chip => chip.classList.remove('chip-on')); applyFilters(); });
let startY = 0, startX = 0, dragging = false;
sheet.addEventListener('touchstart', e => { if(!e.touches.length) return; startY=e.touches[0].clientY; startX=e.touches[0].clientX; dragging=true; sheet.style.transition='none'; }, {passive:true});
sheet.addEventListener('touchmove', e => { if(!dragging || !e.touches.length) return; const dy=e.touches[0].clientY-startY; if(dy>0 && sheet.scrollTop <= 0){ e.preventDefault(); sheet.style.transform=`translate(-50%, ${Math.min(dy,260)}px)`; } }, {passive:false});
sheet.addEventListener('touchend', e => { if(!dragging) return; dragging=false; const touch=e.changedTouches[0]; const dy=touch.clientY-startY; const dx=Math.abs(touch.clientX-startX); if(dy>70 && dx<100 && sheet.scrollTop <= 5) closeSheet(); else { sheet.style.transition='transform .18s ease'; sheet.style.transform='translate(-50%, 0)'; } }, {passive:true});
applyFilters();
</script>
</body>
</html>
"""

CATALOG_HTML = CATALOG_TEMPLATE.replace("__CARDS__", cards_html).replace("__LOGO__", LOGO_SVG)

if current_page == "catalog":
    components.html(CATALOG_HTML, height=900, scrolling=False)
else:
    st.markdown(f'<div class="page-pad"><h3>{PAGES[current_page]}</h3></div>', unsafe_allow_html=True)
    nav_items = []
    for page_key, icon, label in TABS:
        active_class = " kurgin-tab-active" if page_key == current_page else ""
        nav_items.append(f'<a class="kurgin-tab{active_class}" href="?page={page_key}" target="_self"><span class="kurgin-icon">{icon}</span><span>{label}</span></a>')
    st.markdown('<nav class="kurgin-bottom-nav"><div class="kurgin-nav-grid">' + ''.join(nav_items) + '</div></nav>', unsafe_allow_html=True)
