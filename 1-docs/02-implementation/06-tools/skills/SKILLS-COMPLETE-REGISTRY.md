# Black Box 5 Skills Registry

**Date**: 2026-01-30
**Status**: Complete Inventory of All Skills
**Purpose**: Central registry of all skills in Black Box 5

**Update**: Tier 2 BMAD skills have been converted to Agent Skills Standard format.

---

## Overview

This registry provides a complete inventory of all skills in Black Box 5, organized by tier and category.

---

## Tier 1: Engine Skills (Python-Based)

**Location**: `2-engine/01-core/agents/skills/`
**Purpose**: Engine-internal operations
**Format**: Python classes + JSON
**Loading**: SkillManager runtime import

### Engine Skill Categories

#### 1. Memory Operations
- **Path**: `2-engine/01-core/agents/skills/memory/`
- **Purpose**: Memory system operations
- **Skills**:
  - `memory_read.py` - Read from memory system
  - `memory_write.py` - Write to memory system
  - `memory_search.py` - Search memory
  - `memory_compress.py` - Compress old memories

#### 2. Task Orchestration
- **Path**: `2-engine/01-core/agents/skills/tasks/`
- **Purpose**: Task management
- **Skills**:
  - `task_create.py` - Create tasks
  - `task_update.py` - Update task status
  - `task_query.py` - Query tasks
  - `task_dependencies.py` - Manage dependencies

#### 3. Hook Management
- **Path**: `2-engine/01-core/agents/skills/hooks/`
- **Purpose**: Claude Code hooks
- **Skills**:
  - `hook_register.py` - Register hooks
  - `hook_trigger.py` - Trigger hooks
  - `hook_validate.py` - Validate hook responses

#### 4. Agent Operations
- **Path**: `2-engine/01-core/agents/skills/agents/`
- **Purpose**: Agent lifecycle
- **Skills**:
  - `agent_spawn.py` - Spawn new agents
  - `agent_communicate.py` - Agent communication
  - `agent_terminate.py` - Terminate agents

---

## Tier 2: Agent Skills (Markdown-Based)

**Location**: `~/.claude/skills/`
**Purpose**: Cross-platform agent capabilities
**Format**: SKILL.md with YAML frontmatter (Agent Skills Standard)
**Status**: BMAD skills converted ✅

### BMAD Agent Skills (Converted)

All 9 BMAD skills have been converted to Agent Skills Standard format:

| Skill | Agent | Role | Commands | Status |
|-------|-------|------|----------|--------|
| `bmad-pm` | John | Product Manager | CP, VP, EP, CE, IR, CC | ✅ Converted |
| `bmad-architect` | Alex | Architect | CA, VA, EA, IR | ✅ Converted |
| `bmad-analyst` | Mary | Business Analyst | BP, RS, CB, DP | ✅ Converted |
| `bmad-sm` | Sam | Scrum Master | SP, CS, ER, CC | ✅ Converted |
| `bmad-ux` | Uma | UX Designer | CU, VU, EU | ✅ Converted |
| `bmad-dev` | Amelia | Developer | DS, CR, QD | ✅ Converted |
| `bmad-qa` | Quinn | QA Engineer | QA, VT, RT | ✅ Converted |
| `bmad-quick-flow` | Barry | Solo Dev | TS, QD, CR | ✅ Converted |
| `bmad-tea` | TEA | Task Execution Agent | TE | ✅ Converted |

**Location**: `~/.claude/skills/bmad-*/SKILL.md`
**Format**: YAML frontmatter + Markdown content
**Loading**: On-demand via SkillManager with progressive disclosure

### Current Agent Skills Inventory

#### 1. Database Operations

##### **supabase-ddl-rls**
- **Path**: `2-engine/04-work/modules/skills/supabase-ddl-rls.md`
- **Format**: Simple markdown
- **Purpose**: Supabase DDL and RLS operations
- **Content**:
  - DDL rules
  - Migration naming
  - RLS checklist
  - Security advisors
- **Status**: ⚠️ Needs conversion to Agent Skills standard
- **Priority**: HIGH

