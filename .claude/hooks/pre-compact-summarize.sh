#!/bin/bash
# PreCompact hook - runs before context compaction
# Reads JSON from stdin, outputs JSON to stdout

# Read input
read -r input

# Return continue=true to allow compaction to proceed
# Can save state here before compaction happens
echo '{"continue": true}'
exit 0
