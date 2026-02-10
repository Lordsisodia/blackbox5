#!/bin/bash
# RALF Wrapper: Properly drops privileges to run ralf-core.sh
# This avoids the systemd "root/sudo" detection issue with Claude Code

set -e

# Run the actual ralf-core.sh as bb5-runner using su
# -l (login) ensures proper environment including HOME directory
# This ensures Claude Code finds ~/.claude/settings.json
exec su -l bb5-runner -c 'cd /opt/blackbox5 && BB5_DIR=/opt/blackbox5 BB5_MODE=autonomous /opt/blackbox5/bin/ralf-executor/ralf-core.sh'
