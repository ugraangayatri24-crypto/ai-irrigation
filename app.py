import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="AI Irrigation System", layout="centered")

st.title("🌱 Smart AI Irrigation System (Final Advanced)")
st.write("AI + Weather + Crop-based Intelligent Irrigation System")

# INPUTS
st.sidebar.header("Input Parameters")

soil = st.sidebar.slider("Soil Moisture (%)", 0, 100, 40)
water = st.sidebar.slider("Water Availability (%)", 0, 100, 60)
temperature = st.sidebar.slider("Temperature (°C)", 10, 45, 30)

# CROPS (12+)
crop_list = [
    "Rice", "Wheat", "Maize", "Sugarcane", "Cotton",
    "Tomato", "Potato", "Onion", "Mango",
    "Banana", "Grapes", "Chilli"
]
crop = st.sidebar.selectbox("Crop", crop_list)

# IRRIGATION METHODS (12)
methods = [
    "Drip Irrigation", "Sprinkler Irrigation", "Surface Irrigation",
    "Furrow Irrigation", "Basin Irrigation", "Border Irrigation",
    "Subsurface Irrigation", "Manual Irrigation",
    "Center Pivot Irrigation", "Micro Irrigation",
    "Flood Irrigation", "Rain Gun Irrigation"
]
method = st.sidebar.selectbox("Irrigation Method", methods)

# WEATHER (SIMULATED ADVANCED)
weather = st.sidebar.selectbox("Weather", ["Sunny", "Cloudy", "Rainy"])

base_rain = random.randint(0, 100)

if weather == "Rainy":
    rain_probability = min(100, base_rain + 40)
elif weather == "Cloudy":
    rain_probability = base_rain + 10
else:
    rain_probability = max(0, base_rain - 20)

st.subheader("🌧 Rain Prediction")
st.write(f"Chance of Rain: {rain_probability}%")

# CROP WATER REQUIREMENT
crop_water = {
    "Rice": 80, "Wheat": 50, "Maize": 60, "Sugarcane": 90,
    "Cotton": 70, "Tomato": 65, "Potato": 55, "Onion": 50,
    "Mango": 40, "Banana": 85, "Grapes": 60, "Chilli": 55
}

required_water = crop_water[crop]

# AI DECISION
if soil < required_water and rain_probability < 40:
    decision = "Irrigation ON"
    reason = "Crop needs water + low rain"
elif rain_probability >= 60:
    decision = "Irrigation OFF"
    reason = "Rain expected"
else:
    decision = "Moderate Irrigation"
    reason = "Balanced condition"

# OUTPUT
st.subheader("🤖 AI Decision")
st.success(decision)
st.write("Reason:", reason)
st.write("Selected Method:", method)

# SCHEDULING
if rain_probability > 60:
    schedule = "Next irrigation after 2 days"
elif soil < 30:
    schedule = "Immediate irrigation required"
else:
    schedule = "Irrigate after 1 day"

st.subheader("⏱ Irrigation Schedule")
st.write(schedule)

# ALERT
if water < 30:
    st.error("⚠ Low Water Availability")

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

# WATER SAVING CALCULATION (NEW)
water_saved = max(0, 100 - required_water)

st.subheader("💧 Water Saving Estimate")
st.write(f"{water_saved}% water optimized")

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
    st.info("Water saved due to rainfall or sufficient moisture")
else:
    st.info("Controlled irrigation ensures optimal growth")
