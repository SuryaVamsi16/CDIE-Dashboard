import streamlit as st

def show_metadata(df):
    st.subheader("Metadata Summary")
    st.write("Columns:", df.columns.tolist())
    st.write("Shape:", df.shape)
    st.dataframe(df.head())
