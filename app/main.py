"""
Samsung Field Intelligence Dashboard - Main Application
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import warnings
warnings.filterwarnings('ignore')

# Import our modules
from app.config import (
    APP_TITLE, APP_ICON, LAYOUT, SIDEBAR_STATE,
    REQUIRED_COLUMNS, MAX_FILE_SIZE_MB, SUPPORTED_FILE_TYPES
)
from app.auth import init_session_state, show_login_page, show_splash_screen, logout
from app.data_processing import (
    load_data, detect_anomalies, build_store_agg,
    build_wow_alerts, calculate_kpis
)
from app.ai_integration import get_ai_insights, generate_store_report, analyze_anomalies, generate_executive_summary
from app.ui_components import (
    load_css, create_metric_card, create_sidebar_metrics, create_sidebar_summary,
    create_header, create_processing_screen, show_success_alert, show_warning_alert, show_error_alert
)

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=LAYOUT,
    initial_sidebar_state=SIDEBAR_STATE
)

# ─── LOAD STYLING ─────────────────────────────────────────────────────────────
load_css()

# ─── INITIALIZE SESSION STATE ─────────────────────────────────────────────────
init_session_state()

# ─── AUTHENTICATION FLOW ──────────────────────────────────────────────────────
if not st.session_state.authenticated:
    if show_login_page():
        st.rerun()
        st.stop()

if not st.session_state.splash_done:
    show_splash_screen()
        st.stop()

# ─── FILE UPLOAD ──────────────────────────────────────────────────────────────
st.markdown(create_header(
    "SmartSense-LTD",
    "Division MX · Samsung Field Intelligence Platform",
    ["AI-POWERED", "LIVE DATA"]
), unsafe_allow_html=True)

uploaded = st.file_uploader(
    "📤 Upload Excel File",
    type=SUPPORTED_FILE_TYPES,
    help=f"Upload Excel file with required columns: {', '.join(REQUIRED_COLUMNS)}"
)

if not uploaded:
        st.info("👆 Please upload an Excel file to begin analysis")
        st.stop()

# ─── LOAD & PROCESS DATA ──────────────────────────────────────────────────────
try:
    with st.spinner("Processing your data..."):
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown(create_processing_screen(), unsafe_allow_html=True)

        df_raw = load_data(uploaded)
        anomalies_all = detect_anomalies(df_raw)
        wow_all = build_wow_alerts(df_raw)

    show_success_alert("Data processed successfully!")
        st.session_state.data_loaded = True
        st.rerun()

except Exception as e:
    show_error_alert(f"Error processing data: {str(e)}")
    show_warning_alert(f"Please check your Excel file format and ensure it contains the required columns: {', '.join(REQUIRED_COLUMNS)}")
        st.stop()

# ─── MAIN APPLICATION (only runs after data is loaded) ────────────────────────
if st.session_state.get('data_loaded', False):

    # ─── SIDEBAR FILTERS + AI SETTINGS ───────────────────────────────────────────
    with st.sidebar:
        
        st.divider()
        
        st.markdown("**🔽 Filters**", help="Filter data by week, project, category, and price segment")
        

        
        weeks = ['All'] + sorted(df_raw['W'].dropna().unique().tolist())
        sel_week = st.selectbox("📅 Week", weeks)

        projs = ['All'] + sorted(df_raw['Project'].dropna().unique().tolist())
        sel_proj = st.selectbox("📋 Project", projs)

        cats = ['All'] + sorted(df_raw['Category'].dropna().unique().tolist())
        sel_cat = st.selectbox("📦 Category", cats)

        segs = ['All'] + sorted(df_raw['Price segmentation'].dropna().unique().tolist())
        sel_seg = st.selectbox("💰 Price Segment", segs)
        

        
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
        

        
        st.markdown(create_sidebar_summary(kpis), unsafe_allow_html=True)
        
        st.divider()
        

        
    if st.button("🚪 Logout", use_container_width=True):
        
        logout()
        

        
# ─── APPLY FILTERS ────────────────────────────────────────────────────────────
        
df = df_raw.copy()
        
if sel_week != 'All': df = df[df['W'] == sel_week]
        
if sel_proj != 'All': df = df[df['Project'] == sel_proj]
        
if sel_cat  != 'All': df = df[df['Category'] == sel_cat]
        
if sel_seg  != 'All': df = df[df['Price segmentation'] == sel_seg]
        

        
anomalies = anomalies_all[anomalies_all['W'].isin(df['W'].unique())] if sel_week != 'All' else anomalies_all.copy()
        
store_agg = build_store_agg(df)
        
high = anomalies[anomalies['Severity'] == 'HIGH']
        
med = anomalies[anomalies['Severity'] == 'MEDIUM']
        
low = anomalies[anomalies['Severity'] == 'LOW'] if 'LOW' in anomalies['Severity'].values else pd.DataFrame()
        

        
# ─── COMPUTED KPIs ────────────────────────────────────────────────────────────
        
kpis = calculate_kpis(df)
        
kpis['anomalies_count'] = len(anomalies)
        
kpis['high_risk_count'] = len(high)
        

        
# ─── UPDATE SIDEBAR WITH KEY METRICS ──────────────────────────────────────────
        
with st.sidebar:
        
        st.markdown(create_sidebar_metrics(kpis), unsafe_allow_html=True)
        

        
# ─── MAIN TITLE ───────────────────────────────────────────────────────────────
        
st.markdown("""
        
