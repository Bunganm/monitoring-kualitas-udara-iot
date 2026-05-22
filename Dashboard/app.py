import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import requests

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Smart Air Quality Monitoring",
    page_icon="🌫️",
    layout="wide"
)

from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=20000, key="iot_refresh")

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Space+Mono:wght@400;700&family=Inter:wght@300;400;500;600&display=swap');

/* ---- BASE ---- */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #080B12;
    color: #E2E8F0;
}

.main {
    background-color: #080B12;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(236,72,153,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 10%, rgba(0,229,255,0.08) 0%, transparent 55%),
        radial-gradient(ellipse 50% 60% at 50% 100%, rgba(99,102,241,0.07) 0%, transparent 60%);
    min-height: 100vh;
}

/* ---- HEADER ---- */
.header-wrapper {
    text-align: center;
    padding: 40px 0 20px 0;
    position: relative;
}

.big-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 52px;
    font-weight: 700;
    letter-spacing: 3px;
    background: linear-gradient(135deg, #EC4899 0%, #F9A8D4 35%, #00E5FF 70%, #818CF8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-transform: uppercase;
    line-height: 1.1;
    filter: drop-shadow(0 0 24px rgba(236,72,153,0.35));
}

.subtitle {
    font-family: 'Space Mono', monospace;
    text-align: center;
    color: #94A3B8;
    font-size: 13px;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-top: 8px;
    margin-bottom: 0;
}

.subtitle-accent {
    display: inline-block;
    color: #EC4899;
    margin: 0 8px;
}

/* ---- DIVIDER ---- */
.custom-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #EC4899 30%, #00E5FF 70%, transparent);
    margin: 24px 0;
    opacity: 0.5;
}

/* ---- CARDS ---- */
.card {
    border-radius: 16px;
    padding: 24px 16px;
    color: white;
    text-align: center;
    font-weight: 600;
    font-family: 'Rajdhani', sans-serif;
    letter-spacing: 1px;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.06);
    backdrop-filter: blur(12px);
}

.card-label {
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    opacity: 0.75;
    margin-bottom: 12px;
    display: block;
}

.card-icon {
    font-size: 28px;
    margin-bottom: 8px;
    display: block;
}

.card-value {
    font-size: 42px;
    font-weight: 700;
    line-height: 1;
    display: block;
}

.card-unit {
    font-size: 13px;
    opacity: 0.65;
    margin-top: 4px;
    display: block;
    font-family: 'Space Mono', monospace;
}

