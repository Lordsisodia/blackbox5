# Task Agent Tools

## Supabase Database Access

Environment variables available:
- `SUPABASE_URL=https://avdgyrepwrvsvwgxrccr.supabase.co`
- `SUPABASE_ANON_KEY` - For API access

### Query Tasks (using curl)

**Deep Work Tasks:**
```bash
curl -s "${SUPABASE_URL}/rest/v1/deep_work_tasks?select=*&completed=eq.false&user_id=eq.a95135f0-1970-474a-850c-d280fc6ca217&order=priority.asc" \
  -H "apikey: ${SUPABASE_ANON_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_ANON_KEY}"
```

**Light Work Tasks:**
```bash
curl -s "${SUPABASE_URL}/rest/v1/light_work_tasks?select=*&completed=eq.false&user_id=eq.a95135f0-1970-474a-850c-d280fc6ca217&order=priority.asc" \
  -H "apikey: ${SUPABASE_ANON_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_ANON_KEY}"
```

**Subtasks for a Task:**
```bash
curl -s "${SUPABASE_URL}/rest/v1/deep_work_subtasks?select=*&task_id=eq.TASK_ID&completed=eq.false" \
  -H "apikey: ${SUPABASE_ANON_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_ANON_KEY}"
```

### Create Tasks

**Deep Work Task:**
```bash
curl -s -X POST "${SUPABASE_URL}/rest/v1/deep_work_tasks" \
  -H "apikey: ${SUPABASE_ANON_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_ANON_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"title": "Task Name", "priority": "HIGH", "user_id": "a95135f0-1970-474a-850c-d280fc6ca217", "completed": false}'
```

**Light Work Task:**
```bash
curl -s -X POST "${SUPABASE_URL}/rest/v1/light_work_tasks" \
  -H "apikey: ${SUPABASE_ANON_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_ANON_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"title": "Task Name", "priority": "MEDIUM", "user_id": "a95135f0-1970-474a-850c-d280fc6ca217", "completed": false}'
```

**Subtask:**
```bash
curl -s -X POST "${SUPABASE_URL}/rest/v1/deep_work_subtasks" \
  -H "apikey: ${SUPABASE_ANON_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_ANON_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"task_id": "TASK_ID", "title": "Subtask Name", "completed": false}'
```

### Complete Tasks

```bash
curl -s -X PATCH "${SUPABASE_URL}/rest/v1/deep_work_tasks?id=eq.TASK_ID" \
  -H "apikey: ${SUPABASE_ANON_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_ANON_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

## Helper Scripts

Scripts available in `/opt/moltbot/agents/task-agent/scripts/`:
- `show-deep-work.sh` - Show deep work tasks
- `show-light-work.sh` - Show light work tasks
- `task-manager.sh` - Full task management

## Response Format

Always format task lists as:
```
🔴 *Task Title*
ID: `abc123...` | Priority: URGENT | Est: 60m
📎 3 subtasks:
  ├ ○ Subtask 1
  └ ○ Subtask 2
```
