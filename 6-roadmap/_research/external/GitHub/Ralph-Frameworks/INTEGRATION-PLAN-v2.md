# BB5 Continuous Improvement Integration Plan v2
**Objective:** Integrate with existing BB5 agent infrastructure
**Approach:** Use existing agent patterns, extend with CI workflow
**Timeline:** 2 hours

---

## Current BB5 Agent Infrastructure

You already have these agents defined:
- `bb5-explorer` - Codebase exploration
- `bb5-researcher` - Technology research
- `bb5-validator` - Quality validation
- `bb5-architect` - Architecture decisions
- `bb5-security-auditor` - Security audits
- `bb5-synthesizer` - Synthesis and reporting

Plus 20 auto-activation rules in `.claude/rules/`

---

## Phase 0: Archive Legacy (15 min)

### Step 0.1: Create Archive
```bash
mkdir -p bin/ralf-executor/archive
mkdir -p bin/ralf-loops/archive
```

### Step 0.2: Move Fake Code
```bash
# Move (don't delete) fake implementations
cp bin/ralf-executor/agent-spawner.py bin/ralf-executor/archive/
mv bin/ralf-executor/agent-spawner.py bin/ralf-executor/agent-spawner.py.LEGACY

cp bin/ralf-loops/ralf-core-with-agent-teams.sh bin/ralf-loops/archive/
mv bin/ralf-loops/ralf-core-with-agent-teams.sh bin/ralf-loops/ralf-core-with-agent-teams.sh.LEGACY

cp bin/ralf-executor/ralf-six-agent-pipeline.sh bin/ralf-executor/archive/
mv bin/ralf-executor/ralf-six-agent-pipeline.sh bin/ralf-executor/ralf-six-agent-pipeline.sh.LEGACY
```

---

## Phase 1: Create CI Agent Definitions (20 min)

Create 5 new agents using your existing format:

### Agent 1: bb5-error-detector
**File:** `5-project-memory/blackbox5/.claude/agents/bb5-error-detector.md`
```yaml
---
name: bb5-error-detector
description: "Error detection specialist for BB5. Proactively scans logs and system state to find errors, issues, and anomalies."
tools: [Read, Grep, Bash, Write]
model: sonnet
color: red
---

# BB5 Error Detection Agent

## Purpose
Scan BB5 logs and system state to detect errors, issues, and anomalies before they become critical.

## When to Use
- Scheduled system health checks
- After task execution failures
- When logs show warnings
- Proactive monitoring

## Detection Process

### Phase 1: Log Scanning (2 minutes)
1. Read recent logs from `.autonomous/logs/`
2. Search for error patterns:
   - "ERROR" | "FATAL" | "CRITICAL"
   - "Host key verification failed"
   - "Permission denied"
   - "Task failed"
   - "Git push failed"
3. Check for repeated failures

### Phase 2: System State Check (1 minute)
1. Check disk space
2. Check git status (uncommitted changes)
3. Check for stuck processes
4. Verify queue health

### Phase 3: Issue Creation (2 minutes)
For each error found:
1. Create issue record in `.autonomous/ci/issues/ISS-{timestamp}.yaml`
2. Classify severity (critical/high/medium/low)
3. Document context and logs
4. Publish `issue.detected` event

## Output Format

```markdown
## Error Detection Report

### Issues Found: [N]

#### Issue 1: [Title]
- **ID**: ISS-20260210-001
- **Severity**: critical
- **Source**: ralf-core.log
- **Pattern**: "Host key verification failed"
- **Count**: 47 occurrences
- **First Seen**: 2026-02-10T03:00:00Z
- **Impact**: Git synchronization blocked

#### Issue 2: ...

### Recommendations
1. [Immediate action for critical issues]
2. [Short-term fixes]
3. [Long-term improvements]
```

## Issue YAML Format
```yaml
issue_id: ISS-{timestamp}
title: "Brief description"
severity: critical|high|medium|low
status: detected
detected_by: bb5-error-detector
detected_at: ISO timestamp
source_log: path/to/log
error_pattern: "regex pattern"
occurrence_count: N
context: |
  Relevant log lines
