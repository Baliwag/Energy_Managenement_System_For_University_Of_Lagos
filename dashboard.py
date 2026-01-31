# =============================================
# UNILAG Energy Forecast Dashboard (Streamlit + Plotly + Subplots)
# =============================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ------------------------
# Load Dataset
# ------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("unilag_LSTM_8760h_forecast_Jun2025_Jun2026_REAL.csv")

    # Parse timestamp
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    else:
        df.index = pd.date_range(start="2025-06-01", periods=len(df), freq="H")
        df["Timestamp"] = df.index

    df = df.set_index("Timestamp")
    return df

df = load_data()

# ------------------------
# Streamlit Config
# ------------------------
st.set_page_config(
    page_title="UNILAG Smart Energy Forecast Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("⚡ UNILAG Smart Energy Forecast Dashboard")
st.markdown("""
This interactive dashboard presents **forecasted energy usage** for the University of Lagos 
from **June 2025 to June 2026**, based on LSTM model predictions.
""")

# ------------------------
# Sidebar Controls
# ------------------------
st.sidebar.header("⚙️ Dashboard Controls")

columns = [col for col in df.columns if col.lower() not in ["timestamp", "date"]]

default_index = columns.index("Total_MW") if "Total_MW" in columns else 0
selected_feeders = st.sidebar.multiselect("Select Feeders / Loads", columns, default=[columns[default_index]])

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df.index.min().date(), df.index.max().date()],
    min_value=df.index.min().date(),
    max_value=df.index.max().date()
)

granularity = st.sidebar.radio("Aggregation Level", ["Hourly", "Daily", "Weekly", "Monthly"])

rolling_window = st.sidebar.slider("Rolling Average Window (hours)", 0, 168, 0)

tariff_rate = st.sidebar.number_input("Tariff Rate (₦/MWh)", min_value=0.0, value=65.0)

# Filter dataset
df_filtered = df.loc[str(date_range[0]):str(date_range[1]), selected_feeders]

if granularity == "Daily":
    df_filtered = df_filtered.resample("D").mean()
elif granularity == "Weekly":
    df_filtered = df_filtered.resample("W").mean()
elif granularity == "Monthly":
    df_filtered = df_filtered.resample("M").mean()

if rolling_window > 0:
    df_filtered = df_filtered.rolling(rolling_window).mean()

# ------------------------
# KPIs
# ------------------------
st.subheader("📊 Key Performance Indicators")

for feeder in selected_feeders:
    avg_load = df_filtered[feeder].mean()
    peak_load = df_filtered[feeder].max()
    min_load = df_filtered[feeder].min()
    total_energy = df_filtered[feeder].sum()
    load_factor = avg_load / peak_load if peak_load != 0 else 0
    cost_estimate = total_energy * tariff_rate

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric(f"{feeder} Avg Load (MW)", f"{avg_load:.2f}")
    col2.metric(f"{feeder} Peak Load (MW)", f"{peak_load:.2f}")
    col3.metric(f"{feeder} Min Load (MW)", f"{min_load:.2f}")
    col4.metric(f"{feeder} Total Energy (MWh)", f"{total_energy:.2f}")
    col5.metric(f"{feeder} Load Factor", f"{load_factor:.2f}")
    col6.metric(f"{feeder} Est. Cost (₦)", f"{cost_estimate:,.0f}")

st.markdown("---")

# ------------------------
# Subplots: Multi-Feeder Comparison
# ------------------------
st.subheader("📊 Multi-Feeder Subplot Comparison")

if len(selected_feeders) > 1:
    fig_sub = make_subplots(
        rows=len(selected_feeders),
        cols=1,
        shared_xaxes=True,
        subplot_titles=[f"{feeder}" for feeder in selected_feeders]
    )

    for i, feeder in enumerate(selected_feeders, start=1):
        fig_sub.add_trace(
            go.Scatter(x=df_filtered.index, y=df_filtered[feeder], mode="lines", name=feeder),
            row=i, col=1
        )

    fig_sub.update_layout(
        height=300*len(selected_feeders),
        title="Feeder Load Forecasts (Stacked Subplots)",
        xaxis_title="Time",
        yaxis_title="Load (MW)",
        showlegend=False,
        hovermode="x unified",
        template="plotly_white"
    )

    st.plotly_chart(fig_sub, use_container_width=True)
else:
    st.info("Select more than one feeder from the sidebar to see subplot comparison.")

st.markdown("---")

# ------------------------
# Time Series (Overlay)
# ------------------------
st.subheader("📈 Time Series Forecast (Overlay)")

fig = go.Figure()
for feeder in selected_feeders:
    fig.add_trace(go.Scatter(x=df_filtered.index, y=df_filtered[feeder], mode="lines", name=feeder))

fig.update_layout(
    xaxis_title="Time",
    yaxis_title="Load (MW)",
    hovermode="x unified",
    template="plotly_white"
)
st.plotly_chart(fig, use_container_width=True)

# ------------------------
# Boxplots (Seasonality)
# ------------------------
st.subheader("📦 Distribution Analysis (Seasonality)")

df_box = df.copy()
df_box["Month"] = df_box.index.month_name()
df_box["Day"] = df_box.index.day_name()

col1, col2 = st.columns(2)

with col1:
    fig1 = px.box(df_box, x="Month", y=selected_feeders[0], title=f"Monthly Distribution - {selected_feeders[0]}")
    fig1.update_xaxes(categoryorder="array", categoryarray=[
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ])
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.box(df_box, x="Day", y=selected_feeders[0], title=f"Weekly Distribution - {selected_feeders[0]}")
    fig2.update_xaxes(categoryorder="array", categoryarray=[
        "Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"
    ])
    st.plotly_chart(fig2, use_container_width=True)

# ------------------------
# Heatmap Analysis
# ------------------------
st.subheader("🔥 Load Heatmap (Hour vs Month)")

df_heat = df.copy()
df_heat["Month"] = df_heat.index.month_name()
df_heat["Hour"] = df_heat.index.hour

pivot = df_heat.pivot_table(index="Hour", columns="Month", values=selected_feeders[0], aggfunc="mean")

fig3 = px.imshow(pivot, aspect="auto", color_continuous_scale="Viridis",
                 title=f"Heatmap of {selected_feeders[0]} (Hour vs Month)")
st.plotly_chart(fig3, use_container_width=True)

# ------------------------
# Anomaly Detection (Z-score)
# ------------------------
st.subheader("🚨 Anomaly Detection")

feeder = selected_feeders[0]
series = df_filtered[feeder].dropna()
z_score = (series - series.mean()) / series.std()
anomalies = series[z_score.abs() > 3]

fig4 = go.Figure()
fig4.add_trace(go.Scatter(x=series.index, y=series, mode="lines", name="Forecast"))
fig4.add_trace(go.Scatter(x=anomalies.index, y=anomalies, mode="markers", name="Anomalies", marker=dict(color="red", size=8)))

fig4.update_layout(
    title=f"Anomaly Detection for {feeder}",
    xaxis_title="Time",
    yaxis_title="Load (MW)",
    hovermode="x unified",
    template="plotly_white"
)
st.plotly_chart(fig4, use_container_width=True)

# ------------------------
# Data Download
# ------------------------
st.subheader("⬇️ Download Data")

csv = df_filtered.to_csv().encode("utf-8")
st.download_button(
    "Download Filtered Forecast Data (CSV)",
    csv,
    f"forecast_{granularity}.csv",
    "text/csv"
)
