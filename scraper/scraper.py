import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import time

# --- CONFIGURATION ---
# You will need to get these for free at developer.adzuna.com
APP_ID = 'e9841bd4'
APP_KEY = 'dc5cbc7132a653e9e9ceabb7eea18e72'
COUNTRY = 'in'  # e.g., 'in' for India, 'us' for US, 'gb' for UK
RESULTS_PER_PAGE = 50
TARGET_ROLES = ['Business Analyst', 'Data Analyst']  # In scope for MVP


def fetch_jobs(role, pages=5):
    """Fetches job postings from Adzuna API for a specific role."""
    all_jobs = []

    print(f"Fetching data for: {role}...")

    for page in range(1, pages + 1):
        url = f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/{page}"
        params = {
            'app_id': APP_ID,
            'app_key': APP_KEY,
            'results_per_page': RESULTS_PER_PAGE,
            'what': role,
            'content-type': 'application/json'
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            all_jobs.extend(results)
            print(f"  Page {page} retrieved: {len(results)} jobs.")
            time.sleep(1)  # Polite delay
        else:
            print(
                f"  Failed on page {page}. Status code: {response.status_code}")
            break

    return all_jobs


def process_and_save_data(raw_jobs):
    """Parses JSON, cleans HTML, and saves to CSV per the framework."""
    processed_data = []
    current_date = datetime.now().strftime('%Y-%m-%d')

    for job in raw_jobs:
        # Clean HTML from description using BeautifulSoup
        raw_desc = job.get('description', '')
        clean_desc = BeautifulSoup(
            raw_desc, "html.parser").get_text(separator=" ")

        # Map to requested Data Fields
        processed_data.append({
            'Job_ID': job.get('id'),
            'Job_Title': job.get('title'),
            'Company': job.get('company', {}).get('display_name'),
            'Location': job.get('location', {}).get('display_name'),
            # Permanent/Contract
            'Job_Type': job.get('contract_time', 'Unknown'),
            # Adzuna doesn't reliably provide this upfront
            'Experience_Requirement': 'Unknown',
            'Job_Description': clean_desc,
            'Skills': '',  # To be populated in Phase 6
            'Posted_Date': job.get('created'),
            'Job_URL': job.get('redirect_url'),
            'Source': 'Adzuna API',
            'Scraped_Date': current_date
        })

    df = pd.DataFrame(processed_data)

    # Save to the processed folder as required
    output_path = '../data/raw/jobs_raw.csv'
    df.to_csv(output_path, index=False)
    print(f"\nSuccess: {len(df)} jobs saved to {output_path}")


if __name__ == "__main__":
    combined_jobs = []

    for role in TARGET_ROLES:
        # 5 pages * 50 results = 250 jobs per role
        role_jobs = fetch_jobs(role, pages=5)
        combined_jobs.extend(role_jobs)

    process_and_save_data(combined_jobs)
