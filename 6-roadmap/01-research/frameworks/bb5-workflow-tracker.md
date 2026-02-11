# BB5 Workflow Tracker (Simplified Observability)

**Purpose:** Track workflow progress across BB5 agents without noise

## What We Track

| Event | When | Why |
|-------|------|-----|
| `session_start` | Agent begins task | Know who's working on what |
| `workflow_step_start` | Subagent starts a step | Track workflow progress |
| `workflow_step_complete` | Subagent finishes | Know when steps complete |
| `session_complete` | Task done | Completion tracking |
| `git_push` | Code pushed to GitHub | Deployment tracking |

## What We DON'T Track

- ❌ Every tool use (too noisy)
- ❌ Permission requests (not relevant)
- ❌ Context compaction (internal)
- ❌ Pre/post tool use (implementation detail)

## Architecture (Simplified)

```
RALF Executor → Hook Script → Redis → Dashboard
     ↓              ↓            ↓         ↓
   Task Start    Python      Stream    Web UI
   Step 1        Script      (XADD)    (Simple)
   Step 2
   Complete
```

## Hook Implementation

### 1. Session Start Hook

```python
#!/usr/bin/env python3
# ~/.claude/hooks/session_start.py

import json
import sys
import redis
from datetime import datetime

def track_session_start():
    """Track when an agent session starts"""
    input_data = json.load(sys.stdin)

    r = redis.Redis(host='localhost', port=6379, db=0)

    event = {
        'type': 'session_start',
        'session_id': input_data.get('session_id'),
        'agent_type': input_data.get('agent_type', 'unknown'),
        'task': extract_task_from_context(input_data),
        'timestamp': datetime.now().isoformat(),
        'workflow_id': get_workflow_id(input_data)
    }

    # Add to stream
    r.xadd('bb5:workflow:events', event)

    # Set active session
    r.hset('bb5:active:sessions', event['session_id'], json.dumps(event))

if __name__ == '__main__':
    track_session_start()
```

### 2. Workflow Step Tracking

```python
#!/usr/bin/env python3
# ~/.claude/hooks/subagent_start.py

import json
import sys
import redis

def track_workflow_step():
    """Track when a workflow step (subagent) starts"""
    input_data = json.load(sys.stdin)

    r = redis.Redis(host='localhost', port=6379, db=0)

    event = {
        'type': 'workflow_step_start',
        'session_id': input_data.get('session_id'),
        'step_name': input_data.get('agent_id', 'unknown'),
        'step_number': get_step_number(input_data),
        'parent_session': input_data.get('parent_session'),
        'timestamp': datetime.now().isoformat()
    }

    r.xadd('bb5:workflow:events', event)

    # Update workflow progress
    workflow_id = get_workflow_id(input_data)
    r.hincrby(f'bb5:workflow:{workflow_id}:progress', 'steps_started', 1)

if __name__ == '__main__':
    track_workflow_step()
```

### 3. Session Complete

```python
#!/usr/bin/env python3
# ~/.claude/hooks/session_end.py

import json
import sys
import redis

def track_session_complete():
    """Track when an agent completes their task"""
    input_data = json.load(sys.stdin)

    r = redis.Redis(host='localhost', port=6379, db=0)

    session_id = input_data.get('session_id')

    # Get session start info
    session_data = r.hget('bb5:active:sessions', session_id)
    if session_data:
        session = json.loads(session_data)
        duration = calculate_duration(session['timestamp'])

        event = {
            'type': 'session_complete',
            'session_id': session_id,
            'agent_type': session.get('agent_type'),
            'task': session.get('task'),
            'duration_seconds': duration,
            'result': input_data.get('reason', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }

        r.xadd('bb5:workflow:events', event)

        # Remove from active
        r.hdel('bb5:active:sessions', session_id)

        # Update workflow completion
        workflow_id = session.get('workflow_id')
        if workflow_id:
            r.hincrby(f'bb5:workflow:{workflow_id}:progress', 'steps_completed', 1)

if __name__ == '__main__':
    track_session_complete()
```

## Dashboard (Simple)

