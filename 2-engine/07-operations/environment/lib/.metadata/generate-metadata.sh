#!/usr/bin/env bash

# Metadata Template Generator
# Generates metadata.yaml files for Blackbox5 artifacts

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB_DIR="$(dirname "$SCRIPT_DIR")"
SCHEMA_FILE="$LIB_DIR/../../03-knowledge/storage/brain/metadata/schema.yaml"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Artifact types
ARTIFACT_TYPES=("agent" "skill" "plan" "library" "script" "template" "document" "test" "config" "module" "framework" "tool" "workspace" "example")

# Phases
PHASES=(1 2 3 4)

# Layers
LAYERS=("intelligence" "execution" "testing" "documentation" "system" "planning" "workspace")

# Status values
STATUS_VALUES=("active" "deprecated" "archived" "experimental" "beta" "development")

# Stability levels
STABILITY_LEVELS=("high" "medium" "low")

# Relationship types
RELATIONSHIP_TYPES=("implements" "documents" "tests" "uses" "parallel" "extends" "refines" "deprecates" "integrates" "complements" "manages")

show_help() {
    cat << EOF
${BLUE}Metadata Template Generator${NC}

Generates metadata.yaml templates for Blackbox5 artifacts following the AgentMD schema.

${YELLOW}Usage:${NC}
    $0 [options] <artifact_id>

${YELLOW}Arguments:${NC}
    artifact_id          Unique identifier for the artifact (e.g., "my-library")

${YELLOW}Options:${NC}
    -t, --type TYPE      Artifact type: ${ARTIFACT_TYPES[*]}
    -n, --name NAME      Human-readable name
    -c, --category CAT   Category/classification
    -p, --phase PHASE    Development phase (1-4)
    -l, --layer LAYER    System layer: ${LAYERS[*]}
    -s, --status STATUS  Status: ${STATUS_VALUES[*]}
    --stability LEVEL    Stability: ${STABILITY_LEVELS[*]}
    -o, --output FILE    Output file (default: stdout)
    --depends-on ID      Dependency artifact ID
    --used-by ID         Artifact that uses this one
    --relates-to ID:REL  Related artifact with relationship type
    -h, --help           Show this help message

${YELLOW}Examples:${NC}
    # Generate metadata for a new library
    $0 -t library -n "My Library" -c utilities -p 2 -l execution my-lib

    # Generate with dependencies
    $0 -t library -n "Analyzer" -c analysis --depends-on context-vars my-analyzer

    # Generate for a script
    $0 -t script -n "Build Script" -c build -p 3 -l execution build-script

${YELLOW}Output Format:${NC}
    YAML following AgentMD schema at:
    $SCHEMA_FILE

EOF
}

# Default values
TYPE=""
NAME=""
CATEGORY=""
PHASE=""
LAYER=""
STATUS="active"
STABILITY="medium"
OUTPUT=""
DEPENDS_ON=()
USED_BY=()
RELATES_TO=()

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--type)
            TYPE="$2"
            shift 2
            ;;
        -n|--name)
            NAME="$2"
            shift 2
            ;;
        -c|--category)
            CATEGORY="$2"
            shift 2
            ;;
        -p|--phase)
            PHASE="$2"
            shift 2
            ;;
        -l|--layer)
            LAYER="$2"
            shift 2
            ;;
        -s|--status)
            STATUS="$2"
            shift 2
            ;;
        --stability)
            STABILITY="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT="$2"
            shift 2
            ;;
        --depends-on)
            DEPENDS_ON+=("$2")
            shift 2
            ;;
        --used-by)
            USED_BY+=("$2")
            shift 2
            ;;
        --relates-to)
            RELATES_TO+=("$2")
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        -*)
            echo "${RED}Error: Unknown option $1${NC}"
            show_help
            exit 1
            ;;
        *)
            ARTIFACT_ID="$1"
            shift
            ;;
    esac
done

# Validate artifact ID
if [[ -z "$ARTIFACT_ID" ]]; then
    echo "${RED}Error: artifact_id is required${NC}"
    show_help
    exit 1
fi

# Set defaults from ID if not provided
[[ -z "$NAME" ]] && NAME=$(echo "$ARTIFACT_ID" | sed 's/-/ /g' | sed 's/\b\(.\)/\u\1/g')
[[ -z "$TYPE" ]] && TYPE="library"
[[ -z "$CATEGORY" ]] && CATEGORY=$(echo "$ARTIFACT_ID" | cut -d- -f1)
[[ -z "$PHASE" ]] && PHASE="2"
[[ -z "$LAYER" ]] && LAYER="execution"

# Get current date
TODAY=$(date +"%Y-%m-%d")

# Generate YAML
generate_yaml() {
    cat << EOF
# ${NAME} Metadata
# Artifact: ${NAME}
# Type: ${TYPE}

id: "${ARTIFACT_ID}"
type: "${TYPE}"
name: "${NAME}"
category: "${CATEGORY}"
version: "1.0.0"

# Location
path: "2-engine/07-operations/environment/lib/${ARTIFACT_ID}/"
created: "${TODAY}"
modified: "${TODAY}"

# Content
description: |
  TODO: Add description of ${NAME}.
  Include key capabilities, components, and usage information.

tags:
  - "${CATEGORY}"
  - "phase${PHASE}"

keywords:
  - "${CATEGORY}"
  - "${ARTIFACT_ID}"

# Relationships
depends_on:$(if [[ ${#DEPENDS_ON[@]} -gt 0 ]]; then
    echo ""
    for dep in "${DEPENDS_ON[@]}"; do
        echo "  - id: \"${dep}\""
        echo "    type: \"library\""
    done
fi)

used_by:$(if [[ ${#USED_BY[@]} -gt 0 ]]; then
    echo ""
    for user in "${USED_BY[@]}"; do
        echo "  - id: \"${user}\""
        echo "    type: \"agent\""
    done
fi)

relates_to:$(if [[ ${#RELATES_TO[@]} -gt 0 ]]; then
    echo ""
    for rel in "${RELATES_TO[@]}"; do
        IFS=':' read -r rel_id rel_type <<< "$rel"
        echo "  - id: \"${rel_id}\""
        echo "    type: \"library\""
        [[ -n "$rel_type" ]] && echo "    relationship: \"${rel_type}\""
    done
fi)

# Classification
phase: ${PHASE}
layer: "${LAYER}"

# Status
status: "${STATUS}"
stability: "${STABILITY}"

# Ownership
owner: "core-team"
maintainer: "ai-system"

# Documentation
docs:
  primary: "2-engine/07-operations/environment/lib/${ARTIFACT_ID}/README.md"

# Metrics
usage_count: 0
last_used: "${TODAY}"
success_rate: 0.0
EOF
}

# Output
OUTPUT_YAML=$(generate_yaml)

if [[ -n "$OUTPUT" ]]; then
    mkdir -p "$(dirname "$OUTPUT")"
    echo "$OUTPUT_YAML" > "$OUTPUT"
    echo "${GREEN}✓ Metadata written to: $OUTPUT${NC}"
else
    echo "$OUTPUT_YAML"
fi
