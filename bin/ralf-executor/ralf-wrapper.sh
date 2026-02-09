#!/bin/bash
# RALF Wrapper: Properly drops privileges to run ralf-core.sh
# This avoids the systemd "root/sudo" detection issue with Claude Code

set -e

# Export environment variables for su
export BB5_DIR="${BB5_DIR:-/opt/blackbox5}"
export ANTHROPIC_AUTH_TOKEN="${ANTHROPIC_AUTH_TOKEN}"
export ANTHROPIC_BASE_URL="${ANTHROPIC_BASE_URL}"
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS="${CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS}"
export BB5_MODE="${BB5_MODE}"
export CLAUDE_MODEL="${CLAUDE_MODEL}"

# Run the actual ralf-core.sh as bb5-runner using su with preserved environment
# This ensures a clean environment that Claude Code accepts
exec su -p bb5-runner -c 'cd /opt/blackbox5 && /opt/blackbox5/bin/ralf-executor/ralf-core.sh'