<div class="oneui-container">
        
    <h1 class="oneui-headline">Samsung Field Intelligence Dashboard</h1>
        
    <p class="oneui-body">Merchandiser Data · Fake & Anomaly Detection · AI-Powered Insights · Real-Time Intelligence</p>
        
</div>
        
""", unsafe_allow_html=True)
        

        
# ─── KPI ROW ──────────────────────────────────────────────────────────────────
        
k1, k2, k3, k4, k5 = st.columns(5)
        
with k1: st.markdown(create_metric_card("Total Shops", f"{kpis['total_shops']:,}", "Active stores"), unsafe_allow_html=True)
        
with k2: st.markdown(create_metric_card("Samsung Sellout", f"{int(kpis['sam_sellout']):,}", "Units sold"), unsafe_allow_html=True)
        
with k3: st.markdown(create_metric_card("Market Share", f"{kpis['sam_share_pct']:.1f}%", "Of total sellout"), unsafe_allow_html=True)
        
with k4: st.markdown(create_metric_card("Avg Shelf Share", f"{kpis['sam_avg_shelf']:.1f}%", "Per store"), unsafe_allow_html=True)
        

        
ac = "#ff3b30" if len(anomalies) > 50 else "#ff9500" if len(anomalies) > 20 else "#34c759"
        
with k5: st.markdown(create_metric_card("⚠️ Anomalies", f"{len(anomalies)}", "Requires review", f"color:{ac}"), unsafe_allow_html=True)
        

        
# ─── EXECUTIVE SUMMARY ────────────────────────────────────────────────────────
        
st.markdown("""
        
<div class="oneui-card">
        
    <h2 class="oneui-title">🚀 Executive Summary</h2>
        