```html
<!-- Simple dashboard showing workflow progress -->
<!DOCTYPE html>
<html>
<head>
    <title>BB5 Workflow Tracker</title>
    <script src="https://unpkg.com/vue@3"></script>
</head>
<body>
    <div id="app">
        <h1>BB5 Workflow Status</h1>

        <!-- Active Workflows -->
        <div class="workflows">
            <div v-for="workflow in activeWorkflows" :key="workflow.id"
                 class="workflow-card">
                <h3>{{ workflow.name }}</h3>
                <div class="progress">
                    Step {{ workflow.current_step }} of {{ workflow.total_steps }}
                    <div class="progress-bar">
                        <div class="fill" :style="{width: workflow.percent + '%'}"></div>
                    </div>
                </div>
                <div class="agents">
                    <span v-for="agent in workflow.agents" :key="agent.id"
                          :class="['agent-badge', agent.status]">
                        {{ agent.name }}: {{ agent.status }}
                    </span>
                </div>
            </div>
        </div>

        <!-- Recent Events -->
        <div class="events">
            <h2>Recent Activity</h2>
            <div v-for="event in recentEvents" :key="event.id" class="event">
                <span class="timestamp">{{ event.timestamp }}</span>
                <span class="type">{{ event.type }}</span>
                <span class="details">{{ event.task || event.step_name }}</span>
            </div>
        </div>
    </div>

    <script>
        const { createApp } = Vue;

        createApp({
            data() {
                return {
                    activeWorkflows: [],
                    recentEvents: []
                }
            },
            mounted() {
                // Connect to Redis via WebSocket proxy
                this.connectToEvents();
            },
            methods: {
                connectToEvents() {
                    const ws = new WebSocket('ws://vps:4000/ws');
                    ws.onmessage = (msg) => {
                        const event = JSON.parse(msg.data);
                        this.handleEvent(event);
                    };
                },
                handleEvent(event) {
                    this.recentEvents.unshift(event);
                    if (this.recentEvents.length > 50) {
                        this.recentEvents.pop();
                    }

                    // Update workflow progress
                    if (event.workflow_id) {
                        this.updateWorkflow(event);
                    }
                }
            }
        }).mount('#app');
    </script>
</body>
</html>
```

## Redis Schema (Simplified)

```
# Event Stream (all events)
bb5:workflow:events → Redis Stream
  - type: session_start | workflow_step_start | workflow_step_complete | session_complete
  - session_id
  - workflow_id
  - timestamp
  - [task | step_name | duration | result]

# Active Sessions
bb5:active:sessions → Hash
  session_id → {agent_type, task, workflow_id, start_time}

# Workflow Progress
bb5:workflow:{id}:progress → Hash
  steps_total: 5
  steps_started: 3
  steps_completed: 2
  status: in_progress | complete | failed

# Git Activity
bb5:git:pushes → Stream
  - repo
  - branch
  - commit_count
  - timestamp
```

## Usage Example

```bash
# Start workflow
ralf-workflow --name "Research Pipeline" --steps 4

# Dashboard shows:
# ┌─────────────────────────────────────┐
# │ Research Pipeline                   │
# │ Step 2 of 4 [████████░░░░] 50%     │
# │                                     │
# │ scout: complete ✓                  │
# │ analyst: working ◐                 │
# │ planner: waiting ○                 │
# │ executor: waiting ○                │
# └─────────────────────────────────────┘

# Recent Activity:
# 14:32:23 scout completed analysis
# 14:30:15 analyst started ranking
# 14:28:01 workflow started
```

## Deployment

```bash
# 1. Install hooks
sudo -u bb5-runner cp hooks/*.py ~/.claude/hooks/

# 2. Start simple server
sudo -u bb5-runner python3 bb5-workflow-server.py

# 3. Access dashboard
open http://vps:8080
```

## Benefits

- ✅ Track workflow progress at a glance
- ✅ See which agents are working
- ✅ Know when tasks complete
- ✅ Monitor git activity
- ✅ No noise from tool calls
- ✅ Simple, fast, focused
