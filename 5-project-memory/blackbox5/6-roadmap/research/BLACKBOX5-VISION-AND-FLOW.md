# BlackBox5 Vision and Architecture Flow

**Date:** 2026-01-20
**Status:** Core Vision Document
**Purpose:** Define what BlackBox5 is and how it works end-to-end

---

## What is BlackBox5?

**BlackBox5 is an autonomous AI development platform** where AI agents work together to build software, with every action tracked, learned from, and coordinated through a central system.

**Key Concept:** The "Black Box" metaphor represents the AI decision-making process - inputs go in, intelligent processing happens (the "black box"), and high-quality outputs come out, with everything tracked for continuous improvement.

---

## Core Philosophy

### 1. **Spec-Driven Development**
Everything starts from clear specifications:
- User Request → PRD (Product Requirements Document)
- PRD → Epic (Technical Architecture)
- Epic → Tasks (Breakdown into executable units)
- Tasks → Code (Implementation by agents)

**Traceability:** Complete lineage from user intent to shipped code

### 2. **Multi-Agent Collaboration**
No single AI does everything. Specialized agents collaborate:
- **Planning Agents** (Mary, Winston, Arthur) - Break down requirements
- **Execution Agents** (Amelia, Alex, etc.) - Build and implement
- **Review Agents** - Validate and test
- **Orchestrator** - Coordinate everything

### 3. **Project Memory as Single Source of Truth**
Every action, decision, and learning is tracked in Project Memory:
- What agents did
- Why they made decisions
- What worked and what didn't
- Timeline of all work

**Result:** The system learns from every project and gets smarter over time

---

## The Complete Flow

### Phase 1: User Request → Main Agent

```
User: "I need to build a multi-tenant SaaS application"
         ↓
    ┌─────────────────────────────────────┐
    │   MAIN AGENT (Planning Coordinator)  │
    │   - Has own black box functionality   │
    │   - Tracks all ongoing tasks         │
    │   - Monitors different agent groups  │
    │   - Oversees Vibe Kanban board       │
    └─────────────────────────────────────┘
```

**Main Agent Responsibilities:**
1. **Understand the Request** - Parse user intent, ask clarifying questions
2. **Track Progress** - Monitor all active tasks and agent groups
3. **Coordinate Vibe Kanban** - Create/move cards, track status
4. **Make Routing Decisions** - Which agent for which task?
5. **Quality Control** - Review work before accepting

---

### Phase 2: Planning and Documentation

```
    ┌─────────────────────────────────────┐
    │         PLANNING AGENTS              │
    │  (Mary, Winston, Arthur + Ralphy)    │
    └──────────┬──────────────────────────┘
               │
               ▼
    ┌─────────────────────────────────────┐
    │         BMAD METHODOLOGY             │
    │  Business → Model → Architecture    │
    │         → Development               │
    └─────────────────────────────────────┘
               │
               ├──► PRD (Product Requirements Doc)
               ├──► Epic (Technical Architecture)
               └──► 20+ Tasks (breakdown)
```

**Planning Process:**

**(a) Main Agent assigns planning to specialist agents:**
- **Mary (Analyst)** - Research and requirements gathering
- **Winston (Planning)** - Task breakdown and dependency mapping
- **Arthur (Architect)** - Technical architecture and design

**(b) Ralphy autonomous loop for complex planning:**
```
┌──────────────────────────────────────────────────────┐
│  RALPHY PLANNING LOOP (if complex or uncertain)     │
│  ┌────────────────────────────────────────────────┐ │
│  │ Iteration 1: First-pass PRD                   │ │
│  │ Iteration 2: Research gaps identified          │ │
│  │ Iteration 3: Technical architecture            │ │
│  │ Iteration 4: Task breakdown with dependencies│ │
│  │ Iteration 5: Review and refinement            │ │
│  └────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────┘
```

**(c) Output:**
- **PRD Document** - What are we building and why?
- **Epic Document** - How will it work (architecture)?
- **Task List** - 20+ specific tasks with dependencies
- **All pushed to Vibe Kanban** - Cards created for each task

---

### Phase 3: Task Execution and Iteration

