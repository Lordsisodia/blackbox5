# Sub-Agent Architecture Plan for BlackBox5

**Date:** 2026-02-07
**Status:** Planning Phase
**Objective:** Design a hybrid skill/sub-agent system where complex skills become autonomous sub-agents

---

## Current State Analysis

### Existing Skills Inventory (23 Primary Skills)

**BMAD Agent Skills (10):**
- `bmad-pm` - Product Manager (John)
- `bmad-architect` - Technical Architect (Winston)
- `bmad-analyst` - Business Analyst (Mary)
- `bmad-sm` - Scrum Master (Bob)
- `bmad-ux` - UX Designer (Sally)
- `bmad-dev` - Developer (Amelia)
- `bmad-qa` - QA Engineer (Quinn)
- `bmad-tea` - Test Execution Agent (TEA)
- `bmad-quick-flow` - Fast path for simple tasks (Barry)
- `bmad-planning` - Planning Agent (Planner)

**Protocol & Framework Skills (4):**
- `superintelligence-protocol` - Complex problem-solving (7-step process)
- `continuous-improvement` - Systematic self-improvement
- `run-initialization` - Run setup and documentation
- `truth-seeking` - Assumption validation

**Utility Skills (4):**
- `web-search` - External information gathering
- `codebase-navigation` - Codebase exploration
- `supabase-operations` - Database operations
- `git-commit` - Git operations

**Core System Skills (2):**
- `task-selection` - Task selection from STATE.yaml
- `state-management` - STATE.yaml updates

**Infrastructure Skills (3):**
- `ralf-cloud-control` - RALF Kubernetes control
- `github-codespaces-control` - Codespaces management
- `legacy-cloud-control` - Legacy agent control

---

## Proposed Sub-Agent Architecture

### Philosophy

**Hybrid Approach:**
- **Direct Skill Invocation** for quick tasks (< 30s, low complexity)
- **Sub-Agent Delegation** for complex tasks (isolated context, parallelization, specialized reasoning)

### Proposed Sub-Agents

#### 1. **Validator Sub-Agent** (NEW)
**Purpose:** Post-task validation and verification

**Trigger:** Main agent completes a task and claims success

**Inputs:**
- Original task requirements
- Main agent's claimed changes/outputs
- Git diff or file changes
- Test results (if applicable)

**Outputs:**
- Validation report (PASS/FAIL/PARTIAL)
- Specific issues found
- Recommendations for fixes

**Context:**
- Read-only access to task files
- Can run tests, check syntax, verify requirements
- Cannot modify files (reports only)

**System Prompt Focus:**
- Skeptical verification mindset
- Requirements traceability
- Evidence-based assessment

---

#### 2. **Meta/Bookkeeper Sub-Agent** (NEW)
**Purpose:** BlackBox5 administrative hygiene

**Trigger:** Task completion checkpoint

**Inputs:**
- Task ID and status
- Run folder path
- Changes made summary

**Outputs:**
- Updated THOUGHTS.md with learnings
- Updated DECISIONS.md with key decisions
- Updated TIMELINE.md with progress
- Updated task status in task file
- Updated prd.json if applicable

**Context:**
- Write access to run folder documentation
- Read access to task structure

**System Prompt Focus:**
- Organizational discipline
- Documentation standards
- Traceability requirements

---

#### 3. **Superintelligence Sub-Agent** (CONVERT from skill)
**Purpose:** Complex problem analysis with multi-perspective reasoning

**Trigger:** Architecture questions, design decisions, complex problems

**Inputs:**
- Problem statement
- Relevant context (project scans, code snippets)
- Constraints and requirements

**Outputs:**
- Recommendation with confidence score
- Key assumptions
- Risk analysis
- Implementation path
- Alternatives considered

**Context:**
- Can spawn parallel sub-agents (Architect, Researcher, Critic)
- Access to relevant project files
- Web search capability

**System Prompt Focus:**
- First principles thinking
- Multi-perspective analysis
- Structured reasoning
- Uncertainty quantification

**Parallel Sub-Agents:**
- `si-architect` - System design perspective
- `si-researcher` - Information gathering
- `si-critic` - Challenge assumptions
- `si-synthesizer` - Integrate perspectives

---

#### 4. **BMAD Role Sub-Agents** (CONVERT from skills)
**Purpose:** Domain-specific expertise agents

**Candidates for sub-agent conversion:**

| Skill | Convert? | Rationale |
|-------|----------|-----------|
| `bmad-architect` | YES | Complex design work benefits from isolated context |
| `bmad-analyst` | YES | Research tasks need large context windows |
| `bmad-pm` | YES | PRD creation is multi-step, iterative |
| `bmad-qa` | YES | Testing benefits from fresh perspective |
| `bmad-dev` | MAYBE | Simple coding = direct, complex = sub-agent |
| `bmad-ux` | YES | Design work is creative, benefits from focus |
| `bmad-sm` | NO | Coordination tasks are lightweight |
| `bmad-tea` | NO | Task execution is straightforward |
| `bmad-quick-flow` | NO | Explicitly for simple tasks |
| `bmad-planning` | YES | Planning is complex, multi-step |

