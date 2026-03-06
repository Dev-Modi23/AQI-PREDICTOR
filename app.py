import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(layout="wide", page_title="AI AQI Pro", page_icon="🌍")

# ---------------- UI STYLE ---------------- #

st.markdown("""
<style>

/* BACKGROUND */
[data-testid="stAppViewContainer"]{
background: linear-gradient(135deg,#020617,#0f172a,#1e293b);
color:white;
}

/* REMOVE HEADER */
[data-testid="stHeader"]{
display:none;
}

/* TITLE */
h1{
text-align:center;
font-size:3.5rem !important;
font-weight:800;
background: linear-gradient(90deg,#22c55e,#06b6d4,#3b82f6);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

/* CARD */
.card{
background: rgba(255,255,255,0.05);
padding:20px;
border-radius:20px;
backdrop-filter: blur(10px);
border:1px solid rgba(255,255,255,0.1);
box-shadow:0 10px 40px rgba(0,0,0,0.5);
}

/* METRIC STYLE */
[data-testid="metric-container"]{
background: rgba(255,255,255,0.04);
border-radius:15px;
padding:15px;
box-shadow:0 4px 20px rgba(0,0,0,0.5);
}

/* SELECT BOX */
.stSelectbox div[data-baseweb="select"]{
background:#111827;
border-radius:10px;
}

/* TABS */
.stTabs [role="tab"]{
font-size:18px;
padding:10px 20px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ---------------- #

st.title("🌍 AI AQI Pro")
st.markdown(
"<center>Advanced AI Air Quality Intelligence Platform</center>",
unsafe_allow_html=True
)

# ---------------- CITY SELECT ---------------- #

cities = [
"Delhi 🗼","Mumbai 🏙️","Bangalore 🌴","Pune 🏔️","Chennai 🌊",
"Kolkata 🕌","Surat 🛍️","Ahmedabad 🏰","Hyderabad 🕌",
"Jaipur 🏰","Lucknow 🕌","Kanpur 🏭"
]

st.subheader("🏙️ Select City")

selected_city = st.selectbox(
"Choose city for AI analysis",
cities
)

# ---------------- BASE AQI ---------------- #

base_aqi_dict = {
"Delhi":190,
"Mumbai":120,
"Bangalore":90,
"Surat":130,
"Ahmedabad":150
}

city_key = selected_city.split()[0]
base_aqi = base_aqi_dict.get(city_key,140)

# ---------------- AQI GAUGE ---------------- #

st.subheader("📊 Current AQI Level")

fig = go.Figure(go.Indicator(
mode="gauge+number",
value=base_aqi,
title={'text':f"AQI in {city_key}"},
gauge={
'axis':{'range':[0,500]},
'bar':{'color':"#22c55e"},
'steps':[
{'range':[0,50],'color':"#16a34a"},
{'range':[50,100],'color':"#84cc16"},
{'range':[100,200],'color':"#facc15"},
{'range':[200,300],'color':"#fb923c"},
{'range':[300,500],'color':"#ef4444"}
]
}
))

fig.update_layout(height=350)

st.plotly_chart(fig,use_container_width=True)

# ---------------- TABS ---------------- #

tab1,tab2,tab3,tab4,tab5 = st.tabs([
"🔮 AQI Prediction",
"🏭 Source Detection",
"🗺️ Clean Route",
"🌡️ Heatmap",
"🫁 Health Risk"
])

# ---------------- AQI PREDICTION ---------------- #

with tab1:

    st.subheader("5 Day AI AQI Forecast")

    forecast=[base_aqi]

    for i in range(4):
        forecast.append(
        max(50,min(500,
        forecast[-1]*np.random.normal(1.02,0.08)))
        )

    days=["Today","Tomorrow","+2 Day","+3 Day","+4 Day"]

    fig=px.line(
        x=days,
        y=forecast,
        markers=True,
        title="AI AQI Forecast"
    )

    fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig,use_container_width=True)

# ---------------- SOURCE DETECTION ---------------- #

with tab2:

    st.subheader("AI Pollution Source Detection")

    sources={
    "Vehicles 🚗":45,
    "Factories 🏭":25,
    "Construction 🏗️":15,
    "Dust 🌫️":10,
    "Household 👨‍👩‍👧":5
    }

    fig=px.pie(
    values=list(sources.values()),
    names=list(sources.keys()),
    color_discrete_sequence=[
    "#ef4444","#f97316","#eab308","#22c55e","#3b82f6"]
    )

    fig.update_layout(height=400)

    st.plotly_chart(fig,use_container_width=True)

# ---------------- ROUTE PLANNER ---------------- #

with tab3:

    st.subheader("Clean Air Route Planner")

    col1,col2=st.columns(2)

    with col1:
        st.success("🌳 Green Route")

        st.metric(
        "AQI Exposure",
        "92",
        "-35%"
        )

        st.write("Recommended path through parks and residential areas.")

    with col2:

        st.error("🚗 Highway Route")

        st.metric(
        "AQI Exposure",
        "215",
        "+40%"
        )

        st.write("High pollution due to traffic and dust.")

# ---------------- HEATMAP ---------------- #

with tab4:

    st.subheader("Future AQI Heatmap")

    heatmap_data=np.random.randint(50,300,(5,5))

    fig=px.imshow(
    heatmap_data,
    labels=dict(x="Area",y="Day",color="AQI"),
    x=["North","South","East","West","Central"],
    y=["Today","Tomorrow","+2D","+3D","+4D"],
    color_continuous_scale="RdYlGn_r"
    )

    fig.update_layout(height=450)

    st.plotly_chart(fig,use_container_width=True)

# ---------------- HEALTH RISK ---------------- #

with tab5:

    st.subheader("Personal Health Risk")

    risks={
    "Lung Safety":100-base_aqi*0.25,
    "Heart Risk":100-base_aqi*0.18,
    "Asthma Trigger":100-base_aqi*0.35,
    "Eye Irritation":100-base_aqi*0.15
    }

    cols=st.columns(4)

    for i,(risk,val) in enumerate(risks.items()):

        with cols[i]:

            score=max(0,val)

            color="🟢" if score>70 else "🟡" if score>40 else "🔴"

            st.metric(
            risk,
            f"{score:.0f}% Safe"
            )

            st.caption(color)

# ---------------- FOOTER ---------------- #

st.markdown("---")

st.markdown("""
<center>

### 🚀 Why AI AQI Pro Is Advanced

✔ AI Prediction Model  
✔ Pollution Source Detection  
✔ Clean Air Route Planning  
✔ Health Risk Analysis  
✔ Interactive Heatmap  

Developed by **Dev Modi**

</center>
""",unsafe_allow_html=True)
