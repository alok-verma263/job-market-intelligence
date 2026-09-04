import pandas as pd

# Load the raw dataset
df = pd.read_csv('../data/raw/jobs_raw.csv')

print("=" * 50)
print("PHASE 4: RAW DATA PROFILING")
print("=" * 50)

# 1. Dimensions
print(f"Total Rows: {df.shape[0]}")
print(f"Total Columns: {df.shape[1]}\n")

# 2. Schema and Non-Null Counts
print("--- Column Summary & Data Types ---")
df.info()

# 3. Missing Value Audit
print("\n--- Missing Values Count per Field ---")
null_counts = df.isnull().sum()
null_percent = (null_counts / len(df)) * 100
missing_df = pd.DataFrame(
    {'Missing Count': null_counts, 'Percent Missing (%)': null_percent.round(2)})
print(missing_df)

# 4. Duplicate Check
duplicate_ids = df['Job_ID'].duplicated().sum()
duplicate_rows = df.duplicated().sum()
print(f"\nExact Duplicate Rows: {duplicate_rows}")
print(f"Duplicate Job_IDs: {duplicate_ids}")

# 5. Categorical Check
print("\n--- Top Locations ---")
print(df['Location'].value_counts().head(5))

print("\n--- Sample Job Titles ---")
print(df['Job_Title'].value_counts().head(5))
