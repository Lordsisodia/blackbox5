#!/bin/bash
#
# Setup cron job for automated run archival
# Run this script to install the weekly archival schedule
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARCHIVE_SCRIPT="${SCRIPT_DIR}/archive-runs.sh"
CRON_LOG="${HOME}/.blackbox5/5-project-memory/.archive-cron.log"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Check if archive script exists
if [[ ! -f "$ARCHIVE_SCRIPT" ]]; then
    echo "Error: Archive script not found at $ARCHIVE_SCRIPT"
    exit 1
fi

# Make sure archive script is executable
chmod +x "$ARCHIVE_SCRIPT"

# Create cron job
# Run every Sunday at 2:00 AM
CRON_JOB="0 2 * * 0 ${ARCHIVE_SCRIPT} archive >> ${CRON_LOG} 2>&1"

log "Setting up archive cron job..."
log "Schedule: Every Sunday at 2:00 AM"
log "Log file: ${CRON_LOG}"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "archive-runs.sh"; then
    log "Cron job already exists. Updating..."
    # Remove existing job
    crontab -l 2>/dev/null | grep -v "archive-runs.sh" | crontab -
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

log_success "Cron job installed successfully"
echo ""
echo "Current crontab:"
crontab -l | grep "archive-runs" || echo "  (not found)"
echo ""
echo "To remove the cron job, run:"
echo "  crontab -l | grep -v archive-runs | crontab -"
echo ""
echo "To run archival manually:"
echo "  ${ARCHIVE_SCRIPT} archive"
