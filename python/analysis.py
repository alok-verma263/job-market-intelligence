import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs('screenshots', exist_ok=True)
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.sans-serif': 'DejaVu Sans', 'font.size': 10})

conn = sqlite3.connect('sql/job_market.db')

# 1. Top Demanded Skills Overall
query_skills = """
    SELECT s.Skill_Name, COUNT(js.Job_ID) AS Demand_Count
    FROM Skills s
    JOIN Job_Skills js ON s.Skill_ID = js.Skill_ID
    GROUP BY s.Skill_Name
    ORDER BY Demand_Count DESC
    LIMIT 10;
"""
df_skills = pd.read_sql(query_skills, conn)

plt.figure(figsize=(10, 5))
bar1 = sns.barplot(data=df_skills, x='Demand_Count', y='Skill_Name', palette='Blues_r')
plt.title('Top 10 Most Demanded Skills in Analytics Roles', fontsize=13, weight='bold', pad=15)
plt.xlabel('Number of Job Postings', fontsize=11)
plt.ylabel('Skill', fontsize=11)
for p in bar1.patches:
    bar1.annotate(f"{int(p.get_width())}", 
                  (p.get_width() - 3, p.get_y() + p.get_height() / 2.), 
                  ha='center', va='center', color='white', weight='bold')
plt.tight_layout()
plt.savefig('screenshots/eda_top_skills.png', dpi=300)
plt.close()

# 2. Skill Comparison: Business Analyst vs Data Analyst
query_comparison = """
    WITH Roles AS (
        SELECT Job_ID,
               CASE WHEN LOWER(Job_Title) LIKE '%business analyst%' THEN 'Business Analyst'
                    WHEN LOWER(Job_Title) LIKE '%data analyst%' THEN 'Data Analyst'
                    ELSE 'Other' END AS Target_Role
        FROM Jobs
    )
    SELECT s.Skill_Name,
           SUM(CASE WHEN r.Target_Role = 'Business Analyst' THEN 1 ELSE 0 END) AS BA,
           SUM(CASE WHEN r.Target_Role = 'Data Analyst' THEN 1 ELSE 0 END) AS DA
    FROM Skills s
    JOIN Job_Skills js ON s.Skill_ID = js.Skill_ID
    JOIN Roles r ON js.Job_ID = r.Job_ID
    WHERE r.Target_Role IN ('Business Analyst', 'Data Analyst')
    GROUP BY s.Skill_Name
    ORDER BY (BA + DA) DESC
    LIMIT 8;
"""
df_comp = pd.read_sql(query_comparison, conn)
df_comp_melted = df_comp.melt(id_vars=['Skill_Name'], value_vars=['BA', 'DA'], 
                              var_name='Role', value_name='Demand_Count')

plt.figure(figsize=(10, 5))
sns.barplot(data=df_comp_melted, x='Skill_Name', y='Demand_Count', hue='Role', palette=['#1f77b4', '#ff7f0e'])
plt.title('Skill Demand Divergence: Business Analyst vs Data Analyst', fontsize=13, weight='bold', pad=15)
plt.xlabel('Skill', fontsize=11)
plt.ylabel('Frequency in Job Listings', fontsize=11)
plt.xticks(rotation=30, ha='right')
plt.legend(title='Target Role')
plt.tight_layout()
plt.savefig('screenshots/eda_role_comparison.png', dpi=300)
plt.close()

# 3. Geographic Hubs (excluding remote)
query_locations = """
    SELECT City, COUNT(Job_ID) AS Total_Jobs
    FROM Location l
    JOIN Jobs j ON l.Location_ID = j.Location_ID
    WHERE City NOT LIKE '%Remote%'
    GROUP BY City
    ORDER BY Total_Jobs DESC
    LIMIT 6;
"""
df_loc = pd.read_sql(query_locations, conn)

plt.figure(figsize=(8, 4.5))
bar3 = sns.barplot(data=df_loc, x='Total_Jobs', y='City', palette='crest_r')
plt.title('Top Tech Hubs by Job Availability', fontsize=13, weight='bold', pad=15)
plt.xlabel('Open Positions', fontsize=11)
plt.ylabel('Metro Location', fontsize=11)
for p in bar3.patches:
    bar3.annotate(f"{int(p.get_width())}", 
                  (p.get_width() - 2, p.get_y() + p.get_height() / 2.), 
                  ha='center', va='center', color='white', weight='bold')
plt.tight_layout()
plt.savefig('screenshots/eda_location_distribution.png', dpi=300)
plt.close()

conn.close()
print("=" * 50)
print("PHASE 9: EDA CHARTS GENERATED")
print("=" * 50)
print("Generated images in screenshots/:")
print("- eda_top_skills.png")
print("- eda_role_comparison.png")
print("- eda_location_distribution.png")
