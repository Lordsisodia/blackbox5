---
name: openclaw-subagent-usage
description: Train OpenClaw agents on how to use sub-agents and coordinate with them effectively
category: training
version: 1.0
auto-invoke: true
confidence-threshold: 0.7
---

# OpenClaw Sub-Agent Usage & Coordination

## Purpose

This skill teaches OpenClaw agents how to effectively:
- Spawn and manage sub-agent sessions
- Coordinate work across multiple concurrent agents
- Handle agent lifecycle (start, monitor, stop)
- Use agent-specific skills appropriately
- Manage cross-agent communication

## When to Use This Skill

Invoke this skill when:
- An agent needs to understand OpenClaw's sub-agent system
- An agent is planning multi-agent workflows
- An agent needs to coordinate work across specialized agents
- An agent needs to debug sub-agent communication issues

## Key Concepts

### Session Management
Each agent session has:
- `agent:main:main` - Main orchestrator session
- `agent:main:subagent:<uuid>` - Sub-agent session (isolated)
- Sub-agents maintain their own context but share through main agent

### Sub-Agent Configuration
Located in `openclaw.json`:
```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "subagents": {
          "allowAgents": ["*"]
        }
      },
      {
        "id": "content",
        "workspace": "/root/.openclaw/workspace"
      },
      {
        "id": "engineering",
        "workspace": "/root/.openclaw/workspace"
      },
      {
        "id": "general",
        "workspace": "/root/.openclaw/workspace"
      },
      {
        "id": "task-agent",
        "workspace": "/root/.openclaw/workspace"
      }
    ]
  }
}
```

### Available Sub-Agents in BlackBox5

| Agent ID | Name | Purpose | When to Use |
|-----------|------|------------|
| `content` | Content Strategist | Marketing, content strategy, YouTube transcripts |
| `engineering` | Engineering Lead | Code review, refactoring, architecture, video processing |
| `general` | General Assistant | General questions, documentation, research |
| `task-agent` | Task Manager | Task creation, scheduling, prioritization, completion tracking |

## How to Spawn Sub-Agents

### Method 1: Via Agent-to-Agent Communication
Main agent can send messages directly to sub-agent sessions:

```python
# Example from agent code
sessions_send(
    session_key="agent:content:main",
    message="Analyze this YouTube transcript and extract key insights",
    timeout_seconds=300
)
```

### Method 2: Via OpenClaw CLI (Spawned Sessions)
Main agent spawns a dedicated sub-agent session:

```python
# From agent code (using subprocess)
import subprocess
result = subprocess.run([
    'openclaw', 
    'session', 
    'start', 
    'agent', 
    'content', 
    '--message', 'Process these transcripts'
])
```

## Agent Lifecycle Management

### 1. Starting a Sub-Agent

**Step 1: Check if agent is already running**
```bash
openclaw sessions list --kinds subagent --limit 100
```

**Step 2: Spawn new session**
```python
# Using sessions_spawn tool
sessions_spawn(
    task="Analyze these videos and create summary",
    label="video-analysis",
    agent="content",  # Use content agent for YouTube work
    timeout_seconds=600
)
```

**Step 3: Monitor sub-agent status**
```bash
# Check if agent is still running
openclaw sessions list --kinds subagent | grep "video-analysis"
```

### 2. Monitoring a Sub-Agent

**Check activity:**
```python
# From agent code
from datetime import datetime, timedelta
import subprocess

# Get session info
result = subprocess.run([
    'openclaw', 
    'sessions_list', 
    '--kinds', 'subagent',
    '--messageLimit', '0'
], capture_output=True, text=True)

# Parse JSON output
import json
sessions = json.loads(result.stdout)
subagent = sessions.get('video-analysis')

if subagent:
    # Check if session is active (updated in last 5 minutes)
    updated = datetime.fromisoformat(subagent.get('updatedAt').rstrip('Z'))
    if datetime.now() - updated < timedelta(minutes=5):
        status = "RUNNING"
    else:
        status = "IDLE"
    
    print(f"Sub-agent {subagent.get('label')}: {status}")
```

