DROP TABLE IF EXISTS Job_Skills;
DROP TABLE IF EXISTS Skills;
DROP TABLE IF EXISTS Jobs;
DROP TABLE IF EXISTS Company;
DROP TABLE IF EXISTS Location;

CREATE TABLE Location (
    Location_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    City VARCHAR(100),
    State_Region VARCHAR(100),
    Country VARCHAR(50) DEFAULT 'India',
    UNIQUE(City, State_Region, Country)
);

CREATE TABLE Company (
    Company_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Company_Name VARCHAR(255) UNIQUE
);

CREATE TABLE Skills (
    Skill_ID INTEGER PRIMARY KEY,
    Skill_Name VARCHAR(100) UNIQUE,
    Skill_Category VARCHAR(100)
);

CREATE TABLE Jobs (
    Job_ID BIGINT PRIMARY KEY,
    Job_Title VARCHAR(255),
    Company_ID INTEGER,
    Location_ID INTEGER,
    Job_Type VARCHAR(50),
    Experience VARCHAR(50),
    Posted_Date DATE,
    Job_URL TEXT,
    Source VARCHAR(50),
    Scraped_Date DATE,
    Job_Description TEXT,
    FOREIGN KEY (Company_ID) REFERENCES Company(Company_ID),
    FOREIGN KEY (Location_ID) REFERENCES Location(Location_ID)
);

CREATE TABLE Job_Skills (
    Job_ID BIGINT,
    Skill_ID INTEGER,
    PRIMARY KEY (Job_ID, Skill_ID),
    FOREIGN KEY (Job_ID) REFERENCES Jobs(Job_ID),
    FOREIGN KEY (Skill_ID) REFERENCES Skills(Skill_ID)
);

CREATE INDEX idx_jobs_company ON Jobs(Company_ID);
CREATE INDEX idx_jobs_location ON Jobs(Location_ID);
CREATE INDEX idx_bridge_skill ON Job_Skills(Skill_ID);
