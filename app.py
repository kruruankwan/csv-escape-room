


import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime
#โหลดไฟล์ css
with open("style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# -------------------------------------------------
# CONFIG
# -------------------------------------------------
st.markdown('<h1 class="main-title">🔐 CSV Escape Room</h1>', unsafe_allow_html=True)
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbyvMwxoQBgPc7nt4UXduCrLwkOEDJCz6qzQEZMtBJ-rT7MZvEIVF_5CcCdOZzmpAGRY/exec"

st.set_page_config(
    page_title="CSV Escape Room",
    page_icon="🔐",
    layout="centered"
)

# -------------------------------------------------
# FUNCTION : SEND LOG TO GOOGLE SHEET
# -------------------------------------------------
def log_to_sheet(group, room, stage, answer, result, time_used=""):
    payload = {
        "group_name": group,
        "classroom": room,
        "stage": stage,
        "answer": answer,
        "result": result,
        "time_used": time_used
    }
    requests.post(WEBHOOK_URL, json=payload)


# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "stage" not in st.session_state:
    st.session_state.stage = 0

if "group_name" not in st.session_state:
    st.session_state.group_name = ""

if "room" not in st.session_state:
    st.session_state.room = ""

if "start_time" not in st.session_state:
    st.session_state.start_time = None


# -------------------------------------------------
# THEME (ดำ–น้ำเงิน–ม่วง)
# -------------------------------------------------
st.markdown("""
<style>
    body {
        background-color: #0d0f1a;
        color: white;
    }
    .stButton>button {
        background-color: #6a0dad;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: 2px solid #9b5cff;
    }
    .stTextInput>div>input {
        background-color: #1b1e2b;
        color: #fff;
    }
</style>
""", unsafe_allow_html=True)


# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown("<h1 style='color:#b480ff;'>🔐 CSV Escape Room</h1>", unsafe_allow_html=True)

# -------------------------------------------------
# SHOW TIMER
# -------------------------------------------------
if st.session_state.start_time:
    elapsed = int(time.time() - st.session_state.start_time)
    m = elapsed // 60
    s = elapsed % 60
    st.info(f"⏳ เวลาที่ผ่านไป: **{m} นาที {s} วินาที**")


# -------------------------------------------------
# PAGE 0 — INPUT INFO
# -------------------------------------------------
if st.session_state.stage == 0:
    st.markdown("### 🧩 กรุณากรอกข้อมูลก่อนเริ่มเกม")

    st.session_state.group_name = st.text_input("ชื่อกลุ่ม")
    st.session_state.room = st.text_input("ห้องเรียน เช่น ม.3/1")

    if st.button("เริ่มเกม →"):
        if st.session_state.group_name.strip() == "" or st.session_state.room.strip() == "":
            st.warning("กรุณากรอกชื่อกลุ่มและห้องเรียนก่อน!")
        else:
            st.session_state.start_time = time.time()  # เริ่มจับเวลา
            st.session_state.stage = 1
            st.rerun()


# -------------------------------------------------
# STAGE 1 — MAX SALES
# -------------------------------------------------
elif st.session_state.stage == 1:
    st.markdown("## 🔎 ด่านที่ 1 : หายอดขายสูงสุด")

    df = pd.read_csv("1_sales_50.csv")
    correct = df["Sales"].max()

    user = st.number_input("กรอกคำตอบ", step=1)

    if st.button("ตรวจคำตอบ"):
        result = "ถูกต้อง" if user == correct else "ผิด"
        log_to_sheet(st.session_state.group_name, st.session_state.room, 1, user, result)

        if result == "ถูกต้อง":
            st.success("🎉 ถูกต้อง! ไปด่านถัดไป →")
            st.session_state.stage = 2
            st.rerun()
        else:
            st.error("❌ คำตอบผิด")


# -------------------------------------------------
# STAGE 2 — EXERCISE > 40
# -------------------------------------------------
elif st.session_state.stage == 2:
    st.markdown("## 💪 ด่านที่ 2 : หาคนที่ออกกำลังกายน้อยที่สุด")

    df = pd.read_csv("2_exercise_50.csv")
    correct = df["ExerciseMinutes"].min()

    user = st.number_input("กรอกจำนวนคน", step=1)

    if st.button("ตรวจคำตอบ"):
        result = "ถูกต้อง" if user == correct else "ผิด"
        log_to_sheet(st.session_state.group_name, st.session_state.room, 2, user, result)

        if result == "ถูกต้อง":
            st.success("🎉 เก่งมาก! ไปด่านที่ 3 →")
            st.session_state.stage = 3
            st.rerun()
        else:
            st.error("❌ คำตอบผิด")


# -------------------------------------------------
# STAGE 3 — AVERAGE INTERNET HOURS
# -------------------------------------------------
elif st.session_state.stage == 3:
    st.markdown("## 🌐 ด่านที่ 3 : ค่าเฉลี่ยเวลาการใช้อินเทอร์เน็ต (ทศนิยม 2 ตำแหน่ง)")

    df = pd.read_csv("3_internet_survey_50.csv")
    correct = round(df["HoursUsed"].mean(), 2)

    user = st.number_input("กรอกคำตอบ เช่น 4.74", format="%.2f")

    if st.button("ตรวจคำตอบ"):
        result = "ถูกต้อง" if abs(user - correct) < 0.01 else "ผิด"
        log_to_sheet(st.session_state.group_name, st.session_state.room, 3, user, result)

        if result == "ถูกต้อง":
            st.success("🎉 ดีมาก! ไปด่าน 4 →")
            st.session_state.stage = 4
            st.rerun()
        else:
            st.error("❌ คำตอบไม่ถูก")


# -------------------------------------------------
# STAGE 4 — MIN WEBSITE VISITORS (UPDATED)
# -------------------------------------------------
elif st.session_state.stage == 4:
    st.markdown("## 📊 ด่านที่ 4 : หาจำนวนคนที่เข้าเว็บน้อยที่สุด")

    df = pd.read_csv("4_web_traffic_50.csv")
    correct = df["Visitors"].min()  # ด่านใหม่ ใช้ .min()

    user = st.number_input("กรอกจำนวนคน", step=1)

    if st.button("ตรวจคำตอบ"):
        result = "ถูกต้อง" if user == correct else "ผิด"
        log_to_sheet(st.session_state.group_name, st.session_state.room, 4, user, result)

        if result == "ถูกต้อง":
            st.success("🎉 ยอดเยี่ยม! ไปด่านสุดท้าย →")
            st.session_state.stage = 5
            st.rerun()
        else:
            st.error("❌ คำตอบผิด")


# -------------------------------------------------
# STAGE 5 — MAX ELECTRICITY
# -------------------------------------------------
elif st.session_state.stage == 5:
    st.markdown("## ⚡ ด่านที่ 5 : หาหน่วยไฟฟ้าที่ใช้สูงที่สุด")

    df = pd.read_csv("5_electricity_50.csv")
    correct = df["Units"].max()

    user = st.number_input("กรอกคำตอบ", step=1)

    if st.button("ตรวจคำตอบ"):
        finish = time.time()
        total_sec = int(finish - st.session_state.start_time)
        m = total_sec // 60
        s = total_sec % 60
        formatted = f"{m} นาที {s} วินาที"

        result = "ถูกต้อง" if user == correct else "ผิด"

        log_to_sheet(
            st.session_state.group_name,
            st.session_state.room,
            5,
            user,
            result,
            formatted
        )

        if result == "ถูกต้อง":
            st.success(f"🎉 ผ่านครบทุกด่าน! ใช้เวลา {formatted}")
            st.balloons()
        else:

            st.error("❌ คำตอบผิด")