### 3. Stopping a Sub-Agent

**Stop gracefully:**
```bash
# Using sessions_list to get PID, then kill
openclaw sessions_list --kinds subagent | grep "video-analysis" | cut -d':' -f2 | xargs kill
```

## Cross-Agent Coordination

### Task Distribution Strategy

**When to distribute work:**

1. **By Task Type:**
   - Content tasks → content agent
   - Code tasks → engineering agent
   - Research tasks → general agent
   - Video processing → create specialized video agent

2. **By Load Balancing:**
   - If main agent is busy, send to general agent
   - If content agent is at capacity, use task-agent
   - If multiple agents available, use round-robin distribution

3. **By Priority:**
   - High priority tasks → content agent
   - Medium priority → engineering agent
   - Low priority → general agent

### Communication Patterns

### Pattern 1: Main → Sub-Agent → Main
Main agent delegates task to sub-agent, sub-agent executes and reports back to main.

**Example:**
```python
# Main agent orchestrator
def coordinate_subagent(task_type, agent_id, task_data):
    # Spawn sub-agent
    result = sessions_spawn(
        task=task_data['description'],
        label=f"{task_type}-worker",
        agent=agent_id
    )
    
    # Wait for completion or timeout
    for i in range(60):  # Check every second
        status = check_agent_status(result.run_id)
        if status == 'completed':
            return status['output']
        elif status == 'failed':
            return status['error']
        elif status == 'timeout':
            # Handle timeout
            return status['timeout']
    
    # Return final result
    return {
        'status': 'completed',
        'output': sub_agent_result,
        'run_id': result.run_id
    }
```

### Pattern 2: Sub-Agent → Sub-Agent (Peer-to-Peer)

Sub-agents communicate directly for complex tasks.

**Example - Content & Engineering:**
```python
# Content agent spawns engineering agent for a technical task
result = sessions_send(
    session_key="agent:content:main",
    message="Review this code architecture for security issues",
    to_session="agent:engineering:subagent:<uuid>"
)
```

## Framework-Specific Coordination

### BMAD (BlackBox5 Multi-Agent Development) Agents

**BMAD Architecture:**
```
architect      -> System design
executor       -> Task execution
tester         -> Quality assurance
planner         -> Task planning
validator       -> Result verification
scribe          -> Documentation
```

**Coordination Pattern:**
```python
# Main orchestrator uses BMAD agents
def execute_with_bmad(task_description):
    # Step 1: Plan
    planner_result = sessions_spawn(
        task=f"Create implementation plan for: {task_description}",
        label="bmad-planner",
        agent="planner"
    )
    
    # Step 2: Design
    architect_result = sessions_spawn(
        task=f"Design architecture for: {task_description}",
        label="bmad-architect",
        agent="architect"
    )
    
    # Step 3: Execute
    executor_result = sessions_spawn(
        task=f"Execute implementation: {task_description}",
        label="bmad-executor",
        agent="executor"
    )
    
    # Step 4: Verify
    validator_result = sessions_spawn(
        task=f"Verify implementation: {task_description}",
        label="bmad-validator",
        agent="validator"
    )
    
    # Step 5: Document
    scribe_result = sessions_spawn(
        task=f"Document implementation results for: {task_description}",
        label="bmad-scribe",
        agent="scribe"
    )
    
    return {
        'status': 'completed',
        'results': [planner_result, architect_result, executor_result, validator_result, scribe_result]
    }
```

## Common Coordination Issues & Solutions

### Issue 1: Race Conditions

**Problem:** Multiple agents try to modify the same resource simultaneously.

