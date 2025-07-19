# Job search configuration

# Rate limiting configuration
REQUEST_DELAY_SECONDS = 1  # Delay between requests to be respectful
TIMEOUT_SECONDS = 10  # Request timeout

# Keywords to include in job searches
INCLUDE_KEYWORDS = [
    # The first three terms here are expected to catch all relevant jobs
    # Therefore they are frontloaded, to speed up scraping script
    "Engineer",
    "Developer",
    "Software",
    # The remaining terms are unneeded but may help catch any oddball job titles
    "Backend",
    "Full",  # Covers various spellings of full-stack
    "Python",
    "Go",
    "JavaScript",
    "Node.js",
    "Web",
    "Infrastructure",
    "DevOps",
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
    "3",
    "4",
    "5",
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
]

# Output configuration
OUTPUT_TO_CONSOLE = True
OUTPUT_TO_FILES_BY_COMPANY = True
OUTPUT_TO_FILES_BY_SCRAPE = True
LOG_LEVEL = "INFO"
