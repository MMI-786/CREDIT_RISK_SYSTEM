import streamlit as st
import jwt, datetime
from database import get_user, add_user, verify_password

SECRET = "mysecretkey"

def create_token(user):
    return jwt.encode({
        "user": user,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }, SECRET, algorithm="HS256")

def login():

    st.markdown("""
    <style>

    /* 🚨 HARD RESET */
    .block-container {
        padding: 0 !important;
        margin: 0 auto !important;
        max-width: 850px;
    }

    header, footer {visibility:hidden;}

    /* 🚨 REMOVE ALL STREAMLIT GAPS */
    div[data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }

    div[data-testid="stVerticalBlock"] > div {
        margin: 0 !important;
        padding: 0 !important;
    }

    /* 🚨 REMOVE EMPTY/USELESS BLOCKS */
    div:empty {
        display: none !important;
    }

    /* 🚨 FORCE COLLAPSE ALL SPACE */
    section.main > div {
        padding-top: 0 !important;
    }

    /* BACKGROUND */
    .stApp {
        background: radial-gradient(circle at top, #1e293b, #020617);
        color: white;
    }

    /* HEADER */
    .header {
        text-align:center;
        margin-bottom: 10px;
    }

    .title {
        font-size:28px;
        font-weight:600;
    }

    .subtitle {
        font-size:13px;
        color:#94a3b8;
    }

    /* INFO BAR */
    .info-bar {
        max-width:600px;
        margin: 5px auto 10px auto;
        padding:10px;
        border-radius:999px;
        text-align:center;
        font-size:13px;

        background: rgba(255,255,255,0.06);
        backdrop-filter: blur(12px);
        border:1px solid rgba(255,255,255,0.08);
    }

    /* CARD */
    .card {
        margin-top: 0 !important;
        padding:28px;
        border-radius:18px;

        background: rgba(255,255,255,0.06);
        backdrop-filter: blur(18px);

        border:1px solid rgba(255,255,255,0.08);
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }

    /* INPUT */
    .stTextInput input {
        border-radius:10px;
        background: rgba(0,0,0,0.5);
        border:1px solid rgba(255,255,255,0.1);
        color:white;
    }

    /* BUTTON */
    .stButton>button {
        width:100%;
        border-radius:10px;
        background: linear-gradient(90deg,#3b82f6,#60a5fa);
        color:white;
    }

    .stRadio > div {
        justify-content:center;
    }

    </style>
    """, unsafe_allow_html=True)

    # HEADER
    st.markdown("""
    <div class='header'>
        <div class='title'>💳 AI Credit Risk System</div>
        <div class='subtitle'>AI-powered credit intelligence platform</div>
    </div>
    """, unsafe_allow_html=True)

    # INFO BAR (ONLY ONE)
    st.markdown("""
    <div class='info-bar'>
        🚀 Smart Analysis • 🔒 Secure Access • 📊 Real-time Insights • 🤖 AI Engine
    </div>
    """, unsafe_allow_html=True)

    # 🚨 HARD FIX: NO EXTRA CONTAINERS USED

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("Sign in")

    mode = st.radio("", ["Login","Sign Up"], horizontal=True)

    # LOGIN
    if mode == "Login":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Continue"):
            user = get_user(email)

            if user and verify_password(password, user[2]):
                st.session_state.logged_in = True
                st.session_state.user = email
                st.session_state.role = user[3]
                st.session_state.token = create_token(email)
                st.success("Welcome 🚀")
                st.rerun()
            else:
                st.error("Invalid credentials")

    # SIGNUP
    else:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["Admin","Manager","Analyst"])

        if st.button("Create account"):
            if add_user(email, password, role):
                st.success("Account created 🎉")
            else:
                st.warning("User already exists")

    st.markdown("</div>", unsafe_allow_html=True)