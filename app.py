import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="AI Irrigation System", layout="wide")

# ---------- UI STYLE ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #d4fc79, #96e6a1);
}
h1, h2, h3 {
    color: #0a3d62;
}
</style>
""", unsafe_allow_html=True)

# ---------- LOGIN STATE ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------- LOGIN ----------
def login():
    st.title("🔐 Smart Irrigation Login")

    email = st.text_input("Enter Gmail")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if "@gmail.com" in email and len(password) > 3:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Enter valid Gmail")

# ---------- DASHBOARD ----------
def dashboard():

    st.title("🌱 AI Smart Irrigation System")

    # TOP METRICS
    col1, col2, col3 = st.columns(3)
    col1.metric("💧 Water Level", f"{random.randint(50,90)}%")
    col2.metric("🌡 Temperature", f"{random.randint(25,40)}°C")
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

    # ---------- AI SUGGESTION ----------
    best_method = {
        "Rice": "Flood Irrigation",
        "Wheat": "Sprinkler Irrigation",
        "Maize": "Drip Irrigation",
        "Sugarcane": "Furrow Irrigation",
        "Cotton": "Drip Irrigation",
        "Tomato": "Drip Irrigation",
        "Potato": "Sprinkler Irrigation",
        "Onion": "Drip Irrigation",
        "Mango": "Basin Irrigation",
        "Banana": "Drip Irrigation",
        "Grapes": "Drip Irrigation",
        "Chilli": "Drip Irrigation"
    }

    suggested = best_method[crop]

    # ---------- RAIN ----------
    rain_probability = random.randint(0, 100)

    st.subheader("🌧 Rain Prediction")
    st.write(f"{rain_probability}% chance of rain")

    # ---------- AI DECISION ----------
    if soil < 40 and rain_probability < 40:
        decision = "🟢 Irrigation ON"
    elif rain_probability > 60:
        decision = "🔴 Irrigation OFF"
    else:
        decision = "🟡 Moderate Irrigation"

    st.subheader("🤖 AI Decision")
    st.success(decision)

    # ---------- CROP INTELLIGENCE ----------
    st.subheader("🌱 Crop Intelligence")
    st.info(f"Best method for {crop}: {suggested}")

    if method != suggested:
        st.warning("⚠ Selected method is not optimal")

    # ---------- SCHEDULE ----------
    if rain_probability > 60:
        schedule = "After 2 days"
    elif soil < 30:
        schedule = "Immediate"
    else:
        schedule = "After 1 day"

    st.subheader("⏱ Irrigation Schedule")
    st.success(schedule)

    # ---------- GRAPH ----------
    st.subheader("📈 Soil Moisture Trend")

    data = pd.DataFrame({
        "Day": ["D1","D2","D3","D4","D5"],
        "Moisture": [soil-10, soil-5, soil, soil+5, soil+10]
    })

    st.line_chart(data.set_index("Day"))

    # ---------- SENSOR SIMULATION ----------
    st.subheader("📡 Sensor Data")

    col1, col2, col3 = st.columns(3)
    col1.metric("Soil Sensor", f"{random.randint(20,80)}%")
    col2.metric("Temp Sensor", f"{random.randint(25,40)}°C")
    col3.metric("Water Sensor", f"{random.randint(30,90)}%")

    # ---------- MAP ----------
    st.subheader("🌍 Farm Location")

    location = pd.DataFrame({
        'lat': [13.6],
        'lon': [79.4]
    })

    st.map(location)

    # ---------- WATER ANALYTICS ----------
    st.subheader("📊 Water Usage Analytics")

    used = random.randint(40, 80)
    saved = 100 - used

    chart = pd.DataFrame({
        "Type": ["Used Water", "Saved Water"],
        "Value": [used, saved]
    })

    st.bar_chart(chart.set_index("Type"))

    # ---------- AI EXPLANATION ----------
    st.subheader("🧠 AI Explanation")

    st.write(f"""
    Soil Moisture: {soil}%
    Rain Probability: {rain_probability}%
    Crop: {crop}

    Decision: {decision}
    Recommended Method: {suggested}
    """)

# ---------- ROUTING ----------
if not st.session_state.logged_in:
    login()
else:
    dashboard()
