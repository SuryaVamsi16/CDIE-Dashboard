import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def show_grouped_bar(df, num_var, cat_var):
    st.subheader(f"Average {num_var} by {cat_var}")
    fig, ax = plt.subplots()
    grouped = df.groupby(cat_var)[num_var].mean().sort_values()
    grouped.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_ylabel(f"Average {num_var}")
    ax.set_xlabel(cat_var)
    ax.set_title(f"{num_var} by {cat_var}")
    plt.xticks(rotation=45)
    st.pyplot(fig)

def show_histogram(df, num_var):
    st.subheader(f"Distribution of {num_var}")
    fig, ax = plt.subplots()
    sns.histplot(df[num_var].dropna(), kde=True, bins=30, ax=ax, color='salmon')
    ax.set_xlabel(num_var)
    ax.set_title(f"Distribution of {num_var}")
    st.pyplot(fig)

def show_all_visualizations(df):
    numeric_features = [
        "CHILD_DROPOUT_RISK","CAN_PAY_HOSPITAL_BILL"]
    categorical_groups = [
        "AGE_GROUP", "GENDER", "REGION", "TREATMENT_TYPE", "STATE", "CITY",
        "DEPARTMENT", "PROFESSION", "CHILD_EDUCATION_TYPE", "PARENT_EDUCATION"
    ]

    for num in numeric_features:
        if num in df.columns:
            show_histogram(df, num)
            for cat in categorical_groups:
                if cat in df.columns:
                    show_grouped_bar(df, num, cat)



