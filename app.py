import streamlit as st
import pandas as pd
import plotly.express as px

# App Config
st.set_page_config(page_title="Network Monitor", layout="wide")

# Custom CSS for Navbar and Colored Boxes
st.markdown("""
    <style>
    .main {
        background: linear-gradient(120deg, #eef2f3, #8e9eab);
    }
    .sidebar .sidebar-content {
        background-color: #2c3e50;
        color: white;
    }
    .sidebar .sidebar-content a {
        color: #ffffff;
    }
    .metric-box {
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
    }
    .green { background-color: #27ae60; }
    .blue { background-color: #2980b9; }
    .red { background-color: #c0392b; }
    </style>
""", unsafe_allow_html=True)

# Sidebar as Navbar
with st.sidebar:
    st.title("🛰️ Network Dashboard")
    st.markdown("Navigate below:")
    nav_option = st.radio("Go to:", ["📊 Dashboard", "📁 View Data", "📈 Visualizations"])
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
    st.markdown("---")
    st.caption("Made with ❤️ for Network Monitoring")

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    if nav_option == "📁 View Data":
        st.title("📁 Full Data")
        st.dataframe(df, use_container_width=True)

    elif nav_option == "📈 Visualizations":
        st.title("📈 Visualizations")

        st.subheader("🧠 CPU Usage by Device Type")
        fig1 = px.box(df, x="Device Type", y="CPU Usage (%)", color="Device Type")
        st.plotly_chart(fig1, use_container_width=True)

        st.subheader("💾 Memory Usage Distribution")
        fig2 = px.histogram(df, x="Memory Usage (%)", nbins=40, color="Device Type")
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("📶 Total Network Traffic by Location")
        fig3 = px.bar(df.groupby("Location")["Network Traffic (MB)"].sum().reset_index(),
                      x="Location", y="Network Traffic (MB)", color="Location")
        st.plotly_chart(fig3, use_container_width=True)

    else:  # Dashboard
        st.title("📊 Dashboard Overview")

        # Filters
        with st.expander("🔧 Apply Filters"):
            col1, col2, col3 = st.columns(3)
            with col1:
                location = st.multiselect("Filter by Location", df["Location"].unique())
            with col2:
                device_type = st.multiselect("Filter by Device Type", df["Device Type"].unique())
            with col3:
                status = st.multiselect("Filter by Status", df["Status"].unique())

        filtered_df = df.copy()
        if location:
            filtered_df = filtered_df[filtered_df["Location"].isin(location)]
        if device_type:
            filtered_df = filtered_df[filtered_df["Device Type"].isin(device_type)]
        if status:
            filtered_df = filtered_df[filtered_df["Status"].isin(status)]

        # Metrics in colored boxes
        col1, col2, col3 = st.columns(3)
        col1.markdown(f"""
            <div class='metric-box green'>
                <h3>Total Devices</h3>
                <h2>{len(filtered_df)}</h2>
            </div>""", unsafe_allow_html=True)

        col2.markdown(f"""
            <div class='metric-box blue'>
                <h3>Online Devices</h3>
                <h2>{(filtered_df["Status"] == "Online").sum()}</h2>
            </div>""", unsafe_allow_html=True)

        col3.markdown(f"""
            <div class='metric-box red'>
                <h3>Avg. CPU Usage</h3>
                <h2>{filtered_df["CPU Usage (%)"].mean():.2f}%</h2>
            </div>""", unsafe_allow_html=True)

        st.divider()

        # Quick Charts
        st.subheader("📌 Quick Stats")
        col4, col5 = st.columns(2)

        with col4:
            cpu_chart = px.box(filtered_df, x="Device Type", y="CPU Usage (%)", color="Device Type")
            st.plotly_chart(cpu_chart, use_container_width=True)

        with col5:
            mem_chart = px.histogram(filtered_df, x="Memory Usage (%)", nbins=30, color="Device Type")
            st.plotly_chart(mem_chart, use_container_width=True)

else:
    st.warning("📂 Please upload an Excel file from the sidebar to begin.")
