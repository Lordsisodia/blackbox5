#!/bin/bash
# RALF Analyzer Agent - Data Summarization & Pattern Recognition
# Purpose: Analyze scout extractions and create structured summaries

set -e

AGENT_NAME="analyzer"
PROJECT_ROOT="/opt/ralf"
RUN_DIR="$PROJECT_ROOT/5-project-memory/blackbox5/.autonomous/agents/analyzer/runs/run-$(date +%Y%m%d-%H%M%S)"
EVENTS_FILE="$PROJECT_ROOT/5-project-memory/blackbox5/.autonomous/agents/communications/events.yaml"
EXTRACTION_DIR="$PROJECT_ROOT/5-project-memory/blackbox5/.autonomous/agents/scout/extractions"
OUTPUT_DIR="$PROJECT_ROOT/5-project-memory/blackbox5/.autonomous/agents/analyzer/summaries"
CONCEPTS_DIR="$PROJECT_ROOT/5-project-memory/blackbox5/.autonomous/agents/analyzer/concepts"

mkdir -p "$RUN_DIR" "$OUTPUT_DIR" "$CONCEPTS_DIR"

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

analyze_extraction() {
    local extraction_file="$1"
    local repo_name=$(basename "$extraction_file" .yaml)
    local summary_file="$OUTPUT_DIR/${repo_name}-summary.yaml"

    log_event "info" "Analyzing $repo_name"
    update_heartbeat "analyzing:$repo_name"

    # Parse extraction and create summary
    python3 << PYEOF
import yaml
import re
from datetime import datetime

try:
    with open('$extraction_file', 'r') as f:
        data = yaml.safe_load(f)

    extraction = data.get('extraction', {})
    metadata = data.get('metadata', {})
    structure = data.get('structure', '')
    readme = data.get('readme_summary', '')

    # Extract patterns
    patterns = {
        'hooks': len(re.findall(r'hook', readme, re.I)),
        'mcp': len(re.findall(r'mcp', readme, re.I)),
        'skills': len(re.findall(r'skill', readme, re.I)),
        'agents': len(re.findall(r'agent', readme, re.I)),
        'claude': len(re.findall(r'claude', readme, re.I)),
        'automation': len(re.findall(r'automat', readme, re.I))
    }

    # Identify key concepts
    concepts = []
    if patterns['hooks'] > 0:
        concepts.append('hooks')
    if patterns['mcp'] > 0:
        concepts.append('mcp-servers')
    if patterns['skills'] > 0:
        concepts.append('skills')
    if patterns['agents'] > 0:
        concepts.append('agents')
    if patterns['claude'] > 0:
        concepts.append('claude-code')
    if patterns['automation'] > 0:
        concepts.append('automation')

    # Determine category
    category = 'general'
    if 'claude-code' in concepts:
        if 'hooks' in concepts:
            category = 'hooks'
        elif 'mcp-servers' in concepts:
            category = 'mcp'
        elif 'skills' in concepts:
            category = 'skills'
        elif 'agents' in concepts:
            category = 'agents'

    # Calculate relevance score (0-100)
    relevance = min(100, sum(patterns.values()) * 5 + int(metadata.get('stars', 0)) / 100)

    summary = {
        'summary': {
            'repo_name': extraction.get('repo_name'),
            'repo_url': extraction.get('repo_url'),
            'analyzed_at': datetime.utcnow().isoformat() + 'Z',
            'agent': 'analyzer',
            'run_dir': '$RUN_DIR'
        },
        'assessment': {
            'category': category,
            'relevance_score': round(relevance, 1),
            'key_concepts': concepts,
            'complexity': 'high' if len(structure.split('\n')) > 30 else 'medium' if len(structure.split('\n')) > 10 else 'low'
        },
        'metrics': {
            'stars': metadata.get('stars', 0),
            'languages': metadata.get('languages', ''),
            'file_count': metadata.get('file_count', 0),
            'pattern_matches': patterns
        },
        'insights': {
            'primary_purpose': readme.split('\n')[0] if readme else 'Unknown',
            'integration_potential': 'high' if relevance > 70 else 'medium' if relevance > 40 else 'low',
            'recommended_action': 'immediate_review' if relevance > 80 else 'evaluate' if relevance > 50 else 'archive'
        },
        'source_extraction': '$extraction_file'
    }

    with open('$summary_file', 'w') as f:
        yaml.dump(summary, f, default_flow_style=False)

    # Save concepts for cross-repo analysis
    for concept in concepts:
        concept_file = '$CONCEPTS_DIR/' + concept + '.yaml'
        try:
            with open(concept_file, 'r') as f:
                concept_data = yaml.safe_load(f) or {'repos': []}
        except:
            concept_data = {'repos': []}

        concept_data['repos'].append({
            'name': extraction.get('repo_name'),
            'url': extraction.get('repo_url'),
            'relevance': round(relevance, 1),
            'summary_file': '$summary_file'
        })

        with open(concept_file, 'w') as f:
            yaml.dump(concept_data, f, default_flow_style=False)

    print(f"Created summary: $summary_file")

except Exception as e:
    print(f"Error analyzing $extraction_file: {e}")
PYEOF

    log_event "success" "Analyzed $repo_name"
}