##### **siso-tasks**
- **Path**: `2-engine/04-work/modules/skills/siso-tasks/`
- **Format**: MCP-based (prompt.md + skill.json)
- **Purpose**: Query SISO tasks from Supabase
- **MCP Server**: `siso-internal-supabase`
- **Commands**:
  - `/tasks` - List pending tasks
  - `/tasks urgent` - Show urgent tasks
  - `/tasks overdue` - Show overdue tasks
  - `/tasks high` - Show high priority tasks
  - `/tasks search <keyword>` - Search tasks
  - `/tasks stats` - Task statistics
  - `/tasks my` - My assigned tasks
  - `/tasks today` - Tasks due today
  - `/tasks recent` - Recent tasks
- **Status**: ⚠️ Needs MCP-to-CLI conversion
- **Priority**: HIGH

#### 2. Development Workflow

##### **repo-codebase-navigation**
- **Path**: `2-engine/04-work/modules/skills/repo-codebase-navigation.md`
- **Format**: Simple markdown
- **Purpose**: Navigate and understand codebase
- **Status**: ⚠️ Needs conversion
- **Priority**: MEDIUM

##### **testing-playbook**
- **Path**: `2-engine/04-work/modules/skills/testing-playbook.md`
- **Format**: Simple markdown
- **Purpose**: Testing procedures and patterns
- **Status**: ⚠️ Needs conversion
- **Priority**: MEDIUM

#### 3. Process & Planning

##### **feedback-triage**
- **Path**: `2-engine/04-work/modules/skills/feedback-triage.md`
- **Format**: Simple markdown (structured)
- **Purpose**: Convert feedback to prioritized backlog
- **Content**:
  - Purpose
  - Trigger conditions
  - Output artifacts
  - Taxonomy (type, severity, confidence, surface)
  - Output format
- **Status**: ✅ Already well-structured, minor updates needed
- **Priority**: HIGH

#### 4. Integration

##### **notifications-local**
- **Path**: `2-engine/04-work/modules/skills/notifications-local.md`
- **Format**: Simple markdown
- **Purpose**: Local notification workflows
- **Status**: ⚠️ Needs conversion
- **Priority**: LOW

---

## Converted Skills (Agent Skills Standard)

**Location**: `~/.claude/skills/`
**Format**: SKILL.md (YAML + Markdown)
**Status**: ✅ Created and operational

### Converted Skills Inventory

#### BMAD Skills (9 skills)
All BMAD skills converted to Agent Skills Standard:

1. **bmad-pm** - Product Manager (John)
2. **bmad-architect** - Architect (Alex)
3. **bmad-analyst** - Analyst (Mary)
4. **bmad-sm** - Scrum Master (Sam)
5. **bmad-ux** - UX Designer (Uma)
6. **bmad-dev** - Developer (Amelia)
7. **bmad-qa** - QA Engineer (Quinn)
8. **bmad-quick-flow** - Quick Flow (Barry)
9. **bmad-tea** - Task Execution Agent (TEA)

#### Other Skills (16 skills)

**Development & Operations**:
- `feedback-triage` - Convert feedback to prioritized backlog
- `git-workflows` - Codebase navigation and git operations
- `testing-patterns` - Testing procedures and patterns
- `run-initialization` - Initialize Blackbox5 workflows
- `supabase-operations` - Database operations for SISO Internal
- `siso-tasks-cli` - Query SISO tasks from Supabase

**n8n Integration** (7 skills):
- `n8n-code-javascript` - JavaScript in n8n Code nodes
- `n8n-code-python` - Python in n8n Code nodes
- `n8n-expression-syntax` - n8n expression syntax
- `n8n-mcp-tools-expert` - n8n MCP tools expert
- `n8n-node-configuration` - n8n node configuration
- `n8n-validation-expert` - n8n validation expert
- `n8n-workflow-patterns` - n8n workflow patterns

**Integrations**:
- `notifications-local` - Local notification workflows
- `notion-mcp` - Notion integration via MCP
- `test-skill` - Test skill for Tier 2 integration

**Total Converted Skills**: 25 skills

### Planned Conversions

#### Phase 1: High Priority (Week 1)

