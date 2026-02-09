#!/bin/bash
# RALF Wrapper: Properly drops privileges to run ralf-core.sh
# This avoids the systemd "root/sudo" detection issue with Claude Code

set -e

# Run the actual ralf-core.sh as bb5-runner using su
# This ensures a clean environment that Claude Code accepts
exec su - bb5-runner -c 'cd /opt/blackbox5 && /opt/blackbox5/bin/ralf-executor/ralf-core.sh'
