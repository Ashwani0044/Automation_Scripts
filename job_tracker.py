import sqlite3
import requests
from datetime import datetime

DB_NAME = "job_tracker.db" # making database to store seen jobs

# target keywords for the jobs
TARGET_KEYWORDS = ["python", "fastapi", "flask", "backend", "developer", "intern", "full-stack", "cloud"]

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS seen_jobs (
            id TEXT PRIMARY KEY,
            title TEXT,
            company TEXT,
            url TEXT,
            date_added TEXT
        )
    """)
    conn.commit()
    conn.close()

def fetch_remote_jobs():

    url = "https://remoteok.com/api"
    # remoteOK api needs header or they block requests
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # The first item in Remote OK's JSON is usually a legal/meta disclaimer object, so skip it
        jobs = data[1:] if len(data) > 1 else []
        return jobs
    except Exception as e:
        print(f"Error fetching jobs: {e}")
        return []

def process_jobs():

    init_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    raw_jobs = fetch_remote_jobs()
    new_jobs_found = []

    print(f"Scanning {len(raw_jobs)} listings...")

    for job in raw_jobs:
        job_id = str(job.get("id"))
        title = job.get("position", "").lower()
        company = job.get("company", "Unknown")
        apply_url = job.get("url") or job.get("apply_url")
        tags = [t.lower() for t in job.get("tags", [])]

        if not job_id or not apply_url:
            continue

        match_found = any(kw in title or any(kw in tag for tag in tags) for kw in TARGET_KEYWORDS)

        if match_found:
            # Check if we've already seen this job ID in our database
            cursor.execute("SELECT id FROM seen_jobs WHERE id = ?", (job_id,))
            exists = cursor.fetchone()

            if not exists:
                # Save to database so we don't alert about it again
                cursor.execute(
                    "INSERT INTO seen_jobs (id, title, company, url, date_added) VALUES (?, ?, ?, ?, ?)",
                    (job_id, job.get("position"), company, apply_url, datetime.now().strftime("%Y-%m-%d"))
                )
                conn.commit()
                
                new_jobs_found.append({
                    "title": job.get("position"),
                    "company": company,
                    "url": apply_url
                })

    conn.close()
    return new_jobs_found

def notify_user(new_jobs):
    """Handles alerts for new jobs."""
    if not new_jobs:
        print("No new matching jobs found today.")
        return

    print(f"\n Found {len(new_jobs)} NEW matching job(s)!\n")
    for idx, job in enumerate(new_jobs, 1):
        print(f"{idx}. {job['title']} at {job['company']}")
        print(f"   Link: {job['url']}\n")


if __name__ == "__main__":
    new_listings = process_jobs()
    notify_user(new_listings)