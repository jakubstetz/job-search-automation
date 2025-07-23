"""
Main orchestrator for the job scraper.
Loops through company lists, runs scrapers, applies filters, and manages duplicates.
"""

import sys
from datetime import datetime
from typing import Dict, List, Set
from output import print_debug
from collections import defaultdict

from companies import tier_1a, tier_1b, tier_2a, tier_2b, tier_2c
from output import log_to_files, print_summary, print_error
from utils import load_found_jobs, save_new_jobs, get_new_companies
from config import (
    OUTPUT_TO_CONSOLE,
    OUTPUT_TO_FILES_BY_COMPANY,
    OUTPUT_TO_FILES_BY_SCRAPE,
    INCLUDE_KEYWORDS,
    EXCLUDE_KEYWORDS,
)
from scrapers import (
    lever,
    greenhouse,
    ashby,
    myworkdayjobs,
    myworkdaysite,
    smartrecruiters,
    jobvite,
    icims,
)


def scrape_tier(
    tier_name: str, companies: List[Dict], found_jobs=Set[str]
) -> Dict[str, List[Dict]]:
    """
    Scrape jobs for all companies in a tier.

    Args:
        tier_name: Name of the tier (for logging)
        companies: List of companies formatted as dictionaries
        found_jobs: Set containing URLs of previously found listings

    Returns:
        Dictionary mapping company names to lists of jobs found
    """
    tier_results = {}

    print(f"\n{'='*60}")
    print(f"SCRAPING {tier_name.upper()}")
    print(f"{'='*60}")

    # Scrape all companies in tier
    for company_data in companies:
        company_name = company_data.get("name", "")
        formatted_name = company_data.get("formatted_name", "")
        scraper = company_data.get("scraper", "")

        # Skip companies without scrapers configured
        if not scraper:
            print_debug(f"No scraper configured for {company_name}")
            continue

        print(f"\n{'- '*30}")
        try:
            # formatted_name not needed for custom scrapers
            if scraper in [
                lever,
                greenhouse,
                ashby,
                myworkdayjobs,
                myworkdaysite,
                smartrecruiters,
                jobvite,
                icims,
            ]:
                jobs = scraper(formatted_name, found_jobs)
            else:
                jobs = scraper(found_jobs)
            tier_results[company_name] = jobs

            # Print results and log to files
            print(f"Found {len(jobs)} new matching jobs for {company_name}\n")
            for job in jobs:
                # Include location if available
                if job.get("location"):
                    job_line = f"{company_name} --- {job['title']} ({job['location']})"
                else:
                    job_line = f"{company_name} --- {job['title']}"
                print(job_line)
                print(job["url"])
                print()
                log_to_files(company_name, job_line, job["url"])

        except Exception as e:
            print_error(company_name, f"Unexpected error: {e}")
            tier_results[company_name] = []

    return tier_results


def main():
    """
    Main function that orchestrates the entire scraping process.
    """

    print(f"Job Scraper Starting - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    start_time = datetime.now()

    print(f"INCLUDE_KEYWORDS:")
    print(", ".join(INCLUDE_KEYWORDS))
    print()

    print("EXCLUDE_KEYWORDS:")
    print(", ".join(EXCLUDE_KEYWORDS))
    print()

    # Load previously found jobs for duplicate prevention
    print("Loading previously found jobs...")
    found_jobs = load_found_jobs()
    print(f"Loaded {len(found_jobs)} previously found jobs")

    # Define tiers to scrape
    tiers = [
        ("Tier 1A", tier_1a),
        ("Tier 1B", tier_1b),
        ("Tier 2A", tier_2a),
        ("Tier 2B", tier_2b),
        ("Tier 2C", tier_2c),
    ]

    # Get all companies across all tiers to check for new ones
    all_companies = []
    for _, tier_companies in tiers:
        all_companies.extend(tier_companies)

    # Identify companies being scraped for the first time
    new_companies = get_new_companies(all_companies)
    if new_companies:
        print("New companies detected (first-time scrape):")
        for company in new_companies:
            print(f"  - {company}")

    # Scrape each tier and extend list of newly discovered jobs
    all_results = defaultdict(list)  # New listings stored by company
    all_new_jobs = []  # URLs for all newly discoverd listings
    for tier_name, tier_companies in tiers:
        tier_results = scrape_tier(tier_name, tier_companies, found_jobs)

        for company_name, jobs in tier_results.items():
            for job in jobs:
                all_new_jobs.append(job["url"])
                all_results[company_name].append(job)

    # Summarize results and clean up
    print(f"\n{len(all_new_jobs)} new jobs discovered")

    if all_new_jobs:
        print(f"\nSaving newly discovered job URLs to jobs_found.txt...")
        save_new_jobs(all_new_jobs)

    print_summary(all_results, new_companies)

    process_time = (datetime.now() - start_time).total_seconds()
    print(f"\nJob Scraper Completed - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"(Total time taken: {process_time}s)\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)
