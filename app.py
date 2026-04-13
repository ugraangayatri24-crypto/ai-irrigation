import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="AI Irrigation System", layout="centered")

# ---------------- LOGIN STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- LOGIN FUNCTION ----------------
def login():
    st.title("🔐 Smart Irrigation Login")

    username = st.text_input("Email / Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username.strip() == "admin" and password.strip() == "1234":
            st.session_state.logged_in = True
            st.rerun()   # IMPORTANT FIX
        else:
            st.error("Invalid Credentials")

# ---------------- DASHBOARD ----------------
def dashboard():

    st.title("🌱 AI Smart Irrigation Dashboard")

    # TOP CARDS
    col1, col2, col3 = st.columns(3)
    col1.metric("💧 Water Level", "65%")
    col2.metric("🌡 Temperature", "32°C")
    col3.metric("🌧 Rain Chance", f"{random.randint(20,90)}%")

    st.divider()

    # SIDEBAR INPUTS
    st.sidebar.header("Input Parameters")

    soil = st.sidebar.slider("Soil Moisture (%)", 0, 100, 40)
    water = st.sidebar.slider("Water Availability (%)", 0, 100, 60)
    temperature = st.sidebar.slider("Temperature (°C)", 10, 45, 30)

    crop_list = [
        "Rice", "Wheat", "Maize", "Sugarcane", "Cotton",
        "Tomato", "Potato", "Onion", "Mango",
        "Banana", "Grapes", "Chilli"
    ]
    crop = st.sidebar.selectbox("Crop", crop_list)

    irrigation_methods = [
        "Drip Irrigation", "Sprinkler Irrigation", "Surface Irrigation",
        "Furrow Irrigation", "Basin Irrigation", "Border Irrigation",
        "Subsurface Irrigation", "Manual Irrigation",
        "Center Pivot Irrigation", "Micro Irrigation",
        "Flood Irrigation", "Rain Gun Irrigation"
    ]
    method = st.sidebar.selectbox("Irrigation Method", irrigation_methods)

    # RAIN PREDICTION
    rain_probability = random.randint(0, 100)

    st.subheader("🌧 Rain Prediction")
    st.write(f"{rain_probability}% chance of rain")

    # CROP WATER REQUIREMENT
    crop_water = {
        "Rice": 80, "Wheat": 50, "Maize": 60, "Sugarcane": 90,
        "Cotton": 70, "Tomato": 65, "Potato": 55, "Onion": 50,
        "Mango": 40, "Banana": 85, "Grapes": 60, "Chilli": 55
    }

    required = crop_water[crop]

    # AI DECISION
    if soil < required and rain_probability < 40:
        decision = "🟢 Irrigation ON"
        reason = "Low soil moisture + low rain"
    elif rain_probability > 60:
        decision = "🔴 Irrigation OFF"
        reason = "Rain expected"
    else:
        decision = "🟡 Moderate Irrigation"
        reason = "Balanced condition"

    # DISPLAY
    st.subheader("🤖 AI Decision")
    st.success(decision)

    st.write("🧠 Reason:", reason)
    st.write("🌱 Crop:", crop)
    st.write("💧 Method:", method)

    # SCHEDULING
    if rain_probability > 60:
        schedule = "Next irrigation after 2 days"
    elif soil < 30:
        schedule = "Immediate irrigation required"
    else:
        schedule = "Irrigate after 1 day"

    st.subheader("⏱ Irrigation Schedule")
    st.info(schedule)

    # GRAPH
    st.subheader("📈 Soil Moisture Trend")

    data = pd.DataFrame({
        "Day": ["D1", "D2", "D3", "D4", "D5"],
        "Moisture": [
            max(0, soil - 10),
            soil - 5,
            soil,
            soil + 5,
            min(100, soil + 10)
        ]
    })

    st.line_chart(data.set_index("Day"))

    # WATER SAVING
    water_saved = max(0, 100 - required)

    st.subheader("💧 Water Saving Estimate")
    st.write(f"{water_saved}% water optimized")

    # EFFICIENCY
    score = 100 - abs(50 - soil)

    st.subheader("📊 Efficiency Score")
    st.progress(score)
    st.write(f"{score}% Efficient")

    # ALERTS
    st.subheader("🚨 Active Alerts")

    if water < 30:
        st.error("⚠ Low Water Level")

    if temperature > 38:
        st.warning("🔥 High Temperature Risk")

    if rain_probability > 80:
        st.info("🌧 Heavy Rain Expected")

# ---------------- ROUTING ----------------
if not st.session_state.logged_in:
    login()
else:
    dashboard()
