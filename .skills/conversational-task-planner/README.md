# Conversational Task Planner - User Guide

**Version:** 1.0.0
**Skill:** `conversational-task-planner`

---

## Quick Start

The Conversational Task Planner works automatically. Just talk to the main agent (SISO) in natural language, and it will create BlackBox5 task plans for you.

### Example Interactions

```bash
# Create a task
SISO: "I need to fix the YouTube scraper"
→ Creates: TASK-20260210-192900-fix-youtube-scraper.md

# Plan improvements
SISO: "Make a plan for improving RALF loops"
→ Creates: TASK-20260210-193000-improve-ralf-loops.md

# Check status
SISO: "What's the status of the dashboard?"
→ Reports: Current progress on dashboard implementation
```

---

## How It Works

### 1. Listen to Conversation

The planner monitors conversation for task-related phrases:

**Task Creation Triggers:**
- "make a plan for X"
- "I need to fix/implement/build X"
- "create a task for X"
- "work on X"

**Status Inquiries:**
- "status of X"
- "what's the status of X"
- "how's X going"

### 2. Parse and Infer

The planner extracts:
- **Task Name**: What needs to be done
- **Task Type**: fix, implement, improve, refactor, etc.
- **Priority**: critical, high, medium, low (inferred from language)
- **Context**: Additional details from conversation

### 3. Generate Task Plan

The planner creates a complete BlackBox5 task with:
- Research/analysis phase
- Implementation steps
- Testing checklist
- Success criteria
- Rollback strategy

### 4. Track Progress

The planner remembers:
- Active tasks created
- What you're currently working on
- Task progress when asked

---

## Task Location

Tasks are created in:
```
/opt/blackbox5/5-project-memory/blackbox5/tasks/active/
```

Each task is in its own directory:
```
active/TASK-20260210-192900-fix-youtube-scraper/
└── task.md
```

---

## Task Structure

Generated tasks follow the BlackBox5 template:

```markdown
# TASK-[timestamp]: [Task Name]

**Status:** pending
**Priority:** HIGH|MEDIUM|LOW
**Type:** fix|implement|improve|etc.
**Created:** YYYY-MM-DDTHH:MM:SSZ
**Estimated Lines:** [NUMBER]

## Objective
[Clear statement of what needs to be done]

## Research & Analysis Phase
- [ ] Research the problem
- [ ] Analyze current state
- [ ] Document findings

## Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

## Implementation Approach
[Step-by-step plan]

## Testing Checklist
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual verification complete

## Context
[Background information]

## Files to Modify/Create
- [List of files]

## Rollback Strategy
[How to undo changes]

## Notes
[Any warnings or additional context]
```

---

## Priority Inference

The planner determines priority from language:

| Phrase | Priority |
|--------|----------|
| "urgent", "ASAP", "critical" | critical |
| "need to", "must", "important" | high |
| "should", "plan for" | medium |
| "someday", "eventually" | low |

---

## Task Type Inference

The planner determines task type from action words:

| Phrase | Type |
|--------|------|
| "fix", "repair", "debug" | fix |
| "implement", "build", "create" | implement |
| "refactor", "clean up" | refactor |
| "analyze", "investigate" | analyze |
| "improve", "optimize" | improve |
| "research", "explore" | research |

---

## Managing Tasks

### View All Active Tasks
```bash
bb5 task:list
```

### View a Specific Task
```bash
cat /opt/blackbox5/5-project-memory/blackbox5/tasks/active/TASK-XXXX/task.md
```

### Mark Task as In Progress
Edit the task.md file:
```markdown
**Status:** in_progress
```

### Mark Task as Complete
1. Edit task.md:
```markdown
**Status:** completed
```
2. Move to completed directory:
```bash
mv /opt/blackbox5/5-project-memory/blackbox5/tasks/active/TASK-XXXX \
   /opt/blackbox5/5-project-memory/blackbox5/tasks/completed/
```

---

## Example Workflows

### Workflow 1: Fix a Bug
```bash
# 1. Describe the problem
SISO: "I need to fix the authentication bug in the login system"

# 2. Planner creates task
→ TASK-20260210-200000-fix-authentication-bug.md

# 3. Start working
# Edit task.md to change status to "in_progress"

# 4. Complete the work
# Run tests, verify fix

# 5. Mark as complete
# Edit task.md: **Status:** completed
# Move to completed/
```

