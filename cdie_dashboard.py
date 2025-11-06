import streamlit as st
from auth_utils import login_panel
from data_utils import upload_and_merge_datasets
from metadata_utils import show_metadata
from model_utils import run_models
from viz_utils import show_all_visualizations

def main():
    st.set_page_config(page_title="CDIE Dashboard", layout="wide")
    if login_panel():
        df = upload_and_merge_datasets()
        if df is not None:
            show_metadata(df)
            run_models(df)
            show_all_visualizations(df)

if __name__ == "__main__":
    main()
