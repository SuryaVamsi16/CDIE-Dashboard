import streamlit as st
import pandas as pd

def login_panel():
    st.title("CDIE Dashboard Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            users_df = pd.read_csv("users.csv")
            user = users_df[(users_df["username"] == username) & (users_df["password"] == password)]
            if not user.empty:
                role = user.iloc[0]["role"]
                st.session_state.logged_in = True
                st.session_state.role = role
                st.success(f"Welcome, {username}!")
                return True, role
            else:
                st.error("Invalid username or password.")
        except Exception as e:
            st.error(f"Error reading users.csv: {e}")
    return False, None
