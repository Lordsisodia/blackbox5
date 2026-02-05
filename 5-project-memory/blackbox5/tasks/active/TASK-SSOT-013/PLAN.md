# PLAN.md: Split CLAUDE.md - Engine vs Project

**Task:** TASK-SSOT-013 - CLAUDE.md mixes engine and project instructions
**Status:** Planning
**Created:** 2026-02-06
**Estimated Effort:** 2-3 hours
**Importance:** 75 (High)

---

## 1. First Principles Analysis

### The Core Problem
CLAUDE.md files contain mixed content:
- `~/.claude/CLAUDE.md` - Global instructions (may have engine content)
- Project-specific instructions embedded in global file

This creates:
1. **Confusion**: Unclear which instructions apply where
2. **Maintenance Issues**: Project changes require global file edits
3. **Portability**: Hard to move project to different environment
4. **Scope Creep**: Global file grows with project-specific content

### Guiding Principle
- **Global = Universal**: Instructions applicable to all projects
- **Project = Specific**: Instructions only for this project
- **Clear Separation**: No project content in global files
- **Hierarchical Loading**: Global → Project → Task

---

## 2. Current State Analysis

### File Locations

| File | Current Content | Should Be |
|------|-----------------|-----------|
| `~/.claude/CLAUDE.md` | Universal + some project-specific | Universal only |
| `5-project-memory/blackbox5/.claude/CLAUDE.md` | May not exist | Project-specific |

### Issues

1. **Mixed Concerns**: Global file has project instructions
2. **Missing Project File**: No dedicated project CLAUDE.md
3. **Unclear Precedence**: Which instructions take priority?

---

## 3. Proposed Solution

### Decision: Hierarchical CLAUDE.md Structure

**Loading Order:**
1. `~/.claude/CLAUDE.md` - Global universal instructions
2. `5-project-memory/blackbox5/.claude/CLAUDE.md` - Project-specific
3. `5-project-memory/blackbox5/tasks/active/TASK-XXX/.claude/CLAUDE.md` - Task-specific (optional)

### Implementation Plan

#### Phase 1: Audit Global CLAUDE.md (30 min)

1. Read `~/.claude/CLAUDE.md`
2. Identify project-specific sections:
   - BlackBox5-specific commands
   - Project-specific workflows
   - BlackBox5 directory references
   - Task-specific instructions

#### Phase 2: Create Project CLAUDE.md (1 hour)

**File:** `5-project-memory/blackbox5/.claude/CLAUDE.md`

```markdown
# BlackBox5 Project Instructions

## Project-Specific Commands

- `bb5 <command>` - BlackBox5 CLI
- `bb5 task:list` - List tasks
- `bb5 goal:show [ID]` - Show goal details

## Project Structure

```
5-project-memory/blackbox5/
├── tasks/active/     # Current tasks
├── goals/active/     # Current goals
├── runs/             # Run history
└── .autonomous/      # Autonomous system
```

## Workflows

### Starting a Task
1. Read task file completely
2. Create run directory
3. Execute task
4. Update task status

## BlackBox5-Specific Rules

- Always use `bb5` CLI for navigation
- Update STATE.yaml after significant changes
- Follow RALF workflow for autonomous tasks
```

#### Phase 3: Clean Global CLAUDE.md (1 hour)

Remove from global file:
- BlackBox5-specific commands
- Project directory references
- Task-specific workflows

Keep in global file:
- Universal coding standards
- General best practices
- Tool usage guidelines

#### Phase 4: Update Documentation (30 min)

1. Document hierarchical loading
2. Explain when to use each level
3. Add examples

---

## 4. Files to Modify

### New Files
1. `5-project-memory/blackbox5/.claude/CLAUDE.md` - Project instructions

### Modified Files
1. `~/.claude/CLAUDE.md` - Remove project-specific content

---

## 5. Success Criteria

- [ ] Project CLAUDE.md created with BlackBox5-specific instructions
- [ ] Global CLAUDE.md cleaned of project content
- [ ] Hierarchical loading documented
- [ ] No project references in global file
- [ ] Instructions work correctly at each level

---

## 6. Rollback Strategy

If issues arise:

1. **Immediate**: Restore original global CLAUDE.md
2. **Fix**: Debug project file
3. **Re-apply**: Once fixed

---

## 7. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Audit | 30 min | 30 min |
| Phase 2: Create Project File | 1 hour | 1.5 hours |
| Phase 3: Clean Global | 1 hour | 2.5 hours |
| Phase 4: Documentation | 30 min | 3 hours |
| **Total** | | **2-3 hours** |

---

*Plan created based on SSOT violation analysis - CLAUDE.md mixes engine and project*
