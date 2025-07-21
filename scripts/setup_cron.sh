#!/bin/bash

# Setup script for job scraper cron job
# This script helps you configure the cron job for automated job scraping

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
CRON_SCRIPT="$SCRIPT_DIR/run_job_scraper_cron.sh"

echo "🔧 Job Scraper Cron Setup"
echo "=========================="
echo

# Verify the cron script exists and is executable
if [ ! -f "$CRON_SCRIPT" ]; then
    echo "❌ Cron script not found at: $CRON_SCRIPT"
    exit 1
fi

if [ ! -x "$CRON_SCRIPT" ]; then
    echo "🔒 Making cron script executable..."
    chmod +x "$CRON_SCRIPT"
fi

# Show current cron jobs
echo "📋 Current cron jobs:"
crontab -l 2>/dev/null || echo "No current cron jobs found."
echo

# Suggest cron schedule options
echo "⏰ Choose a schedule for your job scraper:"
echo "1. Every 2 hours: 0 */2 * * *"
echo "2. Every 3 hours: 0 */3 * * *"
echo "3. Every 4 hours: 0 */4 * * *"
echo "4. Every 6 hours: 0 */6 * * *"
echo "5. Twice daily (9am, 5pm): 0 9,17 * * *"
echo "6. Custom schedule"
echo

echo "Enter your choice (1-6):"
read -r schedule_choice

case $schedule_choice in
    1) CRON_SCHEDULE="0 */2 * * *" ;;
    2) CRON_SCHEDULE="0 */3 * * *" ;;
    3) CRON_SCHEDULE="0 */4 * * *" ;;
    4) CRON_SCHEDULE="0 */6 * * *" ;;
    5) CRON_SCHEDULE="0 9,17 * * *" ;;
    6) 
        echo "Enter your custom cron schedule (e.g., '0 */3 * * *'):"
        read -r CRON_SCHEDULE
        ;;
    *)
        echo "❌ Invalid choice. Defaulting to every 3 hours."
        CRON_SCHEDULE="0 */3 * * *"
        ;;
esac

# Create the cron job entry
CRON_ENTRY="$CRON_SCHEDULE $CRON_SCRIPT"

echo
echo "📝 Proposed cron job entry:"
echo "$CRON_ENTRY"
echo

echo "🔧 Add this cron job? (y/n)"
read -r add_response
if [[ "$add_response" =~ ^[Yy]$ ]]; then
    # Add to cron
    (crontab -l 2>/dev/null || true; echo "$CRON_ENTRY") | crontab -
    echo "✅ Cron job added successfully!"
    echo
    echo "📋 Updated cron jobs:"
    crontab -l
else
    echo "ℹ️  Cron job not added. You can add it manually with:"
    echo "   crontab -e"
    echo "   Then add this line: $CRON_ENTRY"
fi

echo
echo "📁 Logs will be stored in: $PROJECT_DIR/logs/"
echo "💡 To view recent logs: ls -la $PROJECT_DIR/logs/"
echo "🗑️  To remove the cron job later: crontab -e (then delete the line)"
echo
echo "🎉 Setup complete! Your job scraper will now run automatically." 