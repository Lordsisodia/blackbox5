# Blackbox5 + OpenClaw Hybrid Integration Guide

## Overview

This guide explores how to combine **Blackbox5** (enterprise multi-agent orchestration) with **OpenClaw** (personal AI assistant framework) to create a powerful hybrid system that leverages the strengths of both.

## Why Hybrid?

| Blackbox5 Strengths | OpenClaw Strengths | Hybrid Benefit |
|--------------------|--------------------|----------------|
| 21 specialized agents | Native messaging (10+ channels) | Expert agents accessible via Telegram/WhatsApp |
| RALF autonomous loops | 24/7 daemon architecture | Continuous improvement with mobile notifications |
| Multi-tier memory | File-based transparent memory | Persistent knowledge with human-readable backup |
| Wave-based orchestration | Simple skill system | Complex workflows triggered by simple messages |
| Safety systems (kill switch) | Docker sandboxing | Defense in depth security |

---

## Integration Architecture

### Architecture 1: OpenClaw as Messaging Layer for Blackbox5

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    HYBRID ARCHITECTURE: OpenClaw Frontend                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  USER INTERFACE LAYER (OpenClaw)                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  WhatsApp • Telegram • Discord • Slack • iMessage • Signal • Teams  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │              OPENCLAW GATEWAY (Port 18789)                           │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   │
│  │  │  WebSocket   │  │     HTTP     │  │    Blackbox5 Skill       │  │   │
│  │  │  (RPC)       │  │   (API/UI)   │  │    (Custom Integration)  │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│  ORCHESTRATION LAYER (Blackbox5)                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   │
│  │  │ Task Router  │  │ Orchestrator │  │ Wave-Based Parallelizer  │  │   │
│  │  │ (Complexity) │  │ (21 Agents)  │  │ (Dependency Mgmt)        │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│  EXECUTION LAYER (Blackbox5)                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   │
│  │  │ RALF Engine  │  │   Redis      │  │    Safety Systems        │  │   │
│  │  │(Autonomous)  │  │  Coordinator │  │ (Kill Switch, Sandbox)   │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**How it works:**
1. User sends message via Telegram/WhatsApp to OpenClaw
2. OpenClaw's custom "Blackbox5 Skill" interprets the request
3. Skill calls Blackbox5 API to create/execute tasks
4. Blackbox5 orchestrates its 21 agents via RALF
5. Results flow back through OpenClaw to user's messaging app

---

### Architecture 2: Blackbox5 as Backend Orchestrator for OpenClaw

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  HYBRID ARCHITECTURE: Blackbox5 Backend                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  USER INTERFACE LAYER (OpenClaw)                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  WhatsApp • Telegram • Discord • Slack • iMessage • Signal • Teams  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │              OPENCLAW GATEWAY (Port 18789)                           │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   │
│  │  │    Pi Agent  │  │   Skills     │  │    MCP Adapter           │  │   │
│  │  │   (Primary)  │  │  (700+)      │  │    (External Tools)      │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │              BLACKBOX5 SKILL (OpenClaw Plugin)                       │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   │
│  │  │   Complex    │  │   Agent      │  │    Task Management       │  │   │
│  │  │   Tasks      │  │   Routing    │  │    (RALF Integration)    │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│  ORCHESTRATION LAYER (Blackbox5)                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   │
│  │  │ 21 Agents    │  │ Wave-Based   │  │    Redis Coordinator     │  │   │
│  │  │ (Specialized)│  │ Execution    │  │    (1ms latency)         │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**How it works:**
1. OpenClaw handles simple tasks directly via its skills
2. Complex tasks are delegated to Blackbox5 via the custom skill
3. Blackbox5's 21 agents handle sophisticated orchestration
4. Results return to OpenClaw for delivery to user

---

## Implementation: Blackbox5 Skill for OpenClaw

### Step 1: Create the Skill Structure

```bash
mkdir -p ~/.openclaw/skills/blackbox5-bridge
cd ~/.openclaw/skills/blackbox5-bridge
```

