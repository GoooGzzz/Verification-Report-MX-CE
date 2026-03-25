import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import io
import warnings
warnings.filterwarnings('ignore')

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SmartSense-LTD | MX Field Intelligence",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── PREMIUM CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Orbitron:wght@400;600;700;900&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
[data-testid="stAppViewContainer"] {
    background: linear-gradient(160deg, #04060e 0%, #080d1c 40%, #04060e 100%) !important;
    min-height: 100vh;
}
.main { background: transparent !important; }

/* ── ANIMATIONS ── */
@keyframes fadeIn   { from { opacity:0 } to { opacity:1 } }
@keyframes fadeOut  { from { opacity:1 } to { opacity:0 } }
@keyframes slideUp  { from { opacity:0; transform:translateY(30px) } to { opacity:1; transform:translateY(0) } }
@keyframes slideIn  { from { opacity:0; transform:translateX(-20px) } to { opacity:1; transform:translateX(0) } }
@keyframes glow     { 0%,100%{text-shadow:0 0 20px rgba(20,40,160,.6),0 0 40px rgba(0,153,213,.3)} 50%{text-shadow:0 0 40px rgba(0,153,213,.9),0 0 80px rgba(100,255,218,.5),0 0 120px rgba(20,40,160,.4)} }
@keyframes barUp    { from{transform:scaleY(0)} to{transform:scaleY(1)} }
@keyframes scanline { 0%{top:-10%} 100%{top:110%} }
@keyframes borderPulse { 0%,100%{border-color:rgba(20,40,160,.4)} 50%{border-color:rgba(100,255,218,.6)} }
@keyframes rotateBg { 0%{transform:rotate(0deg)} 100%{transform:rotate(360deg)} }
@keyframes shimmer  { 0%{background-position:-200% 0} 100%{background-position:200% 0} }
@keyframes countUp  { from{opacity:0;transform:scale(.8)} to{opacity:1;transform:scale(1)} }
@keyframes gridMove { from{background-position:0 0} to{background-position:50px 50px} }
@keyframes float    { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }

/* ── AUTH SCREEN ── */
.auth-wrap {
    display:flex; flex-direction:column; align-items:center; justify-content:center;
    min-height:88vh; gap:0;
}
.auth-bg-grid {
    position:fixed; top:0; left:0; right:0; bottom:0; z-index:0;
    background-image: linear-gradient(rgba(20,40,160,.07) 1px, transparent 1px),
                      linear-gradient(90deg, rgba(20,40,160,.07) 1px, transparent 1px);
    background-size:60px 60px;
    animation: gridMove 8s linear infinite;
}
.auth-card {
    position:relative; z-index:1;
    background: rgba(12,15,30,.85);
    border:1px solid rgba(100,255,218,.15);
    border-radius:28px; padding:56px 64px;
    backdrop-filter: blur(24px);
    box-shadow: 0 40px 80px rgba(0,0,0,.6), 0 0 120px rgba(20,40,160,.12), inset 0 1px 0 rgba(255,255,255,.05);
    text-align:center; max-width:480px; width:100%;
    animation: fadeIn .6s ease, borderPulse 3s ease infinite;
}
.auth-logo {
    font-family:'Orbitron',monospace; font-size:13px; font-weight:700;
    letter-spacing:6px; color:#64ffda; text-transform:uppercase;
    margin-bottom:8px; animation: slideUp .6s ease .1s both;
}
.auth-division {
    font-family:'Orbitron',monospace; font-size:11px;
    letter-spacing:4px; color:#4a5580; text-transform:uppercase;
    margin-bottom:32px; animation: slideUp .6s ease .2s both;
}
.auth-icon {
    font-size:56px; margin-bottom:16px; display:block;
    animation: float 3s ease infinite, slideUp .6s ease .3s both;
}
.auth-title {
    font-family:'Orbitron',monospace;
    background: linear-gradient(135deg, #1428A0, #0099D5, #64ffda);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    font-size:22px; font-weight:900; letter-spacing:2px; margin-bottom:8px;
    animation: slideUp .6s ease .4s both;
}
.auth-sub {
    color:#4a5580; font-size:12px; letter-spacing:2px; text-transform:uppercase;
    margin-bottom:32px; animation: slideUp .6s ease .5s both;
}
.auth-divider {
    width:100%; height:1px; margin:0 0 32px 0;
    background: linear-gradient(90deg, transparent, rgba(20,40,160,.5), rgba(100,255,218,.4), rgba(20,40,160,.5), transparent);
    animation: slideUp .6s ease .5s both;
}
.auth-footer {
    margin-top:24px; color:#2d3250; font-size:10px; letter-spacing:3px;
    text-transform:uppercase; animation: slideUp .6s ease .9s both;
}

/* ── SPLASH SCREEN ── */
.splash-wrap {
    min-height:90vh; display:flex; flex-direction:column;
    align-items:center; justify-content:center; gap:20px;
    background: radial-gradient(ellipse 80% 60% at 50% 50%, rgba(20,40,160,.15) 0%, transparent 70%),
                radial-gradient(ellipse 60% 40% at 50% 80%, rgba(0,153,213,.08) 0%, transparent 70%);
    border-radius:20px; position:relative; overflow:hidden;
}
.splash-grid {
    position:absolute; top:0; left:0; right:0; bottom:0;
    background-image: linear-gradient(rgba(20,40,160,.06) 1px, transparent 1px),
                      linear-gradient(90deg, rgba(20,40,160,.06) 1px, transparent 1px);
    background-size:50px 50px; border-radius:20px;
}
.splash-scanline {
    position:absolute; left:0; right:0; height:2px;
    background: linear-gradient(90deg, transparent, rgba(100,255,218,.3), transparent);
    animation: scanline 4s linear infinite; pointer-events:none;
}
.splash-company {
    font-family:'Orbitron',monospace; font-size:12px; font-weight:600;
    letter-spacing:8px; color:#64ffda; text-transform:uppercase;
    animation: slideUp .7s ease .1s both;
}
.splash-eyebrow {
    font-size:11px; letter-spacing:5px; color:#4a5580; text-transform:uppercase;
    animation: slideUp .7s ease .2s both;
}
.splash-title {
    font-family:'Orbitron',monospace;
    font-size:clamp(26px,3.5vw,52px); font-weight:900;
    background: linear-gradient(135deg, #1428A0 0%, #0099D5 45%, #64ffda 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    text-align:center; letter-spacing:4px; line-height:1.15;
    animation: slideUp .7s ease .3s both, glow 3s ease infinite 1s;
}
.splash-sub {
    color:#8892b0; font-size:15px; letter-spacing:3px; text-transform:uppercase;
    animation: slideUp .7s ease .5s both;
}
.splash-divider {
    width:320px; height:1px;
    background: linear-gradient(90deg, transparent, #1428A0 30%, #64ffda 50%, #1428A0 70%, transparent);
    animation: slideUp .7s ease .6s both;
}
.splash-bars {
    display:flex; align-items:flex-end; gap:5px; height:70px;
    animation: slideUp .7s ease .7s both;
}
.splash-bar {
    border-radius:3px 3px 0 0;
    background: linear-gradient(0deg, #1428A0, #0099D5, #64ffda);
    transform-origin:bottom; animation: barUp 1.2s cubic-bezier(.34,1.56,.64,1) both;
}
.splash-stats {
    display:flex; gap:48px;
    animation: slideUp .7s ease .9s both;
}
.splash-stat { text-align:center; }
.splash-stat-val {
    font-family:'Orbitron',monospace; font-size:26px; font-weight:700;
    animation: countUp .6s ease 1.2s both;
}
.splash-stat-lbl { color:#4a5580; font-size:10px; letter-spacing:3px; text-transform:uppercase; margin-top:4px; }
.splash-tagline {
    color:#64ffda; font-size:13px; font-style:italic; opacity:.8;
    animation: slideUp .7s ease 1.1s both;
}
.splash-sig {
    font-family:'Orbitron',monospace; color:#2d3250; font-size:10px;
    letter-spacing:5px; text-transform:uppercase;
    animation: slideUp .7s ease 1.3s both;
}

/* ── COMPANY HEADER ── */
.company-header {
    background: linear-gradient(135deg, rgba(20,40,160,.12), rgba(0,153,213,.08), rgba(100,255,218,.04));
    border:1px solid rgba(20,40,160,.3); border-radius:16px;
    padding:14px 24px; margin-bottom:20px;
    display:flex; align-items:center; justify-content:space-between;
    animation: slideIn .5s ease;
}
.ch-left { display:flex; align-items:center; gap:12px; }
.ch-company {
    font-family:'Orbitron',monospace; font-size:13px; font-weight:700;
    color:#64ffda; letter-spacing:3px; text-transform:uppercase;
}
.ch-division {
    font-size:11px; color:#4a5580; letter-spacing:2px; text-transform:uppercase;
}
.ch-right { display:flex; align-items:center; gap:20px; }
.ch-badge {
    background: rgba(20,40,160,.25); border:1px solid rgba(20,40,160,.5);
    border-radius:8px; padding:4px 12px;
    font-size:10px; font-weight:700; color:#0099D5; letter-spacing:2px; text-transform:uppercase;
}
.ch-sig { color:#2d3250; font-size:10px; letter-spacing:2px; }

/* ── KPI CARDS ── */
.kpi-card {
    background: linear-gradient(135deg, rgba(18,22,40,.95) 0%, rgba(24,28,50,.95) 100%);
    border:1px solid rgba(45,50,80,.7); border-radius:20px;
    padding:22px 24px; text-align:center;
    box-shadow: 0 8px 32px rgba(0,0,0,.4), inset 0 1px 0 rgba(255,255,255,.04);
    transition: all .3s cubic-bezier(.4,0,.2,1);
    backdrop-filter: blur(12px); position:relative; overflow:hidden;
}
.kpi-card::before {
    content:''; position:absolute; top:0; left:0; right:0; height:2px;
    background: linear-gradient(90deg, transparent, rgba(20,40,160,.8), rgba(100,255,218,.6), rgba(20,40,160,.8), transparent);
}
.kpi-card:hover { transform:translateY(-5px); box-shadow:0 20px 60px rgba(0,0,0,.5), 0 0 30px rgba(20,40,160,.2); border-color:rgba(100,255,218,.2); }
.kpi-label { color:#6272a4; font-size:10px; font-weight:700; letter-spacing:2px; text-transform:uppercase; margin-bottom:12px; }
.kpi-value { color:#e6f1ff; font-size:34px; font-weight:800; line-height:1; font-variant-numeric:tabular-nums; }
.kpi-sub { color:#64ffda; font-size:12px; margin-top:8px; font-weight:500; letter-spacing:.5px; }

/* ── SECTION HEADERS ── */
.section-header {
    color:#ccd6f6; font-size:15px; font-weight:700;
    padding:10px 0 10px 16px;
    border-left:3px solid;
    border-image: linear-gradient(180deg, #1428A0, #64ffda) 1;
    border-bottom:1px solid rgba(45,50,80,.4);
    margin-bottom:20px; letter-spacing:.5px;
    background: linear-gradient(90deg, rgba(20,40,160,.08), transparent);
}

/* ── ALERTS ── */
.alert-danger { background:rgba(255,83,83,.07); border:1px solid rgba(255,83,83,.3); border-radius:12px; padding:16px; margin:8px 0; }
.alert-warning { background:rgba(255,193,7,.07); border:1px solid rgba(255,193,7,.3); border-radius:12px; padding:16px; margin:8px 0; }
.alert-success { background:rgba(100,255,218,.07); border:1px solid rgba(100,255,218,.3); border-radius:12px; padding:16px; margin:8px 0; }

/* ── SIDEBAR ── */
div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080b18 0%, #0c1020 100%) !important;
    border-right:1px solid rgba(20,40,160,.25) !important;
}
div[data-testid="stSidebar"]::before {
    content:''; position:absolute; top:0; right:0; width:1px; height:100%;
    background: linear-gradient(180deg, transparent, rgba(100,255,218,.3) 30%, rgba(20,40,160,.5) 70%, transparent);
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(12,15,28,.9) !important; border-radius:14px; padding:5px;
    border:1px solid rgba(45,50,80,.5) !important; backdrop-filter:blur(12px);
    gap:2px !important;
}
.stTabs [data-baseweb="tab"] { color:#6272a4 !important; border-radius:10px !important; font-weight:600 !important; font-size:13px !important; transition:all .2s !important; }
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1428A0, #0099D5) !important;
    color:white !important;
    box-shadow:0 4px 16px rgba(20,40,160,.5) !important;
}
.stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) { color:#ccd6f6 !important; background:rgba(20,40,160,.1) !important; }

/* ── INSIGHT BOX ── */
.insight-box {
    background: linear-gradient(135deg, rgba(8,18,32,.95), rgba(15,25,52,.95));
    border:1px solid rgba(20,40,160,.35); border-radius:18px;
    padding:28px; margin:12px 0; white-space:pre-wrap;
    color:#ccd6f6; line-height:1.85; font-size:14px;
    box-shadow:0 12px 40px rgba(0,0,0,.35), inset 0 1px 0 rgba(100,255,218,.05);
}

/* ── SCORE CARDS ── */
.score-card {
    background:rgba(14,17,35,.9); border:1px solid rgba(45,50,80,.7);
    border-radius:18px; padding:22px; text-align:center; margin:4px;
    backdrop-filter:blur(12px); transition:transform .2s, box-shadow .2s;
    box-shadow:0 4px 20px rgba(0,0,0,.3);
}
.score-card:hover { transform:translateY(-3px); box-shadow:0 12px 40px rgba(0,0,0,.5); }
.score-a { border-top:3px solid #64ffda; }
.score-b { border-top:3px solid #1DB954; }
.score-c { border-top:3px solid #ffb347; }
.score-d { border-top:3px solid #ff5353; }

/* ── ALERT FEED ── */
.alert-feed-drop {
    background:rgba(14,17,35,.8); border-left:4px solid #ff5353;
    border-radius:0 14px 14px 0; padding:14px 18px; margin:6px 0;
    box-shadow:0 4px 16px rgba(0,0,0,.3); transition:transform .15s;
}
.alert-feed-drop:hover { transform:translateX(3px); }
.alert-feed-rise {
    background:rgba(14,17,35,.8); border-left:4px solid #64ffda;
    border-radius:0 14px 14px 0; padding:14px 18px; margin:6px 0;
    box-shadow:0 4px 16px rgba(0,0,0,.3); transition:transform .15s;
}
.alert-feed-rise:hover { transform:translateX(3px); }

/* ── STORE PROFILE ── */
.store-profile {
    background: linear-gradient(135deg, rgba(8,18,32,.95), rgba(15,25,52,.95));
    border:1px solid rgba(45,50,80,.7); border-radius:22px; padding:28px; margin:12px 0;
    backdrop-filter:blur(12px); box-shadow:0 12px 40px rgba(0,0,0,.35);
}

/* ── FOOTER ── */
.app-footer {
    background: linear-gradient(90deg, rgba(20,40,160,.1), rgba(0,153,213,.06), rgba(20,40,160,.1));
    border:1px solid rgba(45,50,80,.4); border-radius:14px;
    padding:16px 28px; margin-top:32px;
    display:flex; justify-content:space-between; align-items:center;
}
.footer-left { color:#4a5580; font-size:11px; letter-spacing:1px; }
.footer-center { color:#2d3250; font-family:'Orbitron',monospace; font-size:10px; letter-spacing:3px; text-transform:uppercase; }
.footer-right { color:#2d3250; font-size:10px; letter-spacing:1px; }

/* ── MISC ── */
.stButton > button { border-radius:12px !important; font-weight:600 !important; letter-spacing:.5px !important; transition:all .2s !important; }
.stButton > button:hover { transform:translateY(-2px) !important; box-shadow:0 8px 24px rgba(0,0,0,.4) !important; }
[data-testid="stSelectbox"] > div > div { border-radius:10px !important; background:rgba(14,17,35,.8) !important; }
[data-testid="stTextInput"] > div > div { border-radius:10px !important; background:rgba(14,17,35,.8) !important; }
div[data-testid="metric-container"] { background:rgba(18,22,40,.8); border:1px solid rgba(45,50,80,.5); border-radius:14px; padding:16px; }
.stDataFrame { border-radius:14px !important; overflow:hidden; }
.stSlider [data-baseweb="slider"] { margin-top:8px; }
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE INIT ────────────────────────────────────────────────────────
for key, val in [('authenticated', False), ('splash_done', False), ('api_key', '')]:
    if key not in st.session_state:
        st.session_state[key] = val

# ══════════════════════════════════════════════════════════════════════════════
# AUTH GATE
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.authenticated:
    st.markdown('<div class="auth-bg-grid"></div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-wrap">', unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        st.markdown("""
        <div class="auth-card">
            <div class="auth-logo">SmartSense-LTD</div>
            <div class="auth-division">Division MX &nbsp;·&nbsp; Field Intelligence Platform</div>
            <span class="auth-icon">🔐</span>
            <div class="auth-title">SECURE ACCESS</div>
            <div class="auth-sub">Authorized Personnel Only</div>
            <div class="auth-divider"></div>
        </div>
        """, unsafe_allow_html=True)

        password = st.text_input(
            "Enter Access Password",
            type="password",
            placeholder="••••••••",
            key="pw_input",
            label_visibility="collapsed"
        )
        st.markdown("<br>", unsafe_allow_html=True)
        login_btn = st.button("🔓  ENTER INTELLIGENCE HUB", type="primary", use_container_width=True)

        if login_btn or (password and password == "solidspy"):
            if password == "solidspy":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.markdown('<div class="alert-danger" style="text-align:center">⛔ <b>Access Denied</b> — Invalid credentials</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="auth-footer">⚡ Innovation Dep · SmartSense-LTD · 2026</div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# CINEMATIC SPLASH SCREEN
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.splash_done:
    bars_html = "".join([
        f'<div class="splash-bar" style="width:14px;height:{h}px;animation-delay:{d}s"></div>'
        for h, d in [(28,.8),(45,.9),(62,1.0),(78,1.1),(55,1.2),(90,1.3),(42,1.4),(70,1.5),(35,1.6),(85,1.7),(60,1.8),(48,1.9),(76,2.0),(30,2.1),(65,2.2)]
    ])

    st.markdown(f"""
    <div class="splash-wrap">
        <div class="splash-grid"></div>
        <div class="splash-scanline"></div>

        <div class="splash-company">⚡ SmartSense-LTD</div>
        <div class="splash-eyebrow">Division MX &nbsp;·&nbsp; Field Intelligence Platform</div>

        <div class="splash-title">
            SAMSUNG FIELD<br>INTELLIGENCE HUB
        </div>
        <div class="splash-sub">Unlocking the Treasure of Your Data</div>

        <div class="splash-divider"></div>

        <div class="splash-bars">{bars_html}</div>

        <div class="splash-stats">
            <div class="splash-stat">
                <div class="splash-stat-val" style="color:#64ffda">360°</div>
                <div class="splash-stat-lbl">Market<br>Visibility</div>
            </div>
            <div class="splash-stat">
                <div class="splash-stat-val" style="color:#0099D5">AI</div>
                <div class="splash-stat-lbl">Powered<br>Insights</div>
            </div>
            <div class="splash-stat">
                <div class="splash-stat-val" style="color:#1428A0">∞</div>
                <div class="splash-stat-lbl">Real-Time<br>Intelligence</div>
            </div>
            <div class="splash-stat">
                <div class="splash-stat-val" style="color:#ffb347">8K</div>
                <div class="splash-stat-lbl">Data<br>Resolution</div>
            </div>
        </div>

        <div class="splash-tagline">"From shelf to strategy — every insight, revealed."</div>

        <div class="splash-divider" style="width:200px;opacity:.5"></div>

        <div class="splash-sig">⚡ Signed · Innovation Dep · SmartSense-LTD · 2026</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    _, c, _ = st.columns([1, 1, 1])
    with c:
        if st.button("▶  LAUNCH INTELLIGENCE HUB", type="primary", use_container_width=True):
            st.session_state.splash_done = True
            st.rerun()
    st.stop()

# ─── COLORS & LAYOUT DEFAULTS ─────────────────────────────────────────────────
COLORS = {
    'Samsung': '#1428A0', 'Oppo': '#1C7C54', 'Realme': '#FFB900',
    'Xiaomi': '#FF6900', 'Infinix': '#7B2D8B', 'Vivo': '#0057A8',
    'Honor': '#C8102E', 'Apple': '#555555', 'Tecno': '#00B0F0', 'Others': '#888888',
}
CL = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font_color='#ccd6f6', font_family='Inter',
    legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='rgba(45,50,80,.5)', borderwidth=1),
    margin=dict(t=20, b=20, l=10, r=10)
)

# ─── DATA FUNCTIONS ───────────────────────────────────────────────────────────
@st.cache_data
def load_data(file):
    df = pd.read_excel(file)
    df.columns = df.columns.str.strip()
    for col in ['Sellout', 'Shelf Share', 'Price']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    df['is_samsung'] = df['Brand'] == 'Samsung'
    return df

@st.cache_data
def detect_anomalies(df):
    flags = []

    # Single-model 100% shelf
    ss100 = df[df['Shelf Share'] == 100][['W', 'Shop Code', 'Shop Name', 'Brand', 'Model', 'Shelf Share']].copy()
    ss100['Issue'] = '🔴 Shelf Share = 100% (impossible single model)'
    ss100['Severity'] = 'HIGH'
    flags.append(ss100)

    # Brand shelf total > 100%
    shelf_total = df.groupby(['W', 'Shop Code', 'Brand'])['Shelf Share'].sum().reset_index()
    shelf_total.columns = ['W', 'Shop Code', 'Brand', 'Total_SS']
    over100 = shelf_total[shelf_total['Total_SS'] > 100].merge(
        df[['Shop Code', 'Shop Name']].drop_duplicates(), on='Shop Code', how='left')
    over100['Model'] = '—'
    over100['Shelf Share'] = over100['Total_SS']
    over100['Issue'] = over100['Total_SS'].apply(lambda x: f'🟠 Brand shelf share total = {x:.0f}% (exceeds 100%)')
    over100['Severity'] = 'MEDIUM'
    flags.append(over100[['W', 'Shop Code', 'Shop Name', 'Brand', 'Model', 'Shelf Share', 'Issue', 'Severity']])

    # Statistical sellout outliers
    mean_s, std_s = df['Sellout'].mean(), df['Sellout'].std()
    if std_s > 0:
        high_sell = df[df['Sellout'] > mean_s + 3 * std_s][['W', 'Shop Code', 'Shop Name', 'Brand', 'Model', 'Sellout']].copy()
        high_sell = high_sell.rename(columns={'Sellout': 'Shelf Share'})
        high_sell['Issue'] = high_sell['Shelf Share'].apply(lambda x: f'🟡 Sellout = {x:.0f} units (statistical outlier)')
        high_sell['Severity'] = 'MEDIUM'
        flags.append(high_sell[['W', 'Shop Code', 'Shop Name', 'Brand', 'Model', 'Shelf Share', 'Issue', 'Severity']])

    valid = [f for f in flags if len(f) > 0]
    return pd.concat(valid, ignore_index=True) if valid else pd.DataFrame(
        columns=['W', 'Shop Code', 'Shop Name', 'Brand', 'Model', 'Shelf Share', 'Issue', 'Severity'])

@st.cache_data
def build_store_agg(df):
    sa = df.groupby(['Shop Code', 'Shop Name', 'Project']).agg(
        Total_Sellout=('Sellout', 'sum'),
        Sam_Sellout=('Sellout', lambda x: x[df.loc[x.index, 'Brand'] == 'Samsung'].sum()),
        Sam_Shelf=('Shelf Share', lambda x: x[df.loc[x.index, 'Brand'] == 'Samsung'].mean()),
        Brands_Stocked=('Brand', 'nunique'),
        Models_Stocked=('Model', 'nunique'),
    ).reset_index()
    sa['Sam_Sellout'] = sa['Sam_Sellout'].fillna(0)
    sa['Sam_Share_Pct'] = (sa['Sam_Sellout'] / sa['Total_Sellout'] * 100).round(1).fillna(0)
    sa['Sam_Shelf'] = sa['Sam_Shelf'].fillna(0).round(1)
    return sa

@st.cache_data
def build_wow_alerts(df):
    weekly = df[df['Brand'] == 'Samsung'].groupby(['W', 'Shop Code', 'Shop Name'])['Sellout'].sum().reset_index()
    weeks = sorted(weekly['W'].unique())
    alerts = []
    for i in range(1, len(weeks)):
        prev = weekly[weekly['W'] == weeks[i - 1]][['Shop Code', 'Shop Name', 'Sellout']].rename(columns={'Sellout': 'Prev'})
        curr = weekly[weekly['W'] == weeks[i]][['Shop Code', 'Shop Name', 'Sellout']].rename(columns={'Sellout': 'Curr'})
        m = prev.merge(curr, on=['Shop Code', 'Shop Name'], how='outer').fillna(0)
        m['Change_Pct'] = ((m['Curr'] - m['Prev']) / m['Prev'].replace(0, 1) * 100).round(1)
        m['From_Week'] = weeks[i - 1]
        m['To_Week'] = weeks[i]
        alerts.append(m)
    return pd.concat(alerts, ignore_index=True) if alerts else pd.DataFrame()

def generate_fake_report_excel(anomalies_df, df_raw):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        pd.DataFrame({
            'Metric': ['Total Anomalies', 'HIGH Severity', 'MEDIUM Severity', 'Suspect Shops', 'Total Shops'],
            'Value': [len(anomalies_df),
                      len(anomalies_df[anomalies_df['Severity'] == 'HIGH']),
                      len(anomalies_df[anomalies_df['Severity'] == 'MEDIUM']),
                      anomalies_df['Shop Code'].nunique() if 'Shop Code' in anomalies_df.columns else 0,
                      df_raw['Shop Code'].nunique()]
        }).to_excel(writer, sheet_name='Summary', index=False)
        anomalies_df.to_excel(writer, sheet_name='All Anomalies', index=False)
        h = anomalies_df[anomalies_df['Severity'] == 'HIGH']
        if len(h):
            h.to_excel(writer, sheet_name='HIGH Risk', index=False)
        shelf_check = df_raw.groupby(['W', 'Shop Code', 'Shop Name', 'Brand'])['Shelf Share'].sum().reset_index()
        shelf_check.columns = ['Week', 'Shop Code', 'Shop Name', 'Brand', 'Total Shelf Share']
        over = shelf_check[shelf_check['Total Shelf Share'] > 100]
        if len(over):
            over.to_excel(writer, sheet_name='Shelf Over 100pct', index=False)
    output.seek(0)
    return output

# ─── AI CALL (FIXED: API key + model) ─────────────────────────────────────────
def call_ai(prompt):
    try:
        # Priority: st.secrets → sidebar input → empty
        try:
            api_key = st.secrets["ANTHROPIC_API_KEY"]
        except Exception:
            api_key = st.session_state.get("api_key", "")

        if not api_key or not api_key.strip():
            return ("⚠️ **API Key Required**\n\n"
                    "Please add your Anthropic API key in the sidebar under ⚙️ AI Settings "
                    "to enable AI-powered insights.\n\n"
                    "Or add `ANTHROPIC_API_KEY` to your Streamlit secrets file.")

        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key.strip(),
                "anthropic-version": "2023-06-01"
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1200,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=45
        )
        data = r.json()
        if 'content' in data and len(data['content']) > 0:
            return data['content'][0]['text']
        elif 'error' in data:
            err = data['error']
            return f"❌ API Error ({err.get('type','unknown')}): {err.get('message','Check API key and quota.')}"
        return "No response received from AI."
    except requests.Timeout:
        return "⏱️ Request timed out. The AI is busy — please try again in a moment."
    except Exception as e:
        return f"AI error: {str(e)}"

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:16px 0 8px 0; text-align:center">
        <div style="font-family:'Orbitron',monospace; font-size:11px; color:#64ffda; letter-spacing:4px; text-transform:uppercase">SmartSense-LTD</div>
        <div style="font-size:10px; color:#4a5580; letter-spacing:2px; margin-top:2px">DIVISION MX</div>
        <div style="font-size:18px; font-weight:800; color:#e6f1ff; margin-top:8px">📱 Field Intelligence</div>
        <div style="font-size:11px; color:#6272a4; margin-top:2px">Merchandiser Dashboard</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    st.markdown("**📁 Upload Data File**")
    uploaded = st.file_uploader("Upload Excel file (.xlsx)", type=['xlsx'], label_visibility="collapsed")

if uploaded is None:
    st.markdown("""
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:65vh;gap:28px;text-align:center">
        <div style="width:100px;height:100px;background:linear-gradient(135deg,rgba(20,40,160,.2),rgba(0,153,213,.1));border:2px solid rgba(20,40,160,.4);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:44px;animation:float 3s ease infinite">📱</div>
        <div>
            <h2 style="color:#e6f1ff;margin:0 0 8px 0;font-size:26px;font-weight:800">Samsung Field Intelligence Dashboard</h2>
            <p style="color:#6272a4;font-size:15px;margin:0">SmartSense-LTD · Division MX · Innovation Dep 2026</p>
        </div>
        <div style="background:rgba(20,40,160,.08);border:1px dashed rgba(20,40,160,.5);border-radius:20px;padding:28px 56px">
            <p style="color:#64ffda;margin:0;font-size:14px;font-weight:600">👈 Upload your Excel data file via the sidebar</p>
            <p style="color:#4a5580;margin:8px 0 0 0;font-size:12px">Supports .xlsx — All data processed locally</p>
        </div>
        <div style="color:#2d3250;font-size:11px;letter-spacing:3px;text-transform:uppercase">⚡ Innovation Dep · 2026</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─── LOAD & PROCESS DATA ──────────────────────────────────────────────────────
with st.spinner("🔄 Loading and processing your data..."):
    df_raw = load_data(uploaded)
    anomalies_all = detect_anomalies(df_raw)
    wow_all = build_wow_alerts(df_raw)

# ─── SIDEBAR FILTERS + AI SETTINGS ───────────────────────────────────────────
with st.sidebar:
    st.divider()
    st.markdown("**🔽 Filters**")
    weeks = ['All'] + sorted(df_raw['W'].dropna().unique().tolist())
    sel_week = st.selectbox("📅 Week", weeks)
    projs = ['All'] + sorted(df_raw['Project'].dropna().unique().tolist())
    sel_proj = st.selectbox("📋 Project", projs)
    cats = ['All'] + sorted(df_raw['Category'].dropna().unique().tolist())
    sel_cat = st.selectbox("📦 Category", cats)
    segs = ['All'] + sorted(df_raw['Price segmentation'].dropna().unique().tolist())
    sel_seg = st.selectbox("💰 Price Segment", segs)

    st.divider()
    st.markdown("**⚙️ AI Settings**")
    api_key_input = st.text_input(
        "Anthropic API Key",
        type="password",
        value=st.session_state.api_key,
        placeholder="sk-ant-...",
        help="Required for AI Insights & Store Reports"
    )
    if api_key_input != st.session_state.api_key:
        st.session_state.api_key = api_key_input

    st.divider()
    st.markdown(
        f"<div style='color:#4a5580;font-size:11px;line-height:1.6'>"
        f"📊 {len(df_raw):,} rows<br>"
        f"🏪 {df_raw['Shop Code'].nunique()} shops<br>"
        f"📅 {df_raw['W'].nunique()} weeks<br>"
        f"🏷️ {df_raw['Brand'].nunique()} brands</div>",
        unsafe_allow_html=True
    )
    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.splash_done = False
        st.rerun()

# ─── APPLY FILTERS ────────────────────────────────────────────────────────────
df = df_raw.copy()
if sel_week != 'All': df = df[df['W'] == sel_week]
if sel_proj != 'All': df = df[df['Project'] == sel_proj]
if sel_cat  != 'All': df = df[df['Category'] == sel_cat]
if sel_seg  != 'All': df = df[df['Price segmentation'] == sel_seg]

anomalies = anomalies_all[anomalies_all['W'].isin(df['W'].unique())] if sel_week != 'All' else anomalies_all.copy()
store_agg  = build_store_agg(df)
high = anomalies[anomalies['Severity'] == 'HIGH']
med  = anomalies[anomalies['Severity'] == 'MEDIUM']
low  = anomalies[anomalies['Severity'] == 'LOW'] if 'LOW' in anomalies['Severity'].values else pd.DataFrame()

# ─── COMPUTED KPIs ────────────────────────────────────────────────────────────
sam_df        = df[df['Brand'] == 'Samsung']
total_sellout = df['Sellout'].sum()
sam_sellout   = sam_df['Sellout'].sum()
sam_share_pct = (sam_sellout / total_sellout * 100) if total_sellout > 0 else 0
sam_avg_shelf = sam_df['Shelf Share'].mean() if len(sam_df) > 0 else 0

# ─── COMPANY HEADER ───────────────────────────────────────────────────────────
st.markdown("""
<div class="company-header">
    <div class="ch-left">
        <span style="font-size:28px">📱</span>
        <div>
            <div class="ch-company">SmartSense-LTD</div>
            <div class="ch-division">Division MX &nbsp;·&nbsp; Samsung Field Intelligence Platform</div>
        </div>
    </div>
    <div class="ch-right">
        <div class="ch-badge">AI-POWERED</div>
        <div class="ch-badge" style="border-color:rgba(100,255,218,.4);color:#64ffda">LIVE DATA</div>
        <div class="ch-sig">⚡ Innovation Dep · 2026</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── MAIN TITLE ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:24px">
    <h1 class="main-title">Samsung Field Intelligence Dashboard</h1>
    <p style="margin:4px 0 0 0; color:#4a5580; font-size:13px; letter-spacing:1px">
        Merchandiser Data · Fake & Anomaly Detection · AI-Powered Insights · Real-Time Intelligence
    </p>
</div>
""", unsafe_allow_html=True)

# ─── KPI ROW ──────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
with k1: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Total Shops</div><div class="kpi-value">{df["Shop Code"].nunique():,}</div><div class="kpi-sub">Active stores</div></div>', unsafe_allow_html=True)
with k2: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Samsung Sellout</div><div class="kpi-value">{int(sam_sellout):,}</div><div class="kpi-sub">Units sold</div></div>', unsafe_allow_html=True)
with k3: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Market Share</div><div class="kpi-value">{sam_share_pct:.1f}%</div><div class="kpi-sub">Of total sellout</div></div>', unsafe_allow_html=True)
with k4: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Avg Shelf Share</div><div class="kpi-value">{sam_avg_shelf:.1f}</div><div class="kpi-sub">Units per store</div></div>', unsafe_allow_html=True)
with k5:
    ac = "#ff5353" if len(anomalies) > 50 else "#ffb347"
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">⚠️ Anomalies</div><div class="kpi-value" style="color:{ac}">{len(anomalies)}</div><div class="kpi-sub">Requires review</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── TABS ─────────────────────────────────────────────────────────────────────
SEG_ORDER = ['ULC', 'Entry', 'Mass', 'Mid', 'High', 'Top', 'Premium', 'Feature Phone']

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📊 Samsung vs Market",
    "🏪 Store Rankings",
    "🗺️ Store Heatmap",
    "📈 Trends & WoW Alerts",
    "🚨 Anomaly + Report",
    "🎯 Model Matrix & Gaps",
    "🏅 Team Scorecard",
    "🤖 AI & Store Lookup",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: SAMSUNG VS MARKET
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-header">📦 Sellout by Brand</div>', unsafe_allow_html=True)
        bs = df.groupby('Brand')['Sellout'].sum().dropna().sort_values(ascending=False).head(12).reset_index()
        bs.columns = ['Brand', 'Sellout']
        fig = px.bar(bs, x='Brand', y='Sellout', color='Brand', color_discrete_map=COLORS, text='Sellout')
        fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig.update_layout(**CL, showlegend=False, xaxis=dict(tickangle=-30, gridcolor='rgba(45,50,80,.5)'), yaxis=dict(gridcolor='rgba(45,50,80,.5)'), height=360)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.markdown('<div class="section-header">🥧 Market Share</div>', unsafe_allow_html=True)
        top8 = bs.head(8)['Brand'].tolist()
        pied = df.copy()
        pied['BG'] = pied['Brand'].apply(lambda x: x if x in top8 else 'Others')
        pd2 = pied.groupby('BG')['Sellout'].sum().reset_index()
        fig2 = px.pie(pd2, values='Sellout', names='BG', color='BG', color_discrete_map=COLORS, hole=0.55)
        fig2.update_traces(textposition='outside', textinfo='percent+label',
                           marker=dict(colors=[COLORS.get(b, '#8892b0') for b in pd2['BG']]))
        fig2.update_layout(**CL, showlegend=False, height=360)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-header">📐 Shelf Share by Segment vs Competitors</div>', unsafe_allow_html=True)
    kb = ['Samsung', 'Oppo', 'Realme', 'Xiaomi', 'Infinix', 'Vivo', 'Honor']
    sg = df.groupby(['Price segmentation', 'Brand'])['Shelf Share'].mean().reset_index()
    sg['BG'] = sg['Brand'].apply(lambda x: x if x in kb else 'Others')
    sg2 = sg.groupby(['Price segmentation', 'BG'])['Shelf Share'].mean().reset_index()
    sg2['Price segmentation'] = pd.Categorical(sg2['Price segmentation'], categories=SEG_ORDER, ordered=True)
    fig3 = px.bar(sg2.sort_values('Price segmentation'), x='Price segmentation', y='Shelf Share',
                  color='BG', barmode='group', color_discrete_map=COLORS)
    fig3.update_layout(**CL, xaxis=dict(gridcolor='rgba(45,50,80,.5)'), yaxis=dict(gridcolor='rgba(45,50,80,.5)', title='Avg Shelf'), height=380)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<div class="section-header">🏷️ Samsung by Price Segment</div>', unsafe_allow_html=True)
    ss_seg = df[df['Brand'] == 'Samsung'].groupby('Price segmentation').agg(
        Sellout=('Sellout', 'sum'), Shelf_Share=('Shelf Share', 'mean'),
        Models=('Model', 'nunique'), Shops=('Shop Code', 'nunique')
    ).reset_index()
    ss_seg['Sellout'] = ss_seg['Sellout'].fillna(0).astype(int)
    ss_seg['Shelf_Share'] = ss_seg['Shelf_Share'].round(1)
    st.dataframe(ss_seg.sort_values('Sellout', ascending=False), use_container_width=True, hide_index=True,
                 column_config={'Sellout': st.column_config.NumberColumn('Sellout', format="%d"),
                                'Shelf_Share': st.column_config.NumberColumn('Avg Shelf', format="%.1f")})

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: STORE RANKINGS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    rm = st.radio("Rank by:", ["Samsung Sellout", "Samsung Shelf Share", "Total Sellout", "Samsung Share %"], horizontal=True)
    sa = store_agg.copy()
    if rm == "Samsung Sellout":       sa = sa.sort_values('Sam_Sellout', ascending=False);   cv, cl = 'Sam_Sellout', 'Samsung Sellout'
    elif rm == "Samsung Shelf Share": sa = sa.sort_values('Sam_Shelf', ascending=False);     cv, cl = 'Sam_Shelf', 'Samsung Avg Shelf'
    elif rm == "Total Sellout":       sa = sa.sort_values('Total_Sellout', ascending=False); cv, cl = 'Total_Sellout', 'Total Sellout'
    else:                              sa = sa.sort_values('Sam_Share_Pct', ascending=False); cv, cl = 'Sam_Share_Pct', 'Samsung Share %'

    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown(f'<div class="section-header">🏆 Top 20 — {cl}</div>', unsafe_allow_html=True)
        fig_r = px.bar(sa.head(20), x=cv, y='Shop Name', orientation='h',
                       color=cv, color_continuous_scale=['#1a2744', '#1428A0', '#0099D5', '#64ffda'], text=cv)
        fig_r.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        fig_r.update_layout(**CL, yaxis=dict(autorange='reversed', gridcolor='rgba(45,50,80,.5)'),
                            xaxis=dict(gridcolor='rgba(45,50,80,.5)'), coloraxis_showscale=False, height=560)
        st.plotly_chart(fig_r, use_container_width=True)
    with c2:
        st.markdown('<div class="section-header">📉 Bottom 20</div>', unsafe_allow_html=True)
        fig_b = px.bar(sa.tail(20).sort_values('Sam_Sellout'), x='Sam_Sellout', y='Shop Name', orientation='h',
                       color='Sam_Sellout', color_continuous_scale=['#ff5353', '#ffb347', '#2d3250'], text='Sam_Sellout')
        fig_b.update_traces(texttemplate='%{text:.0f}', textposition='outside')
        fig_b.update_layout(**CL, yaxis=dict(autorange='reversed', gridcolor='rgba(45,50,80,.5)'),
                            xaxis=dict(gridcolor='rgba(45,50,80,.5)'), coloraxis_showscale=False, height=560)
        st.plotly_chart(fig_b, use_container_width=True)

    st.markdown('<div class="section-header">📋 Full Store Leaderboard</div>', unsafe_allow_html=True)
    srch = st.text_input("🔍 Search shop name...", "")
    disp = sa[sa['Shop Name'].str.contains(srch, case=False, na=False)] if srch else sa
    st.dataframe(disp[['Shop Name', 'Project', 'Sam_Sellout', 'Sam_Shelf', 'Sam_Share_Pct', 'Total_Sellout', 'Brands_Stocked', 'Models_Stocked']].reset_index(drop=True),
                 use_container_width=True,
                 column_config={
                     'Sam_Sellout': st.column_config.NumberColumn('Samsung Sellout', format="%d"),
                     'Sam_Shelf': st.column_config.NumberColumn('Samsung Avg Shelf', format="%.1f"),
                     'Sam_Share_Pct': st.column_config.ProgressColumn('Samsung Share %', min_value=0, max_value=100, format="%.1f%%"),
                     'Total_Sellout': st.column_config.NumberColumn('Total Sellout', format="%d"),
                 })

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3: STORE HEATMAP
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">🗺️ Store Performance Heatmap</div>', unsafe_allow_html=True)
    hm = st.radio("Color heatmap by:", ["Samsung Sellout", "Samsung Share %", "Samsung Avg Shelf", "Total Sellout"], horizontal=True, key="hm")
    hmc = {'Samsung Sellout': 'Sam_Sellout', 'Samsung Share %': 'Sam_Share_Pct',
           'Samsung Avg Shelf': 'Sam_Shelf', 'Total Sellout': 'Total_Sellout'}[hm]

    fig_hm = px.treemap(
        store_agg, path=['Project', 'Shop Name'], values='Total_Sellout', color=hmc,
        color_continuous_scale=['#1a0a0a', '#7a1515', '#cc3300', '#ff8800', '#ffdd00', '#64ffda'],
        hover_data={'Sam_Sellout': True, 'Sam_Share_Pct': ':.1f', 'Sam_Shelf': ':.1f', 'Total_Sellout': True}
    )
    fig_hm.update_traces(texttemplate='<b>%{label}</b><br>%{color:.1f}')
    fig_hm.update_layout(**CL, height=600,
                         coloraxis_colorbar=dict(title=hm, tickfont=dict(color='#ccd6f6')))
    st.plotly_chart(fig_hm, use_container_width=True)

    st.markdown('<div class="alert-warning">💡 <b>How to read:</b> Each box = one store. <b>Size</b> = total sellout. <b>Color</b> = selected metric. Dark red = low Samsung. Bright green = strong Samsung.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">🔥 Hot vs Cold Stores</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**🟢 Top 10 HOT Stores**")
        hot = store_agg.sort_values('Sam_Sellout', ascending=False).head(10)[['Shop Name', 'Project', 'Sam_Sellout', 'Sam_Share_Pct']].reset_index(drop=True)
        hot.index += 1
        st.dataframe(hot, use_container_width=True, column_config={
            'Sam_Sellout': st.column_config.NumberColumn('Samsung Units', format="%d"),
            'Sam_Share_Pct': st.column_config.NumberColumn('Samsung %', format="%.1f%%"),
        })
    with c2:
        st.markdown("**🔴 Top 10 COLD Stores**")
        cold = store_agg[store_agg['Total_Sellout'] > 0].sort_values('Sam_Sellout').head(10)[['Shop Name', 'Project', 'Sam_Sellout', 'Sam_Share_Pct']].reset_index(drop=True)
        cold.index += 1
        st.dataframe(cold, use_container_width=True, column_config={
            'Sam_Sellout': st.column_config.NumberColumn('Samsung Units', format="%d"),
            'Sam_Share_Pct': st.column_config.NumberColumn('Samsung %', format="%.1f%%"),
        })

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4: TRENDS + WoW ALERTS
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    top8b = df_raw.groupby('Brand')['Sellout'].sum().nlargest(8).index.tolist()
    wkly  = df_raw.groupby(['W', 'Brand']).agg(Sellout=('Sellout', 'sum')).reset_index()
    st.markdown('<div class="section-header">📈 Weekly Sellout Trend</div>', unsafe_allow_html=True)
    fig_t = px.line(wkly[wkly['Brand'].isin(top8b)], x='W', y='Sellout', color='Brand',
                    markers=True, color_discrete_map=COLORS, line_shape='spline')
    fig_t.update_traces(line_width=3, marker_size=8)
    fig_t.update_layout(**CL, xaxis=dict(gridcolor='rgba(45,50,80,.5)'), yaxis=dict(gridcolor='rgba(45,50,80,.5)', title='Units'), height=380)
    st.plotly_chart(fig_t, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-header">📊 Samsung Weekly KPIs</div>', unsafe_allow_html=True)
        sw = df_raw[df_raw['Brand'] == 'Samsung'].groupby('W').agg(Sellout=('Sellout', 'sum'), Shelf=('Shelf Share', 'mean')).reset_index()
        fig_sw = make_subplots(specs=[[{"secondary_y": True}]])
        fig_sw.add_trace(go.Bar(x=sw['W'], y=sw['Sellout'], name='Sellout', marker_color='#1428A0', opacity=0.85), secondary_y=False)
        fig_sw.add_trace(go.Scatter(x=sw['W'], y=sw['Shelf'], name='Avg Shelf', line=dict(color='#64ffda', width=3), mode='lines+markers', marker_size=8), secondary_y=True)
        fig_sw.update_layout(**CL, height=340, xaxis=dict(gridcolor='rgba(45,50,80,.5)'))
        fig_sw.update_yaxes(gridcolor='rgba(45,50,80,.5)', secondary_y=False, title_text='Sellout')
        fig_sw.update_yaxes(gridcolor='rgba(45,50,80,.5)', secondary_y=True, title_text='Avg Shelf')
        st.plotly_chart(fig_sw, use_container_width=True)
    with c2:
        st.markdown('<div class="section-header">📉 Samsung Share by Week</div>', unsafe_allow_html=True)
        wt = df_raw.groupby(['W', 'Brand'])['Sellout'].sum().reset_index()
        wtotal = wt.groupby('W')['Sellout'].sum().reset_index().rename(columns={'Sellout': 'Total'})
        wsam = wt[wt['Brand'] == 'Samsung'].merge(wtotal, on='W')
        wsam['Share%'] = (wsam['Sellout'] / wsam['Total'] * 100).round(1)
        fig_ws = go.Figure(go.Scatter(
            x=wsam['W'], y=wsam['Share%'], fill='tozeroy', fillcolor='rgba(20,40,160,0.2)',
            line=dict(color='#1428A0', width=3), mode='lines+markers+text',
            text=wsam['Share%'].apply(lambda x: f'{x:.1f}%'),
            textposition='top center', textfont=dict(color='#64ffda', size=12)
        ))
        fig_ws.update_layout(**CL, xaxis=dict(gridcolor='rgba(45,50,80,.5)'), yaxis=dict(gridcolor='rgba(45,50,80,.5)', title='Samsung Share %'), height=340)
        st.plotly_chart(fig_ws, use_container_width=True)

    # WoW Alert Feed
    st.markdown('<div class="section-header">🚦 Week-over-Week Alert Feed</div>', unsafe_allow_html=True)
    thr = st.slider("Alert on Samsung drop ≥", 10, 80, 30, 5, format="%d%%")

    if len(wow_all) > 0:
        wf = wow_all.copy()
        if sel_proj != 'All':
            ps = df_raw[df_raw['Project'] == sel_proj]['Shop Code'].unique()
            wf = wf[wf['Shop Code'].isin(ps)]
        drops = wf[wf['Change_Pct'] <= -thr].sort_values('Change_Pct')
        rises = wf[wf['Change_Pct'] >= 30].sort_values('Change_Pct', ascending=False)
        a1, a2 = st.columns(2)
        with a1:
            st.markdown(f"**🔴 {len(drops)} Stores Dropped ≥{thr}%**")
            for _, r in drops.head(15).iterrows():
                st.markdown(f'<div class="alert-feed-drop"><b>{r["Shop Name"]}</b> · {r["From_Week"]} → {r["To_Week"]}<br><span style="color:#ff5353;font-size:18px;font-weight:700">{r["Change_Pct"]:.1f}%</span> <span style="color:#6272a4">({int(r["Prev"])} → {int(r["Curr"])} units)</span></div>', unsafe_allow_html=True)
            if len(drops) == 0:
                st.success(f"✅ No stores dropped >{thr}%")
        with a2:
            st.markdown("**🟢 Rising Stores (≥30% Growth)**")
            for _, r in rises.head(15).iterrows():
                st.markdown(f'<div class="alert-feed-rise"><b>{r["Shop Name"]}</b> · {r["From_Week"]} → {r["To_Week"]}<br><span style="color:#64ffda;font-size:18px;font-weight:700">+{r["Change_Pct"]:.1f}%</span> <span style="color:#6272a4">({int(r["Prev"])} → {int(r["Curr"])} units)</span></div>', unsafe_allow_html=True)
            if len(rises) == 0:
                st.info("No stores with ≥30% growth.")
    else:
        st.info("Need at least 2 weeks of data for WoW alerts.")

    st.markdown('<div class="section-header">🔢 Weekly Brand Pivot</div>', unsafe_allow_html=True)
    wp = df_raw.pivot_table(index='Brand', columns='W', values='Sellout', aggfunc='sum').fillna(0).astype(int)
    wp['Total'] = wp.sum(axis=1)
    st.dataframe(wp.sort_values('Total', ascending=False).head(12), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5: ANOMALY + AUTO REPORT
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-header">🚨 Fake & Anomaly Detection</div>', unsafe_allow_html=True)
    a1, a2, a3 = st.columns(3)
    with a1: st.markdown(f'<div class="alert-danger"><b>🔴 HIGH</b><br><span style="font-size:32px;font-weight:800;color:#ff5353">{len(high)}</span><br><span style="color:#6272a4;font-size:12px">critical records</span></div>', unsafe_allow_html=True)
    with a2: st.markdown(f'<div class="alert-warning"><b>🟠 MEDIUM</b><br><span style="font-size:32px;font-weight:800;color:#ffb347">{len(med)}</span><br><span style="color:#6272a4;font-size:12px">warning records</span></div>', unsafe_allow_html=True)
    with a3: st.markdown(f'<div class="alert-success"><b>🟡 LOW</b><br><span style="font-size:32px;font-weight:800;color:#64ffda">{len(low)}</span><br><span style="color:#6272a4;font-size:12px">info records</span></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">📥 Auto Fake Report Export</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown('<div class="alert-warning">📋 <b>Report includes:</b> Executive Summary · All Anomalies · HIGH Risk Sheet · Shelf Share >100% violations · Statistical outliers</div>', unsafe_allow_html=True)
    with c2:
        excel_bytes = generate_fake_report_excel(anomalies, df_raw)
        st.download_button(
            "📥 Download Fake Report (.xlsx)",
            data=excel_bytes,
            file_name="SmartSense_Samsung_Fake_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True, type="primary"
        )

    st.markdown("<br>", unsafe_allow_html=True)
    sv = st.selectbox("Filter by severity:", ["All", "HIGH", "MEDIUM", "LOW"])
    show_a = anomalies if sv == "All" else anomalies[anomalies['Severity'] == sv]
    if len(show_a) > 0:
        st.dataframe(show_a[['W', 'Shop Code', 'Shop Name', 'Brand', 'Model', 'Shelf Share', 'Issue', 'Severity']].reset_index(drop=True),
                     use_container_width=True, column_config={'Issue': st.column_config.TextColumn('Issue', width='large')})
    else:
        st.success("✅ No anomalies found for selected filter.")

    st.markdown('<div class="section-header">🔬 Shelf Share > 100% Suspects</div>', unsafe_allow_html=True)
    sc_df = df.groupby(['W', 'Shop Code', 'Shop Name', 'Brand'])['Shelf Share'].sum().reset_index()
    sc_df.columns = ['Week', 'Shop Code', 'Shop Name', 'Brand', 'Total SS']
    o100 = sc_df[sc_df['Total SS'] > 100].sort_values('Total SS', ascending=False)
    if len(o100) > 0:
        fig_o = px.bar(o100.head(30), x='Shop Name', y='Total SS', color='Brand',
                       color_discrete_map=COLORS, text='Total SS', barmode='group')
        fig_o.add_hline(y=100, line_dash='dash', line_color='#ff5353', annotation_text='100% Limit', annotation_font_color='#ff5353')
        fig_o.update_traces(texttemplate='%{text:.0f}%', textposition='outside')
        fig_o.update_layout(**CL, xaxis=dict(tickangle=-40, gridcolor='rgba(45,50,80,.5)'), yaxis=dict(gridcolor='rgba(45,50,80,.5)'), height=420)
        st.plotly_chart(fig_o, use_container_width=True)
    else:
        st.success("✅ No shops with shelf share >100% in current filter.")

    st.markdown('<div class="section-header">📦 Sellout Outliers</div>', unsafe_allow_html=True)
    ms, ss2 = df['Sellout'].mean(), df['Sellout'].std()
    if ss2 and ss2 > 0:
        out = df[df['Sellout'] > ms + 2.5 * ss2][['W', 'Shop Name', 'Brand', 'Model', 'Sellout', 'Price']].sort_values('Sellout', ascending=False)
        st.dataframe(out.head(30).reset_index(drop=True), use_container_width=True,
                     column_config={'Sellout': st.column_config.NumberColumn('Sellout ⚠️', format="%d"),
                                    'Price': st.column_config.NumberColumn('Price EGP', format="%,.0f")})

# ══════════════════════════════════════════════════════════════════════════════
# TAB 6: MODEL MATRIX + COVERAGE GAP FINDER  ★ FIXED
# ══════════════════════════════════════════════════════════════════════════════
with tab6:
    st.markdown('<div class="section-header">🎯 Model Performance Matrix — Price vs Sellout vs Shelf Share</div>', unsafe_allow_html=True)

    mb = st.selectbox("Show brand:", ['Samsung', 'All Key Brands'], key='mb')
    mdf = df[df['Brand'] == 'Samsung'] if mb == 'Samsung' else df[df['Brand'].isin(list(COLORS.keys())[:9])]

    try:
        mp = mdf.groupby(['Model', 'Brand']).agg(
            Sellout=('Sellout', 'sum'),
            Shelf_Share=('Shelf Share', 'mean'),
            Price=('Price', 'mean'),
            Shops=('Shop Code', 'nunique')
        ).reset_index().dropna()
        # FIX: Filter out zero/negative Shelf_Share to prevent scatter size errors
        mp = mp[(mp['Sellout'] > 0) & (mp['Shelf_Share'] > 0) & (mp['Price'] > 0)]

        if len(mp) > 0:
            fig_mp = px.scatter(mp, x='Price', y='Sellout', size='Shelf_Share', color='Brand',
                                color_discrete_map=COLORS, size_max=40,
                                hover_data={'Model': True, 'Shops': True, 'Shelf_Share': ':.1f', 'Price': ':,.0f'},
                                labels={'Price': 'Avg Price (EGP)', 'Sellout': 'Total Sellout', 'Shelf_Share': 'Avg Shelf'})
            fig_mp.update_layout(**CL, height=520,
                                 xaxis=dict(gridcolor='rgba(45,50,80,.5)', title='Average Price (EGP)'),
                                 yaxis=dict(gridcolor='rgba(45,50,80,.5)', title='Total Sellout (Units)'))
            st.plotly_chart(fig_mp, use_container_width=True)
            st.markdown('<div class="alert-success">📌 <b>Read:</b> X=Price · Y=Sellout · Bubble size=Shelf Share. Top-left = affordable bestsellers. Bottom-right = premium low movers.</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-header">🏆 Samsung Model Leaderboard</div>', unsafe_allow_html=True)
            sml = mp[mp['Brand'] == 'Samsung'].sort_values('Sellout', ascending=False).copy()
            if len(sml) > 0:
                sml['Sellout'] = sml['Sellout'].astype(int)
                sml['Price'] = sml['Price'].round(0).astype(int)
                sml['Shelf_Share'] = sml['Shelf_Share'].round(1)
                st.dataframe(sml[['Model', 'Sellout', 'Shelf_Share', 'Price', 'Shops']].reset_index(drop=True),
                             use_container_width=True, hide_index=True,
                             column_config={
                                 'Sellout': st.column_config.NumberColumn('Sellout', format="%d"),
                                 'Shelf_Share': st.column_config.NumberColumn('Avg Shelf', format="%.1f"),
                                 'Price': st.column_config.NumberColumn('Avg Price EGP', format="%,d")
                             })
        else:
            st.info("No model data available for current filters. Try selecting different filters or switching to 'All Key Brands'.")
    except Exception as e:
        st.error(f"Could not render model matrix: {str(e)}. Try adjusting your filters.")

    # Coverage Gap Finder
    st.markdown('<div class="section-header">🔍 Coverage Gap Finder — Samsung Missing, Competitors Present</div>', unsafe_allow_html=True)
    st.markdown("Finds stores where competitors have strong shelf presence but Samsung shelf share is critically low.")

    gt = st.slider("Flag Samsung shelf below:", 1, 10, 3, 1, key='gt')
    fs = st.selectbox("Segment:", ['All'] + SEG_ORDER, key='fs')
    gdf = df.copy() if fs == 'All' else df[df['Price segmentation'] == fs]

    try:
        sam_ss = gdf[gdf['Brand'] == 'Samsung'].groupby(['Shop Code', 'Shop Name', 'Price segmentation'])['Shelf Share'].sum().reset_index()
        sam_ss.columns = ['Shop Code', 'Shop Name', 'Price segmentation', 'Samsung_SS']
        comp_ss = gdf[gdf['Brand'] != 'Samsung'].groupby(['Shop Code', 'Shop Name', 'Price segmentation'])['Shelf Share'].sum().reset_index()
        comp_ss.columns = ['Shop Code', 'Shop Name', 'Price segmentation', 'Comp_SS']
        top_c = gdf[gdf['Brand'] != 'Samsung'].groupby(['Shop Code', 'Price segmentation', 'Brand'])['Shelf Share'].sum().reset_index()
        top_c = top_c.sort_values('Shelf Share', ascending=False).groupby(['Shop Code', 'Price segmentation']).first().reset_index()
        top_c = top_c.rename(columns={'Brand': 'Top_Comp', 'Shelf Share': 'Top_Comp_SS'})

        gaps = comp_ss.merge(sam_ss, on=['Shop Code', 'Shop Name', 'Price segmentation'], how='left')
        gaps['Samsung_SS'] = gaps['Samsung_SS'].fillna(0)
        gaps = gaps[(gaps['Samsung_SS'] < gt) & (gaps['Comp_SS'] > 5)]
        gaps = gaps.merge(top_c[['Shop Code', 'Price segmentation', 'Top_Comp', 'Top_Comp_SS']], on=['Shop Code', 'Price segmentation'], how='left')
        gaps = gaps.sort_values('Comp_SS', ascending=False)

        if len(gaps) > 0:
            st.warning(f"⚠️ {len(gaps)} coverage gaps found — Samsung weak, competitors strong.")
            gc1, gc2 = st.columns(2)
            with gc1:
                sgc = gaps.groupby('Price segmentation').size().sort_values(ascending=False).reset_index()
                sgc.columns = ['Segment', 'Gaps']
                fig_gc = px.bar(sgc, x='Segment', y='Gaps', color='Segment', text='Gaps')
                fig_gc.update_traces(textposition='outside')
                fig_gc.update_layout(**CL, showlegend=False, xaxis=dict(gridcolor='rgba(45,50,80,.5)', tickangle=-30),
                                     yaxis=dict(gridcolor='rgba(45,50,80,.5)'), title='Gaps by Segment', height=320)
                st.plotly_chart(fig_gc, use_container_width=True)
            with gc2:
                cgc = gaps['Top_Comp'].value_counts().head(8).reset_index()
                cgc.columns = ['Brand', 'Gaps']
                fig_cgc = px.bar(cgc, x='Brand', y='Gaps', color='Brand', color_discrete_map=COLORS, text='Gaps')
                fig_cgc.update_traces(textposition='outside')
                fig_cgc.update_layout(**CL, showlegend=False, xaxis=dict(gridcolor='rgba(45,50,80,.5)', tickangle=-30),
                                      yaxis=dict(gridcolor='rgba(45,50,80,.5)'), title='Who Fills Samsung Gaps', height=320)
                st.plotly_chart(fig_cgc, use_container_width=True)

            st.dataframe(gaps[['Shop Name', 'Price segmentation', 'Samsung_SS', 'Comp_SS', 'Top_Comp', 'Top_Comp_SS']].head(50).reset_index(drop=True),
                         use_container_width=True,
                         column_config={
                             'Samsung_SS': st.column_config.NumberColumn('Samsung Shelf ⚠️', format="%.0f"),
                             'Comp_SS': st.column_config.NumberColumn('Competitor Shelf', format="%.0f"),
                             'Top_Comp_SS': st.column_config.NumberColumn('Top Comp Shelf', format="%.0f")
                         })
        else:
            st.success("✅ No significant coverage gaps in current filter.")
    except Exception as e:
        st.error(f"Coverage gap analysis error: {str(e)}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 7: TEAM SCORECARD  ★ FIXED
# ══════════════════════════════════════════════════════════════════════════════
with tab7:
    st.markdown('<div class="section-header">🏅 Merchandiser Team Scorecard</div>', unsafe_allow_html=True)
    st.markdown("Each project team scored 0–100 across 5 dimensions. **Weights:** Sellout 30% · Data Quality 25% · Shelf Share 20% · Coverage 15% · Efficiency 10%")

    def norm(s, inv=False):
        mn, mx = s.min(), s.max()
        if mx == mn:
            return pd.Series([50.0] * len(s), index=s.index)
        n = (s - mn) / (mx - mn) * 100
        return (100 - n) if inv else n

    plist = sorted(df_raw['Project'].dropna().unique())

    if len(plist) == 0:
        st.warning("No project data available. Please check your data.")
    else:
        rows = []
        for p in plist:
            pd_ = df_raw[df_raw['Project'] == p]
            ps = pd_['Shop Code'].nunique()
            if ps == 0:
                continue
            psam = pd_[pd_['Brand'] == 'Samsung']
            sell  = psam['Sellout'].sum()
            shelf = psam['Shelf Share'].mean()
            # FIX: safe anomaly lookup
            if 'Shop Code' in anomalies_all.columns:
                pa = anomalies_all[anomalies_all['Shop Code'].isin(pd_['Shop Code'].unique())]
            else:
                pa = pd.DataFrame()
            ar   = len(pa) / ps if ps > 0 else 0
            cov  = psam['Shop Code'].nunique() / ps * 100 if ps > 0 else 0
            sps  = sell / ps if ps > 0 else 0
            rows.append({
                'Project': p, 'Shops': ps, 'Samsung_Sell': int(sell),
                'Avg_Shelf': round(float(shelf), 1) if not pd.isna(shelf) else 0,
                'Anomaly_Rate': round(ar, 2), 'Coverage': round(cov, 1),
                'Sell_Per_Shop': round(sps, 1), 'Anomalies': len(pa)
            })

        if len(rows) == 0:
            st.info("No project performance data to display.")
        else:
            sc = pd.DataFrame(rows)
            sc['S_Sell']  = norm(sc['Samsung_Sell'])
            sc['S_Shelf'] = norm(sc['Avg_Shelf'])
            sc['S_Qual']  = norm(sc['Anomaly_Rate'], inv=True)
            sc['S_Cov']   = norm(sc['Coverage'])
            sc['S_Eff']   = norm(sc['Sell_Per_Shop'])
            sc['Overall'] = (sc['S_Sell'] * 0.30 + sc['S_Shelf'] * 0.20 + sc['S_Qual'] * 0.25 + sc['S_Cov'] * 0.15 + sc['S_Eff'] * 0.10).round(1)
            sc = sc.sort_values('Overall', ascending=False).reset_index(drop=True)

            def grade(s):
                if s >= 80: return 'A', '#64ffda', 'score-a'
                if s >= 60: return 'B', '#1DB954', 'score-b'
                if s >= 40: return 'C', '#ffb347', 'score-c'
                return 'D', '#ff5353', 'score-d'

            medals = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
            # FIX: cap columns at 6 to avoid layout issues with many projects
            n_cols = min(len(sc), 6)
            cols = st.columns(n_cols)
            for i, (_, r) in enumerate(sc.head(n_cols).iterrows()):
                g, gc, gcls = grade(r['Overall'])
                medal = medals[i] if i < len(medals) else f"#{i+1}"
                with cols[i]:
                    st.markdown(
                        f'<div class="score-card {gcls}">'
                        f'<div style="font-size:30px">{medal}</div>'
                        f'<div style="color:#e6f1ff;font-size:17px;font-weight:700;margin-top:4px">{r["Project"]}</div>'
                        f'<div style="color:{gc};font-size:44px;font-weight:800;line-height:1.1">{r["Overall"]}</div>'
                        f'<div style="color:#6272a4;font-size:13px">Grade <b style="color:{gc}">{g}</b></div>'
                        f'<div style="color:#4a5580;font-size:11px;margin-top:8px">{int(r["Shops"])} shops</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-header">🕸️ Team Radar Comparison</div>', unsafe_allow_html=True)
            cats_r  = ['Sellout', 'Shelf Share', 'Data Quality', 'Coverage', 'Efficiency']
            rcols_d = ['S_Sell', 'S_Shelf', 'S_Qual', 'S_Cov', 'S_Eff']
            palette = ['#1428A0', '#64ffda', '#FFB900', '#FF6900', '#1C7C54', '#C8102E', '#0057A8', '#7B2D8B']
            fig_r2 = go.Figure()
            for i, (_, r) in enumerate(sc.iterrows()):
                v = [r[c] for c in rcols_d] + [r[rcols_d[0]]]
                fig_r2.add_trace(go.Scatterpolar(
                    r=v, theta=cats_r + [cats_r[0]], fill='toself', name=r['Project'],
                    line=dict(color=palette[i % len(palette)], width=2.5),
                    fillcolor=palette[i % len(palette)].replace('#', 'rgba(') + ',0.08)'
                    if False else f"rgba({int(palette[i%len(palette)][1:3],16)},{int(palette[i%len(palette)][3:5],16)},{int(palette[i%len(palette)][5:7],16)},0.08)"
                ))
            fig_r2.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#ccd6f6',
                polar=dict(
                    bgcolor='rgba(14,17,35,.8)',
                    radialaxis=dict(visible=True, range=[0, 100], gridcolor='rgba(45,50,80,.6)', tickfont=dict(color='#6272a4')),
                    angularaxis=dict(gridcolor='rgba(45,50,80,.6)', tickfont=dict(color='#ccd6f6'))
                ),
                legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='rgba(45,50,80,.5)', borderwidth=1),
                margin=dict(t=20, b=20, l=20, r=20),
                height=440
            )
            st.plotly_chart(fig_r2, use_container_width=True)

            st.markdown('<div class="section-header">📊 Detailed Score Breakdown</div>', unsafe_allow_html=True)
            disp_sc = sc[['Project', 'Overall', 'S_Sell', 'S_Shelf', 'S_Qual', 'S_Cov', 'Samsung_Sell', 'Avg_Shelf', 'Coverage', 'Anomalies', 'Shops']].copy()
            disp_sc.columns = ['Project', 'Overall', 'Sellout Score', 'Shelf Score', 'Quality Score', 'Coverage Score', 'Samsung Units', 'Avg Shelf', 'Coverage %', 'Anomalies', 'Shops']
            st.dataframe(disp_sc.reset_index(drop=True), use_container_width=True, hide_index=True,
                         column_config={
                             'Overall': st.column_config.ProgressColumn('Overall', min_value=0, max_value=100, format="%.1f"),
                             'Samsung Units': st.column_config.NumberColumn('Samsung Units', format="%d"),
                             'Coverage %': st.column_config.NumberColumn('Coverage %', format="%.1f%%")
                         })

# ══════════════════════════════════════════════════════════════════════════════
# TAB 8: AI INSIGHTS + SMART STORE LOOKUP  ★ FIXED
# ══════════════════════════════════════════════════════════════════════════════
with tab8:
    ai_t1, ai_t2 = st.tabs(["🤖 AI Insights", "🔍 Smart Store Lookup"])

    with ai_t1:
        st.markdown('<div class="section-header">🤖 AI-Powered Field Intelligence</div>', unsafe_allow_html=True)

        # Check API key
        has_key = bool(st.session_state.get("api_key", "").strip())
        try:
            has_key = has_key or bool(st.secrets.get("ANTHROPIC_API_KEY", ""))
        except Exception:
            pass

        if not has_key:
            st.markdown('<div class="alert-warning">⚙️ <b>API Key Required</b> — Add your Anthropic API key in the sidebar under ⚙️ AI Settings to enable AI insights.</div>', unsafe_allow_html=True)

        # FIX: safe data prep with error handling
        try:
            bs2 = df.groupby('Brand').agg(Sellout=('Sellout', 'sum'), Shelf=('Shelf Share', 'mean'), Shops=('Shop Code', 'nunique')).sort_values('Sellout', ascending=False).head(10)
            wsam_dict = df_raw[df_raw['Brand'] == 'Samsung'].groupby('W')['Sellout'].sum().to_dict()
            tops = store_agg.sort_values('Sam_Sellout', ascending=False).head(5)[['Shop Name', 'Sam_Sellout', 'Sam_Share_Pct']].to_dict('records')
            bots = store_agg.sort_values('Sam_Sellout').head(5)[['Shop Name', 'Sam_Sellout', 'Sam_Share_Pct']].to_dict('records')
            ctx = (f"Samsung Field Data | SmartSense-LTD Division MX | "
                   f"Shops={df['Shop Code'].nunique()}, Weeks={sorted(df['W'].unique())}, "
                   f"Total sellout={int(df['Sellout'].sum()):,}, Samsung sellout={int(sam_sellout):,} ({sam_share_pct:.1f}%), "
                   f"Avg shelf={sam_avg_shelf:.1f}, Anomalies={len(anomalies)} (HIGH={len(high)},MED={len(med)}), "
                   f"Brands={bs2['Sellout'].to_dict()}, Weekly Samsung={wsam_dict}, "
                   f"Top stores={tops}, Bottom stores={bots}, "
                   f"Filters=Week:{sel_week},Proj:{sel_proj},Cat:{sel_cat},Seg:{sel_seg}")
        except Exception as e:
            ctx = f"Data context error: {str(e)}"

        qt = st.selectbox("Insight type:", ["📊 Executive Summary", "🚨 Fake & Anomaly Report", "💡 Growth Opportunities", "🆚 Competitive Threats", "🏪 Store Action Plan", "✏️ Custom Question"])
        cq = st.text_area("Your question:", placeholder="e.g. Which segment needs most attention?") if qt == "✏️ Custom Question" else ""

        if st.button("🤖 Generate AI Insights", type="primary", use_container_width=True):
            pm = {
                "📊 Executive Summary": f"You are a senior Samsung field analyst for SmartSense-LTD Division MX. Write a concise executive summary: 1)Market position 2)Key wins 3)Key threats 4)Top concerns 5)Immediate actions. Use specific numbers.\nData:{ctx}",
                "🚨 Fake & Anomaly Report": f"You are a data quality auditor for SmartSense-LTD. Analyze: 1)What anomalies suggest 2)Fake reporting patterns 3)Shops needing investigation 4)Corrective actions.\nData:{ctx}",
                "💡 Growth Opportunities": f"You are a Samsung sales consultant at SmartSense-LTD MX division. Identify: 1)Segments to gain share 2)Underperforming stores with potential 3)Competitor weaknesses 4)Quick wins.\nData:{ctx}",
                "🆚 Competitive Threats": f"You are a Samsung competitive analyst at SmartSense-LTD. Which brands are biggest threats? In which segments? What shelf strategy do they use? What should Samsung do?\nData:{ctx}",
                "🏪 Store Action Plan": f"You are a Samsung field operations manager at SmartSense-LTD MX. Prioritized plan: 1)Stores to reward 2)Stores needing urgent attention 3)Suspicious data stores 4)Next week priorities.\nData:{ctx}",
            }
            prompt = pm.get(qt, f"Answer this question for SmartSense-LTD Samsung field team: {cq}\nData:{ctx}")
            with st.spinner("🤖 Analyzing field intelligence..."):
                result = call_ai(prompt)
            st.markdown(f'<div class="insight-box">{result}</div>', unsafe_allow_html=True)

        st.markdown("<br>")
        h1, h2, h3 = st.columns(3)
        if len(store_agg) > 0:
            top_s = store_agg.sort_values('Sam_Sellout', ascending=False).iloc[0]
            with h1: st.markdown(f'<div class="alert-success"><b>✅ Samsung Position</b><br>{sam_share_pct:.1f}% market share · {int(sam_sellout):,} units</div>', unsafe_allow_html=True)
            with h2: st.markdown(f'<div class="alert-danger"><b>🔴 {len(anomalies)} Anomalies</b><br>{len(high)} HIGH severity cases need immediate review</div>', unsafe_allow_html=True)
            with h3: st.markdown(f'<div class="alert-warning"><b>🏆 Top Store</b><br>{top_s["Shop Name"]} — {int(top_s["Sam_Sellout"])} units</div>', unsafe_allow_html=True)

    # ── SMART STORE LOOKUP (FIXED) ─────────────────────────────────────────────
    with ai_t2:
        st.markdown('<div class="section-header">🔍 Smart Store Lookup</div>', unsafe_allow_html=True)
        st.markdown("Select any store to get a complete AI-powered profile, anomaly history, weekly trends, and action plan.")

        shops_list = sorted(df_raw['Shop Name'].dropna().unique().tolist())
        store_sel = st.selectbox("Select store:", [''] + shops_list)

        if store_sel:
            sd   = df_raw[df_raw['Shop Name'] == store_sel]
            ss_  = sd[sd['Brand'] == 'Samsung']
            # FIX: safe anomaly filter — check column exists and handle NaN
            if len(anomalies_all) > 0 and 'Shop Name' in anomalies_all.columns:
                sa_ = anomalies_all[anomalies_all['Shop Name'].fillna('') == store_sel]
            else:
                sa_ = pd.DataFrame()
            proj_ = sd['Project'].iloc[0] if len(sd) > 0 else 'N/A'
            code_ = sd['Shop Code'].iloc[0] if len(sd) > 0 else 'N/A'
            stot  = sd['Sellout'].sum()
            ssell = ss_['Sellout'].sum()
            sshare = (ssell / stot * 100) if stot > 0 else 0
            sshelf = ss_['Shelf Share'].mean() if len(ss_) > 0 else 0
            if pd.isna(sshelf): sshelf = 0

            anom_color = '#ff5353' if len(sa_) > 0 else '#64ffda'

            st.markdown(f"""
            <div class="store-profile">
                <div style="display:flex;align-items:center;gap:16px;margin-bottom:20px">
                    <span style="font-size:40px">🏪</span>
                    <div>
                        <h2 style="margin:0;color:#e6f1ff;font-size:22px;font-weight:800">{store_sel}</h2>
                        <p style="margin:4px 0 0 0;color:#6272a4;font-size:13px">Project: <b style="color:#0099D5">{proj_}</b> &nbsp;·&nbsp; Code: <b style="color:#8892b0">{code_}</b></p>
                    </div>
                </div>
                <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px">
                    <div style="text-align:center;background:rgba(20,40,160,.08);border-radius:12px;padding:16px">
                        <div style="color:#6272a4;font-size:10px;text-transform:uppercase;letter-spacing:2px">Samsung Sellout</div>
                        <div style="color:#e6f1ff;font-size:28px;font-weight:800;margin:6px 0">{int(ssell)}</div>
                        <div style="color:#64ffda;font-size:12px">units</div>
                    </div>
                    <div style="text-align:center;background:rgba(20,40,160,.08);border-radius:12px;padding:16px">
                        <div style="color:#6272a4;font-size:10px;text-transform:uppercase;letter-spacing:2px">Samsung Share</div>
                        <div style="color:#e6f1ff;font-size:28px;font-weight:800;margin:6px 0">{sshare:.1f}%</div>
                        <div style="color:#64ffda;font-size:12px">of store total</div>
                    </div>
                    <div style="text-align:center;background:rgba(20,40,160,.08);border-radius:12px;padding:16px">
                        <div style="color:#6272a4;font-size:10px;text-transform:uppercase;letter-spacing:2px">Avg Shelf</div>
                        <div style="color:#e6f1ff;font-size:28px;font-weight:800;margin:6px 0">{sshelf:.1f}</div>
                        <div style="color:#64ffda;font-size:12px">units on shelf</div>
                    </div>
                    <div style="text-align:center;background:rgba(20,40,160,.08);border-radius:12px;padding:16px">
                        <div style="color:#6272a4;font-size:10px;text-transform:uppercase;letter-spacing:2px">Anomalies</div>
                        <div style="color:{anom_color};font-size:28px;font-weight:800;margin:6px 0">{len(sa_)}</div>
                        <div style="color:#64ffda;font-size:12px">detected</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**📊 Samsung Weekly at This Store**")
                sw_ = ss_.groupby('W')['Sellout'].sum().reset_index()
                if len(sw_) > 0:
                    fg = px.bar(sw_, x='W', y='Sellout', color='Sellout',
                                color_continuous_scale=['#1a2744', '#1428A0', '#64ffda'], text='Sellout')
                    fg.update_traces(texttemplate='%{text:.0f}', textposition='outside')
                    fg.update_layout(**CL, coloraxis_showscale=False,
                                     xaxis=dict(gridcolor='rgba(45,50,80,.5)'),
                                     yaxis=dict(gridcolor='rgba(45,50,80,.5)'), height=300)
                    st.plotly_chart(fg, use_container_width=True)
                else:
                    st.info("No Samsung weekly data for this store.")
            with c2:
                st.markdown("**🥧 Brand Mix at This Store**")
                sb_ = sd.groupby('Brand')['Shelf Share'].sum().sort_values(ascending=False).head(8).reset_index()
                if len(sb_) > 0 and sb_['Shelf Share'].sum() > 0:
                    fg2 = px.pie(sb_, values='Shelf Share', names='Brand', color='Brand',
                                 color_discrete_map=COLORS, hole=0.52)
                    fg2.update_layout(**CL, showlegend=True, height=300)
                    st.plotly_chart(fg2, use_container_width=True)
                else:
                    st.info("No shelf share data for this store.")

            if len(sa_) > 0:
                st.markdown("**⚠️ Anomaly History**")
                display_cols = [c for c in ['W', 'Brand', 'Model', 'Issue', 'Severity'] if c in sa_.columns]
                st.dataframe(sa_[display_cols].reset_index(drop=True), use_container_width=True)

            st.markdown("**🤖 AI Store Intelligence Report**")
            sctx = (f"Store:{store_sel}|Project:{proj_}|Code:{code_}|"
                    f"Samsung sellout:{int(ssell)}|Samsung share:{sshare:.1f}%|"
                    f"Avg shelf:{sshelf:.1f}|Anomalies:{len(sa_)}|Total store sellout:{int(stot)}|"
                    f"Brands:{sd.groupby('Brand')['Shelf Share'].sum().sort_values(ascending=False).head(5).to_dict()}|"
                    f"Samsung models:{ss_.groupby('Model')['Sellout'].sum().sort_values(ascending=False).head(5).to_dict()}|"
                    f"Weekly Samsung:{ss_.groupby('W')['Sellout'].sum().to_dict()}")

            if st.button("🤖 Generate Store Report", type="primary", use_container_width=True):
                with st.spinner(f"Analyzing {store_sel}..."):
                    sp = f"""You are a Samsung field intelligence analyst for SmartSense-LTD Division MX.
Generate a comprehensive store report for '{store_sel}':
1. Overall assessment (strong/average/weak Samsung performer?)
2. Key strengths at this store
3. Key concerns or red flags
4. Competitive threats specific to this store
5. Specific recommended actions for sales team visit
6. Comment on data reliability if anomalies exist
Be concise, professional, use bullet points. Data: {sctx}"""
                    result = call_ai(sp)
                st.markdown(f'<div class="insight-box">{result}</div>', unsafe_allow_html=True)

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
    <div class="footer-left">
        📱 Samsung Field Intelligence · Merchandiser Data · Fake & Anomaly Detection · AI-Powered
    </div>
    <div class="footer-center">
        ⚡ Innovation Dep · 2026
    </div>
    <div class="footer-right">
        SmartSense-LTD &nbsp;·&nbsp; Division MX
    </div>
</div>
""", unsafe_allow_html=True)