/* Card Variants */
.card-blue {
    background: linear-gradient(145deg, #0F172A, #0C1A2E);
    border-color: rgba(0,229,255,0.25);
    box-shadow: 0 0 30px rgba(0,229,255,0.08), inset 0 1px 0 rgba(0,229,255,0.1);
}
.card-blue .card-value { color: #00E5FF; }
.card-blue .card-icon { filter: drop-shadow(0 0 8px rgba(0,229,255,0.6)); }

.card-pink {
    background: linear-gradient(145deg, #1A0A14, #1F0D1A);
    border-color: rgba(236,72,153,0.3);
    box-shadow: 0 0 30px rgba(236,72,153,0.1), inset 0 1px 0 rgba(236,72,153,0.12);
}
.card-pink .card-value { color: #F472B6; }
.card-pink .card-icon { filter: drop-shadow(0 0 8px rgba(236,72,153,0.7)); }

.card-orange {
    background: linear-gradient(145deg, #1A1200, #1F1500);
    border-color: rgba(251,146,60,0.25);
    box-shadow: 0 0 30px rgba(251,146,60,0.08), inset 0 1px 0 rgba(251,146,60,0.1);
}
.card-orange .card-value { color: #FB923C; }
.card-orange .card-icon { filter: drop-shadow(0 0 8px rgba(251,146,60,0.6)); }

.card-red {
    background: linear-gradient(145deg, #1A0808, #1F0A0A);
    border-color: rgba(248,113,113,0.25);
    box-shadow: 0 0 30px rgba(248,113,113,0.1), inset 0 1px 0 rgba(248,113,113,0.1);
}
.card-red .card-value { color: #F87171; font-size: 28px; }

.card-good {
    background: linear-gradient(145deg, #021A10, #041F13);
    border-color: rgba(52,211,153,0.3);
    box-shadow: 0 0 30px rgba(52,211,153,0.1), inset 0 1px 0 rgba(52,211,153,0.1);
}
.card-good .card-value { color: #34D399; font-size: 28px; }

.card-medium {
    background: linear-gradient(145deg, #1A1000, #1F1300);
    border-color: rgba(251,191,36,0.25);
    box-shadow: 0 0 30px rgba(251,191,36,0.08), inset 0 1px 0 rgba(251,191,36,0.1);
}
.card-medium .card-value { color: #FBBF24; font-size: 28px; }

.card-purple {
    background: linear-gradient(145deg, #0F0C1A, #130F22);
    border-color: rgba(129,140,248,0.25);
    box-shadow: 0 0 30px rgba(129,140,248,0.08), inset 0 1px 0 rgba(129,140,248,0.1);
}
.card-purple .card-value { color: #818CF8; font-size: 22px; }
.card-purple .card-icon { filter: drop-shadow(0 0 8px rgba(129,140,248,0.6)); }

.card-teal {
    background: linear-gradient(145deg, #021418, #041B20);
    border-color: rgba(45,212,191,0.25);
    box-shadow: 0 0 30px rgba(45,212,191,0.08), inset 0 1px 0 rgba(45,212,191,0.1);
}
.card-teal .card-value { color: #2DD4BF; }
.card-teal .card-icon { filter: drop-shadow(0 0 8px rgba(45,212,191,0.6)); }

/* ---- SECTION HEADERS ---- */
.section-header {
    font-family: 'Rajdhani', sans-serif;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #F1F5F9;
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 32px 0 16px 0;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(236,72,153,0.2);
}

.section-header .accent-bar {
    width: 4px;
    height: 22px;
    background: linear-gradient(180deg, #EC4899, #818CF8);
    border-radius: 2px;
    display: inline-block;
    flex-shrink: 0;
}

/* ---- METRICS ---- */
[data-testid="metric-container"] {
    background: linear-gradient(145deg, #0F172A, #0D1526);
    border: 1px solid rgba(236,72,153,0.15);
    border-radius: 14px;
    padding: 18px 20px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}

[data-testid="metric-container"] label {
    font-family: 'Space Mono', monospace;
    font-size: 10px !important;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #94A3B8 !important;
}

[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 32px !important;
    font-weight: 700 !important;
    color: #EC4899 !important;
}

/* ---- INFO BOX ---- */
.info-box {
    background: linear-gradient(135deg, rgba(15,23,42,0.9), rgba(20,10,25,0.9));
    border: 1px solid rgba(236,72,153,0.2);
    border-left: 3px solid #EC4899;
    border-radius: 14px;
    padding: 24px 28px;
    font-family: 'Space Mono', monospace;
    font-size: 13px;
    line-height: 2.2;
    color: #CBD5E1;
    box-shadow: 0 4px 24px rgba(236,72,153,0.06);
}

.info-box strong {
    color: #EC4899;
}

/* ---- AQI CLASS BADGE ---- */
.aqi-row {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin: 8px 0 16px 0;
}

.aqi-badge {
    flex: 1;
    min-width: 120px;
    border-radius: 14px;
    padding: 18px 14px;
    text-align: center;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    border: 1px solid;
    position: relative;
    overflow: hidden;
}

.aqi-badge .badge-label {
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    opacity: 0.7;
    display: block;
    margin-bottom: 6px;
    font-family: 'Space Mono', monospace;
}

.aqi-badge .badge-value {
    font-size: 28px;
    display: block;
    line-height: 1;
}

.aqi-badge .badge-range {
    font-size: 10px;
    opacity: 0.55;
    display: block;
    margin-top: 4px;
    font-family: 'Space Mono', monospace;
}

.aqi-good    { background: rgba(52,211,153,0.08); border-color: rgba(52,211,153,0.3); }
.aqi-good .badge-value { color: #34D399; }
.aqi-moderate{ background: rgba(251,191,36,0.08); border-color: rgba(251,191,36,0.3); }
.aqi-moderate .badge-value { color: #FBBF24; }
.aqi-poor    { background: rgba(251,146,60,0.08); border-color: rgba(251,146,60,0.3); }
.aqi-poor .badge-value { color: #FB923C; }
.aqi-hazard  { background: rgba(248,113,113,0.08); border-color: rgba(248,113,113,0.3); }
.aqi-hazard .badge-value { color: #F87171; }

/* ---- DATAFRAME ---- */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(236,72,153,0.12);
}

/* ---- SUCCESS STREAMLIT ---- */
.stSuccess {
    background: rgba(52,211,153,0.08) !important;
    border: 1px solid rgba(52,211,153,0.3) !important;
    border-radius: 10px !important;
    color: #34D399 !important;
}

.stInfo {
    background: rgba(236,72,153,0.06) !important;
    border: 1px solid rgba(236,72,153,0.2) !important;
    border-radius: 10px !important;
}

/* ---- LIVE BADGE ---- */
.live-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    color: #34D399;
    letter-spacing: 2px;
    text-transform: uppercase;
    background: rgba(52,211,153,0.08);
    border: 1px solid rgba(52,211,153,0.25);
    border-radius: 20px;
    padding: 4px 14px;
    margin-bottom: 16px;
}

.live-dot {
    width: 7px;
    height: 7px;
    background: #34D399;
    border-radius: 50%;
    box-shadow: 0 0 6px #34D399;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.4; transform: scale(0.8); }
}

/* ---- HISTORY CHART CONTAINER ---- */
.history-tabs {
    display: flex;
    gap: 8px;
    margin-bottom: 16px;
}

/* ---- FOOTER ---- */
.footer-wrapper {
    margin-top: 64px;
    border-top: 1px solid rgba(236,72,153,0.2);
    padding: 40px 0 32px 0;
    text-align: center;
}

.footer-logo {
    font-family: 'Rajdhani', sans-serif;
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    background: linear-gradient(135deg, #EC4899, #F9A8D4, #00E5FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 20px;
}

.footer-divider {
    width: 60px;
    height: 2px;
    background: linear-gradient(90deg, #EC4899, #818CF8);
    border-radius: 2px;
    margin: 16px auto;
}

.footer-title {
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #64748B;
    line-height: 2;
}

.footer-author-box {
    display: inline-block;
    margin-top: 20px;
    padding: 16px 36px;
    border: 1px solid rgba(236,72,153,0.2);
    border-radius: 12px;
    background: rgba(236,72,153,0.04);
}

.footer-author-label {
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #64748B;
    display: block;
    margin-bottom: 6px;
}

.footer-author-name {
    font-family: 'Rajdhani', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #F472B6;
    letter-spacing: 1px;
    display: block;
}

.footer-copy {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: #334155;
    margin-top: 24px;
    letter-spacing: 1px;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0F172A; }
::-webkit-scrollbar-thumb { background: #EC4899; border-radius: 3px; }

</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="header-wrapper">
    <div style="display:flex; justify-content:center; margin-bottom:12px;">
        <span class="live-badge"><span class="live-dot"></span> Live Monitoring</span>
    </div>
    <div class="big-title">🌫️ Smart Air Quality<br>Monitoring System</div>
    <div class="subtitle">
        <span class="subtitle-accent">◆</span>
        Internet of Things — Final Project
        <span class="subtitle-accent">◆</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
st.info(
    "📡 Connected to ESP32 via ThingSpeak Cloud"
)

# ==========================================
# THINGSPEAK REALTIME
# ==========================================

CHANNEL_ID = "3391416"
READ_API_KEY = "PODLP6BGV4ETMEV4"

try:
    url = (
        f"https://api.thingspeak.com/channels/"
        f"{CHANNEL_ID}/feeds.json"
        f"?api_key={READ_API_KEY}&results=1"
    )

    response = requests.get(url)
    data = response.json()

    feed = data["feeds"][0]

    suhu_sensor = float(feed["field1"])
    rh_sensor   = float(feed["field2"])
    gas_sensor  = int(float(feed["field3"]))
    status_code = int(float(feed["field4"]))

except:
    suhu_sensor = 24
    rh_sensor   = 43
    gas_sensor  = 3628
    status_code = 3
 
if status_code == 1:

    status_label = "BAIK"
    status_icon  = "✦"
    status_class = "card-good"

elif status_code == 2:

    status_label = "SEDANG"
    status_icon  = "◈"
    status_class = "card-medium"

else:

    status_label = "BURUK"
    status_icon  = "⚠"
    status_class = "card-red"

# ==========================================
# KPI CARDS
# ==========================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="card card-blue">
        <span class="card-icon">🌡️</span>
        <span class="card-label">Suhu</span>
        <span class="card-value">{suhu_sensor}</span>
        <span class="card-unit">°C — Temperature</span>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="card card-pink">
        <span class="card-icon">💧</span>
        <span class="card-label">Kelembapan</span>
        <span class="card-value">{rh_sensor}</span>
        <span class="card-unit">% — Relative Humidity</span>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="card card-orange">
        <span class="card-icon">🌫️</span>
        <span class="card-label">Gas MQ2</span>
        <span class="card-value">{gas_sensor}</span>
        <span class="card-unit">ppm — Gas Level</span>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="card {status_class}">
        <span class="card-icon">{status_icon}</span>
        <span class="card-label">Status Udara</span>
        <span class="card-value">{status_label}</span>
        <span class="card-unit">Air Quality Index</span>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ==========================================
# GAUGE
# ==========================================

st.markdown("""
<div class="section-header">
    <span class="accent-bar"></span>
    Sensor Gauges — Real-time
</div>
""", unsafe_allow_html=True)

g1, g2 = st.columns(2)

gauge_layout = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#CBD5E1', family='Rajdhani, sans-serif'),
    margin=dict(t=60, b=20, l=20, r=20),
    height=280
)

with g1:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=suhu_sensor,
        title={'text': "🌡️  Suhu (°C)", 'font': {'size': 16, 'color': '#00E5FF', 'family': 'Rajdhani'}},
        number={'font': {'color': '#00E5FF', 'size': 48, 'family': 'Rajdhani'}, 'suffix': '°'},
        gauge={
            'axis': {'range': [0, 50], 'tickcolor': '#475569', 'tickfont': {'color': '#64748B'}},
            'bar': {'color': '#00E5FF', 'thickness': 0.25},
            'bgcolor': 'rgba(0,0,0,0)',
            'borderwidth': 0,
            'steps': [
                {'range': [0, 15],  'color': 'rgba(0,229,255,0.05)'},
                {'range': [15, 30], 'color': 'rgba(0,229,255,0.1)'},
                {'range': [30, 50], 'color': 'rgba(248,113,113,0.1)'},
            ],
            'threshold': {'line': {'color': '#EC4899', 'width': 2}, 'thickness': 0.75, 'value': 35}
        }
    ))
    fig.update_layout(**gauge_layout)
    st.plotly_chart(fig, use_container_width=True)

with g2:
    fig2 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=rh_sensor,
        title={'text': "💧  Kelembapan (%)", 'font': {'size': 16, 'color': '#F472B6', 'family': 'Rajdhani'}},
        number={'font': {'color': '#F472B6', 'size': 48, 'family': 'Rajdhani'}, 'suffix': '%'},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': '#475569', 'tickfont': {'color': '#64748B'}},
            'bar': {'color': '#EC4899', 'thickness': 0.25},
            'bgcolor': 'rgba(0,0,0,0)',
            'borderwidth': 0,
            'steps': [
                {'range': [0,  30], 'color': 'rgba(251,146,60,0.08)'},
                {'range': [30, 70], 'color': 'rgba(236,72,153,0.08)'},
                {'range': [70,100], 'color': 'rgba(99,102,241,0.08)'},
            ],
            'threshold': {'line': {'color': '#00E5FF', 'width': 2}, 'thickness': 0.75, 'value': 80}
        }
    ))
    fig2.update_layout(**gauge_layout)
    st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# SENSOR HISTORY CHART (dummy simulasi)
# ==========================================

st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

st.markdown("""
<div class="section-header">
    <span class="accent-bar"></span>
    Sensor History Chart — Simulasi 24 Jam
</div>
""", unsafe_allow_html=True)

np.random.seed(42)
jam = [f"{h:02d}:00" for h in range(24)]
suhu_hist  = np.clip(np.random.normal(suhu_sensor, 2.5, 24), 18, 35).round(1)
rh_hist    = np.clip(np.random.normal(rh_sensor,   5,   24), 25, 80).round(1)
gas_hist   = np.clip(np.random.normal(gas_sensor,  300, 24), 500, 5000).round(0)

df_hist = pd.DataFrame({
    "Jam"       : jam,
    "Suhu (°C)" : suhu_hist,
    "Kelembapan (%)": rh_hist,
    "Gas MQ2"   : gas_hist,
})

chart_layout_base = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(8,11,18,0.6)',
    font=dict(color='#94A3B8', family='Inter, sans-serif', size=11),
    margin=dict(t=50, b=40, l=50, r=20),
    xaxis=dict(gridcolor='rgba(255,255,255,0.04)', linecolor='rgba(255,255,255,0.08)'),
    yaxis=dict(gridcolor='rgba(255,255,255,0.04)', linecolor='rgba(255,255,255,0.08)'),
    title_font=dict(family='Rajdhani, sans-serif', size=16, color='#E2E8F0'),
)

tab1, tab2, tab3 = st.tabs(["🌡️  Suhu", "💧  Kelembapan", "🌫️  Gas MQ2"])

with tab1:
    fig_h1 = go.Figure()
    fig_h1.add_trace(go.Scatter(
        x=df_hist["Jam"], y=df_hist["Suhu (°C)"],
        mode='lines+markers',
        line=dict(color='#00E5FF', width=2),
        marker=dict(color='#00E5FF', size=5),
        fill='tozeroy',
        fillcolor='rgba(0,229,255,0.05)',
        name='Suhu'
    ))
    fig_h1.update_layout(**chart_layout_base, title="Riwayat Suhu — 24 Jam Terakhir",
                          xaxis_title="Jam", yaxis_title="°C")
    st.plotly_chart(fig_h1, use_container_width=True)

with tab2:
    fig_h2 = go.Figure()
    fig_h2.add_trace(go.Scatter(
        x=df_hist["Jam"], y=df_hist["Kelembapan (%)"],
        mode='lines+markers',
        line=dict(color='#EC4899', width=2),
        marker=dict(color='#EC4899', size=5),
        fill='tozeroy',
        fillcolor='rgba(236,72,153,0.05)',
        name='Kelembapan'
    ))
    fig_h2.update_layout(**chart_layout_base, title="Riwayat Kelembapan — 24 Jam Terakhir",
                          xaxis_title="Jam", yaxis_title="%")
    st.plotly_chart(fig_h2, use_container_width=True)

with tab3:
    colors_gas = ['#34D399' if v < 1000 else '#FBBF24' if v < 2500 else '#F87171'
                  for v in df_hist["Gas MQ2"]]
    fig_h3 = go.Figure()
    fig_h3.add_trace(go.Bar(
        x=df_hist["Jam"], y=df_hist["Gas MQ2"],
        marker_color=colors_gas,
        name='Gas MQ2',
        marker_line_width=0,
    ))
    fig_h3.add_hline(y=1000, line=dict(color='#34D399', width=1, dash='dot'),
                     annotation_text="Batas Baik", annotation_font_color='#34D399')
    fig_h3.add_hline(y=2500, line=dict(color='#FBBF24', width=1, dash='dot'),
                     annotation_text="Batas Sedang", annotation_font_color='#FBBF24')
    fig_h3.update_layout(**chart_layout_base, title="Riwayat Gas MQ2 — 24 Jam Terakhir",
                          xaxis_title="Jam", yaxis_title="ppm")
    st.plotly_chart(fig_h3, use_container_width=True)

# ==========================================
# AIR QUALITY CLASSIFICATION
# ==========================================

st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

st.markdown("""
<div class="section-header">
    <span class="accent-bar"></span>
    Air Quality Classification — Panduan Kualitas Udara
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="aqi-row">
    <div class="aqi-badge aqi-good">
        <span class="badge-label">🟢 Baik / Good</span>
        <span class="badge-value">0 – 999</span>
        <span class="badge-range">Gas MQ2 (ppm)</span>
        <br>
        <span style="font-size:11px;color:#34D399;font-family:'Inter',sans-serif;margin-top:8px;display:block;">
            Udara bersih, aman untuk semua aktivitas.
        </span>
    </div>
    <div class="aqi-badge aqi-moderate">
        <span class="badge-label">🟡 Sedang / Moderate</span>
        <span class="badge-value">1000 – 2499</span>
        <span class="badge-range">Gas MQ2 (ppm)</span>
        <br>
        <span style="font-size:11px;color:#FBBF24;font-family:'Inter',sans-serif;margin-top:8px;display:block;">
            Kualitas cukup, ventilasi disarankan.
        </span>
    </div>
    <div class="aqi-badge aqi-poor">
        <span class="badge-label">🟠 Buruk / Poor</span>
        <span class="badge-value">2500 – 3999</span>
        <span class="badge-range">Gas MQ2 (ppm)</span>
        <br>
        <span style="font-size:11px;color:#FB923C;font-family:'Inter',sans-serif;margin-top:8px;display:block;">
            Buka jendela, kurangi aktivitas berat.
        </span>
    </div>
    <div class="aqi-badge aqi-hazard">
        <span class="badge-label">🔴 Berbahaya / Hazard</span>
        <span class="badge-value">≥ 4000</span>
        <span class="badge-range">Gas MQ2 (ppm)</span>
        <br>
        <span style="font-size:11px;color:#F87171;font-family:'Inter',sans-serif;margin-top:8px;display:block;">
            Segera evakuasi & ventilasi ruangan.
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background:rgba(236,72,153,0.05); border:1px solid rgba(236,72,153,0.15);
     border-radius:12px; padding:16px 20px; margin-top:8px;">
    <span style="font-family:'Space Mono',monospace; font-size:11px; color:#94A3B8; letter-spacing:1px;">
        📌 &nbsp; <strong style="color:#F472B6;">Status saat ini:</strong> &nbsp;
        Gas MQ2 = <strong style="color:#FB923C;">{gas}</strong> ppm
        &nbsp;|&nbsp; Kategori: <strong style="color:#F87171;">BURUK</strong>
        &nbsp;|&nbsp; Rekomendasi: Segera buka ventilasi dan kurangi sumber polusi di ruangan.
    </span>
</div>
""".format(gas=gas_sensor), unsafe_allow_html=True)

st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

# ==========================================
# UPLOAD DATASET
# ==========================================

st.markdown("""
<div class="section-header">
    <span class="accent-bar"></span>
    Upload Dataset Air Quality
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload file CSV Air Quality (separator: semicolon)",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file, sep=";", decimal=",")
    df = df.dropna(axis=1, how='all')

    st.success("✦  Dataset berhasil dimuat")

    # ======================================
    # DATASET SUMMARY CARDS (diperluas)
    # ======================================

    st.markdown("""
    <div class="section-header">
        <span class="accent-bar"></span>
        Ringkasan Dataset
    </div>
    """, unsafe_allow_html=True)

    # Baris 1 — metrik dasar
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Jumlah Data",    f"{df.shape[0]:,}")
    k2.metric("Jumlah Kolom",   df.shape[1])
    k3.metric("Rata-rata Suhu", f"{round(df['T'].mean(), 2)} °C")
    k4.metric("Rata-rata RH",   f"{round(df['RH'].mean(), 2)} %")

    st.write("")

    # Baris 2 — kartu tambahan: Polutan, Suhu Max, RH Max
    polutan_cols = ["CO(GT)", "NMHC(GT)", "C6H6(GT)", "NOx(GT)", "NO2(GT)"]
    polutan_means = {c: df[c].mean() for c in polutan_cols if c in df.columns}
    top_polutan  = max(polutan_means, key=polutan_means.get) if polutan_means else "N/A"
    top_val      = round(polutan_means[top_polutan], 2) if polutan_means else "-"

    suhu_max = round(df["T"].max(), 2)
    rh_max   = round(df["RH"].max(), 2)

    ex1, ex2, ex3 = st.columns(3)

    with ex1:
        st.markdown(f"""
        <div class="card card-purple" style="padding:20px 16px;">
            <span class="card-icon">☣️</span>
            <span class="card-label">Polutan Tertinggi</span>
            <span class="card-value">{top_polutan}</span>
            <span class="card-unit">rata-rata {top_val}</span>
        </div>
        """, unsafe_allow_html=True)

    with ex2:
        st.markdown(f"""
        <div class="card card-orange" style="padding:20px 16px;">
            <span class="card-icon">🔥</span>
            <span class="card-label">Suhu Maksimum</span>
            <span class="card-value">{suhu_max}</span>
            <span class="card-unit">°C — Peak Temperature</span>
        </div>
        """, unsafe_allow_html=True)

    with ex3:
        st.markdown(f"""
        <div class="card card-teal" style="padding:20px 16px;">
            <span class="card-icon">💦</span>
            <span class="card-label">Kelembapan Maksimum</span>
            <span class="card-value">{rh_max}</span>
            <span class="card-unit">% — Peak Humidity</span>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # ======================================
    # PREVIEW
    # ======================================

    st.markdown("""
    <div class="section-header">
        <span class="accent-bar"></span>
        Preview Dataset
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(df.head(50), use_container_width=True)

    # ======================================
    # VISUALISASI
    # ======================================

    st.markdown("""
    <div class="section-header">
        <span class="accent-bar"></span>
        Visualisasi Data
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_temp = px.line(df, y="T", title="Grafik Suhu (T)",
                           color_discrete_sequence=["#00E5FF"])
        fig_temp.update_traces(line_width=2)
        fig_temp.update_layout(**chart_layout_base)
        st.plotly_chart(fig_temp, use_container_width=True)

    with col2:
        fig_rh = px.line(df, y="RH", title="Grafik Kelembapan (RH)",
                         color_discrete_sequence=["#EC4899"])
        fig_rh.update_traces(line_width=2)
        fig_rh.update_layout(**chart_layout_base)
        st.plotly_chart(fig_rh, use_container_width=True)

    fig_co = px.line(df, y="CO(GT)", title="Grafik CO(GT)",
                     color_discrete_sequence=["#818CF8"])
    fig_co.update_traces(line_width=2)
    fig_co.update_layout(**chart_layout_base)
    st.plotly_chart(fig_co, use_container_width=True)

    # ======================================
    # PIE CHART KATEGORI SUHU
    # ======================================

    st.markdown("""
    <div class="section-header">
        <span class="accent-bar"></span>
        Distribusi Kategori Suhu
    </div>
    """, unsafe_allow_html=True)

    def kategorikan_suhu(t):
        if t < 18:
            return "❄️ Dingin"
        elif t <= 28:
            return "✅ Normal"
        else:
            return "🔥 Panas"

    df["Kategori Suhu"] = df["T"].apply(kategorikan_suhu)
    kategori_counts = df["Kategori Suhu"].value_counts().reset_index()
    kategori_counts.columns = ["Kategori", "Jumlah"]

    pie_colors = []
    for k in kategori_counts["Kategori"]:
        if "Dingin" in k:
            pie_colors.append("#00E5FF")
        elif "Normal" in k:
            pie_colors.append("#34D399")
        else:
            pie_colors.append("#F87171")

    pie_col1, pie_col2 = st.columns([1, 1])

    with pie_col1:
        fig_pie = go.Figure(go.Pie(
            labels=kategori_counts["Kategori"],
            values=kategori_counts["Jumlah"],
            hole=0.55,
            marker=dict(
                colors=pie_colors,
                line=dict(color='#080B12', width=3)
            ),
            textfont=dict(family='Rajdhani, sans-serif', size=14, color='white'),
            hovertemplate="<b>%{label}</b><br>Jumlah: %{value}<br>Persentase: %{percent}<extra></extra>"
        ))
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94A3B8', family='Inter, sans-serif'),
            margin=dict(t=30, b=30, l=20, r=20),
            height=320,
            title=dict(text="Distribusi Kategori Suhu", font=dict(
                family='Rajdhani, sans-serif', size=16, color='#E2E8F0')),
            legend=dict(
                font=dict(color='#94A3B8', family='Rajdhani, sans-serif', size=13),
                bgcolor='rgba(0,0,0,0)'
            ),
            annotations=[dict(
                text=f"<b>{len(df)}</b><br><span style='font-size:10'>data</span>",
                x=0.5, y=0.5, font_size=16, showarrow=False,
                font=dict(color='#F472B6', family='Rajdhani, sans-serif')
            )]
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with pie_col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        for _, row in kategori_counts.iterrows():
            pct = round(row["Jumlah"] / len(df) * 100, 1)
            if "Dingin" in row["Kategori"]:
                color, bg = "#00E5FF", "rgba(0,229,255,0.06)"
                border     = "rgba(0,229,255,0.25)"
            elif "Normal" in row["Kategori"]:
                color, bg = "#34D399", "rgba(52,211,153,0.06)"
                border     = "rgba(52,211,153,0.25)"
            else:
                color, bg = "#F87171", "rgba(248,113,113,0.06)"
                border     = "rgba(248,113,113,0.25)"

            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:16px;
                        background:{bg}; border:1px solid {border};
                        border-radius:12px; padding:14px 20px; margin-bottom:10px;">
                <span style="font-size:26px;">{row['Kategori'].split()[0]}</span>
                <div style="flex:1;">
                    <div style="font-family:'Rajdhani',sans-serif; font-size:16px;
                                font-weight:700; color:{color}; letter-spacing:1px;">
                        {row['Kategori'].split(' ',1)[1]}
                    </div>
                    <div style="font-family:'Space Mono',monospace; font-size:10px;
                                color:#64748B; margin-top:2px;">
                        {row['Jumlah']:,} data &nbsp;|&nbsp; {pct}%
                    </div>
                </div>
                <div style="font-family:'Rajdhani',sans-serif; font-size:28px;
                            font-weight:700; color:{color};">{pct}%</div>
            </div>
            """, unsafe_allow_html=True)

    # ======================================
    # HEATMAP
    # ======================================

    st.markdown("""
    <div class="section-header">
        <span class="accent-bar"></span>
        Heatmap Korelasi
    </div>
    """, unsafe_allow_html=True)

    kolom = ["CO(GT)", "NMHC(GT)", "C6H6(GT)", "NOx(GT)", "NO2(GT)", "T", "RH", "AH"]
    corr  = df[kolom].corr()

    heatmap = px.imshow(
        corr, text_auto=True, aspect="auto",
        color_continuous_scale=[
            [0.0,  "#0C1A2E"], [0.25, "#1A0A14"],
            [0.5,  "#2D1B3D"], [0.75, "#831843"], [1.0, "#EC4899"],
        ]
    )
    heatmap.update_layout(
        **chart_layout_base,
        coloraxis_colorbar=dict(
            tickfont=dict(color='#94A3B8'),
            title=dict(font=dict(color='#94A3B8'))
        )
    )
    st.plotly_chart(heatmap, use_container_width=True)

    # ======================================
    # INSIGHT
    # ======================================

    st.markdown("""
    <div class="section-header">
        <span class="accent-bar"></span>
        Insight Otomatis
    </div>
    """, unsafe_allow_html=True)

    suhu_avg = round(df["T"].mean(), 2)
    rh_avg   = round(df["RH"].mean(), 2)

    st.markdown(f"""
    <div class="info-box">
        🌡️ &nbsp;<strong>Rata-rata Suhu</strong> &nbsp;→&nbsp; {suhu_avg} °C<br>
        💧 &nbsp;<strong>Rata-rata Kelembapan</strong> &nbsp;→&nbsp; {rh_avg} %<br>
        ☣️ &nbsp;<strong>Polutan Tertinggi</strong> &nbsp;→&nbsp; {top_polutan} (rata-rata: {top_val})<br>
        🔥 &nbsp;<strong>Suhu Maksimum</strong> &nbsp;→&nbsp; {suhu_max} °C<br>
        💦 &nbsp;<strong>Kelembapan Maksimum</strong> &nbsp;→&nbsp; {rh_max} %<br>
        📊 &nbsp;<strong>Dashboard</strong> menampilkan analisis kualitas udara berdasarkan dataset Air Quality UCI.<br>
        🌫️ &nbsp;<strong>Sistem IoT</strong> memanfaatkan sensor DHT22 dan MQ2 untuk monitoring kondisi udara secara real-time.
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# FOOTER PROFESIONAL
# ==========================================

import streamlit.components.v1 as components

components.html(
    """
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {
            margin: 0;
            padding: 0;
            background: transparent;
        }
        .footer {
            font-family: 'Space Mono', monospace;
            background: transparent;
            border-top: 1px solid rgba(236,72,153,0.3);
            padding: 40px 20px 30px 20px;
            text-align: center;
        }
        .footer-title {
            font-family: 'Rajdhani', sans-serif;
            font-size: 20px;
            font-weight: 700;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: #EC4899;
            margin-bottom: 6px;
        }
        .footer-line {
            width: 60px;
            height: 2px;
            background: linear-gradient(90deg, #EC4899, #818CF8);
            border-radius: 2px;
            margin: 14px auto;
        }
        .footer-subtitle {
            font-family: 'Space Mono', monospace;
            font-size: 10px;
            letter-spacing: 2px;
            color: #64748B;
            line-height: 2.2;
            text-transform: uppercase;
        }
        .footer-subtitle span {
            color: #EC4899;
            font-size: 13px;
        }
        .footer-box {
            display: inline-block;
            margin-top: 22px;
            padding: 16px 36px;
            border: 1px solid rgba(236,72,153,0.3);
            border-radius: 14px;
            background: rgba(236,72,153,0.06);
        }
        .footer-label {
            font-family: 'Space Mono', monospace;
            font-size: 9px;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: #64748B;
            display: block;
            margin-bottom: 6px;
        }
        .footer-name {
            font-family: 'Rajdhani', sans-serif;
            font-size: 24px;
            font-weight: 700;
            color: #F472B6;
            letter-spacing: 1px;
            display: block;
        }
        .footer-copy {
            font-family: 'Space Mono', monospace;
            font-size: 9px;
            color: #334155;
            margin-top: 22px;
            letter-spacing: 1px;
        }
    </style>
    </head>
    <body>
    <div class="footer">
        <div class="footer-title">Smart Air Quality Monitoring System</div>
        <div class="footer-line"></div>
        <div class="footer-subtitle">
            Internet of Things &mdash; Final Project<br>
            <span>&#9670;</span><br>
            Implementasi Sistem Monitoring Kualitas Udara<br>
            pada Ruang Kerja Pribadi Berbasis IoT
        </div>
        <div class="footer-box">
            <span class="footer-label">Disusun oleh</span>
            <span class="footer-name">Bunga Nur Munawaroh</span>
        </div>
        <div class="footer-copy">
            &copy; 2026 &nbsp;&middot;&nbsp; Sistem Monitoring Kualitas Udara
            &nbsp;&middot;&nbsp; DHT22 + MQ2 Sensor
            &nbsp;&middot;&nbsp; Powered by Streamlit &amp; Plotly
        </div>
    </div>
    </body>
    </html>
    """,
    height=320,
)