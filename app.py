import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import openai

from model_utils import predict
from report_generator import generate_report, generate_full_report
from login import login

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Credit Risk System", layout="wide")

# ---------------- PREMIUM UI ----------------
st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: white;
}
h1, h2, h3 {
    color: #00C9A7;
}
.stButton>button {
    border-radius: 10px;
    background-color: #00C9A7;
    color: white;
    font-weight: bold;
}
.stMetric {
    background-color: #1c1f26;
    padding: 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- OPENAI ----------------
openai.api_key = "YOUR_API_KEY"   # 🔑 Replace

def real_llm(user_input, age, income, loan, credit, prob):

    prompt = f"""
    You are a financial AI expert.

    If user greets (hi/hello), respond politely.

    If user asks about borrower:
    - Explain risk clearly
    - Give 2–3 reasons
    - Give recommendation (approve/reject)

    Borrower Details:
    Age: {age}
    Income: {income}
    Loan: {loan}
    Credit Score: {credit}
    Default Probability: {prob}

    User Question:
    {user_input}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['choices'][0]['message']['content']


# ---------------- LOGIN ----------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

# ---------------- HEADER ----------------
st.title("💳 AI Credit Risk Prediction System")

st.markdown("""
### 🔍 Intelligent Credit Risk Assessment Platform  
AI-powered system for real-time borrower evaluation and decision support.
""")

st.write(f"👤 {st.session_state['user']} | Role: {st.session_state['role']}")

if st.button("Logout"):
    st.session_state["logged_in"] = False
    st.rerun()

st.divider()

# ---------------- INPUT ----------------
st.subheader("📥 Enter Borrower Details")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", value=30)
    income = st.number_input("Income", value=30000)

with col2:
    loan = st.number_input("Loan Amount", value=10000)
    credit = st.number_input("Credit Score", value=650)

st.divider()

# ---------------- PREDICT ----------------
if st.button("🚀 Predict Risk"):

    result, prob = predict([age, income, loan, credit])
    label = "High Risk" if result == 1 else "Low Risk"

    st.markdown("## 📊 Prediction Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Probability", round(prob, 2))

    with col2:
        st.metric("Risk Level", label)

    with col3:
        st.metric("Credit Score", credit)

    if result == 1:
        st.error("⚠ High Risk Borrower")
    else:
        st.success("✅ Safe Borrower")

    # SAVE HISTORY
    new = pd.DataFrame([[age, income, loan, credit, prob, label, st.session_state["user"]]],
                       columns=["age","income","loan","credit","probability","result","user"])

    if os.path.exists("history.csv"):
        df = pd.read_csv("history.csv")
        df = pd.concat([df, new], ignore_index=True)
    else:
        df = new

    df.to_csv("history.csv", index=False)

    # ---------------- GAUGE ----------------
    st.subheader("📈 Risk Gauge")

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob * 100,
        title={'text': "Risk %"}
    ))

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ---------------- LLM ----------------
    st.subheader("🤖 AI Assistant (LLM Powered)")

    user_input = st.text_input("Ask AI (e.g., 'hi', 'Is this risky?')")

    if st.button("Ask AI"):

        if user_input.strip() == "":
            st.warning("Please enter a question")
        else:
            answer = real_llm(user_input, age, income, loan, credit, prob)
            st.write(answer)

    st.divider()

    # ---------------- REPORT ----------------
    generate_report(label, prob)

    with open("report.pdf", "rb") as f:
        st.download_button("📄 Download Report", f)

# ---------------- BULK ----------------
st.subheader("📂 Bulk Loan Prediction (Upload Multiple Customers)")

file = st.file_uploader("Upload CSV")

if file:
    df = pd.read_csv(file)
    probs = []

    for _, r in df.iterrows():
        _, p = predict([r["age"], r["income"], r["loan"], r["credit"]])
        probs.append(p)

    df["Prediction"] = probs
    st.dataframe(df)

st.divider()

# ---------------- ANALYTICS ----------------
st.subheader("📊 System Analytics Dashboard")

try:
    df = pd.read_csv("history.csv")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Predictions", len(df))

    with col2:
        st.metric("Average Risk", round(df["probability"].mean(), 2))

    st.bar_chart(df["result"].value_counts())
    st.line_chart(df["probability"])

    st.dataframe(df)

except:
    st.info("No data available yet")

# ---------------- ADMIN ----------------
if st.session_state["role"] == "Admin":

    st.divider()
    st.subheader("👑 Admin Panel")

    users = pd.read_csv("users.csv")
    st.dataframe(users)

    u = st.selectbox("Delete user", users["username"])

    if st.button("Delete User"):
        users = users[users["username"] != u]
        users.to_csv("users.csv", index=False)
        st.success("User deleted")

# ---------------- FULL REPORT ----------------
if st.button("📄 Generate Full Report"):
    generate_full_report()

    with open("full_report.pdf", "rb") as f:
        st.download_button("Download Full Report", f)