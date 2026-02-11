import streamlit as st
import pandas as pd
import time
import random
import datetime
import altair as alt
import folium
from streamlit_folium import st_folium
import qrcode
from PIL import Image
import io

# ================= КОНФИГУРАЦИЯ =================
st.set_page_config(
    page_title="Degeres Ecosystem", 
    layout="wide", 
    page_icon="🧬",
    initial_sidebar_state="collapsed" # <--- Скрываем меню слева по умолчанию
)

# 🔴 ССЫЛКА НА ВИДЕО (ДЛЯ ВСЕХ ТОВАРОВ)
GLOBAL_VIDEO_LINK = "https://youtu.be/bIEP0JWpNd0?si=hLIP6gEdg5TiEHSt"

# ================= CSS (GLOBAL STYLES - ВЫСОКИЙ КОНТРАСТ) =================
st.markdown("""
<style>
    /* 1. Убираем верхний хедер (черную полосу) и отступы */
    [data-testid="stHeader"] {
        display: none;
    }
    
    /* Основной фон приложения */
    .stApp {
        background-color: #f0f2f6;
        font-family: 'Inter', 'Helvetica Neue', sans-serif;
    }

    /* Глобальный цвет текста - ТЕМНЫЙ */
    h1, h2, h3, h4, h5, h6, p, div, span, label {
        color: #1a1a1a !important;
    }

    /* Карточки (контейнеры) */
    div.css-1r6slb0, div.stContainer, div[data-testid="column"] > div {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border: 1px solid #dee2e6;
    }

    /* Исправление видимости Метрик */
    div[data-testid="stMetricLabel"] label {
        color: #444444 !important;
        font-weight: 600;
        font-size: 1rem;
    }
    div[data-testid="stMetricValue"] div {
        color: #000000 !important;
        font-weight: 700;
    }

    /* Кнопки */
    .stButton>button {
        border-radius: 8px;
        font-weight: 700;
        border: none;
        width: 100%;
        padding: 12px 20px;
        background-color: #28a745; 
        color: white !important;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #218838;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        color: white !important;
    }

    /* Вкладки */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #ffffff;
        padding: 10px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: nowrap;
        background-color: #f8f9fa;
        border-radius: 5px;
        border: 1px solid #ddd;
        color: #333 !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #e8f5e9;
        border-color: #28a745;
        font-weight: bold;
    }

    /* Отступы контента (поднимаем выше, так как хедера нет) */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 5rem;
    }
</style>
""", unsafe_allow_html=True)

