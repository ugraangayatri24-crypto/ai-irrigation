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
    page_title="AquaMind AI – Smart Irrigation",
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

    /* ── Root reset ── */
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

    .stApp {
        background: linear-gradient(135deg, #0b3d2e 0%, #0d4f3c 30%, #083a5c 70%, #051e3a 100%);
        min-height: 100vh;
    }

    /* ── Hide Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

    /* ── Glass card ── */
    .glass {
        background: rgba(255,255,255,0.07);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border: 1px solid rgba(255,255,255,0.13);
        border-radius: 20px;
        padding: 1.4rem 1.6rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.28);
        transition: transform .2s ease, box-shadow .2s ease;
        color: #e8f5e9;
    }
    .glass:hover { transform: translateY(-3px); box-shadow: 0 14px 40px rgba(0,0,0,0.38); }

    /* ── Metric card ── */
    .metric-card {
        background: rgba(255,255,255,0.07);
        backdrop-filter: blur(18px);
        border: 1px solid rgba(255,255,255,0.13);
        border-radius: 20px;
        padding: 1.3rem 1.4rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.25);
        transition: transform .2s ease;
    }
    .metric-card:hover { transform: translateY(-4px); }
    .metric-label { font-size: 0.78rem; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; color: rgba(200,230,200,0.75); margin-bottom: 0.4rem; }
    .metric-value { font-family: 'Syne', sans-serif; font-size: 2.4rem; font-weight: 800; line-height: 1; }
    .metric-unit  { font-size: 0.82rem; color: rgba(200,230,200,0.65); margin-top: 0.25rem; }
    .metric-icon  { font-size: 1.6rem; margin-bottom: 0.5rem; }

    /* ── Section title ── */
    .sec-title {
        font-family: 'Syne', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #80cfa9;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* ── Status badge ── */
    .badge {
        display: inline-block;
        padding: 0.45rem 1.1rem;
        border-radius: 50px;
        font-family: 'Syne', sans-serif;
        font-size: 0.95rem;
        font-weight: 700;
        letter-spacing: 0.04em;
    }
    .badge-on   { background: rgba(0,200,120,0.22); border: 1.5px solid #00c878; color: #00c878; }
    .badge-off  { background: rgba(255,100,100,0.18); border: 1.5px solid #ff6464; color: #ff6464; }
    .badge-mod  { background: rgba(255,190,50,0.18); border: 1.5px solid #ffbe32; color: #ffbe32; }

    /* ── Sensor pill ── */
    .sensor-pill {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 14px;
        padding: 0.9rem 1rem;
        text-align: center;
        color: #e0f0ea;
    }
    .sensor-name  { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.07em; color: rgba(200,230,200,0.65); }
    .sensor-value { font-family: 'Syne', sans-serif; font-size: 1.4rem; font-weight: 700; }
    .sensor-status { font-size: 0.7rem; margin-top: 0.2rem; }
    .sensor-ok   { color: #00c878; }
    .sensor-warn { color: #ffbe32; }

    /* ── Warning box ── */
    .warn-box {
        background: rgba(255,180,50,0.12);
        border: 1px solid rgba(255,180,50,0.4);
        border-radius: 14px;
        padding: 0.8rem 1.1rem;
        color: #ffd27a;
        font-size: 0.88rem;
    }

    /* ── Explanation box ── */
    .explain-row {
        display: flex; align-items: flex-start; gap: 0.7rem;
        padding: 0.55rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        color: #d4edda;
        font-size: 0.88rem;
    }
    .explain-row:last-child { border-bottom: none; }
    .explain-icon { font-size: 1.1rem; min-width: 1.4rem; }
    .explain-text b { color: #80cfa9; }

    /* ── Login page ── */
    .login-wrap {
        max-width: 400px;
        margin: 3rem auto;
        background: rgba(255,255,255,0.07);
        backdrop-filter: blur(24px);
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 28px;
        padding: 2.6rem 2.4rem 2.2rem;
        box-shadow: 0 24px 60px rgba(0,0,0,0.4);
    }
    .login-logo { text-align: center; font-size: 2.8rem; margin-bottom: 0.3rem; }
    .login-title {
        text-align: center;
        font-family: 'Syne', sans-serif;
        font-size: 1.6rem; font-weight: 800;
        color: #e8f5e9; margin-bottom: 0.2rem;
    }
    .login-sub { text-align: center; color: rgba(200,230,200,0.65); font-size: 0.88rem; margin-bottom: 1.8rem; }

    .social-btn {
        width: 100%; padding: 0.65rem;
        border-radius: 12px; border: 1px solid rgba(255,255,255,0.18);
        background: rgba(255,255,255,0.08); color: #e8f5e9;
        font-family: 'DM Sans', sans-serif; font-size: 0.9rem;
        cursor: pointer; transition: background .2s;
        display: flex; align-items: center; justify-content: center; gap: 0.5rem;
        margin-bottom: 0.6rem;
    }
    .social-btn:hover { background: rgba(255,255,255,0.14); }

    .divider {
        display: flex; align-items: center; gap: 0.8rem;
        color: rgba(200,230,200,0.45); font-size: 0.8rem;
        margin: 1rem 0;
    }
    .divider::before, .divider::after {
        content: ''; flex: 1;
        height: 1px; background: rgba(255,255,255,0.12);
    }

    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.09) !important;
        border: 1px solid rgba(255,255,255,0.18) !important;
        border-radius: 12px !important;
        color: #e8f5e9 !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #00c878 !important;
        box-shadow: 0 0 0 2px rgba(0,200,120,0.2) !important;
    }
    .stTextInput label { color: rgba(200,230,200,0.8) !important; font-size: 0.85rem !important; }

    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #00c878, #00a86b) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 12px !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        padding: 0.65rem !important;
        letter-spacing: 0.04em !important;
        transition: opacity .2s !important;
    }
    .stButton > button:hover { opacity: 0.88 !important; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(8,30,50,0.82) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.08) !important;
    }
    [data-testid="stSidebar"] * { color: #d4edda !important; }
    [data-testid="stSidebar"] .stSlider > div > div > div { background: #00c878 !important; }
    [data-testid="stSidebar"] label { font-size: 0.83rem !important; }

    /* Charts */
    .stPlotlyChart { border-radius: 16px; overflow: hidden; }

    /* Map */
    .stDeckGlJsonChart, .element-container iframe { border-radius: 16px !important; }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(0,200,120,0.35); border-radius: 3px; }
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
    if rain > 60:   return "After 2 Days (rain expected)"
    if soil < 30:   return "Immediate"
    return "After 1 Day"

def moisture_color(v):
    if v < 30: return "#ff6464"
    if v < 60: return "#ffbe32"
    return "#00c878"


# ─────────────────────────────────────────────
# LOGIN PAGE
# ─────────────────────────────────────────────
def login():
    inject_css()

    st.markdown("""
    <div class="login-wrap">
        <div class="login-logo">🌿</div>
        <div class="login-title">AquaMind AI</div>
        <div class="login-sub">Smart Irrigation Intelligence Platform</div>
        <button class="social-btn">🔵 &nbsp; Continue with Google</button>
        <button class="social-btn">⬛ &nbsp; Continue with Apple</button>
        <div class="divider">or sign in with email</div>
    </div>
    """, unsafe_allow_html=True)

    # Center the form
    _, col, _ = st.columns([1, 2, 1])
    with col:
        email = st.text_input("Email", placeholder="you@gmail.com", key="login_email")
        password = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass")
        login_btn = st.button("Sign In →")

        if login_btn:
            gmail_re = r'^[a-zA-Z0-9_.+-]+@gmail\.com$'
            if not re.match(gmail_re, email):
                st.error("⚠️ Please enter a valid Gmail address (e.g., user@gmail.com)")
            elif len(password) < 6:
                st.error("⚠️ Password must be at least 6 characters.")
            else:
                st.session_state["logged_in"] = True
                st.session_state["user_email"] = email
                st.rerun()

        st.markdown("""
        <div style="text-align:center; margin-top:1rem; color:rgba(200,230,200,0.45); font-size:0.78rem;">
        Demo: any valid Gmail + any 6+ char password
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────
def dashboard():
    inject_css()

    # ── Live sensor sim (refresh every render) ──
    live_soil  = random.randint(25, 85)
    live_temp  = round(random.uniform(22, 38), 1)
    live_water = random.randint(40, 95)
    live_rain  = random.randint(5, 80)

    # ── Sidebar ──
    with st.sidebar:
        st.markdown('<div class="sec-title">⚙️ Farm Parameters</div>', unsafe_allow_html=True)
        soil   = st.slider("Soil Moisture (%)", 0, 100, live_soil)
        water  = st.slider("Water Availability (%)", 0, 100, live_water)
        temp   = st.slider("Temperature (°C)", 10, 45, int(live_temp))
        crop   = st.selectbox("Crop Type", list(CROP_BEST_METHOD.keys()))
        method = st.selectbox("Irrigation Method", ["Drip","Sprinkler","Flood","Furrow","Basin","Manual","Sub-surface"])

        st.markdown("---")
        st.markdown(f'<div style="color:rgba(200,230,200,0.55); font-size:0.78rem;">Signed in as<br><b style="color:#80cfa9">{st.session_state.get("user_email","")}</b></div>', unsafe_allow_html=True)
        if st.button("Sign Out"):
            st.session_state["logged_in"] = False
            st.rerun()

    # ── Header ──
    st.markdown("""
    <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1.6rem;">
        <span style="font-size:2.2rem;">🌿</span>
        <div>
            <div style="font-family:'Syne',sans-serif;font-size:1.65rem;font-weight:800;color:#e8f5e9;line-height:1;">AquaMind AI</div>
            <div style="color:rgba(200,230,200,0.55);font-size:0.82rem;letter-spacing:0.06em;">SMART IRRIGATION DASHBOARD</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Farm Status Metrics ──
    st.markdown('<div class="sec-title">📊 Farm Status</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        (c1, "💧", "Soil Moisture", f"{soil}", "%", moisture_color(soil)),
        (c2, "🌡️", "Temperature",  f"{temp}", "°C", "#64b5f6"),
        (c3, "🪣", "Water Level",  f"{water}", "%", "#4fc3f7"),
        (c4, "🌧️", "Rain Probability", f"{live_rain}", "%", "#ce93d8"),
    ]
    for col, icon, label, val, unit, color in metrics:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">{icon}</div>
                <div class="metric-label">{label}</div>
                <div class="metric-value" style="color:{color};">{val}</div>
                <div class="metric-unit">{unit}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 2: AI Decision + Crop Intelligence ──
    left, right = st.columns([1.1, 0.9])

    with left:
        decision, mode = ai_decision(soil, live_rain)
        badge_cls = {"on":"badge-on","off":"badge-off","mod":"badge-mod"}[mode]
        best = CROP_BEST_METHOD[crop]
        sched = schedule(live_rain, soil)

        st.markdown(f"""
        <div class="glass">
            <div class="sec-title">🤖 AI Decision Engine</div>
            <div style="margin-bottom:1rem;">
                <span class="badge {badge_cls}">{decision}</span>
            </div>
            <div class="explain-row">
                <span class="explain-icon">💧</span>
                <span class="explain-text"><b>Soil Moisture:</b> {soil}% — {"Low – needs water" if soil<40 else "Adequate"}</span>
            </div>
            <div class="explain-row">
                <span class="explain-icon">🌧️</span>
                <span class="explain-text"><b>Rain Probability:</b> {live_rain}% — {"High – skip irrigation" if live_rain>60 else "Low – proceed"}</span>
            </div>
            <div class="explain-row">
                <span class="explain-icon">🌡️</span>
                <span class="explain-text"><b>Temperature:</b> {temp}°C — {"Hot – increase frequency" if temp>35 else "Moderate"}</span>
            </div>
            <div class="explain-row">
                <span class="explain-icon">🌾</span>
                <span class="explain-text"><b>Crop:</b> {crop} – optimal method is <b>{best}</b></span>
            </div>
            <div class="explain-row">
                <span class="explain-icon">🗓️</span>
                <span class="explain-text"><b>Next Irrigation:</b> {sched}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown(f"""
        <div class="glass" style="height:100%;">
            <div class="sec-title">🌾 Crop Intelligence</div>
            <div style="margin-bottom:0.8rem; color:#e0f0ea; font-size:0.88rem;">
                Selected crop: <b style="color:#80cfa9">{crop}</b>
            </div>
            <div class="explain-row">
                <span class="explain-icon">✅</span>
                <span class="explain-text">Recommended method: <b>{best}</b></span>
            </div>
            <div class="explain-row">
                <span class="explain-icon">🔧</span>
                <span class="explain-text">Your selection: <b>{method}</b></span>
            </div>
        """, unsafe_allow_html=True)

        if method != best:
            st.markdown(f"""
            <div class="warn-box" style="margin-top:0.8rem;">
                ⚠️ <b>Sub-optimal choice!</b> For {crop}, <b>{best}</b> irrigation delivers up to 30% better yield efficiency. Consider switching.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:rgba(0,200,120,0.1);border:1px solid rgba(0,200,120,0.35);border-radius:12px;padding:0.7rem 1rem;color:#80cfa9;margin-top:0.8rem;font-size:0.87rem;">
                ✅ <b>Excellent!</b> Your irrigation method matches the optimal recommendation for this crop.
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 3: Charts ──
    chart_l, chart_r = st.columns(2)

    with chart_l:
        st.markdown('<div class="sec-title">📈 Soil Moisture Trend (5 Days)</div>', unsafe_allow_html=True)
        days = ["Day 1","Day 2","Day 3","Day 4","Day 5"]
        vals = [random.randint(20,90) for _ in range(5)]
        vals[-1] = soil
        df_trend = pd.DataFrame({"Day": days, "Soil Moisture (%)": vals})
        st.line_chart(df_trend.set_index("Day"), color="#00c878", height=220)

    with chart_r:
        st.markdown('<div class="sec-title">💦 Water Usage (Litres)</div>', unsafe_allow_html=True)
        used  = random.randint(200, 800)
        saved = random.randint(100, 500)
        df_water = pd.DataFrame({"Category": ["Water Used","Water Saved"], "Litres": [used, saved]})
        st.bar_chart(df_water.set_index("Category"), color="#00a86b", height=220)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 4: Sensors + Map ──
    sens_col, map_col = st.columns([1, 1.4])

    with sens_col:
        st.markdown('<div class="sec-title">📡 Live Sensor Feed</div>', unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        sensor_data = [
            (s1, "Soil Sensor", f"{soil}%",  "sensor-ok" if soil>=30 else "sensor-warn", "● Active" if soil>=30 else "⚠ Low"),
            (s2, "Temp Sensor", f"{temp}°C", "sensor-ok" if temp<=35 else "sensor-warn", "● Normal" if temp<=35 else "⚠ High"),
            (s3, "Water Sensor",f"{water}%", "sensor-ok" if water>=40 else "sensor-warn", "● OK"     if water>=40 else "⚠ Low"),
        ]
        for col, name, val, cls, status in sensor_data:
            with col:
                st.markdown(f"""
                <div class="sensor-pill">
                    <div class="sensor-name">{name}</div>
                    <div class="sensor-value">{val}</div>
                    <div class="sensor-status {cls}">{status}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Irrigation Schedule box ──
        st.markdown(f"""
        <div class="glass">
            <div class="sec-title">🗓️ Irrigation Schedule</div>
            <div style="font-size:0.88rem;color:#d4edda;">
                <div class="explain-row"><span class="explain-icon">⏰</span><span class="explain-text">Next run: <b>{sched}</b></span></div>
                <div class="explain-row"><span class="explain-icon">🌱</span><span class="explain-text">Crop water need: <b>{"High" if soil<30 else "Medium" if soil<60 else "Low"}</b></span></div>
                <div class="explain-row"><span class="explain-icon">🌊</span><span class="explain-text">Estimated usage: <b>{used} L</b></span></div>
                <div class="explain-row"><span class="explain-icon">♻️</span><span class="explain-text">Projected savings: <b>{saved} L</b></span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with map_col:
        st.markdown('<div class="sec-title">🗺️ Farm Location</div>', unsafe_allow_html=True)
        map_df = pd.DataFrame({
            "lat": [13.6 + random.uniform(-0.003, 0.003) for _ in range(8)],
            "lon": [79.4 + random.uniform(-0.003, 0.003) for _ in range(8)],
        })
        st.map(map_df, zoom=13, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Footer ──
    st.markdown("""
    <div style="text-align:center;color:rgba(200,230,200,0.35);font-size:0.75rem;letter-spacing:0.05em;padding-top:1rem;border-top:1px solid rgba(255,255,255,0.06);">
    AquaMind AI · Smart Irrigation System · Powered by AI · Built with Streamlit
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    dashboard()
else:
    login()
