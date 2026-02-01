# Black Box 5 Skills System: Complete Analysis & Documentation

**Date**: 2026-01-28
**Status**: Comprehensive Analysis
**Purpose**: Analyze current BB5 skills implementation vs Agent Skills standard

---

## Executive Summary

Black Box 5 has a **custom Python-based skills system** that differs significantly from the **Agent Skills Standard** (agentskills.io). Both approaches have strengths, but they serve different purposes:

| Aspect | BB5 Current System | Agent Skills Standard |
|--------|-------------------|----------------------|
| **Format** | Python classes + JSON | SKILL.md (YAML + Markdown) |
| **Discovery** | Filesystem scanning (`.py`, `.json`) | Filesystem scanning (`.md`) |
| **Loading** | Runtime import/parsing | On-demand context injection |
| **Extensibility** | Programmatic (code) | Declarative (docs + scripts) |
| **Agent Integration** | Direct Python API | Universal Claude/agents standard |
| **Best For** | Engine-internal operations | Cross-platform agent capabilities |

**Recommendation**: **Hybrid approach** - Keep BB5's engine-internal Python skills for operations, adopt Agent Skills standard for agent capabilities.

---

## Part 1: Current Black Box 5 Implementation

### Architecture Overview

```
blackbox5/
├── 2-engine/
│   ├── 01-core/agents/core/
│   │   └── skill_manager.py          # Core skills system
│   └── 04-work/modules/skills/       # Skill definitions
│       ├── README.md                 # Simple skills (legacy)
│       ├── feedback-triage.md        # Markdown skills
│       ├── supabase-ddl-rls.md      # Markdown skills
│       ├── testing-playbook.md       # Markdown skills
│       ├── repo-codebase-navigation.md
│       ├── notifications-local.md
│       ├── siso-tasks/
│       │   ├── prompt.md            # MCP-based skill
│       │   ├── skill.json           # JSON metadata
│       │   ├── examples/            # Example files
│       │   └── README.md
│       └── ...
└── 1-docs/02-implementation/06-tools/skills/
    ├── SKILLS-CONVERSION-FINAL-SUMMARY.md  # Conversion tracking
    ├── SKILLS-REGISTRY-README.md
    └── SKILLS-IMPORT-COMPLETE.md
```

### Core Components

#### 1. SkillManager (`skill_manager.py`)

**Purpose**: Central skill discovery and management system

**Key Features**:
- Loads skills from JSON and Python files
- Categorizes skills by type
- Maps skills to agents
- Runtime skill registration

**Skill Types**:
```python
class SkillType(Enum):
    OPERATION = "operation"      # Executable operations
    WORKFLOW = "workflow"        # Multi-step workflows
    KNOWLEDGE = "knowledge"      # Knowledge retrieval
    INTEGRATION = "integration"  # External system integrations
    TOOL = "tool"               # Utility tools
```

**Data Structure**:
```python
@dataclass
class Skill:
    name: str
    description: str
    category: str
    skill_type: SkillType
    capabilities: List[str]
    metadata: Dict[str, Any]
    enabled: bool
```

#### 2. Skill Formats Supported

**A. JSON Skills** (`skill.json`)
```json
{
  "name": "siso-tasks",
  "version": "1.0.0",
  "description": "Query and manage SISO Internal tasks",
  "category": "database",
  "tags": ["tasks", "supabase", "siso"],
  "mcp_server": "siso-internal-supabase",
  "commands": [...]
}
```

**B. Python Skills** (`.py` files)
- Classes with `__skill_name__` or `*Skill` naming
- `__skill_info__` dict metadata
- Direct executable code

**C. Markdown Skills** (`.md` files)
- Simple documentation format
- Used for: `feedback-triage.md`, `supabase-ddl-rls.md`, etc.
- NOT directly loaded by SkillManager
- Used as reference/documentation

#### 3. Current Skill Examples

**Example 1: SISO Tasks (MCP-based)**
- Location: `2-engine/04-work/modules/skills/siso-tasks/`
- Format: `prompt.md` + `skill.json`
- Purpose: Query Supabase via MCP server
- Commands: `/tasks`, `/tasks urgent`, `/tasks overdue`, etc.

**Example 2: Supabase DDL + RLS**
- Location: `2-engine/04-work/modules/skills/supabase-ddl-rls.md`
- Format: Simple markdown
- Purpose: Database schema rules
- Content: Checklists, triggers, advisors

