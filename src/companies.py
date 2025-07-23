from scrapers import (
    greenhouse,
    lever,
    ashby,
    myworkdayjobs,
    myworkdaysite,
    icims,
    successfactors,
    nc2,
    jobvite,
    smartrecruiters,
    avature,
    netflix,
    spotify,
    uber,
    meta,
    google,
    wiz,
    apple,
    amazon,
    microsoft,
    hubspot,
    deloitte,
    qualcomm,
    linkedin,
    peloton,
    atlassian,
    github,
)

tier_1a = [
    {
        "name": "Meta",
        "formatted_name": "meta",
        "scraper": meta,
        "manually_verified": False,
    },
    {
        "name": "Google",
        "formatted_name": "google",
        "scraper": google,
        "manually_verified": False,
    },
    {
        "name": "LinkedIn",
        "formatted_name": "linkedin",
        "scraper": linkedin,
        "manually_verified": False,
    },
    {
        "name": "Uber",
        "formatted_name": "uber",
        "scraper": uber,
        "manually_verified": False,
    },
    # https://salesforce.wd12.myworkdayjobs.com/External_Career_Site
    {
        "name": "Salesforce",
        "formatted_name": "salesforce",
        "scraper": myworkdayjobs,
        "manually_verified": False,
    },
    {
        "name": "Stripe",
        "formatted_name": "stripe",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    # https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite
    {
        "name": "NVIDIA",
        "formatted_name": "nvidia",
        "scraper": myworkdayjobs,
        "manually_verified": False,
    },
]

tier_1b = [
    {
        "name": "Apple",
        "formatted_name": "apple",
        "scraper": apple,
        "manually_verified": False,
    },
    {
        "name": "Netflix",
        "formatted_name": "netflix",
        "scraper": netflix,
        "manually_verified": False,
    },
    {
        "name": "OpenAI",
        "formatted_name": "openai",
        "scraper": ashby,
        "manually_verified": False,
    },
    {
        "name": "Microsoft",
        "formatted_name": "microsoft",
        "scraper": microsoft,
        "manually_verified": False,
    },
    {
        "name": "Amazon",
        "formatted_name": "amazon",
        "scraper": amazon,
        "manually_verified": False,
    },
]

tier_2a = [
    {
        "name": "Snowflake",
        "formatted_name": "snowflake",
        "scraper": ashby,
        "manually_verified": False,
    },
    {
        "name": "Databricks",
        "formatted_name": "databricks",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    {
        "name": "Reddit",
        "formatted_name": "reddit",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    {
        "name": "Cloudflare",
        "formatted_name": "cloudflare",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    {
        "name": "Spotify",
        "formatted_name": "spotify",
        "scraper": spotify,
        "manually_verified": False,
    },
    {
        "name": "Roblox",
        "formatted_name": "roblox",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    {
        "name": "Plaid",
        "formatted_name": "plaid",
        "scraper": lever,
        "manually_verified": False,
    },
    {
        "name": "Notion",
        "formatted_name": "notion",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    {
        "name": "Duolingo",
        "formatted_name": "duolingo",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    {
        "name": "Brex",
        "formatted_name": "brex",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    {
        "name": "DataDog",
        "formatted_name": "datadog",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    {
        "name": "Okta",
        "formatted_name": "okta",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    {
        "name": "Anthropic",
        "formatted_name": "anthropic",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    # Note: Shopify hires on all teams on a rolling basis; scraper would be useless
    {
        "name": "Shopify",
        "formatted_name": "shopify",
        "scraper": "",
        "manually_verified": False,
    },
    {
        "name": "Splunk",
        "formatted_name": "splunk",
        "scraper": jobvite,
        "manually_verified": False,
    },
    {
        "name": "Ramp",
        "formatted_name": "ramp",
        "scraper": ashby,
        "manually_verified": False,
    },
    # https://crowdstrike.wd5.myworkdayjobs.com/crowdstrikecareers
    {
        "name": "CrowdStrike",
        "formatted_name": "crowdstrike",
        "scraper": myworkdayjobs,
        "manually_verified": False,
    },
    {
        "name": "Palo Alto Networks",
        "formatted_name": "paloaltonetworks2",
        "scraper": smartrecruiters,
        "manually_verified": False,
    },
    {
        "name": "Wiz",
        "formatted_name": "wiz",
        "scraper": wiz,
        "manually_verified": False,
    },
    {
        "name": "Elastic",
        "formatted_name": "elastic",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    {
        "name": "ServiceNow",
        "formatted_name": "servicenow",
        "scraper": smartrecruiters,
        "manually_verified": False,
    },
    # https://capitalone.wd12.myworkdayjobs.com/Capital_One
    {
        "name": "Capital One",
        "formatted_name": "capitalone",
        "scraper": myworkdayjobs,
        "manually_verified": False,
    },
    {
        "name": "Anduril Industries",
        "formatted_name": "andurilindustries",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    {
        "name": "Cohere",
        "formatted_name": "cohere",
        "scraper": ashby,
        "manually_verified": False,
    },
    # https://www.github.careers/careers-home/jobs?page=2
    {
        "name": "GitHub",
        "formatted_name": "githubinc",
        "scraper": github,
        "manually_verified": False,
    },
    {
        "name": "Affirm",
        "formatted_name": "affirm",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    {
        "name": "Rubrik",
        "formatted_name": "rubrik",
        "scraper": greenhouse,
        "manually_verified": False,
    },
]

tier_2b = [
    {
        "name": "AirBnB",
        "formatted_name": "airbnb",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    # https://www.atlassian.com/company/careers/all-jobs
    {
        "name": "Atlassian",
        "formatted_name": "apac-atlassian",
        "scraper": atlassian,
        "manually_verified": False,
    },
    {
        "name": "Twilio",
        "formatted_name": "twilio",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    # https://zillow.wd5.myworkdayjobs.com/Zillow_Group_External
    {
        "name": "Zillow",
        "formatted_name": "zillow",
        "scraper": myworkdayjobs,
        "manually_verified": False,
    },
    # https://etsy.wd5.myworkdayjobs.com/Etsy_Careers
    {
        "name": "Etsy",
        "formatted_name": "etsy",
        "scraper": myworkdayjobs,
        "manually_verified": False,
    },
    {
        "name": "Instacart",
        "formatted_name": "instacart",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    {
        "name": "Coursera",
        "formatted_name": "coursera",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    {
        "name": "MongoDB",
        "formatted_name": "mongodb",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    {
        "name": "Squarespace",
        "formatted_name": "squarespace",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    {
        "name": "Wayfair",
        "formatted_name": "wayfair",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    {
        "name": "Fastly",
        "formatted_name": "fastly",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    {
        "name": "NetApp",
        "formatted_name": "netapp",
        "scraper": successfactors,
        "manually_verified": False,
    },
    {
        "name": "Shield AI",
        "formatted_name": "shield ai",
        "scraper": lever,
        "manually_verified": False,
    },
    {
        "name": "Palantir",
        "formatted_name": "palantir",
        "scraper": lever,
        "manually_verified": False,
    },
    {
        "name": "Bloomberg",
        "formatted_name": "bloomberg",
        "scraper": avature,
        "manually_verified": False,
    },
    # https://cohesity.wd5.myworkdayjobs.com/Cohesity_Careers/
    {
        "name": "Cohesity",
        "formatted_name": "cohesity",
        "scraper": myworkdayjobs,
        "manually_verified": False,
    },
    # https://thoughtspot.wd5.myworkdayjobs.com/careers
    {
        "name": "ThoughtSpot",
        "formatted_name": "thoughtspot",
        "scraper": myworkdayjobs,
        "manually_verified": False,
    },
    {
        "name": "Postman",
        "formatted_name": "postman",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    {
        "name": "Freshworks",
        "formatted_name": "freshworks",
        "scraper": smartrecruiters,
        "manually_verified": False,
    },
    # https://redhat.wd5.myworkdayjobs.com/Jobs
    {
        "name": "Red Hat",
        "formatted_name": "redhat",
        "scraper": myworkdayjobs,
        "manually_verified": False,
    },
    {
        "name": "RunPod",
        "formatted_name": "runpod",
        "scraper": greenhouse,
        "manually_verified": False,
    },
]

tier_2c = [
    {
        "name": "Lyft",
        "formatted_name": "lyft",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    {
        "name": "Pinterest",
        "formatted_name": "pinterest",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    {
        "name": "DoorDash",
        "formatted_name": "doordashusa",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    {
        "name": "Robinhood",
        "formatted_name": "robinhood",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    {
        "name": "Peloton",
        "formatted_name": "peloton",
        "scraper": peloton,
        "manually_verified": False,
    },
    {
        "name": "Gusto",
        "formatted_name": "gusto",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    {
        "name": "Qualcomm",
        "formatted_name": "qualcomm",
        "scraper": qualcomm,
        "manually_verified": False,
    },
    {
        "name": "Asana",
        "formatted_name": "asana",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    # https://wd3.myworkdaysite.com/recruiting/takeaway/grubhubcareers
    {
        "name": "GrubHub",
        "formatted_name": "grubhub",
        "scraper": myworkdaysite,
        "manually_verified": False,
    },
    {
        "name": "HubSpot",
        "formatted_name": "hubspot",
        "scraper": hubspot,
        "manually_verified": False,
    },
    {
        "name": "Eventbrite",
        "formatted_name": "eventbriteinc",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    # https://uscareers-yelp.icims.com/jobs/search?ss=1
    {
        "name": "Yelp",
        "formatted_name": "uscareers-yelp",
        "scraper": icims,
        "manually_verified": False,
    },
    {
        "name": "IBM",
        "formatted_name": "ibm",
        "scraper": avature,
        "manually_verified": False,
    },
    # https://gartner.wd5.myworkdayjobs.com/en-US/ext
    {
        "name": "Gartner",
        "formatted_name": "gartner",
        "scraper": myworkdayjobs,
        "manually_verified": False,
    },
    {
        "name": "Riverbed",
        "formatted_name": "careers-riverbed",
        "scraper": icims,
        "manually_verified": False,
    },
    {
        "name": "Deloitte",
        "formatted_name": "deloitte",
        "scraper": deloitte,
        "manually_verified": False,
    },
    # https://globalhr.wd5.myworkdayjobs.com/REC_RTX_Ext_Gateway
    {
        "name": "Raytheon Technologies",
        "formatted_name": "globalhr",
        "scraper": myworkdayjobs,
        "manually_verified": False,
    },
    # https://gdit.wd5.myworkdayjobs.com/External_Career_Site
    {
        "name": "General Dynamics",
        "formatted_name": "gdit",
        "scraper": myworkdayjobs,
        "manually_verified": False,
    },
    {
        "name": "L3Harris",
        "formatted_name": "l3harris",
        "scraper": nc2,
        "manually_verified": False,
    },
    {
        "name": "Mattermost",
        "formatted_name": "mattermost",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    {
        "name": "Canonical",
        "formatted_name": "canonical",
        "scraper": greenhouse,
        "manually_verified": False,
    },
    {
        "name": "Zest AI",
        "formatted_name": "zestai",
        "scraper": greenhouse,
        "manually_verified": False,
    },
]
