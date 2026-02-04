#!/bin/bash
# SessionEnd hook - updates context on session end
# Reads JSON from stdin, outputs JSON to stdout

# Read input (for logging/debugging if needed)
read -r input

# Always return success - this hook is informational
# Exit code 0 with valid JSON allows session to end normally
echo '{"continue": true}'
exit 0
