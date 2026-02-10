---
name: framework-usage
description: Use frameworks (BMAD, RALF, custom) effectively with OpenClaw sub-agent system
category: training
version: 1.0
auto-invoke: false
confidence-threshold: 0.75
---

# Framework Usage with OpenClaw Sub-Agents

## Purpose

This skill teaches OpenClaw agents how to effectively integrate and use BlackBox5 frameworks (BMAD, RALF, custom) with the sub-agent system.

## When to Use This Skill

Invoke this skill when:
- Planning multi-agent workflows that use BMAD/RALF frameworks
- Understanding framework-specific coordination patterns
- Choosing the right framework for a task type
- Implementing framework-specific agent communication protocols

## Framework Overview

### BMAD (BlackBox5 Multi-Agent Development)

**Components:**
- **Architect** - System design, architecture patterns
- **Planner** - Implementation planning, task decomposition
- **Executor** - Code execution, Bash scripting
- **Tester** - Quality assurance, validation
- **Verifier** - Result verification
- **Scribe** - Documentation

**Use When:**
- Complex system design or refactoring tasks
- Multi-stage implementations
- Tasks requiring architectural validation
- Projects with multiple code modules

**Coordination Pattern:**
```
Main → Architect → Plan → Execute → Verify → Document
```

### RALF (Run Agent Framework)

**Components:**
- **Scout** - Analyzes code, identifies improvement opportunities
- **Planner** - Creates execution plans
- **Executor** - Runs Bash scripts, monitors processes
- **Verifier** - Validates results, quality checks
- **Scribe** - Documents all activities

**Use When:**
- Codebase analysis and improvement
- Process automation and optimization
- CI/CD pipeline implementation
- Infrastructure deployment

**Coordination Pattern:**
```
Scout → Plan → Execute → Verify → Document
```

### Custom Frameworks

**BlackBox5 Custom Agents:**
- **YouTube Agent** - Continuous video scraping, transcript processing
- **Kimi Load Balancer** - API key management, load distribution
- **Conversational Planner** - Natural language to task plans
- **API Manager** - Multi-provider API coordination

**Use When:**
- Domain-specific tasks (YouTube, API management)
- Custom workflows requiring specialized knowledge
- Tasks that don't fit standard frameworks

## Framework Selection Guide

### Decision Tree

```
Is this a task type that requires a framework?

├─ Yes
│   ├─ Is it a multi-stage project?
│   │   ├─ Yes → Use BMAD (orchestrated, specialized roles)
│   │   └─ No → Can use RALF or custom
│   │
├─ No
│   ├─ Is it a code task?
│   │   ├─ Yes → Use RALF (process-oriented)
│   │   └─ No → Use custom or BMAD simplified
│   │
└─ Is it high-priority/urgent?
    └─ Yes → Use BMAD with priority queuing
    └─ No → Can use any framework
```

### Framework Comparison

| Feature | BMAD | RALF | Custom |
|---------|-------|---------|---------|
| **Structured Roles** | ✅ | ❌ | ⚙️ |
| **Orchestration** | ✅ | ❌ | ⚙️ |
| **Built-in Testing** | ✅ | ❌ | ⚙️ |
| **Parallel Execution** | ⚙️ | ⚙️ | ⚙️ |
| **Documentation** | ✅ | ✅ | ⚙️ |
| **Flexibility** | ⚙️ | ⚙️ | ✅ |
| **Setup Time** | Medium | Fast | Variable |

## BMAD Integration Patterns

### Pattern 1: Orchestrated BMAD Workflow

```
Main Agent (Orchestrator)
  │
  ├─→ Architect Agent
  │     ├─ Creates system design
  │     └─→ Planner Agent
  │           ├─ Creates implementation plan
  │           ├─ Breaks down into tasks
  │           └─→ Task Queue
  │                 ├─ Executor Agent (x3)
  │                 ├─ Tester Agent
  │                 └─ Verifier Agent
  │                       └─→ Scribe Agent
  └─→ Main Agent (collects results)
```

**When to Use:**
- System architecture projects
- Multi-module deployments
- Complex refactoring tasks
- Tasks requiring validation and testing

### Pattern 2: RALF Scout-Execute Loop

```
Main Agent
  │
  ├─→ Scout Agent
  │     ├─ Analyzes codebase
  │     └─→ Planner Agent
  │           ├─ Creates improvement plan
  │           ├─ Breaks into actionable tasks
  │           └─→ Task Queue
  │                 ├─ Executor Agent
  │                 └─ Main Agent
```

**When to Use:**
- Continuous improvement tasks
- Codebase optimization
- Performance tuning
- Bug fixing

## Framework-Specific Communication

### BMAD Agent Communication

