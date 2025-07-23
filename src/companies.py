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
)

tier_1a = [
    {"name": "Meta", "formatted_name": "meta", "scraper": meta},
    {"name": "Google", "formatted_name": "google", "scraper": google},
    {"name": "LinkedIn", "formatted_name": "linkedin", "scraper": linkedin},
    {"name": "Uber", "formatted_name": "uber", "scraper": uber},
    # https://salesforce.wd12.myworkdayjobs.com/External_Career_Site
    {"name": "Salesforce", "formatted_name": "salesforce", "scraper": myworkdayjobs},
    {"name": "Stripe", "formatted_name": "stripe", "scraper": greenhouse},
    # https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite
    {"name": "NVIDIA", "formatted_name": "nvidia", "scraper": myworkdayjobs},
]

tier_1b = [
    {"name": "Apple", "formatted_name": "apple", "scraper": apple},
    {"name": "Netflix", "formatted_name": "netflix", "scraper": netflix},
    {"name": "OpenAI", "formatted_name": "openai", "scraper": ashby},
    {"name": "Microsoft", "formatted_name": "microsoft", "scraper": microsoft},
    {"name": "Amazon", "formatted_name": "amazon", "scraper": amazon},
]

tier_2a = [
    {"name": "Snowflake", "formatted_name": "snowflake", "scraper": ashby},
    {"name": "Databricks", "formatted_name": "databricks", "scraper": greenhouse},
    {"name": "Reddit", "formatted_name": "reddit", "scraper": greenhouse},
    {"name": "Cloudflare", "formatted_name": "cloudflare", "scraper": greenhouse},
    {"name": "Spotify", "formatted_name": "spotify", "scraper": spotify},
    {"name": "Roblox", "formatted_name": "roblox", "scraper": greenhouse},
    {"name": "Plaid", "formatted_name": "plaid", "scraper": lever},
    {"name": "Notion", "formatted_name": "notion", "scraper": greenhouse},
    {"name": "Duolingo", "formatted_name": "duolingo", "scraper": greenhouse},
    {"name": "Brex", "formatted_name": "brex", "scraper": greenhouse},
    {"name": "DataDog", "formatted_name": "datadog", "scraper": greenhouse},
    {"name": "Okta", "formatted_name": "okta", "scraper": greenhouse},
    {"name": "Anthropic", "formatted_name": "anthropic", "scraper": greenhouse},
    # Note: Shopify hires on all teams on a rolling basis; scraper would be useless
    {"name": "Shopify", "formatted_name": "shopify", "scraper": ""},
    {"name": "Splunk", "formatted_name": "splunk", "scraper": jobvite},
    {"name": "Ramp", "formatted_name": "ramp", "scraper": ashby},
    # https://crowdstrike.wd5.myworkdayjobs.com/crowdstrikecareers
    {"name": "CrowdStrike", "formatted_name": "crowdstrike", "scraper": myworkdayjobs},
    {
        "name": "Palo Alto Networks",
        "formatted_name": "paloaltonetworks2",
        "scraper": smartrecruiters,
    },
    {"name": "Wiz", "formatted_name": "wiz", "scraper": wiz},
    {"name": "Elastic", "formatted_name": "elastic", "scraper": greenhouse},
    {"name": "ServiceNow", "formatted_name": "servicenow", "scraper": smartrecruiters},
    # https://capitalone.wd12.myworkdayjobs.com/Capital_One
    {"name": "Capital One", "formatted_name": "capitalone", "scraper": myworkdayjobs},
    {
        "name": "Anduril Industries",
        "formatted_name": "andurilindustries",
        "scraper": greenhouse,
    },
    {"name": "Cohere", "formatted_name": "cohere", "scraper": ashby},
    # https://careers-githubinc.icims.com/
    {"name": "GitHub", "formatted_name": "githubinc", "scraper": icims},
    {"name": "Affirm", "formatted_name": "affirm", "scraper": greenhouse},
    {"name": "Rubrik", "formatted_name": "rubrik", "scraper": greenhouse},
]