**Solution:** Implement resource locking:
```python
# Use BlackBox5 task files to lock resources
class ResourceManager:
    def __init__(self):
        self.locked_resources = set()
    
    def acquire(self, resource_id):
        while resource_id in self.locked_resources:
            import time
            time.sleep(1)
        self.locked_resources.add(resource_id)
        return True
    
    def release(self, resource_id):
        self.locked_resources.remove(resource_id)
```

### Issue 2: Duplicate Work

**Problem:** Two agents work on the same task unknowingly.

**Solution:** Implement task deduplication:
```python
# Check active tasks in BlackBox5 before spawning
import os
import json

def check_active_tasks():
    tasks_dir = "/opt/blackbox5/5-project-memory/blackbox5/tasks/active/"
    
    for filename in os.listdir(tasks_dir):
        if filename.startswith("TASK-") and filename.endswith(".md"):
            with open(os.path.join(tasks_dir, filename), 'r') as f:
                task = json.load(f)
                # Check if task is already being worked on
                if task.get('status') == 'in-progress':
                    return task.get('title')
    
    return None  # No conflicts
```

### Issue 3: Deadlock

**Problem:** Agent A waits for B, B waits for A - circular dependency.

**Solution:** Implement timeout and escalation:
```python
# Set timeouts for all sub-agent operations
TIMEOUT_SHORT = 300   # 5 minutes
TIMEOUT_MEDIUM = 600  # 10 minutes
TIMEOUT_LONG = 3600   # 1 hour

def execute_with_timeout(subagent_session, task):
    try:
        result = sessions_send(
            session_key=subagent_session,
            message=task,
            timeout_seconds=TIMEOUT_MEDIUM
        )
        return result
    except Exception as e:
        # Escalate to main agent if sub-agent fails
        return {
            'status': 'escalated',
            'error': str(e)
        }
```

## Best Practices for Sub-Agent Coordination

### 1. Clear Task Boundaries

Each sub-agent should have:
- **Well-defined scope** - Know exactly what they need to do
- **Acceptance criteria** - How to determine task is complete
- **Reporting format** - What information to return to main agent
- **Escalation path** - What to do when stuck

### 2. Proper Resource Management

- **Memory limits** - Monitor context window usage per agent
- **Token budget** - Set per-agent token limits
- **Timeout handling** - Don't let agents run indefinitely
- **Cleanup** - Stop idle agents to free resources

### 3. Effective Communication

- **Structured messages** - Use JSON for complex requests
- **Progress updates** - Send periodic status updates
- **Error reporting** - Immediate notification of failures
- **Completion signaling** - Clear acknowledgment when done

### 4. Scalability Considerations

**For Large-Scale Work (100+ concurrent agents):**

1. **Agent Pools**
   - Create agent pools for common tasks
   - Distribute work across pools
   - Pool manager assigns work to available agents

2. **Hierarchical Coordination**
   - Main agent coordinates multiple "team lead" agents
   - Each team lead manages a small pool of workers
   - Reduces main agent's coordination overhead

3. **Queue-Based Coordination**
   - Use BlackBox5 task queue for work distribution
   - Agents poll queue for available tasks
   - Natural load balancing based on agent availability

## Integration with BlackBox5 Systems

### Task Queue Integration

```python
# From agent code - use BlackBox5 task queue
def get_next_task(agent_type):
    import subprocess
    import json
    
    # Query BlackBox5 task queue
    result = subprocess.run([
        'cat', '/opt/blackbox5/5-project-memory/blackbox5/tasks/queue.json'
    ], capture_output=True, text=True)
    
    queue = json.loads(result.stdout)
    
    # Find task for this agent type
    available_tasks = [
        task for task in queue 
        if task.get('assigned_to') == agent_type 
        and task.get('status') == 'pending'
    ]
    
    if available_tasks:
        # Return highest priority task
        return sorted(available_tasks, key=lambda x: x.get('priority', 99))
    else:
        return None
```

### Knowledge Base Integration