```
    ┌─────────────────────────────────────────────────────────┐
    │              VIBE KANBAN BOARD                           │
    │  ┌────────┬───────────┬──────────┬──────────┬────────┐│
    │  │Backlog │   Todo    │ In Progress│ Review  │  Done  ││
    │  ├────────┼───────────┼──────────┼──────────┼────────┤│
    │  │ Task 1 │  Task 5   │  Task 12 │  Task 18 │ Task 22││
    │  │ Task 2 │  Task 6   │  Task 13 │  Task 19 │        ││
    │  │ Task 3 │  Task 7   │  Task 14 │          │        ││
    │  │ Task 4 │  Task 8   │  Task 15 │          │        ││
    │  │        │  Task 9   │  Task 16 │          │        ││
    │  │        │  Task 10  │  Task 17 │          │        ││
    │  │        │  Task 11  │          │          │        ││
    │  └────────┴───────────┴──────────┴──────────┴────────┘│
    └─────────────────────────────────────────────────────────┘
                          ↓
    ┌─────────────────────────────────────────────────────────┐
    │         ORCHESTRATOR AGENT (Traffic Control)            │
    │  • Assigns agents to tasks                              │
    │  • Monitors progress in real-time                        │
    │  • Makes routing decisions (complex vs simple)           │
    └─────────────────────────────────────────────────────────┘
                          ↓
        ┌─────────────────┴──────────────────┐
        │                                      │
    Simple Tasks                      Complex Tasks
        │                                      │
        ▼                                      ▼
┌──────────────────┐              ┌──────────────────────────┐
│ Direct Execution │              │   RALPHY AUTONOMOUS      │
│                  │              │   LOOP (Multi-iteration) │
│ Agent completes │              │                          │
│ task in one go  │              │ ┌──────────────────────┐ │
└──────────────────┘              │ │ Iteration 1: Design  │ │
                                   │ │ Iteration 2: Code    │ │
                                   │ │ Iteration 3: Test    │ │
                                   │ │ Iteration 4: Docs    │ │
                                   │ │ Iteration 5: Refine  │ │
                                   │ └──────────────────────┘ │
                                   └──────────────────────────┘
```

**Task Execution Patterns:**

**(a) Simple Tasks (Direct Execution):**
- Configuration changes
- Documentation updates
- Simple bug fixes
- Test additions
- **Pattern:** Agent picks task → completes → moves to Done → commits to Git

**(b) Complex Tasks (RALPHY Loop):**
- Feature implementation
- Architecture changes
- Multi-file refactoring
- **Pattern:**
  ```
  1. Ralphy creates isolated git worktree
  2. Iteration 1: Design/Plan
  3. Iteration 2: Implementation
  4. Iteration 3: Self-review and fixes
  5. Iteration 4: Testing
  6. Iteration 5: Documentation
  7. Review: Check if quality standards met
  8. If yes → merge to main branch
  9. If no → more iterations
  ```

**Vibe Kanban Integration:**
- Cards move: Todo → In Progress → Review → Done
- Real-time status updates
- Main Agent monitors all cards
- Blocked tasks flagged for attention

---

### Phase 4: Monitoring and Standardization

```
    During Execution:
         ↓
    ┌─────────────────────────────────────────────────────┐
    │     AGENT THOUGHT PROCESS EXPOSURE                 │
    │  • Agents show their thinking (not just output)    │
    │  • Chain of Thought reasoning visible               │
    │  • Decision rationale documented                    │
    │  • Alternative approaches considered                │
    └─────────────────────────────────────────────────────┘
         ↓
    ┌─────────────────────────────────────────────────────┐
    │     STANDARDIZED DATABASE STORAGE                  │
    │  • All actions tracked in Project Memory            │
    │  • Structured format (consistent across agents)     │
    │  • Timeline of all work                            │
    │  • Learnings archived for future reuse              │
    └─────────────────────────────────────────────────────┘
         ↓
    ┌─────────────────────────────────────────────────────┐
    │     GIT INTEGRATION                                 │
    │  • Each RALPHY loop = isolated worktree            │
    │  • Main Agent reviews quality before merge          │
    │  • Good work → merge to main branch                 │
    │  • Bad work → feedback and retry                    │
    └─────────────────────────────────────────────────────┘
```

**Monitoring Requirements:**

**(a) Thought Process Exposure:**
Agents must show:
- What they're thinking (Chain of Thought)
- Why they made decisions (rationale)
- What alternatives they considered
- What they learned (insights)

