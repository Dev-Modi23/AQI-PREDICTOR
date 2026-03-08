import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
import joblib
from streamlit_folium import folium_static

st.set_page_config(layout="wide", page_title="AQI PREDICTOR", page_icon="🌐")

# ================= LOAD ML MODEL WITH ERROR HANDLING =================
@st.cache_data
def load_models():
    try:
        model = joblib.load("air_quality_model.pkl")
        scaler_X = joblib.load("scaler_X.pkl")
        scaler_y = joblib.load("scaler_y.pkl")
        return model, scaler_X, scaler_y
    except FileNotFoundError:
        st.error("Model files not found. Using fallback prediction.")
        return None, None, None

model, scaler_X, scaler_y = load_models()

# ================= CITY COORDINATES =================
city_coords = {
    "Delhi": (28.61,77.21),"Ghaziabad": (28.67,77.42),"Faridabad": (28.41,77.31),
    "Noida": (28.58,77.33),"Gurugram": (28.46,77.03),"Kanpur": (26.45,80.33),
    "Lucknow": (26.85,80.95),"Meerut": (28.99,77.71),"Agra": (27.18,78.02),
    "Varanasi": (25.32,82.99),"Patna": (25.59,85.14),"Ludhiana": (30.91,75.85),
    "Amritsar": (31.63,74.87),"Jalandhar": (31.33,75.58),"Panipat": (29.39,76.97),
    "Mumbai": (19.07,72.88),"Pune": (18.52,73.86),"Surat": (21.17,72.83),
    "Ahmedabad": (23.02,72.57),"Vadodara": (22.30,73.18),"Rajkot": (22.30,70.80),
    "Nashik": (20.00,73.79),"Aurangabad": (19.88,75.34),"Nagpur": (21.15,79.09),
    "Thane": (19.22,72.98),"Solapur": (17.67,75.91),"Kolhapur": (16.70,74.24),
    "Bangalore": (12.97,77.59),"Hyderabad": (17.39,78.49),"Chennai": (13.08,80.27),
    "Coimbatore": (11.02,76.96),"Madurai": (9.92,78.12),"Visakhapatnam": (17.69,83.22),
    "Vijayawada": (16.51,80.65),"Kochi": (9.93,76.27),"Thiruvananthapuram": (8.52,76.94),
    "Mysore": (12.30,76.65),"Mangalore": (12.91,74.86),"Belgaum": (15.85,74.50),
    "Hubli": (15.36,75.12),"Tiruchirappalli": (10.79,78.70),"Salem": (11.66,78.15),
    "Warangal": (18.00,79.58),"Kolkata": (22.57,88.36),"Bhubaneswar": (20.30,85.82),
    "Guwahati": (26.14,91.74),"Dhanbad": (23.80,86.43),"Asansol": (23.68,86.95),
    "Durgapur": (23.52,87.31),"Indore": (22.72,75.86),"Bhopal": (23.25,77.41),
    "Jabalpur": (23.18,79.99),"Gwalior": (26.21,78.18),"Raipur": (21.25,81.63),
    "Bilaspur": (22.08,82.14),"Jaipur": (26.91,75.79),"Chandigarh": (30.73,76.78),
    "Srinagar": (34.08,74.80),"Shimla": (31.10,77.17),"Dehradun": (30.32,78.03),
    "Gorakhpur": (26.75,83.37),"Allahabad": (25.45,81.85)
}

# ================= CITY POLLUTION BASE DATA =================
city_pollution = {
    "Delhi":[180,320,150],"Mumbai":[120,200,110],"Surat":[130,210,120],
    "Ahmedabad":[150,230,140],"Bangalore":[90,150,80],"Chennai":[110,180,100],
    "Kolkata":[140,240,130],"Pune":[100,170,90],"Hyderabad":[105,185,95],
    "Jaipur":[135,225,125],"Lucknow":[125,205,115],"Kanpur":[155,255,145],
    "Nagpur":[115,195,105],"Indore":[95,165,85],"Bhopal":[110,190,100],
    "Visakhapatnam":[85,155,75],"Patna":[145,245,135]
}

# ================= FIXED ML PREDICTION =================
def predict_aqi(city):
    if model is None or scaler_X is None or scaler_y is None:
        pm25, _, _ = city_pollution.get(city, [120, 200, 100])
        return max(50, min(450, int(pm25 * 1.2)))
    
    try:
        pm25, pm10, no2 = city_pollution.get(city, [120, 200, 100])
        
        features_dict = {
            'PM2.5': pm25,
            'PM10': pm10,
            'NO2': no2,
            'PM2.5_lag1': pm25 * 0.95,
            'AQI_lag1': pm25 * 1.1,
            'PM2.5_7d_avg': pm25 * 0.9,
            'AQI_7d_avg': pm25 * 1.05
        }
        
        features = pd.DataFrame([features_dict])
        X_scaled = scaler_X.transform(features)
        pred_scaled = model.predict(X_scaled)
        prediction = scaler_y.inverse_transform(pred_scaled.reshape(-1, 1))
        return int(prediction[0][0])
        
    except Exception as e:
        pm25, _, _ = city_pollution.get(city, [120, 200, 100])
        return max(50, min(450, int(pm25 * 1.2)))

