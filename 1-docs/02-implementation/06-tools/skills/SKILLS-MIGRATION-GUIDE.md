# Skills Migration Guide: Black Box 5 → Agent Skills Standard

**Date**: 2026-01-28
**Purpose**: Step-by-step guide for converting BB5 skills to Agent Skills standard

---

## Overview

This guide explains how to convert existing Black Box 5 skills to the universal Agent Skills standard format, ensuring compatibility with Claude Code, OpenCode, and other agent platforms.

---

## Understanding the Two Formats

### Current BB5 Format

**Simple Markdown Skills**:
```markdown
# Skill: Feedback Triage

## Purpose
Turn messy feedback into actionable backlog

## Trigger
- New feedback lands
- Pre-release review

## Outputs
1. Plan folder
2. Triage report
```

**MCP-Based Skills**:
- `prompt.md` - Instructions
- `skill.json` - Metadata
- Examples folder

### Agent Skills Standard Format

```yaml
---
name: feedback-triage
description: Turn feedback into prioritized backlog
tags: [feedback, triage, backlog, planning]
author: SISO Internal
version: 1.0.0
---

# Feedback Triage

## Purpose
Turn messy qualitative feedback into a prioritized, actionable backlog with clear ownership.

## When to Use
- New feedback lands (doc dump, QA notes, screenshots)
- Pre-release review
- Weekly "hygiene" pass

## Prerequisites
- Access to feedback sources
- Plan folder structure: `.blackbox/.plans/`

## Core Commands
...
```

---

## Migration Steps

### Step 1: Inventory Current Skills

**List all current skills**:
```bash
find blackbox5/2-engine/04-work/modules/skills -name "*.md" -o -name "*.json"
```

**Current Skills**:
1. `feedback-triage.md`
2. `supabase-ddl-rls.md`
3. `testing-playbook.md`
4. `repo-codebase-navigation.md`
5. `notifications-local.md`
6. `siso-tasks/` (folder with prompt.md, skill.json, examples)

### Step 2: Create Directory Structure

**Create global skills directory**:
```bash
mkdir -p ~/.claude/skills
```

**Or project-specific**:
```bash
mkdir -p blackbox5/.claude/skills
```

### Step 3: Convert Each Skill

#### Conversion Template

**For each skill**, follow this process:

1. **Create skill directory**:
   ```bash
   mkdir -p ~/.claude/skills/<skill-name>
   ```

2. **Create SKILL.md** with:
   - YAML frontmatter (name, description, tags)
   - Purpose section
   - Prerequisites
   - Core commands (with examples)
   - Common workflows
   - Troubleshooting

3. **Add supporting files** (if needed):
   - `scripts/` - Helper scripts
   - `examples/` - Example inputs/outputs
   - `configs/` - Configuration templates

#### Example: Feedback Triage

**Original** (`feedback-triage.md`):
```markdown
# Skill: Feedback Triage

## Purpose
Turn messy qualitative feedback into a **prioritized, actionable backlog** with clear ownership and next steps.

## Trigger (when to use)
- New feedback lands (doc dump, QA notes, screenshots)
- Pre-release review
- Weekly "hygiene" pass

## Outputs (artifacts)
1. A plan folder in `.blackbox/.plans/`
2. A triage report in that plan folder (suggested: `triage-report.md`)

## Taxonomy
For each item:
- Type: bug / UX confusion / missing feature / performance / data / docs
- Severity: blocker / high / medium / low
- Confidence: confirmed / likely / speculative
- Surface: UI / backend / database / architecture / docs

## Output format (suggested)
- Summary
- Themes
- Backlog (prioritized)
- Open questions
```

**Converted** (`~/.claude/skills/feedback-triage/SKILL.md`):
```yaml
---
name: feedback-triage
description: Turn qualitative feedback into prioritized, actionable backlog
tags: [feedback, triage, backlog, planning, qa]
author: SISO Internal
version: 1.0.0
---

# Feedback Triage

## Purpose
Turn messy qualitative feedback into a **prioritized, actionable backlog** with clear ownership and next steps.

## When to Use
- New feedback lands (doc dump, QA notes, screenshots)
- Pre-release review
- Weekly "hygiene" pass

## Prerequisites
- Access to feedback sources (docs, tickets, notes)
- Plan folder structure: `.blackbox/.plans/`
- Understanding of project context

## Core Process

### Step 1: Collect Feedback
Gather all feedback items from:
- Documentation
- QA notes
- Screenshots
- User reports
- Meeting notes

### Step 2: Categorize Each Item
For each feedback item, classify:

**Type**:
- `bug` - Defect or error
- `ux_confusion` - UI/UX issue
- `missing_feature` - Missing capability
- `performance` - Speed/responsiveness
- `data` - Data quality/accuracy
- `docs` - Documentation issue

**Severity**:
- `blocker` - Blocks release/critical functionality
- `high` - Important but not blocking
- `medium` - Should fix eventually
- `low` - Nice to have

**Confidence**:
- `confirmed` - Verified issue
- `likely` - Probable issue
- `speculative` - Needs investigation

**Surface**:
- `ui` - Frontend/interface
- `backend` - Server-side logic
- `database` - Data layer
- `architecture` - System design
- `docs` - Documentation

### Step 3: Create Output Artifacts

**Create Plan Folder**:
```bash
mkdir -p .blackbox/.plans/feedback-triage-$(date +%Y%m%d)
cd .blackbox/.plans/feedback-triage-$(date +%Y%m%d)
```

**Create Triage Report** (`triage-report.md`):
```markdown
# Feedback Triage Report

