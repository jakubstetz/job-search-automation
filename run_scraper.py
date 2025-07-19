#!/usr/bin/env python3
"""
Simple run script for the job scraper.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Import and run the main function
from main import main

if __name__ == "__main__":
    main()
