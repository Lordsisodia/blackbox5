#!/bin/bash
#
# YouTube Scraper Cron Configuration
# This script sets up cron jobs for automated YouTube scraping
#
# Usage:
#   ./cron-config.sh install    - Install cron jobs
#   ./cron-config.sh uninstall  - Remove cron jobs
#   ./cron-config.sh status     - Show current cron jobs
#

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRAPER_SCRIPT="$SCRIPT_DIR/scraper.py"
LOG_DIR="$SCRIPT_DIR/logs"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Create log directory
mkdir -p "$LOG_DIR"

# Function to print colored output
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to check if scraper exists
check_scraper() {
    if [ ! -f "$SCRAPER_SCRIPT" ]; then
        print_status "$RED" "Error: Scraper script not found at $SCRAPER_SCRIPT"
        exit 1
    fi

    if [ ! -x "$SCRAPER_SCRIPT" ]; then
        print_status "$YELLOW" "Making scraper script executable..."
        chmod +x "$SCRAPER_SCRIPT"
    fi
}

# Function to install cron jobs
install_cron() {
    print_status "$GREEN" "Installing YouTube scraper cron jobs..."

    check_scraper

    # Get current crontab
    local current_cron=$(crontab -l 2>/dev/null || echo "")

    # Check if already installed
    if echo "$current_cron" | grep -q "youtube-scraper"; then
        print_status "$YELLOW" "Cron jobs already installed. Run '$0 status' to view."
        exit 0
    fi

    # Add cron jobs
    # Run every 10 minutes
    local cron_entry="*/10 * * * * cd $SCRIPT_DIR && /usr/bin/python3 $SCRAPER_SCRIPT --once --config $SCRIPT_DIR/config/config.yaml >> $LOG_DIR/cron.log 2>&1"

    # Append to crontab
    (echo "$current_cron"; echo "# YouTube Scraper - Run every 10 minutes"; echo "$cron_entry") | crontab -

    print_status "$GREEN" "✓ Cron job installed successfully!"
    print_status "$GREEN" "  Schedule: Every 10 minutes"
    print_status "$GREEN" "  Log: $LOG_DIR/cron.log"
    print_status "$GREEN" ""
    print_status "$GREEN" "To view cron jobs, run: $0 status"
    print_status "$GREEN" "To uninstall, run: $0 uninstall"
}

# Function to uninstall cron jobs
uninstall_cron() {
    print_status "$YELLOW" "Removing YouTube scraper cron jobs..."

    # Get current crontab
    local current_cron=$(crontab -l 2>/dev/null || echo "")

    # Filter out youtube-scraper entries
    local new_cron=$(echo "$current_cron" | grep -v "youtube-scraper" | grep -v "^# YouTube Scraper")

    # Write new crontab
    if [ -n "$new_cron" ]; then
        echo "$new_cron" | crontab -
    else
        crontab -r 2>/dev/null || true
    fi

    print_status "$GREEN" "✓ Cron jobs removed successfully!"
}

# Function to show cron status
show_status() {
    print_status "$GREEN" "Current cron jobs for YouTube scraper:"
    echo ""

    local cron_output=$(crontab -l 2>/dev/null | grep -A1 "youtube-scraper" || echo "No cron jobs installed")

    if echo "$cron_output" | grep -q "No cron jobs"; then
        print_status "$YELLOW" "No YouTube scraper cron jobs found."
        echo ""
        echo "To install cron jobs, run: $0 install"
    else
        echo "$cron_output"
    fi

    echo ""
    echo "Recent cron logs:"
    echo "----------------"

    if [ -f "$LOG_DIR/cron.log" ]; then
        tail -20 "$LOG_DIR/cron.log"
    else
        print_status "$YELLOW" "No cron log file found at $LOG_DIR/cron.log"
    fi
}

# Function to test cron job manually
test_run() {
    print_status "$GREEN" "Running scraper manually (as cron would)..."
    echo ""

    cd "$SCRIPT_DIR" || exit 1

    /usr/bin/python3 "$SCRAPER_SCRIPT" --once --config "$SCRIPT_DIR/config/config.yaml"

    local exit_code=$?

    echo ""
    if [ $exit_code -eq 0 ]; then
        print_status "$GREEN" "✓ Test run completed successfully!"
    else
        print_status "$RED" "✗ Test run failed with exit code: $exit_code"
    fi
}

# Function to show usage
show_usage() {
    echo "YouTube Scraper Cron Configuration"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  install    - Install cron jobs for automated scraping"
    echo "  uninstall  - Remove cron jobs"
    echo "  status     - Show current cron jobs and recent logs"
    echo "  test       - Run scraper manually (test cron setup)"
    echo "  help       - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 install"
    echo "  $0 status"
    echo "  $0 test"
    echo ""
}

# Main script logic
case "${1:-help}" in
    install)
        install_cron
        ;;
    uninstall)
        uninstall_cron
        ;;
    status)
        show_status
        ;;
    test)
        test_run
        ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        print_status "$RED" "Unknown command: $1"
        echo ""
        show_usage
        exit 1
        ;;
esac