# ================= STATE MANAGEMENT (БАЗА ДАННЫХ) =================
if 'db_products' not in st.session_state:
    st.session_state['db_products'] = [
        {
            "id": "BATCH-880", "farmer": "Хозяйство 'Адал'", "product": "Шубат", "amount": 50, "unit": "Литров",
            "price": 60000, "status": "Verified", "score": 95, "history": ["Создано фермером", "Водитель принял груз", "Доставлено в Хаб (3.2°C)", "Сертифицировано (Score: 95)"], "temp": 3.2, "ph": 5.8, "video_uploaded": True, "video_link": GLOBAL_VIDEO_LINK, "image_icon": "🥛"
        },
        {
            "id": "BATCH-881", "farmer": "Ферма 'Родина'", "product": "Конина", "amount": 20, "unit": "Кг",
            "price": 50000, "status": "Ready", "score": 0, "history": ["Создано фермером"], "temp": 0, "ph": 0, "video_uploaded": True, "video_link": GLOBAL_VIDEO_LINK, "image_icon": "🥩"
        },
        {
            "id": "BATCH-882", "farmer": "Хозяйство 'Адал'", "product": "Говядина", "amount": 30, "unit": "Кг",
            "price": 75000, "status": "Rejected", "score": 50, "history": ["Создано фермером", "Водитель принял груз", "Доставлено в Хаб (7.5°C)", "Отбраковано лабораторией"], "temp": 7.5, "ph": 6.2, "video_uploaded": True, "video_link": GLOBAL_VIDEO_LINK, "image_icon": "🍖"
        },
        {
            "id": "BATCH-883", "farmer": "Ферма 'Родина'", "product": "Кумыс", "amount": 15, "unit": "Литров",
            "price": 18000, "status": "Ready", "score": 0, "history": ["Создано фермером"], "temp": 0, "ph": 0, "video_uploaded": True, "video_link": GLOBAL_VIDEO_LINK, "image_icon": "🍶"
        },
        {
            "id": "BATCH-884", "farmer": "Хозяйство 'Жетісу'", "product": "Баранина", "amount": 25, "unit": "Кг",
            "price": 65000, "status": "Verified", "score": 88, "history": ["Создано фермером", "Водитель принял груз", "Доставлено в Хаб (2.1°C)", "Сертифицировано (Score: 88)"], "temp": 2.1, "ph": 6.1, "video_uploaded": True, "video_link": GLOBAL_VIDEO_LINK, "image_icon": "🐑"
        },
        {
            "id": "BATCH-886", "farmer": "Хозяйство 'Алатау'", "product": "Молоко", "amount": 100, "unit": "Литров",
            "price": 45000, "status": "Verified", "score": 92, "history": ["Создано фермером", "Водитель принял груз", "Доставлено в Хаб (1.5°C)", "Сертифицировано (Score: 92)"], "temp": 1.5, "ph": 6.5, "video_uploaded": True, "video_link": GLOBAL_VIDEO_LINK, "image_icon": "🥛"
        },
        {
            "id": "BATCH-887", "farmer": "Ферма 'Байлык'", "product": "Мед", "amount": 10, "unit": "Кг",
            "price": 25000, "status": "At Hub", "score": 0, "history": ["Создано фермером", "Водитель принял груз", "Доставлено в Хаб (22.0°C)"], "temp": 22.0, "ph": 4.0, "video_uploaded": True, "video_link": GLOBAL_VIDEO_LINK, "image_icon": "🍯"
        },
        {
            "id": "BATCH-888", "farmer": "Хозяйство 'Адал'", "product": "Конина", "amount": 15, "unit": "Кг",
            "price": 40000, "status": "Verified", "score": 90, "history": ["Создано фермером", "Водитель принял груз", "Доставлено в Хаб (1.0°C)", "Сертифицировано (Score: 90)"], "temp": 1.0, "ph": 5.9, "video_uploaded": True, "video_link": GLOBAL_VIDEO_LINK, "image_icon": "🥩"
        },
        {
            "id": "BATCH-890", "farmer": "Хозяйство 'Алатау'", "product": "Овощи", "amount": 50, "unit": "Кг",
            "price": 35000, "status": "Verified", "score": 85, "history": ["Создано фермером", "Водитель принял груз", "Доставлено в Хаб (8.0°C)", "Сертифицировано (Score: 85)"], "temp": 8.0, "ph": 6.8, "video_uploaded": True, "video_link": GLOBAL_VIDEO_LINK, "image_icon": "🥕"
        }
    ]

if 'user_session' not in st.session_state:
    st.session_state['user_session'] = None

# ================= ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ =================
def get_status_color(status):
    if status == "Ready": return "orange"
    if status == "In Transit": return "blue"
    if status == "At Hub": return "purple"
    if status == "Verified": return "#d4edda" 
    if status == "Rejected": return "#f8d7da" 
    return "gray"

def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

