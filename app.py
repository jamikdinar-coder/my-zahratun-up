import streamlit as st
import pandas as pd
import plotly.express as px

# Настройка страницы
st.set_page_config(page_title="Zahratun Dashboard", layout="wide")

# Боковая панель
st.sidebar.title("Zahratun (Jondor-1)")
menu = st.sidebar.radio("Navigation", ["Main Dashboard", "Sales Analytics", "Staff Planning"])

if menu == "Main Dashboard":
    st.title("Main Dashboard — Weekly Overview")
    
    # Блок с основными цифрами (KPI)
    st.subheader("General Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", "15,400", "+12%")
    col2.metric("Total Orders", "850", "+5%")
    col3.metric("Avg. Check", "18.1", "-2%")
    col4.metric("Active Staff", "12", "0")

    st.markdown("---")

    # Таблица по типам заказов
    st.subheader("Revenue by Order Type")
    
    # Создаем таблицу с данными
    sales_data = {
        "Order Type": ["Dine-in (Зал)", "Takeaway (С собой)", "Delivery (Доставка)", "Pick-up (Самовывоз)"],
        "Checks": [320, 210, 180, 140],
        "Revenue": [6400, 4200, 2800, 2000],
        "Avg. Time (min)": [15, 8, 35, 10]
    }
    df_sales = pd.DataFrame(sales_data)
    
    # Отображаем таблицу и график рядом
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.dataframe(df_sales, use_container_config=True)
    
    with c2:
        fig = px.pie(df_sales, values='Revenue', names='Order Type', title="Revenue Share")
        st.plotly_chart(fig, use_container_width=True)

    # График выручки по времени (пример)
    st.subheader("Daily Revenue Trend")
    chart_data = pd.DataFrame({
        'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'Revenue': [1800, 2100, 1900, 2300, 3100, 4200, 3800]
    })
    line_fig = px.line(chart_data, x='Day', y='Revenue', markers=True)
    st.plotly_chart(line_fig, use_container_width=True)

else:
    st.title(menu)
    st.info("This section is under development.")
