import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def show_comparison_bar(df, emp_df, feature, title):
    st.subheader(title)
    fig, ax = plt.subplots()

    overall_avg = df[feature].mean()
    emp_value = emp_df[feature].iloc[0]

    comparison = pd.DataFrame({
        "Group": ["Selected Employee", "All Employees"],
        feature: [emp_value, overall_avg]
    })

    sns.barplot(data=comparison, x="Group", y=feature, palette=["orange", "steelblue"], ax=ax)
    ax.set_title(f"{feature} Comparison")
    st.pyplot(fig)

def show_category_vs_outcome(df, outcome_col):
    st.subheader(f"{outcome_col} by Category")

    # Identify categorical columns
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns
    categorical_cols = [col for col in categorical_cols if col.upper() != "EMP_ID"]

    for cat_col in categorical_cols:
        if outcome_col in df.columns and cat_col in df.columns:
            grouped = df.groupby(cat_col)[outcome_col].mean().reset_index()
            fig, ax = plt.subplots()
            sns.barplot(data=grouped, x=cat_col, y=outcome_col, ax=ax, palette="viridis")
            ax.set_title(f"{outcome_col} by {cat_col}")
            ax.set_ylabel(f"Average {outcome_col}")
            ax.set_xlabel(cat_col)
            plt.xticks(rotation=45)
            st.pyplot(fig)

def show_all_visualizations(df):
    st.title("Employee vs Overall Comparison")

    df.columns = df.columns.str.upper()

    emp_ids = df["EMP_ID"].dropna().unique()
    selected_emp_id = st.selectbox("Select EMP_ID", emp_ids)

    emp_df = df[df["EMP_ID"] == selected_emp_id]

    numeric_features = [
        "SALARY", "SPOUSE_SALARY", "OTHER_INCOME", "COMBINED_SALARY",
        "HOSPITAL_BILL_AMOUNT", "SCHOOL_FEE", "INSURANCE_AMOUNT",
        "MONTHLY_EXPENSES"
    ]

    for feature in numeric_features:
        if feature in df.columns:
            show_comparison_bar(df, emp_df, feature, f"{feature} vs Overall")

    # Binary comparisons
    if "CAN_PAY" in df.columns:
        show_comparison_bar(df, emp_df, "CAN_PAY", "Hospital Bill Payment Ability")
        show_category_vs_outcome(df, "CAN_PAY")

    if "CHILD_DROPOUT_RISK" in df.columns:
        show_comparison_bar(df, emp_df, "CHILD_DROPOUT_RISK", "Child Dropout Risk")
        show_category_vs_outcome(df, "CHILD_DROPOUT_RISK")
