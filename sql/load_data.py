import sqlite3
import pandas as pd

DB_PATH = 'sql/job_market.db'
SCHEMA_PATH = 'sql/schema.sql'

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

with open(SCHEMA_PATH, 'r') as f:
    cursor.executescript(f.read())

df_jobs = pd.read_csv('data/processed/jobs_tagged.csv')
df_skills = pd.read_csv('data/processed/skills_dim.csv')
df_bridge = pd.read_csv('data/processed/job_skills_bridge.csv')

# Populate Company Dimension
companies = df_jobs[['Company']].drop_duplicates().dropna()
companies.columns = ['Company_Name']
companies.to_sql('Company', conn, if_exists='append', index=False)

company_map = pd.read_sql('SELECT Company_ID, Company_Name FROM Company', conn)
df_jobs = df_jobs.merge(company_map, left_on='Company', right_on='Company_Name', how='left')

# Populate Location Dimension
locations = df_jobs[['City', 'State_Region', 'Country']].drop_duplicates().dropna()
locations.to_sql('Location', conn, if_exists='append', index=False)

location_map = pd.read_sql('SELECT Location_ID, City, State_Region, Country FROM Location', conn)
df_jobs = df_jobs.merge(location_map, on=['City', 'State_Region', 'Country'], how='left')

# Populate Skills Dimension
df_skills.to_sql('Skills', conn, if_exists='append', index=False)

# Populate Jobs Table
jobs_table = df_jobs[[
    'Job_ID', 'Job_Title', 'Company_ID', 'Location_ID', 'Job_Type', 
    'Experience_Requirement', 'Posted_Date', 'Job_URL', 'Source', 
    'Scraped_Date', 'Job_Description'
]].rename(columns={'Experience_Requirement': 'Experience'})

jobs_table.to_sql('Jobs', conn, if_exists='append', index=False)

# Populate Job_Skills Bridge Table
df_bridge.to_sql('Job_Skills', conn, if_exists='append', index=False)

conn.commit()

print("=" * 50)
print("PHASE 7: SQL DATABASE CREATION & VERIFICATION")
print("=" * 50)
for table in ['Company', 'Location', 'Skills', 'Jobs', 'Job_Skills']:
    cnt = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"Table '{table}': {cnt} records")

conn.close()
