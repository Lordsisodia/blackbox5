#!/bin/bash
# RALF Scout Agent - GitHub Repo Discovery & Extraction
# Purpose: Extract key knowledge from GitHub repos and store in structured format

set -e

AGENT_NAME="scout"
PROJECT_ROOT="/opt/ralf"
RUN_DIR="$PROJECT_ROOT/5-project-memory/blackbox5/.autonomous/agents/scout/runs/run-$(date +%Y%m%d-%H%M%S)"
QUEUE_FILE="$PROJECT_ROOT/5-project-memory/blackbox5/.autonomous/agents/communications/queue.yaml"
EVENTS_FILE="$PROJECT_ROOT/5-project-memory/blackbox5/.autonomous/agents/communications/events.yaml"
REPO_LIST="$PROJECT_ROOT/6-roadmap/research/external/GitHub/repo-list.yaml"
OUTPUT_DIR="$PROJECT_ROOT/5-project-memory/blackbox5/.autonomous/agents/scout/extractions"

mkdir -p "$RUN_DIR" "$OUTPUT_DIR"

log_event() {
    local type="$1"
    local message="$2"
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)

    cat >> "$EVENTS_FILE" << EOF
- timestamp: "$timestamp"
  agent: $AGENT_NAME
  type: $type
  message: "$message"
  run_dir: "$RUN_DIR"

EOF
}

update_heartbeat() {
    local status="$1"
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)

    python3 << PYEOF
import yaml
import sys

try:
    with open('$PROJECT_ROOT/5-project-memory/blackbox5/.autonomous/agents/communications/heartbeat.yaml', 'r') as f:
        data = yaml.safe_load(f) or {'heartbeats': {}}
except:
    data = {'heartbeats': {}}

if 'heartbeats' not in data:
    data['heartbeats'] = {}

data['heartbeats']['$AGENT_NAME'] = {
    'status': '$status',
    'last_seen': '$timestamp',
    'run_dir': '$RUN_DIR'
}

with open('$PROJECT_ROOT/5-project-memory/blackbox5/.autonomous/agents/communications/heartbeat.yaml', 'w') as f:
    yaml.dump(data, f, default_flow_style=False)
PYEOF
}

extract_repo_data() {
    local repo_url="$1"
    local repo_name=$(basename "$repo_url" .git)
    local extraction_file="$OUTPUT_DIR/${repo_name}-$(date +%s).yaml"

    log_event "info" "Starting extraction for $repo_name"
    update_heartbeat "extracting:$repo_name"

    # Clone and analyze repo
    local temp_dir=$(mktemp -d)
    cd "$temp_dir"

    if git clone --depth 1 "$repo_url" "$repo_name" 2>/dev/null; then
        cd "$repo_name"

        # Extract key information
        local stars=$(curl -s "https://api.github.com/repos/$(echo $repo_url | sed 's|https://github.com/||')" | python3 -c "import sys,json; print(json.load(sys.stdin).get('stargazers_count', 0))" 2>/dev/null || echo "0")
        local last_commit=$(git log -1 --format=%cd --date=short 2>/dev/null || echo "unknown")
        local languages=$(find . -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.go" -o -name "*.rs" \) | head -20 | xargs -I {} basename {} | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -5 | awk '{print $2}' | tr '\n' ',' | sed 's/,$//')
        local readme=$(cat README.md 2>/dev/null | head -100 || echo "No README")
        local structure=$(find . -type f -not -path './.git/*' | head -50 | sed 's|^\./||' | sort)

        # Create extraction record
        cat > "$extraction_file" << EOF
extraction:
  repo_name: "$repo_name"
  repo_url: "$repo_url"
  extracted_at: "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  agent: scout
  run_dir: "$RUN_DIR"

metadata:
  stars: $stars
  last_commit: "$last_commit"
  languages: "$languages"
  file_count: $(find . -type f -not -path './.git/*' | wc -l)

structure: |
$(echo "$structure" | sed 's/^/  /')

readme_summary: |
$(echo "$readme" | sed 's/^/  /')

key_files:
$(find . -type f \( -name "*.md" -o -name "*.yaml" -o -name "*.yml" -o -name "*.json" \) -not -path './.git/*' | head -20 | sed 's/^\./  - /')

analysis_status: pending_analyzer
EOF

        log_event "success" "Extracted $repo_name to $(basename $extraction_file)"
        echo "$extraction_file"
    else
        log_event "error" "Failed to clone $repo_url"
        echo ""
    fi

    rm -rf "$temp_dir"
}

main() {
    log_event "start" "Scout agent starting autonomous run"
    update_heartbeat "running"

    # Get repos from repo-list.yaml
    local repos=$(cat "$REPO_LIST" | grep -A 1 "url:" | grep "https://github.com" | head -20)

    local count=0
    for repo in $repos; do
        count=$((count + 1))
        echo "[$count] Processing: $repo"

        extraction_file=$(extract_repo_data "$repo")

        if [ -n "$extraction_file" ]; then
            # Notify analyzer via events
            log_event "ready_for_analysis" "Extraction complete: $extraction_file"
        fi

        # Brief pause between repos
        sleep 5
    done

    log_event "complete" "Scout agent completed. Processed $count repos."
    update_heartbeat "idle"

    # Create results file
    cat > "$RUN_DIR/RESULTS.md" << EOF
# Scout Agent Run Results

**Run:** $(basename $RUN_DIR)
**Completed:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Repos Processed:** $count

## Extractions

$(ls -1 $OUTPUT_DIR/*.yaml 2>/dev/null | wc -l) extraction files created in:
\`$OUTPUT_DIR\`

## Next Steps

Analyzer agent should process extractions and create summaries.
EOF
}

main "$@"
