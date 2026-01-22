# Action Plan System

A comprehensive system for creating and executing structured action plans in Blackbox5 with first principles integration, context management, and progress tracking.

## Overview

The Action Plan system wraps together different Blackbox5 systems into a step-by-step process that agents can use to carry out tasks. It provides:

- **Multi-phase Planning**: Break down complex tasks into phases with clear dependencies
- **Task Management**: Create tasks with subtasks, context templates, and dependencies
- **First Principles Integration**: Apply first principles thinking at every level
- **Persistent Context**: Never lose sight of the goal with persistent context tracking
- **Checkpoint Recovery**: Save and resume from any point
- **Workspace Management**: Automatic temporary workspace creation and management

## Installation

The Action Plan system is located at:
```
2-engine/02-agents/capabilities/skills-cap/action_plan/
```

## Quick Start

### Basic Usage

```python
from action_plan import (
    create_action_plan,
    TaskContext,
    Constraint,
    Assumption,
    ConstraintType,
    TaskResult
)

# Create an action plan
plan = create_action_plan(
    name="Build User Authentication",
    description="Implement secure authentication with JWT",
    apply_first_principles=True
)

# Add a phase
phase = plan.add_phase(
    name="Requirements Analysis",
    description="Analyze authentication requirements",
    exit_criteria=["All requirements documented"]
)

# Create a task
task = plan.create_task(
    phase_id=phase.id,
    title="Identify Security Requirements",
    description="Document security requirements",
    context_template=TaskContext(
        objective="Identify security requirements",
        constraints=[
            Constraint(
                text="Must use industry-standard encryption",
                type=ConstraintType.HARD,
                source="security_policy"
            )
        ],
        assumptions=[
            Assumption(
                text="JWT tokens are appropriate",
                confidence="high",
                test="Research JWT best practices"
            )
        ],
        resources=["OWASP guidelines", "JWT spec"],
        success_criteria=["All security requirements documented"],
        thinking_process="""
        First Principles:
        1. What problem are we solving? User authentication
        2. What do we know is TRUE? Security is critical
        3. What are we assuming? JWT is the right approach
        4. What MUST be included? Secure password storage
        """
    )
)

# Add subtasks
plan.add_subtask(
    task_id=task.id,
    title="Review OWASP guidelines",
    description="Review security best practices",
    thinking_process="Industry standards must be followed",
    order=1
)

# Execute
next_task = plan.get_next_task()
plan.start_task(next_task)

# Complete task
result = TaskResult(
    task_id=next_task.id,
    success=True,
    output="Requirements documented",
    thinking_steps=["Reviewed OWASP", "Identified constraints"]
)
plan.complete_task(next_task.id, result)

# Generate report
print(plan.generate_report())
```

## Core Concepts

### 1. ActionPlan

The main orchestrator that manages phases, tasks, and execution.

```python
plan = create_action_plan(
    name="Plan Name",
    description="What this plan achieves",
    apply_first_principles=True  # Auto-analyze with FP
)
```

### 2. Phases

High-level stages of your plan with dependencies and exit criteria.

```python
phase = plan.add_phase(
    name="Implementation",
    description="Build the feature",
    dependencies=["phase_001"],  # Must complete phase_001 first
    exit_criteria=["All tests passing", "Documentation complete"]
)
```

### 3. Tasks

Executable units within phases with rich context templates.

```python
task = plan.create_task(
    phase_id=phase.id,
    title="Implement Core Logic",
    description="Build the main feature",
    context_template=TaskContext(
        objective="Implement feature X",
        constraints=[...],
        assumptions=[...],
        resources=[...],
        success_criteria=[...],
        thinking_process="..."  # First principles analysis
    )
)
```

### 4. Subtasks

Fine-grained steps within tasks for detailed execution.

```python
plan.add_subtask(
    task_id=task.id,
    title="Write unit tests",
    description="Create comprehensive tests",
    thinking_process="Test coverage is essential",
    order=1
)
```

## First Principles Integration

The Action Plan system automatically applies first principles thinking:

### Automatic Analysis

When you create a plan with `apply_first_principles=True`, it automatically:
1. Analyzes the overall problem
2. Analyzes each phase
3. Generates hypotheses for different approaches
4. Identifies assumptions to validate

### Manual Analysis

You can also apply first principles manually:

```python
from action_plan import FirstPrinciplesIntegration

fp = FirstPrinciplesIntegration()

# Analyze a problem
analysis = fp.analyze_problem(
    "Build a scalable microservices architecture"
)

print(f"True Problem: {analysis.true_problem}")
print(f"Fundamental Truths: {analysis.fundamental_truths}")
print(f"Assumptions: {analysis.assumptions}")
```

## Checkpoint Recovery

Never lose progress with automatic checkpoints:

```python
# Create checkpoint
checkpoint_id = plan.create_checkpoint()

# Later, recover from checkpoint
new_plan = create_action_plan(...)
new_plan.load_checkpoint(checkpoint_id)
```

