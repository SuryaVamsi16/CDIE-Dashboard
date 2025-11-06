import streamlit as st
import pandas as pd
import os

def admin_panel():
    st.header("🔐 Admin Access Manager")

    # Load access requests
    if os.path.exists("access_requests.csv"):
        requests = pd.read_csv("access_requests.csv")
        pending = requests[requests["status"] == "pending"]
        if pending.empty:
            st.info("No pending access requests.")
        else:
            st.subheader("Pending Requests")
            for i, row in pending.iterrows():
                with st.expander(f"{row['name']} ({row['email']})"):
                    st.write(f"📧 Email: {row['email']}")
                    st.write(f"📝 Reason: {row['reason']}")
                    st.write(f"📅 Requested On: {row['requested_on']}")
                    username = st.text_input(f"Username for {row['email']}", key=f"user_{i}")
                    password = st.text_input(f"Password for {row['email']}", key=f"pass_{i}")
                    role = st.selectbox("Role", ["user", "admin"], key=f"role_{i}")
                    if st.button(f"✅ Approve {row['email']}", key=f"approve_{i}"):
                        # Add to users.csv
                        new_user = pd.DataFrame([{
                            "username": username,
                            "password": password,
                            "role": role
                        }])
                        if not os.path.exists("users.csv"):
                            new_user.to_csv("users.csv", index=False)
                        else:
                            new_user.to_csv("users.csv", mode="a", header=False, index=False)

                        # Update access_requests.csv
                        requests.at[i, "status"] = "approved"
                        requests.to_csv("access_requests.csv", index=False)
                        st.success(f"{username} has been approved and added to users.csv.")
    else:
        st.warning("No access_requests.csv file found.")
