import streamlit as st
import pandas as pd
import plotly.express as px

# ✅ لازم يكون هنا فورا بعد import
st.set_page_config(page_title="Golden.Egy", layout="wide")

# 🟡 تحميل البيانات
@st.cache_data
def load_data():
    return pd.read_csv("golden_egy_data.csv", parse_dates=["datetime"])

df = load_data()

# 🎨 عنوان
st.title("💰 Golden.Egy – Gold & Dollar Tracker")

# 🕓 فلترة بالتاريخ
start_date = st.sidebar.date_input("📅 من تاريخ", df["datetime"].min().date())
end_date = st.sidebar.date_input("📅 إلى تاريخ", df["datetime"].max().date())

mask = (df["datetime"].dt.date >= start_date) & (df["datetime"].dt.date <= end_date)
filtered_df = df[mask]

# 📈 اختيارات الرسم
metric = st.selectbox("📊 اختر ما تريد تتبعه:", df.columns.drop("datetime"))

fig = px.line(filtered_df, x="datetime", y=metric, title=f"حركة {metric} بمرور الوقت")
st.plotly_chart(fig, use_container_width=True)

# 💡 مقارنة بالدولار
if metric.startswith("عيار") or metric == "جنيه الذهب":
    fig2 = px.line(filtered_df, x="datetime", y=["دولار السوق", "دولار الصاغة", "دولار البنوك"],
                   title="🟢 مقارنة بين أسعار الدولار")
    st.plotly_chart(fig2, use_container_width=True)

# 📌 تذييل
st.markdown("""
---
Developed with ❤️ by **You**  
Follow updates on Telegram – Golden.Egy
""")