**Example 3: Feedback Triage**
- Location: `2-engine/04-work/modules/skills/feedback-triage.md`
- Format: Simple markdown
- Purpose: Process feedback into backlog
- Content: Taxonomy, outputs, workflows

---

## Part 2: Agent Skills Standard

### Specification Overview

**Official Specification**: [agentskills.io/specification](https://agentskills.io/specification)

**Published**: December 18, 2025
**Status**: Universal open standard for LLM agent capabilities

### File Format

**Structure**: SKILL.md files with YAML frontmatter + Markdown content

```yaml
---
name: skill-name
description: Brief description
tags: [optional, list, of, tags]
author: Optional author
version: 1.0.0
---

# Skill Title

## Overview
Detailed explanation...

## Prerequisites
- Tool 1
- Tool 2

## Core Commands

### Command Name
```bash
command --arguments
```

**Description**: What it does

## Common Workflows

### Workflow 1: Task Name
1. Step one
2. Step two

## Troubleshooting

### Problem: Error
**Solution**: Fix
```

### Directory Structure

```
~/.claude/skills/
├── skill-one/
│   ├── SKILL.md
│   ├── scripts/
│   │   └── helper.sh
│   ├── configs/
│   └── resources/
└── skill-two/
    └── SKILL.md
```

### Discovery & Loading

1. **Automatic Scanning**: Agents scan `~/.claude/skills/` directory
2. **Frontmatter Parsing**: Read YAML metadata from SKILL.md
3. **Just-in-Time Loading**: Skills loaded when relevant (not upfront)
4. **Context Injection**: Two-message pattern for efficient loading

### Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| **Claude Code** | ✅ Native | `~/.claude/skills/` directory |
| **OpenCode** | ✅ Native | Open-source alternative |
| **Gemini CLI** | 🔄 In Progress | GitHub issue #11506 |
| **Cursor** | ✅ Supported | IDE integration |

---

## Part 3: Comparison & Analysis

### Key Differences

| Aspect | BB5 System | Agent Skills Standard |
|--------|-----------|----------------------|
| **Primary Use** | Engine-internal operations | Cross-platform agent capabilities |
| **Format** | Python code + JSON | Markdown + YAML |
| **Discovery** | Custom SkillManager | Universal filesystem scanning |
| **Extensibility** | Programmatic | Declarative + optional scripts |
| **Loading** | Runtime import | On-demand context injection |
| **Integration** | BB5 engine only | Any Claude/agents-compatible tool |
| **Token Efficiency** | N/A (engine-internal) | Optimized for LLM context |
| **Maintenance** | Requires Python knowledge | Markdown editing |
| **Portability** | BB5-specific | Universal |

### Strengths & Weaknesses

#### BB5 System

**Strengths**:
- ✅ Direct Python execution (full programmability)
- ✅ Type-safe (Python classes)
- ✅ Runtime skill registration
- ✅ Complex state management
- ✅ Engine integration (direct API access)
- ✅ Performance (no parsing overhead)

**Weaknesses**:
- ❌ BB5-specific (not portable)
- ❌ Requires Python knowledge to create
- ❌ Not compatible with Claude/agents ecosystem
- ❌ No standard discovery mechanism
- ❌ Heavier (code vs documentation)

#### Agent Skills Standard

**Strengths**:
- ✅ Universal compatibility (Claude, OpenCode, etc.)
- ✅ Simple to create (just Markdown)
- ✅ Token-efficient (on-demand loading)
- ✅ Portable (folder-based)
- ✅ Ecosystem support (growing rapidly)
- ✅ CLI-friendly (agents already trained on docs)

**Weaknesses**:
- ❌ No direct execution (requires scripts/tools)
- ❌ Limited to what's exposed via CLI/tools
- ❌ Less structured than Python classes
- ❌ Depends on external tools

---

## Part 4: What You're Currently Doing vs Best Practices

### Current BB5 Approach

**What You Have**:
1. **Python SkillManager** - Custom loading and management
2. **Mixed formats** - JSON, Python, Markdown
3. **MCP-based skills** - SISO tasks using MCP server
4. **Simple markdown skills** - Checklist-style docs
5. **Engine-internal focus** - Skills for BB5 operations

**What You're Doing Well**:
- ✅ Organized skill categories
- ✅ Multiple format support
- ✅ MCP integration for Supabase
- ✅ Comprehensive documentation

**What's Missing** (vs Agent Skills standard):
- ❌ YAML frontmatter for discoverability
- ❌ Standard SKILL.md format
- ❌ Universal agent compatibility
- ❌ On-demand loading (token efficiency)
- ❌ Cross-platform portability

### What the Research Says

**Best Practices from Research**:

1. **Start with Evaluations, Not Documentation**
   - Create evaluations BEFORE writing docs
   - Ensure skills solve real problems

2. **Assume Agent Brilliance**
   - Only add context agent doesn't have
   - Don't over-explain basics

3. **Provide Concrete Examples**
   - Real commands with actual output
   - Common workflow patterns

4. **Actionable Workflows**
   - Step-by-step procedures
   - Decision trees

5. **Token Efficiency**
   - Progressive disclosure (load details when needed)
   - Don't dump everything upfront

---

## Part 5: Best Version - Hybrid Approach

### Recommendation: Two-Tier Skills System

```
┌─────────────────────────────────────────────────────────────┐
│                    Black Box 5 Skills System               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Tier 1: Engine Skills (Python)                    │    │
│  │  ─────────────────────────────────────────────────  │    │
│  │  • Location: 2-engine/01-core/agents/skills/       │    │
│  │  • Format: Python classes + JSON                   │    │
│  │  • Purpose: Engine-internal operations             │    │
│  │  • Loading: SkillManager (runtime import)          │    │
│  │  • Examples:                                       │    │
│  │    - Agent lifecycle management                    │    │
│  │    - Memory system operations                      │    │
│  │    - Task orchestration                            │    │
│  │    - Hook management                               │    │
│  └────────────────────────────────────────────────────┘    │
│                          ↕                                  │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Tier 2: Agent Skills (Agent Skills Standard)      │    │
│  │  ─────────────────────────────────────────────────  │    │
│  │  • Location: ~/.claude/skills/                     │    │
│  │  • Format: SKILL.md (YAML + Markdown)              │    │
│  │  • Purpose: Cross-platform agent capabilities      │    │
│  │  • Loading: On-demand by Claude/agents             │    │
│  │  • Examples:                                       │    │
│  │    - Supabase CLI operations                       │    │
│  │    - Git workflows                                 │    │
│  │    - Testing patterns                              │    │
│  │    - MCP-to-CLI conversions                        │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Implementation Plan

#### Phase 1: Keep Engine Skills (Tier 1)

**What to Keep**:
- `skill_manager.py` - For engine-internal operations
- Python skill classes - For complex operations
- JSON skill definitions - For engine configuration

**Path**: `2-engine/01-core/agents/skills/`

**Example Structure**:
```
2-engine/01-core/agents/skills/
├── __init__.py
├── engine/
│   ├── memory_operations.py
│   ├── task_orchestration.py
│   └── hook_management.py
├── registry/
│   └── skills.json
└── README.md
```

#### Phase 2: Adopt Agent Skills Standard (Tier 2)

**What to Create**:
- `~/.claude/skills/` directory
- SKILL.md files for each agent capability
- Convert existing markdown skills to standard format

**Path**: `~/.claude/skills/` (global) or `blackbox5/.claude/skills/` (project-specific)

**Example Structure**:
```
.claude/skills/
├── supabase-operations/
│   └── SKILL.md
├── git-workflows/
│   ├── SKILL.md
│   └── scripts/
│       └── git-aliases.sh
├── testing/
│   ├── unit-testing/
│   │   └── SKILL.md
│   └── integration-testing/
│       └── SKILL.md
└── siso-tasks/
    ├── SKILL.md
    ├── scripts/
    │   └── task-query.sh
    └── examples/
        └── task-output.json
```

#### Phase 3: Bridge the Two Tiers

**Integration Strategy**:
1. Engine skills expose operations via CLI
2. Agent skills use those CLI commands
3. Clean separation of concerns

**Example**:
```python
# Engine skill (Tier 1)
class SupabaseOperationsSkill:
    """Engine-internal Supabase operations"""
    def __init__(self):
        self.cli_path = "/usr/local/bin/supabase"

    def execute_migration(self, migration_file: str):
        """Execute a Supabase migration"""
        # Direct Python execution
        pass
```

```yaml
---
name: supabase-operations
description: Supabase CLI operations for BB5
tags: [supabase, database, cli]
---

# Supabase Operations

## Commands

### Execute Migration
```bash
bb5-supabase migrate <file.sql>
```

**Description**: Execute a Supabase migration file

## Workflows
...
```

---

## Part 6: Migration Guide

### Converting Current Skills to Agent Skills Standard

#### Step 1: Audit Current Skills

**Current Skills Inventory**:
1. `feedback-triage.md` → Process/workflow skill
2. `supabase-ddl-rls.md` → Database operations skill
3. `testing-playbook.md` → Testing skill
4. `repo-codebase-navigation.md` → Development workflow
5. `notifications-local.md` → Integration skill
6. `siso-tasks/` → Database query skill (MCP-based)

#### Step 2: Convert to SKILL.md Format

**Template**:
```yaml
---
name: <skill-name>
description: <Brief description>
tags: [<tag1>, <tag2>, ...]
author: SISO Internal
version: 1.0.0
---

# <Skill Title>

## Purpose
<What this skill does>

## Prerequisites
- Required tools
- Environment setup

## Core Commands

### Command Name
```bash
command --arguments
```

**Description**: What it does

**Example**:
```bash
# Real example
command --flag value
```

**Expected Output**:
```
Example output
```

## Common Workflows

### Workflow 1: Name
1. Step one
2. Step two

## Troubleshooting

### Problem: Error
**Solution**: Fix
```

#### Step 3: Create Directory Structure

```bash
mkdir -p ~/.claude/skills/<skill-name>
# Create SKILL.md
# Add supporting files if needed
```

#### Step 4: Test with Agent

```bash
# Test with Claude Code
claude-code "Use the <skill-name> skill to..."
```

---

## Part 7: Supabase Multi-Project Support

### Challenge: Multiple Supabase Projects/Accounts

**Current Issue**:
- BB5 likely uses multiple Supabase projects
- Each project has different credentials
- Need project-specific skills

### Solution: Environment-Specific Skills

#### Approach 1: Per-Project Skills

```
~/.claude/skills/
├── supabase-project1/
│   └── SKILL.md          # Project 1 specific
├── supabase-project2/
│   └── SKILL.md          # Project 2 specific
└── supabase-common/
    └── SKILL.md          # Shared operations
```

**Skill Template**:
```yaml
---
name: supabase-project1
description: Supabase operations for Project1 (production)
tags: [supabase, project1, production]
project_id: proj1_***
access_token: SUPABASE_ACCESS_TOKEN_PROJECT1
---

# Supabase Project1 Operations

## Environment Setup
```bash
export SUPABASE_ACCESS_TOKEN=spb_***
export SUPABASE_PROJECT_ID=proj1_***
```

## Commands
...
```

#### Approach 2: CLI Wrapper Script

Create `supabase-wrapper.sh`:
```bash
#!/bin/bash
# Multi-project Supabase CLI wrapper

PROJECT=$1
COMMAND=${@:2}

case $PROJECT in
  "project1")
    export SUPABASE_ACCESS_TOKEN=spb_***
    export SUPABASE_PROJECT_ID=proj1_***
    ;;
  "project2")
    export SUPABASE_ACCESS_TOKEN=spb_***
    export SUPABASE_PROJECT_ID=proj2_***
    ;;
