import streamlit as st
import random
import numpy as np
import pandas as pd
import re
import requests

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SMART AI IRRIGATION SYSTEM",
    page_icon="🌿",
    layout="wide"
)

# ─────────────────────────────────────────────
# WEATHER API
# ─────────────────────────────────────────────
API_KEY = "YOUR_API_KEY_HERE"

def get_weather(lat=13.6, lon=79.4):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    try:
        res = requests.get(url)
        data = res.json()

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        rain = data.get("rain", {}).get("1h", 0)

        rain_prob = min(100, int(rain * 20 + humidity * 0.3))

        return temp, humidity, rain_prob
    except:
        return 30, 50, 20

# ─────────────────────────────────────────────
# AI LOGIC
# ─────────────────────────────────────────────
CROP_BEST_METHOD = {
    "Rice": "Flood", "Wheat": "Sprinkler", "Maize": "Drip",
    "Sugarcane": "Furrow", "Cotton": "Drip", "Tomato": "Drip"
}

def ai_decision(soil, rain):
    if soil < 40 and rain < 40:
        return "Irrigation ON"
    elif rain > 60:
        return "Irrigation OFF"
    else:
        return "Moderate Irrigation"

def predict_yield(crop, soil, temp, water):
    score = 0

    if soil > 60: score += 30
    elif soil > 40: score += 20
    else: score += 10

    if 20 <= temp <= 32: score += 30
    elif temp <= 38: score += 20
    else: score += 10

    if water > 70: score += 30
    elif water > 50: score += 20
    else: score += 10

    if crop in ["Rice", "Sugarcane"]:
        score += 10

    yield_percent = min(100, score)

    if yield_percent > 80:
        status = "High Yield Expected"
    elif yield_percent > 60:
        status = "Moderate Yield"
    else:
        status = "Low Yield Risk"

    return yield_percent, status

# ─────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────
def login():
    st.title("🌿 SMART AI IRRIGATION SYSTEM")
    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if "@gmail.com" in email and len(password) >= 6:
            st.session_state["logged_in"] = True
            st.rerun()
        else:
            st.error("Invalid login")

# ─────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────
def dashboard():

    # Real weather
    temp, humidity, rain = get_weather()

    soil = st.slider("Soil Moisture (%)", 0, 100, 50)
    water = st.slider("Water Availability (%)", 0, 100, 60)
    crop = st.selectbox("Crop", list(CROP_BEST_METHOD.keys()))

    st.title("🌿 SMART AI IRRIGATION SYSTEM")

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Soil Moisture", f"{soil}%")
    col2.metric("Temperature", f"{temp}°C")
    col3.metric("Rain Probability", f"{rain}%")
    col4.metric("Humidity", f"{humidity}%")

    # AI Decision
    decision = ai_decision(soil, rain)
    st.subheader("🤖 AI Irrigation Decision")
    st.success(decision)

    # Yield Prediction
    yield_percent, status = predict_yield(crop, soil, temp, water)

    st.subheader("📊 Yield Prediction")
    st.write(f"Expected Yield: {yield_percent}%")
    st.write(f"Status: {status}")

    # Chart
    df = pd.DataFrame({
        "Day": ["Mon","Tue","Wed","Thu","Fri"],
        "Moisture": [random.randint(20,80) for _ in range(5)]
    })
    st.line_chart(df.set_index("Day"))

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    dashboard()
else:
    login()
