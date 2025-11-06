import streamlit as st
import pandas as pd
from io import BytesIO

from auth_utils import login_panel
from admin_utils import admin_panel
from data_utils import upload_and_merge_datasets, safe_read_csv
from metadata_utils import show_metadata
from model_utils import run_models
from viz_utils_1 import show_all_visualizations

def debug_file_upload(label, key):
    uploaded_file = st.file_uploader(f"Upload {label} Data", type="csv", key=f"{key}_uploader")
    if uploaded_file:
        file_bytes = uploaded_file.read()  # ✅ Convert to bytes
        st.session_state[key] = file_bytes  # ✅ Store raw bytes

        st.write(f"📥 {label} file uploaded: `{uploaded_file.name}`")

        try:
            raw_text = file_bytes.decode("utf-8", errors="ignore")
            st.text_area(f"📄 Raw {label} File Preview", raw_text[:1000], height=200)

            df = safe_read_csv(BytesIO(file_bytes), label)
            st.subheader(f"✅ Parsed {label} Data Preview")
            st.dataframe(df.head())
            st.success(f"{label} file loaded successfully. Shape: {df.shape}")
        except Exception as e:
            st.error(f"❌ Error reading {label} file: {e}")

def main():
    st.set_page_config(page_title="CDIE Dashboard", layout="wide")

    # Initialize login state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "role" not in st.session_state:
        st.session_state.role = None

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

        # Initialize session keys
        for key in list(dataset_keys.keys()) + ["merged_df", "dashboard_ready"]:
            if key not in st.session_state:
                st.session_state[key] = None

        # Upload and preview each file
        for key, label in dataset_keys.items():
            debug_file_upload(label, key)

        st.subheader("📦 Upload Status")
        for key, label in dataset_keys.items():
            if st.session_state[key] is not None:
                st.success(f"✅ {label} uploaded")
            else:
                st.warning(f"⏳ {label} not uploaded")

        # Merge datasets
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
                    st.error(f"❌ Error during merge: {e}")

            if st.session_state.merged_df is not None:
                st.subheader("✅ Merged Data Preview")
                st.dataframe(st.session_state.merged_df.head())
                st.session_state.dashboard_ready = True

        # Show metadata, models, and visualizations
        if st.session_state.dashboard_ready and st.session_state.merged_df is not None:
            show_metadata(st.session_state.merged_df)
            run_models(st.session_state.merged_df)
            show_all_visualizations(st.session_state.merged_df)

    elif selected_tab == "Admin":
        admin_panel()

if __name__ == "__main__":
    main()