```python
# From agent code - store learnings in BlackBox5 knowledge base
def store_learning(agent_type, insight_type, data):
    import subprocess
    import json
    from datetime import datetime
    
    # Create knowledge entry
    knowledge_entry = {
        'timestamp': datetime.now().isoformat(),
        'agent_type': agent_type,
        'insight_type': insight_type,
        'data': data,
        'tags': ['sub-agent-coordination', agent_type]
    }
    
    # Store in BlackBox5 knowledge base
    result = subprocess.run([
        'openclaw', 'message', 
        '--to', 'agent:main',
        f"Store learning in BlackBox5 knowledge: {json.dumps(knowledge_entry)}"
    ], capture_output=True, text=True)
    
    return result
```

## Troubleshooting Sub-Agent Issues

### Problem: Sub-agent not responding

**Steps:**
1. Check session status:
```bash
openclaw sessions list --kinds subagent | grep "content-agent"
```

2. Check agent logs:
```bash
openclaw process list --agent content
tail -50 /root/.openclaw/agents/content/sessions/latest/session.jsonl
```

3. Restart sub-agent:
```bash
openclaw session kill --agent content
openclaw session start --agent content --message "Reconnect"
```

### Problem: Sub-agent in error state

**Steps:**
1. Check agent health
2. Review error logs
3. Restart or replace sub-agent

## Framework-Specific Guidelines

### For RALF (Run Agent Framework)

**RALF Sub-Agents:**
- **Scout** - Analyzes code, identifies improvement opportunities
- **Planner** - Creates execution plans
- **Executor** - Runs Bash scripts, monitors processes
- **Verifier** - Validates results, quality checks
- **Scribe** - Documents all activities

**RALF Coordination:**
```python
# RALF coordinator pattern
class RALFCoordinator:
    def __init__(self):
        self.agents = []
    
    def orchestrate(self, task):
        # Plan work
        self.agents['planner'].execute(task)
        
        # Execute in sequence
        for stage in ['scout', 'planner', 'executor', 'verifier']:
            self.agents[stage].execute(task)
        
        # Verify
        self.agents['verifier'].validate(task)
        
        # Document
        self.agents['scribe'].document(task)
```

### For BMAD (BlackBox5 Multi-Agent Development)

**BMAD Agent Coordination:**
- **Architect** - System design
- **Planner** - Implementation planning
- **Executor** - Code execution
- **Tester** - Quality assurance
- **Scribe** - Documentation

**BMAD Workflow:**
1. Architect creates system design
2. Planner creates detailed implementation plan
3. Executor implements according to plan
4. Tester validates quality
5. Scribe documents everything

## Success Metrics for Sub-Agent Coordination

### Key Metrics to Track

1. **Task Completion Rate**
   - Tasks completed per hour
   - Average time to completion
   - Success vs failure ratio

2. **Sub-Agent Utilization**
   - Percentage of time sub-agents are actively working
   - Number of concurrent sub-agents
   - Resource efficiency (tokens per task)

3. **Coordination Overhead**
   - Time main agent spends coordinating vs doing work
   - Message throughput (messages per second)
   - Session management efficiency

4. **Scalability**
   - Maximum concurrent sub-agents
   - Performance degradation point
   - Resource saturation threshold

## Advanced Coordination Techniques

### Technique 1: Agent Orchestration Graph

Create a dynamic agent coordination graph:
```python
# Example: Dynamic coordination
class AgentGraph:
    def __init__(self):
        self.agents = {}
        self.tasks = {}
        self.dependencies = {}  # task_id -> [task_ids]
    
    def add_agent(self, agent_id, capabilities):
        self.agents[agent_id] = {
            'capabilities': capabilities,
            'current_tasks': [],
            'performance_history': []
        }
    
    def add_task(self, task_id, task_data):
        self.tasks[task_id] = task_data
        
        # Find agents with required capabilities
        capable_agents = [
            agent_id for agent_id, caps in self.agents 
            if all(cap in self.agents[agent_id]['capabilities'] for cap in task_data['required_capabilities'])
        ]
        
        return capable_agents
    
    def assign_task(self, task_id, agent_id):
        self.agents[agent_id]['current_tasks'].append(task_id)
        self.dependencies[task_id] = agent_id
    
    def get_available_agents(self, task_type):
        return [aid for aid, caps in self.agents[aid]['capabilities'] 
               if all(cap in self.agents[aid]['capabilities'] for cap in task_type['required_capabilities'])]
```

