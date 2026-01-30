# Ralph Autonomous Agent - Project Specification

**Created**: 2026-01-30
**Location**: `blackbox5/5-project-memory/siso-internal/ralph.p/`
**Purpose**: Autonomous multi-project management for SISO ecosystem
**Target Machine**: MacBook (M1) - Initial setup, then migrate to Mac Mini (M4)

---

## Integration with BlackBox 5 Ralph System

This project-specific configuration extends the **existing Ralph infrastructure** in BlackBox 5:

| Component | Location | Purpose |
|-----------|----------|---------|
| Ralph Master Prompt | `2-engine/02-agents/implementations/04-specialists/4-specialists/ralph-agent/PROMPT.md` | Core autonomous loop behavior |
| Ralph Protocol | `2-engine/02-agents/implementations/04-specialists/4-specialists/ralph-agent/protocol.md` | Session lifecycle & documentation |
| Ralph Runtime | `2-engine/07-operations/environment/lib/ralph-runtime/` | Execution engine |
| Ralph Manifest | `2-engine/02-agents/implementations/04-specialists/4-specialists/ralph-agent/manifest.json` | Agent configuration |
| **This Config** | `5-project-memory/siso-internal/ralph.p/` | **Project-specific settings** |

---

## 1. PROJECT OVERVIEW

### Primary Goal
Run autonomous agents that manage multiple projects, build features, test functionality (connected to Supabase), and maintain organization - all while staying on the `dev` branch.

### Projects to Manage

#### 1. E-Commerce Client Project
**Priority**: HIGH
**Status**: Active development
**Branch**: `dev` (MUST stay on dev, main has working version)

**Work Areas**:
1. **Admin Section** - Sort out admin pages and functionality
2. **Feature Implementation** - Build specific functionalities (core logic only, UI later)
3. **Documentation** - Improve documentation side of things
4. **Architecture** - Small refactors only if required for functionality
5. **Idea Generation** - Organize existing documents, understand use cases

**Tech Stack**:
- Frontend: React/Next.js (assumed)
- Backend: Supabase (database + auth)
- API: GLM 4.7 + Kimi 2.5 for AI features

#### 2. SISO Internal App
**Priority**: MEDIUM
**Status**: Active
**Location**: Current project (`SISO-INTERNAL`)

**Work Areas**:
- Setup agent for organization
- Error prevention
- Idea generation and testing
- Feature implementation
- Project memory management

**Existing Infrastructure**:
- BlackBox 5 project memory system
- Ralph runtime (in `operations/agents/history/sessions/ralph/`)
- Ralph agent system (in `2-engine/02-agents/implementations/04-specialists/ralph-agent/`)
- STATE.yaml tracking
- GitHub integration

---

## 2. INFRASTRUCTURE

### 2.1 Brain Infrastructure (BlackBox 5)

**Location**: `blackbox5/5-project-memory/siso-internal/`

**Current Structure** (6 folders):
```
5-project-memory/siso-internal/
├── decisions/          # Why we're doing it this way
├── knowledge/          # How it works + learnings
├── operations/         # System operations
├── plans/              # What we're building
├── project/            # Project identity & direction
└── tasks/              # What we're working on
```

**Key Files**:
- `STATE.yaml` - Single source of truth
- `ACTIVE.md` - Dashboard of active work
- `WORK-LOG.md` - Activity log
- `FEATURE-BACKLOG.yaml` - Feature queue

**Tweaks Needed**:
- Simplify if necessary for autonomous operation
- Ensure Ralph can read/write to all locations
- Maintain existing structure (proven to work)

### 2.2 Task Organization

**Current System**:
- Tasks stored in `tasks/active/` and `tasks/working/`
- PRDs in `plans/prds/active/`
- Epics in `plans/active/[feature-name]/`
- State tracked in `STATE.yaml`

**Ralph Integration**:
- Ralph should read from `STATE.yaml` to understand current work
- Ralph should write to `WORK-LOG.md` for activity tracking
- Ralph should create tasks following existing template

### 2.3 API Keys & Commands

**Configured Commands**:
```bash
# GLM 4.7 (2,000 prompts / 5 hours)
claude

# Kimi 2.5 (500 prompts / 5 hours)
cso-kimi
```

