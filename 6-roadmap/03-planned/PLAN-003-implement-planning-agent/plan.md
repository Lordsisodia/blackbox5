# PLAN-003: Implement Planning Agent

**Priority:** 🔴 CRITICAL
**Status:** Planned
**Estimated Effort:** 3-5 days
**Dependencies:** PLAN-001 (Skills System), PLAN-002 (YAML Agents)
**Validation Agent:** Agent 7 (Ralphy & Workflow)

---

## Problem Statement

**Planning Agent doesn't exist**, blocking end-to-end workflow automation.

**Expected Workflow:**
```
User Request → Planning Agent → Vibe Kanban → Orchestrator → Agents
                  ↑                                    ↓
              (MISSING)                        Complex → Ralphy
```

**Impact:**
- Can't automate PRD creation
- Can't generate Epics and Tasks
- Manual workflow only
- Ralphy can't be used for planning
- Vibe Kanban underutilized

---

## Solution Design

### Planning Agent Responsibilities

1. **Requirements Analysis** - Parse user request into structured requirements
2. **PRD Generation** - Create Product Requirements Documents
3. **Epic Creation** - Break PRDs into epics
4. **Task Breakdown** - Break epics into actionable tasks
5. **Vibe Kanban Integration** - Create cards/columns automatically
6. **Agent Assignment** - Recommend which agents for which tasks
7. **BMAD Methodology** - Business, Model, Architecture, Development workflow

---

## Architecture

### Planning Agent Class Structure

```python
# blackbox5/2-engine/01-core/agents/PlanningAgent.py

from agents.core.base_agent import BaseAgent, AgentConfig, AgentTask, AgentResult
from typing import List, Dict
import yaml

class PlanningAgent(BaseAgent):
    """
    Planning Agent - Converts user requests into structured plans

    Workflow:
    1. Parse user request
    2. Analyze requirements
    3. Generate PRD (Product Requirements Document)
    4. Break into Epics
    5. Break Epics into Tasks
    6. Create Vibe Kanban cards
    7. Assign to agents
    """

    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.vibe_kanban = None  # VibeKanbanManager
        self.bmad_framework = BMADFramework()

    async def execute(self, task: AgentTask) -> AgentResult:
        """Execute planning task"""

        request = task.description

        # Step 1: Analyze requirements
        requirements = await self._analyze_requirements(request)

        # Step 2: Generate PRD
        prd = await self._generate_prd(requirements)

        # Step 3: Create Epics
        epics = await self._create_epics(prd)

        # Step 4: Break into Tasks
        tasks = await self._breakdown_tasks(epics)

        # Step 5: Create Vibe Kanban cards
        await self._create_kanban_cards(tasks)

        # Step 6: Assign to agents
        assignments = await self._assign_agents(tasks)

        return AgentResult(
            success=True,
            output=f"Created {len(epics)} epics, {len(tasks)} tasks",
            artifacts={
                "prd": prd,
                "epics": epics,
                "tasks": tasks,
                "assignments": assignments
            }
        )
```

### BMAD Framework Integration

```python
class BMADFramework:
    """Business, Model, Architecture, Development methodology"""

    async def analyze(self, request: str) -> Dict:
        """Apply BMAD to user request"""

        return {
            "business": await self._business_analysis(request),
            "model": await self._model_design(request),
            "architecture": await self._architecture_design(request),
            "development": await self._development_plan(request)
        }

    async def _business_analysis(self, request: str) -> Dict:
        """Business analysis - What are we building and why?"""
        return {
            "goals": extract_goals(request),
            "users": identify_users(request),
            "value_proposition": extract_value(request),
            "success_metrics": define_metrics(request)
        }

    async def _model_design(self, request: str) -> Dict:
        """Model design - What's the conceptual model?"""
        return {
            "entities": extract_entities(request),
            "relationships": extract_relationships(request),
            "data_flow": model_data_flow(request),
            "state_model": define_states(request)
        }

    async def _architecture_design(self, request: str) -> Dict:
        """Architecture design - How will it work?"""
        return {
            "components": identify_components(request),
            "interfaces": define_interfaces(request),
            "data_stores": select_stores(request),
            "integration_points": find_integrations(request)
        }

    async def _development_plan(self, request: str) -> Dict:
        """Development plan - How do we build it?"""
        return {
            "phases": break_into_phases(request),
            "tasks": define_tasks(request),
            "dependencies": find_dependencies(request),
            "effort_estimates": estimate_effort(request)
        }
```

---

## Implementation Plan

### Phase 1: Core Planning Agent (2 days)

**Day 1: Basic Agent Structure**

1. Create PlanningAgent class
2. Implement basic execute() method
3. Add requirements analysis
4. Add PRD generation

**Day 2: Task Breakdown**

1. Implement epic creation
2. Implement task breakdown
3. Add agent assignment logic
4. Add output formatting

**Deliverable:** PlanningAgent that generates PRDs, epics, tasks

---

### Phase 2: Vibe Kanban Integration (1 day)

**Tasks:**
1. Integrate VibeKanbanManager
2. Create Kanban columns (Todo, In Progress, Review, Done)
3. Create card creation logic
4. Create card movement logic
5. Test integration

