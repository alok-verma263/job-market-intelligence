import sqlite3
import pandas as pd

DB_PATH = 'sql/job_market.db'
conn = sqlite3.connect(DB_PATH)

queries = {
    "1. Top Demanded Skills": """
        SELECT s.Skill_Name, s.Skill_Category, COUNT(js.Job_ID) AS Demand_Count,
               ROUND(COUNT(js.Job_ID) * 100.0 / (SELECT COUNT(*) FROM Jobs), 2) AS Demand_Pct
        FROM Skills s
        JOIN Job_Skills js ON s.Skill_ID = js.Skill_ID
        GROUP BY s.Skill_ID ORDER BY Demand_Count DESC LIMIT 8;
    """,
    "2. Top Hiring Cities": """
        SELECT l.City, COUNT(j.Job_ID) AS Total_Jobs,
               ROUND(COUNT(j.Job_ID) * 100.0 / (SELECT COUNT(*) FROM Jobs), 2) AS Share_Pct
        FROM Location l
        JOIN Jobs j ON l.Location_ID = j.Location_ID
        GROUP BY l.City ORDER BY Total_Jobs DESC LIMIT 6;
    """,
    "3. Role Skill Contrast (BA vs DA)": """
        WITH Roles AS (
            SELECT Job_ID,
                   CASE WHEN LOWER(Job_Title) LIKE '%business analyst%' THEN 'Business Analyst'
                        WHEN LOWER(Job_Title) LIKE '%data analyst%' THEN 'Data Analyst'
                        ELSE 'Other' END AS Target_Role
            FROM Jobs
        )
        SELECT s.Skill_Name,
               SUM(CASE WHEN r.Target_Role = 'Business Analyst' THEN 1 ELSE 0 END) AS BA_Count,
               SUM(CASE WHEN r.Target_Role = 'Data Analyst' THEN 1 ELSE 0 END) AS DA_Count
        FROM Skills s
        JOIN Job_Skills js ON s.Skill_ID = js.Skill_ID
        JOIN Roles r ON js.Job_ID = r.Job_ID
        WHERE r.Target_Role IN ('Business Analyst', 'Data Analyst')
        GROUP BY s.Skill_Name ORDER BY (BA_Count + DA_Count) DESC LIMIT 8;
    """,
    "4. Top Skill Co-Occurrences": """
        SELECT s1.Skill_Name || ' + ' || s2.Skill_Name AS Skill_Pair, COUNT(*) AS Pair_Count
        FROM Job_Skills js1
        JOIN Job_Skills js2 ON js1.Job_ID = js2.Job_ID AND js1.Skill_ID < js2.Skill_ID
        JOIN Skills s1 ON js1.Skill_ID = s1.Skill_ID
        JOIN Skills s2 ON js2.Skill_ID = s2.Skill_ID
        GROUP BY Skill_Pair ORDER BY Pair_Count DESC LIMIT 5;
    """
}

print("=" * 60)
print("PHASE 8: SQL ANALYSIS QUERY RESULTS")
print("=" * 60)

for title, q in queries.items():
    print(f"\n--- {title} ---")
    df_res = pd.read_sql(q, conn)
    print(df_res.to_string(index=False))

conn.close()
