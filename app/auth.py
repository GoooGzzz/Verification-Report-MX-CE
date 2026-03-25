"""
Authentication and session management for the dashboard
"""
import streamlit as st
from app.config import PASSWORD

def init_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'splash_done' not in st.session_state:
        st.session_state.splash_done = False
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""

def show_login_page() -> bool:
    """Display login page and return authentication status"""
    st.markdown("""
    <style>
    .auth-bg-grid {
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(45deg, #f8fafc 25%, transparent 25%),
                    linear-gradient(-45deg, #f8fafc 25%, transparent 25%),
                    linear-gradient(45deg, transparent 75%, #f8fafc 75%),
                    linear-gradient(-45deg, transparent 75%, #f8fafc 75%);
        background-size: 20px 20px;
        background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
        z-index: -1;
    }
    .auth-wrap {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        padding: 20px;
    }
    .auth-card {
        background: white;
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 20px 60px rgba(0, 122, 255, 0.15);
        border: 2px solid #007aff;
        max-width: 400px;
        width: 100%;
        text-align: center;
    }
    .auth-icon { font-size: 48px; margin-bottom: 16px; }
    .auth-logo {
        font-size: 24px;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 4px;
    }
    .auth-division {
        font-size: 14px;
        color: #6b7280;
        margin-bottom: 24px;
    }
    .auth-title {
        font-size: 18px;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 8px;
    }
    .auth-sub {
        font-size: 14px;
        color: #6b7280;
        margin-bottom: 24px;
    }
    .auth-divider {
        height: 1px;
        background: #e5e7eb;
        margin: 24px 0;
    }
    .auth-footer {
        font-size: 12px;
        color: #9ca3af;
        margin-top: 24px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="auth-bg-grid"></div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-wrap">', unsafe_allow_html=True)

    with st.container():
        st.markdown("""
        <div class="auth-card">
            <div class="auth-icon">🔐</div>
            <div class="auth-logo">SmartSense-LTD</div>
            <div class="auth-division">Division MX · Field Intelligence Platform</div>
            <div class="auth-title">SECURE ACCESS</div>
            <div class="auth-sub">Authorized Personnel Only</div>
            <div class="auth-divider"></div>
        </div>
        """, unsafe_allow_html=True)

        password = st.text_input(
            "Enter Access Password",
            type="password",
            placeholder="Enter password...",
            key="pw_input",
            help="Contact your administrator for access credentials"
        )

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            login_btn = st.button("🔓 AUTHENTICATE", type="primary", use_container_width=True)

        if login_btn or (password and password == PASSWORD):
            if password == PASSWORD:
                st.session_state.authenticated = True
                st.success("✅ Access Granted")
                st.rerun()
            else:
                st.error("❌ Access Denied — Invalid credentials")

        st.markdown('<div class="auth-footer">⚡ Innovation Dep · SmartSense-LTD · 2026</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    return st.session_state.authenticated

def show_splash_screen():
    """Display animated splash screen"""
    st.markdown("""
    <style>
    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
    @keyframes slideUp { from { transform: translateY(30px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
    .splash-wrap {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        padding: 40px;
    }
    .splash-scanline {
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ff88, transparent);
        animation: scan 2s linear infinite;
    }
    .splash-company {
        font-size: 14px;
        opacity: 0.8;
        margin-bottom: 8px;
        animation: slideUp 0.5s ease-out;
    }
    .splash-eyebrow {
        font-size: 12px;
        opacity: 0.7;
        margin-bottom: 24px;
        animation: slideUp 0.5s ease-out 0.1s both;
    }
    .splash-title {
        font-size: 36px;
        font-weight: 800;
        margin-bottom: 16px;
        animation: slideUp 0.5s ease-out 0.2s both;
        line-height: 1.1;
    }
    .splash-sub {
        font-size: 16px;
        opacity: 0.9;
        margin-bottom: 32px;
        animation: slideUp 0.5s ease-out 0.3s both;
        max-width: 500px;
    }
    .splash-divider {
        width: 60px;
        height: 2px;
        background: rgba(255,255,255,0.3);
        margin-bottom: 32px;
        animation: slideUp 0.5s ease-out 0.4s both;
    }
    .splash-bars {
        display: flex;
        gap: 4px;
        margin-bottom: 40px;
        animation: slideUp 0.5s ease-out 0.5s both;
    }
    .splash-bar {
        background: rgba(255,255,255,0.6);
        border-radius: 1px;
        animation: pulse 1.5s ease-in-out infinite;
    }
    @keyframes scan {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100vw); }
    }
    </style>
    """, unsafe_allow_html=True)

    bars_html = "".join([
        f'<div class="splash-bar" style="width:4px;height:{h}px;animation-delay:{d*.5}s"></div>'
        for d, h in enumerate([20, 35, 25, 40, 30, 45, 35, 25, 38, 28, 42, 32])
    ])

    st.markdown('<div class="splash-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="splash-scanline"></div>', unsafe_allow_html=True)
    st.markdown('<div class="splash-company">⚡ SmartSense-LTD</div>', unsafe_allow_html=True)
    st.markdown('<div class="splash-eyebrow">Division MX &nbsp;·&nbsp; Field Intelligence Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="splash-title">SAMSUNG FIELD<br>INTELLIGENCE HUB</div>', unsafe_allow_html=True)
    st.markdown('<div class="splash-sub">Unlocking the Treasure of Your Data</div>', unsafe_allow_html=True)
    st.markdown('<div class="splash-divider"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="splash-bars">{bars_html}</div>', unsafe_allow_html=True)

    if st.button("▶  LAUNCH INTELLIGENCE HUB", type="primary", use_container_width=True, key="launch_btn"):
        st.session_state.splash_done = True
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

def logout():
    """Handle user logout"""
    st.session_state.authenticated = False
    st.session_state.splash_done = False
    st.rerun()