""", unsafe_allow_html=True)
        

        
col1, col2 = st.columns([2, 1])
        
with col1:
        
        st.markdown(f"""
        
    This dashboard provides cutting-edge AI-powered analytics for Samsung's field intelligence operations.
        

        
    **Current Performance:**
        
    - **{kpis['total_shops']:,} stores** actively reporting data
        
    - **{kpis['sam_share_pct']:.1f}% market share** across all tracked locations
        
    - **{kpis['sam_avg_shelf']:.1f}% average shelf share** per store
        
    - **{len(anomalies)} anomalies** detected requiring attention
        

        
    **Data Coverage:** {kpis['weeks_analyzed']} weeks, {kpis['brands_tracked']} brands, {kpis['categories']} categories
        
    """)
        

        
with col2:
        
    if st.button("🤖 Generate AI Summary", use_container_width=True):
        
        with st.spinner("Generating executive summary..."):
        
            ai_summary = generate_executive_summary(kpis, st.session_state.api_key)
        
            st.markdown("**AI-Generated Executive Summary:**")
        
            st.markdown(ai_summary)
        

        
# ─── MAIN DASHBOARD TABS ──────────────────────────────────────────────────────
        
tabs = st.tabs([
        
    "📊 Overview", "📦 Brand Analysis", "🥧 Market Share", "📐 Shelf Analysis",
        
    "🔮 3D Analytics", "🏆 Leaderboards", "📈 Trends", "🚨 Anomalies",
        
    "🚦 WoW Alerts", "🔢 Brand Pivot", "🚨 Fake Detection", "🏅 Team Performance"
        
])
        

        
# Tab implementations would go here - keeping the structure for now
        
with tabs[0]:  # Overview
        
        st.markdown('<h2 class="oneui-title">📊 Overview</h2>', unsafe_allow_html=True)
        
        st.info("Dashboard overview content would go here")
        

        
with tabs[1]:  # Brand Analysis
        
        st.markdown('<h2 class="oneui-title">📦 Brand Analysis</h2>', unsafe_allow_html=True)
        
        st.info("Brand analysis content would go here")
        

        
with tabs[2]:  # Market Share
        
        st.markdown('<h2 class="oneui-title">🥧 Market Share</h2>', unsafe_allow_html=True)
        
        st.info("Market share analysis would go here")
        

        
with tabs[3]:  # Shelf Analysis
        
        st.markdown('<h2 class="oneui-title">📐 Shelf Analysis</h2>', unsafe_allow_html=True)
        
        st.info("Shelf share analysis would go here")
        

        
with tabs[4]:  # 3D Analytics
        
        st.markdown('<h2 class="oneui-title">🔮 3D Analytics</h2>', unsafe_allow_html=True)
        
        st.info("3D market analysis would go here")
        

        
with tabs[5]:  # Leaderboards
        
        st.markdown('<h2 class="oneui-title">🏆 Leaderboards</h2>', unsafe_allow_html=True)
        
        st.info("Store performance leaderboards would go here")
        

        
with tabs[6]:  # Trends
        
        st.markdown('<h2 class="oneui-title">📈 Trends</h2>', unsafe_allow_html=True)
        
        st.info("Weekly trend analysis would go here")
        

        
with tabs[7]:  # Anomalies
        
        st.markdown('<h2 class="oneui-title">🚨 Anomalies</h2>', unsafe_allow_html=True)
        

        
    if not anomalies.empty:
        
        st.markdown(f"**{len(anomalies)} anomalies detected**")
        

        
        # Severity breakdown
        
        severity_counts = anomalies['Severity'].value_counts()
        
        st.markdown("**Severity Breakdown:**")
        
        for severity, count in severity_counts.items():
        
            color = {"HIGH": "🔴", "MEDIUM": "🟠", "LOW": "🟡"}.get(severity, "⚪")
        
            st.markdown(f"{color} {severity}: {count}")
        

        
        # Show anomalies table
        
        st.dataframe(anomalies, use_container_width=True)
        

        
        # AI Analysis
        
        if st.button("🤖 Analyze Anomalies with AI"):
        
            with st.spinner("Analyzing anomalies..."):
        
                ai_analysis = analyze_anomalies(anomalies, st.session_state.api_key)
        
                st.markdown("**AI Analysis:**")
        
                st.markdown(ai_analysis)
        
    else:
        
        show_success_alert("No anomalies detected in the current dataset")
        

        
with tabs[8]:  # WoW Alerts
        
        st.markdown('<h2 class="oneui-title">🚦 Week-over-Week Alerts</h2>', unsafe_allow_html=True)
        
        st.info("WoW alerts content would go here")
        

        
with tabs[9]:  # Brand Pivot
        
        st.markdown('<h2 class="oneui-title">🔢 Brand Pivot</h2>', unsafe_allow_html=True)
        
        st.info("Brand pivot analysis would go here")
        

        
with tabs[10]:  # Fake Detection
        
        st.markdown('<h2 class="oneui-title">🚨 Fake Detection</h2>', unsafe_allow_html=True)
        
        st.info("Fake data detection would go here")
        

        
with tabs[11]:  # Team Performance
        
        st.markdown('<h2 class="oneui-title">🏅 Team Performance</h2>', unsafe_allow_html=True)
        
        st.info("Team performance analysis would go here")
        

        
    # ─── FOOTER ───────────────────────────────────────────────────────────────────
        
        st.markdown("---")
        
        st.markdown("""
        
    <div style="text-align: center; color: #6b7280; font-size: 14px;">
        
        <strong>SmartSense-LTD</strong> | Division MX | Field Intelligence Platform | Innovation Department © 2026
        
    </div>
        
    """, unsafe_allow_html=True)
        

        

        

        
