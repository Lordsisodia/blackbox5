#!/bin/bash
# RALF Planner Agent - Integration Planning
# Purpose: Review analyzer summaries and create integration plans for Blackbox5

set -e

AGENT_NAME="planner"
PROJECT_ROOT="/opt/ralf"
RUN_DIR="$PROJECT_ROOT/5-project-memory/blackbox5/.autonomous/agents/planner/runs/run-$(date +%Y%m%d-%H%M%S)"
EVENTS_FILE="$PROJECT_ROOT/5-project-memory/blackbox5/.autonomous/agents/communications/events.yaml"
SUMMARY_DIR="$PROJECT_ROOT/5-project-memory/blackbox5/.autonomous/agents/analyzer/summaries"
PLANS_DIR="$PROJECT_ROOT/5-project-memory/blackbox5/.autonomous/agents/planner/integration-plans"
TASKS_DIR="$PROJECT_ROOT/5-project-memory/blackbox5/tasks/active"

mkdir -p "$RUN_DIR" "$PLANS_DIR"

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

create_integration_plan() {
    local summary_file="$1"
    local repo_name=$(basename "$summary_file" -summary.yaml)
    local plan_file="$PLANS_DIR/PLAN-${repo_name}.md"

    log_event "info" "Creating integration plan for $repo_name"
    update_heartbeat "planning:$repo_name"

    python3 << PYEOF
import yaml
import re

try:
    with open('$summary_file', 'r') as f:
        data = yaml.safe_load(f)

    summary = data.get('summary', {})
    assessment = data.get('assessment', {})
    metrics = data.get('metrics', {})
    insights = data.get('insights', {})

    repo_name = summary.get('repo_name', 'unknown')
    repo_url = summary.get('repo_url', '')
    category = assessment.get('category', 'general')
    concepts = assessment.get('key_concepts', [])
    relevance = assessment.get('relevance_score', 0)
    action = insights.get('recommended_action', 'archive')

    # Generate integration strategy based on category
    if category == 'hooks':
        strategy = """
## Integration Strategy: Hook System

### Analysis
This repository provides Claude Code hooks that could enhance Blackbox5's automation.

### Integration Options

1. **Direct Adoption**
   - Copy relevant hooks to \`.claude/hooks/\`
   - Adapt to Blackbox5's hook naming convention
   - Test with ralf-post-tool-hook.sh framework

2. **Hybrid Approach**
   - Extract hook logic into Blackbox5 skill system
   - Create wrapper scripts in \`bin/\`
   - Maintain compatibility with existing RALF agents

3. **Reference Implementation**
   - Document patterns for future Blackbox5 hooks
   - Add to architecture documentation
   - Create example implementations

### Implementation Tasks
- [ ] Review hook compatibility with Blackbox5 lifecycle
- [ ] Adapt hook to Blackbox5 directory structure
- [ ] Add configuration via Blackbox5 settings
- [ ] Test with ralf-session-start-hook.sh
- [ ] Document in integration guide
"""
    elif category == 'mcp':
        strategy = """
## Integration Strategy: MCP Server

### Analysis
This repository provides MCP (Model Context Protocol) servers for Claude Code.

### Integration Options

1. **Direct Integration**
   - Add to \`.mcp-moltbot.json\`
   - Configure via environment variables
   - Test with mcp-openclaw-direct.py

2. **RALF Agent Enhancement**
   - Create MCP-enabled RALF agent variant
   - Add MCP tools to agent capabilities
   - Enable cross-agent communication via MCP

3. **Blackbox5 Service**
   - Run as persistent service
   - Integrate with Moltbot monitoring
   - Add health checks to ralf-keepalive

### Implementation Tasks
- [ ] Verify MCP protocol compatibility
- [ ] Add server to MCP configuration
- [ ] Create connection test script
- [ ] Document usage in Blackbox5 context
- [ ] Add to moltbot monitoring
"""
    elif category == 'skills':
        strategy = """
## Integration Strategy: Skills Library

### Analysis
This repository provides Claude Code skills that could enhance Blackbox5 capabilities.

### Integration Options

1. **Skill Import**
   - Copy skills to \`~/.claude/skills/\`
   - Adapt to Blackbox5 skill format
   - Register in skill registry

2. **RALF Agent Skills**
   - Create agent-specific skill variants
   - Add to scout/analyzer/planner capabilities
   - Enable dynamic skill loading

3. **Skill Framework Enhancement**
   - Extract skill patterns for Blackbox5
   - Improve skill: command handling
   - Add skill metrics tracking

### Implementation Tasks
- [ ] Review skill format compatibility
- [ ] Adapt skill metadata for Blackbox5
- [ ] Test skill invocation
- [ ] Add to skill-usage.yaml tracking
- [ ] Document in skill guide
"""
    elif category == 'agents':
        strategy = """
## Integration Strategy: Agent Framework

### Analysis
This repository provides multi-agent orchestration capabilities.

### Integration Options

1. **Agent Pattern Adoption**
   - Study agent communication patterns
   - Adapt to RALF file-based protocol
   - Enhance scout/analyzer/planner agents

2. **Orchestration Layer**
   - Add to Blackbox5 2-engine architecture
   - Create agent supervisor
   - Implement agent-to-agent messaging

3. **RALF Enhancement**
   - Improve ralf-dual-v2 with new patterns
   - Add agent negotiation protocols
   - Enable dynamic agent spawning

### Implementation Tasks
- [ ] Map agent patterns to Blackbox5
- [ ] Design integration architecture
- [ ] Prototype agent communication
- [ ] Test with existing RALF agents
- [ ] Document agent protocols
"""
    else:
        strategy = """
## Integration Strategy: General Reference

### Analysis
This repository has moderate relevance to Blackbox5.

### Integration Options

1. **Documentation Reference**
   - Add to research knowledge base
   - Document key concepts
   - Reference in architecture decisions

2. **Future Evaluation**
   - Monitor for updates
   - Re-evaluate if scope changes
   - Archive for now

### Implementation Tasks
- [ ] Document in research log
- [ ] Tag for future review
- [ ] Add to external resources
"""

    # Generate priority based on relevance
    if relevance >= 80:
        priority = "CRITICAL"
        timeline = "1-2 days"
    elif relevance >= 60:
        priority = "HIGH"
        timeline = "1 week"
    elif relevance >= 40:
        priority = "MEDIUM"
        timeline = "2 weeks"
    else:
        priority = "LOW"
        timeline = "Backlog"

    plan = f"""# Integration Plan: {repo_name}

**Generated:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Planner Run:** $(basename $RUN_DIR)
**Priority:** {priority}
**Timeline:** {timeline}

## Source Repository

- **Name:** {repo_name}
- **URL:** {repo_url}
- **Category:** {category}
- **Relevance Score:** {relevance}/100
- **Key Concepts:** {', '.join(concepts) if concepts else 'None identified'}

{strategy}

## Success Criteria

- [ ] Integration tested in isolation
- [ ] Documentation updated
- [ ] RALF agents can utilize enhancement
- [ ] No regression in existing functionality
- [ ] Performance impact assessed

## Rollback Plan

1. Revert changes via git
2. Remove from MCP configuration if applicable
3. Update agent configurations
4. Document reason for rollback

## Related Resources

- Source Summary: $summary_file
- Blackbox5 Architecture: 5-project-memory/blackbox5/.docs/blackbox5-architecture.md
- Integration Guide: 1-docs/.docs/moltbot/HYBRID-INTEGRATION.md
"""

    with open('$plan_file', 'w') as f:
        f.write(plan)

    print(f"Created plan: $plan_file")

    # Create task file if high priority
    if relevance >= 60:
        task_id = f"TASK-INTEGRATE-{repo_name.upper()[:10]}"
        task_file = "$TASKS_DIR/{task_id}.md"
        task_content = f"""# {task_id}: Integrate {repo_name}

**Status:** pending
**Priority:** {priority}
**Created:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Source:** GitHub Analysis Pipeline
**Relevance Score:** {relevance}/100

## Objective
Integrate {repo_name} ({repo_url}) into Blackbox5 following the integration plan.

## Success Criteria
- [ ] Review integration plan at {plan_file}
- [ ] Implement integration approach
- [ ] Test with existing RALF agents
- [ ] Update documentation
- [ ] Verify no regressions

## Context
This task was auto-generated by the planner agent analyzing GitHub repos for Blackbox5 enhancement opportunities.

Category: {category}
Key Concepts: {', '.join(concepts) if concepts else 'N/A'}

## Approach
1. Read integration plan
2. Review source repository
3. Implement integration
4. Test thoroughly
5. Document changes

## Rollback Strategy
Revert git changes and remove from configuration files.
"""
        with open(task_file, 'w') as f:
            f.write(task_content)
        print(f"Created task: {task_file}")

except Exception as e:
    print(f"Error creating plan for $summary_file: {e}")
PYEOF

    log_event "success" "Created plan for $repo_name"
}

