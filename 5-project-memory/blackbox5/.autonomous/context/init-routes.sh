#!/bin/bash
# init-routes.sh - Initialize routes.yaml from template
# Usage: ./init-routes.sh [PROJECT_NAME] [PROJECT_PATH]

set -e

# Default values
DEFAULT_PROJECT_NAME="blackbox5"
DEFAULT_PROJECT_PATH="/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5"

# Use provided arguments or defaults
PROJECT_NAME="${1:-$DEFAULT_PROJECT_NAME}"
PROJECT_PATH="${2:-$DEFAULT_PROJECT_PATH}"
PROJECT_NAME_UPPER=$(echo "$PROJECT_NAME" | tr '[:lower:]' '[:upper:]')

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_FILE="$SCRIPT_DIR/routes.yaml.template"
OUTPUT_FILE="$SCRIPT_DIR/routes.yaml"

# Check if template exists
if [[ ! -f "$TEMPLATE_FILE" ]]; then
    echo "Error: Template file not found at $TEMPLATE_FILE"
    exit 1
fi

# Create backup of existing routes.yaml if it exists
if [[ -f "$OUTPUT_FILE" ]]; then
    BACKUP_FILE="$OUTPUT_FILE.backup.$(date +%Y%m%d_%H%M%S)"
    cp "$OUTPUT_FILE" "$BACKUP_FILE"
    echo "Created backup: $BACKUP_FILE"
fi

# Replace placeholders in template
sed -e "s|{{PROJECT_NAME}}|$PROJECT_NAME|g" \
    -e "s|{{PROJECT_NAME_UPPER}}|$PROJECT_NAME_UPPER|g" \
    -e "s|{{PROJECT_PATH}}|$PROJECT_PATH|g" \
    "$TEMPLATE_FILE" > "$OUTPUT_FILE"

echo "Successfully generated routes.yaml"
echo "  Project Name: $PROJECT_NAME"
echo "  Project Path: $PROJECT_PATH"
echo "  Output: $OUTPUT_FILE"