# ================= ЭКРАН 0: LOGIN =================
def login_screen():
    c1, c2 = st.columns([1, 1])
    with c1:
        st.image("https://cdn-icons-png.flaticon.com/512/2917/2917995.png", width=100)
        st.markdown("# Degeres Ecosystem")
        st.markdown("### Единая платформа продовольственной безопасности")
        st.markdown("---")
        # QR код убран по просьбе

    with c2:
        st.markdown("### Выберите роль для входа:")
        col_farmer, col_driver = st.columns(2)
        col_hub, col_client = st.columns(2)

        with col_farmer:
            with st.container():
                st.markdown("**👨‍🌾 Фермер**")
                st.caption("Создавайте и управляйте заявками на поставку.")
                if st.button("Войти как Фермер", key='login_farmer'):
                    st.session_state['user_session'] = 'farmer'
                    st.rerun()

        with col_driver:
            with st.container():
                st.markdown("**🚕 Водитель**")
                st.caption("Принимайте и доставляйте продукцию.")
                if st.button("Войти как Водитель", key='login_driver'):
                    st.session_state['user_session'] = 'driver'
                    st.rerun()

        with col_hub:
            with st.container():
                st.markdown("**🛡️ Хаб/Лаборатория**")
                st.caption("Проверяйте качество и безопасность.")
                if st.button("Войти как Хаб", key='login_hub'):
                    st.session_state['user_session'] = 'hub'
                    st.rerun()

        with col_client:
            with st.container():
                st.markdown("**🛒 Покупатель**")
                st.caption("Выбирайте и покупайте проверенную продукцию.")
                if st.button("Войти как Покупатель", key='login_client'):
                    st.session_state['user_session'] = 'client'
                    st.rerun()

# ================= ЭКРАН 1: ФЕРМЕР =================
def farmer_ui():
    with st.sidebar:
        st.title("👨‍🌾 Фермер")
        if st.button("⬅ Выйти"):
            st.session_state['user_session'] = None
            st.rerun()

    st.subheader("📊 Панель управления фермера")

    # Метрики
    farmer_products = [p for p in st.session_state['db_products'] if p['farmer'] == "Хозяйство 'Береке'" or p['farmer'] == "Хозяйство 'Адал'"]
    
    total_deliveries = len(farmer_products)
    products_in_transit = len([p for p in farmer_products if p['status'] in ['Ready', 'In Transit', 'At Hub']])
    successfully_verified = len([p for p in farmer_products if p['status'] == 'Verified'])
    
    scores = [p['score'] for p in farmer_products if p['status'] == 'Verified' and p['score'] > 0]
    average_score = sum(scores) / len(scores) if scores else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Всего поставок", total_deliveries)
    col2.metric("В пути", products_in_transit)
    col3.metric("Проверено", successfully_verified)
    col4.metric("Ср. рейтинг", f"{average_score:.1f}")

    st.markdown("---")
    st.subheader("📤 Новая поставка")

    with st.container():
        farmer_name_input = st.text_input("Название хозяйства", value="Хозяйство 'Береке'")
        c1, c2 = st.columns(2)
        with c1:
            prod = st.selectbox("Продукт", ["Конина", "Говядина", "Кумыс", "Шубат", "Баранина", "Сыры", "Молоко", "Мед", "Курт", "Овощи"], key="new_product_select")
            amount = st.number_input("Объем", min_value=1, value=10, key="new_amount_input")
        with c2:
            unit = st.selectbox("Единица", ["Кг", "Литров"], key="new_unit_select")
            price_per_unit = st.number_input("Цена за единицу (₸)", min_value=100, value=2500, step=100, key="new_price_per_unit")
            total_price_calculated = amount * price_per_unit
            st.success(f"Расчетная общая цена: **{total_price_calculated} ₸**")

        photo_uploaded = st.file_uploader("Фото продукта (обязательно)", type=['jpg', 'png'], key="new_photo_uploader")
        video_uploaded_file = st.file_uploader("Видео процесса (обязательно)", type=['mp4'], key="new_video_uploader")
        st.caption("Система автоматически проверит геолокацию и предложит AI-анализ качества.")

        if st.button("🚀 Отправить и Вызвать такси", key="send_new_batch_button"):
            if not photo_uploaded:
                st.error("Пожалуйста, загрузите фото продукта.")
            elif not video_uploaded_file:
                st.error("Пожалуйста, загрузите видео процесса.")
            else:
                with st.spinner("AI Анализ... Поиск водителей..."):
                    time.sleep(1.5)

                new_id = f"BATCH-{random.randint(1000,9999)}"
                new_item = {
                    "id": new_id,
                    "farmer": farmer_name_input,
                    "product": prod,
                    "amount": amount,
                    "unit": unit,
                    "price": total_price_calculated,
                    "status": "Ready",
                    "score": 0,
                    "history": ["Создано фермером"],
                    "temp": 0,
                    "ph": 0,
                    "video_uploaded": True,
                    "video_link": GLOBAL_VIDEO_LINK, 
                    "image_icon": "❓"
                }
                st.session_state['db_products'].append(new_item)
                st.balloons()
                st.success(f"Заявка {new_id} создана! Статус: Ожидает водителя.")
                time.sleep(1)
                st.rerun()

    st.markdown("---")

    tab_active, tab_history = st.tabs(["Активные партии", "История поставок"])

    with tab_active:
        st.markdown("### 📋 Мои активные заявки")
        my_active_prods = [p for p in st.session_state['db_products'] if (p['farmer'] == farmer_name_input or p['farmer'] == "Хозяйство 'Адал'") and p['status'] in ['Ready', 'In Transit', 'At Hub']]
        if my_active_prods:
            active_df = pd.DataFrame(my_active_prods)[['id', 'product', 'amount', 'unit', 'status']]
            active_df['status_color'] = active_df['status'].apply(get_status_color)
            st.dataframe(active_df.style.apply(lambda x: [f'background-color: {get_status_color(v)}' if k == 'status' else '' for k, v in x.items()], axis=1), column_config={"status_color": None}, hide_index=True)
            st.caption("Цвет статуса: Оранжевый - Ожидает водителя, Синий - В пути, Фиолетовый - В хабе.")
        else:
            st.info("Нет активных заявок.")

    with tab_history:
        st.markdown("### 📂 Архив поставок")
        my_history_prods = [p for p in st.session_state['db_products'] if (p['farmer'] == farmer_name_input or p['farmer'] == "Хозяйство 'Адал'") and p['status'] in ['Verified', 'Rejected']]
        if my_history_prods:
            history_df = pd.DataFrame(my_history_prods)[['id', 'product', 'amount', 'unit', 'score', 'status']]
            history_df['status_color'] = history_df['status'].apply(get_status_color)
            st.dataframe(history_df.style.apply(lambda x: [f'background-color: {get_status_color(v)}' if k == 'status' else '' for k, v in x.items()], axis=1), column_config={"status_color": None}, hide_index=True)
        else:
            st.info("История поставок пуста.")