**Date**: YYYY-MM-DD
**Source**: <feedback source>

## Summary
<High-level summary of feedback>

## Themes
<Common patterns or issues>

## Backlog (Prioritized)

### 🔴 Blocker (X items)
1. [ ] <Issue description>
   - Type: <type>
   - Confidence: <confidence>
   - Surface: <surface>

### 🟠 High (X items)
...

### 🟡 Medium (X items)
...

### 🟢 Low (X items)
...

## Open Questions
<Items needing clarification>
```

## Common Workflows

### Workflow 1: Process New Feedback
1. Collect all feedback items
2. Create plan folder: `.blackbox/.plans/feedback-triage-<date>/`
3. Categorize each item by type, severity, confidence, surface
4. Create prioritized backlog
5. Generate triage report
6. Report summary

### Workflow 2: Weekly Hygiene Pass
1. Review recent feedback (last 7 days)
2. Update backlog items
3. Identify new themes
4. Check for resolved items
5. Adjust priorities

### Workflow 3: Pre-Release Review
1. Collect all pending feedback
2. Identify release-blocking issues
3. Verify high-severity items
4. Create release backlog
5. Document release notes

## Output Format

### Triage Report Structure
```markdown
# Feedback Triage Report

**Date**: YYYY-MM-DD
**Total Items**: X
**Blockers**: X
**High Priority**: X

## Summary
<Brief overview of feedback landscape>

## Key Themes
1. <Theme 1> (X occurrences)
2. <Theme 2> (X occurrences)
...

## Prioritized Backlog
<Blocker → High → Medium → Low>

## Open Questions
<Items needing investigation>
```

## Best Practices

1. **Be Specific**
   - Include reproduction steps for bugs
   - Add screenshots for UI issues
   - Reference related code/files

2. **Stay Objective**
   - Report facts, not opinions
   - Include evidence (logs, screenshots)
   - Note confidence levels

3. **Prioritize Ruthlessly**
   - If everything is high priority, nothing is
   - Consider impact vs effort
   - Focus on user-facing issues first

4. **Follow Up**
   - Track resolutions
   - Update confidence levels
   - Close the loop

## Troubleshooting

### Problem: Too Many Items
**Solution**: Group similar items, focus on themes, create separate triage sessions

### Problem: Unclear Severity
**Solution**: Use user impact as guide - blocker = affects critical functionality

### Problem: Low Confidence Items
**Solution**: Flag for investigation, don't prioritize until confirmed

### Problem: No Clear Owner
**Solution**: Assign based on surface (backend → backend team, etc.)

## Related Skills
- `bug-triage` - Specific to bug reports
- `feature-planning` - For feature requests
- `qa-review` - QA-specific workflows

## See Also
- [Black Box 5 Planning System](../../project-memory/planning/README.md)
- [Backlog Management Guide](../../workflows/backlog/README.md)
```

### Step 4: Add Supporting Files

**For Feedback Triage**:
```
~/.claude/skills/feedback-triage/
├── SKILL.md
├── templates/
│   └── triage-report.md
├── examples/
│   └── sample-triage-report.md
└── scripts/
    └── collect-feedback.sh
```

**Template** (`templates/triage-report.md`):
```markdown
# Feedback Triage Report

**Date**: {{DATE}}
**Source**: {{SOURCE}}
**Items Analyzed**: {{COUNT}}

## Summary
{{SUMMARY}}

## Themes
{{THEMES}}

## Backlog
{{BACKLOG}}
```

### Step 5: Test the Skill

**Test with Claude Code**:
```bash
claude-code
```

**Then**:
```
Use the feedback-triage skill to process the feedback in /path/to/feedback
```

**Verify**:
- [ ] Skill is discovered
- [ ] Commands are understood
- [ ] Output is generated correctly
- [ ] Examples are helpful

---

## Conversion Checklist