esac

supabase $COMMAND
```

**Usage in skill**:
```bash
supabase-wrapper.sh project1 db push
supabase-wrapper.sh project2 functions deploy
```

---

## Part 8: MCP-to-Skills Conversion

### Converting MCP Servers to CLI Skills

#### Using mcp2tool

**Installation**:
```bash
npm install -g @mcp-use/mcp2skill
```

**Usage**:
```bash
# Convert MCP server config
mcp2skill convert mcp-config.json

# Output: SKILL.md + supporting files
```

**Web Interface**: [mcp2skill.streamlit.app](https://mcp2skill.streamlit.app/)

#### Manual Conversion Process

**For SISO Tasks MCP** (current example):

1. **Analyze MCP Server**
   - Tool: `execute_sql`
   - Purpose: Query Supabase database
   - Tables: `public.tasks`

2. **Create CLI Equivalent**
   ```bash
   # Supabase CLI equivalent
   supabase db execute --query "SELECT * FROM tasks..."
   ```

3. **Create SKILL.md**
   ```yaml
   ---
   name: siso-tasks
   description: Query SISO Internal tasks from Supabase
   tags: [tasks, supabase, siso, cli]
   ---

   # SISO Tasks

   ## Commands

   ### List Tasks
   ```bash
   supabase db execute --query "SELECT * FROM tasks WHERE status = 'pending' LIMIT 50"
   ```
   ```

4. **Add Examples & Workflows**
   - Daily task review
   - Weekly planning
   - Task discovery

---

## Part 9: Best Practices Checklist

### For Creating Agent Skills

✅ **YAML Frontmatter**
- [ ] Name (kebab-case)
- [ ] Description (clear, concise)
- [ ] Tags (for discoverability)
- [ ] Version (optional)

✅ **Content Structure**
- [ ] Purpose (why use this skill)
- [ ] Prerequisites (what's needed)
- [ ] Core commands (with examples)
- [ ] Workflows (step-by-step)
- [ ] Troubleshooting (common issues)

✅ **Command Examples**
- [ ] Real command syntax
- [ ] Actual output examples
- [ ] Expected results
- [ ] Error handling

✅ **Token Efficiency**
- [ ] Progressive disclosure
- [ ] Don't dump everything
- [ ] Load details on-demand

✅ **Cross-References**
- [ ] Related skills
- [ ] External documentation
- [ ] See also links

### For Black Box 5 Engine Skills

✅ **Python Structure**
- [ ] Class-based (clean organization)
- [ ] `__skill_info__` metadata
- [ ] Type hints
- [ ] Error handling

✅ **Registration**
- [ ] SkillManager integration
- [ ] Category assignment
- [ ] Capability definitions
- [ ] Agent mapping

---

## Part 10: Documentation Checklist

### ✅ Required Documentation

**For Agent Skills (Tier 2)**:
- [x] This analysis document
- [ ] SKILLS-MIGRATION-GUIDE.md - How to convert existing skills
- [ ] SKILLS-REFERENCE.md - Complete skills reference
- [ ] SKILLS-TEMPLATES.md - Templates for common skill types
- [ ] SUPABASE-MULTI-PROJECT.md - Multi-project setup guide

**For Engine Skills (Tier 1)**:
- [x] skill_manager.py (existing)
- [ ] SKILL-DEVELOPMENT-GUIDE.md - How to create engine skills
- [ ] SKILL-ARCHITECTURE.md - Engine skills architecture
- [ ] SKILL-REGISTRY.md - Skills registry documentation

**For Integration**:
- [ ] SKILLS-BRIDGE.md - How Tier 1 and Tier 2 interact
- [ ] SKILLS-TESTING.md - How to test skills
- [ ] SKILLS-DEPLOYMENT.md - How to deploy skills

---

## Part 11: Action Items

### Immediate Actions

1. **✅ Document current system** (this file)
2. **Create `~/.claude/skills/` directory structure**
3. **Convert top 5 skills to Agent Skills standard**:
   - `supabase-operations`
   - `git-workflows`
   - `testing-patterns`
   - `feedback-triage`
   - `siso-tasks` (MCP-to-CLI conversion)

### Short-term Actions (Week 1-2)

1. **Create skill templates** for common patterns
2. **Set up multi-project Supabase skills**
3. **Test with Claude Code** to verify compatibility
4. **Document conversion process**

### Long-term Actions (Month 1)

1. **Convert all 30+ legacy skills** to Agent Skills standard
2. **Create comprehensive skills registry**
3. **Build skill testing framework**
4. **Integrate with BB5 engine** (bridge Tier 1 and Tier 2)

---

## Conclusion

Black Box 5 has a **solid foundation** with its Python-based skills system, but it's **limited to BB5 operations**. The **Agent Skills Standard** offers **universal compatibility** and **token efficiency** for agent capabilities.

**Best approach**: **Hybrid system** - Keep engine skills for BB5 internals, adopt Agent Skills standard for agent capabilities. This gives you:
- ✅ Engine performance (Python skills)
- ✅ Universal compatibility (Agent Skills)
- ✅ Token efficiency (on-demand loading)
- ✅ Cross-platform portability
- ✅ Ecosystem support

---

**Next Steps**:
1. Review this analysis
2. Decide on hybrid approach
3. Create migration plan
4. Begin skill conversion

---

**Document Version**: 1.0.0
**Last Updated**: 2026-01-28
**Author**: Claude (Black Box 5 Analysis)
