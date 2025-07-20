"""
Scraper functions for different job platforms (Lever, Greenhouse, Ashby, etc.)
Each function returns a list of job dictionaries: {title, url}
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Set
import time

from config import REQUEST_DELAY_SECONDS, TIMEOUT_SECONDS
from utils import should_include_job
from output import print_debug, print_error


def make_request(url: str, **kwargs) -> Optional[requests.Response]:
    """Make a request with timeout and error handling."""
    try:
        response = requests.get(url, timeout=TIMEOUT_SECONDS, **kwargs)
        time.sleep(REQUEST_DELAY_SECONDS)  # Rate limiting
        return response
    except requests.exceptions.RequestException as e:
        print_debug(f"Request failed for {url}: {e}")
        return None


def make_post_request(url: str, **kwargs) -> Optional[requests.Response]:
    """Make a POST request with timeout and error handling."""
    try:
        response = requests.post(url, timeout=TIMEOUT_SECONDS, **kwargs)
        time.sleep(REQUEST_DELAY_SECONDS)  # Rate limiting
        return response
    except requests.exceptions.RequestException as e:
        print_debug(f"POST request failed for {url}: {e}")
        return None


# --------------------------------------------


def lever(company: str, found_jobs: Set[str]) -> List[Dict]:
    """
    Scrape jobs from Lever platform.

    Args:
        company: Name of company, already formatted for immediate use
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    jobs = []
    api_url = f"https://jobs.lever.co/{company}"

    print_debug(f"Scraping Lever for {company}")

    response = make_request(api_url)
    if not response or response.status_code != 200:
        print_error(
            company,
            f"Failed to fetch Lever jobs (status: {response.status_code if response else 'None'})",
        )
        return jobs

    try:
        soup = BeautifulSoup(response.content, "html.parser")
        job_postings = soup.find_all("div", attrs={"class": "posting"})

        for posting in job_postings:
            title_elem = posting.find("h5")
            url_elem = posting.find("a")

            if title_elem and url_elem:
                title = title_elem.get_text(strip=True)
                url = url_elem["href"]

                # Apply filtering and check for duplicates
                if should_include_job(title) and url not in found_jobs:
                    jobs.append(
                        {
                            "title": title,
                            "url": url,
                        }
                    )

    except Exception as e:
        print_error(company, f"Error parsing Lever response: {e}")

    return jobs


def greenhouse(company: str, found_jobs: Set[str]) -> List[Dict]:
    """
    Scrape jobs from Greenhouse platform.

    Args:
        company: Name of company, already formatted for immediate use
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    jobs = []
    api_url = f"https://api.greenhouse.io/v1/boards/{company}/jobs"

    print_debug(f"Scraping Greenhouse for {company}")

    response = make_request(api_url)
    if not response or response.status_code != 200:
        print_error(
            company,
            f"Failed to fetch Greenhouse jobs (status: {response.status_code if response else 'None'})",
        )
        return jobs

    try:
        data = response.json()
        job_listings = data.get("jobs", [])

        for job in job_listings:
            title = job.get("title", "")
            url = job.get("absolute_url", "")

            # Apply filtering and check for duplicates
            if should_include_job(title) and url not in found_jobs:
                jobs.append(
                    {
                        "title": title,
                        "url": url,
                    }
                )

    except Exception as e:
        print_error(company, f"Error parsing Greenhouse response: {e}")

    return jobs


def ashby(company: str, found_jobs: Set[str]) -> List[Dict]:
    """
    Scrape jobs from Ashby platform.

    Args:
        company: Name of company, already formatted for immediate use
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    jobs = []
    api_url = f"https://api.ashbyhq.com/posting-api/job-board/{company}"

    print_debug(f"Scraping Ashby for {company}")

    response = make_request(api_url)
    if not response or response.status_code != 200:
        print_error(
            company,
            f"Failed to fetch Ashby jobs (status: {response.status_code if response else 'None'})",
        )
        return jobs

    try:
        data = response.json()
        job_listings = data.get("jobs", [])

        for job in job_listings:
            title = job.get("title", "")
            url = job.get("jobUrl", "")

            # Apply filtering and check for duplicates
            if should_include_job(title) and url not in found_jobs:
                jobs.append(
                    {
                        "title": title,
                        "url": url,
                    }
                )

    except Exception as e:
        print_error(company, f"Error parsing Ashby response: {e}")

    return jobs


