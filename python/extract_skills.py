import pandas as pd
import re

SKILL_TAXONOMY = {
    # Technical / Analytics
    "SQL": {"category": "Technical / Analytics", "patterns": [r"\bsql\b", r"\bstructured query language\b"]},
    "Python": {"category": "Technical / Analytics", "patterns": [r"\bpython\b"]},
    "R": {"category": "Technical / Analytics", "patterns": [r"\br\b(?:\s+programming|\s+language|\s+scripting)?"]},
    "Excel": {"category": "Technical / Analytics", "patterns": [r"\bexcel\b", r"\bms excel\b", r"\badvanced excel\b"]},
    "Statistics": {"category": "Technical / Analytics", "patterns": [r"\bstatistics\b", r"\bstatistical analysis\b", r"\bstatistical modeling\b"]},
    "Data Analysis": {"category": "Technical / Analytics", "patterns": [r"\bdata analysis\b", r"\bdata analytics\b"]},
    
    # Business Intelligence
    "Power BI": {"category": "Business Intelligence", "patterns": [r"\bpower\s*bi\b", r"\bpower-bi\b"]},
    "Tableau": {"category": "Business Intelligence", "patterns": [r"\btableau\b"]},
    "Looker": {"category": "Business Intelligence", "patterns": [r"\blooker\b"]},
    
    # Business Skills
    "Requirements Gathering": {"category": "Business Skills", "patterns": [r"\brequirements gathering\b", r"\bbusiness requirements\b", r"\bbrd\b", r"\bfrd\b"]},
    "Stakeholder Management": {"category": "Business Skills", "patterns": [r"\bstakeholder management\b", r"\bstakeholder engagement\b", r"\bstakeholders\b"]},
    "Business Process Analysis": {"category": "Business Skills", "patterns": [r"\bbusiness process\b", r"\bprocess analysis\b", r"\bgap analysis\b"]},
    "Process Mapping": {"category": "Business Skills", "patterns": [r"\bprocess mapping\b", r"\bworkflow\b", r"\bflowcharts?\b"]},
    
    # Project / Delivery
    "Agile": {"category": "Project / Delivery", "patterns": [r"\bagile\b"]},
    "Scrum": {"category": "Project / Delivery", "patterns": [r"\bscrum\b"]},
    "Jira": {"category": "Project / Delivery", "patterns": [r"\bjira\b"]},
    
    # Communication
    "Communication": {"category": "Communication", "patterns": [r"\bcommunication skills?\b", r"\bverbal and written\b"]},
    "Presentation": {"category": "Communication", "patterns": [r"\bpresentation skills?\b", r"\bpresenting\b"]},
    "Documentation": {"category": "Communication", "patterns": [r"\bdocumentation\b", r"\btechnical documentation\b"]}
}

def extract_skills_from_text(text):
    if not isinstance(text, str):
        return []
    text_lower = text.lower()
    matched = []
    for skill, data in SKILL_TAXONOMY.items():
        for pat in data["patterns"]:
            if re.search(pat, text_lower):
                matched.append(skill)
                break
    return matched

def run():
    clean_path = '../data/processed/jobs_cleaned.csv'
    tagged_path = '../data/processed/jobs_tagged.csv'
    bridge_path = '../data/processed/job_skills_bridge.csv'
    skills_ref_path = '../data/processed/skills_dim.csv'
    
    df = pd.read_csv(clean_path)
    
    df['Skills_List'] = df['Job_Description'].apply(extract_skills_from_text)
    df['Skills'] = df['Skills_List'].apply(lambda x: "; ".join(x))
    df['Skill_Count'] = df['Skills_List'].apply(len)
    
    df.drop(columns=['Skills_List']).to_csv(tagged_path, index=False)
    
    skill_records = []
    skill_to_id = {}
    for idx, (name, details) in enumerate(SKILL_TAXONOMY.items(), start=1):
        skill_to_id[name] = idx
        skill_records.append({
            'Skill_ID': idx,
            'Skill_Name': name,
            'Skill_Category': details['category']
        })
    pd.DataFrame(skill_records).to_csv(skills_ref_path, index=False)
    
    bridge_records = []
    for _, row in df.iterrows():
        job_id = row['Job_ID']
        for skill in row['Skills_List']:
            bridge_records.append({'Job_ID': job_id, 'Skill_ID': skill_to_id[skill]})
            
    bridge_df = pd.DataFrame(bridge_records)
    bridge_df.to_csv(bridge_path, index=False)
    
    print("=" * 50)
    print("PHASE 6: SKILL EXTRACTION COMPLETE")
    print("=" * 50)
    print(f"Total Jobs Tagged:    {len(df)}")
    print(f"Total Skill Matches:  {len(bridge_df)}")
    print(f"Avg Skills per Job:   {round(df['Skill_Count'].mean(), 2)}")
    print(f"Jobs with >= 1 Skill: {len(df[df['Skill_Count'] > 0])}")

if __name__ == '__main__':
    run()
