# Setup & Organization Agent Workflow

**Purpose**: Ensure project structure is correct, prevent errors, validate configuration
**Trigger**: Run at startup, then periodically (every 4 hours)
**Mode**: `setup`

---

## Workflow Steps

### 1. Project Structure Validation

```yaml
step: validate_structure
actions:
  - Check BlackBox 5 memory folders exist:
      - decisions/
      - knowledge/
      - operations/
      - plans/
      - project/
      - tasks/

  - Check key files exist:
      - STATE.yaml
      - ACTIVE.md
      - WORK-LOG.md
      - FEATURE-BACKLOG.yaml

  - Check Ralph project structure:
      - PROJECT-SPEC.md
      - CONFIG.yaml
      - WORKFLOWS/
      - LOGS/
      - STATE/

  - Report any missing files/folders
  - Create missing structure if auto-fix enabled
```

### 2. Branch Safety Check

```yaml
step: check_branch
critical: true  # Stop if this fails
actions:
  - Get current branch: git branch --show-current
  - Verify branch is in allowed list:
      - dev
      - develop
      - feature/*
      - ralph/*

  - If on forbidden branch (main/master):
      - STOP immediately
      - Alert user
      - Do not proceed

  - If on feature branch:
      - Verify it was branched from dev
      - Check for uncommitted changes
      - Suggest commit if needed

  - Log branch status
```

### 3. Supabase Connection Verification

```yaml
step: verify_supabase
actions:
  For each project in CONFIG.yaml:
    - Check if project_ref is configured
    - Test connection to Supabase
    - Verify database is accessible
    - Check RLS policies are in place
    - Report connection status

  - Update project status in CONFIG.yaml
  - Log any connection failures
```

### 4. STATE.yaml Review

```yaml
step: review_state
actions:
  - Read STATE.yaml
  - Check for inconsistencies:
      - Tasks marked complete but not in completed_tasks
      - Active tasks with no files
      - Orphaned features
      - Missing GitHub sync info

  - Verify file references exist:
      - Task files exist
      - Epic files exist
      - PRD files exist

  - Report inconsistencies
  - Suggest fixes
```

### 5. API Key Validation

```yaml
step: validate_api_keys
actions:
  - Test GLM command: claude --version (or equivalent)
  - Test Kimi command: cso-kimi --version (or equivalent)
  - Check rate limit status from LOGS/usage.yaml
  - Alert if approaching limits
  - Log API status
```

### 6. Work Log Initialization

```yaml
step: init_work_log
actions:
  - Check WORK-LOG.md exists
  - If not, create with header
  - Add session start entry
  - Log all validation results
```

### 7. Generate Setup Report

```yaml
step: generate_report
output: STATE/setup-report-{timestamp}.yaml
content:
  - timestamp
  - validation_results:
      - structure: pass/fail
      - branch: pass/fail
      - supabase: pass/fail
      - state: pass/fail
      - api: pass/fail
  - issues_found: []
  - recommendations: []
  - next_actions: []
```

---

## Decision Points

### If Structure Validation Fails
```
Option 1: Auto-fix (if enabled in CONFIG.yaml)
  - Create missing folders
  - Create missing files with templates

Option 2: Report only
  - Log issues
  - Alert user
  - Wait for manual fix
```

### If Branch Check Fails
```
CRITICAL: Must stop immediately
- Log error
- Alert user
- Exit workflow
```

### If Supabase Connection Fails
```
Option 1: Retry with exponential backoff
  - Try 3 times
  - Wait 5s, 10s, 30s between attempts

Option 2: Mark project as offline
  - Update CONFIG.yaml
  - Skip Supabase-dependent tasks
  - Continue with other work
```

---

## Output

### Success
```yaml
status: success
timestamp: "2026-01-30T10:00:00Z"
results:
  structure: valid
  branch: dev (allowed)
  supabase: connected (2/2 projects)
  state: consistent
  api: both available
next_action: "Proceed with feature development"
```

### Failure
```yaml
status: failure
timestamp: "2026-01-30T10:00:00Z"
errors:
  - type: branch
    message: "Currently on main branch - forbidden"
    action_required: "Switch to dev branch"
  - type: supabase
    message: "Cannot connect to ecommerce-client Supabase"
    action_required: "Check project_ref in CONFIG.yaml"
critical: true  # Do not proceed
```

---

## Integration with Other Agents

After setup completes successfully:
1. Signal feature-dev agent if tasks are pending
2. Signal idea-generation agent if scheduled
3. Update STATE.yaml with setup results
4. Log completion to WORK-LOG.md
