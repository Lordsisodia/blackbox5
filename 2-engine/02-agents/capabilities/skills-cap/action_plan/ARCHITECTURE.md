# Action Plan System - Architecture

**Purpose:** Wraps together different Blackbox5 systems into a step-by-step process that agents can use to carry out tasks.

**Version:** 1.0.0
**Last Updated:** 2026-01-21

---

## Overview

The Action Plan system provides a structured, first-principles-driven approach to task execution. It integrates:
- First Principles reasoning engine
- Multi-phase task breakdown
- Persistent context management
- Temporary workspace management
- Progress tracking and checkpointing

---

## Core Components

### 1. ActionPlan Class
**Location:** `action_plan.py`

**Responsibilities:**
- Plan creation and initialization
- Phase management
- Task tracking
- Progress persistence

**Key Methods:**
```python
class ActionPlan:
    def __init__(self, name: str, description: str, workspace_path: str)
    def add_phase(self, phase: ActionPhase)
    def create_task(self, phase_id: str, task: ActionTask)
    def get_next_task(self) -> Optional[ActionTask]
    def complete_task(self, task_id: str, result: TaskResult)
    def save_checkpoint(self) -> str
    def load_checkpoint(self, checkpoint_id: str)
```

### 2. ActionPhase Class
**Location:** `models.py`

**Purpose:** Represents a phase in the execution plan

**Structure:**
```python
@dataclass
class ActionPhase:
    id: str
    name: str
    description: str
    order: int
    first_principles_analysis: Optional[FirstPrinciplesResult]
    tasks: List[ActionTask]
    status: PhaseStatus  # pending, in_progress, completed, blocked
    dependencies: List[str]  # IDs of phases this depends on
```

### 3. ActionTask Class
**Location:** `models.py`

**Purpose:** Represents an executable task within a phase

**Structure:**
```python
@dataclass
class ActionTask:
    id: str
    phase_id: str
    title: str
    description: str
    context_template: TaskContext
    status: TaskStatus  # pending, in_progress, completed, failed, blocked
    dependencies: List[str]  # IDs of tasks this depends on
    subtasks: List[ActionSubtask]
    metadata: Dict[str, Any]
```

### 4. ActionSubtask Class
**Location:** `models.py`

**Purpose:** Breaks down tasks into smaller steps

**Structure:**
```python
@dataclass
class ActionSubtask:
    id: str
    parent_task_id: str
    title: str
    description: str
    thinking_process: str  # First principles reasoning
    status: TaskStatus
    order: int
```

### 5. TaskContext Class
**Location:** `models.py`

**Purpose:** Templates for context creation during execution

**Structure:**
```python
@dataclass
class TaskContext:
    objective: str
    constraints: List[str]
    assumptions: List[str]
    resources: List[str]
    success_criteria: List[str]
    thinking_process: str  # First principles analysis
```

### 6. FirstPrinciplesIntegration
**Location:** `first_principles_integration.py`

**Purpose:** Integrates first principles thinking into action plans

**Key Methods:**
```python
class FirstPrinciplesIntegration:
    def analyze_phase(self, phase: ActionPhase) -> FirstPrinciplesResult
    def analyze_task(self, task: ActionTask) -> FirstPrinciplesResult
    def generate_hypotheses(self, analysis: FirstPrinciplesResult) -> List[Hypothesis]
    def validate_approach(self, approach: str, constraints: List[Constraint]) -> ValidationResult
```

### 7. WorkspaceManager
**Location:** `workspace_manager.py`

**Purpose:** Manages temporary workspaces for action plan execution

**Key Methods:**
```python
class WorkspaceManager:
    def create_workspace(self, plan_id: str) -> str
    def get_workspace_path(self, plan_id: str) -> str
    def save_task_context(self, plan_id: str, task_id: str, context: Dict[str, Any])
    def load_task_context(self, plan_id: str, task_id: str) -> Dict[str, Any]
    def cleanup_workspace(self, plan_id: str)
    def archive_workspace(self, plan_id: str, destination: str)
```

---

## Data Flow

```
User Request
    ↓
ActionPlan Creation
    ↓
First Principles Analysis (What are we ACTUALLY solving?)
    ↓
Phase Breakdown (High-level steps)
    ↓
Task Creation (Detailed steps within phases)
    ↓
Subtask Generation (First-principles-driven decomposition)
    ↓
Workspace Creation (Temporary folder for this plan)
    ↓
Execution Loop:
    ├── Get next task
    ├── Load context template
    ├── Apply first principles reasoning
    ├── Execute task
    ├── Save result
    ├── Update checkpoint
    └── Repeat until all tasks complete
    ↓
Workspace Archive (Save or cleanup)
    ↓
Final Report
```

---

## First Principles Integration

### When First Principles is Triggered

1. **Plan Creation** - Initial analysis of the overall problem
2. **Phase Creation** - Analyze what the phase is ACTUALLY solving
3. **Task Creation** - Decompose tasks to fundamentals
4. **Blockage Detection** - Re-analyze when stuck
5. **Failure Recovery** - Re-examine assumptions after failure

