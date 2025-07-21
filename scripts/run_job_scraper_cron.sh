#!/bin/bash

# Job Scraper Cron Runner
# This script handles running the job scraper in a cron environment
# with proper logging and error handling.

# Set strict error handling
set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$PROJECT_DIR/logs"
TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Log files
CRON_LOG="$LOG_DIR/cron_${TIMESTAMP}.log"
ERROR_LOG="$LOG_DIR/cron_error_${TIMESTAMP}.log"

# Function to log with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$CRON_LOG"
}

# Function to log errors
log_error() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1" >> "$ERROR_LOG"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1" >> "$CRON_LOG"
}

# Start logging
log "=== Job Scraper Cron Job Started ==="
log "Project directory: $PROJECT_DIR"
log "Log directory: $LOG_DIR"

# Change to project directory
cd "$PROJECT_DIR"
log "Changed to project directory: $(pwd)"

# Set up PATH to ensure Python and other tools are available
export PATH="/usr/local/bin:/usr/bin:/bin:$HOME/.local/bin:$PATH"

# Check if we're in a virtual environment or if we should create/activate one
if [ -d "venv" ]; then
    log "Activating virtual environment..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    log "Activating virtual environment..."
    source .venv/bin/activate
else
    log "No virtual environment found, using system Python"
fi

# Verify Python and required modules are available
if ! command -v python3 &> /dev/null; then
    log_error "python3 not found in PATH"
    exit 1
fi

log "Using Python: $(which python3)"
log "Python version: $(python3 --version)"

# Check if requirements are satisfied (optional check)
if [ -f "requirements.txt" ]; then
    log "Checking dependencies..."
    python3 -c "import requests, bs4" 2>/dev/null || {
        log_error "Required dependencies not available. Please install: pip install -r requirements.txt"
        exit 1
    }
fi

# Run the scraper and capture both stdout and stderr
log "Starting job scraper..."
if python3 run_scraper.py >> "$CRON_LOG" 2>> "$ERROR_LOG"; then
    log "Job scraper completed successfully"
    
    # Clean up old log files (keep last 30 days)
    log "Cleaning up old log files..."
    find "$LOG_DIR" -name "cron_*.log" -mtime +30 -delete 2>/dev/null || true
    
else
    RETURN_CODE=$?
    log_error "Job scraper failed with return code: $RETURN_CODE"
    
    # If there's an error, you might want to send an email or notification
    # Uncomment and modify the line below if you want email notifications
    # echo "Job scraper failed. Check logs at $ERROR_LOG" | mail -s "Job Scraper Failed" your-email@example.com
    
    exit $RETURN_CODE
fi

log "=== Job Scraper Cron Job Completed ===" 