**Usage Strategy**:
- **GLM**: Primary workhorse for coding tasks, research, documentation
- **Kimi**: Complex reasoning, architecture decisions, quality checks
- **Rate Limit Awareness**: Track usage to avoid hitting limits

---

## 3. RALPH CONFIGURATION

### 3.1 Agent Modes

#### Mode 1: Setup & Organization Agent
**Purpose**: Ensure project structure is correct, prevent errors
**Frequency**: Run once at startup, then periodically
**Tasks**:
- Validate project structure
- Check for missing documentation
- Ensure dev branch is active
- Verify Supabase connections
- Review STATE.yaml for inconsistencies

#### Mode 2: Feature Development Agent
**Purpose**: Build features based on PRDs and requirements
**Trigger**: When tasks are marked "ready for dev"
**Tasks**:
- Read PRD from `plans/prds/active/`
- Read epic from `plans/active/[feature]/`
- Implement core functionality (no UI polish)
- Write tests for Supabase connections
- Update task status in STATE.yaml

#### Mode 3: Idea Generation Agent
**Purpose**: Organize documents, generate new ideas
**Trigger**: Scheduled or on-demand
**Tasks**:
- Read existing documentation
- Identify gaps or opportunities
- Generate feature ideas
- Create PRDs for promising ideas
- Add to FEATURE-BACKLOG.yaml

#### Mode 4: Testing Agent
**Purpose**: Test functionality, ensure Supabase connections work
**Trigger**: After feature implementation
**Tasks**:
- Run automated tests
- Verify Supabase RLS policies
- Test API endpoints
- Document test results

### 3.2 Autonomous Loop Configuration

```yaml
ralph_config:
  # Timing
  check_interval: 300  # 5 minutes between checks
  max_session_duration: 14400  # 4 hours max per session

  # Branches
  allowed_branches:
    - dev
    - feature/*
  forbidden_branches:
    - main
    - master
    - production

  # Projects
  projects:
    - name: "ecommerce-client"
      path: "../ecommerce-client"  # Adjust as needed
      priority: high
      tasks:
        - admin_section
        - feature_implementation
        - documentation

    - name: "siso-internal"
      path: "."
      priority: medium
      tasks:
        - organization
        - idea_generation
        - feature_dev

  # API Usage
  api_rotation:
    primary: glm      # Use GLM for most tasks
    secondary: kimi   # Use Kimi for complex tasks
    fallback: glm     # Fallback to GLM if Kimi hits limits

  # Safety
  require_confirmation_for:
    - git_push
    - database_migration
    - branch_switch
    - destructive_operation

  auto_approve:
    - file_read
    - documentation_update
    - test_run
    - research
```

---

## 4. WORKFLOW

### 4.1 Daily Workflow

```
1. STARTUP (Manual or Scheduled)
   └─> Run setup agent
       └─> Check project structure
       └─> Verify dev branch
       └─> Check Supabase connections
       └─> Review STATE.yaml

2. PLANNING
   └─> Read STATE.yaml for active tasks
   └─> Read FEATURE-BACKLOG.yaml for pending features
   └─> Prioritize based on user goals

3. EXECUTION
   └─> For each task:
       └─> Read PRD/epic
       └─> Implement core functionality
       └─> Write tests
       └─> Update STATE.yaml
       └─> Log to WORK-LOG.md

4. TESTING
   └─> Run test suite
   └─> Verify Supabase connections
   └─> Document results

5. REPORTING
   └─> Update ACTIVE.md
   └─> Generate summary
   └─> Notify user of completed work
```

### 4.2 Branch Safety Protocol

**CRITICAL**: All work MUST stay on `dev` branch

```bash
# Before any work:
git branch --show-current  # Must show "dev"

# If not on dev:
git checkout dev
git pull origin dev

# Create feature branch from dev if needed:
git checkout -b feature/ralph-[task-name]

# Never merge to main without explicit approval
```

### 4.3 Supabase Integration

**Connection Check**:
```bash
# Verify Supabase is accessible
# Test RLS policies
# Verify table structures match PRD requirements
```

**Safety**:
- Always test on dev database first
- Never run migrations on production without approval
- Document all schema changes

---

## 5. FOLDER STRUCTURE

### 5.1 Ralph Project Folder (`blackbox5/ralph.p/`)

