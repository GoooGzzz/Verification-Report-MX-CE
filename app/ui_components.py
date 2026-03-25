"""
UI components and styling for the dashboard
"""
import streamlit as st
from typing import Dict, Any

def load_css():
    """Load the One UI 8 CSS styling"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    *, *::before, *::after { box-sizing: border-box; }
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background: #f8fafc !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    [data-testid="stAppViewContainer"] {
        background: #f8fafc !important;
        min-height: 100vh;
    }

    /* ── ONE UI 8 DESIGN SYSTEM ── */
    :root {
        --oneui-primary: #007aff;
        --oneui-secondary: #636366;
        --oneui-surface: #ffffff;
        --oneui-surface-variant: #f2f2f7;
        --oneui-on-surface: #1c1c1e;
        --oneui-on-surface-variant: #3a3a3c;
        --oneui-outline: #c6c6c8;
        --oneui-error: #ff3b30;
        --oneui-success: #34c759;
        --oneui-warning: #ff9500;
        --oneui-radius-s: 8px;
        --oneui-radius-m: 12px;
        --oneui-radius-l: 16px;
        --oneui-radius-xl: 28px;
        --oneui-shadow-light: 0 1px 3px rgba(0, 0, 0, 0.1);
        --oneui-shadow-medium: 0 2px 8px rgba(0, 0, 0, 0.12);
        --oneui-shadow-heavy: 0 4px 16px rgba(0, 0, 0, 0.15);
    }

    /* ── TYPOGRAPHY ── */
    .oneui-headline {
        font-size: 28px;
        font-weight: 700;
        line-height: 1.3;
        color: var(--oneui-on-surface);
        letter-spacing: -0.5px;
    }
    .oneui-title {
        font-size: 22px;
        font-weight: 600;
        line-height: 1.4;
        color: var(--oneui-on-surface);
    }
    .oneui-body {
        font-size: 17px;
        font-weight: 400;
        line-height: 1.5;
        color: var(--oneui-on-surface);
    }
    .oneui-caption {
        font-size: 13px;
        font-weight: 500;
        line-height: 1.4;
        color: var(--oneui-on-surface-variant);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* ── COMPONENTS ── */
    .oneui-card {
        background: var(--oneui-surface);
        border-radius: var(--oneui-radius-l);
        padding: 20px;
        box-shadow: var(--oneui-shadow-light);
        border: 1px solid var(--oneui-outline);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .oneui-card:hover {
        box-shadow: var(--oneui-shadow-medium);
        transform: translateY(-2px);
    }

    .oneui-button {
        background: var(--oneui-primary);
        color: white;
        border: none;
        border-radius: var(--oneui-radius-m);
        padding: 12px 24px;
        font-size: 17px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: var(--oneui-shadow-light);
    }
    .oneui-button:hover {
        background: #0056cc;
        box-shadow: var(--oneui-shadow-medium);
        transform: translateY(-1px);
    }

    .oneui-chip {
        background: var(--oneui-surface-variant);
        border: 1px solid var(--oneui-outline);
        border-radius: var(--oneui-radius-xl);
        padding: 8px 16px;
        font-size: 14px;
        font-weight: 500;
        color: var(--oneui-on-surface);
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }

    /* ── LAYOUT ── */
    .oneui-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 24px;
    }

    .oneui-section {
        margin-bottom: 32px;
    }

    .oneui-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        margin-bottom: 24px;
    }

    /* ── SPECIFIC COMPONENTS ── */
    .oneui-metric-card {
        background: var(--oneui-surface);
        border-radius: var(--oneui-radius-l);
        padding: 24px;
        text-align: center;
        box-shadow: var(--oneui-shadow-light);
        border: 1px solid var(--oneui-outline);
        transition: all 0.3s ease;
    }
    .oneui-metric-card:hover {
        box-shadow: var(--oneui-shadow-medium);
        transform: translateY(-4px);
    }
    .oneui-metric-value {
        font-size: 36px;
        font-weight: 800;
        color: var(--oneui-primary);
        line-height: 1.2;
        margin-bottom: 8px;
    }
    .oneui-metric-label {
        font-size: 15px;
        color: var(--oneui-on-surface-variant);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .oneui-metric-sub {
        font-size: 13px;
        color: var(--oneui-secondary);
        margin-top: 8px;
    }

    .oneui-header {
        background: var(--oneui-surface);
        border-radius: var(--oneui-radius-xl);
        padding: 24px 32px;
        margin-bottom: 24px;
        box-shadow: var(--oneui-shadow-light);
        border: 1px solid var(--oneui-outline);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .oneui-header-left {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    .oneui-header-title {
        font-size: 20px;
        font-weight: 700;
        color: var(--oneui-on-surface);
        margin: 0;
    }
    .oneui-header-subtitle {
        font-size: 14px;
        color: var(--oneui-on-surface-variant);
        margin: 4px 0 0 0;
        font-weight: 500;
    }
    .oneui-header-badges {
        display: flex;
        gap: 12px;
    }

    .oneui-sidebar {
        background: var(--oneui-surface);
        border-radius: var(--oneui-radius-l);
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: var(--oneui-shadow-light);
        border: 1px solid var(--oneui-outline);
    }
    .oneui-sidebar-title {
        font-size: 14px;
        color: var(--oneui-on-surface-variant);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    .oneui-sidebar-value {
        font-size: 24px;
        font-weight: 700;
        color: var(--oneui-on-surface);
    }

    /* ── TABS ── */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--oneui-surface) !important;
        border-radius: var(--oneui-radius-l) !important;
        border: 1px solid var(--oneui-outline) !important;
        box-shadow: var(--oneui-shadow-light) !important;
        gap: 0 !important;
        padding: 4px !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: var(--oneui-on-surface-variant) !important;
        border-radius: var(--oneui-radius-m) !important;
        font-weight: 500 !important;
        font-size: 15px !important;
        transition: all 0.2s ease !important;
        padding: 12px 20px !important;
    }
    .stTabs [aria-selected="true"] {
        background: var(--oneui-primary) !important;
        color: white !important;
        box-shadow: 0 2px 8px rgba(0, 122, 255, 0.3) !important;
    }
    .stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {
        color: var(--oneui-primary) !important;
        background: var(--oneui-surface-variant) !important;
    }

    /* ── SIDEBAR ── */
    div[data-testid="stSidebar"] {
        background: var(--oneui-surface) !important;
        border-right: 1px solid var(--oneui-outline) !important;
        box-shadow: var(--oneui-shadow-light) !important;
    }

    /* ── INPUTS ── */
    [data-testid="stSelectbox"] > div > div,
    [data-testid="stTextInput"] > div > div {
        border-radius: var(--oneui-radius-m) !important;
        background: var(--oneui-surface) !important;
        border: 1px solid var(--oneui-outline) !important;
        box-shadow: var(--oneui-shadow-light) !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stSelectbox"] > div > div:hover,
    [data-testid="stTextInput"] > div > div:hover {
        border-color: var(--oneui-primary) !important;
        box-shadow: 0 0 0 2px rgba(0, 122, 255, 0.1) !important;
    }

    /* ── DATAFRAMES ── */
    .stDataFrame {
        border-radius: var(--oneui-radius-l) !important;
        overflow: hidden;
        border: 1px solid var(--oneui-outline);
        box-shadow: var(--oneui-shadow-light);
    }

    /* ── ALERTS ── */
    .alert-success {
        background: rgba(52, 199, 89, 0.1);
        border: 1px solid var(--oneui-success);
        border-radius: var(--oneui-radius-m);
        padding: 16px;
        margin: 8px 0;
        color: var(--oneui-success);
        font-weight: 500;
    }
    .alert-warning {
        background: rgba(255, 149, 0, 0.1);
        border: 1px solid var(--oneui-warning);
        border-radius: var(--oneui-radius-m);
        padding: 16px;
        margin: 8px 0;
        color: var(--oneui-warning);
        font-weight: 500;
    }
    .alert-danger {
        background: rgba(255, 59, 48, 0.1);
        border: 1px solid var(--oneui-error);
        border-radius: var(--oneui-radius-m);
        padding: 16px;
        margin: 8px 0;
        color: var(--oneui-error);
        font-weight: 500;
    }

    /* ── ANIMATIONS ── */
    @keyframes oneui-fade-in {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes oneui-pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    .oneui-fade-in {
        animation: oneui-fade-in 0.5s ease-out;
    }
    .oneui-pulse {
        animation: oneui-pulse 2s ease-in-out infinite;
    }

    /* ── RESPONSIVE ── */
    @media (max-width: 768px) {
        .oneui-container {
            padding: 0 16px;
        }
        .oneui-grid {
            grid-template-columns: 1fr;
            gap: 16px;
        }
        .oneui-header {
            flex-direction: column;
            gap: 16px;
            text-align: center;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def create_metric_card(label: str, value: str, subtitle: str = "") -> str:
    """Create a One UI 8 metric card"""
    return f"""
    <div class="oneui-metric-card">
        <div class="oneui-metric-label">{label}</div>
        <div class="oneui-metric-value">{value}</div>
        {f'<div class="oneui-metric-sub">{subtitle}</div>' if subtitle else ''}
    </div>
    """

def create_sidebar_metrics(kpis: Dict[str, Any]) -> str:
    """Create sidebar metrics display"""
    return f"""
    <div class="oneui-sidebar">
        <div class="oneui-sidebar-title">📈 Key Metrics</div>
        <div style='font-size:14px; line-height:1.6; color:#374151; font-weight:500'>
        • Samsung Sellout: <strong>{int(kpis.get('sam_sellout', 0)):,}</strong> units<br>
        • Market Share: <strong>{kpis.get('sam_share_pct', 0):.1f}%</strong><br>
        • Avg Shelf Share: <strong>{kpis.get('sam_avg_shelf', 0):.1f}%</strong><br>
        • Anomalies Detected: <strong>{kpis.get('anomalies_count', 0)}</strong><br>
        • High Risk Issues: <strong>{kpis.get('high_risk_count', 0)}</strong>
        </div>
    </div>
    """

def create_sidebar_summary(kpis: Dict[str, Any]) -> str:
    """Create sidebar data summary"""
    return f"""
    <div class="oneui-sidebar">
        <div class="oneui-sidebar-title">📊 Data Summary</div>
        <div style='font-size:14px; line-height:1.6; color:#374151; font-weight:500'>
        • {kpis.get('total_records', 0):,} records loaded<br>
        • {kpis.get('total_shops', 0)} active stores<br>
        • {kpis.get('weeks_analyzed', 0)} weeks analyzed<br>
        • {kpis.get('brands_tracked', 0)} brands tracked<br>
        • {kpis.get('categories', 0)} categories<br>
        • {kpis.get('price_segments', 0)} price segments
        </div>
    </div>
    """

def create_header(title: str, subtitle: str = "", badges: list = None) -> str:
    """Create One UI 8 header component"""
    badges_html = ""
    if badges:
        badges_html = "".join([f'<div class="oneui-chip">{badge}</div>' for badge in badges])

    return f"""
    <div class="oneui-header">
        <div class="oneui-header-left">
            <span style="font-size:24px">📊</span>
            <div>
                <div class="oneui-header-title">{title}</div>
                {f'<div class="oneui-header-subtitle">{subtitle}</div>' if subtitle else ''}
            </div>
        </div>
        {f'<div class="oneui-header-badges">{badges_html}</div>' if badges_html else ''}
    </div>
    """

def create_processing_screen() -> str:
    """Create processing screen with One UI 8 styling"""
    return """
    <div class="oneui-card" style="text-align: center; background: linear-gradient(135deg, #f0f9ff, #f8fafc); border: 2px solid var(--oneui-primary);">
        <div style="font-size:48px;margin-bottom:16px;animation:oneui-pulse 2s ease infinite">⚙️</div>
        <h3 class="oneui-title" style="margin:0 0 12px 0;">Processing Your Data</h3>
        <p class="oneui-body" style="margin:0 0 20px 0;">Analyzing records, detecting anomalies, computing insights...</p>
        <div style="display:flex;gap:6px;justify-content:center;margin:24px 0">
            <div style="width:8px;height:8px;background:var(--oneui-primary);border-radius:50%;animation:oneui-pulse 1.4s ease infinite"></div>
            <div style="width:8px;height:8px;background:#0056cc;border-radius:50%;animation:oneui-pulse 1.4s ease infinite 0.2s"></div>
            <div style="width:8px;height:8px;background:#004299;border-radius:50%;animation:oneui-pulse 1.4s ease infinite 0.4s"></div>
        </div>
        <p class="oneui-caption" style="margin:0;">Building Real-Time Dashboard...</p>
    </div>
    """

def show_success_alert(message: str):
    """Show success alert"""
    st.markdown(f'<div class="alert-success">✅ {message}</div>', unsafe_allow_html=True)

def show_warning_alert(message: str):
    """Show warning alert"""
    st.markdown(f'<div class="alert-warning">⚠️ {message}</div>', unsafe_allow_html=True)

def show_error_alert(message: str):
    """Show error alert"""
    st.markdown(f'<div class="alert-danger">❌ {message}</div>', unsafe_allow_html=True)