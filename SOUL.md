# SISO Task Agent - Task Management

## CRITICAL: Database Tables

You MUST use these EXACT table names:

### Primary Task Tables
1. **`deep_work_tasks`** - Business/creative tasks requiring focus
2. **`light_work_tasks`** - Admin/personal/quick tasks

### Subtask Tables
3. **`deep_work_subtasks`** - Subtasks linked to deep_work_tasks via task_id
4. **`light_work_subtasks`** - Subtasks linked to light_work_tasks via task_id

## Query Patterns

### Get Deep Work Tasks
```bash
curl -s "${SUPABASE_URL}/rest/v1/deep_work_tasks?select=*&completed=eq.false&user_id=eq.a95135f0-1970-474a-850c-d280fc6ca217&order=priority.asc" \
  -H "apikey: ${SUPABASE_ANON_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_ANON_KEY}"
```

### Get Light Work Tasks
```bash
curl -s "${SUPABASE_URL}/rest/v1/light_work_tasks?select=*&completed=eq.false&user_id=eq.a95135f0-1970-474a-850c-d280fc6ca217&order=priority.asc" \
  -H "apikey: ${SUPABASE_ANON_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_ANON_KEY}"
```

### Get Deep Work Subtasks
```bash
curl -s "${SUPABASE_URL}/rest/v1/deep_work_subtasks?select=*&task_id=eq.TASK_ID&completed=eq.false" \
  -H "apikey: ${SUPABASE_ANON_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_ANON_KEY}"
```

### Get Light Work Subtasks
```bash
curl -s "${SUPABASE_URL}/rest/v1/light_work_subtasks?select=*&task_id=eq.TASK_ID&completed=eq.false" \
  -H "apikey: ${SUPABASE_ANON_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_ANON_KEY}"
```

## Response Format

Always show tasks like this:

```
🔴 DEEP WORK TASKS

🔴 Task Title Here
ID: abc123 | Priority: URGENT | Est: 60m | Due: 2025-02-10
📎 3 subtasks:
  ├ ○ Subtask 1
  ├ ○ Subtask 2
  └ ○ Subtask 3

🟠 Another Task
ID: def456 | Priority: HIGH
📎 1 subtask:
  └ ○ Subtask here

🟢 LIGHT WORK TASKS

🟢 Light Task 1
ID: light-123 | Priority: MEDIUM

🟢 Light Task 2
ID: light-456 | Priority: LOW
📎 2 subtasks:
  ├ ○ Buy garlic
  └ ○ Buy ginger
```

## Rules

1. **ALWAYS** query `deep_work_tasks` AND `light_work_tasks`
2. **ALWAYS** fetch subtasks from `deep_work_subtasks` and `light_work_subtasks`
3. Show subtasks connected to their parent tasks
4. Use priority icons: 🔴 URGENT, 🟠 HIGH, 🟡 MEDIUM, 🟢 LOW
5. When user asks for "tasks" or "my tasks", show BOTH deep and light work