tier_2b = [
    {"name": "AirBnB", "formatted_name": "airbnb", "scraper": greenhouse},
    # https://globalcareers-atlassian.icims.com/
    {"name": "Atlassian", "formatted_name": "apac-atlassian", "scraper": icims},
    {"name": "Twilio", "formatted_name": "twilio", "scraper": greenhouse},
    # https://zillow.wd5.myworkdayjobs.com/Zillow_Group_External
    {"name": "Zillow", "formatted_name": "zillow", "scraper": myworkdayjobs},
    # https://etsy.wd5.myworkdayjobs.com/Etsy_Careers
    {"name": "Etsy", "formatted_name": "etsy", "scraper": myworkdayjobs},
    {"name": "Instacart", "formatted_name": "instacart", "scraper": greenhouse},
    {"name": "Coursera", "formatted_name": "coursera", "scraper": greenhouse},
    {"name": "MongoDB", "formatted_name": "mongodb", "scraper": greenhouse},
    {"name": "Squarespace", "formatted_name": "squarespace", "scraper": greenhouse},
    {"name": "Wayfair", "formatted_name": "wayfair", "scraper": greenhouse},
    {"name": "Fastly", "formatted_name": "fastly", "scraper": greenhouse},
    {"name": "NetApp", "formatted_name": "netapp", "scraper": successfactors},
    {"name": "Shield AI", "formatted_name": "shield ai", "scraper": lever},
    {"name": "Palantir", "formatted_name": "palantir", "scraper": lever},
    {"name": "Bloomberg", "formatted_name": "bloomberg", "scraper": avature},
    # https://cohesity.wd5.myworkdayjobs.com/Cohesity_Careers/
    {"name": "Cohesity", "formatted_name": "cohesity", "scraper": myworkdayjobs},
    # https://thoughtspot.wd5.myworkdayjobs.com/careers
    {"name": "ThoughtSpot", "formatted_name": "thoughtspot", "scraper": myworkdayjobs},
    {"name": "Postman", "formatted_name": "postman", "scraper": greenhouse},
    {"name": "Freshworks", "formatted_name": "freshworks", "scraper": smartrecruiters},
    # https://redhat.wd5.myworkdayjobs.com/Jobs
    {"name": "Red Hat", "formatted_name": "redhat", "scraper": myworkdayjobs},
    {"name": "RunPod", "formatted_name": "runpod", "scraper": greenhouse},
]

tier_2c = [
    {"name": "Lyft", "formatted_name": "lyft", "scraper": greenhouse},
    {"name": "Pinterest", "formatted_name": "pinterest", "scraper": greenhouse},
    {"name": "DoorDash", "formatted_name": "doordashusa", "scraper": greenhouse},
    {"name": "Robinhood", "formatted_name": "robinhood", "scraper": greenhouse},
    {"name": "Peloton", "formatted_name": "peloton", "scraper": peloton},
    {"name": "Gusto", "formatted_name": "gusto", "scraper": greenhouse},
    {"name": "Qualcomm", "formatted_name": "qualcomm", "scraper": qualcomm},
    {"name": "Asana", "formatted_name": "asana", "scraper": greenhouse},
    # https://wd3.myworkdaysite.com/recruiting/takeaway/grubhubcareers
    {"name": "GrubHub", "formatted_name": "grubhub", "scraper": myworkdaysite},
    {"name": "HubSpot", "formatted_name": "hubspot", "scraper": hubspot},
    {"name": "Eventbrite", "formatted_name": "eventbriteinc", "scraper": greenhouse},
    # uscareers-yelp.icims.com/
    {"name": "Yelp", "formatted_name": "yelp", "scraper": icims},
    {"name": "IBM", "formatted_name": "ibm", "scraper": avature},
    # https://gartner.wd5.myworkdayjobs.com/en-US/ext
    {"name": "Gartner", "formatted_name": "gartner", "scraper": myworkdayjobs},
    # https://careers-riverbed.icims.com/
    {"name": "Riverbed", "formatted_name": "riverbed", "scraper": icims},
    {"name": "Deloitte", "formatted_name": "deloitte", "scraper": deloitte},
    # https://globalhr.wd5.myworkdayjobs.com/REC_RTX_Ext_Gateway
    {
        "name": "Raytheon Technologies",
        "formatted_name": "globalhr",
        "scraper": myworkdayjobs,
    },
    # https://gdit.wd5.myworkdayjobs.com/External_Career_Site
    {
        "name": "General Dynamics",
        "formatted_name": "gdit",
        "scraper": myworkdayjobs,
    },
    {"name": "L3Harris", "formatted_name": "l3harris", "scraper": nc2},
    {"name": "Mattermost", "formatted_name": "mattermost", "scraper": greenhouse},
    {"name": "Canonical", "formatted_name": "canonical", "scraper": greenhouse},
    {"name": "Zest AI", "formatted_name": "zestai", "scraper": greenhouse},
]
