import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
import time
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')

# --- 8K CINEMATIC UI CONFIG ---
st.set_page_config(page_title="SMARTSENSE-LTD | Global Intelligence", page_icon="💎", layout="wide")

# Custom CSS for Glassmorphism and Cinematic UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;800&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; background-color: #050505; }
    
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #020617);
    }
    
    .main-stats-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 30px;
        text-align: center;
        transition: transform 0.3s ease;
    }
    .main-stats-card:hover {
        transform: translateY(-5px);
        border-color: #38bdf8;
    }
    
    .stat-value { font-size: 42px; font-weight: 800; color: #f8fafc; letter-spacing: -1px; }
    .stat-label { font-size: 12px; color: #38bdf8; text-transform: uppercase; font-weight: 700; letter-spacing: 2px; }
    
    .section-header { 
        font-size: 22px; font-weight: 800; color: #f8fafc; 
        margin: 40px 0 20px 0; padding-left: 15px; border-left: 5px solid #38bdf8;
    }
    
    #splash-container {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: #020617; z-index: 9999; display: flex;
        justify-content: center; align-items: center; flex-direction: column;
    }
</style>
""", unsafe_allow_html=True)

# --- AUTH ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align:center; color:white; margin-top:100px;'>💎 SMARTSENSE-LTD COMMAND</h1>", unsafe_allow_html=True)
    with st.container():
        c1, c2, c3 = st.columns([1,1,1])
        with c2:
            pw = st.text_input("", type="password", placeholder="Enter Intelligence Key...")
            if st.button("INITIALIZE SYSTEM", use_container_width=True):
                if pw == "solidspy": 
                    st.session_state.authenticated = True
                    st.rerun()
    st.stop()

# --- SPLASH ANIMATION ---
if 'data_processed' not in st.session_state: st.session_state.data_processed = False

def run_splash():
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
            <div id="splash-container">
                <h1 style="color:#38bdf8; font-weight:800; letter-spacing:10px;">SMARTSENSE-LTD</h1>
                <p style="color:#94a3b8; letter-spacing:4px;">DECRYPTING FIELD INTELLIGENCE...</p>
                <div style="width:200px; height:2px; background:rgba(56,189,248,0.2); margin-top:20px;">
                    <div style="width:50%; height:100%; background:#38bdf8; animation: load 2s infinite;"></div>
                </div>
            </div>
            <style>
                @keyframes load { 0% { width: 0%; } 100% { width: 100%; } }
            </style>
        """, unsafe_allow_html=True)
        time.sleep(2.2)
    placeholder.empty()

# --- DATA ENGINE ---
@st.cache_data
def load_global_intel(att_file, sales_files):
    att = pd.read_excel(att_file)
    att.columns = att.columns.str.strip().str.lower()
    att['duration_min'] = pd.to_timedelta(att['duration'], errors='coerce').dt.total_seconds() / 60
    
    sales = pd.concat([pd.read_excel(f) for f in sales_files], ignore_index=True)
    sales.rename(columns={'Emp Code': 'emp_code', 'Shop Code': 'code', 'Date': 'date', 'Shelf Share': 'shelf'}, inplace=True)
    
    att_agg = att.groupby(['emp_code', 'code']).agg(Visits=('id', 'count'), Total_Hours=('duration_min', lambda x: x.sum()/60)).reset_index()
    sales_agg = sales.groupby(['emp_code', 'code']).agg(Sellout=('Sellout', 'sum'), Avg_Shelf=('shelf', 'mean')).reset_index()
    
    merged = pd.merge(att_agg, sales_agg, on=['emp_code', 'code'], how='outer').fillna(0)
    merged['ROI'] = (merged['Sellout'] / merged['Total_Hours']).replace([float('inf')], 0).fillna(0)
    return merged, att, sales

# --- UI LAYOUT ---
st.sidebar.markdown("<h2 style='color:#38bdf8;'>🛰️ DATA UPLINK</h2>", unsafe_allow_html=True)
att_up = st.sidebar.file_uploader("Attendance Intel", type=['xlsx'])
sales_up = st.sidebar.file_uploader("Sales/Sellout Intel", type=['xlsx'], accept_multiple_files=True)

if not att_up or not sales_up:
    st.markdown("<h1 style='font-weight:900; color:white;'>SMARTSENSE-LTD : HUB</h1>", unsafe_allow_html=True)
    st.info("Awaiting secure data uplink to generate cinematic reports...")
    st.stop()

if not st.session_state.data_processed:
    run_splash()
    st.session_state.data_processed = True

