import streamlit as st
import pandas as pd
from io import BytesIO

from auth_utils import login_panel
from admin_utils import admin_panel
from data_utils import upload_and_merge_datasets, safe_read_csv
from metadata_utils import show_metadata
from model_utils import run_models
from viz_utils import show_all_visualizations

def main():
    st.set_page_config(page_title="CDIE Dashboard", layout="wide")

    # Initialize login state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "role" not in st.session_state:
        st.session_state.role = None

    # Logout button
    if st.session_state.logged_in:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.role = None
            for key in list(st.session_state.keys()):
                if key not in ["logged_in", "role"]:
                    del st.session_state[key]
            st.rerun()

    # Login once per session
    if not st.session_state.logged_in:
        logged_in, role = login_panel()
        if logged_in:
            st.session_state.logged_in = True
            st.session_state.role = role
        else:
            st.stop()

    # Tabs
    tabs = ["Dashboard"]
    if st.session_state.role == "admin":
        tabs.append("Admin")
    selected_tab = st.selectbox("Choose a tab", tabs)

    if selected_tab == "Dashboard":
        st.header("Upload All Required Datasets")

        dataset_keys = {
            "emp": "Employee Data",
            "health": "Health Data",
            "savings": "Savings Data",
            "edu": "Education Data"
        }

        for key in list(dataset_keys.keys()) + ["merged_df", "dashboard_ready"]:
            if key not in st.session_state:
                st.session_state[key] = None

        for key, label in dataset_keys.items():
            uploaded_file = st.file_uploader(label, type="csv", key=f"{key}_uploader")
            if uploaded_file:
                file_bytes = uploaded_file.read()
                st.session_state[key] = file_bytes
                st.write(f"{label} file received: {uploaded_file.name}")
                try:
                    df_preview = pd.read_csv(BytesIO(file_bytes))
                    st.subheader(f"{label} Preview")
                    st.dataframe(df_preview.head())
                except Exception as e:
                    st.error(f"Error reading {label}: {e}")

        st.subheader("Upload Status")
        for key, label in dataset_keys.items():
            if st.session_state[key] is not None:
                st.success(f"{label} uploaded")
            else:
                st.warning(f"{label} not uploaded")

        if all([st.session_state[k] is not None for k in dataset_keys]):
            if st.session_state.merged_df is None:
                try:
                    merged_df = upload_and_merge_datasets(
                        st.session_state["emp"],
                        st.session_state["health"],
                        st.session_state["savings"],
                        st.session_state["edu"]
                    )
                    st.session_state.merged_df = merged_df
                except Exception as e:
                    st.error(f"Failed to merge datasets: {e}")

            if st.session_state.merged_df is not None:
                st.subheader("Merged Data Preview")
                st.dataframe(st.session_state.merged_df.head())
                st.session_state.dashboard_ready = True

        if st.session_state.dashboard_ready and st.session_state.merged_df is not None:
            show_metadata(st.session_state.merged_df)
            run_models(st.session_state.merged_df)
            show_all_visualizations(st.session_state.merged_df)

    elif selected_tab == "Admin":
        admin_panel()

if __name__ == "__main__":
    main()