recommendation: "Suggested fix"
```

## Completion Checklist
- [ ] All logs scanned
- [ ] Error patterns identified
- [ ] Issues created with proper severity
- [ ] Events published
- [ ] Recommendations provided
```

### Agent 2: bb5-issue-validator
**File:** `5-project-memory/blackbox5/.claude/agents/bb5-issue-validator.md`
```yaml
---
name: bb5-issue-validator
description: "Issue validation specialist. Validates that detected issues are real, actionable, and not duplicates."
tools: [Read, Bash, Write]
model: sonnet
color: orange
---

# BB5 Issue Validation Agent

## Purpose
Validate that detected issues are real, actionable, and not false positives or duplicates.

## When to Use
- After `issue.detected` event
- Before creating implementation plans
- When issue severity is unclear

## Validation Process

### Phase 1: Reproduction Check (2 minutes)
1. Read issue record
2. Attempt to reproduce error
3. Check if error is transient
4. Verify error still exists

### Phase 2: Duplicate Detection (1 minute)
1. Search existing issues
2. Check for similar patterns
3. Merge duplicates if found

### Phase 3: Severity Assessment (1 minute)
1. Assess actual impact
2. Check affected systems
3. Determine urgency

### Phase 4: Decision (1 minute)
- **VALID**: Update status to "validated", publish `issue.validated`
- **INVALID**: Update status to "rejected", add reason, publish `issue.rejected`
- **DUPLICATE**: Link to original, close as duplicate

## Output
Updated issue YAML with validation results.
```

### Agent 3: bb5-ci-planner
**File:** `5-project-memory/blackbox5/.claude/agents/bb5-ci-planner.md`
```yaml
---
name: bb5-ci-planner
description: "Continuous improvement planning specialist. Creates implementation plans for validated issues."
tools: [Read, Write, WebSearch]
model: sonnet
color: blue
---

# BB5 CI Planning Agent

## Purpose
Create detailed implementation plans for validated issues in the continuous improvement system.

## When to Use
- After `issue.validated` event
- For complex fixes requiring multiple steps
- When solution approach is unclear

## Planning Process

### Phase 1: Analysis (3 minutes)
1. Read validated issue
2. Research solution approaches
3. Check similar past fixes
4. Identify dependencies

### Phase 2: Plan Creation (3 minutes)
Create plan with:
- Step-by-step implementation
- Required commands
- File modifications
- Testing approach
- Rollback strategy

### Phase 3: Output (2 minutes)
Write plan to `.autonomous/ci/plans/PLAN-{issue_id}.yaml`
Publish `plan.created` event

## Plan YAML Format
```yaml
plan_id: PLAN-{issue_id}
issue_id: ISS-xxx
title: "Fix description"
steps:
  - order: 1
    description: "What to do"
    command: "command to run"
    expected_output: "what success looks like"
  - order: 2
    ...
acceptance_criteria:
  - "Criterion 1"
  - "Criterion 2"
estimated_effort: "15 minutes"
rollback_steps:
  - "How to undo"
risks:
  - "Potential risk and mitigation"
```
```

### Agent 4: bb5-ci-executor
**File:** `5-project-memory/blackbox5/.claude/agents/bb5-ci-executor.md`
```yaml
---
name: bb5-ci-executor
description: "Continuous improvement execution specialist. Implements fixes according to plans."
tools: [Read, Write, Edit, Bash]
model: sonnet
color: green
---

# BB5 CI Execution Agent

## Purpose
Execute implementation plans to fix validated issues in the BB5 system.

## When to Use
- After `plan.created` event
- For automated fixes
- When execution is straightforward

## Execution Process

### Phase 1: Preparation (1 minute)
1. Read plan
2. Check prerequisites
3. Verify environment

### Phase 2: Execution (variable)
Execute each step:
1. Run command or make edit
2. Verify step succeeded
3. Document result
4. Continue or abort on failure

### Phase 3: Documentation (2 minutes)
Create execution record:
```yaml
execution_id: EXEC-{plan_id}
plan_id: PLAN-xxx
status: completed|failed
steps_completed:
  - step: 1
    result: success
    output: "..."
  - step: 2
    result: failed
    error: "..."