### Workflow 2: Plan a Feature
```bash
# 1. Request a plan
SISO: "Make a plan for implementing user notifications"

# 2. Planner creates task
→ TASK-20260210-201000-implement-user-notifications.md

# 3. Review the generated plan
# Read task.md to see research phase and approach

# 4. Implement following the plan
# Follow the Implementation Approach section

# 5. Complete when done
# Mark all success criteria as checked
```

### Workflow 3: Check Status
```bash
# 1. Ask for status
SISO: "What's the status of the YouTube scraper?"

# 2. Planner checks active tasks
# Finds: TASK-20260210-192900-fix-youtube-scraper.md

# 3. Reports progress
→ "The YouTube scraper fix is in progress. Currently working on updating
   selectors. 3/5 implementation steps complete. Testing pending."
```

---

## Best Practices

### 1. Be Specific
```
✓ "I need to fix the YouTube scraper that's failing on long videos"
✗ "Fix the scraper"
```

### 2. Provide Context
```
✓ "Make a plan for improving RALF loops - they're running too slowly"
✗ "Improve RALF loops"
```

### 3. Update Task Progress
Edit the task.md file as you work:
- Add notes about what you've done
- Check off completed success criteria
- Update status when you start/finish

### 4. Use Status Inquiries
Check progress without navigating directories:
```
"What's the status of the dashboard implementation?"
"How's the authentication fix going?"
```

---

## Advanced Usage

### Custom Task Names
The planner generates a slug from your request:
```
"I need to fix the YouTube scraper"
→ TASK-20260210-192900-fix-youtube-scraper
```

You can also specify a task name:
```
"Create a task for AUTH-001: Fix login timeout"
→ TASK-20260210-192900-AUTH-001-fix-login-timeout
```

### Multiple Tasks in One Request
If you mention multiple things, the planner will ask for clarification:
```
SISO: "Fix the YouTube scraper and improve RALF loops"
→ "I can create tasks for both. Which should I start with, or
    should I create both?"
```

### Status Summary
```
SISO: "What am I working on?"
→ Lists all active tasks with their current status
```

---

## Troubleshooting

### Task Not Created
- Check if your request was clear and complete
- Try rephrasing with more specific language
- Ensure you used a trigger phrase (e.g., "need to", "make a plan for")

### Wrong Priority Inferred
- Edit the task.md file to adjust priority
- Use clearer language ("urgent", "ASAP", "should")

### Wrong Task Type
- Edit the task.md file to change type
- Use more specific action words ("implement" vs "fix")

### Task Too Generic
- Add more context to your request
- Ask the planner to regenerate with more details

---

## Integration with bb5 Commands

The planner works seamlessly with existing BlackBox5 commands:

```bash
# List all active tasks (includes planner-created tasks)
bb5 task:list

# View task details
bb5 task:show TASK-20260210-192900-fix-youtube-scraper

# Mark task as in progress
bb5 task:start TASK-20260210-192900-fix-youtube-scraper

# Mark task as complete
bb5 task:complete TASK-20260210-192900-fix-youtube-scraper
```

---

## Example Tasks

See the `examples/` directory for complete task plans generated from natural conversation:

- `TASK-20260210-192900-fix-youtube-scraper/` - Bug fix task
- `TASK-20260210-193000-improve-ralf-loops/` - Performance improvement task
- `TASK-20260210-193100-implement-user-dashboard/` - Feature implementation task

---

## Feedback and Improvement

The planner learns from context. If you notice patterns in how you phrase requests:

- Use consistent language for similar task types
- Provide the same context you'd want in a task plan
- Give feedback if the planner misses important details

Future enhancements may include:
- Learning from your task creation patterns
- Automatically suggesting related tasks
- Integrating with code analysis to suggest files to modify

---

## FAQ

**Q: Can I edit the generated task?**
A: Yes! Task files are just Markdown. Edit them directly.

**Q: How does the planner know which files to modify?**
A: It infers from the task context. You can edit the task.md to add/remove files.

**Q: What if I need more detailed planning?**
A: The planner creates a solid foundation. You can expand sections (approach, testing, etc.) as needed.

**Q: Can I create tasks without the planner?**
A: Yes! You can manually create task.md files in the tasks/active/ directory.

**Q: Does the planner automatically track progress?**
A: No. You update the task.md file as you work. The planner can read and report progress when asked.

---

## See Also

- `SKILL.md` - Skill documentation and technical details
- `examples/` - Example task plans
- `/opt/blackbox5/5-project-memory/blackbox5/tasks/README.md` - BlackBox5 task system
- `/opt/blackbox5/5-project-memory/blackbox5/tasks/template/task.md` - Task template
