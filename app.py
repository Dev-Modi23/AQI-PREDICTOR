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
    page_title="AQI Predictor AI",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# WORLD-CLASS CUSTOM CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}
.main { background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%); }
.glass-hero {
    background: rgba(255,255,255,0.95);
    backdrop-filter: blur(30px);
    border-radius: 32px;
    border: 1px solid rgba(255,255,255,0.3);
    box-shadow: 0 32px 64px rgba(0,0,0,0.12);
    transition: all 0.4s cubic-bezier(0.4,0,0.2,1);
}
.glass-hero:hover { transform: translateY(-4px); box-shadow: 0 48px 96px rgba(0,0,0,0.2); }
.aqi-good { background: linear-gradient(135deg, #10b981, #34d399); }
.aqi-moderate { background: linear-gradient(135deg, #f59e0b, #fbbf24); }
.aqi-unhealthy { background: linear-gradient(135deg, #ef4444, #f87171); }
.aqi-hazardous { background: linear-gradient(135deg, #7c3aed, #a855f7); }
.metric-card {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(20px);
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,0.4);
    padding: 2rem;
    transition: all 0.3s ease;
}
.metric-card:hover { transform: translateY(-2px); box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
.navbar { 
    background: rgba(255,255,255,0.95); 
    backdrop-filter: blur(20px); 
    border-bottom: 1px solid rgba(255,255,255,0.3);
}
.gradient-text { 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
</style>
""", unsafe_allow_html=True)

# Simulated premium data
@st.cache_data
def get_aqi_data():
    cities = ['Delhi', 'Mumbai', 'Bangalore', 'Surat', 'Chennai']
    dates = pd.date_range("2026-03-01", periods=30, freq="H")
    np.random.seed(42)
    
    data = pd.DataFrame({
        'timestamp': np.tile(dates, 5),
        'city': np.repeat(cities, len(dates)),
        'aqi': np.random.normal(120, 40, len(dates)*5).clip(10, 400),
        'pm25': np.random.normal(45, 20, len(dates)*5).clip(5, 200),
        'pm10': np.random.normal(85, 35, len(dates)*5).clip(10, 300),
        'no2': np.random.normal(35, 15, len(dates)*5).clip(5, 100),
        'so2': np.random.normal(15, 8, len(dates)*5).clip(2, 50),
        'co': np.random.normal(1.2, 0.5, len(dates)*5).clip(0.1, 5),
        'o3': np.random.normal(65, 25, len(dates)*5).clip(10, 150),
        'temp': np.random.normal(28, 5, len(dates)*5).clip(15, 40),
        'humidity': np.random.normal(65, 15, len(dates)*5).clip(30, 95),
        'wind_speed': np.random.normal(8, 3, len(dates)*5).clip(1, 20)
    })
    data['predicted_aqi'] = data['aqi'] + np.random.normal(0, 8, len(data))
    data['confidence'] = np.random.uniform(0.85, 0.99, len(data))
    return data

# TOP NAVBAR
with st.container():
    navbar_col1, navbar_col2, navbar_col3, navbar_col4 = st.columns([1, 3, 1, 1])
    with navbar_col1:
        st.markdown('<h1 class="gradient-text" style="font-size: 1.8rem; margin: 0;">🌫️ AQI Predictor AI</h1>', unsafe_allow_html=True)
    with navbar_col2:
        st.text_input("", placeholder="🔍 Search cities or pollutants...", key="city_search")
    with navbar_col3:
        st.button("🔔", key="notifications")
    with navbar_col4:
        st.markdown('<img src="https://via.placeholder.com/36" style="border-radius: 50%;">', unsafe_allow_html=True)

# LEFT SIDEBAR NAVIGATION
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 2rem 1rem;">
        <h2 class="gradient-text" style="font-size: 2rem; margin: 0;">🏙️ AQI Predictor</h2>
        <p style="color: #6b7280; margin-top: 0.5rem;">AI-Powered Air Quality</p>
    </div>
    """, unsafe_allow_html=True)
    
    nav_options = {
        "📊 Dashboard": "dashboard",
        "🔮 Live Prediction": "prediction", 
        "📈 Pollution Analytics": "analytics",
        "📊 Historical Data": "history",
        "❤️ Health Insights": "health",
        "⚙️ Settings": "settings"
    }
    
    selected_page = st.radio("", list(nav_options.values()), index=0, horizontal=False, key="sidebar_nav")
    st.markdown("---")
    
    # Quick city switcher
    current_city = st.selectbox("📍 Current City", ["Delhi", "Surat", "Mumbai", "Bangalore"], index=1)

# HERO AQI PREDICTION CARD - DASHBOARD
if selected_page == "dashboard":
    data = get_aqi_data()
    recent_data = data[data['city'] == current_city].tail(1).iloc[0]
    
    # Hero AQI Card (Full Width)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"""
        <div class="glass-hero" style="padding: 3rem; margin-bottom: 2rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h1 style="font-size: 4.5rem; font-weight: 800; margin: 0; color: #1f2937;">
                        {recent_data['predicted_aqi']:.0f}
                    </h1>
                    <p style="font-size: 1.3rem; color: #6b7280; margin: 0.5rem 0;">AQI Prediction</p>
                    <div style="font-size: 1.1rem; color: #10b981; font-weight: 600;">
                        ● Moderate • 92% Confidence
                    </div>
                </div>
                <div style="font-size: 6rem; opacity: 0.8;">🌫️</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # KPI Summary Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <p style="color: #6b7280; margin: 0 0 1rem 0; font-weight: 500;">PM2.5</p>
            <p style="font-size: 2.2rem; font-weight: 800; color: #ef4444; margin: 0;">{recent_data['pm25']:.1f}</p>
            <p style="font-size: 0.85rem; color: #10b981; margin: 0.5rem 0 0 0;">↓ 3.2%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <p style="color: #6b7280; margin: 0 0 1rem 0; font-weight: 500;">Temperature</p>
            <p style="font-size: 2.2rem; font-weight: 800; color: #3b82f6;">{recent_data['temp']:.1f}°C</p>
            <p style="font-size: 0.85rem; color: #6b7280;">Clear Sky</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <p style="color: #6b7280; margin: 0 0 1rem 0; font-weight: 500;">Humidity</p>
            <p style="font-size: 2.2rem; font-weight: 800; color: #8b5cf6;">68%</p>
            <p style="font-size: 0.85rem; color: #10b981;">Optimal</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <p style="color: #6b7280; margin: 0 0 1rem 0; font-weight: 500;">Wind Speed</p>
            <p style="font-size: 2.2rem; font-weight: 800; color: #06b6d4;">7.2 km/h</p>
            <p style="font-size: 0.85rem; color: #f59e0b;">Light Breeze</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 style="color: #1f2937; font-weight: 700; margin-bottom: 2rem;">Pollution Trends (24h)</h3>', unsafe_allow_html=True)
        
        # Pollution subplot
        fig = make_subplots(rows=2, cols=2, 
                          subplot_titles=('PM2.5', 'PM10', 'NO2', 'SO2'),
                          vertical_spacing=0.1)
        
        hourly_data = data[data['city'] == current_city].tail(24)
        fig.add_trace(go.Scatter(x=hourly_data['timestamp'], y=hourly_data['pm25'], 
                                name='PM2.5', line=dict(color='#ef4444')), row=1, col=1)
        fig.add_trace(go.Scatter(x=hourly_data['timestamp'], y=hourly_data['pm10'], 
                                name='PM10', line=dict(color='#f59e0b')), row=1, col=2)
        fig.add_trace(go.Scatter(x=hourly_data['timestamp'], y=hourly_data['no2'], 
                                name='NO2', line=dict(color='#8b5cf6')), row=2, col=1)
        fig.add_trace(go.Scatter(x=hourly_data['timestamp'], y=hourly_data['so2'], 
                                name='SO2', line=dict(color='#10b981')), row=2, col=2)
        
        fig.update_layout(height=450, showlegend=False, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<h3 style="color: #1f2937; font-weight: 700; margin-bottom: 2rem;">AQI Historical Trend</h3>', unsafe_allow_html=True)
        
        daily_data = data[data['city'] == current_city].resample('D', on='timestamp').mean().tail(30)
        fig = px.line(daily_data, x=daily_data.index, y=['aqi', 'predicted_aqi'], 
                     title="30-Day AQI Trend",
                     labels={'value': 'AQI', 'variable': 'Type'})
        fig.update_traces(line=dict(width=4))
        fig.update_layout(height=450, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

# HEALTH INSIGHTS PAGE
elif selected_page == "health":
    st.markdown('<h2 style="font-size: 2.8rem; font-weight: 800; color: #1f2937;">❤️ Health Recommendations</h2>', unsafe_allow_html=True)
    
    recommendations = [
        "✅ **Safe to go outside** - Air quality is moderate",
        "😷 **N95 mask recommended** for sensitive groups",
        "👶 **Children & elderly**: Limit outdoor activities",
        "🏃‍♂️ **Exercise**: Good conditions for outdoor workout",
        "🌳 **Best time**: 6 AM - 10 AM for outdoor activities"
    ]
    
    for rec in recommendations:
        st.markdown(f"""
        <div class="metric-card" style="margin-bottom: 1rem; padding: 1.5rem;">
            <div style="font-size: 1.1rem; font-weight: 600; color: #1f2937;">{rec}</div>
        </div>
        """, unsafe_allow_html=True)

# Run: streamlit run aqi_dashboard.py
st.markdown("---")
st.markdown("<p style='text-align: center; color: #6b7280;'>Powered by AI • Real-time Predictions • World-class Design</p>", unsafe_allow_html=True)
