# Login once per session
if not st.session_state.logged_in:
    st.title("Welcome to CDIE Dashboard")
    st.subheader("Login")

    logged_in, role = login_panel()
    if logged_in:
        st.session_state.logged_in = True
        st.session_state.role = role
        st.rerun()
    else:
        st.markdown("---")
        st.subheader("Request Access")
        with st.form("access_request_form"):
            full_name = st.text_input("Full Name")
            access_email = st.text_input("Email Address")
            department = st.text_input("Department or Role")
            access_type = st.selectbox("Type of Access", ["View Only", "Edit", "Admin", "Custom"])
            reason = st.text_area("Reason for Access")

            access_submitted = st.form_submit_button("Submit Access Request")
            if access_submitted:
                if full_name and access_email and reason:
                    st.success("Your access request has been submitted.")
                else:
                    st.warning("Please fill out all required fields.")
        st.stop()
