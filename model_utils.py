import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, f1_score

def encode_categorical_columns(df):
    categorical_cols = [
        "TREATMENT_TYPE", "REGION", "CHILD_EDUCATION_TYPE", "PARENT_EDUCATION",
        "DEPARTMENT", "PROFESSION", "ROLE", "GENDER", "CITY", "STATE"
    ]
    existing = [col for col in categorical_cols if col in df.columns]
    df_encoded = pd.get_dummies(df, columns=existing, drop_first=True)
    return df_encoded

def calculate_combined_salary(row):
    return row["COMBINED_HOUSEHOLD_SALARY"] + row["SAVINGS_AMOUNT"]

def run_models(df):
    df["COMBINED_SALARY"] = df.apply(calculate_combined_salary, axis=1)
    df["CAN_PAY"] = (
        df["COMBINED_SALARY"] + df["INSURANCE_COVERAGE"]
    ) > (
        df["HOSPITAL_BILL"] + df["MONTHLY_EXPENSES"]
    )
    df["CHILD_DROPOUT_RISK"] = (df["TUITION_FEES"] > (
        df["LOAN_AMOUNT_X"] + df["COMBINED_SALARY"] + df["MONTHLY_INCOME"]
    )
)

    df = encode_categorical_columns(df)


    # Hospital model
    hospital_features = [col for col in df.columns if col.startswith("COMBINED_SALARY") or
                         col.startswith("HOSPITAL_BILL") or
                         col.startswith("TREATMENT_TYPE_") or
                         col.startswith("REGION_")]
    X_hospital = df[hospital_features]
    y_hospital = df["CAN_PAY"]

    hospital_imputer = SimpleImputer(strategy="mean")
    X_hospital_imputed = hospital_imputer.fit_transform(X_hospital)

    hospital_scaler = StandardScaler()
    X_hospital_scaled = hospital_scaler.fit_transform(X_hospital_imputed)

    hospital_model = RandomForestClassifier(n_estimators=100, random_state=42)
    hospital_model.fit(X_hospital_scaled, y_hospital)

    # Dropout model
    dropout_features = [col for col in df.columns if col.startswith("COMBINED_SALARY") or
                        col.startswith("TUITION_FEES") or
                        col.startswith("CHILD_EDUCATION_TYPE_") or
                        col.startswith("PARENT_EDUCATION_") or
                        col.startswith("REGION_")]
    X_dropout = df[dropout_features]
    y_dropout = df["CHILD_DROPOUT_RISK"]

    dropout_imputer = SimpleImputer(strategy="mean")
    X_dropout_imputed = dropout_imputer.fit_transform(X_dropout)

    dropout_scaler = StandardScaler()
    X_dropout_scaled = dropout_scaler.fit_transform(X_dropout_imputed)

    dropout_model = RandomForestClassifier(n_estimators=100, random_state=42)
    dropout_model.fit(X_dropout_scaled, y_dropout)

    metrics = {
        "HOSPITAL_F1": f1_score(y_hospital, hospital_model.predict(X_hospital_scaled)),
        "DROPOUT_F1": f1_score(y_dropout, dropout_model.predict(X_dropout_scaled)),
        "HOSPITAL_ACCURACY": accuracy_score(y_hospital, hospital_model.predict(X_hospital_scaled)),
        "DROPOUT_ACCURACY": accuracy_score(y_dropout, dropout_model.predict(X_dropout_scaled)),
        "HOSPITAL_MODEL_USED": "Random Forest",
        "DROPOUT_MODEL_USED": "Random Forest"
    }

    return hospital_model, hospital_scaler, hospital_imputer, dropout_model, dropout_scaler, dropout_imputer, df, metrics

def predict_cross_domain(emp_id, df, hospital_model, hospital_scaler, hospital_imputer,
                          dropout_model, dropout_scaler, dropout_imputer):
    row = df[df["EMP_ID"] == emp_id].iloc[0]

    hospital_input = pd.DataFrame([{
        "COMBINED_SALARY": row["COMBINED_SALARY"],
        "HOSPITAL_BILL": row["HOSPITAL_BILL"],
        **{col: row[col] for col in df.columns if col.startswith("TREATMENT_TYPE_")},
        **{col: row[col] for col in df.columns if col.startswith("REGION_")}
    }])
    hospital_imputed = hospital_imputer.transform(hospital_input)
    hospital_scaled = hospital_scaler.transform(hospital_imputed)
    can_pay = hospital_model.predict(hospital_scaled)[0]

    dropout_input = pd.DataFrame([{
        "COMBINED_SALARY": row["COMBINED_SALARY"],
        "TUITION_FEES": row["TUITION_FEES"],
        **{col: row[col] for col in df.columns if col.startswith("CHILD_EDUCATION_TYPE_")},
        **{col: row[col] for col in df.columns if col.startswith("PARENT_EDUCATION_")},
        **{col: row[col] for col in df.columns if col.startswith("REGION_")}
    }])
    dropout_imputed = dropout_imputer.transform(dropout_input)
    dropout_scaled = dropout_scaler.transform(dropout_imputed)
    dropout_risk = dropout_model.predict(dropout_scaled)[0]

    return {
        "EMP_ID": row["EMP_ID"],
        "CAN_PAY_HOSPITAL_BILL": bool(can_pay),
        "CHILD_DROPOUT_RISK": bool(dropout_risk),
        "COMBINED_SALARY": row["COMBINED_SALARY"],
        "HOSPITAL_BILL": row["HOSPITAL_BILL"],
        "TUITION_FEES": row["TUITION_FEES"],
        "INSURANCE_AMOUNT": row["INSURANCE_AMOUNT"],
        "MONTHLY_EXPENSES": row["MONTHLY_EXPENSES"],
        "DEPARTMENT": row.get("DEPARTMENT", None),
        "PROFESSION": row.get("PROFESSION", None),
        "ROLE": row.get("ROLE", None),
        "AGE": row.get("AGE", None),
        "GENDER": row.get("GENDER", None),
        "CITY": row.get("CITY", None),
        "STATE": row.get("STATE", None),
        "REGION": row.get("REGION", None)
    }