**Example:**
```markdown
## Agent Thinking Process

### Task: Implement user authentication

### Considered Approaches:
1. **JWT tokens** - Stateless, scalable, industry standard
2. **Session cookies** - Simple, server-side state
3. **OAuth2** - External providers, complex

### Decision: JWT tokens
**Rationale:**
- Scalability (no server-side session storage)
- Mobile-friendly (easy token refresh)
- Industry best practice
- Good library support (python-jose)

### Implementation Plan:
1. Create /auth endpoints
2. Implement JWT generation/validation
3. Add middleware for protected routes
4. Write tests for token refresh

### Risks Identified:
- Token revocation challenge → implement blacklist
- Secret key management → use environment variables
```

**(b) Standardized Storage:**

All agent actions stored in Project Memory with consistent schema:

```yaml
# Project Memory / agents / sessions / {session_id} / session.md

session:
  id: "session_20250120_001"
  agent: "Amelia (Developer)"
  task: "Implement user authentication"
  start_time: "2025-01-20T10:00:00Z"
  end_time: "2025-01-20T14:30:00Z"
  status: "completed"

thinking_process:
  - step:
      phase: "planning"
      thought: "Considered JWT vs sessions"
      decision: "JWT for scalability"
      rationale: "Stateless, mobile-friendly"
  - step:
      phase: "implementation"
      thought: "Need secure secret key management"
      decision: "Use environment variables"
      rationale: "Never commit secrets"

artifacts:
  - file: "src/auth/jwt.py"
    lines_changed: 245
    description: "JWT token generation and validation"
  - file: "src/auth/middleware.py"
    lines_changed: 89
    description: "Protected route middleware"

git_integration:
  worktree: "git_worktree_session_001"
  branch: "feature/user-auth"
  commits: 4
  merge_status: "pending_review"

learnings:
  - insight: "JWT token refresh is tricky"
    solution: "Implement sliding window refresh"
  - insight: "Secret key rotation needed"
    future_task: "Add key rotation to deployment checklist"
```

**(c) Timeline Tracking:**

Every action is timestamped and searchable:

```
Project Memory / timeline.md

| Time | Agent | Action | Result |
|------|-------|--------|--------|
| 10:00 | Mary | Created PRD | ✅ Approved |
| 10:30 | Arthur | Architecture design | ✅ Approved |
| 11:00 | Winston | Task breakdown | 20 tasks created |
| 11:30 | Amelia | Implement auth | 🔄 In progress |
| 12:00 | Ralphy | Auth iteration 1 | Design complete |
| 13:00 | Ralphy | Auth iteration 2 | Code complete |
| 14:00 | Ralphy | Auth iteration 3 | Tests passing |
| ... | ... | ... | ... |
```

---

## Phase 5: Skills System

```
    Each Agent has Access to Skills:
         ↓
    ┌─────────────────────────────────────────────────────┐
    │         SKILLS DOCUMENT                             │
    │  • Lists all available skills                       │
    │  • Each skill = specific capability                 │
    │  • Training data for agents                         │
    └─────────────────────────────────────────────────────┘
                          ↓
    ┌─────────────────────────────────────────────────────┐
    │      SKILL EXECUTION (Agent uses skill)            │
    │  1. Agent recognizes need for specific capability  │
    │  2. Loads skill definition from skills document    │
    │  3. Follows skill protocol to execute              │
    │  4. Adapts skill to current context                 │
    └─────────────────────────────────────────────────────┘
```

**Skill Examples:**

| Skill | Description | Used By |
|-------|-------------|---------|
| `tdd` | Test-driven development protocol | Amelia (Developer) |
| `code_review` | Systematic code review checklist | All agents |
| `debugging` | Debugging workflow and tools | Amelia |
| `architecture_review` | Architecture evaluation checklist | Alex (Architect) |
| `competitive_analysis` | Market research methodology | Mary (Analyst) |
| `documentation` | Technical writing standards | All agents |
| `refactoring` | Code improvement patterns | Amelia |
| `testing` | Test creation and execution | TEAAgent |

**How Skills Work:**

**(a) Skill Definition:**
```markdown
# Skill: TDD (Test-Driven Development)

## Description
Systematic approach: test → code → refactor

## Protocol
1. Write failing test
2. Write minimum code to pass
3. Refactor for quality
4. Repeat

## Examples
- Unit test for auth controller
- Integration test for API endpoint
- E2E test for user flow

## Quality Checks
- All tests pass
- Code coverage > 80%
- No code smells
```