```python
# Example: BMAD orchestrator coordinates framework agents
def orchestrate_bmad_workflow(task_description):
    # Step 1: Spawn architect
    architect = sessions_spawn(
        task=f"Design architecture for: {task_description}",
        label="bmad-architect",
        agent="architect"
    )
    
    # Step 2: Spawn planner
    planner = sessions_spawn(
        task=f"Create implementation plan for: {task_description}",
        label="bmad-planner",
        agent="planner"
    )
    
    # Step 3: Get plan details
    planner_plan = sessions_send(
        session_key=planner['session_key'],
        message="Provide detailed task breakdown with milestones",
        to_session="main"
    )
    
    # Step 4: Spawn multiple executors
    for task in planner_plan['tasks']:
        executor = sessions_spawn(
            task=task['description'],
            label=f"bmad-executor-{task['id']}",
            agent="executor"
        )
    
    # Step 5: Verify
    verifier = sessions_spawn(
        task=f"Verify all implementations",
        label="bmad-verifier",
        agent="verifier"
    )
    
    # Step 6: Document
    scribe = sessions_spawn(
        task=f"Document entire workflow: {task_description}",
        label="bmad-scribe",
        agent="scribe"
    )
    
    # Step 7: Collect results
    # Main agent collects all results from agents
```

### RALF Agent Communication

```python
# Example: RALF scout-execute loop
def orchestrate_ralf_workflow(task_type, agent_id):
    # Spawn scout
    scout = sessions_spawn(
        task=f"Analyze: {task_type} in codebase",
        label="ralph-scout",
        agent="scout"
    )
    
    # Wait for analysis
    time.sleep(5)
    
    # Get scout results
    scout_result = sessions_send(
        session_key=scout['session_key'],
        message="Provide detailed analysis with improvement opportunities",
        to_session="main"
    )
    
    # Spawn executor
    executor = sessions_spawn(
        task=scout_result['improvement_actions'][0],
        label=f"ralph-executor-{agent_id}",
        agent=agent_id
    )
```

## Custom Framework Integration

### YouTube Agent Coordination

```python
# YouTube agent works with other agents
def youtube_with_architect(task_description):
    # 1. Ask architect for system design
    architect = sessions_spawn(
        task=f"Design YouTube scraping system architecture",
        label="youtube-architect",
        agent="architect"
    )
    
    # 2. Get design
    design = sessions_send(
        session_key=architect['session_key'],
        message="Provide detailed system design for continuous scraping",
        to_session="main"
    )
    
    # 3. Spawn scraper
    scraper = sessions_spawn(
        task=design['implementation_steps'][0],
        label="youtube-scraper",
        agent="youtube"
    )
    
    # 4. Monitor and log
    scribe = sessions_spawn(
        task=f"Monitor scraper performance and log all activities",
        label="scribe",
        agent="scribe"
    )
```

### Kimi Load Balancer Coordination

```python
# Load balancer works with other agents for heavy tasks
def kimibalance_with_agents(task_type):
    # 1. Check API key usage
    # 2. If heavy task, use multiple agents in parallel
    # 3. Distribute work across agents
    # 4. Monitor performance

# Spawn multiple agents for parallel execution
agents = []
for i in range(3):
    agent = sessions_spawn(
        task=f"Process transcript batch {i} with Kimi API",
        label=f"kimi-worker-{i}",
        agent="youtube"
    )
    agents.append(agent)
```

## Best Practices

### 1. Framework Selection

- Match framework to task complexity
- BMAD: High complexity, structured workflows
- RALF: Medium complexity, process-oriented
- Custom: Low complexity, domain-specific

### 2. Agent Role Mapping

```
Task Type              → Main Agent     → Framework Manager
                           ├─ Architect Agent
                           ├─ Planner Agent
                           └─ Executor Agent

Code Development Task     → Main Agent     → Scout Agent
                           └─ Executor Agent

Continuous Improvement Task → Main Agent     → Scout Agent
                           └─ Executor Agent

YouTube Task             → Main Agent     → YouTube Agent
                           └─ Scribe Agent
```

### 3. Lifecycle Management

**Spawn Phase:**
1. Main agent creates framework task
2. Framework manager selects appropriate agents
3. Agents spawn sub-agents for framework components
4. Sub-agents execute framework-specific workflows
5. Framework manager collects results
6. Main agent verifies and documents

**Execution Phase:**
- Framework agents run their workflows independently
- Main agent monitors progress (not micromanaging)
- Agents report back to framework manager
- Framework manager coordinates with main agent

**Completion Phase:**
- All framework agents complete their work
- Framework manager validates results
- Scribe documents entire framework workflow
- Framework manager reports to main agent

### 4. Error Handling

**Framework-Level Errors:**
- If architect fails → Main agent handles (fallback to custom)
- If multiple executors fail → Main agent retries with reduced scope
- If verification fails → Main agent logs and continues