### First Principles Loop

```python
def first_principles_loop(self, context: str):
    """
    Apply first principles thinking to any context
    """
    # 1. What problem are we ACTUALLY solving?
    problem = self.extract_true_problem(context)

    # 2. What do we know to be TRUE?
    truths = self.extract_fundamental_truths(problem)

    # 3. What are we assuming?
    assumptions = self.identify_assumptions(context)

    # 4. What MUST be included? What can we eliminate?
    requirements = self.derive_requirements(truths)
    optional = self.identify_optional(context)

    return {
        'true_problem': problem,
        'fundamental_truths': truths,
        'assumptions': assumptions,
        'essential_requirements': requirements,
        'optional_elements': optional
    }
```

---

## Template System

### Task Context Template

Located at: `templates/task_context_template.md`

```markdown
# Task: {{task_title}}

## Objective
{{objective}}

## First Principles Analysis

### What problem are we ACTUALLY solving?
{{true_problem}}

### What do we know to be TRUE?
{{fundamental_truths}}

### What are we assuming?
{{assumptions}}

### What MUST be included?
{{essential_requirements}}

### What can we eliminate?
{{optional_elements}}

## Constraints
{{constraints}}

## Success Criteria
{{success_criteria}}

## Resources
{{resources}}

## Thinking Process
{{thinking_process}}
```

### Phase Template

Located at: `templates/phase_template.md`

```markdown
# Phase: {{phase_name}}

## Description
{{description}}

## First Principles Analysis
{{first_principles_analysis}}

## Tasks
{{tasks}}

## Dependencies
{{dependencies}}

## Exit Criteria
{{exit_criteria}}
```

---

## Workspace Structure

```
/tmp/action_plans/
└── {plan_id}/
    ├── plan.json              # Full plan state
    ├── checkpoints/           # Recovery checkpoints
    │   ├── checkpoint_001.json
    │   └── checkpoint_002.json
    ├── tasks/                 # Task-specific data
    │   ├── task_001/
    │   │   ├── context.json
    │   │   ├── result.json
    │   │   └── thinking.md
    │   └── task_002/
    │       └── ...
    ├── phases/                # Phase-specific data
    │   ├── phase_001/
    │   │   └── analysis.json
    │   └── ...
    ├── artifacts/             # Generated artifacts
    │   ├── diagrams/
    │   ├── code/
    │   └── docs/
    └── logs/                  # Execution logs
        └── execution.log
```

---

## Persistence Strategy

### Checkpoint Format

```json
{
  "checkpoint_id": "checkpoint_001",
  "timestamp": "2026-01-21T10:30:00Z",
  "plan_state": {
    "current_phase": "phase_002",
    "current_task": "task_005",
    "completed_phases": ["phase_001"],
    "completed_tasks": ["task_001", "task_002", "task_003", "task_004"]
  },
  "context": {
    "decisions_made": [...],
    "assumptions_validated": [...],
    "blockers_resolved": [...]
  }
}
```

### Recovery Process

1. Load latest checkpoint
2. Verify workspace integrity
3. Validate dependencies still satisfied
4. Resume from last completed task
5. Re-run first principles analysis if context changed significantly

---

## Agent Integration

### As a Skill

Agents can invoke the action plan skill:

```python
from blackbox5.engine.agents.capabilities.skills_cap.action_plan import create_action_plan

# In agent code
def execute_complex_task(self, task_description: str):
    plan = create_action_plan(
        name=task_description,
        description=self.break_down_task(task_description),
        workspace_path=self.get_temp_dir()
    )

    # Add phases with first principles analysis
    plan.add_phase(
        name="Analysis",
        first_principles=self.run_fp_analysis(task_description)
    )

    # Execute
    result = plan.execute()
    return result
```

### As a Standalone Agent

```python
from blackbox5.engine.agents.action_plan_agent import ActionPlanAgent

agent = ActionPlanAgent()
result = agent.execute(
    objective="Build a new feature",
    context={...}
)
```

---

## Success Metrics

1. **Context Retention** - AI never loses sight of the goal
2. **First Principles Compliance** - Every major decision includes FP analysis
3. **Recovery Capability** - Can resume from any checkpoint
4. **Progress Visibility** - Clear status at all times
5. **Template Reusability** - Context templates reduce repeated thinking

---

## Integration Points

1. **First Principles Engine** - `2-engine/07-operations/environment/lib/python/core/runtime/fp_engine/first_principles.py`
2. **Memory System** - `5-project-memory/siso-internal/`
3. **Skills Registry** - `2-engine/02-agents/capabilities/skills-cap/`
4. **Agent Base** - `2-engine/01-core/agents/core/base_agent.py`

---

## Future Enhancements

1. **Parallel Task Execution** - Run independent tasks concurrently
2. **Dynamic Replanning** - Adjust plan based on execution results
3. **Learning from Plans** - Extract patterns from successful plans
4. **Plan Templates** - Pre-built plans for common patterns
5. **Collaborative Planning** - Multiple agents contributing to same plan
