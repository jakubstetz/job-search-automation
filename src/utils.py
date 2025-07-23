"""
Shared utility functions for the job scraper.
"""

from pathlib import Path
from typing import Set, List, Dict
from config import INCLUDE_KEYWORDS, EXCLUDE_KEYWORDS


def get_new_companies(all_companies: List[Dict]) -> Set[str]:
    """
    Determine which companies are being scraped for the first time.

    Args:
        all_companies: List of all company dictionaries from all tiers

    Returns:
        Set of company names that don't have existing log files
    """
    from output import BY_COMPANY_DIR  # Import here to avoid circular imports

    new_companies = set()

    for company_data in all_companies:
        company_name = company_data.get("name", "")
        if not company_name:
            continue

        # Create safe filename from company name (same logic as in log_to_files)
        safe_company_name = company_name.lower().replace(" ", "_").replace("-", "_")
        log_file = BY_COMPANY_DIR / f"{safe_company_name}.txt"

        # If log file doesn't exist, this is a new company
        if not log_file.exists():
            new_companies.add(company_name)

    return new_companies


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


def should_include_job(job_title: str, location: str = "") -> bool:
    """
    Determine if a job should be included based on keyword and location filters.

    Args:
        job_title: Job title extracted from listing
        location: Job location (optional)

    Returns:
        True if job satisfies keyword include/exclude and location requirements, False otherwise
    """
    job_title_lower = job_title.lower()

    # Must match at least one include keyword
    if not any(keyword.lower() in job_title_lower for keyword in INCLUDE_KEYWORDS):
        return False

    # Must not match any exclude keywords
    if any(keyword.lower() in job_title_lower for keyword in EXCLUDE_KEYWORDS):
        return False

    # Location filtering: include if no location specified OR location is US/EU
    if location and not is_us_or_eu_location(location):
        return False

    return True


