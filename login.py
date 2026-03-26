import streamlit as st
import pandas as pd
import hashlib
import os

FILE = "users.csv"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists(FILE):
        return pd.read_csv(FILE)
    else:
        return pd.DataFrame(columns=["username","password","role"])

def save_user(username, password, role):
    df = load_users()
    hashed = hash_password(password)

    new_user = pd.DataFrame([[username, hashed, role]],
                            columns=["username","password","role"])

    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(FILE, index=False)

def login():

    menu = ["Login", "Sign Up"]
    choice = st.selectbox("Select Option", menu)

    df = load_users()

    if choice == "Login":

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            hashed = hash_password(password)

            user = df[(df["username"] == username) &
                      (df["password"] == hashed)]

            if not user.empty:
                st.session_state["logged_in"] = True
                st.session_state["user"] = username
                st.session_state["role"] = user.iloc[0]["role"]
            else:
                st.error("Invalid credentials")

    elif choice == "Sign Up":

        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["Admin","Manager","Analyst"])

        if st.button("Sign Up"):

            if new_user in df["username"].values:
                st.warning("User exists")
            else:
                save_user(new_user, new_pass, role)
                st.success("Account created")