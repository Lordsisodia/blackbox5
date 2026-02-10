#!/bin/bash
#
# BlackBox5 Autonomous Self-Improvement Loop Wrapper
# Called by cron every 30 minutes
#

set -e

# Configuration
BB5_DIR="/opt/blackbox5"
SCRIPT_DIR="${BB5_DIR}/bin/self-improvement"
PYTHON_SCRIPT="${SCRIPT_DIR}/run-improvement-loop.py"
LOG_DIR="${BB5_DIR}/.autonomous/self-improvement/logs"

# Environment
export BB5_DIR="${BB5_DIR}"
export PYTHONPATH="${BB5_DIR}:${BB5_DIR}/engine:${PYTHONPATH}"

# Ensure log directory exists
mkdir -p "${LOG_DIR}"

# Run the improvement loop
cd "${BB5_DIR}"

# Execute Python script
python3 "${PYTHON_SCRIPT}" >> "${LOG_DIR}/wrapper.log" 2>&1

exit_code=$?

# Check exit code
if [ $exit_code -ne 0 ]; then
    echo "[$(date -u +"%Y-%m-%d %H:%M:%S UTC")] ERROR: Self-improvement loop failed with exit code ${exit_code}" >> "${LOG_DIR}/wrapper-errors.log"
fi

exit $exit_code