**(b) Agent Using Skill:**
```python
# Agent (Amelia) executing task with TDD skill

task = "Add user registration endpoint"

# Agent recognizes: "This needs TDD"
# Loads TDD skill definition
# Follows protocol:

# Step 1: Write failing test
test_endpoint_returns_201()  # FAILS ✗

# Step 2: Write minimum code
def register_user():  # Simple implementation
    return {"status": "created"}

# Step 3: Verify test passes
test_endpoint_returns_201()  # PASSES ✓

# Step 4: Refactor for quality
def register_user(request):
    """Validate input, create user, return response"""
    # Improved implementation
    ...
```

---

## Complete End-to-End Example

### User Request
"Build a REST API for user authentication with registration, login, and password reset"

### Phase 1: Main Agent
- **Receives request**
- **Asks clarifying questions:**
  - "What email provider for password reset?"
  - "Any rate limiting requirements?"
  - "Mobile app or web app or both?"
- **Assigns to planning team**

### Phase 2: Planning (Mary, Winston, Arthur)
- **Mary:** Research best practices for auth APIs
- **Arthur:** Design JWT token architecture
- **Winston:** Break down into 25 tasks

**Output:**
```markdown
# PRD: User Authentication API

## Requirements
- User registration with email verification
- JWT-based authentication
- Password reset via email
- Rate limiting on endpoints
- Mobile-friendly token refresh

# Epic: Auth API Architecture

## Components
1. Auth service (business logic)
2. JWT middleware (token validation)
3. Email service (password reset)
4. Rate limiter (abuse prevention)

## API Endpoints
POST /auth/register
POST /auth/login
POST /auth/refresh
POST /auth/logout
POST /auth/forgot-password
POST /auth/reset-password

# Tasks (25 total)
1. Setup project structure
2. Create database models
3. Implement JWT service
4. Create registration endpoint
5. ... (21 more tasks)
```

### Phase 3: Vibe Kanban
- **25 cards created** (one per task)
- **Cards organized:** Backlog → Todo → In Progress → Review → Done
- **Dependencies mapped** on cards

### Phase 4: Execution

**Task 1: Setup project structure**
- Agent: Amelia
- Type: Simple
- Execution: Direct completion
- Result: ✅ Done, committed to Git

**Task 2: Create database models**
- Agent: Alex (Architect)
- Type: Simple
- Execution: Direct completion
- Result: ✅ Done, committed to Git

**Task 3: Implement JWT service** (COMPLEX)
- Agent: Ralphy autonomous loop
- Type: Complex
- Execution:
  ```
  Iteration 1: Research JWT libraries
  Iteration 2: Design JWT service interface
  Iteration 3: Implement token generation
  Iteration 4: Implement token validation
  Iteration 5: Add tests (TDD skill)
  Iteration 6: Document API
  Iteration 7: Code review
  Iteration 8: Refactor based on review
  ```
- Result: ✅ Done, merged to main branch

**Tasks 4-25:** Similar pattern

### Phase 5: Monitoring

**During Execution:**
- All agents show thought process
- All actions stored in Project Memory
- Timeline updated in real-time
- Vibe Kanban reflects current status

**Git Integration:**
- Each RALPHY loop = isolated worktree
- Main Agent reviews each worktree
- Good merges = accepted
- Bad merges = feedback + retry

**Final State:**
```
✅ 25/25 tasks complete
✅ All tests passing
✅ Documentation complete
✅ Code reviewed and merged
✅ Deployed to staging
✅ Project Memory updated with learnings
```

---

## Key Architectural Components

### 1. **Main Agent (Orchestrator)**
- **Location:** `main.py` (central coordinator)
- **Responsibilities:**
  - Receive user requests
  - Coordinate planning agents
  - Monitor Vibe Kanban board
  - Make routing decisions
  - Review work quality
  - Merge Git changes

### 2. **Planning Agents**
- **Mary (Analyst)** - Research, requirements, competitive analysis
- **Winston (Planning)** - Task breakdown, dependency mapping
- **Arthur (Architect)** - Technical architecture, design patterns
- **RALPHY** - Autonomous loop for complex planning

