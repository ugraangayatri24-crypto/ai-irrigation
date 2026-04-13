import streamlit as st
import random

st.set_page_config(page_title="AI Irrigation System", layout="centered")

st.title("🌱 Smart AI Irrigation System")
st.write("AI-based irrigation decision system with rain prediction")

# INPUTS
st.sidebar.header("Input Parameters")
soil = st.sidebar.slider("Soil Moisture (%)", 0, 100, 40)
water = st.sidebar.slider("Water Availability (%)", 0, 100, 60)
weather = st.sidebar.selectbox("Weather", ["Sunny", "Cloudy", "Rainy"])
crop = st.sidebar.selectbox("Crop", ["Rice", "Wheat", "Maize"])

# RAIN PREDICTION
rain_probability = random.randint(0, 100)

st.subheader("🌧 Rain Prediction")
st.write(f"Chance of Rain: {rain_probability}%")

# AI LOGIC
if soil < 35 and rain_probability < 40:
    decision = "Irrigation ON"
    reason = "Dry soil + low rain chance"
elif rain_probability >= 60:
    decision = "Irrigation OFF"
    reason = "Rain expected"
elif soil > 60:
    decision = "Irrigation OFF"
    reason = "Soil already wet"
else:
    decision = "Moderate Irrigation"
    reason = "Balanced condition"

# OUTPUT
st.subheader("🤖 AI Decision")
st.success(decision)
st.write("Reason:", reason)

# ALERT
if water < 30:
    st.error("⚠ Low Water Availability")

# SCORE
score = 100 - abs(50 - soil)
st.subheader("📊 Efficiency")
st.progress(score)
st.write(f"{score}% Efficient")