### Technique 2: Adaptive Task Scheduling

Implement priority queue with adaptive scheduling:
```python
# Adaptive scheduler
import heapq
from datetime import datetime, timedelta

class AdaptiveScheduler:
    def __init__(self):
        self.task_queue = []
        self.agent_availability = {}  # agent_id -> available_until timestamp
        self.agent_performance = {}  # agent_id -> {success_rate, avg_time}
    
    def add_task(self, task):
        heapq.heappush(self.task_queue, task)
    
    def get_next_task(self):
        while self.task_queue:
            task = heapq.heappop(self.task_queue)
            required_agents = task['required_capabilities']
            
            # Find available agents
            for agent_id in required_agents:
                if agent_id in self.agent_availability:
                    if datetime.now() < self.agent_availability[agent_id]:
                        return task, agent_id
            
            # No agents available now, return None
    
    def mark_agent_busy(self, agent_id, duration_minutes=30):
        self.agent_availability[agent_id] = datetime.now() + timedelta(minutes=duration_minutes)
    
    def update_agent_performance(self, agent_id, success, time_taken):
        if agent_id not in self.agent_performance:
            self.agent_performance[agent_id] = {'success': 0, 'avg_time': 0, 'attempts': 0}
        
        perf = self.agent_performance[agent_id]
        perf['attempts'] += 1
        
        if success:
            perf['success'] += 1
        
        perf['avg_time'] = (
            perf['avg_time'] * (perf['attempts'] - 1) 
            + time_taken
        ) / perf['attempts']
```

## Training OpenClaw Agents

### How to Teach Agents to Use Sub-Agents

### Step 1: Create Training Examples

Create training data showing best practices:
```yaml
# OpenClaw training example
training_examples:
  - example_1:
      context: "Create a content marketing strategy for YouTube channel"
      good_response: "Spawn content agent with task: 'Create YouTube marketing strategy'"
      agent: "content"
      reasoning: "Content tasks should be handled by content specialist"
      
  - example_2:
      context: "Review code for security vulnerabilities"
      good_response: "Spawn engineering agent and scribe agent"
      agents: ["engineering", "scribe"]
      reasoning: "Code reviews need technical expertise, documentation should track all findings"
      
  - example_3:
      context: "Coordinate multi-agent workflow for video processing"
      good_response: "Use orchestrator pattern: main -> coordinator -> worker agents"
      agent: "main"
      reasoning: "Main agent should use orchestration pattern for parallel work distribution"
```

### Step 2: Add Examples to Agent Instructions

Update agent instructions with sub-agent examples:
```markdown
# Agent instruction example

When you need to use sub-agents, follow these patterns:

## Pattern 1: Simple Task Delegation

To delegate a task:
```
1. I need [task description] done
```

Good response:
```
I'm spawning a sub-agent to handle this:
- Agent: [agent_name]
- Task: [task_description]
- Expected completion: [time estimate]
```

## Pattern 2: Parallel Task Distribution

To run parallel tasks:
```
1. I need to [task1] and [task2] done in parallel
```

Good response:
```
I'm spawning multiple sub-agents:
- Agent 1: [agent1_name] for [task1]
- Agent 2: [agent2_name] for [task2]
- Expected completion: [time estimate]
```

## Pattern 3: Cross-Agent Communication

To have agents communicate:
```
1. Tell [agent2] to send result to [agent3]
```

Good response:
```
I'm establishing communication between [agent2] and [agent3]:
- Agent 2 will send: "[message content]"
- Agent 3 will process and report back to me
```
```

