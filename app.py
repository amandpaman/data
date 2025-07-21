import streamlit as st
import pandas as pd
import plotly.express as px

# App Config
st.set_page_config(page_title="Network Monitoring Dashboard", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(120deg, #f5f7fa, #c3cfe2);
        padding: 2rem;
    }
    .block-container {
        padding-top: 2rem;
    }
    h1, h2 {
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
st.title("📡 Network Device Monitoring Dashboard")
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Display data
    st.subheader("🔍 Raw Data")
    st.dataframe(df, use_container_width=True)

    # Filter Sidebar
    with st.sidebar:
        st.header("📊 Filters")
        location = st.multiselect("Location", df["Location"].unique())
        device_type = st.multiselect("Device Type", df["Device Type"].unique())
        status = st.multiselect("Status", df["Status"].unique())

    filtered_df = df.copy()
    if location:
        filtered_df = filtered_df[filtered_df["Location"].isin(location)]
    if device_type:
        filtered_df = filtered_df[filtered_df["Device Type"].isin(device_type)]
    if status:
        filtered_df = filtered_df[filtered_df["Status"].isin(status)]

    st.subheader("📈 Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Devices", len(filtered_df))
    col2.metric("Online Devices", (filtered_df["Status"] == "Online").sum())
    col3.metric("Avg CPU Usage", f'{filtered_df["CPU Usage (%)"].mean():.2f}%')

    st.divider()

    # CPU Usage Graph
    st.subheader("🧠 CPU Usage by Device Type")
    fig1 = px.box(filtered_df, x="Device Type", y="CPU Usage (%)", color="Device Type", title="CPU Usage Distribution")
    st.plotly_chart(fig1, use_container_width=True)

    # Memory Usage Pie Chart
    st.subheader("💾 Memory Usage Overview")
    mem_fig = px.histogram(filtered_df, x="Memory Usage (%)", nbins=40, color="Device Type")
    st.plotly_chart(mem_fig, use_container_width=True)

    # Network Traffic
    st.subheader("📶 Network Traffic by Location")
    traffic_fig = px.bar(filtered_df.groupby("Location")["Network Traffic (MB)"].sum().reset_index(),
                         x="Location", y="Network Traffic (MB)", color="Location")
    st.plotly_chart(traffic_fig, use_container_width=True)
