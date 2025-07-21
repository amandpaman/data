import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Excel Dashboard", layout="wide")

st.title("📊 Excel Data Dashboard")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("Preview of Data")
    st.dataframe(df)

    numeric_columns = df.select_dtypes(include='number').columns.tolist()
    categorical_columns = df.select_dtypes(include='object').columns.tolist()

    st.sidebar.header("📌 Plot Controls")
    chart_type = st.sidebar.selectbox("Choose Chart Type", ["Bar", "Line", "Scatter", "Pie"])

    x_axis = st.sidebar.selectbox("X-axis", options=df.columns)
    y_axis = st.sidebar.selectbox("Y-axis", options=numeric_columns)

    if chart_type == "Bar":
        fig = px.bar(df, x=x_axis, y=y_axis)
    elif chart_type == "Line":
        fig = px.line(df, x=x_axis, y=y_axis)
    elif chart_type == "Scatter":
        fig = px.scatter(df, x=x_axis, y=y_axis)
    elif chart_type == "Pie":
        fig = px.pie(df, names=x_axis, values=y_axis)

    st.plotly_chart(fig, use_container_width=True)