main() {
    log_event "start" "Planner agent starting autonomous run"
    update_heartbeat "running"

    local count=0
    for summary in "$SUMMARY_DIR"/*-summary.yaml; do
        if [ -f "$summary" ]; then
            count=$((count + 1))
            echo "[$count] Planning: $(basename $summary)"
            create_integration_plan "$summary"
            sleep 2
        fi
    done

    # Create master plan index
    cat > "$PLANS_DIR/MASTER-PLAN-INDEX.md" << EOF
# Integration Plans Master Index

**Generated:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Planner Run:** $(basename $RUN_DIR)
**Total Plans:** $count

## Plans by Priority

### CRITICAL (Score 80+)
$(ls -1 "$PLANS_DIR"/PLAN-*.md 2>/dev/null | while read f; do
    if grep -q "Priority: CRITICAL" "$f" 2>/dev/null; then
        repo=$(grep "^# Integration Plan:" "$f" | head -1 | sed 's/# Integration Plan: //')
        echo "- [$repo]($(basename "$f"))"
    fi
done)

### HIGH (Score 60-79)
$(ls -1 "$PLANS_DIR"/PLAN-*.md 2>/dev/null | while read f; do
    if grep -q "Priority: HIGH" "$f" 2>/dev/null; then
        repo=$(grep "^# Integration Plan:" "$f" | head -1 | sed 's/# Integration Plan: //')
        echo "- [$repo]($(basename "$f"))"
    fi
done)

### MEDIUM (Score 40-59)
$(ls -1 "$PLANS_DIR"/PLAN-*.md 2>/dev/null | while read f; do
    if grep -q "Priority: MEDIUM" "$f" 2>/dev/null; then
        repo=$(grep "^# Integration Plan:" "$f" | head -1 | sed 's/# Integration Plan: //')
        echo "- [$repo]($(basename "$f"))"
    fi
done)

## Auto-Generated Tasks

$(ls -1 "$TASKS_DIR"/TASK-INTEGRATE-*.md 2>/dev/null | wc -l) integration tasks created in \`$TASKS_DIR\`

## Next Steps

1. Review CRITICAL priority plans first
2. Assign tasks to executor agents
3. Track progress via events.yaml
4. Update plans as integrations complete
EOF

    log_event "complete" "Planner agent completed. Created $count plans."
    update_heartbeat "idle"

    # Create results file
    cat > "$RUN_DIR/RESULTS.md" << EOF
# Planner Agent Run Results

**Run:** $(basename $RUN_DIR)
**Completed:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Plans Created:** $count

## Outputs

- Integration Plans: \`$PLANS_DIR\`
- Master Index: \`$PLANS_DIR/MASTER-PLAN-INDEX.md\`
- Auto-Generated Tasks: \`$TASKS_DIR\`

## Status

All plans created. Executor agents can now claim integration tasks.
EOF
}

main "$@"