started_at: ISO timestamp
completed_at: ISO timestamp
```

Publish `execution.completed` event

## Safety Rules
- Stop on first failure
- Document all changes
- Create rollback checkpoint
- Never delete, only move
```

### Agent 5: bb5-ci-validator
**File:** `5-project-memory/blackbox5/.claude/agents/bb5-ci-validator.md`
```yaml
---
name: bb5-ci-validator
description: "Continuous improvement validation specialist. Verifies that executed fixes actually work."
tools: [Read, Bash, Write]
model: sonnet
color: purple
---

# BB5 CI Validation Agent

## Purpose
Verify that executed plans actually solved the issue and didn't break anything.

## When to Use
- After `execution.completed` event
- Before marking issue resolved
- For quality gates

## Validation Process

### Phase 1: Acceptance Check (2 minutes)
1. Read execution record
2. Check acceptance criteria from plan
3. Verify each criterion is met

### Phase 2: Regression Check (2 minutes)
1. Test that fix worked
2. Check for side effects
3. Verify related systems still work

### Phase 3: Decision (1 minute)
- **VALID**: Update issue status to "resolved", publish `issue.resolved`
- **INVALID**: Update execution status to "failed", publish `execution.failed`

## Output
Validation report with pass/fail status.
```

---

## Phase 2: Create CI Orchestrator (25 min)

