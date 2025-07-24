#!/usr/bin/env python3
"""
Manual testing script for scrapers.
- Only outputs to console (no files)
- No filtering on job roles (all openings listed)
- Only scrapes companies with manually_verified=False
"""

import sys
import os
from datetime import datetime
from typing import Dict, List, Set
from collections import defaultdict

# Add src directory to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from companies import tier_1a, tier_1b, tier_2a, tier_2b, tier_2c
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

# Override filtering to disable it for manual testing
os.environ["APPLY_FILTERING"] = "False"


def should_include_job_no_filter(job_title: str, location: str = "") -> bool:
    """Always return True to bypass all filtering for manual testing."""
    return True


def scrape_unverified_company(company_data: Dict, found_jobs: Set[str]) -> List[Dict]:
    """
    Scrape jobs for a single unverified company.

    Args:
        company_data: Company dictionary with scraper info
        found_jobs: Set of previously found job URLs (for duplicate detection)

    Returns:
        List of jobs found for this company
    """
    company_name = company_data.get("name", "")
    formatted_name = company_data.get("formatted_name", "")
    scraper = company_data.get("scraper", "")
    manually_verified = company_data.get("manually_verified", True)

    # Skip manually verified companies
    if manually_verified:
        return []

    # Skip companies without scrapers configured
    if not scraper:
        print(f"No scraper configured for {company_name}")
        return []

    print(f"\nScraping {company_name}...")
    print("-" * 40)

    try:
        # Call the appropriate scraper
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

        print(f"Found {len(jobs)} jobs for {company_name}")

        # Print each job to console
        for job in jobs:
            if job.get("location"):
                print(f"  • {job['title']} ({job['location']})")
            else:
                print(f"  • {job['title']}")
            print(f"    {job['url']}")

        return jobs

    except Exception as e:
        print(f"ERROR scraping {company_name}: {e}")
        return []


def main():
    """Main function for manual testing."""
    print("Manual Scraper Testing - No Filters, Console Only")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print("Testing companies with manually_verified=False only")
    print("All job openings will be listed (no role filtering)")
    print("=" * 60)

    start_time = datetime.now()

    # Use empty set for found_jobs since we're not tracking duplicates for testing
    found_jobs = set()

    # Collect all companies from all tiers
    all_tiers = [
        ("Tier 1A", tier_1a),
        ("Tier 1B", tier_1b),
        ("Tier 2A", tier_2a),
        ("Tier 2B", tier_2b),
        ("Tier 2C", tier_2c),
    ]

    all_results = defaultdict(list)
    total_jobs = 0
    companies_scraped = 0

    # Process each tier
    for tier_name, companies in all_tiers:
        print(f"\n{'='*20} {tier_name} {'='*20}")

        unverified_companies = [
            c for c in companies if not c.get("manually_verified", True)
        ]
        verified_companies = [c for c in companies if c.get("manually_verified", True)]

        print(f"Unverified companies to test: {len(unverified_companies)}")
        print(f"Verified companies (skipped): {len(verified_companies)}")

        if verified_companies:
            print("Skipping verified companies:")
            for company in verified_companies:
                print(f"  - {company.get('name', 'Unknown')}")

        # Scrape unverified companies
        for company_data in unverified_companies:
            jobs = scrape_unverified_company(company_data, found_jobs)
            if jobs:
                company_name = company_data.get("name", "")
                all_results[company_name] = jobs
                total_jobs += len(jobs)
                companies_scraped += 1

    # Print summary
    print(f"\n{'='*60}")
    print("MANUAL TESTING SUMMARY")
    print(f"{'='*60}")
    print(f"Companies scraped: {companies_scraped}")
    print(f"Total jobs found: {total_jobs}")

    if all_results:
        print(f"\nJobs by company:")
        for company_name, jobs in all_results.items():
            print(f"  {company_name}: {len(jobs)} jobs")

    process_time = (datetime.now() - start_time).total_seconds()
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total time: {process_time:.1f}s")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nTesting interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)
