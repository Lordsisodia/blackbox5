# Task Agent Tools

## CRITICAL: Use These Exact Table Names

- `deep_work_tasks` - NOT "tasks" or "deep_tasks"
- `light_work_tasks` - NOT "light_tasks"
- `deep_work_subtasks` - NOT "subtasks"
- `light_work_subtasks` - NOT "light_subtasks"

## Supabase Environment

```bash
SUPABASE_URL=https://avdgyrepwrvsvwgxrccr.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF2ZGd5cmVwd3J2c3Z3Z3hyY2NyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM2MzgwODIsImV4cCI6MjA1OTIxNDA4Mn0.8MZ2etAhQ1pTJnK84uoqAFfUirv_kaoYcmKHhKgLAWU
USER_ID=a95135f0-1970-474a-850c-d280fc6ca217
```

## Query Commands

### Get All Deep Work Tasks
```bash
curl -s "${SUPABASE_URL}/rest/v1/deep_work_tasks?select=*&completed=eq.false&user_id=eq.${USER_ID}&order=priority.asc" \
  -H "apikey: ${SUPABASE_ANON_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_ANON_KEY}"
```

### Get All Light Work Tasks
```bash
curl -s "${SUPABASE_URL}/rest/v1/light_work_tasks?select=*&completed=eq.false&user_id=eq.${USER_ID}&order=priority.asc" \
  -H "apikey: ${SUPABASE_ANON_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_ANON_KEY}"
```

### Get Deep Work Subtasks for a Task
```bash
curl -s "${SUPABASE_URL}/rest/v1/deep_work_subtasks?select=*&task_id=eq.TASK_ID&completed=eq.false" \
  -H "apikey: ${SUPABASE_ANON_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_ANON_KEY}"
```

### Get Light Work Subtasks for a Task
```bash
curl -s "${SUPABASE_URL}/rest/v1/light_work_subtasks?select=*&task_id=eq.TASK_ID&completed=eq.false" \
  -H "apikey: ${SUPABASE_ANON_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_ANON_KEY}"
```

### Create Deep Work Task
```bash
curl -s -X POST "${SUPABASE_URL}/rest/v1/deep_work_tasks" \
  -H "apikey: ${SUPABASE_ANON_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_ANON_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"title": "Task Name", "priority": "HIGH", "user_id": "'${USER_ID}'", "completed": false}'
```

### Create Light Work Task
```bash
curl -s -X POST "${SUPABASE_URL}/rest/v1/light_work_tasks" \
  -H "apikey: ${SUPABASE_ANON_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_ANON_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"title": "Task Name", "priority": "MEDIUM", "user_id": "'${USER_ID}'", "completed": false}'
```

### Create Subtask
```bash
curl -s -X POST "${SUPABASE_URL}/rest/v1/deep_work_subtasks" \
  -H "apikey: ${SUPABASE_ANON_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_ANON_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"task_id": "TASK_ID", "title": "Subtask Name", "completed": false}'
```

### Mark Task Complete
```bash
curl -s -X PATCH "${SUPABASE_URL}/rest/v1/deep_work_tasks?id=eq.TASK_ID" \
  -H "apikey: ${SUPABASE_ANON_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_ANON_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

## Helper Scripts

Available in `/opt/moltbot/agents/task-agent/scripts/`:
- `show-deep-work.sh` - Query deep_work_tasks
- `show-light-work.sh` - Query light_work_tasks
- `task-manager.sh` - Full CRUD operations

## Response Format

Always format as:
```
🔴 DEEP WORK TASKS

🔴 Task Title
ID: abc123 | Priority: URGENT | Est: 60m
📎 2 subtasks:
  ├ ○ Subtask 1
  └ ○ Subtask 2

🟢 LIGHT WORK TASKS

🟢 Light Task
ID: light-123 | Priority: MEDIUM
📎 1 subtask:
  └ ○ Buy garlic
```
