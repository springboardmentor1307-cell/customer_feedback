# ============================
# ReviewSense – Login Page
# ============================

import streamlit as st
import hashlib

st.set_page_config(
    page_title="ReviewSense – Login",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Credentials (SHA-256 hashed) ─────────────────────────────
USERS = {
    "admin":   hashlib.sha256("admin123".encode()).hexdigest(),
    "analyst": hashlib.sha256("review2025".encode()).hexdigest(),
}

# ── Session State ─────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ── CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
#MainMenu, footer, header { display: none !important; }

[data-testid="stAppViewContainer"] {
    background: #0a0e1a !important;
}

/* ✅ Fix white text – target every possible Streamlit input selector */
input[type="text"],
input[type="password"],
input[type="email"],
.stTextInput input,
.stTextInput > div > div > input,
[data-testid="stTextInput"] input,
[data-baseweb="input"] input,
[data-baseweb="base-input"] input {
    color: #111111 !important;
    background-color: #ffffff !important;
    caret-color: #111111 !important;
    -webkit-text-fill-color: #111111 !important;
    border: 1.5px solid #cccccc !important;
    border-radius: 8px !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 1rem !important;
}

input[type="text"]:focus,
input[type="password"]:focus,
.stTextInput input:focus {
    border-color: #1d63dc !important;
    box-shadow: 0 0 0 3px rgba(29,99,220,0.2) !important;
    outline: none !important;
}

/* Input wrapper background */
[data-baseweb="base-input"],
[data-baseweb="input"] {
    background-color: #ffffff !important;
}

/* Input labels */
.stTextInput label,
[data-testid="stTextInput"] label {
    color: rgba(255,255,255,0.8) !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

/* Sign In button */
.stButton > button {
    width: 100% !important;
    background: #1d63dc !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    padding: 0.7rem !important;
    margin-top: 0.5rem !important;
}
.stButton > button:hover {
    background: #1752ba !important;
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# ── Redirect if already logged in ─────────────────────────────
if st.session_state.authenticated:
    st.success(f"✅ Welcome back, **{st.session_state.username}**!")
    st.page_link("milestone4.py", label="➡️ Go to Dashboard", icon="📊")
    st.stop()

# ── Login UI ───────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 2.5rem 0 1.5rem;">
    <div style="font-size:2.8rem; margin-bottom:0.5rem;">📊</div>
    <h1 style="color:#ffffff; font-size:2rem; margin:0; font-weight:800;">ReviewSense</h1>
    <p style="color:rgba(255,255,255,0.45); margin:0.3rem 0 0; font-size:0.9rem;">
        Customer Feedback Intelligence Platform
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<h3 style='color:#ffffff; margin-bottom:0.1rem;'>Welcome back</h3>", unsafe_allow_html=True)
st.markdown("<p style='color:rgba(255,255,255,0.4); margin-bottom:1rem; font-size:0.88rem;'>Sign in to access your dashboard</p>", unsafe_allow_html=True)

username = st.text_input("Username", placeholder="Enter your username")
password = st.text_input("Password", placeholder="Enter your password", type="password")

st.markdown("<div style='margin:0.4rem 0'></div>", unsafe_allow_html=True)

if st.button("Sign In →", use_container_width=True):
    if not username or not password:
        st.error("⚠️ Please enter both username and password.")
    elif USERS.get(username.strip().lower()) == hashlib.sha256(password.encode()).hexdigest():
        st.session_state.authenticated = True
        st.session_state.username = username.strip().lower()
        st.success("✅ Login successful! Loading dashboard…")
        st.rerun()
    else:
        st.error("❌ Invalid username or password.")

st.markdown("""
<p style="text-align:center; color:rgba(255,255,255,0.3); font-size:0.78rem; margin-top:1.2rem;">
    Demo — username: <span style="color:#38c9a4; font-weight:600;">admin</span>
    &nbsp;·&nbsp;
    password: <span style="color:#38c9a4; font-weight:600;">admin123</span>
</p>
""", unsafe_allow_html=True)
