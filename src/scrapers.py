"""
Scraper functions for different job platforms (Lever, Greenhouse, Ashby, etc.)
Each function returns a list of job dictionaries: {title, url}
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Set
import time

from config import REQUEST_DELAY_SECONDS, TIMEOUT_SECONDS, MYWORKDAYJOBS_URL_DETAILS
from utils import should_include_job
from output import print_debug, print_error


def make_request(
    url: str, max_retries: int = 3, **kwargs
) -> Optional[requests.Response]:
    """Make a request with timeout, error handling, and retries."""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=TIMEOUT_SECONDS, **kwargs)
            time.sleep(REQUEST_DELAY_SECONDS)  # Rate limiting
            return response
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:  # Last attempt
                print_debug(
                    f"Request failed for {url} after {max_retries} attempts: {e}"
                )
                return None
            else:
                print_debug(
                    f"Request attempt {attempt + 1} failed for {url}: {e}, retrying..."
                )
                # Brief exponential backoff before retry
                time.sleep(REQUEST_DELAY_SECONDS * (2**attempt))
    return None


def make_post_request(
    url: str, max_retries: int = 3, **kwargs
) -> Optional[requests.Response]:
    """Make a POST request with timeout, error handling, and retries."""
    for attempt in range(max_retries):
        try:
            response = requests.post(url, timeout=TIMEOUT_SECONDS, **kwargs)
            time.sleep(REQUEST_DELAY_SECONDS)  # Rate limiting
            return response
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:  # Last attempt
                print_debug(
                    f"POST request failed for {url} after {max_retries} attempts: {e}"
                )
                return None
            else:
                print_debug(
                    f"POST request attempt {attempt + 1} failed for {url}: {e}, retrying..."
                )
                # Brief exponential backoff before retry
                time.sleep(REQUEST_DELAY_SECONDS * (2**attempt))
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
            location_elem = posting.find(
                "span", class_="sort-by-location posting-category small-category-label"
            )

            if title_elem and url_elem:
                title = title_elem.get_text(strip=True)
                url = url_elem["href"]
                location = location_elem.get_text(strip=True) if location_elem else ""

                # Apply filtering and check for duplicates
                if should_include_job(title, location) and url not in found_jobs:
                    job_data = {
                        "title": title,
                        "url": url,
                    }
                    if location:
                        job_data["location"] = location

                    jobs.append(job_data)

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
            location = (
                job.get("location", {}).get("name", "") if job.get("location") else ""
            )

            # Apply filtering and check for duplicates
            if should_include_job(title, location) and url not in found_jobs:
                job_data = {
                    "title": title,
                    "url": url,
                }
                if location:
                    job_data["location"] = location

                jobs.append(job_data)

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

            # Handle Ashby's complex location format
            location = ""
            location_data = job.get("locationName", "") or job.get("address", "")

            if isinstance(location_data, dict):
                # Handle nested location structure like {'postalAddress': {'addressCountry': 'United States', ...}}
                if "postalAddress" in location_data:
                    postal = location_data["postalAddress"]
                    parts = []
                    if postal.get("addressLocality"):
                        parts.append(postal["addressLocality"])
                    if postal.get("addressRegion"):
                        parts.append(postal["addressRegion"])
                    if postal.get("addressCountry"):
                        parts.append(postal["addressCountry"])
                    location = ", ".join(parts)
                else:
                    # Try other common fields in location dict
                    location = (
                        location_data.get("name")
                        or location_data.get("city")
                        or location_data.get("location")
                        or str(location_data)
                    )
            else:
                location = location_data or ""

            # Apply filtering and check for duplicates
            if should_include_job(title, location) and url not in found_jobs:
                job_data = {
                    "title": title,
                    "url": url,
                }
                if location:
                    job_data["location"] = location

                jobs.append(job_data)

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
    # Netflix API hardcodes 10 jobs per request — this can't be changed using parameters
    page_size = 10
    start = 0
    # Netflix had ~546 jobs at the time of development
    max_pages = 80
    pages_fetched = 0

    print_debug("Scraping Netflix custom API")

    while pages_fetched < max_pages:
        api_url = f"https://explore.jobs.netflix.net/api/apply/v2/jobs?domain=netflix.com&start={start}"

        print_debug(f"Fetching Netflix page {pages_fetched + 1} (start={start})")

        response = make_request(api_url)
        if not response or response.status_code != 200:
            print_error(
                "Netflix",
                f"Failed to fetch Netflix jobs (status: {response.status_code if response else 'None'})",
            )
            break

        try:
            data = response.json()
            job_listings = data.get("positions", [])
            total_count = data.get("count", 0)  # Total jobs available

            # If no jobs returned, we've reached the end
            if not job_listings:
                print_debug(f"No more Netflix jobs found after {pages_fetched} pages")
                break

            page_jobs_found = 0
            for job in job_listings:
                title = job.get("name", "")
                url = job.get("canonicalPositionUrl", "")
                location = job.get("locations", [""])[0] if job.get("locations") else ""

                # Apply filtering and check for duplicates
                if should_include_job(title, location) and url not in found_jobs:
                    job_data = {
                        "title": title,
                        "url": url,
                    }
                    if location:
                        job_data["location"] = location

                    jobs.append(job_data)
                    page_jobs_found += 1

            print_debug(
                f"Found {page_jobs_found} new Netflix jobs on page {pages_fetched + 1} (total available: {total_count})"
            )

            # If we got fewer jobs than requested, we've likely reached the end
            if len(job_listings) < page_size:
                print_debug(
                    f"Netflix returned fewer jobs than requested, stopping pagination"
                )
                break

            # Increment by actual number of jobs returned (always 10 for Netflix)
            start += page_size
            pages_fetched += 1

            # Additional sleep between pages to be respectful
            if pages_fetched < max_pages:
                print_debug("Sleeping briefly between Netflix pages...")
                time.sleep(REQUEST_DELAY_SECONDS)

        except Exception as e:
            print_error("Netflix", f"Error parsing Netflix response: {e}")
            break

    print_debug(
        f"Netflix pagination complete: {len(jobs)} total new jobs found across {pages_fetched} pages"
    )
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
            location = job.get("city", "")

            # Apply filtering and check for duplicates
            if should_include_job(title, location) and url not in found_jobs:
                job_data = {
                    "title": title,
                    "url": url,
                }
                if location:
                    job_data["location"] = location

                jobs.append(job_data)

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

    page_size = 50
    current_page = 0
    max_pages = 20  # Reasonable limit to prevent infinite loops

    print_debug("Scraping Uber custom API")

    headers = {
        "x-csrf-token": "x",
    }

    params = {
        "localeCode": "en",
    }

    while current_page < max_pages:
        json_data = {
            "params": {
                "department": [
                    "Engineering",
                ],
            },
            "page": current_page,
            "limit": page_size,
        }

        print_debug(f"Fetching Uber page {current_page + 1}")

        response = make_post_request(
            api_url, params=params, headers=headers, json=json_data
        )
        if not response or response.status_code != 200:
            print_error(
                "Uber",
                f"Failed to fetch Uber jobs (status: {response.status_code if response else 'None'})",
            )
            break

        try:
            data = response.json()
            job_listings = data.get("data", {}).get("results", [])

            # If no jobs returned, we've reached the end
            if not job_listings:
                print_debug(f"No more Uber jobs found after {current_page} pages")
                break

            page_jobs_found = 0
            for job in job_listings:
                title = job.get("title", "")
                job_id = job.get("id", "")
                url = job_url_template.format(job_id) if job_id else ""

                # Extract location from potentially complex location data
                location_data = job.get("location", "")
                if isinstance(location_data, dict):
                    # Handle dictionary location data - try common fields
                    location = (
                        location_data.get("name", "")
                        or location_data.get("city", "")
                        or location_data.get("location", "")
                        or ""
                    )
                else:
                    location = location_data or ""

                # Apply filtering and check for duplicates
                if should_include_job(title, location) and url not in found_jobs:
                    job_data = {
                        "title": title,
                        "url": url,
                    }
                    if location:
                        job_data["location"] = location

                    jobs.append(job_data)
                    page_jobs_found += 1

            print_debug(
                f"Found {page_jobs_found} new Uber jobs on page {current_page + 1}"
            )

            # If we got fewer jobs than requested, we've likely reached the end
            if len(job_listings) < page_size:
                print_debug(
                    f"Uber returned fewer jobs than requested, stopping pagination"
                )
                break

            current_page += 1

            # Additional sleep between pages to be respectful
            if current_page < max_pages:
                print_debug("Sleeping briefly between Uber pages...")
                time.sleep(REQUEST_DELAY_SECONDS)

        except Exception as e:
            print_error("Uber", f"Error parsing Uber response: {e}")
            break

    print_debug(
        f"Uber pagination complete: {len(jobs)} total new jobs found across {current_page} pages"
    )
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
    jobs = []

    # Get company-specific URL details from config
    if company not in MYWORKDAYJOBS_URL_DETAILS:
        print_error(company, f"No Workday URL configuration found for {company}")
        return jobs

    config = MYWORKDAYJOBS_URL_DETAILS[company]
    datacenter_id = config["datacenter_id"]
    final_path_segment = config["final_path_segment"]

    # Construct the API endpoint URL
    api_url = f"https://{company}.wd{datacenter_id}.myworkdayjobs.com/wday/cxs/{company}/{final_path_segment}/jobs"
    base_url = (
        f"https://{company}.wd{datacenter_id}.myworkdayjobs.com/{final_path_segment}"
    )

    print_debug(f"Scraping Workday API for {company} at {api_url}")

    page_size = 20
    current_offset = 0
    # Workday sites can have many jobs, so higher limit
    # At the time of development, Raytheon Technologies had ~2600 jobs
    max_pages = 150
    pages_fetched = 0

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    }

    while pages_fetched < max_pages:
        # Workday API parameters
        # No filters used since different Workday-using companies have different filters on their job boards
        search_params = {
            "appliedFacets": {},
            "limit": page_size,
            "offset": current_offset,
            "searchText": "",
        }

        print_debug(
            f"Fetching {company} Workday page {pages_fetched + 1} (offset={current_offset})"
        )

        response = make_post_request(api_url, json=search_params, headers=headers)
        if not response or response.status_code != 200:
            print_error(
                company,
                f"Failed to fetch Workday jobs (status: {response.status_code if response else 'None'})",
            )
            break

        try:
            data = response.json()
            job_listings = data.get("jobPostings", [])

            # If no jobs returned, we've reached the end
            if not job_listings:
                print_debug(
                    f"No more {company} Workday jobs found after {pages_fetched} pages"
                )
                break

            page_jobs_found = 0
            for job in job_listings:
                title = job.get("title", "")
                external_path = job.get("externalPath", "")

                if not external_path:
                    continue

                # Construct the full job URL
                job_url = f"{base_url}{external_path}"

                # Extract location if available
                location = job.get("locationsText", "")

                # Apply filtering and check for duplicates
                if should_include_job(title, location) and job_url not in found_jobs:
                    job_data = {
                        "title": title,
                        "url": job_url,
                    }
                    if location:
                        job_data["location"] = location

                    jobs.append(job_data)
                    page_jobs_found += 1

            print_debug(
                f"Found {page_jobs_found} new {company} Workday jobs on page {pages_fetched + 1}"
            )

            # If we got fewer jobs than requested, we've likely reached the end
            if len(job_listings) < page_size:
                print_debug(
                    f"{company} Workday returned fewer jobs than requested, stopping pagination"
                )
                break

            current_offset += page_size
            pages_fetched += 1

            # Additional sleep between pages to be respectful
            if pages_fetched < max_pages:
                print_debug(f"Sleeping briefly between {company} Workday pages...")
                time.sleep(REQUEST_DELAY_SECONDS)

        except Exception as e:
            print_error(company, f"Error parsing Workday JSON response: {e}")
            break

    print_debug(
        f"{company} Workday pagination complete: {len(jobs)} total new jobs found across {pages_fetched} pages"
    )
    return jobs


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

    Note:
    Many companies that use iCIMS don't have a centralized "view all jobs" page.
    These companies have custom scrapers implemented for them.

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
    jobs = []

    # Jobvite uses jobs.jobvite.com/company-careers/jobs pattern
    api_url = f"https://jobs.jobvite.com/{company}-careers/jobs"

    print_debug(f"Scraping Jobvite for {company}")

    response = make_request(api_url)
    if not response or response.status_code != 200:
        print_error(
            company,
            f"Failed to fetch Jobvite jobs (status: {response.status_code if response else 'None'})",
        )
        return jobs

    try:
        soup = BeautifulSoup(response.content, "html.parser")

        # Look for job links in the table structure
        job_links = soup.find_all("a", href=lambda x: x and "/job/" in x)

        for link in job_links:
            title = link.get_text(strip=True)
            url = link.get("href", "")

            # Make URL absolute if relative
            if url and not url.startswith("http"):
                url = (
                    f"https://jobs.jobvite.com{url}"
                    if url.startswith("/")
                    else f"https://jobs.jobvite.com/{url}"
                )

            # Try to extract location from the table row
            location = ""
            # Look for location in the same table row
            tr_parent = link
            while tr_parent and tr_parent.name != "tr":
                tr_parent = tr_parent.parent

            if tr_parent:
                # Location is typically in the second column
                tds = tr_parent.find_all("td")
                if len(tds) > 1:
                    location = tds[1].get_text(strip=True)

            # Apply filtering and check for duplicates
            if (
                title
                and url
                and should_include_job(title, location)
                and url not in found_jobs
            ):
                job_data = {
                    "title": title,
                    "url": url,
                }
                if location:
                    job_data["location"] = location

                jobs.append(job_data)

    except Exception as e:
        print_error(company, f"Error parsing Jobvite response: {e}")

    return jobs


def smartrecruiters(company: str, found_jobs: Set[str]) -> List[Dict]:
    """
    Scraper for SmartRecruiters platform.

    Args:
        company: Name of company, already formatted for immediate use
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    jobs = []
    current_run_urls = set()  # Track URLs found in this run to prevent duplicates
    base_url = f"https://careers.smartrecruiters.com/{company}/"

    current_page = 1
    max_pages = 20  # Reasonable limit for HTML scraping

    print_debug(f"Scraping SmartRecruiters for {company}")

    while current_page <= max_pages:
        # SmartRecruiters uses page parameter for pagination
        if current_page == 1:
            api_url = base_url
        else:
            api_url = base_url + f"&page={current_page}"

        print_debug(f"Fetching {company} SmartRecruiters page {current_page}")

        response = make_request(api_url)
        if not response or response.status_code != 200:
            print_error(
                company,
                f"Failed to fetch SmartRecruiters jobs (status: {response.status_code if response else 'None'})",
            )
            break

        try:
            soup = BeautifulSoup(response.content, "html.parser")
            job_postings = soup.find_all(
                "li", attrs={"class": "opening-job job column wide-7of16 medium-1of2"}
            )

            # If no jobs found on this page, we've reached the end
            if not job_postings:
                print_debug(
                    f"No more {company} SmartRecruiters jobs found after {current_page - 1} pages"
                )
                break

            page_jobs_found = 0
            for posting in job_postings:
                title_elem = posting.find("h4")
                url_elem = posting.find("a")
                location_elem = posting.find("span", class_="job-location")

                if title_elem and url_elem:
                    title = title_elem.get_text(strip=True)
                    url = url_elem["href"]
                    location = (
                        location_elem.get_text(strip=True) if location_elem else ""
                    )

                    # Apply filtering and check for duplicates (both previous runs and current run)
                    if (
                        should_include_job(title, location)
                        and url not in found_jobs
                        and url not in current_run_urls
                    ):
                        job_data = {
                            "title": title,
                            "url": url,
                        }
                        if location:
                            job_data["location"] = location

                        jobs.append(job_data)
                        current_run_urls.add(
                            url
                        )  # Track this URL to prevent duplicates in same run
                        page_jobs_found += 1

            print_debug(
                f"Found {page_jobs_found} new {company} SmartRecruiters jobs on page {current_page}"
            )

            # If no new jobs found on this page, we've likely reached the end
            if page_jobs_found == 0:
                print_debug(
                    f"No new {company} SmartRecruiters jobs found on page {current_page}, stopping pagination"
                )
                break

            current_page += 1

            # Additional sleep between pages to be respectful
            if current_page <= max_pages:
                print_debug(
                    f"Sleeping briefly between {company} SmartRecruiters pages..."
                )
                time.sleep(REQUEST_DELAY_SECONDS)

        except Exception as e:
            print_error(company, f"Error parsing SmartRecruiters response: {e}")
            break

    print_debug(
        f"{company} SmartRecruiters pagination complete: {len(jobs)} total new jobs found across {current_page - 1} pages"
    )
    return jobs


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


def atlassian(found_jobs: Set[str]) -> List[Dict]:
    """
    Custom scraper for Atlassian.

    Args:
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    print("🚧 ATLASSIAN SCRAPER NOT YET IMPLEMENTED 🚧")
    return []


def github(found_jobs: Set[str]) -> List[Dict]:
    """
    Custom scraper for GitHub.

    Args:
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    print("🚧 GITHUB SCRAPER NOT YET IMPLEMENTED 🚧")
    return []


def ebay(found_jobs: Set[str]) -> List[Dict]:
    """
    Custom scraper for eBay.

    Args:
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    print("🚧 EBAY SCRAPER NOT YET IMPLEMENTED 🚧")
    return []


def tiktok(found_jobs: Set[str]) -> List[Dict]:
    """
    Custom scraper for TikTok.

    Args:
        found_jobs: Set containing URLs of previously found listings

    Returns:
        A list of new job listings for that company
    """
    print("🚧 TIKTOK SCRAPER NOT YET IMPLEMENTED 🚧")
    return []


# --------------------------------------------
