# Queries GitHub's public API endpoint to get a live list of your repositories, star counts, primary programming languages, and last updated timestamps.

import os
import subprocess
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")

# github personal access token is required for private repo
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

BACKUP_DIR = "./github_backups" # to store the repo backup locally

def get_github_repos():

    url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos?per_page=100"
    headers = {"Accept", "vnd.github+json"}

    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    try:
        response = requests.get(url ,headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching repositories from Github API: {e}")
        return []


def backup_and_report_repos(repos):
    """clones new repo or pulls from the existing ones, and compiles status"""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    total_stars = 0
    languages = {}
    updated_repos_count = 0

    print(f"\n Starting Github backup and sync for user: {GITHUB_USERNAME}\n")

    for repo in repos:
        repo_name = repo["name"]
        clone_url = repo["clone_url"]
        stars = repo["stargazers_count"]
        lang = repo["language"] or "Unknown"
        updated_at = repo["updated_at"]

        # Aggregate stats
        total_stars += stars
        languages[lang] = languages.get(lang, 0) + 1

        # Local path for this specific repo
        repo_path = os.path.join(BACKUP_DIR, repo_name)

        if os.path.exists(repo_path):
            print(f"Pulling latest updates for the repo: {repo_name}\n")
            try:
                subprocess.run(
                    ["git", "-C", repo_path, "pull"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=True
                )

                updated_repos_count += 1
            except subprocess.CalledProcessError:
                print(f"   Warning: Could not pull updates for {repo_name} (local changes might exist).")
        else:
            print(f"Cloning the new repo: {repo_name}\n")
            try:
                subprocess.run(
                    ["git", "clone", clone_url, repo_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=True
                )
            except:
                print(f"ERROR: Failed to clone {repo_name}")

    # generate summary report text
    report = f"""
        ========================================
        GITHUB ACTIVITY & BACKUP REPORT
        ========================================
        Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        User: {GITHUB_USERNAME}
        Total Repositories Managed: {len(repos)}
        Total Stars Earned: {total_stars}
        Repositories Synced Locally: {updated_repos_count}

        Top Languages Breakdown:
    """
    for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
        report += f" - {lang}: {count} repo(s)\n"
    
    report += "========================================\n"
    
    # Save report to a text file locally
    report_filename = f"github_report_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(report_filename, "w", encoding="utf-8") as f:
        f.write(report)

    print(report)
    print(f"Backup completed! Report saved to {report_filename}")


def main():
    repos = get_github_repos()
    if repos:
        backup_and_report_repos(repos)
    else:
        print("No repositories found or failed to connect.")

if __name__ == "__main__":
    main() 