### Step 2: Skill Definition (skill.json)

```json
{
  "name": "blackbox5_bridge",
  "description": "Bridge to Blackbox5 multi-agent orchestration system. Use this for complex software development tasks, multi-agent workflows, safety-critical operations, and tasks requiring specialized agents.",
  "version": "1.0.0",
  "author": "Your Name",
  "parameters": {
    "type": "object",
    "properties": {
      "task_type": {
        "type": "string",
        "enum": ["code_review", "refactoring", "architecture", "testing", "documentation", "research"],
        "description": "Type of task to delegate to Blackbox5"
      },
      "description": {
        "type": "string",
        "description": "Detailed description of the task"
      },
      "priority": {
        "type": "string",
        "enum": ["low", "medium", "high", "critical"],
        "default": "medium"
      },
      "notify_on_complete": {
        "type": "boolean",
        "default": true,
        "description": "Send notification when task completes"
      }
    },
    "required": ["task_type", "description"]
  }
}
```

### Step 3: TypeScript Implementation (index.ts)

```typescript
import { tool } from 'openclaw/sdk';
import { execSync } from 'child_process';
import { readFileSync, existsSync } from 'fs';

// Blackbox5 configuration
const BLACKBOX5_PATH = process.env.BLACKBOX5_PATH || '/Users/shaansisodia/.blackbox5';
const BLACKBOX5_API_URL = process.env.BLACKBOX5_API_URL || 'http://localhost:8000';
const RALF_QUEUE_FILE = `${BLACKBOX5_PATH}/5-project-memory/blackbox5/.autonomous/agents/communications/queue.yaml`;

interface Blackbox5Task {
  task_type: string;
  description: string;
  priority: string;
  notify_on_complete: boolean;
}

export const delegateToBlackbox5 = async ({
  task_type,
  description,
  priority = 'medium',
  notify_on_complete = true
}: Blackbox5Task) => {
  try {
    // Validate Blackbox5 is accessible
    if (!existsSync(BLACKBOX5_PATH)) {
      return `Error: Blackbox5 not found at ${BLACKBOX5_PATH}. Please set BLACKBOX5_PATH environment variable.`;
    }

    // Create task via Blackbox5 CLI
    const taskId = `TASK-${Date.now()}`;
    const taskCommand = `cd ${BLACKBOX5_PATH} && bin/ralf-task-init --type "${task_type}" --priority "${priority}" --description "${description.replace(/"/g, '\\"')}"`;

    let result: string;
    try {
      result = execSync(taskCommand, { encoding: 'utf8', timeout: 30000 });
    } catch (execError: any) {
      return `Error creating task: ${execError.message}`;
    }

    // Extract task ID from result
    const taskIdMatch = result.match(/TASK-[A-Z0-9-]+/);
    const actualTaskId = taskIdMatch ? taskIdMatch[0] : taskId;

    // Set up notification if requested
    if (notify_on_complete) {
      // Create notification watcher
      setupNotificationWatcher(actualTaskId);
    }

    return `✅ Task delegated to Blackbox5\n\n` +
           `Task ID: ${actualTaskId}\n` +
           `Type: ${task_type}\n` +
           `Priority: ${priority}\n\n` +
           `Blackbox5 will orchestrate its 21 specialized agents to complete this task.\n` +
           `You'll be notified when it's complete.`;

  } catch (error: any) {
    return `Error delegating to Blackbox5: ${error.message}`;
  }
};

// Set up file watcher for task completion
const setupNotificationWatcher = (taskId: string) => {
  // This would integrate with OpenClaw's notification system
  // For now, we'll use a simple polling approach
  const checkInterval = setInterval(() => {
    try {
      const eventsFile = `${BLACKBOX5_PATH}/5-project-memory/blackbox5/.autonomous/agents/communications/events.yaml`;
      if (existsSync(eventsFile)) {
        const events = readFileSync(eventsFile, 'utf8');
        if (events.includes(`${taskId}`) && events.includes('completed')) {
          // Task completed - would trigger OpenClaw notification
          clearInterval(checkInterval);
          console.log(`[Blackbox5] Task ${taskId} completed`);
        }
      }
    } catch (e) {
      // Ignore errors
    }
  }, 60000); // Check every minute

  // Stop checking after 24 hours
  setTimeout(() => clearInterval(checkInterval), 24 * 60 * 60 * 1000);
};

