"""
Output formatting and logging utilities for job scraper.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List

# Ensure search_results directories exist
SEARCH_RESULTS_DIR = Path(__file__).parent / "search_results"
BY_COMPANY_DIR = SEARCH_RESULTS_DIR / "by_company"
BY_SCRAPE_DIR = SEARCH_RESULTS_DIR / "by_scrape"

# Create both directories
BY_COMPANY_DIR.mkdir(parents=True, exist_ok=True)
BY_SCRAPE_DIR.mkdir(parents=True, exist_ok=True)


def log_to_files(company: str, job_line: str, url: str) -> None:
    """Append job listing to company-specific log file."""
    # Create safe filename from company name
    safe_company_name = company.lower().replace(" ", "_").replace("-", "_")
    log_file = BY_COMPANY_DIR / f"{safe_company_name}.txt"

    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Append to log file
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {job_line}\n")
        f.write(f"{url}\n")
        f.write("\n")


def print_summary(jobs_found: Dict[str, List[Dict]]) -> None:
    """Print a summary of jobs found across all companies."""
    print("\n" + "=" * 60)
    print("SCRAPING SUMMARY")
    print("=" * 60)

    total_jobs = 0
    companies_with_jobs = 0

    for company, jobs in jobs_found.items():
        job_count = len(jobs)
        total_jobs += job_count

        if jobs:
            companies_with_jobs += 1
            print(f"{company}: {job_count} jobs")

    print(f"\nTotal jobs found: {total_jobs}")
    print(f"Companies with jobs: {companies_with_jobs}")

    # Create summary log file
    create_summary_log(jobs_found, total_jobs, companies_with_jobs)


def create_summary_log(
    jobs_found: Dict[str, List[Dict]], total_jobs: int, companies_with_jobs: int
) -> None:
    """Create a summary log file with all jobs found in this run."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M")
    summary_file = BY_SCRAPE_DIR / f"{timestamp}.txt"

    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(
            f"Job Scraper Summary - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        f.write("=" * 60 + "\n\n")

        f.write(f"Total jobs found: {total_jobs}\n")
        f.write(f"Companies with jobs: {companies_with_jobs}\n")

        for company, jobs in jobs_found.items():
            if jobs:
                f.write(f"\n{company} ({len(jobs)} jobs):\n")
                f.write("-" * 40 + "\n")

                for job in jobs:
                    if job.get("location"):
                        f.write(f"{company} --- {job['title']} ({job['location']})\n")
                    else:
                        f.write(f"{company} --- {job['title']}\n")
                    f.write(f"{job['url']}\n\n")


def print_error(company: str, error_message: str) -> None:
    """
    Print and log error messages for failed company scrapes.
    """
    error_msg = f"ERROR scraping {company}: {error_message}"
    print(error_msg)

    # Log error to error log file in by_scrape directory
    error_log_file = BY_SCRAPE_DIR / "errors.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(error_log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {error_msg}\n")


def print_debug(message: str) -> None:
    """
    Print debug messages (can be toggled based on log level).
    """
    from config import LOG_LEVEL

    if LOG_LEVEL == "DEBUG":
        print(f"DEBUG: {message}")
