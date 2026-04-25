import streamlit as st
import pandas as pd
import plotly.express as px

# Basic Page Config
st.set_page_config(page_title="Zahratun Dashboard", layout="wide")

# Sidebar Navigation
st.sidebar.title("Zahratun (Jondor-1)")
menu = st.sidebar.radio("Navigation", ["Main Dashboard", "Sales Analytics", "Staff Planning", "Inventory"])

st.title(f"Zahratun Fast-Food: {menu}")

# Placeholder for Data
st.info("System is ready. Please upload your 'SPMH (1).xlsx' file to start tracking.")

# Simple Demo Chart
data = {
    'Category': ['Burgers', 'Drinks', 'Sides', 'Desserts'],
    'Revenue': [450, 200, 150, 100]
}
df = pd.DataFrame(data)
fig = px.bar(df, x='Category', y='Revenue', title="Weekly Performance (Demo)")
st.plotly_chart(fig)

if menu == "Main Dashboard":
    st.subheader("Key Performance Indicators (KPI)")
    col1, col2, col3 = st.columns(3)
    col1.metric("Revenue Plan", "100%", "+5%")
    col2.metric("Orders", "1,240", "-2%")
    col3.metric("Average Check", "$12.5", "+0.4%")

elif menu == "Staff Planning":
    st.write("Section for calculating salaries and schedules.")