1. **supabase-operations**
   - **Source**: `supabase-ddl-rls.md`
   - **Target**: `~/.claude/skills/supabase-operations/SKILL.md`
   - **Commands**:
     - Migration execution
     - RLS validation
     - Security checks
     - Type generation

2. **siso-tasks-cli**
   - **Source**: `siso-tasks/`
   - **Target**: `~/.claude/skills/siso-tasks-cli/SKILL.md`
   - **Conversion**: MCP-to-CLI
   - **Commands**:
     - Task listing
     - Task searching
     - Task statistics

3. **feedback-triage**
   - **Source**: `feedback-triage.md`
   - **Target**: `~/.claude/skills/feedback-triage/SKILL.md`
   - **Enhancements**:
     - YAML frontmatter
     - Detailed workflows
     - Templates
     - Examples

4. **git-workflows**
   - **Source**: `repo-codebase-navigation.md`
   - **Target**: `~/.claude/skills/git-workflows/SKILL.md`
   - **Commands**:
     - Repository navigation
     - Code search
     - Branch management
     - History inspection

#### Phase 2: Medium Priority (Week 2)

5. **testing-patterns**
   - **Source**: `testing-playbook.md`
   - **Target**: `~/.claude/skills/testing-patterns/SKILL.md`
   - **Sub-skills**:
     - `unit-testing/`
     - `integration-testing/`
     - `e2e-testing/`

6. **notifications-local**
   - **Source**: `notifications-local.md`
   - **Target**: `~/.claude/skills/notifications-local/SKILL.md`
   - **Commands**:
     - Desktop notifications
     - System alerts
     - Notification routing

---

## Legacy Skills (Archived)

**Location**: `.blackbox/.skills/` (archived) and `2-engine/.autonomous/skills/`
**Status**: No longer actively maintained

### Legacy BMAD Skills (Source)
The original BMAD skills in `2-engine/.autonomous/skills/` are now considered legacy source files. The converted versions in `~/.claude/skills/` are the canonical versions.

**Source Files** (for reference):
- `bmad-pm.md`, `bmad-architect.md`, `bmad-analyst.md`, `bmad-sm.md`, `bmad-ux.md`
- `bmad-dev.md`, `bmad-qa.md`, `bmad-quick-flow.md`, `bmad-tea.md`

### Legacy Skills Inventory

From `SKILLS-CONVERSION-FINAL-SUMMARY.md`:

- **Total Created**: 41 skills
- **Status**: 59% complete (target was 70)
- **Format**: XML-based Agent OS format
- **Location**: `.blackbox5/engine/agents/.skills-new/`

### Categories Created

1. **Database Operations**
   - `orm-patterns/` - Prisma/Drizzle ORM
   - `migrations/` - Database migrations

2. **Testing Quality**
   - `integration-testing/` - API testing
   - `e2e-testing/` - Playwright E2E tests

3. **Deployment Ops**
   - `ci-cd/` - GitHub Actions CI/CD
   - `kubernetes/` - K8s deployments

4. **Collaboration Communication**
   - `task-automation/` - Task automation

**Note**: These were created in XML format for Agent OS. May need conversion to Agent Skills standard if still relevant.

---

## Skills by Category

### Database Skills
- `supabase-ddl-rls` (Tier 2)
- `siso-tasks` (Tier 2, MCP-based)
- `orm-patterns` (Legacy)
- `migrations` (Legacy)

### Development Skills
- `repo-codebase-navigation` (Tier 2)
- `testing-playbook` (Tier 2)
- `integration-testing` (Legacy)
- `e2e-testing` (Legacy)

### Process Skills
- `feedback-triage` (Tier 2)
- `task-automation` (Legacy)

### Integration Skills
- `notifications-local` (Tier 2)
- `ci-cd` (Legacy)
- `kubernetes` (Legacy)

### Engine Skills (Tier 1)
- Memory operations
- Task orchestration
- Hook management
- Agent operations

---

## Skills Conversion Status

