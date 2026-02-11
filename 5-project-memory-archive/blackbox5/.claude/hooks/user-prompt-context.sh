#!/bin/bash
# UserPromptSubmit hook - adds context to user prompts
# Reads JSON from stdin, outputs JSON to stdout

# Read input
read -r input

# Return continue=true to allow prompt processing
# Can add systemMessage to inject context
echo '{"continue": true}'
exit 0