### File: `bin/ralf-executor/ci-orchestrator.py`
```python
#!/usr/bin/env python3
"""BB5 Continuous Improvement Orchestrator.

Integrates with existing BB5 agent infrastructure to provide
automated error detection, planning, and resolution.
"""
import os
import sys
import json
import time
import yaml
from datetime import datetime
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# BB5 paths
BB5_ROOT = "/Users/shaansisodia/blackbox5"
PROJECT_ROOT = f"{BB5_ROOT}/5-project-memory/blackbox5"
CI_ROOT = f"{PROJECT_ROOT}/.autonomous/ci"
EVENTS_FILE = f"{CI_ROOT}/events/events.jsonl"

class EventBus:
    """Simple event bus for CI system."""

    def __init__(self):
        self.events_file = EVENTS_FILE
        os.makedirs(os.path.dirname(self.events_file), exist_ok=True)

    def publish(self, event_type, payload, source="ci-orchestrator"):
        event = {
            "id": f"evt-{int(time.time())}",
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "payload": payload,
            "source": source
        }
        with open(self.events_file, 'a') as f:
            f.write(json.dumps(event) + '\n')
        return event["id"]

class StateManager:
    """Manages CI state (issues, plans, executions)."""

    def __init__(self):
        self.ci_root = CI_ROOT
        os.makedirs(f"{self.ci_root}/issues", exist_ok=True)
        os.makedirs(f"{self.ci_root}/plans", exist_ok=True)
        os.makedirs(f"{self.ci_root}/executions", exist_ok=True)

    def create_issue(self, issue_id, data):
        filepath = f"{self.ci_root}/issues/{issue_id}.yaml"
        data['created_at'] = datetime.now().isoformat()
        data['updated_at'] = data['created_at']
        with open(filepath, 'w') as f:
            yaml.dump(data, f)
        return filepath

    def update_issue(self, issue_id, updates):
        filepath = f"{self.ci_root}/issues/{issue_id}.yaml"
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = yaml.safe_load(f)
            data.update(updates)
            data['updated_at'] = datetime.now().isoformat()
            with open(filepath, 'w') as f:
                yaml.dump(data, f)

    def get_issue(self, issue_id):
        filepath = f"{self.ci_root}/issues/{issue_id}.yaml"
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return yaml.safe_load(f)
        return None

    def list_issues(self, status=None):
        issues = []
        issues_dir = f"{self.ci_root}/issues"
        if not os.path.exists(issues_dir):
            return issues
        for filename in os.listdir(issues_dir):
            if filename.endswith('.yaml'):
                with open(f"{issues_dir}/{filename}", 'r') as f:
                    data = yaml.safe_load(f)
                    if status is None or data.get('status') == status:
                        issues.append(data)
        return sorted(issues, key=lambda x: x.get('created_at', ''), reverse=True)

class CIOrchestrator:
    """Main orchestrator for continuous improvement."""

    def __init__(self):
        self.event_bus = EventBus()
        self.state = StateManager()

    def spawn_agent(self, agent_name, prompt, timeout=300):
        """Spawn a BB5 agent using the Task tool."""
        # This is where we'd use the actual Task tool
        # For now, log that we would spawn
        print(f"[ORCHESTRATOR] Would spawn: {agent_name}")
        print(f"[ORCHESTRATOR] Prompt length: {len(prompt)} chars")
        # TODO: Implement actual Task tool call
        # return task(prompt=prompt, agent=agent_name, timeout=timeout)
        return None

    def run_error_detection(self):
        """Run error detection workflow."""
        print(f"[{datetime.now()}] Running error detection...")

        # Check for common errors in logs
        logs_dir = f"{PROJECT_ROOT}/.autonomous/logs"
        if os.path.exists(logs_dir):
            for log_file in os.listdir(logs_dir):
                if log_file.endswith('.log'):
                    filepath = os.path.join(logs_dir, log_file)
                    try:
                        with open(filepath, 'r') as f:
                            content = f.read()

                        # Check for SSH errors
                        if "Host key verification failed" in content:
                            issue_id = f"ISS-{int(time.time())}"
                            self.state.create_issue(issue_id, {
                                'issue_id': issue_id,
                                'title': 'SSH authentication failed',
                                'description': 'Git push failing due to missing SSH keys',
                                'severity': 'critical',
                                'status': 'detected',
                                'source_log': filepath,
                                'error_pattern': 'Host key verification failed',
                                'recommendation': 'Generate SSH keys and add to GitHub deploy keys'
                            })
                            self.event_bus.publish('issue.detected', {
                                'issue_id': issue_id,
                                'severity': 'critical'
                            })
                            print(f"  Created issue: {issue_id}")

                        # Check for task failures
                        if "Task failed" in content or "ERROR" in content:
                            # Count occurrences
                            count = content.count("Task failed") + content.count("ERROR")
                            if count > 5:
                                issue_id = f"ISS-{int(time.time())}"
                                self.state.create_issue(issue_id, {
                                    'issue_id': issue_id,
                                    'title': f'Multiple task failures detected ({count})',
                                    'description': 'Tasks are failing repeatedly',
                                    'severity': 'high',
                                    'status': 'detected',
                                    'source_log': filepath,
                                    'error_pattern': 'Task failed|ERROR',
                                    'occurrence_count': count,
                                    'recommendation': 'Review task execution logs and fix underlying issues'
                                })
                                self.event_bus.publish('issue.detected', {
                                    'issue_id': issue_id,
                                    'severity': 'high'
                                })
                                print(f"  Created issue: {issue_id}")
                    except Exception as e:
                        print(f"  Error reading {log_file}: {e}")

    def process_issues(self):
        """Process detected issues through validation."""
        issues = self.state.list_issues(status='detected')

        for issue in issues[:3]:  # Process max 3 at a time
            issue_id = issue['issue_id']
            print(f"[{datetime.now()}] Processing issue: {issue_id}")

            # Auto-validate for now (in production, spawn bb5-issue-validator)
            self.state.update_issue(issue_id, {
                'status': 'validated',
                'validated_at': datetime.now().isoformat(),
                'validation_notes': 'Auto-validated by orchestrator'
            })
            self.event_bus.publish('issue.validated', {
                'issue_id': issue_id
            })
            print(f"  Validated: {issue_id}")

            # For critical issues, we might want to auto-plan
            if issue.get('severity') == 'critical':
                print(f"  Critical issue - would spawn planner")

    def run_cycle(self):
        """Run one CI cycle."""
        print(f"\n{'='*60}")
        print(f"BB5 Continuous Improvement Cycle")
        print(f"Time: {datetime.now()}")
        print(f"{'='*60}\n")

        # Step 1: Error Detection
        self.run_error_detection()

        # Step 2: Process Issues
        self.process_issues()

        print(f"\n{'='*60}")
        print(f"Cycle complete. Sleeping...")
        print(f"{'='*60}\n")

    def run(self, daemon=False):
        """Main entry point."""
        if daemon:
            print("Starting CI Orchestrator in daemon mode...")
            while True:
                try:
                    self.run_cycle()
                except Exception as e:
                    print(f"Error in cycle: {e}")
                time.sleep(300)  # 5 minutes
        else:
            self.run_cycle()

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--daemon', action='store_true')
    parser.add_argument('--once', action='store_true')
    args = parser.parse_args()

    orchestrator = CIOrchestrator()

    if args.once:
        orchestrator.run_cycle()
    else:
        orchestrator.run(daemon=args.daemon)

if __name__ == '__main__':
    main()
```