---

#### 5. **Orchestrator Sub-Agent** (NEW)
**Purpose:** Coordinate multiple sub-agents for complex tasks

**Trigger:** Tasks requiring multiple domain experts

**Inputs:**
- Complex task description
- Required expertise areas
- Dependencies between sub-tasks

**Outputs:**
- Coordinated sub-agent execution plan
- Integrated results
- Conflict resolution

**Context:**
- Can spawn and manage other sub-agents
- Tracks parallel execution
- Handles result synthesis

---

#### 6. **Context Gatherer Sub-Agent** (NEW)
**Purpose:** Pre-task context collection

**Trigger:** Before complex tasks

**Inputs:**
- Task description
- Project scope hints

**Outputs:**
- Structured project summary
- Relevant file list
- Dependency map
- Architecture overview

**Context:**
- Read-only codebase access
- Can use codebase-navigation skill

---

## Migration Strategy

### Phase 1: Core Infrastructure (Week 1)
1. Create sub-agent framework
2. Implement Validator sub-agent
3. Implement Meta/Bookkeeper sub-agent
4. Test with simple tasks

### Phase 2: Complex Skills (Week 2-3)
1. Convert `superintelligence-protocol` to sub-agent
2. Convert `bmad-architect` to sub-agent
3. Convert `bmad-analyst` to sub-agent
4. Parallel execution testing

### Phase 3: BMAD Roles (Week 4-5)
1. Convert remaining BMAD skills
2. Implement Orchestrator
3. Full integration testing

### Phase 4: Optimization (Week 6)
1. Performance tuning
2. Cost analysis
3. Documentation updates

---

## Technical Design

### Sub-Agent Interface

```yaml
sub_agent_invocation:
  name: "validator"
  inputs:
    task_id: "TASK-001"
    claimed_changes: "Fixed bug in auth.ts"
    files_modified: ["src/auth.ts"]
  context:
    task_file: "/path/to/TASK-001.md"
    run_folder: "/path/to/run-20260207_120000"
  outputs_expected:
    - validation_report
    - issues_found
    - recommendations
```

### Execution Modes

**Sequential Mode:**
```
Main Agent -> Sub-Agent A -> (waits) -> Result -> Continue
```

**Parallel Mode:**
```
Main Agent -> Sub-Agent A (async)
          -> Sub-Agent B (async)
          -> Sub-Agent C (async)
          -> (waits for all) -> Synthesize -> Continue
```

**Pipeline Mode:**
```
Main Agent -> Sub-Agent A -> Result -> Sub-Agent B -> Result -> Sub-Agent C
```

---

## Decision Log

### Decision 1: Hybrid Approach
**Decision:** Use direct skills for quick tasks, sub-agents for complex tasks
**Rationale:** Avoid overhead for simple operations, gain benefits for complex ones
**Date:** 2026-02-07

### Decision 2: Validator as First Sub-Agent
**Decision:** Build Validator sub-agent first
**Rationale:** Immediate value for quality assurance, simpler scope
**Date:** 2026-02-07

### Decision 3: Meta/Bookkeeper as Second Sub-Agent
**Decision:** Build Meta/Bookkeeper sub-agent second
**Rationale:** Ensures BlackBox5 discipline without burdening main agent
**Date:** 2026-02-07

### Decision 4: Convert Superintelligence to Sub-Agent
**Decision:** Convert superintelligence-protocol skill to sub-agent with parallel expert sub-agents
**Rationale:** Natural fit for parallel multi-perspective analysis
**Date:** 2026-02-07

---

## Open Questions

1. **Cost Analysis:** What's the token/cost overhead of sub-agents vs direct skills?
2. **Latency:** How much latency does sub-agent spawning add?
3. **State Management:** How do we pass state between main agent and sub-agents?
4. **Error Handling:** What happens when a sub-agent fails?
5. **Context Limits:** How much context should be passed to sub-agents?

---

## Next Steps

1. [ ] Design sub-agent framework interface
2. [ ] Implement Validator sub-agent prototype
3. [ ] Test Validator with sample tasks
4. [ ] Document lessons learned
5. [ ] Design Meta/Bookkeeper sub-agent
6. [ ] Create cost/latency measurement system

---

## Related Documents

- `~/.blackbox5/2-engine/.autonomous/skills/` - Current skill definitions
- `~/.blackbox5/5-project-memory/blackbox5/operations/skill-selection.yaml` - Skill selection framework
- `~/.blackbox5/6-roadmap/01-research/superintelligence-protocol/` - Superintelligence research
