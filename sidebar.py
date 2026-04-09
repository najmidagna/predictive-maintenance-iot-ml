import streamlit as st
import datetime

def show_sidebar():
    with st.sidebar:
        st.markdown("""
        <style>
        .sidebar-title {
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 2px;
            text-shadow: 1px 1px 4px rgba(0,0,0,0.2);
        }

        .sidebar-subtitle {
            font-size: 13px;
            opacity: 0.8;
            margin-bottom: 18px;
        }

        .sidebar-box {
            background: rgba(255, 255, 255, 0.05);
            padding: 12px 14px;
            border-radius: 12px;
            margin-bottom: 12px;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        .sidebar-label {
            font-size: 12px;
            opacity: 0.75;
            margin-bottom: 4px;
        }

        .sidebar-value {
            font-size: 14px;
            font-weight: 600;
        }

        .sidebar-footer {
            font-size: 12px;
            opacity: 0.7;
            text-align: center;
            margin-top: 20px;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sidebar-title">🛠️ Predictive Maintenance</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-subtitle">Oil & Gas Equipment Monitoring</div>', unsafe_allow_html=True)

        username = st.session_state.get("username", "Guest")
        role = st.session_state.get("role", "user").capitalize()
        current_time = datetime.datetime.now().strftime("%d %b %Y • %H:%M")

        st.markdown(f"""
        <div class="sidebar-box">
            <div class="sidebar-label">Logged in as</div>
            <div class="sidebar-value">👤 {username}</div>
            <div class="sidebar-label" style="margin-top:8px;">Role</div>
            <div class="sidebar-value">🔑 {role}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="sidebar-box">
            <div class="sidebar-label">System Status</div>
            <div class="sidebar-value">🟢 Active</div>
            <div class="sidebar-label" style="margin-top:8px;">Model</div>
            <div class="sidebar-value">📊 XGBoost</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="sidebar-box">
            <div class="sidebar-label">Current Time</div>
            <div class="sidebar-value">📅 {current_time}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.caption("Use the page menu above to navigate through the system.")
        st.markdown('<div class="sidebar-footer">Najmi Dagna • Final Year Project • 2026</div>', unsafe_allow_html=True)