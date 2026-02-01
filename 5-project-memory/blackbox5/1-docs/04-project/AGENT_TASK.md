# BlackBox5 Agent Task - PLAN-008

You are working on the BlackBox5 AI development platform.

## CRITICAL: Fix API Mismatches in main.py

The system CANNOT PROCESS ANY REQUEST due to 3 API parameter mismatches.

### Issues to Fix:

1. **Line 450**: `Task(task_id=...)` → Should be `Task(id=...)`
2. **Line 612**: `execute_wave_based(...)` → Should be `execute_workflow(...)`
3. **Line 558**: `AgentTask(id=...)` → Should be `AgentTask(task_id=...)`
4. **Lines 392, 401, 457, 586, 614**: `task.task_id` → Should be `task.id`

### Steps:

1. Read blackbox5/6-roadmap/03-planned/PLAN-008-fix-critical-api-mismatches.md
2. Fix the 3 API mismatches in main.py
3. Test that system boots and processes requests
4. Document everything in blackbox5/6-roadmap/04-active/PLAN-008-fix-critical-api-mismatches/
5. Update Vibe Kanban task status to "done"

### Success Criteria:
- No TypeError or AttributeError
- System can process simple requests
- All changes documented

Start by reading the plan document!