For each skill, verify:

### YAML Frontmatter
- [ ] `name` (kebab-case)
- [ ] `description` (clear, concise)
- [ ] `tags` (relevant, discoverable)
- [ ] `author` (attribution)
- [ ] `version` (tracking)

### Content Sections
- [ ] Purpose (why use this skill)
- [ ] When to Use (triggers)
- [ ] Prerequisites (what's needed)
- [ ] Core Process/Commands (how to use)
- [ ] Common Workflows (typical use cases)
- [ ] Output Format (what you get)
- [ ] Best Practices (tips for success)
- [ ] Troubleshooting (common issues)

### Supporting Files
- [ ] Templates (if applicable)
- [ ] Examples (if helpful)
- [ ] Scripts (if needed)
- [ ] Configs (if required)

### Cross-References
- [ ] Related skills (internal)
- [ ] See also (external docs)
- [ ] Dependencies (other skills/tools)

---

## Priority Conversion Order

### High Priority (Convert First)

1. **supabase-operations** (from `supabase-ddl-rls.md`)
   - Critical for database operations
   - High usage frequency

2. **siso-tasks** (from `siso-tasks/`)
   - MCP-to-CLI conversion
   - Daily task management

3. **feedback-triage** (from `feedback-triage.md`)
   - Common workflow
   - High impact

4. **git-workflows** (from `repo-codebase-navigation.md`)
   - Development operations
   - Universal applicability

5. **testing-patterns** (from `testing-playbook.md`)
   - Quality assurance
   - Standard process

### Medium Priority

6. **notifications-local** (from `notifications-local.md`)
   - Integration workflow
   - Platform-specific

### Low Priority

7. **Legacy skills** (archived or rarely used)
   - Convert as needed

---

## Common Conversion Patterns

### Pattern 1: Checklist → Skill

**Original** (checklist format):
```markdown
## DDL rules
- Use `siso-internal-supabase.apply_migration`
- Name migrations in `snake_case`

## RLS checklist
- Confirm policies enforce user isolation
- Validate reads and writes
```

**Converted** (structured format):
```yaml
---
name: supabase-ddl
description: Supabase DDL and RLS operations
tags: [supabase, database, ddl, rls]
---

# Supabase DDL Operations

## Core Commands

### Execute DDL Migration
```bash
siso-internal-supabase.apply_migration <migration_file>
```

**Rules**:
- Name migrations in `snake_case`
- Use transaction for safety
- Test in staging first

### Check RLS Policies
```bash
# Step 1: List policies
siso-internal-supabase.get_policies

# Step 2: Validate user isolation
# (Manual verification step)

# Step 3: Test read access
# (Manual test)

# Step 4: Test write access
# (Manual test)
```

## Workflows

### DDL + RLS Workflow
1. Write migration (snake_case)
2. Test in staging
3. Apply migration
4. Run security advisors
5. Validate RLS policies
6. Add regression tests

### RLS Validation Checklist
- [ ] Policies enforce user isolation
- [ ] Read access validated
- [ ] Write access validated
- [ ] Regression tests added
```

### Pattern 2: MCP-Based → CLI-Based

**Original** (MCP server):
```markdown
## MCP Server
Uses: `siso-internal-supabase` MCP server with `execute_sql` tool.

## Task Data Structure
**Table**: `public.tasks`
**Columns**: id, title, description, status, priority...
```

**Converted** (CLI-based):
```yaml
---
name: siso-tasks
description: Query SISO Internal tasks via Supabase CLI
tags: [tasks, supabase, siso, cli]
---

# SISO Tasks

## Overview
Query and manage tasks from SISO Internal Supabase database.

## Core Commands

### List Pending Tasks
```bash
supabase db execute --query "SELECT id, title, priority, due_date FROM tasks WHERE status = 'pending' ORDER BY priority LIMIT 50;"
```

### Show Urgent Tasks
```bash
supabase db execute --query "SELECT id, title, description, status, due_date FROM tasks WHERE priority = 'urgent' AND status NOT IN ('done', 'completed') ORDER BY due_date;"
```

### Task Statistics
```bash
supabase db execute --query "SELECT COUNT(*) as total, COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending, COUNT(CASE WHEN priority = 'urgent' THEN 1 END) as urgent FROM tasks;"
```

## Workflows
...
```

### Pattern 3: Simple Instructions → Full Skill

**Original** (minimal):
```markdown
# Repo Codebase Navigation

Navigate and understand codebase structure.
```

**Converted** (comprehensive):
```yaml
---
name: repo-codebase-navigation
description: Navigate and understand codebase structure efficiently
tags: [navigation, codebase, exploration, documentation]
---

# Codebase Navigation

## Purpose
Quickly understand and navigate the codebase structure, find relevant files, and understand relationships.

## Core Commands

### Find Files by Pattern
```bash
find . -name "*.ts" -path "*/components/*"
```

### Search Code Content
```bash
rg "function_name" --type ts
```

### Show Directory Structure
```bash
tree -L 2 -I "node_modules|target|dist"
```

## Workflows

### Workflow 1: Understand New Feature
1. Find feature entry point
2. Trace dependencies
3. Identify related tests
4. Document architecture

### Workflow 2: Locate Bug
1. Search error message
2. Find source file
3. Check related files
4. Identify test coverage
```

---

## Advanced: Multi-Project Skills

### Supabase Multi-Project Skills

**Challenge**: Multiple Supabase projects with different credentials

**Solution**: Environment-specific skills

**Structure**:
```
~/.claude/skills/
├── supabase-project1/
│   └── SKILL.md
├── supabase-project2/
│   └── SKILL.md
└── supabase-common/
    ├── SKILL.md
    └── scripts/
        └── supabase-wrapper.sh
```

**Skill Template**:
```yaml
---
name: supabase-project1
description: Supabase operations for Project1 (production)
tags: [supabase, project1, production]
project_id: proj1_***
env_file: ~/.supabase/project1.env
---

# Supabase Project1

## Environment Setup
```bash
source ~/.supabase/project1.env
# Or:
export SUPABASE_ACCESS_TOKEN=spb_***
export SUPABASE_PROJECT_ID=proj1_***
```

## Commands
### Database Push
```bash
supabase db push --project-id proj1_***
```

### Functions Deploy
```bash
supabase functions deploy --project-id proj1_***
```
```

---

## Testing Converted Skills

### Test Plan

1. **Discovery Test**
   - Verify skill appears in agent's skill list
   - Check metadata is parsed correctly

2. **Content Test**
   - Verify all sections present
   - Check examples are accurate
   - Validate commands work

3. **Integration Test**
   - Use skill with real agent
   - Test common workflows
   - Verify output format

4. **Performance Test**
   - Check token usage
   - Verify on-demand loading
   - Test with multiple skills

### Test Script

```bash
#!/bin/bash
# Test converted skill

SKILL_NAME=$1

echo "Testing skill: $SKILL_NAME"

# Test 1: Discovery
echo "Test 1: Discovery"
claude-code "List all available skills" | grep -q "$SKILL_NAME"
if [ $? -eq 0 ]; then
    echo "✓ Skill discovered"
else
    echo "✗ Skill not discovered"
fi

# Test 2: Content
echo "Test 2: Content"
cat ~/.claude/skills/$SKILL_NAME/SKILL.md | grep -q "## Purpose"
if [ $? -eq 0 ]; then
    echo "✓ Purpose section present"
else
    echo "✗ Purpose section missing"
fi

# Test 3: Integration
echo "Test 3: Integration"
claude-code "Use the $SKILL_NAME skill to..." < /dev/null
if [ $? -eq 0 ]; then
    echo "✓ Skill integrates successfully"
else
    echo "✗ Skill integration failed"
fi
```

---

## Rollback Plan

If conversion fails:

1. **Keep Originals**
   - Don't delete original skill files
   - Maintain parallel structure during migration

2. **Document Issues**
   - Track conversion problems
   - Note missing features
   - Identify workarounds

3. **Iterative Improvement**
   - Fix issues in converted version
   - Re-test after fixes
   - Archive original only when confident

---

## Post-Migration

### Maintenance

1. **Update Skills**
   - Keep SKILL.md files current
   - Update examples as workflows change
   - Version track major updates

2. **Deprecation**
   - Archive unused skills
   - Document deprecation reasons
   - Migrate users to new skills

3. **Documentation**
   - Maintain skills registry
   - Track skill usage
   - Gather user feedback

---

## Summary

**Migration Steps**:
1. ✅ Inventory current skills
2. ✅ Create `~/.claude/skills/` directory
3. ✅ Convert each skill to SKILL.md format
4. ✅ Add supporting files (templates, examples, scripts)
5. ✅ Test with Claude Code
6. ✅ Verify integration and functionality

**Success Criteria**:
- All skills converted to Agent Skills standard
- Skills discoverable by Claude Code
- Skills work with other agent platforms
- Token efficiency improved
- Documentation comprehensive

**Estimated Time**:
- Simple skills: 15-30 minutes each
- Complex skills (MCP-based): 1-2 hours each
- Total migration: 1-2 weeks for all skills

---

**Document Version**: 1.0.0
**Last Updated**: 2026-01-28
**Related**: [BLACKBOX5-SKILLS-ANALYSIS.md](./BLACKBOX5-SKILLS-ANALYSIS.md)