# ================= ЭКРАН 2: ВОДИТЕЛЬ =================
def driver_ui():
    with st.sidebar:
        st.title("🚕 Водитель")
        if st.button("⬅ Выйти"):
            st.session_state['user_session'] = None
            st.rerun()

    st.subheader("🚚 Управление доставками")
    tab1, tab2, tab3 = st.tabs(["Заказы рядом", "Активный рейс", "История рейсов"])

    with tab1:
        st.markdown("### Доступные заказы")
        available = [p for p in st.session_state['db_products'] if p['status'] == "Ready"]
        if available:
            for item in available:
                with st.expander(f"📦 **{item['product']}** от {item['farmer']} ({item['amount']} {item['unit']})"):
                    st.write(f"**ID партии:** {item['id']}")
                    st.write(f"**Ожидаемая цена:** {item['price']} ₸")
                    if st.button("Принять заказ", key=f"take_order_{item['id']}"):
                        item['status'] = "In Transit"
                        item['history'].append(f"Водитель принял груз {datetime.datetime.now().strftime('%H:%M')}")
                        st.toast("Заказ принят! Перейдите во вкладку 'Активный рейс'.")
                        st.rerun()
        else:
            st.info("Нет новых заказов в вашем районе.")

    with tab2:
        st.markdown("### Ваш активный рейс")
        active = [p for p in st.session_state['db_products'] if p['status'] == "In Transit"]
        if active:
            item = active[0]
            st.success(f"Вы везете: **{item['product']}** (#{item['id']})")
            c1, c2 = st.columns([2, 1])
            with c1:
                m = folium.Map(location=[50.28, 57.16], zoom_start=10)
                folium.Marker([50.28, 57.16], popup="HUB", icon=folium.Icon(color="purple")).add_to(m)
                st_folium(m, height=250, returned_objects=[])
            with c2:
                st.markdown("**Параметры груза (IoT):**")
                st.metric("IoT Температура", "3.4 °C", "Normal")
                st.metric("IoT Влажность", "70%", "Normal")
                if st.button("🏁 Прибыл в Хаб", key=f"arrive_hub_{item['id']}"):
                    item['status'] = "At Hub"
                    item['history'].append(f"Доставлено в Хаб (IoT Temp: 3.4°C) {datetime.datetime.now().strftime('%H:%M')}")
                    st.balloons()
                    st.success("Груз сдан лаборантам!")
                    time.sleep(1)
                    st.rerun()
        else:
            st.info("Вы пока никуда не едете.")

    with tab3:
        st.markdown("### История доставок")
        delivered_by_driver = [p for p in st.session_state['db_products'] if any("Водитель принял груз" in h for h in p['history']) and p['status'] not in ['Ready', 'In Transit', 'At Hub']]
        if delivered_by_driver:
            history_df = pd.DataFrame(delivered_by_driver)[['id', 'product', 'farmer', 'status', 'score']]
            st.dataframe(history_df, use_container_width=True)
        else:
            st.info("Нет завершенных доставок.")

