import pandas as pd
from io import BytesIO

def safe_read_csv(file_buffer, label):
    print(f"\n🔍 Checking {label} file...")

    try:
        df = pd.read_csv(file_buffer, header=0)

        if df.empty or df.columns.size == 0:
            raise ValueError(f"{label} file was read but contains no data or columns.")

        print(f"✅ {label} file read successfully. Shape: {df.shape}")
        print(f"📊 {label} columns: {list(df.columns)}")
        return df

    except Exception as e:
        print(f"❌ Error reading {label} file: {e}")
        raise ValueError(f"{label} file could not be read: {e}")

def upload_and_merge_datasets(emp_bytes, health_bytes, savings_bytes, edu_bytes):
    from io import BytesIO

    try:
        emp_df = safe_read_csv(BytesIO(emp_bytes), "Employee")
        health_df = safe_read_csv(BytesIO(health_bytes), "Health")
        savings_df = safe_read_csv(BytesIO(savings_bytes), "Savings")
        edu_df = safe_read_csv(BytesIO(edu_bytes), "Education")

        print("🔍 Column names before merge:")
        print("Employee:", emp_df.columns.tolist())
        print("Health:", health_df.columns.tolist())
        print("Savings:", savings_df.columns.tolist())
        print("Education:", edu_df.columns.tolist())

        merged_df = emp_df.merge(health_df, on="EMP_id", how="left")
        merged_df = merged_df.merge(savings_df, on="EMP_id", how="left")
        merged_df = merged_df.merge(edu_df, on="EMP_id", how="left")

        return merged_df

    except Exception as e:
        raise ValueError(f"Error merging datasets: {e}")