main() {
    log_event "start" "Analyzer agent starting autonomous run"
    update_heartbeat "running"

    local count=0
    for extraction in "$EXTRACTION_DIR"/*.yaml; do
        if [ -f "$extraction" ]; then
            count=$((count + 1))
            echo "[$count] Analyzing: $(basename $extraction)"
            analyze_extraction "$extraction"
            sleep 2
        fi
    done

    # Create master summary
    cat > "$OUTPUT_DIR/MASTER-SUMMARY-$(date +%Y%m%d).md" << EOF
# GitHub Repo Analysis Master Summary

**Generated:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Analyzer Run:** $(basename $RUN_DIR)
**Repos Analyzed:** $count

## By Category

$(for f in "$CONCEPTS_DIR"/*.yaml; do
    if [ -f "$f" ]; then
        concept=$(basename "$f" .yaml)
        count=$(grep -c "name:" "$f" 2>/dev/null || echo "0")
        echo "- **$concept**: $count repos"
    fi
done)

## High Relevance Repos (>80)

$(grep -l "relevance_score: [8-9][0-9]" "$OUTPUT_DIR"/*-summary.yaml 2>/dev/null | while read f; do
    repo=$(grep "repo_name:" "$f" | head -1 | cut -d: -f2 | tr -d ' "')
    score=$(grep "relevance_score:" "$f" | head -1 | cut -d: -f2 | tr -d ' ')
    echo "- $repo (score: $score)"
done)

## Integration Recommendations

### Immediate Review (score >80)
$(grep -l "recommended_action: immediate_review" "$OUTPUT_DIR"/*-summary.yaml 2>/dev/null | while read f; do
    grep "repo_name:" "$f" | head -1 | cut -d: -f2 | tr -d ' "' | sed 's/^/- /'
done)

### Evaluate (score 50-80)
$(grep -l "recommended_action: evaluate" "$OUTPUT_DIR"/*-summary.yaml 2>/dev/null | head -10 | while read f; do
    grep "repo_name:" "$f" | head -1 | cut -d: -f2 | tr -d ' "' | sed 's/^/- /'
done)

## Next Steps

Planner agent should review summaries and create integration plans.
EOF

    log_event "complete" "Analyzer agent completed. Analyzed $count repos."
    update_heartbeat "idle"

    # Create results file
    cat > "$RUN_DIR/RESULTS.md" << EOF
# Analyzer Agent Run Results

**Run:** $(basename $RUN_DIR)
**Completed:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Repos Analyzed:** $count

## Outputs

- Summaries: \`$OUTPUT_DIR\`
- Concepts: \`$CONCEPTS_DIR\`
- Master Summary: \`$OUTPUT_DIR/MASTER-SUMMARY-$(date +%Y%m%d).md\`

## Status

Ready for planner agent to create integration plans.
EOF
}

main "$@"