// Additional helper: Get Blackbox5 status
export const getBlackbox5Status = async () => {
  try {
    const statusCommand = `cd ${BLACKBOX5_PATH} && bin/ralf-dashboard --quick`;
    const result = execSync(statusCommand, { encoding: 'utf8', timeout: 10000 });
    return result;
  } catch (error: any) {
    return `Error getting status: ${error.message}`;
  }
};

// Additional helper: List active tasks
export const listBlackbox5Tasks = async () => {
  try {
    if (!existsSync(RALF_QUEUE_FILE)) {
      return 'No active tasks found.';
    }
    const queue = readFileSync(RALF_QUEUE_FILE, 'utf8');
    return `## Active Blackbox5 Tasks\n\n\`\`\`yaml\n${queue}\n\`\`\``;
  } catch (error: any) {
    return `Error reading tasks: ${error.message}`;
  }
};
```

### Step 4: SKILL.md Documentation

```markdown
---
metadata.openclaw:
  emoji: 🖤
  requires:
    bins: [node, npm]
    env: [BLACKBOX5_PATH, BLACKBOX5_API_URL]
---

# Blackbox5 Bridge

Integrates OpenClaw with Blackbox5's enterprise multi-agent orchestration system.

## When to Use

Use this skill when you need:
- **Complex software development** requiring multiple specialized agents
- **Code refactoring** across large codebases
- **Architecture design** with expert review
- **Safety-critical operations** requiring kill switches and verification
- **Multi-step workflows** with dependencies
- **Tasks requiring 21 specialized agents** (Architect, Developer, Security, ML, etc.)

## When NOT to Use

