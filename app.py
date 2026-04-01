import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

from login import login
from database import create_tables, get_history, save_history, get_users

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Credit Risk System", layout="wide")
create_tables()

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()

# ---------------- STYLE ----------------
st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background: radial-gradient(circle at top, #1e293b, #020617);
    color: white;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(10px);
}

/* CARD */
.card {
    padding:20px;
    border-radius:15px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(15px);
    border:1px solid rgba(255,255,255,0.08);
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    margin-bottom:15px;
}

/* BUTTON */
.stButton>button {
    border-radius:10px;
    background: linear-gradient(90deg,#3b82f6,#60a5fa);
    color:white;
}

/* METRIC */
.metric {
    font-size:22px;
    font-weight:600;
}

</style>
""", unsafe_allow_html=True)

# ---------------- MODEL ----------------
model = joblib.load("model.pkl")

def predict(x):
    return model.predict([x])[0], model.predict_proba([x])[0][1]

# ---------------- SIDEBAR ----------------
st.sidebar.title("💳 AI System")
menu = ["Dashboard", "Prediction", "Analytics", "Admin"]
choice = st.sidebar.radio("Navigation", menu)

st.sidebar.write(f"👤 {st.session_state.user}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# ---------------- HEADER ----------------
st.title("💳 AI Credit Risk System")
st.caption("AI-powered credit intelligence platform")

# =========================================================
# 📊 DASHBOARD
# =========================================================
if choice == "Dashboard":

    df = pd.DataFrame(get_history(),
        columns=["id","age","income","loan","credit","prob","result"])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"<div class='card'><div class='metric'>Total</div><h2>{len(df)}</h2></div>", unsafe_allow_html=True)

    with col2:
        avg = round(df["prob"].mean(),2) if not df.empty else 0
        st.markdown(f"<div class='card'><div class='metric'>Avg Risk</div><h2>{avg}</h2></div>", unsafe_allow_html=True)

    with col3:
        rejected = (df["result"]=="Rejected").sum() if not df.empty else 0
        st.markdown(f"<div class='card'><div class='metric'>Rejected</div><h2>{rejected}</h2></div>", unsafe_allow_html=True)

# =========================================================
# 🤖 PREDICTION
# =========================================================
elif choice == "Prediction":

    st.subheader("Loan Risk Prediction")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", value=30)
        income = st.number_input("Income", value=30000)

    with col2:
        loan = st.number_input("Loan Amount", value=10000)
        credit = st.number_input("Credit Score", value=650)

    if st.button("Analyze"):

        _, p = predict([age, income, loan, credit])
        decision = "Approved" if p < 0.3 else "Rejected"

        st.markdown(f"<div class='card'><h3>{decision}</h3><p>Risk: {round(p,2)}</p></div>", unsafe_allow_html=True)

        save_history(age, income, loan, credit, p, decision)

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=p * 100,
            title={'text': "Risk %"}
        ))
        st.plotly_chart(fig, use_container_width=True)

# =========================================================
# 📉 ANALYTICS
# =========================================================
elif choice == "Analytics":

    st.subheader("Analytics")

    df = pd.DataFrame(get_history(),
        columns=["id","age","income","loan","credit","prob","result"])

    if not df.empty:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.bar_chart(df["result"].value_counts())
        st.line_chart(df["prob"])
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No data available")

# =========================================================
# 🔐 ADMIN
# =========================================================
elif choice == "Admin":

    if st.session_state.role != "Admin":
        st.error("Access denied")
    else:
        st.subheader("Admin Panel")

        users = pd.DataFrame(get_users(), columns=["id","username","role"])
        df = pd.DataFrame(get_history(),
            columns=["id","age","income","loan","credit","prob","result"])

        st.markdown("<div class='card'>Users</div>", unsafe_allow_html=True)
        st.dataframe(users)

        st.markdown("<div class='card'>Applications</div>", unsafe_allow_html=True)
        st.dataframe(df)