# ================= SOURCE ANALYSIS =================
def get_city_sources(city_name, current_aqi):
    industrial_cities = ["Kanpur","Ghaziabad","Ludhiana","Dhanbad","Faridabad","Surat","Panipat","Durgapur"]
    vehicle_cities = ["Delhi","Mumbai","Pune","Bangalore","Hyderabad","Chennai","Thane","Nashik"]
    construction_cities = ["Noida","Gurugram","Ahmedabad","Indore","Nagpur","Gwalior"]

    if city_name in industrial_cities:
        sources = {"Factories 🏭":40,"Vehicles 🚗":25,"Road Dust 🌫️":20,"Construction 🏗️":10,"Household 👨‍👩‍👧":5}
    elif city_name in vehicle_cities:
        sources = {"Vehicles 🚗":45,"Factories 🏭":25,"Road Dust 🌫️":15,"Construction 🏗️":10,"Household 👨‍👩‍👧":5}
    elif city_name in construction_cities:
        sources = {"Construction 🏗️":35,"Vehicles 🚗":30,"Factories 🏭":20,"Road Dust 🌫️":10,"Household 👨‍👩‍👧":5}
    else:
        sources = {"Vehicles 🚗":35,"Factories 🏭":25,"Construction 🏗️":20,"Road Dust 🌫️":15,"Household 👨‍👩‍👧":5}

    total = sum(sources.values())
    return {k:round((v/total)*100,1) for k,v in sources.items()}

# ================= UI STYLE =================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
background: linear-gradient(135deg,#020617 0%,#0f172a 50%,#1e293b 100%);
color:white;}
[data-testid="stHeader"]{display:none;}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.title("🌐 AQI PREDICTOR")
st.markdown("<center>AI Based Air Quality Prediction</center>",unsafe_allow_html=True)

# ================= CITY SELECT =================
cities_display=[
"Delhi 🗼","Mumbai 🏙️","Bangalore 🌴","Pune 🏔️","Chennai 🌊","Kolkata 🕌",
"Surat 🛍️","Ahmedabad 🏰","Hyderabad 🕌","Jaipur 🏰","Lucknow 🕌","Kanpur 🏭",
"Nagpur 🏙️","Indore 🛒","Bhopal 🏛️","Visakhapatnam 🌊","Patna 🛕"
]

selected_city=st.selectbox("Select City",cities_display)
city_name=selected_city.split()[0]

# ================= ML AQI =================
current_aqi=predict_aqi(city_name)
lat,lon=city_coords.get(city_name,(20.59,78.96))

# ================= METRIC =================
st.metric("Predicted AQI",current_aqi)

# ================= GAUGE =================
fig=go.Figure(go.Indicator(
mode="gauge+number",
value=current_aqi,
title={'text':f"AQI - {city_name}"},
gauge={
'axis':{'range':[0,500]},
'bar':{'color':"#22c55e" if current_aqi<150 else "#ef4444"},
'steps':[
{'range':[0,50],'color':"#10b981"},
{'range':[50,100],'color':"#84cc16"},
{'range':[100,200],'color':"#facc15"},
{'range':[200,300],'color':"#fb923c"},
{'range':[300,500],'color':"#ef4444"}
]
))
st.plotly_chart(fig,use_container_width=True)

# ================= TABS =================
tab1,tab2,tab3,tab4=st.tabs(["Forecast","Sources","Map","Health"])

# ================= FORECAST =================
with tab1:
    np.random.seed(hash(city_name)%100)
    forecast=[current_aqi]
    for i in range(4):
        change=np.random.uniform(-0.08,0.08)
        forecast.append(max(50,min(500,forecast[-1]*(1+change))))
    days=["Today","Tomorrow","+2D","+3D","+4D"]
    fig=px.line(x=days,y=forecast,markers=True,title="AI Forecast")
    st.plotly_chart(fig,use_container_width=True)

# ================= SOURCES =================
with tab2:
    sources=get_city_sources(city_name,current_aqi)
    fig=px.pie(values=list(sources.values()),names=list(sources.keys()))
    st.plotly_chart(fig,use_container_width=True)

# ================= MAP =================
with tab3:
    m=folium.Map(location=[lat,lon],zoom_start=10)
    folium.CircleMarker(
        [lat,lon],
        radius=current_aqi/12,
        popup=f"{city_name} AQI {current_aqi}",
        color="red" if current_aqi>200 else "green",
        fill=True
    ).add_to(m)
    folium_static(m)

# ================= HEALTH =================
with tab4:
    if current_aqi>300:
        st.error("Hazardous air quality")
    elif current_aqi>200:
        st.warning("Very unhealthy")
    elif current_aqi>100:
        st.info("Moderate air quality")
    else:
        st.success("Good air quality")

# ================= ORIGINAL FOOTER =================
st.markdown("---")
st.markdown("Dev Modi | AI AQI Predictor | ML Integrated")
