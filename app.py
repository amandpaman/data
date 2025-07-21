import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📊 Excel Data Dashboard", layout="wide")

# Style
st.markdown("""
    <style>
        .main {
            background: linear-gradient(to right, #d9e4f5, #f4f9fc);
        }
        .block-container {
            padding: 2rem;
            border-radius: 12px;
        }
        .stButton>button {
            background-color: #4CAF50 !important;
            color: white !important;
            font-weight: bold;
        }
        .stSelectbox, .stMultiselect, .stTextInput {
            background-color: #ffffff !important;
            border-radius: 10px !important;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Excel Visual Dashboard")
st.markdown("Use this dashboard to visualize and filter data from Excel files.")
st.markdown("---")

# Navigation
menu = st.sidebar.radio("🔍 Navigation", ["📁 Upload File", "🧾 View Data", "📈 Visualize Data", "📤 Export Data"])

# Store globally
if "df" not in st.session_state:
    st.session_state.df = None

# Upload File
if menu == "📁 Upload File":
    st.subheader("📥 Upload Excel File")
    file = st.file_uploader("Upload your Excel file (.xlsx)", type=["xlsx"])
    if file:
        try:
            df = pd.read_excel(file)
            st.session_state.df = df
            st.success("✅ File uploaded successfully!")
            st.write(df.head())
        except Exception as e:
            st.error(f"❌ Error loading file: {e}")

# View Data
elif menu == "🧾 View Data":
    df = st.session_state.df
    if df is not None:
        st.subheader("📄 Raw Data Preview")
        st.dataframe(df, use_container_width=True)
        st.markdown(f"**Shape:** `{df.shape[0]} rows × {df.shape[1]} columns`")
    else:
        st.warning("⚠️ Please upload a file first.")

# Visualization
elif menu == "📈 Visualize Data":
    df = st.session_state.df
    if df is not None:
        st.subheader("📊 Data Visualization")

        filter_cols = df.columns.tolist()
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        all_cols = df.columns.tolist()

        with st.expander("🧰 Filters", expanded=True):
            if "Location" in df.columns:
                locs = st.multiselect("📍 Filter by Location", df["Location"].unique())
                if locs:
                    df = df[df["Location"].isin(locs)]

            if "Device" in df.columns:
                devices = st.multiselect("💻 Filter by Device", df["Device"].unique())
                if devices:
                    df = df[df["Device"].isin(devices)]

            if "Status" in df.columns:
                statuses = st.multiselect("📶 Filter by Status", df["Status"].unique())
                if statuses:
                    df = df[df["Status"].isin(statuses)]

            if "Date" in df.columns:
                df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
                date_range = st.date_input("🗓 Filter by Date Range",
                                           value=(df["Date"].min(), df["Date"].max()))
                if len(date_range) == 2:
                    df = df[(df["Date"] >= pd.to_datetime(date_range[0])) & (df["Date"] <= pd.to_datetime(date_range[1]))]

        col1, col2, col3 = st.columns(3)

        with col1:
            x_axis = st.selectbox("🧭 X-axis", options=all_cols)
        with col2:
            y_axis = st.selectbox("📊 Y-axis (numeric)", options=numeric_cols)
        with col3:
            chart_type = st.selectbox("📈 Chart Type", ["Bar", "Line", "Scatter", "Pie"])

        if st.button("🔍 Generate Chart"):
            try:
                fig = None
                if chart_type == "Bar":
                    fig = px.bar(df, x=x_axis, y=y_axis, color=x_axis)
                elif chart_type == "Line":
                    fig = px.line(df, x=x_axis, y=y_axis)
                elif chart_type == "Scatter":
                    fig = px.scatter(df, x=x_axis, y=y_axis, color=x_axis, size=y_axis)
                elif chart_type == "Pie":
                    fig = px.pie(df, names=x_axis, values=y_axis)

                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"❌ Failed to generate chart: {e}")
    else:
        st.warning("⚠️ Please upload a file first.")

# Export filtered data
elif menu == "📤 Export Data":
    df = st.session_state.df
    if df is not None:
        st.subheader("📤 Export Filtered Data")
        st.download_button(
            label="📥 Download CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="filtered_data.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ Please upload a file first.")