| Skill | Current Format | Target Format | Priority | Status |
|-------|---------------|---------------|----------|--------|
| `bmad-*` (9 skills) | Markdown | SKILL.md | HIGH | ✅ Complete |
| `supabase-operations` | Simple MD | SKILL.md | HIGH | ✅ Complete |
| `siso-tasks-cli` | MCP-based | SKILL.md (CLI) | HIGH | ✅ Complete |
| `feedback-triage` | Structured MD | SKILL.md | HIGH | ✅ Complete |
| `git-workflows` | Simple MD | SKILL.md | HIGH | ✅ Complete |
| `testing-patterns` | Simple MD | SKILL.md | MEDIUM | ✅ Complete |
| `notifications-local` | Simple MD | SKILL.md | LOW | ✅ Complete |
| `run-initialization` | Markdown | SKILL.md | MEDIUM | ✅ Complete |
| `n8n-*` (7 skills) | Various | SKILL.md | MEDIUM | ✅ Complete |
| `notion-mcp` | Markdown | SKILL.md | LOW | ✅ Complete |
| `test-skill` | Markdown | SKILL.md | LOW | ✅ Complete |
| `orm-patterns` | XML (Legacy) | SKILL.md | LOW | Not started |
| `migrations` | XML (Legacy) | SKILL.md | LOW | Not started |
| `integration-testing` | XML (Legacy) | SKILL.md | LOW | Not started |
| `e2e-testing` | XML (Legacy) | SKILL.md | LOW | Not started |
| `ci-cd` | XML (Legacy) | SKILL.md | LOW | Not started |
| `kubernetes` | XML (Legacy) | SKILL.md | LOW | Not started |
| `task-automation` | XML (Legacy) | SKILL.md | LOW | Not started |

---

## Skills Metadata

### Engine Skills (Tier 1)

**SkillManager Capabilities**:
- Total Skills: Dynamic (loaded at runtime)
- Categories: 5 (Memory, Tasks, Hooks, Agents, Tools)
- Skill Types: Operation, Workflow, Knowledge, Integration, Tool
- Loading: JSON + Python files
- Discovery: Filesystem scanning

### Agent Skills (Tier 2)

**Current Count**: 6 active skills
**Formats**: 2 types (Simple MD, MCP-based)
**MCP Servers Used**: 1 (`siso-internal-supabase`)
**Average Size**: 50-200 lines

### Legacy Skills

**Total Created**: 41 skills
**Format**: XML-based Agent OS
**Progress**: 59% complete
**Categories**: 3 main categories, 5 sub-categories

---

## Skills Dependencies

### Internal Dependencies

**Engine Skills**:
- Hook management → Memory operations
- Task orchestration → Agent operations
- All engine skills → SkillManager

**Agent Skills**:
- `supabase-ddl-rls` → Supabase CLI
- `siso-tasks` → `siso-internal-supabase` MCP server
- `testing-playbook` → Testing frameworks

### External Dependencies

**Tools Required**:
- Supabase CLI
- Claude Code (for Agent Skills)
- MCP servers (for MCP-based skills)
- Git CLI
- Testing frameworks (Jest, Playwright, etc.)

---

## Skills Usage Statistics

### Current Usage (Estimates)

| Skill | Usage Frequency | Users | Last Updated |
|-------|----------------|-------|--------------|
| `supabase-ddl-rls` | Daily | All devs | 2025-01-18 |
| `siso-tasks` | Daily | All users | 2026-01-16 |
| `feedback-triage` | Weekly | PMs, Devs | Unknown |
| `repo-codebase-navigation` | Weekly | All devs | Unknown |
| `testing-playbook` | As needed | QA, Devs | Unknown |
| `notifications-local` | Rarely | Devs | Unknown |

### Success Metrics

**Engine Skills**:
- Load time: <1 second
- Success rate: >99%
- Error handling: Comprehensive

**Agent Skills**:
- Discovery rate: Unknown (needs testing)
- Usage rate: Unknown (needs tracking)
- Error rate: Unknown (needs monitoring)

---

## Skills Maintenance

### Update Frequency

**Engine Skills**: As needed (code changes)
**Agent Skills**: Monthly or as workflows change
**Legacy Skills**: Archived (no updates)

### Version Tracking

**Engine Skills**: Git-based
**Agent Skills**: Manual (needs implementation)
**Legacy Skills**: XML-based versions

### Ownership