# ================= ЭКРАН 3: ХАБ =================
def hub_ui():
    with st.sidebar:
        st.title("🛡️ Хаб")
        if st.button("⬅ Выйти"):
            st.session_state['user_session'] = None
            st.rerun()

    st.subheader("🔬 Лаборатория: Проверка партий")
    incoming_batches = [p for p in st.session_state['db_products'] if p['status'] == "At Hub"]

    if incoming_batches:
        batch_options = {f"{p['id']} - {p['product']} от {p['farmer']}": p for p in incoming_batches}
        selected_batch_key = st.selectbox("Выберите партию для проверки:", list(batch_options.keys()), key="hub_batch_selector")

        if selected_batch_key:
            item = batch_options[selected_batch_key]
            with st.container():
                st.markdown(f"### Проверка партии: {item['id']} ({item['product']})")
                c1, c2 = st.columns(2)
                with c1:
                    temp = st.slider("Температура (°C)", 0.0, 10.0, 3.5, key=f"temp_{item['id']}")
                    ph = st.slider("pH", 4.0, 9.0, 6.0, key=f"ph_{item['id']}")
                with c2:
                    antibio = st.checkbox("Антибиотики обнаружены", False, key=f"ab_{item['id']}")
                    visual = st.checkbox("Визуальный осмотр OK", True, key=f"vis_{item['id']}")

                rejection_reason = ""
                current_score = 100
                if temp > 6: current_score -= 20
                if not visual: current_score -= 30
                if antibio: current_score = 0

                if current_score < 80:
                    st.warning("Внимание: низкий балл. Требуется причина отбраковки.")
                    rejection_reason = st.text_area("Причина отбраковки:", key=f"reason_{item['id']}")

                if st.button("🖨️ Генерировать Сертификат", key=f"gen_{item['id']}"):
                    item['score'] = current_score
                    item['temp'] = temp
                    item['ph'] = ph
                    
                    if current_score >= 80:
                        item['status'] = "Verified"
                        item['history'].append(f"Сертифицировано (Score: {current_score}) {datetime.datetime.now().strftime('%H:%M')}")
                        st.balloons()
                        st.success("ОДОБРЕНО!")
                        
                        qr_data = item.get('video_link') if item.get('video_uploaded') else f"ID: {item['id']} Verified"
                        st.image(generate_qr(qr_data), width=150, caption="QR-код продукта")
                    else:
                        if not rejection_reason:
                            st.error("Укажите причину отбраковки!")
                        else:
                            item['status'] = "Rejected"
                            item['history'].append(f"Отбраковано: {rejection_reason}")
                            st.error("ОТКАЗ! Партия утилизирована.")
                    
                    time.sleep(2)
                    st.rerun()
    else:
        st.info("Очередь на проверку пуста.")

    st.markdown("---")
    st.markdown("### Реестр партий")
    all_processed = [p for p in st.session_state['db_products'] if p['status'] in ['Verified', 'Rejected']]
    if all_processed:
        processed_df = pd.DataFrame(all_processed)[['id', 'product', 'farmer', 'score', 'status']]
        st.dataframe(processed_df.style.apply(lambda x: [f'background-color: {get_status_color(v)}' if k == 'status' else '' for k, v in x.items()], axis=1), use_container_width=True)

