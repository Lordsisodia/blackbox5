# Conversational Task Planner

**Skill Name:** `conversational-task-planner`
**Version:** 1.0.0
**Category:** Planning & Orchestration

---

## Overview

The Conversational Task Planner listens to natural conversation from the main agent (SISO) and automatically creates structured BlackBox5 task plans. No forms, no structured input—just parse natural requests and generate actionable task plans.

---

## Capabilities

### 1. Natural Language Parsing
- Extracts task intent from casual conversation
- Infers task type, priority, and scope from context
- Identifies success criteria and research needs

### 2. Automatic Task Generation
- Creates complete BlackBox5 task files with:
  - Research/analysis phase
  - Implementation steps
  - Testing checklist
  - Success criteria
- Generates unique task IDs with timestamps
- Places tasks in `/opt/blackbox5/5-project-memory/blackbox5/tasks/active/`

### 3. Status Tracking
- Monitors active tasks
- Responds to status inquiries
- Provides updates on work in progress

---

## Trigger Patterns

The planner activates when SISO uses phrases like:

**Task Creation:**
- "make a plan for X"
- "plan for improving X"
- "create a task for X"
- "I need to fix X"
- "I need to implement X"
- "I need to build X"
- "work on X"

**Status Inquiries:**
- "status of the dashboard"
- "what's the status of X"
- "how's X going"

**Planning Requests:**
- "make a plan for improving RALF loops"
- "plan for fixing the YouTube scraper"
- "task for optimizing the database"

---

## Task Structure

Generated tasks follow BlackBox5 format:

```markdown
# TASK-[timestamp]: [Task Name]

**Status:** pending
**Priority:** HIGH|MEDIUM|LOW
**Type:** implement|fix|refactor|analyze|organize|research|improve
**Created:** YYYY-MM-DDTHH:MM:SSZ
**Estimated Lines:** [NUMBER]

## Objective
[Clear statement of what needs to be done]

## Research & Analysis Phase
- [ ] Research the problem space
- [ ] Identify existing solutions/patterns
- [ ] Analyze dependencies
- [ ] Document findings

## Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

## Implementation Approach
[Step-by-step implementation plan]

## Testing Checklist
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual verification complete
- [ ] Edge cases covered
- [ ] Documentation updated

## Context
[Background information and conversation context]

## Files to Modify
- `[path]`: [what to change]
- `[path]`: [what to change]

## Files to Create
- `[path]`: [purpose]

## Rollback Strategy
[How to undo changes if needed]

## Notes
[Any warnings or additional context]
```

---

## Priority Inference

The planner infers priority from language cues:

| Indicators | Priority |
|------------|----------|
| "urgent", "ASAP", "critical", "blocking" | critical |
| "need to", "must", "important" | high |
| "should", "would be nice", "plan for" | medium |
| "someday", "eventually", "future" | low |

---

## Task Type Inference

The planner infers task type from action words:

| Action Words | Task Type |
|--------------|-----------|
| fix, repair, debug | fix |
| implement, build, create | implement |
| refactor, clean up, improve code | refactor |
| analyze, investigate, understand | analyze |
| organize, consolidate, structure | organize |
| research, explore, learn about | research |
| improve, optimize, enhance | improve |
| optimize, speed up, reduce latency | optimize |

---

## Usage Examples

### Example 1: Fix Request
**Input:** "I need to fix the YouTube scraper"

**Output:** Creates `TASK-20260210-192900-fix-youtube-scraper.md`
- Type: fix
- Priority: high (inferred from "need to")
- Includes research phase for diagnosing the issue
- Implementation steps for fixing the scraper
- Testing checklist for verifying the fix

### Example 2: Improvement Planning
**Input:** "Make a plan for improving RALF loops"

**Output:** Creates `TASK-20260210-193000-improve-ralf-loops.md`
- Type: improve
- Priority: medium (inferred from "plan for")
- Research phase for understanding current loop behavior
- Implementation steps for optimizations
- Success criteria for measuring improvement

### Example 3: Status Inquiry
**Input:** "What's the status of the dashboard?"

**Output:**
- Checks active tasks for dashboard-related work
- Reports current progress
- Identifies any blockers or issues

---

## Conversation Flow

### When SISO Requests a Plan:

1. **Parse Request** - Extract task name, type, priority, context
2. **Generate Task ID** - Create unique ID: `TASK-YYYYMMDD-HHMMSS-[slug-name]`
3. **Create Task Directory** - `/opt/blackbox5/5-project-memory/blackbox5/tasks/active/TASK-ID/`
4. **Write Task File** - Generate `task.md` with complete structure
5. **Confirm Creation** - "Created TASK-XXXXXX: [Task Name] with [N] steps"
6. **Track Active Work** - Remember what SISO is working on

### When SISO Asks for Status:

1. **Query Active Tasks** - Scan tasks/active/ for relevant tasks
2. **Read Task Files** - Check status, progress, notes
3. **Report Findings** - Provide update on what's in progress
4. **Identify Next Steps** - Suggest what to do next

---

## State Management

The planner tracks:
- **Active tasks** - Tasks created and not yet completed
- **Work in progress** - What SISO is currently working on
- **Conversation context** - Recent requests for better parsing

State is maintained in:
- `/opt/blackbox5/5-project-memory/blackbox5/tasks/active/` - Active task files
- Memory can be enhanced with a tracking file (optional)

---

## Integration with BlackBox5

The planner integrates with the existing BlackBox5 task system:

1. **Task Directory Structure** - Uses standard BlackBox5 task locations
2. **Task Format** - Follows BlackBox5 task template conventions
3. **Task Lifecycle** - Supports pending → in_progress → completed flow
4. **Commands Compatible** - Tasks created can be managed via `bb5 task:list`

---

## Success Criteria

The conversational planner is successful when:
- [ ] Natural language requests are parsed correctly (>90% accuracy)
- [ ] Generated tasks follow BlackBox5 format exactly
- [ ] Task IDs are unique and follow naming convention
- [ ] Priority and type inference is reasonable
- [ ] Status inquiries provide useful information
- [ ] Task files are created in correct location
- [ ] Example task plans demonstrate the system

---

## Limitations

- **Complex Dependencies** - Planner assumes single-task focus; multi-task dependencies require manual coordination
- **Technical Details** - May miss specific implementation details without follow-up
- **Context Loss** - Long conversations may lose context without memory persistence
- **Ambiguous Requests** - Very vague requests may need clarification

---

## Enhancement Ideas

Future improvements could include:
- Multi-task plan generation (breaking large requests into subtasks)
- Automatic dependency detection between tasks
- Integration with `bb5` CLI for task management
- Persistent conversation memory for better context
- Automatic time estimation based on similar past tasks

---

## Testing the Planner

To test the planner, try these conversations:

```bash
# Simulate natural requests
"I need to fix the authentication bug"
"Make a plan for optimizing the database queries"
"Plan for improving the user dashboard"
"Task for implementing the new API endpoint"
"Work on refactoring the payment module"

# Test status inquiries
"What's the status of the authentication bug fix?"
"How's the dashboard optimization going?"
```

---

## See Also

- `/opt/blackbox5/5-project-memory/blackbox5/tasks/README.md` - Task system documentation
- `/opt/blackbox5/5-project-memory/blackbox5/tasks/template/task.md` - Task template
- `/opt/blackbox5/5-project-memory/blackbox5/tasks/active/` - Example active tasks