---

## Phase 3: Integration (20 min)

### Step 3.1: Create Directory Structure
```bash
mkdir -p 5-project-memory/blackbox5/.autonomous/ci/{events,issues,plans,executions}
```

### Step 3.2: Create Service Wrapper
**File:** `bin/ralf-executor/ci-orchestrator.sh`
```bash
#!/bin/bash
# CI Orchestrator Service Wrapper

cd /Users/shaansisodia/blackbox5 || exit 1

export ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
export BB5_MODE=autonomous

exec python3 bin/ralf-executor/ci-orchestrator.py --daemon
```

```bash
chmod +x bin/ralf-executor/ci-orchestrator.sh
chmod +x bin/ralf-executor/ci-orchestrator.py
```

### Step 3.3: Create Systemd Service
**File:** `bin/ralf-executor/bb5-ci-orchestrator.service`
```ini
[Unit]
Description=BB5 Continuous Improvement Orchestrator
After=network.target

[Service]
Type=simple
User=bb5-runner
WorkingDirectory=/opt/blackbox5
Environment="HOME=/home/bb5-runner"
Environment="ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}"
Environment="BB5_MODE=autonomous"
ExecStart=/usr/bin/su -l bb5-runner -c 'cd /opt/blackbox5 && python3 bin/ralf-executor/ci-orchestrator.py --daemon'
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Step 3.4: Integrate with Existing RALF
Modify `ralf-core.sh` to trigger CI events:

Add at end of task completion:
```bash
# Trigger CI analysis
trigger_ci_event() {
    local task_id="$1"
    local status="$2"

    python3 -c "
import sys
sys.path.insert(0, 'bin/ralf-executor')
from ci_orchestrator import EventBus
ebus = EventBus()
ebus.publish('task.completed', {
    'task_id': '$task_id',
    'status': '$status'
}, source='ralf-core')
" 2>/dev/null || true
}

# Call after task completion
trigger_ci_event "$CURRENT_TASK" "$STATUS"
```

---

## Phase 4: Test & Deploy (20 min)

### Step 4.1: Local Test
```bash
# Test orchestrator
python3 bin/ralf-executor/ci-orchestrator.py --once

# Check events were created
cat 5-project-memory/blackbox5/.autonomous/ci/events/events.jsonl

# Check issues were created
ls -la 5-project-memory/blackbox5/.autonomous/ci/issues/
```

### Step 4.2: Commit
```bash
git add -A
git commit -m "feat: Add continuous improvement system v2

- 5 new CI agents (error-detector, validator, planner, executor, validator)
- CI orchestrator with event bus and state management
- Integration with existing BB5 agent infrastructure
- Service wrapper and systemd config
- Archive legacy fake code

Uses existing BB5 agent patterns and integrates with
bb5-explorer, bb5-researcher, bb5-validator, etc."
```

### Step 4.3: Push & Deploy
```bash
git push origin autonomous-improvement

# On VPS:
# git pull origin autonomous-improvement
# sudo systemctl enable bb5-ci-orchestrator
# sudo systemctl start bb5-ci-orchestrator
```

---

## What This Achieves

1. **Uses your existing agent infrastructure** - Same format as bb5-explorer, etc.
2. **Real error detection** - Scans logs, creates issues
3. **Event-driven workflow** - JSONL event bus
4. **State management** - YAML files for issues/plans
5. **Integration with RALF** - Triggers on task completion
6. **Archive (not delete)** - Preserves legacy code

---

## Next Steps (After This Works)

1. Implement actual Task tool spawning in `spawn_agent()`
2. Add remaining 3 agents (improvement, test-analysis, integration-decision)
3. Add circuit breaker for safety
4. Create monitoring dashboard

---

**Ready to execute?** Say "execute" and I'll implement this step by step.