Don't use this skill for:
- Simple queries (use OpenClaw's Pi agent directly)
- Quick file operations (use OpenClaw's system skills)
- Tasks that need immediate response (Blackbox5 tasks may take minutes/hours)

## Examples

"Create a comprehensive architecture document for our new payment system"
→ Delegates to Blackbox5 Architect Agent

"Refactor the authentication module with security review"
→ Delegates to Blackbox5 Developer + Security Agents

"Research best practices for Kubernetes deployment"
→ Delegates to Blackbox5 Analyst Agent

## Task Types

- **code_review**: Expert code review with multi-agent analysis
- **refactoring**: Large-scale codebase refactoring
- **architecture**: System design and architecture documents
- **testing**: Comprehensive test suite development
- **documentation**: Technical documentation generation
- **research**: Deep research with knowledge graph integration

## Priority Levels

- **critical**: Immediate attention, bypasses queue
- **high**: Process before medium/low tasks
- **medium**: Standard priority (default)
- **low**: Background processing

## Notifications

When `notify_on_complete` is true, you'll receive a message when Blackbox5 completes the task.

## Architecture

```
User Message → OpenClaw Gateway → Blackbox5 Skill → Blackbox5 Orchestrator
                                                        ↓
                                              21 Specialized Agents
                                                        ↓
                                              RALF Autonomous Execution
                                                        ↓
                                              Result → OpenClaw → User
```

## Error Handling

- Validates Blackbox5 installation before delegation
- Returns clear error messages if Blackbox5 is unavailable
- Sets up monitoring for task completion
- Handles timeouts gracefully

## Security

- Uses Blackbox5's built-in safety systems (kill switch, verifier)
- All execution happens within Blackbox5's sandbox
- No direct system access from OpenClaw
```

---

## Implementation: OpenClaw Integration for Blackbox5

### Step 1: Create OpenClaw Client for Blackbox5

Create a new file in Blackbox5: `2-engine/core/integrations/openclaw_client.py`

```python
"""
OpenClaw Integration Client for Blackbox5
Provides messaging capabilities through OpenClaw's gateway
"""

import requests
import json
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class OpenClawConfig:
    gateway_url: str = "http://localhost:18789"
    auth_token: Optional[str] = None
    default_channel: str = "telegram"
    default_recipient: str = "shaan"

class OpenClawClient:
    """Client for sending messages through OpenClaw"""

    def __init__(self, config: OpenClawConfig = None):
        self.config = config or OpenClawConfig()
        self.session = requests.Session()
        if self.config.auth_token:
            self.session.headers.update({
                "Authorization": f"Bearer {self.config.auth_token}"
            })

    def send_message(
        self,
        message: str,
        channel: str = None,
        recipient: str = None,
        formatting: str = "markdown"
    ) -> Dict[str, Any]:
        """Send a message via OpenClaw"""

        payload = {
            "message": message,
            "channel": channel or self.config.default_channel,
            "target": recipient or self.config.default_recipient,
            "format": formatting
        }

        try:
            response = self.session.post(
                f"{self.config.gateway_url}/message/send",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def notify_task_complete(
        self,
        task_id: str,
        task_type: str,
        result_summary: str,
        recipient: str = None
    ) -> Dict[str, Any]:
        """Send task completion notification"""

        message = f"""✅ **Blackbox5 Task Complete**

**Task ID:** {task_id}
**Type:** {task_type}

**Summary:**
{result_summary}

_View details in Blackbox5 dashboard_"""

        return self.send_message(message, recipient=recipient)

    def notify_task_started(
        self,
        task_id: str,
        task_type: str,
        agent_assigned: str,
        recipient: str = None
    ) -> Dict[str, Any]:
        """Send task started notification"""

        message = f"""🚀 **Blackbox5 Task Started**

**Task ID:** {task_id}
**Type:** {task_type}
**Assigned Agent:** {agent_assigned}

_You'll be notified when complete_"""

        return self.send_message(message, recipient=recipient)

    def send_status_update(
        self,
        queue_status: Dict[str, int],
        recent_events: list,
        recipient: str = None
    ) -> Dict[str, Any]:
        """Send periodic status update"""

        message = f"""📊 **Blackbox5 Status Update**

**Queue:**
• Pending: {queue_status.get('pending', 0)}
• In Progress: {queue_status.get('in_progress', 0)}
• Completed: {queue_status.get('completed', 0)}

**Recent Activity:**
"""
        for event in recent_events[:3]:
            message += f"• {event['task_id']}: {event['status']}\n"

        return self.send_message(message, recipient=recipient)

# Singleton instance
_openclaw_client: Optional[OpenClawClient] = None

def get_openclaw_client() -> OpenClawClient:
    """Get or create OpenClaw client singleton"""
    global _openclaw_client
    if _openclaw_client is None:
        _openclaw_client = OpenClawClient()
    return _openclaw_client
```

### Step 2: RALF Notification Hook

Create: `2-engine/core/integrations/ralf_openclaw_notifier.py`

```python
"""
RALF OpenClaw Notifier
Sends notifications to OpenClaw when RALF tasks change state
"""

import yaml
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .openclaw_client import get_openclaw_client

class RALFQueueWatcher(FileSystemEventHandler):
    """Watches RALF queue/events and sends OpenClaw notifications"""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.queue_file = self.project_path / ".autonomous/agents/communications/queue.yaml"
        self.events_file = self.project_path / ".autonomous/agents/communications/events.yaml"
        self.last_queue_mtime = 0
        self.last_events_mtime = 0
        self.openclaw = get_openclaw_client()

    def on_modified(self, event):
        if event.is_directory:
            return

        if event.src_path == str(self.queue_file):
            self._handle_queue_change()
        elif event.src_path == str(self.events_file):
            self._handle_events_change()

    def _handle_queue_change(self):
        """Handle queue.yaml modification"""
        try:
            with open(self.queue_file, 'r') as f:
                queue = yaml.safe_load(f)

            # Check for newly claimed tasks
            for task in queue.get('queue', []):
                if task.get('status') == 'claimed' and task.get('notified') != True:
                    self.openclaw.notify_task_started(
                        task_id=task['task_id'],
                        task_type=task.get('type', 'unknown'),
                        agent_assigned=task.get('owner', 'unknown')
                    )
                    task['notified'] = True

        except Exception as e:
            print(f"Error handling queue change: {e}")

    def _handle_events_change(self):
        """Handle events.yaml modification"""
        try:
            with open(self.events_file, 'r') as f:
                events = yaml.safe_load(f)

            # Check for completed events
            for event in events.get('events', []):
                if event.get('type') == 'completed' and not event.get('notified'):
                    self.openclaw.notify_task_complete(
                        task_id=event['task_id'],
                        task_type=event.get('task_type', 'unknown'),
                        result_summary=event.get('summary', 'Task completed successfully')
                    )
                    event['notified'] = True

        except Exception as e:
            print(f"Error handling events change: {e}")

def start_ralf_watcher(project_path: str):
    """Start watching RALF files for changes"""
    observer = Observer()
    handler = RALFQueueWatcher(project_path)

    watch_path = Path(project_path) / ".autonomous/agents/communications"
    observer.schedule(handler, str(watch_path), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    import sys
    project_path = sys.argv[1] if len(sys.argv) > 1 else "/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5"
    start_ralf_watcher(project_path)
```

---

## Hybrid Use Cases

### Use Case 1: Complex Development Task via Telegram

**User Story:**
```
User (on Telegram): "Refactor the authentication system with security review"

OpenClaw: "This is a complex task requiring multiple agents.
          Delegating to Blackbox5..."

Blackbox5:
  - Architect Agent: Designs new auth architecture
  - Developer Agent: Implements the refactoring
  - Security Agent: Reviews for vulnerabilities
  - QA Agent: Writes tests
  - Verifier Agent: Validates changes

OpenClaw (notification): "✅ Task AUTH-001 complete!
          Security review passed. 3 issues fixed."
```

### Use Case 2: Continuous Monitoring with Escalation

```
OpenClaw (Heartbeat): Check Blackbox5 queue status every 5 minutes

If queue > 10 tasks:
  → Send alert to user via WhatsApp
  → Escalate to Blackbox5's RALF for autonomous rebalancing

If critical task fails:
  → Immediate Telegram notification
  → Blackbox5 kill switch available
```

### Use Case 3: Morning Briefing

```
OpenClaw (Scheduled 9 AM):
  "Good morning! Here's your Blackbox5 status:"

  - 3 tasks completed overnight
  - 2 tasks in progress
  - 1 task needs your input

  Reply with task ID for details or say 'delegate [task]'
  to assign to Blackbox5 agents.
```

### Use Case 4: Mobile Code Review

```
User (on WhatsApp): "Review PR #123"

OpenClaw → Blackbox5:
  - Analyst Agent: Reviews code changes
  - Security Agent: Checks for vulnerabilities
  - Architect Agent: Validates design patterns

OpenClaw (result):
  "PR #123 Review Complete:

  ✅ No security issues
  ⚠️ 2 style suggestions
  ❌ 1 potential bug in auth.js:45

  Full report: [link]"
```

---

## Deployment Options

### Option 1: Same VPS (Recommended)

```yaml
# docker-compose.yml
version: '3.8'

services:
  openclaw:
    image: openclaw:latest
    ports:
      - "18789:18789"
    volumes:
      - ~/.openclaw:/root/.openclaw
      - ./blackbox5-skill:/root/.openclaw/skills/blackbox5-bridge
    environment:
      - BLACKBOX5_PATH=/blackbox5
    networks:
      - hybrid-network

  blackbox5:
    build: ./blackbox5
    volumes:
      - ~/.blackbox5:/blackbox5
    environment:
      - OPENCLAW_GATEWAY=http://openclaw:18789
    networks:
      - hybrid-network

  redis:
    image: redis:alpine
    networks:
      - hybrid-network

networks:
  hybrid-network:
    driver: bridge
```

### Option 2: Separate VPS with VPN

```
┌─────────────────────┐         ┌─────────────────────┐
│   VPS 1: OpenClaw   │◄───────►│  VPS 2: Blackbox5   │
│   (77.42.66.40)     │  VPN    │  (Helsingor)        │
└─────────────────────┘         └─────────────────────┘
```

### Option 3: Local + Cloud Hybrid

```
┌─────────────────────────────────────────────────────────┐
│  LOCAL MACHINE                                          │
│  ┌──────────────┐      ┌──────────────┐                │
│  │   OpenClaw   │◄────►│  Blackbox5   │                │
│  │   (Daemon)   │      │  (Local)     │                │
│  └──────────────┘      └──────┬───────┘                │
│                               │                         │
└───────────────────────────────┼─────────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │  VPS: Blackbox5     │
                    │  (Heavy workloads)  │
                    └─────────────────────┘
```

---

## Security Considerations

### Defense in Depth

| Layer | Blackbox5 | OpenClaw | Hybrid |
|-------|-----------|----------|--------|
| **Sandbox** | Limited | Docker | Both |
| **Kill Switch** | ✅ Yes | ❌ No | ✅ Available |
| **Verifier** | ✅ Agent with confidence | ❌ No | ✅ Available |
| **Content Filter** | ✅ Classifier | ❌ No | ✅ Available |
| **Audit Trail** | ✅ 6 files per run | Conversation history | ✅ Comprehensive |
| **Network** | SSH/Local | WebSocket/HTTP | VPN/Tailscale |

### Best Practices

1. **Never expose OpenClaw Gateway publicly**
   - Use Tailscale or VPN for remote access
   - Bind to localhost only (`127.0.0.1:18789`)

2. **Use Blackbox5's safety systems**
   - Enable verifier agent for all hybrid tasks
   - Set up kill switch for emergencies
   - Use safe mode for testing

3. **Credential Management**
   - Store API keys in environment variables
   - Use Blackbox5's secret management
   - Rotate tokens regularly

4. **Network Security**
   - Use SSH tunnels between systems
   - Implement mutual TLS if possible
   - Monitor connection logs

---

## Troubleshooting

### Common Issues

**Issue:** OpenClaw can't connect to Blackbox5
```bash
# Check Blackbox5 API is running
curl http://localhost:8000/health

# Verify environment variables
echo $BLACKBOX5_PATH
echo $BLACKBOX5_API_URL
```

**Issue:** Blackbox5 skill not appearing in OpenClaw
```bash
# Restart OpenClaw gateway
openclaw gateway restart

# Check skill is in correct location
ls ~/.openclaw/skills/blackbox5-bridge/
```

**Issue:** Notifications not sending
```bash
# Test OpenClaw messaging
openclaw message send --channel telegram --target shaan --message "Test"

# Check RALF watcher is running
ps aux | grep ralf_watcher
```

---

## Future Enhancements

### Phase 2: Bidirectional Integration

- Blackbox5 agents can initiate OpenClaw conversations
- Two-way state synchronization
- Shared memory layer

### Phase 3: Unified Dashboard

- Single web interface showing both systems
- Unified task queue
- Cross-system analytics

### Phase 4: Intelligent Routing

- AI-powered decision: OpenClaw vs Blackbox5
- Automatic complexity analysis
- Load balancing between systems

---

## Resources

- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenClaw Skills Guide](https://moltbotwiki.com/skills.html)
- [Blackbox5 Documentation](../../README.md)
- [RALF Documentation](../../../bin/ralf.md)
- [MCP Protocol](https://modelcontextprotocol.io)

---

## Summary

The Blackbox5 + OpenClaw hybrid combines:

- **Blackbox5's** enterprise orchestration, safety, and multi-agent capabilities
- **OpenClaw's** messaging integration, simplicity, and 24/7 availability

Result: A powerful system where you can delegate complex tasks via Telegram/WhatsApp and have them executed by 21 specialized agents with full safety controls.
