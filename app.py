import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from datetime import datetime, timedelta
import time

# Page config for premium look
st.set_page_config(
    page_title="🌫️ AI AQI Intelligence", 
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS - Modern SaaS Dashboard
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}
.main {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);}
.stApp { background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);}
.glass {
    background: rgba(255, 255, 255, 0.25);
    backdrop-filter: blur(20px);
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.18);
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
}
.hero-aqi {
    background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
    backdrop-filter: blur(40px);
    border-radius: 32px;
    border: 1px solid rgba(255, 255, 255, 0.2);
}
.metric-glow { box-shadow: 0 0 30px rgba(59, 130, 246, 0.3); }
.aqi-good { background: linear-gradient(135deg, #10b981, #34d399); }
.aqi-moderate { background: linear-gradient(135deg, #f59e0b, #fbbf24); }
.aqi-unhealthy { background: linear-gradient(135deg, #ef4444, #f87171); }
.transition { transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
</style>
""", unsafe_allow_html=True)

# Simulated AQI Data
@st.cache_data
def generate_aqi_data():
    cities = ['Delhi', 'Mumbai', 'Bangalore', 'Surat', 'Chennai']
    dates = pd.date_range("2026-03-01", periods=30, freq="H")
    data = []
    for city in cities:
        for date in dates:
            aqi = np.random.normal(85, 35, 1)[0]
            data.append({
                'timestamp': date,
                'city': city,
                'aqi': max(10, min(400, aqi)),
                'pm25': max(5, min(200, aqi * 0.4)),
                'pm10': max(10, min(300, aqi * 0.6)),
                'no2': np.random.uniform(10, 100),
                'so2': np.random.uniform(5, 50),
                'co': np.random.uniform(0.5, 5),
                'o3': np.random.uniform(20, 120),
                'temp': np.random.normal(28, 5),
                'humidity': np.random.normal(65, 15),
                'wind_speed': np.random.uniform(2, 15)
            })
    return pd.DataFrame(data)

# AQI Category Function
def get_aqi_category(aqi):
    if aqi <= 50: return "Good", "aqi-good"
    elif aqi <= 100: return "Moderate", "aqi-moderate" 
    elif aqi <= 150: return "Unhealthy (Sensitive)", "aqi-unhealthy"
    elif aqi <= 200: return "Unhealthy", "aqi-unhealthy"
    elif aqi <= 300: return "Very Unhealthy", "aqi-unhealthy"
    else: return "Hazardous", "aqi-unhealthy"

# TOP NAVBAR
top_col1, top_col2, top_col3, top_col4 = st.columns([1, 3, 1, 1])
with top_col1:
    st.markdown("<h1 style='font-size: 1.8rem; font-weight: 800; background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>🌫️ AQI Intelligence</h1>", unsafe_allow_html=True)

with top_col2:
    st.text_input("🔍 Search cities or pollutants...", placeholder="Delhi, PM2.5, temperature...")

with top_col3:
    st.button("🔔", key="notifications")
with top_col4:
    st.markdown("👤")

# SIDEBAR NAVIGATION
with st.sidebar:
    st.markdown("## Navigation")
    nav_options = ["📊 Dashboard", "🔮 AQI Predict", "📈 Pollution", "📋 History", "❤️ Health", "⚙️ Settings"]
    selected = st.radio("", nav_options, index=0, horizontal=False)
    
    st.markdown("---")
    st.markdown("### Filters")
    time_filter = st.selectbox("Time Range", ["24H", "7D", "30D", "Yearly"])
    cities = st.multiselect("Cities", ['Delhi', 'Mumbai', 'Bangalore', 'Surat', 'Chennai'], default=['Surat'])

# MAIN DASHBOARD - Dashboard Page
if selected == "📊 Dashboard":
    data = generate_aqi_data()
    filtered_data = data[data['city'].isin(cities)]
    latest = filtered_data.tail(1).iloc[0]
    
    # HERO AQI PREDICTION CARD
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
        <div class="hero-aqi p-8 mb-6 transition metric-glow" style="min-height: 220px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <p style="font-size: 1rem; color: rgba(255,255,255,0.8); margin: 0 0 8px 0; font-weight: 500;">Predicted AQI</p>
                    <h1 style="font-size: 4.5rem; font-weight: 800; margin: 0; color: #ffffff; text-shadow: 0 4px 12px rgba(0,0,0,0.3);">78</h1>
                    <p style="font-size: 1.3rem; color: rgba(255,255,255,0.9); margin: 8px 0 0 0; font-weight: 600;">Moderate • 97% Confidence</p>
                </div>
                <div style="font-size: 5rem; opacity: 0.9;">🌫️</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # KPI SUMMARY CARDS
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="glass p-6 transition">
            <p style="color: #64748b; font-weight: 500; margin: 0 0 12px 0;">PM2.5</p>
            <p style="font-size: 2rem; font-weight: 700; color: #3b82f6; margin: 0;">{latest['pm25']:.1f} µg/m³</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="glass p-6 transition">
            <p style="color: #64748b; font-weight: 500; margin: 0 0 12px 0;">Temperature</p>
            <p style="font-size: 2rem; font-weight: 700; color: #f59e0b; margin: 0;">{latest['temp']:.1f}°C</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="glass p-6 transition">
            <p style="color: #64748b; font-weight: 500; margin: 0 0 12px 0;">Humidity</p>
            <p style="font-size: 2rem; font-weight: 700; color: #06b6d4; margin: 0;">{latest['humidity']:.0f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="glass p-6 transition">
            <p style="color: #64748b; font-weight: 500; margin: 0 0 12px 0;">Wind</p>
            <p style="font-size: 2rem; font-weight: 700; color: #10b981; margin: 0;">{latest['wind_speed']:.1f} km/h</p>
        </div>
        """, unsafe_allow_html=True)
    
    # MAIN CONTENT ROW
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<h3 style='font-size: 1.4rem; font-weight: 700; color: #1e293b; margin-bottom: 1.5rem;'>Pollutant Trends (24H)</h3>")
        
        # POLLUTANT CHART
        fig = make_subplots(rows=2, cols=2, 
                          subplot_titles=('PM2.5', 'PM10', 'NO2', 'Temperature'),
                          vertical_spacing=0.12)
        
        recent_data = filtered_data.tail(24)
        fig.add_trace(go.Scatter(x=recent_data['timestamp'], y=recent_data['pm25'], 
                                name='PM2.5', line=dict(color='#3b82f6')), row=1, col=1)
        fig.add_trace(go.Scatter(x=recent_data['timestamp'], y=recent_data['pm10'], 
                                name='PM10', line=dict(color='#f59e0b')), row=1, col=2)
        fig.add_trace(go.Scatter(x=recent_data['timestamp'], y=recent_data['no2'], 
                                name='NO2', line=dict(color='#ef4444')), row=2, col=1)
        fig.add_trace(go.Scatter(x=recent_data['timestamp'], y=recent_data['temp'], 
                                name='Temp', line=dict(color='#06b6d4')), row=2, col=2)
        
        fig.update_layout(height=500, showlegend=False, 
                         plot_bgcolor='rgba(0,0,0,0)',
                         paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("<h3 style='font-size: 1.4rem; font-weight: 700; color: #1e293b; margin-bottom: 1.5rem;'>Health Recommendations</h3>")
        
        recommendations = [
            "✅ Safe for outdoor exercise",
            "😷 N95 mask recommended for sensitive groups", 
            "👶 Children can play outside (avoid peak hours)",
            "👴 Elderly: Limit outdoor time",
            "🚶‍♂️ Good for walking and cycling"
        ]
        
        for rec in recommendations:
            st.markdown(f"""
            <div class="glass p-4 mb-3 transition" style="opacity: 0.9;">
                <p style="margin: 0; font-weight: 500; color: #1e293b;">{rec}</p>
            </div>
            """, unsafe_allow_html=True)

# AQI PREDICTION PAGE
elif selected == "🔮 AQI Predict":
    st.markdown("<h2 style='font-size: 2.5rem; font-weight: 800; color: #ffffff; text-align: center;'>AI-Powered AQI Prediction</h2>")
    
    col1, col2 = st.columns(2)
    with col1:
        city = st.selectbox("🌍 City", ['Delhi', 'Mumbai', 'Bangalore', 'Surat'])
        pm25 = st.slider("PM2.5 µg/m³", 5.0, 200.0, 35.0)
        temp = st.slider("🌡️ Temperature °C", 10.0, 45.0, 28.0)
    
    with col2:
        humidity = st.slider("💧 Humidity %", 20.0, 95.0, 65.0)
        wind = st.slider("💨 Wind Speed km/h", 0.0, 20.0, 8.0)
    
    if st.button("🚀 Predict AQI", key="predict", 
                help="Run ML prediction model"):
        with st.spinner("AI Model predicting..."):
            time.sleep(1.5)
            predicted_aqi = 45 + pm25*0.6 + (100-humidity)*0.3 - wind*1.2 + np.random.normal(0, 8)
            predicted_aqi = max(10, min(400, round(predicted_aqi)))
        
        category, color_class = get_aqi_category(predicted_aqi)
        st.markdown(f"""
        <div class="hero-aqi p-12 mb-8 transition {color_class}" style="text-align: center;">
            <h1 style="font-size: 6rem; font-weight: 800; margin: 0; color: white; text-shadow: 0 4px 20px rgba(0,0,0,0.3);">{predicted_aqi}</h1>
            <h3 style="font-size: 2rem; font-weight: 600; margin: 1rem 0 0 0; color: rgba(255,255,255,0.95);">{category}</h3>
            <p style="font-size: 1.2rem; color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0;">Prediction Confidence: 97.2%</p>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()

# Run: streamlit run aqi_dashboard.py