**Engine Skills**: BB5 Core Team
**Agent Skills**: SISO Internal Team
**Legacy Skills**: Archived (no owner)

---

## Skills Roadmap

### Q1 2026 (Jan-Mar)

**Phase 1: Foundation (January)**
- ✅ Document current system
- ✅ Create migration guide
- ⏳ Convert top 5 skills to Agent Skills standard
- ⏳ Test converted skills with Claude Code

**Phase 2: Expansion (February)**
- Convert remaining high-priority skills
- Create skill templates
- Document best practices
- Build skills registry

**Phase 3: Integration (March)**
- Integrate Tier 1 and Tier 2 skills
- Create bridge layer
- Test complete system
- Document architecture

### Q2 2026 (Apr-Jun)

**Phase 4: Optimization**
- Optimize token usage
- Improve discovery mechanism
- Add skill testing framework
- Create skill analytics

**Phase 5: Ecosystem**
- Publish skills to community
- Contribute to Agent Skills standard
- Create skill marketplace
- Build skill development tools

---

## Skills Documentation

### Core Documentation

1. **[BLACKBOX5-SKILLS-ANALYSIS.md](./BLACKBOX5-SKILLS-ANALYSIS.md)**
   - Complete analysis of BB5 skills system
   - Comparison with Agent Skills standard
   - Recommendations and best practices

2. **[SKILLS-MIGRATION-GUIDE.md](./SKILLS-MIGRATION-GUIDE.md)**
   - Step-by-step conversion guide
   - Conversion templates
   - Testing procedures

3. **[SKILLS-REGISTRY-README.md](./SKILLS-REGISTRY-README.md)**
   - How to use this registry
   - How to add new skills
   - How to update skills

4. **[SKILLS-TEMPLATES.md](./SKILLS-TEMPLATES.md)** (to be created)
   - Templates for common skill types
   - YAML frontmatter templates
   - Content structure templates

5. **[SKILLS-BEST-PRACTICES.md](./SKILLS-BEST-PRACTICES.md)** (to be created)
   - How to write effective skills
   - Common patterns and anti-patterns
   - Tips for token efficiency

6. **[SKILLS-REFERENCE.md](./SKILLS-REFERENCE.md)** (to be created)
   - Complete skills reference
   - Command reference
   - Workflow reference

---

## Skills Analytics

### Metrics to Track

1. **Discovery Metrics**
   - Skills discovered by agents
   - Skills loaded successfully
   - Skills failed to load

2. **Usage Metrics**
   - Skills used per session
   - Most used skills
   - Least used skills

3. **Performance Metrics**
   - Token usage per skill
   - Load time per skill
   - Error rate per skill

4. **Quality Metrics**
   - Skill completeness
   - Documentation quality
   - Example accuracy

### Reporting

**Monthly**:
- Skills usage report
- Skills performance report
- Skills quality report

**Quarterly**:
- Skills roadmap review
- Skills architecture review
- Skills ecosystem review

---

## Skills Governance

### Approval Process

**New Engine Skills**:
1. Create skill class
2. Add unit tests
3. Code review
4. Merge to main branch

**New Agent Skills**:
1. Create SKILL.md
2. Test with Claude Code
3. Peer review
4. Add to registry

### Deprecation Process

**Engine Skills**:
1. Mark as deprecated in code
2. Document replacement
3. Remove in next major version

**Agent Skills**:
1. Mark as deprecated in registry
2. Document replacement
3. Archive after 6 months

---

## Summary

**Total Skills**: 66 (25 active Tier 2, 4 Tier 1, 37 legacy/archived)

**Active Skills**: 29 (25 Tier 2 agent skills, 4 Tier 1 engine skill categories)

**Conversion Status**: 100% of high-priority skills converted to Agent Skills standard

**Next Actions**:
1. ✅ Create `~/.claude/skills/` directory
2. ✅ Convert BMAD skills (9 skills)
3. ✅ Convert other high-priority skills (16 skills)
4. ✅ Test with Claude Code
5. ✅ Update registry
6. Monitor skill usage and gather feedback

---

**Registry Version**: 1.1.0
**Last Updated**: 2026-01-30
**Next Review**: 2026-02-28
**Maintainer**: SISO Internal Team
