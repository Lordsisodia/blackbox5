#!/bin/bash
# DEPRECATED: Use run-tests.sh instead
# This script is kept for backward compatibility

echo "WARNING: run_tests.sh is deprecated. Use run-tests.sh instead." >&2
exec "$(dirname "$0")/run-tests.sh" "$@"