def netflix(found_jobs: Set[str]) -> List[Dict]:
    """
    Custom scraper for Netflix.

    Args:
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    jobs = []
    api_url = "https://explore.jobs.netflix.net/api/apply/v2/jobs?domain=netflix.com&start=0&num=50&query=Software%20Engineer&sort_by=relevance"

    print_debug("Scraping Netflix custom API")

    response = make_request(api_url)
    if not response or response.status_code != 200:
        print_error(
            "Netflix",
            f"Failed to fetch Netflix jobs (status: {response.status_code if response else 'None'})",
        )
        return jobs

    try:
        data = response.json()
        job_listings = data.get("positions", [])

        for job in job_listings:
            title = job.get("name", "")
            url = job.get("canonicalPositionUrl", "")

            # Apply filtering and check for duplicates
            if should_include_job(title) and url not in found_jobs:
                jobs.append(
                    {
                        "title": title,
                        "url": url,
                    }
                )

    except Exception as e:
        print_error("Netflix", f"Error parsing Netflix response: {e}")

    return jobs


def spotify(found_jobs: Set[str]) -> List[Dict]:
    """
    Custom scraper for Spotify.

    Args:
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    jobs = []
    api_url = "https://api-dot-new-spotifyjobs-com.nw.r.appspot.com/wp-json/animal/v1/job/search?c=engineering"
    listing_url_template = "https://www.lifeatspotify.com/jobs/{}"

    print_debug("Scraping Spotify custom API")

    response = make_request(api_url)
    if not response or response.status_code != 200:
        print_error(
            "Spotify",
            f"Failed to fetch Spotify jobs (status: {response.status_code if response else 'None'})",
        )
        return jobs

    try:
        data = response.json()
        job_listings = data.get("result", [])

        for job in job_listings:
            title = job.get("text", "")
            job_id = job.get("id", "")
            url = listing_url_template.format(job_id) if job_id else ""

            # Apply filtering and check for duplicates
            if should_include_job(title) and url not in found_jobs:
                jobs.append(
                    {
                        "title": title,
                        "url": url,
                    }
                )

    except Exception as e:
        print_error("Spotify", f"Error parsing Spotify response: {e}")

    return jobs


def uber(found_jobs: Set[str]) -> List[Dict]:
    """
    Custom scraper for Uber.

    Args:
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    jobs = []
    api_url = "https://www.uber.com/api/loadSearchJobsResults"
    job_url_template = "https://www.uber.com/global/en/careers/list/{}/"

    print_debug("Scraping Uber custom API")

    headers = {
        "x-csrf-token": "x",
    }

    params = {
        "localeCode": "en",
    }

    json_data = {
        "params": {
            "department": [
                "Engineering",
            ],
            "query": "software engineer",
        },
        "page": 0,
        "limit": 50,
    }

    response = make_post_request(
        api_url, params=params, headers=headers, json=json_data
    )
    if not response or response.status_code != 200:
        print_error(
            "Uber",
            f"Failed to fetch Uber jobs (status: {response.status_code if response else 'None'})",
        )
        return jobs

    try:
        data = response.json()
        job_listings = data.get("data", {}).get("results", [])

        for job in job_listings:
            title = job.get("title", "")
            job_id = job.get("id", "")
            url = job_url_template.format(job_id) if job_id else ""

            # Apply filtering and check for duplicates
            if should_include_job(title) and url not in found_jobs:
                jobs.append(
                    {
                        "title": title,
                        "url": url,
                    }
                )

    except Exception as e:
        print_error("Uber", f"Error parsing Uber response: {e}")

    return jobs


def servicenow(found_jobs: Set[str]) -> List[Dict]:
    """
    Custom scraper for ServiceNow.

    Args:
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    jobs = []
    api_url = (
        "https://careers.smartrecruiters.com/ServiceNow/?search=software%20engineer"
    )

    print_debug("Scraping ServiceNow custom API")

    response = make_request(api_url)
    if not response or response.status_code != 200:
        print_error(
            "ServiceNow",
            f"Failed to fetch ServiceNow jobs (status: {response.status_code if response else 'None'})",
        )
        return jobs

    try:
        soup = BeautifulSoup(response.content, "html.parser")
        job_postings = soup.find_all(
            "li", attrs={"class": "opening-job job column wide-7of16 medium-1of2"}
        )

        for posting in job_postings:
            title_elem = posting.find("h4")
            url_elem = posting.find("a")

            if title_elem and url_elem:
                title = title_elem.get_text(strip=True)
                url = url_elem["href"]

                # Apply filtering and check for duplicates
                if should_include_job(title) and url not in found_jobs:
                    jobs.append(
                        {
                            "title": title,
                            "url": url,
                        }
                    )

    except Exception as e:
        print_error("ServiceNow", f"Error parsing ServiceNow response: {e}")

    return jobs


# --------------------------------------------
# NOT YET IMPLEMENTED
# --------------------------------------------