## Workspace Management

Each plan gets an isolated workspace:

```
/tmp/action_plans/{plan_id}/
├── plan.json              # Current plan state
├── checkpoints/           # Recovery checkpoints
├── tasks/                 # Task-specific data
│   └── {task_id}/
│       ├── context.json
│       ├── result.json
│       └── thinking.md
├── phases/                # Phase-specific data
│   └── {phase_id}/
│       └── analysis.json
├── artifacts/             # Generated artifacts
│   ├── diagrams/
│   ├── code/
│   └── docs/
└── logs/                  # Execution logs
    └── execution.log
```

## Progress Tracking

Always know where you are:

```python
progress = plan.get_progress()
print(f"Progress: {progress['task_progress']}")
print(f"Complete: {progress['percent_complete']:.1f}%")
```

Generate reports:

```python
report = plan.generate_report()
print(report)
```

## As a Skill for Agents

Agents can use the Action Plan skill:

```python
from blackbox5.engine.agents.capabilities.skills_cap.action_plan import create_action_plan

class MyAgent(BaseAgent):
    def execute_complex_task(self, task_description: str):
        # Create an action plan
        plan = create_action_plan(
            name=task_description,
            description=self.break_down_task(task_description),
            apply_first_principles=True
        )

        # Add phases
        analysis_phase = plan.add_phase(
            name="Analysis",
            description="Understand the problem",
            exit_criteria=["Problem understood"]
        )

        # Execute tasks
        while True:
            task = plan.get_next_task()
            if not task:
                break

            result = self.execute_task(task)
            plan.complete_task(task.id, result)

        return plan.generate_report()
```

## First Principles Loop

The system includes a first principles loop that can be triggered at any point:

```python
from action_plan import create_first_principles_analysis

# Apply first principles to any context
analysis = create_first_principles_analysis(
    "We need to implement user authentication"
)

# Get the analysis
print(f"True Problem: {analysis.true_problem}")
print(f"What we know to be TRUE: {analysis.fundamental_truths}")
print(f"What we're assuming: {analysis.assumptions}")
print(f"What MUST be included: {analysis.essential_requirements}")
```

## Examples

See `example.py` for comprehensive examples including:
- Basic action plan creation
- Task execution simulation
- Checkpoint recovery
- First principles integration

Run examples:
```bash
cd 2-engine/02-agents/capabilities/skills-cap/action_plan
python example.py
```

## Architecture

See `ARCHITECTURE.md` for detailed architecture documentation including:
- Component design
- Data flow
- First principles integration
- Template system
- Workspace structure
- Persistence strategy

## Templates

The system uses Jinja2 templates for context generation:

- `templates/task_context_template.md` - Task context template
- `templates/phase_template.md` - Phase template

## API Reference

### ActionPlan

**Methods:**
- `add_phase()` - Add a phase to the plan
- `create_task()` - Create a task within a phase
- `add_subtask()` - Add a subtask to a task
- `get_next_task()` - Get the next task ready for execution
- `start_task()` - Mark a task as started
- `complete_task()` - Mark a task as complete with result
- `save_checkpoint()` - Save a checkpoint for recovery
- `load_checkpoint()` - Load a checkpoint
- `get_progress()` - Get current progress
- `generate_report()` - Generate human-readable report
- `cleanup()` - Clean up workspace

### TaskContext

**Fields:**
- `objective` - What the task achieves
- `constraints` - Hard and soft constraints
- `assumptions` - Assumptions being made
- `resources` - Available resources
- `success_criteria` - Definition of done
- `thinking_process` - First principles reasoning

### TaskResult

**Fields:**
- `task_id` - ID of the task
- `success` - Whether task succeeded
- `output` - Task output
- `artifacts` - Generated artifacts
- `error` - Error message if failed
- `thinking_steps` - Steps taken during execution

## Integration with Existing Systems

The Action Plan system integrates with:
- **First Principles Engine** - `2-engine/07-operations/environment/lib/python/core/runtime/fp_engine/`
- **Memory System** - `5-project-memory/siso-internal/`
- **Skills Registry** - `2-engine/02-agents/capabilities/skills-cap/`
- **Agent Base** - `2-engine/01-core/agents/core/base_agent.py`

## Best Practices

1. **Always Apply First Principles** - Start with `apply_first_principles=True`
2. **Create Clear Exit Criteria** - Each phase should have measurable completion criteria
3. **Document Thinking** - Use the `thinking_process` field extensively
4. **Save Checkpoints** - Call `create_checkpoint()` after major milestones
5. **Validate Assumptions** - Use the Assumptions field to track what needs validation
6. **Generate Reports** - Use `generate_report()` to communicate progress

## Future Enhancements

- Parallel task execution
- Dynamic replanning
- Learning from past plans
- Pre-built plan templates
- Collaborative planning (multiple agents)

## License

Part of the Blackbox5 project.
