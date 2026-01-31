# Skill Tracking Guide

**Location:** `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/operations/skill-usage.yaml`

## Purpose

Track skill usage patterns, effectiveness, and identify optimization opportunities for the BlackBox5 skill system.

## Quick Reference

### Recording a Skill Invocation

After using any skill, append to the `usage_log` section:

```yaml
usage_log:
  - timestamp: "2026-02-01T12:00:00Z"
    skill: bmad-dev
    task_id: TASK-123
    trigger_reason: "Implementation of feature X"
    execution_time_ms: 45000
    result: success
    notes: "Clean execution, no issues"
```

### Updating Aggregate Stats

Periodically (weekly/monthly), update the skill's aggregate statistics:

```yaml
skills:
  - name: bmad-dev
    usage_count: 5          # Increment by number of new invocations
    last_used: "2026-02-01T12:00:00Z"
    success_count: 4        # Update based on results
    failure_count: 1
    avg_execution_time_ms: 42000  # Calculate new average
    trigger_accuracy: high  # Assess: did it trigger when needed?
```

## Schema Reference

### Skill Entry Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Unique skill identifier |
| `description` | string | One-line description |
| `category` | enum | agent, protocol, utility, core, infrastructure |
| `agent` | string | Agent name (for agent skills) |
| `usage_count` | integer | Total invocations |
| `first_used` | timestamp | First invocation date |
| `last_used` | timestamp | Most recent invocation |
| `success_count` | integer | Successful completions |
| `failure_count` | integer | Failed/partial completions |
| `avg_execution_time_ms` | integer | Average execution time |
| `trigger_accuracy` | enum | high, medium, low, unknown |
| `notes` | string | Observations and trigger patterns |

### Usage Log Entry Fields

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | timestamp | When the skill was invoked |
| `skill` | string | Skill name used |
| `task_id` | string | Associated task ID |
| `trigger_reason` | string | Why this skill was selected |
| `execution_time_ms` | integer | Time taken (if known) |
| `result` | enum | success, failure, partial |
| `notes` | string | Additional observations |

## Workflow

### For Skill Users (Claude)

1. After invoking a skill, note the timestamp and result
2. Append entry to `usage_log` section
3. Update aggregate stats if doing batch update

### For System Maintainers

**Weekly:**
- Review `usage_log` entries
- Update aggregate `skills` statistics
- Check for patterns in `trigger_accuracy`

**Monthly:**
- Update `analysis` section
- Identify top skills and underutilized skills
- Note any trigger accuracy issues
- Document recommendations

**Quarterly:**
- Comprehensive skill system review
- Consider adding/removing skills based on data
- Update skill triggers based on accuracy findings

## Analysis Queries

### Find Most Used Skills

```bash
# View skills sorted by usage_count
grep -A 2 "name:" operations/skill-usage.yaml | grep -E "(name:|usage_count:)"
```

### Calculate Success Rate

```bash
# Success rate = success_count / usage_count * 100
# Calculate per skill from aggregate stats
```

### Identify Underutilized Skills

Look for skills with:
- `usage_count: 0` (never used)
- `trigger_accuracy: low` (not triggering when needed)
- Low usage relative to expected frequency

## Automation Roadmap

### Phase 1: Manual (Current)
- Hand-update YAML after skill usage
- Periodic batch updates of aggregates

### Phase 2: Semi-Automated
- Wrapper script captures skill invocations
- Auto-appends to usage_log
- Weekly aggregate update script

### Phase 3: Fully Automated
- Skill router auto-logs invocations
- Real-time dashboard
- Automated monthly analysis reports

## Examples

### Example 1: Recording a Successful Invocation

```yaml
# In usage_log:
- timestamp: "2026-02-01T14:30:00Z"
  skill: superintelligence-protocol
  task_id: TASK-456
  trigger_reason: "User asked 'Should we refactor the auth system?'"
  execution_time_ms: 120000
  result: success
  notes: "Protocol activated correctly, 7-step analysis completed"

# Update aggregate for superintelligence-protocol:
- name: superintelligence-protocol
  usage_count: 3
  last_used: "2026-02-01T14:30:00Z"
  success_count: 3
  trigger_accuracy: high
```

### Example 2: Recording a Partial Result

```yaml
# In usage_log:
- timestamp: "2026-02-01T15:00:00Z"
  skill: bmad-dev
  task_id: TASK-789
  trigger_reason: "Feature implementation"
  execution_time_ms: 300000
  result: partial
  notes: "Core feature done, tests pending - context overflow"

# Update aggregate for bmad-dev:
- name: bmad-dev
  usage_count: 5
  last_used: "2026-02-01T15:00:00Z"
  success_count: 3
  failure_count: 1
  # partial counts as neither success nor failure
```

## Related Files

- `2-engine/.autonomous/skills/README.md` - Skill definitions
- `2-engine/.autonomous/skills/*/SKILL.md` - Individual skill details
- `CLAUDE.md` - User instructions with skill triggers
