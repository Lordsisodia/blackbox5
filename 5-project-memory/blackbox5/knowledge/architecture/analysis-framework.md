# Architecture Analysis Framework

**Version:** 1.0.0
**Created:** 2026-02-04
**Purpose:** Systematic approach for AI agents to analyze codebase architecture

---

## Overview

This framework enables AI agents to:
1. Analyze any area of the codebase systematically
2. Identify improvement opportunities
3. Validate against first principles
4. Prioritize by impact and effort
5. Execute improvements iteratively

---

## The Analysis Loop

```
┌─────────────────────────────────────────────────────────────┐
│  1. SCAN     →  2. IDENTIFY  →  3. VALIDATE  →  4. SCORE   │
│      ↓                                                      │
│  5. PRIORITIZE  →  6. EXECUTE  →  7. FEEDBACK  →  [loop]   │
└─────────────────────────────────────────────────────────────┘
```

---

## Step 1: Scan

**Purpose:** Get complete picture of the area

**Actions:**
- List all files and directories
- Read key documents
- Identify patterns and conventions
- Note anomalies or inconsistencies

**Output:** Raw inventory of the area

---

## Step 2: Identify

**Purpose:** Find improvement opportunities

**Questions to Ask:**
- Are there duplicate files or content?
- Are naming conventions consistent?
- Is the hierarchy clear (Project → Plan → Task)?
- Is documentation minimal and necessary?
- Are there single sources of truth?
- Are cross-references maintained?
- Is anything obsolete or outdated?

**Target:** 10 specific improvements per area

---

## Step 3: Validate

**Purpose:** Check against first principles

**Principles:**
1. **Single Source of Truth** - One canonical location per topic
2. **Convention over Configuration** - Standard naming and locations
3. **Minimal Viable Documentation** - Delete what isn't needed
4. **Hierarchy of Information** - Clear Project → Plan → Task structure

**Process:**
For each identified improvement:
- Check against each principle
- Score 1-5 for each principle
- Document rationale

---

## Step 4: Score

**Purpose:** Quantify improvement value

**Criteria:**

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Impact | 30% | How much does this improve daily work? |
| Effort | 20% | How easy is this to implement? |
| Prevention | 25% | Does this prevent future issues? |
| Principles | 25% | How well does it align with first principles? |

**Scoring:** 1-5 scale for each criterion

**Formula:**
```
Weighted Score =
  (Impact × 0.30) +
  (Effort × 0.20) +
  (Prevention × 0.25) +
  (Principles × 0.25)
```

---

## Step 5: Prioritize

**Purpose:** Select what to work on

**Process:**
1. Sort improvements by weighted score
2. Select top 2-3 improvements
3. Verify no dependencies between them
4. Confirm they fit in one session

**Selection Criteria:**
- Score > 3.5 preferred
- Can be completed in 45-60 minutes
- No external dependencies
- Clear acceptance criteria

---

## Step 6: Execute

**Purpose:** Implement improvements

**For Each Selected Improvement:**
1. Create detailed execution plan
2. Make changes
3. Validate against acceptance criteria
4. Update cross-references
5. Document in run files

**Output:**
- THOUGHTS.md - Reasoning
- DECISIONS.md - Key decisions
- RESULTS.md - Outcomes
- LEARNINGS.md - Insights

---

## Step 7: Feedback

**Purpose:** Learn and improve the process

**Questions:**
- What worked well?
- What was harder than expected?
- What would you do differently?
- How can the framework improve?

**Output:**
- Update ASSUMPTIONS.md
- Update ARCHITECTURE.md
- Refine framework if needed

---

## Area-Specific Checklists

### Root Directory Checklist

- [ ] File count appropriate (< 10 .md files?)
- [ ] Naming consistent (all lowercase?)
- [ ] No duplicate structure docs
- [ ] State files have clear purpose
- [ ] README is comprehensive
- [ ] Cross-references work
- [ ] No obsolete files
- [ ] Hierarchy clear

### Knowledge Base Checklist

- [ ] Categories well-defined
- [ ] Subdirectories logical
- [ ] No duplicate content
- [ ] Stale docs identified
- [ ] Cross-references maintained
- [ ] Naming consistent
- [ ] Easy to navigate
- [ ] Coverage complete

### Tasks Directory Checklist

- [ ] Naming consistent (task.md not TASK.md)
- [ ] Active/completed separation clear
- [ ] No duplicate tasks
- [ ] Cross-references maintained
- [ ] Templates up to date
- [ ] Hierarchy respected
- [ ] Status accurate

---

## Output Template

### Improvement Documentation

```markdown
## Improvement #[N]: [Title]

**Area:** [root/knowledge/tasks/etc]
**Current State:** [what exists]
**Proposed Change:** [what to do]
**Rationale:** [why this helps]

### First Principles Validation

| Principle | Score | Notes |
|-----------|-------|-------|
| Single Source | 1-5 | |
| Convention | 1-5 | |
| Minimal | 1-5 | |
| Hierarchy | 1-5 | |

### Impact Assessment

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Impact | 1-5 | 30% | |
| Effort | 1-5 | 20% | |
| Prevention | 1-5 | 25% | |
| Principles | 1-5 | 25% | |
| **TOTAL** | | | **[score]** |

### Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
```

---

## Success Metrics

**Framework is working when:**
- 10 improvements identified per area
- Improvements scored consistently
- Top improvements selected reliably
- Execution completes in timebox
- Feedback captured each loop
- Architecture measurably improves

---

## Usage Example

```
User: "Analyze the root directory"

AI:
1. Scan → List all root files
2. Identify → Find 10 improvements
3. Validate → Score against principles
4. Score → Calculate weighted scores
5. Prioritize → Select top 3
6. Execute → Implement improvements
7. Feedback → Document learnings
```

---

*Framework Version: 1.0*
*Last Updated: 2026-02-04*
