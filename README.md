# Job Scraper

A Python-based job scraper that automatically pulls recent job postings from various company career pages and job platforms.

## Features

- **Modular Design**: Separate scrapers for different platforms (Lever, Greenhouse, Ashby, etc.)
- **Duplicate Prevention**: Tracks previously found jobs to avoid duplicates
- **Configurable Filtering**: Keyword-based filtering for job titles
- **Multiple Output Formats**: Console output and log files
- **Company Organization**: Companies organized by tiers for prioritized scraping
- **Rate Limiting**: Respectful scraping with built-in delays

## Quick Start

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the scraper**:

   ```bash
   python run_scraper.py
   ```

3. **Check results**:
   - Console output shows jobs in real-time
   - Log files are saved in `src/search_results/`
   - Summary files are generated with each run

## Configuration

### Keywords (src/config.py)

- **INCLUDE_KEYWORDS**: Jobs must match at least one of these keywords
- **EXCLUDE_KEYWORDS**: Jobs are filtered out if they match any of these keywords

### Companies (src/companies.py)

- Companies are organized into tiers (tier_1a, tier_1b, tier_2a, tier_2b, tier_2c)
- Each company has a `name`, `formatted_name`, and `scraper` type

### Supported Platforms

- **Lever**: `lever`
- **Greenhouse**: `greenhouse`
- **Ashby**: `ashby`
- **Custom scrapers**: `netflix`, `spotify`, `uber`, `servicenow`

## Project Structure

```
src/
├── main.py              # Main orchestrator
├── scrapers.py          # Platform-specific scrapers
├── companies.py         # Company lists and configuration
├── config.py            # Keywords and filters
├── output.py            # Output formatting
├── utils.py             # Utility functions
├── jobs_found.txt       # Duplicate tracking
└── search_results/      # Output files
```

## Output Format

Jobs are displayed in the format:

```
Company --- Job Title
https://link.to/job
```

## Automation

The scraper can be run automatically via cron. Example crontab entry to run daily at 9 AM:

```bash
0 9 * * * /path/to/python /path/to/job-scraper/run_scraper.py
```

## Adding New Companies

1. Add the company to the appropriate tier in `src/companies.py`
2. Specify the correct scraper type:
   - `"greenhouse"` for Greenhouse-based companies
   - `"lever"` for Lever-based companies
   - `"ashby"` for Ashby-based companies
   - Custom scraper name for companies with custom implementations

## License

MIT License
