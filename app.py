import streamlit as st
import random
import numpy as np
import pandas as pd
import re
import time

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SMART AI IRRIGATION SYSTEM",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

    .stApp {
        background: linear-gradient(135deg, #0b3d2e 0%, #0d4f3c 30%, #083a5c 70%, #051e3a 100%);
        min-height: 100vh;
    }

    #MainMenu, footer, header { visibility: hidden; }

    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

    .glass {
        background: rgba(255,255,255,0.07);
        backdrop-filter: blur(18px);
        border: 1px solid rgba(255,255,255,0.13);
        border-radius: 20px;
        padding: 1.4rem 1.6rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.28);
        color: #e8f5e9;
    }

    .sec-title {
        font-family: 'Syne', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #80cfa9;
        margin-bottom: 0.8rem;
    }
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────
CROP_BEST_METHOD = {
    "Rice": "Flood", "Wheat": "Sprinkler", "Maize": "Drip",
    "Sugarcane": "Furrow", "Cotton": "Drip", "Tomato": "Drip",
    "Potato": "Sprinkler", "Onion": "Drip", "Mango": "Basin",
    "Banana": "Drip", "Grapes": "Drip", "Chilli": "Drip",
}

def ai_decision(soil, rain):
    if soil < 40 and rain < 40:
        return "Irrigation ON", "on"
    elif rain > 60:
        return "Irrigation OFF", "off"
    else:
        return "Moderate Irrigation", "mod"

def schedule(rain, soil):
    if rain > 60: return "After 2 Days"
    if soil < 30: return "Immediate"
    return "After 1 Day"


# ─────────────────────────────────────────────
# LOGIN PAGE
# ─────────────────────────────────────────────
def login():
    inject_css()

    st.markdown("""
    <div style="max-width:400px;margin:3rem auto;padding:2rem;border-radius:20px;
    background:rgba(255,255,255,0.07);text-align:center;">
        <h2>🌿 SMART AI IRRIGATION SYSTEM</h2>
        <p>Login to continue</p>
    </div>
    """, unsafe_allow_html=True)

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
    inject_css()

    soil = random.randint(20, 80)
    rain = random.randint(10, 80)
    temp = random.randint(20, 40)

    decision, _ = ai_decision(soil, rain)
    sched = schedule(rain, soil)

    st.markdown("""
    <h1 style="color:white;">🌿 SMART AI IRRIGATION SYSTEM</h1>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-title">📊 Farm Status</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Soil Moisture", f"{soil}%")
    col2.metric("Temperature", f"{temp}°C")
    col3.metric("Rain Chance", f"{rain}%")

    st.markdown('<div class="sec-title">🤖 AI Decision</div>', unsafe_allow_html=True)
    st.success(decision)

    st.markdown('<div class="sec-title">📅 Schedule</div>', unsafe_allow_html=True)
    st.info(sched)

    # Chart
    df = pd.DataFrame({
        "Day": ["Mon","Tue","Wed","Thu","Fri"],
        "Moisture": [random.randint(20,80) for _ in range(5)]
    })
    st.line_chart(df.set_index("Day"))

    # Map
    st.markdown('<div class="sec-title">🗺️ Location</div>', unsafe_allow_html=True)
    map_df = pd.DataFrame({
        "lat": [13.6 + random.random()/100],
        "lon": [79.4 + random.random()/100]
    })
    st.map(map_df)


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    dashboard()
else:
    login()