**Agent-Level Errors:**
- If executor task fails → Agent retries (framework manager handles)
- Timeouts → Framework manager escalates to main agent
- Resource exhaustion → Framework manager pauses and reschedules

### 5. Performance Optimization

**Parallel Execution Strategy:**
```python
# Example: Parallel BMAD execution
def parallel_bmad_execution(tasks):
    # Group tasks by agent type
    executors = []
    testers = []
    
    # Stage 1: Plan
    planner = sessions_spawn(task="Create parallel execution plan")
    planner_tasks = planner.get('tasks')
    
    # Stage 2: Execute
    for task in planner_tasks:
        if task['type'] == 'execution':
            executors.append(sessions_spawn(task=task))
        elif task['type'] == 'verification':
            testers.append(sessions_spawn(task=task))
    
    # Stage 3: Verify
    for tester in testers:
        verification = sessions_spawn(task=tests[i].get('validation'))
    
    # Stage 4: Document
    scribe = sessions_spawn(task="Document parallel execution results")
    
    return {'status': 'completed', 'parallel_tasks': len(executors)}
```

**Resource Pooling:**
```python
# Framework-specific resource management
class FrameworkResourceManager:
    def __init__(self):
        self.agent_pools = {}
        self.available_agents = {}
    
    def register_agent(self, framework_type, agent_id):
        if framework_type not in self.agent_pools:
            self.agent_pools[framework_type] = []
        self.available_agents[framework_type] = {}
        
        self.available_agents[framework_type][agent_id] = {
            'capabilities': [],
            'current_tasks': [],
            'status': 'idle'
        }
    
    def allocate_agent(self, framework_type, task):
        # Find available agent
        for agent_id, info in self.available_agents[framework_type].items():
            if info['status'] == 'idle' and all(cap in task['required_capabilities'] for cap in info['capabilities']):
                return agent_id
        
        # Mark as busy
        return agent_id
```

## Framework Training Data

### Example Framework Tasks for Training

**Task 1: BMAD Architect for System Design**
```yaml
context: "Design a scalable system architecture for a video processing platform"
framework: bmad
agents:
  - architect: "Creates system design"
  - planner: "Creates implementation plan"
  - executor: "Executes implementation"
best_response: |
  The architect should create a comprehensive system design with:
  - Component decomposition
  - Technology stack recommendations
  - Data flow diagrams
  - Security considerations
  
  The planner should then break this down into concrete tasks for the executors.

The framework manager coordinates this workflow:
  1. Main agent spawns architect
  2. Architect creates system design
  3. Planner creates execution plan
  4. Multiple executors implement in parallel
  5. Verifier validates implementation
   6. Scribe documents everything
```

**Task 2: RALF Scout for Code Improvement**
```yaml
context: "Analyze codebase and identify optimization opportunities"
framework: ralf
agents:
  - scout: "Analyzes code, identifies improvement opportunities"
  - planner: "Creates improvement plan"
  - executor: "Runs improvement tasks"
best_response: |
  The scout should analyze the codebase and provide:
  - Performance bottlenecks
  - Code quality issues
  - Architecture improvements
  - Test coverage gaps
  
  The planner then prioritizes these findings and creates an improvement plan.

The RALF coordinator ensures:
  1. Continuous analysis
  2. Prioritized improvements
  3. Systematic enhancement
```

## Quick Reference

### Framework Quick Start Commands

```bash
# Using BMAD orchestrator
openclaw sessions_spawn --task "Design new feature with BMAD" --label "bmad-orchestrator"

# Using RALF scout-execute loop
openclaw sessions_spawn --task "Analyze and improve codebase" --label "ralph-scout-execute"

# Using custom framework (YouTube)
openclaw sessions_spawn --task "Process YouTube transcripts" --agent "youtube"
```

### Framework Selection Flowchart

```
User Request
    │
    ├─→ Agent analyzes task
    │
    ├─→ Is this a framework-type task?
    │   ├─ Yes → Use BMAD
    │   ├─ No → Use RALF or Custom
    │   │
    └─→ Is this complex enough for framework?
    │   └─→ Yes → Use BMAD simplified
    │
    └─→ No → Use direct agent spawning
```

## Monitoring Framework Usage

### Key Metrics

1. **Framework Adoption Rate**
   - Percentage of tasks using frameworks vs custom
   - Success rate of framework-based workflows
   - Time savings from framework orchestration

2. **Framework Performance**
   - Average task completion time with frameworks
   - Resource utilization efficiency
   - Coordination overhead (time spent coordinating vs working)

3. **Agent Utilization**
   - Framework agents active time vs working time ratio
   - Number of framework agents spawned per task type

---

**Created:** 2026-02-10
**Skill Version:** 1.0
**Last Updated:** 2026-02-10T20:12:00.000Z
```
