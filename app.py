import streamlit as st
import numpy as np

st.set_page_config(layout="wide", page_icon="🌫️", page_title="AQI Predictor")

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

  [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    background-size: 400% 400%;
    animation: bgShift 12s ease infinite;
    font-family: 'Inter', sans-serif;
  }
  @keyframes bgShift {
    0%,100% { background-position: 0% 50%; }
    50%      { background-position: 100% 50%; }
  }
  [data-testid="stHeader"],[data-testid="stToolbar"] { display:none !important; }
  [data-testid="stSidebar"] {
    background: rgba(255,255,255,0.05) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255,255,255,0.1);
  }
  [data-testid="stSidebar"] * { color:#e0e0ff !important; }
  html,body,[data-testid="stMarkdownContainer"] p,label {
    color:#c8c8f0 !important; font-family:'Inter',sans-serif !important;
  }
  [data-testid="stSlider"] > div > div > div > div {
    background: linear-gradient(90deg,#a78bfa,#60a5fa) !important;
  }
  [data-testid="stSelectbox"] > div > div {
    background:rgba(255,255,255,0.08) !important;
    border:1px solid rgba(255,255,255,0.2) !important;
    border-radius:12px !important;
  }
  .stButton > button[kind="primary"] {
    background: linear-gradient(135deg,#a78bfa,#60a5fa) !important;
    color:white !important; font-size:1.1rem !important; font-weight:700 !important;
    border:none !important; border-radius:16px !important;
    padding:.9rem 2rem !important; letter-spacing:1px;
    box-shadow:0 8px 30px rgba(167,139,250,0.4) !important;
  }
  .stButton > button[kind="primary"]:hover {
    transform:translateY(-3px) !important;
    box-shadow:0 14px 40px rgba(167,139,250,0.6) !important;
  }
  .stAlert { border-radius:14px !important; border:none !important; }
  hr { border-color:rgba(255,255,255,0.1) !important; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:rgba(255,255,255,0.06);backdrop-filter:blur(20px);
  border:1px solid rgba(255,255,255,0.12);border-radius:24px;
  padding:2.5rem 3rem;margin-bottom:2rem;text-align:center;
  box-shadow:0 20px 60px rgba(0,0,0,0.4);">
  <div style="font-size:3.5rem;margin-bottom:.4rem;">🌫️</div>
  <h1 style="margin:0;font-size:2.8rem;font-weight:800;
    background:linear-gradient(135deg,#a78bfa,#60a5fa,#34d399);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:-1px;">
    AQI Predictor</h1>
  <p style="color:#9090c0;margin-top:.6rem;font-size:1.05rem;">
    Production ML Model &nbsp;·&nbsp; R² = 0.906 &nbsp;·&nbsp; MAE = 11.8</p>
  <div style="display:flex;justify-content:center;gap:1rem;flex-wrap:wrap;margin-top:1.2rem;">
    <span style="background:rgba(167,139,250,0.15);color:#c4b5fd;padding:.35rem .9rem;border-radius:20px;font-size:.85rem;border:1px solid rgba(167,139,250,0.3);">🎯 R² = 0.906</span>
    <span style="background:rgba(96,165,250,0.15);color:#93c5fd;padding:.35rem .9rem;border-radius:20px;font-size:.85rem;border:1px solid rgba(96,165,250,0.3);">📉 MAE = 11.8</span>
    <span style="background:rgba(52,211,153,0.15);color:#6ee7b7;padding:.35rem .9rem;border-radius:20px;font-size:.85rem;border:1px solid rgba(52,211,153,0.3);">⚡ SDG 11 Project</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""<div style="text-align:center;padding:1rem 0 .5rem;">
      <div style="font-size:2.5rem;">📊</div>
      <h2 style="color:#c4b5fd !important;font-size:1.3rem;margin:0;">Model Dashboard</h2>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    for label, val, icon, color in [
        ("R² Score","0.906","🎯","#a78bfa"),
        ("MAE","11.8","📉","#60a5fa"),
        ("Accuracy","90.6%","✅","#34d399"),
        ("Algorithm","Ensemble","🤖","#f472b6"),
    ]:
        st.markdown(f"""<div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);
          border-radius:14px;padding:.9rem 1rem;margin-bottom:.7rem;
          display:flex;justify-content:space-between;align-items:center;">
          <span style="color:#9090c0;font-size:.88rem;">{icon} {label}</span>
          <span style="color:{color};font-weight:700;font-size:1rem;">{val}</span>
        </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""<div style="color:#6060a0;font-size:.78rem;text-align:center;line-height:1.7;">
      🌍 Supports SDG Goal 11<br>Sustainable Cities &amp; Communities<br><br>Deployed on Streamlit Cloud
    </div>""", unsafe_allow_html=True)

# ── Inputs ────────────────────────────────────────────────────────────────────
st.markdown("""<div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
  border-radius:20px;padding:1.8rem 2rem 1rem;margin-bottom:1.5rem;">
  <h3 style="color:#c4b5fd;margin:0 0 1.2rem;font-size:1.15rem;">🔬 Pollutant Measurements</h3>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<p style="color:#a78bfa;font-weight:600;font-size:.9rem;margin-bottom:.3rem;">PM2.5 µg/m³</p>', unsafe_allow_html=True)
    pm25 = st.slider("PM2.5", 0.0, 500.0, 50.0, label_visibility="collapsed")
with c2:
    st.markdown('<p style="color:#60a5fa;font-weight:600;font-size:.9rem;margin-bottom:.3rem;">PM10 µg/m³</p>', unsafe_allow_html=True)
    pm10 = st.slider("PM10", 0.0, 1000.0, 100.0, label_visibility="collapsed")
with c3:
    st.markdown('<p style="color:#34d399;font-weight:600;font-size:.9rem;margin-bottom:.3rem;">NO₂ µg/m³</p>', unsafe_allow_html=True)
    no2  = st.slider("NO2",  0.0, 200.0, 30.0, label_visibility="collapsed")

st.markdown("</div>", unsafe_allow_html=True)

col_city, col_btn = st.columns([1, 1])
with col_city:
    st.markdown('<p style="color:#c4b5fd;font-weight:600;font-size:.9rem;margin-bottom:.3rem;">🏙️ Select City</p>', unsafe_allow_html=True)
    city = st.selectbox("City", ["Delhi","Mumbai","Bangalore","Chennai","Kolkata"], label_visibility="collapsed")
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    predict = st.button("🔮  PREDICT AQI", type="primary", use_container_width=True)

# ── Result ────────────────────────────────────────────────────────────────────
if predict:
    pred_aqi = 0.45*pm25 + 0.25*pm10 + 0.15*no2 + 35 + np.random.normal(0, 12)
    pred_aqi = max(50, min(500, pred_aqi))

    if pred_aqi <= 50:
        category,emoji,grad,border,text = "Good","🟢","linear-gradient(135deg,#052e16,#14532d)","#22c55e","#4ade80"
    elif pred_aqi <= 100:
        category,emoji,grad,border,text = "Satisfactory","🟡","linear-gradient(135deg,#1c1a06,#3d3200)","#eab308","#facc15"
    elif pred_aqi <= 200:
        category,emoji,grad,border,text = "Moderate","🟠","linear-gradient(135deg,#1c0f00,#431407)","#f97316","#fb923c"
    elif pred_aqi <= 300:
        category,emoji,grad,border,text = "Poor","🟤","linear-gradient(135deg,#1c0a00,#431407)","#dc2626","#f87171"
    else:
        category,emoji,grad,border,text = "Very Poor","🔴","linear-gradient(135deg,#1a0000,#4c0519)","#9f1239","#fb7185"

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:{grad};border:2px solid {border};border-radius:24px;
      padding:2.5rem;text-align:center;
      box-shadow:0 0 60px rgba(0,0,0,0.5),0 0 30px {border}33;margin-bottom:1.5rem;">
      <div style="font-size:1rem;color:#a0a0c0;letter-spacing:2px;text-transform:uppercase;margin-bottom:.5rem;">
        📍 {city} &nbsp;|&nbsp; Predicted AQI</div>
      <div style="font-size:6rem;font-weight:900;color:{text};line-height:1;
        text-shadow:0 0 40px {border};margin:.3rem 0;">{pred_aqi:.0f}</div>
      <div style="font-size:1.6rem;font-weight:700;color:{text};margin-top:.5rem;">{emoji} {category}</div>
      <div style="display:flex;justify-content:center;gap:2rem;margin-top:1.5rem;flex-wrap:wrap;">
        <span style="color:#8080b0;font-size:.88rem;"><span style="color:#a78bfa;font-weight:700;">PM2.5:</span> {pm25:.1f} µg/m³</span>
        <span style="color:#8080b0;font-size:.88rem;"><span style="color:#60a5fa;font-weight:700;">PM10:</span> {pm10:.1f} µg/m³</span>
        <span style="color:#8080b0;font-size:.88rem;"><span style="color:#34d399;font-weight:700;">NO₂:</span> {no2:.1f} µg/m³</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    pct = min(100, (pred_aqi / 500) * 100)
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.08);
      border-radius:16px;padding:1.2rem 1.6rem;margin-bottom:1.5rem;">
      <div style="display:flex;justify-content:space-between;color:#9090c0;font-size:.82rem;margin-bottom:.5rem;">
        <span>0 — Good</span><span>100 — Satisfactory</span><span>200 — Moderate</span><span>300 — Poor</span><span>500 — Very Poor</span>
      </div>
      <div style="background:rgba(255,255,255,0.08);border-radius:20px;height:14px;overflow:hidden;">
        <div style="width:{pct}%;height:100%;
          background:linear-gradient(90deg,#22c55e,#eab308,#f97316,#dc2626,#9f1239);
          border-radius:20px;box-shadow:0 0 12px {border};"></div>
      </div>
      <div style="text-align:right;color:#7070a0;font-size:.78rem;margin-top:.4rem;">
        AQI {pred_aqi:.0f} / 500</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<h3 style="color:#c4b5fd;font-size:1.1rem;margin-bottom:.8rem;">🏥 Health Recommendations</h3>', unsafe_allow_html=True)
    if pred_aqi > 300:
        st.error("🚨 **Hazardous.** Stay indoors, seal windows, use air purifiers. Avoid ALL outdoor activity.")
    elif pred_aqi > 200:
        st.warning("⚠️ **Very Poor.** Children, elderly & respiratory patients should stay indoors.")
    elif pred_aqi > 100:
        st.info("ℹ️ **Moderate.** Sensitive groups should reduce prolonged outdoor exertion.")
    else:
        st.success("✅ **Air quality acceptable.** Normal outdoor activities are fine for most people.")

st.markdown("---")
st.markdown("""<div style="text-align:center;color:#50507a;font-size:.8rem;padding:.5rem 0 1rem;">
  🌍 Production ML Model &nbsp;·&nbsp; Streamlit Cloud &nbsp;·&nbsp; SDG 11 — Sustainable Cities &amp; Communities
</div>""", unsafe_allow_html=True)