def is_us_or_eu_location(location) -> bool:
    """
    Check if a location is in the United States or European Union.

    Args:
        location: Location string or dict to check

    Returns:
        True if location is in US or EU, False otherwise
    """
    if not location:
        return False

    # Handle non-string location data (e.g., dict from APIs)
    if not isinstance(location, str):
        return False

    location_lower = location.lower()

    import re

    # US country and general indicators (simple substring match)
    us_general_indicators = [
        "united states",
        "usa",
        "america",
        "american",
    ]

    # US states full names (simple substring match)
    us_state_names = [
        "california",
        "new york",
        "texas",
        "florida",
        "washington",
        "illinois",
        "pennsylvania",
        "ohio",
        "georgia",
        "north carolina",
        "michigan",
        "new jersey",
        "virginia",
        "tennessee",
        "arizona",
        "massachusetts",
        "indiana",
        "maryland",
        "missouri",
        "wisconsin",
        "colorado",
        "minnesota",
        "south carolina",
        "alabama",
        "louisiana",
        "kentucky",
        "oregon",
        "oklahoma",
        "connecticut",
        "utah",
        "iowa",
        "nevada",
        "arkansas",
        "mississippi",
        "kansas",
        "new mexico",
        "nebraska",
        "west virginia",
        "idaho",
        "hawaii",
        "new hampshire",
        "maine",
        "rhode island",
        "montana",
        "delaware",
        "south dakota",
        "north dakota",
        "alaska",
        "vermont",
        "wyoming",
    ]

    # US state abbreviations (word boundary match only)
    us_state_abbrevs = [
        "ca",
        "ny",
        "tx",
        "fl",
        "wa",
        "il",
        "pa",
        "oh",
        "ga",
        "nc",
        "mi",
        "nj",
        "va",
        "tn",
        "az",
        "ma",
        "in",
        "md",
        "mo",
        "wi",
        "co",
        "mn",
        "sc",
        "al",
        "la",
        "ky",
        "or",
        "ok",
        "ct",
        "ut",
        "ia",
        "nv",
        "ar",
        "ms",
        "ks",
        "nm",
        "ne",
        "wv",
        "id",
        "hi",
        "nh",
        "me",
        "ri",
        "mt",
        "de",
        "sd",
        "nd",
        "ak",
        "vt",
        "wy",
    ]

    # Major US cities (simple substring match)
    us_cities = [
        "san francisco",
        "los angeles",
        "chicago",
        "houston",
        "phoenix",
        "philadelphia",
        "san antonio",
        "san diego",
        "dallas",
        "san jose",
        "austin",
        "jacksonville",
        "fort worth",
        "columbus",
        "charlotte",
        "detroit",
        "el paso",
        "memphis",
        "denver",
        "washington dc",
        "boston",
        "nashville",
        "baltimore",
        "portland",
        "milwaukee",
        "las vegas",
        "atlanta",
        "miami",
        "seattle",
        "new york city",
        "nyc",
    ]

    # EU countries and indicators
    eu_indicators = [
        "european union",
        "eu",
        "europe",
        "european",
        # EU countries
        "germany",
        "german",
        "france",
        "french",
        "italy",
        "italian",
        "spain",
        "spanish",
        "poland",
        "polish",
        "romania",
        "romanian",
        "netherlands",
        "dutch",
        "belgium",
        "belgian",
        "greece",
        "greek",
        "czech republic",
        "czech",
        "portugal",
        "portuguese",
        "sweden",
        "swedish",
        "hungary",
        "hungarian",
        "austria",
        "austrian",
        "belarus",
        "switzerland",
        "swiss",
        "bulgaria",
        "bulgarian",
        "serbia",
        "serbian",
        "denmark",
        "danish",
        "finland",
        "finnish",
        "slovakia",
        "slovak",
        "norway",
        "norwegian",
        "ireland",
        "irish",
        "croatia",
        "croatian",
        "bosnia",
        "albania",
        "lithuanian",
        "slovenia",
        "latvian",
        "estonia",
        "estonian",
        "moldova",
        "macedonia",
        "malta",
        "luxembourg",
        "cyprus",
        "iceland",
        "monaco",
        "montenegro",
        "liechtenstein",
        # Major EU cities
        "berlin",
        "madrid",
        "rome",
        "paris",
        "bucharest",
        "hamburg",
        "munich",
        "milan",
        "naples",
        "turin",
        "palermo",
        "genoa",
        "bologna",
        "florence",
        "barcelona",
        "valencia",
        "seville",
        "zaragoza",
        "málaga",
        "murcia",
        "palma",
        "bilbao",
        "alicante",
        "córdoba",
        "warsaw",
        "kraków",
        "łódź",
        "wrocław",
        "poznań",
        "gdańsk",
        "szczecin",
        "bydgoszcz",
        "lublin",
        "amsterdam",
        "rotterdam",
        "hague",
        "utrecht",
        "eindhoven",
        "tilburg",
        "groningen",
        "almere",
        "brussels",
        "antwerp",
        "ghent",
        "charleroi",
        "liège",
        "bruges",
        "athens",
        "thessaloniki",
        "prague",
        "brno",
        "ostrava",
        "lisbon",
        "porto",
        "stockholm",
        "gothenburg",
        "malmö",
        "budapest",
        "debrecen",
        "szeged",
        "vienna",
        "graz",
        "linz",
        "salzburg",
        "innsbruck",
        "zurich",
        "geneva",
        "basel",
        "bern",
        "lausanne",
        "sofia",
        "plovdiv",
        "varna",
        "belgrade",
        "novi sad",
        "copenhagen",
        "aarhus",
        "odense",
        "aalborg",
        "helsinki",
        "espoo",
        "tampere",
        "vantaa",
        "turku",
        "bratislava",
        "košice",
        "oslo",
        "bergen",
        "stavanger",
        "trondheim",
        "dublin",
        "cork",
        "limerick",
        "galway",
        "zagreb",
        "split",
        "rijeka",
        "reykjavik",
    ]

    # Check for US indicators using different matching strategies

    # 1. Check general US indicators (simple substring match)
    if any(indicator in location_lower for indicator in us_general_indicators):
        return True

    # 2. Check US state full names (simple substring match)
    if any(state in location_lower for state in us_state_names):
        return True

    # 3. Check US cities (simple substring match)
    if any(city in location_lower for city in us_cities):
        return True

    # 4. Check US state abbreviations (word boundary match only to avoid false positives)
    for abbrev in us_state_abbrevs:
        # Use word boundaries to ensure abbreviation appears as complete word
        pattern = r"\b" + re.escape(abbrev) + r"\b"
        if re.search(pattern, location_lower):
            return True

    # Check for EU indicators
    if any(indicator in location_lower for indicator in eu_indicators):
        return True

    return False
