import pandas as pd
import re


def clean_location(loc_str):
    """Splits raw location strings into structured City, State, Country."""
    if not isinstance(loc_str, str) or loc_str.strip() == "":
        return "Unknown", "Unknown", "India"

    parts = [p.strip() for p in loc_str.split(",")]
    if len(parts) >= 2:
        city = parts[0]
        state = parts[1]
        country = parts[2] if len(parts) > 2 else "India"
    elif len(parts) == 1:
        if parts[0].lower() == "india":
            city, state, country = "Remote / Nationwide", "Pan-India", "India"
        else:
            city, state, country = parts[0], "Unknown", "India"
    else:
        city, state, country = "Unknown", "Unknown", "India"

    return city, state, country


def clean_data():
    raw_path = '../data/raw/jobs_raw.csv'
    clean_path = '../data/processed/jobs_cleaned.csv'

    df = pd.read_csv(raw_path)
    initial_rows = len(df)

    # 1. Deduplicate by Job_ID
    df = df.drop_duplicates(subset=['Job_ID']).copy()
    deduped_rows = len(df)

    # 2. Impute Missing Companies
    df['Company'] = df['Company'].fillna('Not Specified').str.strip()

    # 3. Standardize Dates (ISO Format YYYY-MM-DD)
    df['Posted_Date'] = pd.to_datetime(
        df['Posted_Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    df['Posted_Date'] = df['Posted_Date'].fillna(df['Scraped_Date'])

    # 4. Standardize Job Type
    df['Job_Type'] = df['Job_Type'].replace({
        'permanent': 'Full-Time',
        'contract': 'Contract',
        'Unknown': 'Not Specified'
    }).fillna('Not Specified')

    # 5. Extract Structured Location Details
    loc_splits = df['Location'].apply(clean_location)
    df['City'] = [x[0] for x in loc_splits]
    df['State_Region'] = [x[1] for x in loc_splits]
    df['Country'] = [x[2] for x in loc_splits]

    # 6. Basic Description Normalization (collapse redundant whitespaces)
    df['Job_Description'] = df['Job_Description'].fillna('').astype(str)
    df['Job_Description'] = df['Job_Description'].apply(
        lambda x: re.sub(r'\s+', ' ', x).strip())

    # Save cleaned dataset
    df.to_csv(clean_path, index=False)

    print("=" * 50)
    print("PHASE 5: CLEANING COMPLETE")
    print("=" * 50)
    print(f"Initial Rows:       {initial_rows}")
    print(f"Duplicates Removed: {initial_rows - deduped_rows}")
    print(f"Final Cleaned Rows: {len(df)}")
    print(f"Cleaned output:     {clean_path}\n")


if __name__ == '__main__':
    clean_data()