### Step 3: Update System Prompts

Add sub-agent coordination examples to system prompts:

**System prompt enhancement:**
```text
You have access to OpenClaw's sub-agent system. When coordinating work across multiple agents:

1. Always check if sub-agents are already working on related tasks
2. Use the agent that best matches the task type
3. Monitor sub-agent status and handle failures gracefully
4. Set appropriate timeouts (300s for simple tasks, 3600s for complex tasks)
5. Ensure tasks have clear acceptance criteria before spawning
6. Document all coordination in the scribe knowledge base

Available sub-agents:
- main (orchestrator)
- content (Content Strategist)
- engineering (Engineering Lead)
- general (General Assistant)
- task-agent (Task Manager)

Use them wisely: content for marketing/content tasks, engineering for code/architecture tasks, general for research/questions.
```

## Monitoring Sub-Agent Coordination

Create dashboards to track:
- Active sub-agents count
- Task distribution across agents
- Sub-agent success/failure rates
- Coordination efficiency metrics

Example dashboard URL: http://77.42.66.40:8001/ (your dashboard UI)
```

## Self-Improvement for Sub-Agent Coordination

The system should learn and optimize:
1. Which agent types work best together
2. Optimal task distribution strategies
3. Effective communication patterns
4. Best resource allocation

Track learnings in BlackBox5 knowledge base with tags: [sub-agent-coordination, orchestration]
```

## Implementation Checklist

For OpenClaw agent developers integrating sub-agent support:

- [ ] Test agent spawning (sessions_spawn) in various scenarios
- [ ] Implement sub-agent status monitoring (sessions_list)
- [ ] Add sub-agent-to-sub-agent communication (sessions_send)
- [ ] Create task distribution logic
- [ ] Implement timeout and escalation handling
- [ ] Set up resource management (prevent over-allocation)
- [ ] Add performance tracking and metrics collection
- [ ] Create training examples for agents
- [ ] Document best practices in agent instructions
- [ ] Implement deadlock prevention
- [ ] Add cross-agent coordination patterns
- [ ] Create monitoring dashboards
- [ ] Implement adaptive task scheduling
- [ ] Add error handling and retry logic
- [ ] Set up knowledge base integration for learnings
- [ ] Test with multiple concurrent sub-agents (stress test)
- [ ] Create agent pool management
- [ ] Implement hierarchical coordination (main → team leads → workers)
- [ ] Add queue-based coordination for large-scale work
- [ ] Implement agent graph for dynamic coordination
- [ ] Add BMAD/RALF framework specific coordination
- [ ] Create training data and examples
- [ ] Optimize for scalability (100+ agents)

## Quick Reference

### Commands to Check Sub-Agents

```bash
# List all sub-agent sessions
openclaw sessions list --kinds subagent --limit 100

# Get specific agent info
openclaw sessions list --kinds subagent | grep "content"

# Stop a sub-agent
openclaw sessions kill --agent content --message "Please stop"
```

### Sub-Agent IDs

```
main          - Main orchestrator session
content        - Content Strategist sub-agent
engineering     - Engineering Lead sub-agent
general         - General Assistant sub-agent
task-agent      - Task Manager sub-agent
```

### Agent Roles Matrix

| Task Type | Best Agent | Alternative Agent |
|-----------|--------------|-----------------|
| Content | content | general |
| Code | engineering | general |
| Architecture | engineering | architect (create if needed) |
| Research | general | general |
| Video | content | engineering |
| Task Mgmt | task-agent | general |
| Documentation | scribe | general |

Use this matrix to quickly identify which agent should handle a given task type!

---

**Created:** 2026-02-10
**Skill Version:** 1.0
**Last Updated:** 2026-02-10T20:12:00.000Z
```
