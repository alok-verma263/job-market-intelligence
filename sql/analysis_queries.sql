-- ====================================================================
-- PHASE 8: BUSINESS INTELLIGENCE & SQL ANALYSIS
-- Database: SQLite (sql/job_market.db)
-- ====================================================================

-- --------------------------------------------------------------------
-- 1. Skill Demand: Top Demanded Skills & Percentage of Jobs Requiring Them
-- Business Question: What skills are most in demand across postings?
-- --------------------------------------------------------------------
SELECT 
    s.Skill_Name,
    s.Skill_Category,
    COUNT(js.Job_ID) AS Demand_Count,
    ROUND(COUNT(js.Job_ID) * 100.0 / (SELECT COUNT(*) FROM Jobs), 2) AS Demand_Percentage
FROM Skills s
JOIN Job_Skills js ON s.Skill_ID = js.Skill_ID
GROUP BY s.Skill_ID, s.Skill_Name, s.Skill_Category
ORDER BY Demand_Count DESC;

-- --------------------------------------------------------------------
-- 2. Location Intelligence: Opportunities by City
-- Business Question: Where are the top geographical hiring hubs?
-- --------------------------------------------------------------------
SELECT 
    l.City,
    l.State_Region,
    COUNT(j.Job_ID) AS Total_Jobs,
    ROUND(COUNT(j.Job_ID) * 100.0 / (SELECT COUNT(*) FROM Jobs), 2) AS Market_Share_Percentage
FROM Location l
JOIN Jobs j ON l.Location_ID = j.Location_ID
GROUP BY l.City, l.State_Region
ORDER BY Total_Jobs DESC
LIMIT 10;

-- --------------------------------------------------------------------
-- 3. Role-Based Skill Comparison: Business Analyst vs Data Analyst
-- Business Question: How do skill demands differ between BA and DA roles?
-- --------------------------------------------------------------------
WITH Categorized_Jobs AS (
    SELECT 
        Job_ID,
        CASE 
            WHEN LOWER(Job_Title) LIKE '%business analyst%' THEN 'Business Analyst'
            WHEN LOWER(Job_Title) LIKE '%data analyst%' THEN 'Data Analyst'
            ELSE 'Other Analytics'
        END AS Target_Role
    FROM Jobs
)
SELECT 
    s.Skill_Name,
    SUM(CASE WHEN cj.Target_Role = 'Business Analyst' THEN 1 ELSE 0 END) AS BA_Demand,
    SUM(CASE WHEN cj.Target_Role = 'Data Analyst' THEN 1 ELSE 0 END) AS DA_Demand,
    COUNT(js.Job_ID) AS Total_Demand
FROM Skills s
JOIN Job_Skills js ON s.Skill_ID = js.Skill_ID
JOIN Categorized_Jobs cj ON js.Job_ID = cj.Job_ID
WHERE cj.Target_Role IN ('Business Analyst', 'Data Analyst')
GROUP BY s.Skill_Name
ORDER BY Total_Demand DESC;

-- --------------------------------------------------------------------
-- 4. Company Intelligence: Top Hiring Companies
-- Business Question: Which employers are driving hiring volume?
-- --------------------------------------------------------------------
SELECT 
    c.Company_Name,
    COUNT(j.Job_ID) AS Total_Postings
FROM Company c
JOIN Jobs j ON c.Company_ID = j.Company_ID
WHERE c.Company_Name != 'Not Specified'
GROUP BY c.Company_ID, c.Company_Name
ORDER BY Total_Postings DESC
LIMIT 10;

-- --------------------------------------------------------------------
-- 5. Skill Co-occurrence: Most Common Skill Pairs
-- Business Question: Which skills are most frequently required together?
-- --------------------------------------------------------------------
SELECT 
    s1.Skill_Name AS Skill_A,
    s2.Skill_Name AS Skill_B,
    COUNT(*) AS Co_Occurrence_Count
FROM Job_Skills js1
JOIN Job_Skills js2 ON js1.Job_ID = js2.Job_ID AND js1.Skill_ID < js2.Skill_ID
JOIN Skills s1 ON js1.Skill_ID = s1.Skill_ID
JOIN Skills s2 ON js2.Skill_ID = s2.Skill_ID
GROUP BY Skill_A, Skill_B
ORDER BY Co_Occurrence_Count DESC
LIMIT 10;
