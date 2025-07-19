"""
Shared utility functions for the job scraper.
"""

from pathlib import Path
from typing import Set, List
from config import INCLUDE_KEYWORDS, EXCLUDE_KEYWORDS


def load_found_jobs() -> Set[str]:
    """
    Load previously found job URLs from jobs_found.txt into a set.

    Returns:
        Set of job URLs that have been found in previous runs
    """
    found_jobs = set()

    jobs_found_file = Path(__file__).parent / "jobs_found.txt"

    if jobs_found_file:  # Return empty set if file doesn't exist
        try:
            with open(jobs_found_file, "r", encoding="utf-8") as f:
                for line in f:
                    url = line.strip()
                    if url and url.startswith("http"):  # Basic URL validation
                        found_jobs.add(url)
        except Exception as e:
            print(f"Error loading jobs_found.txt: {e}")

    return found_jobs


def save_new_jobs(new_job_urls: List[str]) -> None:
    """
    Append new job URLs to jobs_found.txt.

    Args:
        new_job_urls: List of new job URLs to save
    """
    if not new_job_urls:
        return  # No new jobs found

    jobs_found_file = Path(__file__).parent / "jobs_found.txt"

    # Create new jobs_found.txt file if one doesn't already exist
    if not jobs_found_file.exists():
        jobs_found_file.touch()

    try:
        with open(jobs_found_file, "a", encoding="utf-8") as f:
            for url in new_job_urls:
                f.write(f"{url}\n")
    except Exception as e:
        print(f"Error saving new jobs to jobs_found.txt: {e}")


def should_include_job(job_title: str) -> bool:
    """
    Determine if a job should be included based on keyword filters.

    Args:
        job_title: Job title extracted from listing

    Returns:
        True if job satisfies keyword include and exclude requirements, False otherwise
    """
    job_title_lower = job_title.lower()

    # Must match at least one include keyword
    if not any(keyword.lower() in job_title_lower for keyword in INCLUDE_KEYWORDS):
        return False

    # Must not match any exclude keywords
    if any(keyword.lower() in job_title_lower for keyword in EXCLUDE_KEYWORDS):
        return False

    return True