```
blackbox5/ralph.p/
├── PROJECT-SPEC.md          # This file - main specification
├── CONFIG.yaml              # Ralph runtime configuration
├── WORKFLOWS/
│   ├── setup-agent.md       # Setup & organization workflow
│   ├── feature-dev-agent.md # Feature development workflow
│   ├── idea-agent.md        # Idea generation workflow
│   └── test-agent.md        # Testing workflow
├── LOGS/
│   ├── sessions/            # Session logs
│   ├── errors/              # Error logs
│   └── performance/         # Performance metrics
├── STATE/
│   ├── current-session.yaml # Current session state
│   ├── task-queue.yaml      # Pending tasks
│   └── completed.yaml       # Completed work
└── SCRIPTS/
    ├── start-ralph.sh       # Start Ralph autonomous loop
    ├── stop-ralph.sh        # Stop Ralph gracefully
    └── status.sh            # Check Ralph status
```

### 5.2 Integration with BlackBox 5 Memory

Ralph reads from:
- `../5-project-memory/siso-internal/STATE.yaml`
- `../5-project-memory/siso-internal/ACTIVE.md`
- `../5-project-memory/siso-internal/FEATURE-BACKLOG.yaml`
- `../5-project-memory/siso-internal/tasks/active/`
- `../5-project-memory/siso-internal/plans/active/`

Ralph writes to:
- `../5-project-memory/siso-internal/WORK-LOG.md`
- `../5-project-memory/siso-internal/STATE.yaml` (updates)
- `../5-project-memory/siso-internal/tasks/working/`

---

## 6. IMPLEMENTATION STEPS

### Phase 1: Setup (Today - MacBook)

1. **Create Ralph configuration** ✅ (this document)
2. **Create CONFIG.yaml** with API settings
3. **Create workflow documents** for each agent mode
4. **Create startup scripts**
5. **Test Ralph on simple task** (e.g., update documentation)
6. **Verify branch safety** (ensure dev branch protection works)

### Phase 2: E-Commerce Project Integration

1. **Map e-commerce project structure**
2. **Identify admin section requirements**
3. **Create PRDs for missing features**
4. **Run feature development agent**
5. **Test Supabase connections**

### Phase 3: SISO Internal Enhancement

1. **Run setup agent** on SISO internal
2. **Generate ideas** from existing documents
3. **Implement high-priority features**
4. **Improve documentation**

### Phase 4: Mac Mini Migration

1. **Copy Ralph configuration** to Mac Mini
2. **Verify API keys** work on Mac Mini
3. **Test autonomous loop** for 24-hour period
4. **Optimize for 24/7 operation**

---

## 7. SAFETY & LIMITATIONS

### 7.1 Hard Limits

- **NO commits to main/master** - ever
- **NO production database changes** without explicit approval
- **NO destructive operations** without confirmation
- **Max 4 hours** per autonomous session (prevent runaway)
- **Rate limit tracking** - monitor GLM/Kimi usage

### 7.2 Soft Limits

- Prefer small, focused commits
- Document all decisions
- Test before marking complete
- Log all activity

### 7.3 User Override

User can always:
- Stop Ralph immediately
- Override any decision
- Change priorities
- Add new tasks
- Request human review

---

## 8. SUCCESS METRICS

### Short Term (This Week)

- [ ] Ralph runs successfully on MacBook
- [ ] Setup agent validates project structure
- [ ] Feature agent completes 1-2 small tasks
- [ ] All work stays on dev branch
- [ ] Supabase connections tested and working

### Medium Term (This Month)

- [ ] E-commerce admin section functional
- [ ] 5+ features implemented and tested
- [ ] Documentation improved
- [ ] Idea generation agent produces viable features
- [ ] Mac Mini running 24/7

### Long Term (Ongoing)

- [ ] Autonomous loop runs without errors
- [ ] New features regularly deployed to dev
- [ ] Project organization maintained
- [ ] Zero incidents on main branch

---

## 9. NEXT ACTIONS

1. **Review this document** - Ensure it matches your vision
2. **Create CONFIG.yaml** - API keys, project paths, settings
3. **Create workflow scripts** - Start with setup agent
4. **Test on MacBook** - Run first autonomous session
5. **Iterate** - Adjust based on results

---

**Document Owner**: Ralph Autonomous System
**Last Updated**: 2026-01-30
**Version**: 1.0