### 3. **Execution Agents**
- **Amelia (Developer)** - Coding, implementation, debugging
- **Alex (Architect)** - Architecture, design patterns
- **TEAAgent** - Testing, quality assurance
- **TechWriter** - Documentation
- **Plus 15+ specialist agents**

### 4. **Vibe Kanban Integration**
- **Purpose:** Visual project management
- **Features:**
  - Task cards with status
  - Dependency tracking
  - Agent assignment
  - Progress monitoring
  - Blocking issue flags

### 5. **Project Memory System**
- **Purpose:** Single source of truth for all project data
- **Contents:**
  - Agent sessions and decisions
  - Code indexes and understanding
  - Timeline of all work
  - Learnings and patterns
  - Git integration history

### 6. **Skills System**
- **Purpose:** Train agents for specific capabilities
- **Structure:** Hierarchical skill definitions
- **Usage:** Agents load and follow skill protocols

### 7. **RALPHY Runtime**
- **Purpose:** Autonomous multi-iteration execution
- **Use Case:** Complex tasks requiring multiple iterations
- **Features:**
  - Git worktree isolation
  - Iteration planning
  - Self-review
  - Quality gates
  - Automatic retry on failure

---

## Success Criteria

BlackBox5 is working correctly when:

### ✅ User Can:
1. Describe a feature in natural language
2. Get a complete PRD and task breakdown
3. Watch agents work in parallel on Vibe Kanban
4. See all thought processes and decisions
5. Review and merge completed work
6. Access complete project history

### ✅ System Does:
1. Route tasks to appropriate agents automatically
2. Track all work in Project Memory
3. Show agent thinking (not just output)
4. Use skills for consistent quality
5. Execute RALPHY loops for complex tasks
6. Merge only quality work to Git

### ✅ Continuous Learning:
1. Every session archived
2. Patterns identified and reused
3. Skills improved based on usage
4. Bad patterns flagged and avoided
5. System gets smarter with each project

---

## Current Implementation Status

### ✅ What Works:
- Core architecture (engine/memory separation)
- BMAD methodology (10 specialized agents)
- Vibe Kanban integration
- Project Memory system (4-layer memory)
- Skills system (70 skills, 47% verified)
- Basic agent coordination

### ⚠️ What Needs Work:
- **Main Agent** - Needs API fixes (PLAN-008)
- **Planning Agent** - Not implemented (PLAN-003)
- **YAML Agent Loading** - Only 3 of 21 agents work (PLAN-002)
- **Skills System** - 3 duplicate systems (PLAN-001)
- **RALPHY Integration** - Partially implemented
- **Git Worktree Pattern** - Not adopted (high priority)

### 🚨 What's Broken:
- **main.py** - API mismatches (PLAN-008)
- **Import paths** - Multiple broken (PLAN-004)
- **Dependencies** - Missing from requirements.txt (PLAN-010)

---

## Vision vs Reality

### The Vision (What We're Building)
A fully autonomous AI development platform where:
1. Users describe goals in natural language
2. AI breaks down into executable tasks
3. Specialized agents work in parallel
4. RALPHY handles complex iterative tasks
5. Everything tracked in Project Memory
6. System learns and improves continuously

### The Reality (What We Have)
- Strong foundation (85% complete)
- Core components working
- Critical bugs blocking execution
- Missing some key pieces (Planning Agent)
- Some redundancy to clean up

### The Path Forward
1. **Fix Critical Bugs** (PLAN-008, 009, 010) - 3-4 hours
2. **Implement Missing Pieces** (PLAN-001, 002, 003, 005) - 1-2 weeks
3. **Complete Skills System** (validation, verification) - 2-3 weeks
4. **Full RALPHY Integration** (git worktree pattern) - 1 week
5. **Testing & Optimization** - 1-2 weeks

**Total: 4-6 weeks to fully functional system**

---

## Conclusion

BlackBox5 represents a **paradigm shift** in software development:
- From manual to AI-assisted
- From isolated to collaborative
- From opaque to transparent
- From one-off to continuous learning

The core insight is that **AI agents working together, with proper coordination and memory, can build software better and faster than humans alone** - while maintaining quality, transparency, and continuous improvement.

**Status:** Vision defined, architecture sound, implementation 85% complete
**Next:** Fix critical bugs, complete missing pieces, full integration testing

---

**Last Updated:** 2026-01-20
**Maintained By:** BlackBox5 Development Team
**Version:** 1.0 (Core Vision)
