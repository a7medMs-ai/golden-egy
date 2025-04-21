import streamlit as st
import pandas as pd
import plotly.express as px

# ✅ Set page configuration
st.set_page_config(page_title="Golden.Egy", layout="wide")

# 🟡 Load data with caching
@st.cache_data
def load_data():
    # Load the dataset and drop the 'Unnamed: 0' column
    df = pd.read_csv("golden_egy_data.csv", parse_dates=["datetime"])
    if "Unnamed: 0" in df.columns:
        df.drop(columns=["Unnamed: 0"], inplace=True)
    return df

df = load_data()

# 🎨 Title
st.title("💰 Golden.Egy – Gold & Dollar Tracker")

# 🕓 Date filtering
start_date = st.sidebar.date_input("📅 From Date", df["datetime"].min().date())
end_date = st.sidebar.date_input("📅 To Date", df["datetime"].max().date())

mask = (df["datetime"].dt.date >= start_date) & (df["datetime"].dt.date <= end_date)
filtered_df = df[mask]

# 📈 Select metric to track
default_metric = "عيار 21"
metric_options = [col for col in df.columns if col not in ["datetime"]]
metric = st.sidebar.selectbox("📊 Choose Metric to Track:", metric_options, index=metric_options.index(default_metric))

# Main chart for selected metric
fig = px.line(
    filtered_df,
    x="datetime",
    y=metric,
    title=f"Movement of {metric} Over Time",
    labels={"datetime": "Date", metric: "Price"},
    hover_data={"Difference": filtered_df["سعر البيع"] - filtered_df["سعر الشراء"] if metric == "عيار 21" else None},
)

# Add custom hover template for "عيار 21"
if metric == "عيار 21":
    fig.update_traces(
        hovertemplate="Date: %{x}<br>Price: %{y}<br>Difference: %{customdata[0]}<extra></extra>",
    )

st.plotly_chart(fig, use_container_width=True)

# 💰 Show three lines: Gold 21, Bank Dollar, and Jewelry Dollar
if metric == "عيار 21":
    st.subheader("Comparison: Gold 21 vs. Dollar Prices")
    fig_comparison = px.line(
        filtered_df,
        x="datetime",
        y=["عيار 21", "دولار البنوك", "دولار الصاغة"],
        title="Gold 21 vs. Dollar Prices",
        labels={"datetime": "Date", "value": "Price"},
        color_discrete_map={
            "عيار 21": "blue",
            "دولار البنوك": "green",
            "دولار الصاغة": "red",
        },
    )
    st.plotly_chart(fig_comparison, use_container_width=True)

# 📌 Footer
st.markdown("""
---
Developed with ❤️ by **You**  
Follow updates on Telegram – Golden.Egy
""")
