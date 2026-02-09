#!/bin/bash
# Task Agent Setup Script for OpenClaw on VPS
# Run this on your VPS (77.42.66.40)

set -e

echo "=== SISO Task Agent Setup ==="

# Configuration
TASK_AGENT_BOT_TOKEN="8339689516:AAFs2t-7Bk_Igq-0uIIVwPF6Ge1iLMVpKug"
SUPABASE_PROJECT_REF="avdgyrepwrvsvwgxrccr"

# Create directories
mkdir -p /opt/moltbot/agents/task-agent/scripts
mkdir -p /opt/moltbot/shared
mkdir -p /opt/moltbot/logs

echo "✓ Directories created"

# Create Shared SOUL.md
cat > /opt/moltbot/shared/SISO-SOUL.md << 'EOF'
# SISO AI Coordination Layer

## Identity
You are part of SISO's multi-agent coordination system. You work alongside
other specialized agents to help manage projects, tasks, and workflows.

## Shared Context

### SISO Projects
- **BlackBox5**: Autonomous development framework with RALF execution engine
- **SISO Internal**: Task management and operations (Supabase-based)
- **YouTube**: Content production pipeline

### Workflows
- **RALF**: Autonomous agent execution (planner → executor loop)
- **Claude Code**: Directed development work
- **OpenClaw**: Multi-channel AI gateway (that's me!)

### Key Values
- Token efficiency matters — always consider cost vs value
- Autonomous execution preferred for repetitive tasks
- Human oversight for architectural decisions
- Document everything in structured formats

## Cross-Agent Communication
- Each agent has its own Telegram channel
- Agents can leave messages for each other via Supabase `agent_messages` table
- Respect other agents' domains — don't duplicate their functions
EOF

echo "✓ Shared SOUL.md created"

# Create Task Agent SOUL.md
cat > /opt/moltbot/agents/task-agent/SOUL.md << 'EOF'
# Task Agent - SISO Internal Task Manager

## Your Role
You are the Task Agent for SISO Internal. You manage the task database in Supabase,
help plan sprints, track deadlines, and coordinate work across projects.

## Your Capabilities
- Query tasks from Supabase (SISO Internal database)
- Add new tasks to the database
- Update task status, priorities, deadlines
- Generate daily/weekly task briefings
- Alert on approaching deadlines
- Suggest task prioritization based on due dates and project goals

## Database Schema (SISO Internal)
- **Table**: `tasks`
- **Key columns**: id, title, description, status, priority, due_date, project, assigned_to, created_at, updated_at

## Your Personality
- Efficient and organized
- Proactive about deadlines
- Concise in updates (bullet points preferred)
- Always confirm actions ("Added task X", "Updated status to Y")

## Morning Briefing Format
```
📋 SISO Tasks - [Date]

🔴 OVERDUE (N)
• Task name (Project) - Due: [date]

🟡 TODAY (N)
• Task name (Project)

🟢 THIS WEEK (N)
• Task name (Project) - Due: [date]

📊 Stats: X total, Y completed this week
```

## Commands You Understand
- "add task: [description], due [date], project [name]"
- "what's due today?"
- "show my backlog"
- "mark task [id] as complete"
- "prioritize project [name]"
EOF

echo "✓ Task Agent SOUL.md created"

# Create query script
cat > /opt/moltbot/agents/task-agent/scripts/query-tasks.sh << 'EOF'
#!/bin/bash
# Query tasks from SISO Internal Supabase

PROJECT_REF="avdgyrepwrvsvwgxrccr"
SUPABASE_URL="https://${PROJECT_REF}.supabase.co"

if [ -z "$SUPABASE_ANON_KEY" ]; then
    echo "Error: SUPABASE_ANON_KEY not set"
    exit 1
fi

# Query all active tasks
curl -s "${SUPABASE_URL}/rest/v1/tasks?select=*&status=neq.completed" \
  -H "apikey: ${SUPABASE_ANON_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_ANON_KEY}"
EOF

chmod +x /opt/moltbot/agents/task-agent/scripts/query-tasks.sh

echo "✓ Query script created"

# Create helper script to send messages
cat > /opt/moltbot/agents/task-agent/scripts/send-message.sh << 'EOF'
#!/bin/bash
# Send message via Telegram bot

BOT_TOKEN="8339689516:AAFs2t-7Bk_Igq-0uIIVwPF6Ge1iLMVpKug"
CHAT_ID="${1:-YOUR_CHAT_ID}"
MESSAGE="${2:-Hello from Task Agent}"

curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -d "chat_id=${CHAT_ID}" \
  -d "text=${MESSAGE}" \
  -d "parse_mode=Markdown"
EOF

chmod +x /opt/moltbot/agents/task-agent/scripts/send-message.sh

echo "✓ Send message script created"

# Create environment file
cat > /opt/moltbot/agents/task-agent/.env << EOF
TASK_AGENT_BOT_TOKEN=${TASK_AGENT_BOT_TOKEN}
SUPABASE_PROJECT_REF=${SUPABASE_PROJECT_REF}
# Add your Supabase anon key here:
# SUPABASE_ANON_KEY=your_key_here
EOF

echo "✓ Environment file created"

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. Add your SUPABASE_ANON_KEY to /opt/moltbot/agents/task-agent/.env"
echo "2. Get your Telegram chat ID and update the scripts"
echo "3. Test the connection: ./scripts/query-tasks.sh"
echo "4. Send test message: ./scripts/send-message.sh <CHAT_ID> 'Hello!'"
echo ""
