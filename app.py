import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="AI Irrigation System", layout="centered")

st.title("🌱 Smart AI Irrigation System (Advanced)")
st.write("AI-based irrigation with prediction & visualization")

# INPUTS
st.sidebar.header("Input Parameters")

soil = st.sidebar.slider("Soil Moisture (%)", 0, 100, 40)
water = st.sidebar.slider("Water Availability (%)", 0, 100, 60)
temperature = st.sidebar.slider("Temperature (°C)", 10, 45, 30)
weather = st.sidebar.selectbox("Weather", ["Sunny", "Cloudy", "Rainy"])
crop = st.sidebar.selectbox("Crop", ["Rice", "Wheat", "Maize"])

# ADVANCED RAIN LOGIC
base_rain = random.randint(0, 100)

if weather == "Rainy":
    rain_probability = min(100, base_rain + 40)
elif weather == "Cloudy":
    rain_probability = base_rain + 10
else:
    rain_probability = max(0, base_rain - 20)

st.subheader("🌧 Rain Prediction")
st.write(f"Chance of Rain: {rain_probability}%")

# AI DECISION
if soil < 35 and rain_probability < 40:
    decision = "Irrigation ON"
    water_needed = "High"
    reason = "Dry soil + low rain"
elif rain_probability >= 60:
    decision = "Irrigation OFF"
    water_needed = "None"
    reason = "Rain expected"
elif soil > 60:
    decision = "Irrigation OFF"
    water_needed = "None"
    reason = "Soil already wet"
else:
    decision = "Moderate Irrigation"
    water_needed = "Medium"
    reason = "Balanced condition"

# ALERT
if water < 30:
    st.error("⚠ Low Water Availability")

# OUTPUT
st.subheader("🤖 AI Decision")
st.success(decision)

st.write("💧 Water Required:", water_needed)
st.write("🧠 Reason:", reason)

# GRAPH
st.subheader("📈 Soil Moisture Trend")

data = pd.DataFrame({
    "Day": ["Day1", "Day2", "Day3", "Day4", "Day5"],
    "Moisture": [
        max(0, soil - 10),
        soil - 5,
        soil,
        soil + 5,
        min(100, soil + 10)
    ]
})

st.line_chart(data.set_index("Day"))

# EFFICIENCY
score = 100 - abs(50 - soil)

st.subheader("📊 Efficiency Score")
st.progress(score)
st.write(f"{score}% Efficient")

# AI INSIGHT
st.subheader("🧠 AI Insight")

if decision == "Irrigation ON":
    st.info("System recommends watering crops now")
elif decision == "Irrigation OFF":
    st.info("Water saved due to sufficient moisture or rainfall")
else:
    st.info("Controlled irrigation for optimal growth")
