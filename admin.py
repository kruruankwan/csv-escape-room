import streamlit as st
import pandas as pd

st.set_page_config(page_title="Admin Dashboard — Escape Room", page_icon="📊", layout="wide")

st.title("📊 Dashboard — ผล CSV Escape Room")

# --- Load data from Google Sheet ---
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQIHdSOZCCAyAPLg41A9no_hJmAhm9dPV4lim7xxBctg-WSJxrnO5Uc6bdD9WSo16o0krwa6319JQ1p/pub?output=csv"
df = pd.read_csv(SHEET_CSV_URL)

# --- Clean ---
# ถ้าไม่มีคอลัมน์ time_used ให้สร้างคอลัมน์เปล่า
if "time_used" not in df.columns:
    df["time_used"] = None

# แปลง timestamp
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"])

# แปลงเวลาเป็นวินาที (ถ้ามีข้อมูล)
def convert_time(t):
    if pd.isna(t):
        return None
    try:
        parts = t.split(" ")
        minutes = int(parts[0])
        seconds = int(parts[2])
        return minutes * 60 + seconds
    except:
        return None

df["time_seconds"] = df["time_used"].apply(convert_time)

# --- Sidebar filter ---
st.sidebar.header("🔎 ตัวกรองข้อมูล")
if "group_name" in df.columns:
    group_filter = st.sidebar.multiselect("เลือกกลุ่ม", df["group_name"].unique(), default=df["group_name"])
else:
    group_filter = []

if "classroom" in df.columns:
    room_filter = st.sidebar.multiselect("เลือกห้อง", df["classroom"].unique(), default=df["classroom"])
else:
    room_filter = []

# กรองข้อมูล
if group_filter:
    df = df[df["group_name"].isin(group_filter)]
if room_filter:
    df = df[df["classroom"].isin(room_filter)]

# --- Show table ---
st.subheader("📋 ตารางข้อมูลทั้งหมด")
st.dataframe(df)

# --- Summary ---
st.subheader("📊 สรุป")

col1, col2 = st.columns(2)
with col1:
    if "group_name" in df.columns:
        st.metric("จำนวนกลุ่ม", df["group_name"].nunique())
    st.metric("จำนวนรายการทั้งหมด", len(df))

with col2:
    if "result" in df.columns:
        st.metric("ตอบถูกทั้งหมด", (df["result"] == "ถูกต้อง").sum())
        st.metric("ตอบผิดทั้งหมด", (df["result"] == "ผิด").sum())

# --- Ranking (เฉพาะที่มี time_seconds) ---
if df["time_seconds"].notna().sum() > 0:
    st.subheader("🏆 อันดับเวลาเร็วสุด (เฉพาะกลุ่มที่มีข้อมูลเวลา)")
    rank = df.dropna(subset=["time_seconds"]).groupby("group_name")["time_seconds"].min().sort_values()
    st.table(rank.reset_index().rename(columns={"time_seconds": "เวลา (วินาที)"}))

# --- Charts ---
if "result" in df.columns:
    st.subheader("📈 กราฟคำตอบถูก/ผิด")
    chart_data = df.groupby(["stage", "result"]).size().unstack(fill_value=0)
    st.bar_chart(chart_data)

# --- Download ---
st.subheader("📥 ดาวน์โหลดข้อมูล")
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("ดาวน์โหลด CSV", csv, "escape_room_results.csv", "text/csv")