def myworkdayjobs(company: str, found_jobs: Set[str]) -> List[Dict]:
    """
    Scraper for Workday platform, specifically the myworkdayjobs.com domain.

    Args:
        company: Name of company, already formatted for immediate use
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    print("🚧 MYWORKDAYJOBS SCRAPER NOT YET IMPLEMENTED 🚧")
    return []


def myworkdaysite(company: str, found_jobs: Set[str]) -> List[Dict]:
    """
    Scraper for Workday platform, specifically the myworkdaysite.com domain.

    Args:
        company: Name of company, already formatted for immediate use
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    print("🚧 MYWORKDAYSITE SCRAPER NOT YET IMPLEMENTED 🚧")
    return []


def icims(company: str, found_jobs: Set[str]) -> List[Dict]:
    """
    Scraper for iCIMS platform.

    Args:
        company: Name of company, already formatted for immediate use
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    print("🚧 ICIMS SCRAPER NOT YET IMPLEMENTED 🚧")
    return []


def successfactors(company: str, found_jobs: Set[str]) -> List[Dict]:
    """
    Scraper for SuccessFactors platform.

    Args:
        company: Name of company, already formatted for immediate use
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    print("🚧 SUCCESSFACTORS SCRAPER NOT YET IMPLEMENTED 🚧")
    return []


def nc2(company: str, found_jobs: Set[str]) -> List[Dict]:
    """
    Scraper for NC2 platform.

    Args:
        company: Name of company, already formatted for immediate use
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    print("🚧 NC2 SCRAPER NOT YET IMPLEMENTED 🚧")
    return []


def jobvite(company: str, found_jobs: Set[str]) -> List[Dict]:
    """
    Scraper for Jobvite platform.

    Args:
        company: Name of company, already formatted for immediate use
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    print("🚧 JOBVITE SCRAPER NOT YET IMPLEMENTED 🚧")
    return []


def smartrecruiters(company: str, found_jobs: Set[str]) -> List[Dict]:
    """
    Scraper for SmartRecruiters platform.

    Args:
        company: Name of company, already formatted for immediate use
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    print("🚧 SMARTRECRUITERS SCRAPER NOT YET IMPLEMENTED 🚧")
    return []


def avature(company: str, found_jobs: Set[str]) -> List[Dict]:
    """
    Scraper for Avature platform.

    Args:
        company: Name of company, already formatted for immediate use
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    print("🚧 AVATURE SCRAPER NOT YET IMPLEMENTED 🚧")
    return []


def meta(found_jobs: Set[str]) -> List[Dict]:
    """
    Custom scraper for Meta.

    Args:
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    print("🚧 META SCRAPER NOT YET IMPLEMENTED 🚧")
    return []


def google(found_jobs: Set[str]) -> List[Dict]:
    """
    Custom scraper for Google.

    Args:
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    print("🚧 GOOGLE SCRAPER NOT YET IMPLEMENTED 🚧")
    return []


def wiz(found_jobs: Set[str]) -> List[Dict]:
    """
    Custom scraper for Wiz.

    Args:
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    print("🚧 WIZ SCRAPER NOT YET IMPLEMENTED 🚧")
    return []


def apple(found_jobs: Set[str]) -> List[Dict]:
    """
    Custom scraper for Apple.

    Args:
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    print("🚧 APPLE SCRAPER NOT YET IMPLEMENTED 🚧")
    return []


def amazon(found_jobs: Set[str]) -> List[Dict]:
    """
    Custom scraper for Amazon.

    Args:
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    print("🚧 AMAZON SCRAPER NOT YET IMPLEMENTED 🚧")
    return []


def microsoft(found_jobs: Set[str]) -> List[Dict]:
    """
    Custom scraper for Microsoft.

    Args:
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    print("🚧 MICROSOFT SCRAPER NOT YET IMPLEMENTED 🚧")
    return []


def hubspot(found_jobs: Set[str]) -> List[Dict]:
    """
    Custom scraper for HubSpot.

    Args:
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    print("🚧 HUBSPOT SCRAPER NOT YET IMPLEMENTED 🚧")
    return []


def deloitte(found_jobs: Set[str]) -> List[Dict]:
    """
    Custom scraper for Deloitte.

    Args:
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    print("🚧 DELOITTE SCRAPER NOT YET IMPLEMENTED 🚧")
    return []


def qualcomm(found_jobs: Set[str]) -> List[Dict]:
    """
    Custom scraper for Qualcomm.

    Args:
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    print("🚧 QUALCOMM SCRAPER NOT YET IMPLEMENTED 🚧")
    return []


def peloton(found_jobs: Set[str]) -> List[Dict]:
    """
    Custom scraper for Peloton.

    Args:
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    print("🚧 PELOTON SCRAPER NOT YET IMPLEMENTED 🚧")
    return []


def linkedin(found_jobs: Set[str]) -> List[Dict]:
    """
    Custom scraper for LinkedIn.

    Args:
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    print("🚧 APPLE SCRAPER NOT YET IMPLEMENTED 🚧")
    return []


# --------------------------------------------