# ================= ЭКРАН 4: ПОКУПАТЕЛЬ =================
def client_ui():
    with st.sidebar:
        st.title("🛒 Магазин")
        if st.button("⬅ Выйти"):
            st.session_state['user_session'] = None
            st.rerun()

    st.subheader("Витрина Degeres (Verified ✅)")
    all_shop_items = [p for p in st.session_state['db_products'] if p['status'] == "Verified"]

    if not all_shop_items:
        st.warning("Витрина пуста.")
        return

    c1, c2, c3 = st.columns(3)
    with c1:
        unique_products = sorted(list(set([i['product'] for i in all_shop_items])))
        sel_prod = st.multiselect("Фильтр: Продукт", unique_products, default=unique_products)
    with c2:
        unique_farmers = sorted(list(set([i['farmer'] for i in all_shop_items])))
        sel_farm = st.multiselect("Фильтр: Фермер", unique_farmers, default=unique_farmers)
    with c3:
        sort_opt = st.selectbox("Сортировка", ["Рейтинг (убыв.)", "Цена (возр.)"])

    filtered = [i for i in all_shop_items if i['product'] in sel_prod and i['farmer'] in sel_farm]
    if sort_opt == "Рейтинг (убыв.)": filtered.sort(key=lambda x: x['score'], reverse=True)
    else: filtered.sort(key=lambda x: x['price'])

    if filtered:
        cols = st.columns(3)
        for idx, item in enumerate(filtered):
            with cols[idx % 3]:
                with st.container():
                    st.markdown(f"<div style='font-size: 3em; text-align: center;'>{item.get('image_icon', '📦')}</div>", unsafe_allow_html=True)
                    st.markdown(f"#### {item['product']}")
                    st.caption(f"от {item['farmer']}")
                    st.metric("Safety Score", f"{item['score']}/100")
                    st.markdown(f"**{item['price']} ₸**")
                    if st.button("Подробнее", key=f"buy_{item['id']}"):
                        st.session_state['view_item'] = item
                        st.rerun()
    
    if 'view_item' in st.session_state:
        v = st.session_state['view_item']
        st.markdown("---")
        st.subheader(f"🔍 Паспорт: {v['id']} - {v['product']}")
        c1, c2 = st.columns(2)
        with c1:
            st.info("История блокчейна:")
            for h in v['history']:
                st.text(f"⬇ {h}")
        with c2:
            st.success(f"Лаборатория: pH {v['ph']} | Temp {v['temp']}°C")
            if v.get('video_link'):
                st.image(generate_qr(v['video_link']), width=200, caption="Видео производства (сканируй)")
            
            if st.button(f"💳 Купить за {v['price']} ₸"):
                st.balloons()
                st.success("Спасибо за покупку!")

# ================= ГЛАВНЫЙ КОНТРОЛЛЕР =================
if st.session_state['user_session'] == 'farmer':
    farmer_ui()
elif st.session_state['user_session'] == 'driver':
    driver_ui()
elif st.session_state['user_session'] == 'hub':
    hub_ui()
elif st.session_state['user_session'] == 'client':
    client_ui()
else:
    login_screen()
    
