# Job search configuration

# Rate limiting configuration
REQUEST_DELAY_SECONDS = 3  # Delay between requests to be respectful
TIMEOUT_SECONDS = 10  # Request timeout

# Keywords to include in job searches
INCLUDE_KEYWORDS = [
    # The first four terms here are expected to catch all relevant jobs
    # Therefore they are frontloaded, to speed up scraping script
    "Engineer",
    "Developer",
    "Software",
    "MTS",
    "Technical Staff"
    # The remaining terms are unneeded but may help catch any oddball job titles
    "Backend",
    "Stack",  # Covers various spellings of full-stack
    "Python",
    "Go",
    "JavaScript",
    "Node.js",
    "Web",
    "Infrastructure",
    "DevOps",
    "Systems",
    "Reliability",  # e.g. Site Reliability Engineer
    "Platform",  # e.g. Platform Engineer
    "Data",
    "Machine Learning",
    "ML",
    "AI",
    "SRE",
    "Cloud Engineer",
    "API",
    "Microservice",
    "Distributed",
]

# Keywords to exclude from job searches
EXCLUDE_KEYWORDS = [
    # Filter out senior and managerial roles
    "Senior",
    "Staff",
    "III",
    "IV",
    "V",
    "Experienced",
    "Principal",
    "Lead",
    "Manager",
    "Dir",  # e.g. Director
    "VP",
    "Head",
    "Chief",
    "Sr",
    # Filter out roles in areas that are definitely out of scope
    "Ambassador",
    "Solutions Architect",
    "Analyst",
    "Technical Support",
    "Partner",
    "Security",
    "Hardware",
    "Mobile",
    "iOS",
    "Research",
    "Sales",
    "Scientist",
    "Trainer",
    "Solutions Engineer",
    "Design",
    "Firmware",
    "Control Systems",
    "Conductor",
    "Electrical",
    "Mechanical",
    "FGPA",
    "Field",
    "Power",
    "Energy",
    "Propulsion",
    "Radar",
    "Robotics",
    "Sustainment",
    "Motion",
    "Fluid",
    "Manufacturing",
    "Thermal",
    "Telecom",
    "Structural",
    "Material",
    "Industrial",
    "Aerospace",
    "Sourcing",
    "Perception",
    "Vision",
    "Administrator",
    "Forward Deployed",
]

# Required URL details for companies using Workday ATS (specifically myworkdayjobs)
# These datacenter IDs and final path segments were found by manually checking each company's job board
MYWORKDAYJOBS_URL_DETAILS = {
    "salesforce": {"datacenter_id": "12", "final_path_segment": "External_Career_Site"},
    "crowdstrike": {"datacenter_id": "5", "final_path_segment": "crowdstrikecareers"},
    "capitalone": {"datacenter_id": "12", "final_path_segment": "Capital_One"},
    "zillow": {"datacenter_id": "5", "final_path_segment": "Zillow_Group_External"},
    "etsy": {"datacenter_id": "5", "final_path_segment": "Etsy_Careers"},
    "cohesity": {"datacenter_id": "5", "final_path_segment": "Cohesity_Careers/"},
    "thoughtspot": {"datacenter_id": "5", "final_path_segment": "careers"},
    "redhat": {"datacenter_id": "5", "final_path_segment": "Jobs"},
    "gartner": {"datacenter_id": "5", "final_path_segment": "en-US/ext"},
    "globalhr": {  # Raytheon Technologies
        "datacenter_id": "5",
        "final_path_segment": "REC_RTX_Ext_Gateway",
    },
    "gdit": {  # General Dynamics
        "datacenter_id": "5",
        "final_path_segment": "External_Career_Site",
    },
    "nvidia": {
        "datacenter_id": "5",
        "final_path_segment": "NVIDIAExternalCareerSite",
    },
}

# Output configuration
OUTPUT_TO_CONSOLE = True
OUTPUT_TO_FILES_BY_COMPANY = True
OUTPUT_TO_FILES_BY_SCRAPE = True
LOG_LEVEL = "INFO"
