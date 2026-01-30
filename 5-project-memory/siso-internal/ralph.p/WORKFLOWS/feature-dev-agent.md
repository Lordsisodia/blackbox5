# Feature Development Agent Workflow

**Purpose**: Build features based on PRDs and requirements
**Trigger**: When tasks are marked "ready for dev" or on-demand
**Mode**: `feature_dev`
**Max Concurrent**: 2 tasks

---

## Workflow Steps

### 1. Task Selection

```yaml
step: select_task
actions:
  - Read STATE.yaml for active tasks
  - Filter for tasks with:
      - status: "pending" or "ready_for_dev"
      - type: "implementation" or "feature"
      - no unmet dependencies

  - Prioritize by:
      - priority: high > medium > low
      - created_at: oldest first
      - project: ecommerce-client > siso-internal

  - Select top task
  - Mark as "in_progress" in STATE.yaml
```

### 2. Requirements Gathering

```yaml
step: gather_requirements
actions:
  - Read task file from tasks/active/
  - Identify associated:
      - PRD: plans/prds/active/[feature].md
      - Epic: plans/active/[feature]/epic.md
      - Architecture: plans/active/[feature]/ARCHITECTURE.md

  - Read all related documents
  - Extract:
      - Functional requirements
      - Non-functional requirements
      - Acceptance criteria
      - Technical specifications
      - Dependencies

  - Create context bundle
```

### 3. Implementation Planning

```yaml
step: plan_implementation
actions:
  - Analyze requirements
  - Identify files to modify/create
  - Plan changes:
      - Database schema (if needed)
      - API endpoints (if needed)
      - Core logic/functions
      - Tests

  - Check for existing code:
      - Search for similar implementations
      - Check for reusable components
      - Review patterns in codebase

  - Create implementation plan
  - Estimate effort
```

### 4. Core Implementation

```yaml
step: implement_core
critical: true
actions:
  - For each planned file:
      - Read existing file (if modifying)
      - Implement core functionality
      - Follow existing code patterns
      - Add error handling
      - Add logging

  - Focus on:
      - Functionality over UI polish
      - Working code over perfect code
      - Tests for critical paths

  - Skip:
      - UI styling (unless required for functionality)
      - Edge cases (unless specified in requirements)
      - Performance optimization (unless NFR)
```

### 5. Supabase Integration

```yaml
step: integrate_supabase
actions:
  - If database changes needed:
      - Create migration file
      - Test migration locally
      - Document changes

  - If RLS policies needed:
      - Create policy definitions
      - Test policies
      - Document policies

  - Verify connection works
  - Test basic CRUD operations
```

### 6. Testing

```yaml
step: write_tests
actions:
  - Write tests for:
      - Happy path
      - Error cases
      - Supabase integration

  - Run tests:
      - Unit tests
      - Integration tests

  - Fix any failing tests
  - Document test coverage
```

### 7. Documentation

```yaml
step: update_documentation
actions:
  - Update code comments
  - Update API documentation (if applicable)
  - Update task file with implementation notes
  - Create/update feature documentation
```

### 8. Validation

```yaml
step: validate_implementation
actions:
  - Run final tests
  - Verify acceptance criteria:
      - Check each AC from PRD
      - Mark as met or not met

  - Code review checklist:
      - Follows project conventions
      - No console.logs left
      - Error handling in place
      - No hardcoded secrets

  - If all ACs met:
      - Mark task as "completed"
  - If ACs not met:
      - Document gaps
      - Mark as "partial"
```

### 9. State Update

```yaml
step: update_state
actions:
  - Update STATE.yaml:
      - Mark task as completed
      - Update feature progress
      - Add completed_at timestamp

  - Update WORK-LOG.md:
      - Log implementation details
      - Log time spent
      - Log any issues encountered

  - Update ACTIVE.md if needed
```

### 10. Git Operations

```yaml
step: git_operations
actions:
  - Check git status
  - Stage changes
  - Create commit:
      - Format: "feat: [feature-name] - [brief description]"
      - Include task ID

  - Push to dev branch:
      - Requires confirmation (per CONFIG.yaml)
      - Or create PR if configured

  - Update GitHub issue if linked
```

---

## Decision Points

### If Requirements Unclear
```
Action: Pause and document
- Log unclear requirements
- Mark task as "blocked"
- Suggest clarification needed
- Do not proceed with implementation
```

### If Implementation Too Large
```
Action: Break down
- Identify separable components
- Create sub-tasks
- Update epic with new tasks
- Complete current sub-task only
```

### If Tests Fail
```
Action: Fix or document
- Attempt to fix (max 3 tries)
- If cannot fix:
    - Document failing tests
    - Mark task as "partial"
    - Create follow-up task
```

### If Branch Check Fails
```
CRITICAL: Stop immediately
- Do not commit
- Alert user
- Exit workflow
```

---

## Output

### Success
```yaml
status: success
task_id: "TASK-2026-01-18-XXX"
feature: "user-profile"
results:
  files_created:
    - src/features/user-profile/api.ts
    - src/features/user-profile/hooks.ts
  files_modified:
    - src/lib/supabase.ts
  tests_added: 5
  tests_passing: 5
  acceptance_criteria:
    - AC1: met
    - AC2: met
    - AC3: met
  commit: "abc123"
  time_spent: "2 hours"
next_action: "Select next task"
```

### Partial
```yaml
status: partial
task_id: "TASK-2026-01-18-XXX"
feature: "user-profile"
results:
  files_created:
    - src/features/user-profile/api.ts
  acceptance_criteria:
    - AC1: met
    - AC2: not_met (requires UI)
    - AC3: met
  gaps:
    - "UI components need styling"
    - "Error handling incomplete"
  follow_up_tasks:
    - "TASK-2026-01-30-001: Complete UI styling"
    - "TASK-2026-01-30-002: Add error handling"
```

### Failure
```yaml
status: failure
task_id: "TASK-2026-01-18-XXX"
error: "Cannot implement - requirements conflict with existing code"
action: "Requires human review"
```

---

## Safety Checks

### Before Any Edit
```
1. Verify on allowed branch
2. Check file is not in .gitignore
3. Verify no merge conflicts
4. Check disk space
```

### Before Commit
```
1. Review all changes
2. Run tests
3. Check no secrets in code
4. Verify commit message format
```

### Before Push
```
1. Confirm branch is not main/master
2. Verify remote is correct
3. Check for force-push protection
```

---

## Integration with Other Agents

After feature dev completes:
1. Signal testing agent if tests need verification
2. Signal idea-generation agent for next features
3. Update STATE.yaml
4. Log to WORK-LOG.md
5. Check if more tasks available
