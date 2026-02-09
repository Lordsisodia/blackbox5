# PLAN.md: Split CLAUDE.md - Engine vs Project

**Task:** TASK-SSOT-039 - CLAUDE.md mixes engine and project instructions
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 2-3 hours
**Importance:** 70 (High)

---

## 1. First Principles Analysis

### The Core Problem
CLAUDE.md contains mixed content:
- Global instructions with project-specific content
- No separation between universal and project-specific
- Hard to maintain
- Confusing scope

This creates:
1. **Scope Confusion**: Unclear which instructions apply where
2. **Maintenance Issues**: Project changes require global edits
3. **Portability**: Hard to move project
4. **Clutter**: Global file grows with project content

### First Principles Solution
- **Hierarchical Structure**: Global → Project → Task
- **Clear Separation**: Universal vs specific
- **Explicit Loading**: Each level explicitly defined
- **Documentation**: Clear guidance on each level

---

## 2. Proposed Solution

### Hierarchical CLAUDE.md Structure

**Level 1: Global** (`~/.claude/CLAUDE.md`)
- Universal coding standards
- General best practices
- Tool usage guidelines

**Level 2: Project** (`5-project-memory/blackbox5/.claude/CLAUDE.md`)
- BlackBox5-specific commands
- Project workflows
- Directory structure

**Level 3: Task** (`tasks/active/TASK-XXX/.claude/CLAUDE.md`)
- Task-specific instructions
- Context for specific task

### Project CLAUDE.md Template

```markdown
# BlackBox5 Project Instructions

## Project Overview
BlackBox5 is an autonomous task execution system with RALF workflow.

## Project Commands

### bb5 CLI
- `bb5 whereami` - Show current location
- `bb5 task:list` - List tasks
- `bb5 task:show [ID]` - Show task details
- `bb5 goal:show [ID]` - Show goal details

## Directory Structure

```
5-project-memory/blackbox5/
├── tasks/active/     # Current tasks
├── goals/active/     # Current goals
├── runs/             # Run history
├── .autonomous/      # Autonomous system
│   ├── agents/       # Agent definitions
│   ├── bin/          # Scripts
│   └── context/      # Context files
└── operations/       # Operations data
```

## Workflows

### Starting a Task
1. Read task file completely
2. Create run directory with THOUGHTS.md, DECISIONS.md
3. Execute task
4. Update task status
5. Document learnings

### RALF Workflow
- **Review**: Check current state
- **Align**: Confirm understanding
- **Load**: Gather context
- **Fulfill**: Execute task

## BlackBox5-Specific Rules

- Always use `bb5` CLI for navigation
- Update STATE.yaml after significant changes
- Follow RALF workflow for autonomous tasks
- Document decisions in DECISIONS.md
- Log thoughts in THOUGHTS.md
```

### Implementation Plan

#### Phase 1: Audit Global CLAUDE.md (30 min)

Identify project-specific content:
- BlackBox5 commands
- Project directory references
- Task-specific workflows

#### Phase 2: Create Project CLAUDE.md (1 hour)

1. Create `.claude/` directory in project
2. Create CLAUDE.md with project-specific content
3. Include all BlackBox5-specific instructions

#### Phase 3: Clean Global CLAUDE.md (1 hour)

Remove from global:
- BlackBox5-specific commands
- Project directory references
- Task-specific workflows

Keep in global:
- Universal coding standards
- General best practices
- Tool usage guidelines

#### Phase 4: Document Hierarchy (30 min)

Document the loading order:
1. Global CLAUDE.md
2. Project CLAUDE.md
3. Task CLAUDE.md (if exists)

---

## 3. Success Criteria

- [ ] Project CLAUDE.md created
- [ ] Global CLAUDE.md cleaned
- [ ] Hierarchy documented
- [ ] Instructions work at each level

---

## 4. Estimated Timeline

| Phase | Duration |
|-------|----------|
| Audit | 30 min |
| Project File | 1 hour |
| Clean Global | 1 hour |
| Documentation | 30 min |
| **Total** | **2-3 hours** |

---

*Plan created based on SSOT violation analysis*