roi_df, df_att, df_sales = load_global_intel(att_up, sales_up)

# --- 8K DASHBOARD ---
st.markdown("<h1 style='font-weight:900; color:white; margin-bottom:0;'>PLATINUM EXECUTIVE VIEW</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#38bdf8; margin-top:0;'>SMARTSENSE-LTD • Division Intelligence</p>", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)
with k1: st.markdown(f'<div class="main-stats-card"><div class="stat-label">Market Sellout</div><div class="stat-value">{df_sales["Sellout"].sum():,.0f}</div></div>', unsafe_allow_html=True)
with k2: st.markdown(f'<div class="main-stats-card"><div class="stat-label">Market Share (Shelf)</div><div class="stat-value">{df_sales["shelf"].mean():.1f}%</div></div>', unsafe_allow_html=True)
with k3: st.markdown(f'<div class="main-stats-card"><div class="stat-label">ROI Multiplier</div><div class="stat-value">{(df_sales["Sellout"].sum()/(df_att["duration_min"].sum()/60)):.2f}x</div></div>', unsafe_allow_html=True)
with k4: st.markdown(f'<div class="main-stats-card"><div class="stat-label">Active Agents</div><div class="stat-value">{df_att["emp_code"].nunique()}</div></div>', unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["💎 MARKET MATRIX", "🏹 AGENT PERFORMANCE", "🛰️ OPERATIONAL AUDIT"])

with t1:
    st.markdown('<div class="section-header">The Market Dominance Matrix</div>', unsafe_allow_html=True)
    fig = px.scatter(roi_df, x="Total_Hours", y="Sellout", size="Visits", color="ROI",
                     hover_name="code", color_continuous_scale="Viridis",
                     template="plotly_dark", title="Market Value vs. Time Investment")
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color="#f8fafc")
    st.plotly_chart(fig, use_container_width=True)

with t2:
    st.markdown('<div class="section-header">AI-Driven Agent Personas</div>', unsafe_allow_html=True)
    
    q_high = roi_df['ROI'].quantile(0.8)
    def agent_intel(row):
        if row['ROI'] >= q_high: return "💎 ELITE CLOSER"
        if row['Sellout'] == 0 and row['Total_Hours'] > 10: return "🔴 RESOURCE DRAIN"
        if row['Avg_Shelf'] > 80: return "🏆 BRAND GUARDIAN"
        return "⚙️ STEADY PERFORMER"

    roi_df['Intelligence_Tag'] = roi_df.apply(agent_intel, axis=1)
    
    # FIXED: Removed .style.background_gradient to prevent Matplotlib ImportError
    # Using Streamlit's native dataframe styling for high-performance rendering
    st.dataframe(
        roi_df.sort_values("ROI", ascending=False), 
        use_container_width=True,
        column_config={
            "ROI": st.column_config.ProgressColumn("Efficiency (ROI)", format="%.2f", min_value=0, max_value=float(roi_df['ROI'].max())),
            "Avg_Shelf": st.column_config.NumberColumn("Shelf Share %", format="%.1f%%")
        }
    )

with t3:
    st.markdown('<div class="section-header">Executive Briefing & Discrepancies</div>', unsafe_allow_html=True)
    
    top_performer = roi_df.iloc[roi_df['ROI'].idxmax()]['emp_code'] if not roi_df.empty else "N/A"
    total_waste = len(roi_df[(roi_df['Sellout'] == 0) & (roi_df['Total_Hours'] > 5)])
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div style="background:rgba(56,189,248,0.1); padding:20px; border-radius:15px; border:1px solid #38bdf8;">
            <h4 style="color:#38bdf8; margin-top:0;">SMARTSENSE-LTD INTELLIGENCE</h4>
            <p style="color:white;">Current operational audit identifies <b>{top_performer}</b> as the lead ROI generator. 
            System detected <b>{total_waste}</b> leakage points where labor cost is high with zero revenue conversion.
            Action required: Re-assign agents categorized as 'Resource Drain'.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        efficiency_val = (roi_df[roi_df['Sellout']>0]['emp_code'].nunique() / roi_df['emp_code'].nunique()) * 100 if not roi_df.empty else 0
        efficiency_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = efficiency_val,
            title = {'text': "Active Revenue Coverage %", 'font': {'color': "white"}},
            gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#38bdf8"}}
        ))
        efficiency_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", height=250, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(efficiency_gauge, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.caption("ENGINE: V3.5 PLATINUM • SMARTSENSE-LTD")