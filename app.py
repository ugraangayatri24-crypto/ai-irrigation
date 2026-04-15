import streamlit as st
import random
import numpy as np
import pandas as pd
import re
import requests

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
st.set_page_config(page_title="AquaMind AI", layout="wide")

API_KEY = "YOUR_OPENWEATHER_API_KEY"  # 🔴 Replace this

# ─────────────────────────────────────────────
# WEATHER API
# ─────────────────────────────────────────────
def get_weather(city="Madanapalle"):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        rain = data.get("rain", {}).get("1h", 0)

        rain_prob = min(100, int(humidity * 0.7 + rain * 10))
        return temp, humidity, rain_prob

    except:
        return 30, 60, 20  # fallback


# ─────────────────────────────────────────────
# CROP DATA
# ─────────────────────────────────────────────
CROP_DATA = {
    "Rice": {"method": "Flood", "water": "High"},
    "Wheat": {"method": "Sprinkler", "water": "Medium"},
    "Maize": {"method": "Drip", "water": "Medium"},
    "Sugarcane": {"method": "Furrow", "water": "High"},
    "Cotton": {"method": "Drip", "water": "Low"},
    "Tomato": {"method": "Drip", "water": "Medium"},
}

# ─────────────────────────────────────────────
# AI LOGIC
# ─────────────────────────────────────────────
def ai_decision(soil, rain):
    if soil < 40 and rain < 40:
        return "Irrigation ON"
    elif rain > 60:
        return "Irrigation OFF"
    else:
        return "Moderate Irrigation"

def yield_prediction(soil, temp, water, method, crop):
    score = 0

    if 40 <= soil <= 70: score += 30
    if 20 <= temp <= 35: score += 30
    if water > 50: score += 20
    if method == CROP_DATA[crop]["method"]: score += 20

    return min(score, 100)

def crop_advice(crop):
    data = CROP_DATA[crop]
    return f"Best method: {data['method']} | Water need: {data['water']}"

# ─────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────
def login():
    st.title("🌿 AquaMind AI Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if "@gmail.com" in email and len(password) >= 6:
            st.session_state["login"] = True
            st.rerun()
        else:
            st.error("Invalid login")

# ─────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────
def dashboard():

    st.title("🌿 AquaMind AI Dashboard")

    # Weather API
    temp_api, humidity, rain = get_weather()

    st.sidebar.header("Inputs")

    soil = st.sidebar.slider("Soil Moisture", 0, 100, 50)
    water = st.sidebar.slider("Water Level", 0, 100, 60)
    crop = st.sidebar.selectbox("Crop", list(CROP_DATA.keys()))
    method = st.sidebar.selectbox(
        "Irrigation Method",
        ["Drip", "Sprinkler", "Flood", "Furrow"]
    )

    # AI outputs
    decision = ai_decision(soil, rain)
    yield_score = yield_prediction(soil, temp_api, water, method, crop)
    advice = crop_advice(crop)

    # ── DISPLAY ──
    col1, col2, col3 = st.columns(3)

    col1.metric("🌡 Temperature", f"{temp_api} °C")
    col2.metric("💧 Soil Moisture", f"{soil}%")
    col3.metric("🌧 Rain Chance", f"{rain}%")

    st.subheader("🤖 AI Decision")
    st.success(decision)

    st.subheader("🌾 Crop Intelligence")
    st.info(advice)

    st.subheader("📊 Yield Prediction")
    st.progress(yield_score / 100)
    st.write(f"Estimated Yield Efficiency: **{yield_score}%**")

    # Chart
    df = pd.DataFrame({
        "Day": ["1","2","3","4","5"],
        "Moisture": np.random.randint(30, 80, 5)
    })
    st.line_chart(df.set_index("Day"))

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if "login" not in st.session_state:
    st.session_state["login"] = False

if st.session_state["login"]:
    dashboard()
else:
    login()