**Code Example:**
```python
async def _create_kanban_cards(self, tasks: List[Dict]):
    """Create Kanban cards for tasks"""

    # Get or create project
    project = await self.vibe_kanban.get_project("BlackBox5")

    # Get columns
    columns = await self.vibe_kanban.list_columns(project["id"])

    # Create cards
    for task in tasks:
        card = await self.vibe_kanban.create_card(
            project_id=project["id"],
            column_id=columns["todo"]["id"],
            title=task["title"],
            description=task["description"],
            metadata={
                "priority": task["priority"],
                "assigned_to": task["agent"],
                "estimated_effort": task["effort"]
            }
        )
```

**Deliverable:** Cards created in Vibe Kanban automatically

---

### Phase 3: BMAD Methodology (1-2 days)

**Tasks:**
1. Implement BMADFramework class
2. Add business analysis
3. Add model design
4. Add architecture design
5. Add development planning
6. Integrate with PlanningAgent

**Deliverable:** Full BMAD methodology applied

---

### Phase 4: Testing & Integration (1 day)

**Test Suite:**
```python
# test_planning_agent.py

async def test_prd_generation():
    """PlanningAgent generates PRD from user request"""
    agent = PlanningAgent(config)

    task = AgentTask(
        id="1",
        description="Build a REST API for user management"
    )

    result = await agent.execute(task)

    assert "prd" in result.artifacts
    assert result.artifacts["prd"]["title"] == "User Management API"
    assert len(result.artifacts["prd"]["requirements"]) > 0

async def test_epic_creation():
    """PlanningAgent breaks PRD into epics"""
    agent = PlanningAgent(config)
    result = await agent.execute(task)

    assert "epics" in result.artifacts
    assert len(result.artifacts["epics"]) > 0

async def test_task_breakdown():
    """PlanningAgent breaks epics into tasks"""
    result = await agent.execute(task)

    assert "tasks" in result.artifacts
    assert len(result.artifacts["tasks"]) > 0

async def test_kanban_integration():
    """PlanningAgent creates Kanban cards"""
    result = await agent.execute(task)

    # Verify cards created
    cards = await vibe_kanban.list_cards(project_id)
    assert len(cards) > 0

async def test_agent_assignment():
    """PlanningAgent assigns tasks to appropriate agents"""
    result = await agent.execute(task)

    assignments = result.artifacts["assignments"]
    assert len(assignments) > 0

    # Check appropriate assignments
    for task_id, agent_name in assignments.items():
        assert agent_name in ["developer", "analyst", "architect", ...]
```

---

## File Structure

```
blackbox5/2-engine/01-core/agents/
├── PlanningAgent.py           # NEW - Main Planning Agent
├── core/
│   ├── base_agent.py          # EXISTING
│   ├── agent_loader.py        # EXISTING (updated in PLAN-002)
│   └── skill_manager.py       # EXISTING (updated in PLAN-001)
├── bmad/                      # NEW - BMAD Framework
│   ├── __init__.py
│   ├── framework.py           # Main BMAD class
│   ├── business.py            # Business analysis
│   ├── model.py               # Model design
│   ├── architecture.py        # Architecture design
│   └── development.py         # Development planning
└── DeveloperAgent.py          # EXISTING
```

---

## Success Criteria

- ✅ PlanningAgent class created
- ✅ Analyzes user requirements
- ✅ Generates PRD documents
- ✅ Breaks PRDs into epics
- ✅ Breaks epics into tasks
- ✅ Creates Vibe Kanban cards
- ✅ Assigns tasks to agents
- ✅ BMAD methodology applied
- ✅ All tests passing (6/6)
- ✅ End-to-end workflow working

---

## Rollout Plan

### Pre-conditions
- [ ] PLAN-001 complete (skills working)
- [ ] PLAN-002 complete (all agents loading)
- [ ] Vibe Kanban database initialized (PLAN-005)
- [ ] BMAD methodology documented

### Execution
1. Create PlanningAgent class
2. Implement BMAD framework
3. Add Vibe Kanban integration
4. Run test suite
5. Test end-to-end workflow

### Post-conditions
- [ ] Planning Agent working
- [ ] Can automate PRD creation
- [ ] Can generate Epics and Tasks
- [ ] Vibe Kanban integration working
- [ ] End-to-end workflow functional

---

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| BMAD too complex | Medium | Medium | Start simple, iterate |
| Vibe Kanban API issues | Medium | High | Test integration early |
| Quality of PRDs | Medium | Medium | Use LLM with good prompts |
| Task estimation accuracy | High | Low | Provide ranges, not exact |

---

## Dependencies

**Blocks:**
- End-to-end workflow automation
- Ralphy planning loops
- Vibe Kanban full utilization

**Blocked By:**
- PLAN-001: Fix Skills System (needs skills)
- PLAN-002: Fix YAML Agent Loading (needs all agents)
- PLAN-005: Initialize Vibe Kanban Database

**Can Parallel With:**
- PLAN-004: Fix Import Paths
- PLAN-006: Remove Duplicates

---

## Next Steps

1. Document BMAD methodology (1 day)
2. Create PlanningAgent class (1 day)
3. Implement task breakdown (1 day)
4. Integrate Vibe Kanban (1 day)
5. Implement BMAD framework (1-2 days)
6. Test and verify (1 day)

**Total Estimated Time:** 3-5 days

---

**Status:** Planned
**Ready to Execute:** After PLAN-001, PLAN-002, PLAN-005
**Assigned To:** Unassigned
**Priority:** 🔴 CRITICAL (blocks end-to-end workflow)
