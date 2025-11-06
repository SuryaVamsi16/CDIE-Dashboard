import streamlit as st
from auth_utils import login_panel
from admin_utils import admin_panel
from data_utils import upload_and_merge_datasets
from metadata_utils import show_metadata
from model_utils import run_models
from viz_utils import show_all_visualizations

def main():
    st.set_page_config(page_title="CDIE Dashboard", layout="wide")
    tabs = st.tabs(["Dashboard", "Admin"])

    with tabs[0]:
        if login_panel():
            st.header("Upload All Required Datasets")
            emp = st.file_uploader("Employee Data", type="csv")
            health = st.file_uploader("Health Data", type="csv")
            savings = st.file_uploader("Savings Data", type="csv")
            edu = st.file_uploader("Education Data", type="csv")

            if emp and health and savings and edu:
                df = upload_and_merge_datasets(emp, health, savings, edu)
                if st.button("▶️ Run Dashboard"):
                    show_metadata(df)
                    run_models(df)
                    show_all_visualizations(df)
            else:
                st.warning("Please upload all four datasets to proceed.")

    with tabs[1]:
        admin_panel()

if __name__ == "__main__":
    main()
