# Thoughts - TASK-1769899001

## Task
Create Skill Selection Guidance Framework - Add skill selection guidance to ~/.claude/CLAUDE.md to help agents systematically identify and invoke relevant skills for tasks.

## Approach
1. Read the current CLAUDE.md to understand structure and find insertion point
2. Review available skills from 2-engine/.autonomous/skills/README.md
3. Reference operations/skill-usage.yaml and operations/skill-metrics.yaml for skill data
4. Create comprehensive "When to Use Skills" section with:
   - Skill selection process (check → match → apply)
   - Domain-to-skill mapping table
   - Confidence threshold (>80%)
   - Skill invocation patterns with examples
   - Documentation requirements

## Execution Log

### Step 1: Read CLAUDE.md
- Found the "Sub-Agent Rules" section ending at line 182
- Identified insertion point: after "USE DIRECT READS" subsection, before "Context Management"
- This location makes sense as skills are an alternative to direct reads/sub-agents

### Step 2: Review Available Skills
From 2-engine/.autonomous/skills/README.md:
- 10 BMAD agent skills (pm, architect, analyst, sm, ux, dev, qa, tea, quick-flow, planning)
- 3 Protocol skills (superintelligence-protocol, continuous-improvement, run-initialization)
- 3 Utility skills (web-search, codebase-navigation, supabase-operations)
- 4 Core skills (truth-seeking, git-commit, task-selection, state-management)
- 3 Infrastructure skills (ralf-cloud-control, github-codespaces-control, legacy-cloud-control)

### Step 3: Reference Skill Data
From operations/skill-usage.yaml:
- All skills have trigger notes documenting when to use them
- Categories: agent, protocol, utility, core, infrastructure

From operations/skill-metrics.yaml:
- Baseline minutes defined for each skill
- When to use / when to avoid recommendations
- Effectiveness tracking schema

### Step 4: Create Skill Selection Section
Inserted new section "When to Use Skills" with:
1. **Skill Selection Process**: 3-step workflow (check → match → apply)
2. **Domain-to-Skill Mapping**: Comprehensive table with domains, skills, triggers, and confidence thresholds
3. **Skill Invocation Patterns**: 3 patterns with examples (direct call, keyword detection, task type matching)
4. **Skill Usage Documentation**: Template for updating skill-metrics.yaml
5. **When NOT to Use Skills**: Clear exclusions (confidence <80%, simple tasks, no matching domain)

## Challenges & Resolution

**Challenge**: Determining appropriate confidence thresholds
**Resolution**: Used 80% as baseline (as specified in task), with 85-90% for specialized domains (architecture, UX, QA) where incorrect skill selection would be costly.

**Challenge**: Organizing 23 skills into actionable guidance
**Resolution**: Grouped by domain in mapping table, focused on most commonly used skills in examples, referenced full skill list in skill-usage.yaml.

**Challenge**: Making guidance actionable vs. comprehensive
**Resolution**: Provided specific trigger keywords and examples for each pattern, while keeping the section concise enough to be referenceable during task execution.
