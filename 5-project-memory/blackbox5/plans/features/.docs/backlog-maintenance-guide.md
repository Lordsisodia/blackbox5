# Feature Backlog Maintenance Guide

**Version:** 1.0.0
**Last Updated:** 2026-02-01
**Purpose:** Guide for maintaining the Feature Backlog to ensure sustainable feature delivery

---

## Table of Contents

1. [Purpose](#purpose)
2. [Backlog Overview](#backlog-overview)
3. [How to Add Features](#how-to-add-features)
4. [How to Prioritize Features](#how-to-prioritize-features)
5. [How to Maintain the Backlog](#how-to-maintain-the-backlog)
6. [Feature Lifecycle](#feature-lifecycle)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

---

## Purpose

The Feature Backlog is the single source of truth for all planned features in the RALF system. It serves as:

- **Task Pipeline:** Source of feature tasks for the Planner to create
- **Visibility Document:** Shows what features are planned, active, and completed
- **Prioritization Tool:** Ensures high-value features are executed first
- **Strategic Record:** Tracks the strategic shift from "fix problems" to "create value"

**Who should use this guide:**
- Planner agents (create tasks from backlog)
- Executor agents (reference during feature implementation)
- System operators (review and adjust backlog)

---

## Backlog Overview

### File Structure

```
plans/features/
├── BACKLOG.md                          # Main backlog document (THIS FILE)
├── .docs/
│   └── backlog-maintenance-guide.md    # This guide
├── FEATURE-001-multi-agent-coordination.md
├── FEATURE-002-advanced-skills-library.md
└── FEATURE-XXX-[feature-name].md       # Individual feature specs
```

### Backlog Sections

**BACKLOG.md contains:**
1. **Backlog Summary** - Quick stats (planned, active, completed counts)
2. **Planned Features** - All features with status=planned, sorted by priority
3. **Active Features** - Features currently being implemented
4. **Completed Features** - Features successfully delivered
5. **Feature Acceptance Criteria** - Standard completion checklist
6. **Feature Prioritization Matrix** - Priority scoring formula and sorted list
7. **Metrics** - Feature delivery performance tracking
8. **Next Actions** - Recommended immediate actions
9. **Change Log** - Version history

---

## How to Add Features

### Step 1: Identify Feature Opportunity

**Sources of feature ideas:**
- **System Gaps:** What is missing? (UI, integrations, capabilities)
- **User Pain Points:** What frustrates operators? (manual tasks, lack of visibility)
- **Strategic Goals:** What moves RALF forward? (scaling, automation, quality)
- **External Inspiration:** What do other systems have? (GitHub Actions, n8n, Make)

**Before adding, ask:**
1. Does this solve a real problem?
2. Who benefits and how?
3. Is this feasible (1-4 hours)?
4. Does this align with RALF's autonomous nature?

### Step 2: Document the Feature

**Create a brief feature summary for BACKLOG.md:**

```markdown
### F-XXX: [Feature Name]

**Status:** planned
**Priority:** [HIGH/MEDIUM/LOW] (Score: X.X)
**Estimated:** XXX minutes (~X hours)
**Value Score:** X/10
**Effort:** X hours
**Added:** YYYY-MM-DD

**User Value:**
- **Who:** [Target user or system component]
- **Problem:** [Clear problem statement]
- **Value:** [Measurable benefit]

**MVP Scope:**
- [Core capability 1]
- [Core capability 2]
- [Core capability 3]

**Success Criteria:**
- [Criterion 1 - Specific, testable]
- [Criterion 2 - Specific, testable]
- [Criterion 3 - Specific, testable]

**Dependencies:** [None or list]
**Category:** [UI/Integration/Agent Capabilities/System Ops/Dev Experience]
**File:** `plans/features/FEATURE-XXX-[slug].md` (to be created)

**Priority Rationale:** [Why this priority score]
```

### Step 3: Calculate Priority Score

**Use the value/effort formula:**

```
Score = (Value × 10) / Effort (hours)

Value: 1-10 (10 = highest impact)
Effort: In hours (1 = 1 hour)

Priority Levels:
- HIGH: Score ≥ 5 (high value, low effort)
- MEDIUM: Score 2-5 (medium value/effort)
- LOW: Score < 2 (low value, high effort)
```

**Example:**
- Feature: Automated Documentation Generator
- Value: 9/10 (saves time, improves consistency)
- Effort: 1.5 hours (quick win)
- Score: (9 × 10) / 1.5 = **60.0 / 1.5 = 10.0** (HIGH priority)

### Step 4: Add to Backlog (Sorted)

1. Add feature to BACKLOG.md **Planned Features** section
2. **Sort by priority score** (HIGH → MEDIUM → LOW)
3. Update **Backlog Summary** (increment planned count)
4. Add entry to **Change Log**
5. Update **Metrics** (if backlog count changes)

---

## How to Prioritize Features

### Priority Scoring Guidelines

| Score Range | Priority | Description | Example |
|-------------|----------|-------------|---------|
| **Score ≥ 5** | **HIGH** | Quick wins, high value, low effort | Auto docs (10.0), User prefs (8.0) |
| **Score 2-5** | **MEDIUM** | Medium value/effort, strategic | CI/CD (6.0), Testing (3.6) |
| **Score < 2** | **LOW** | Low value, high effort, backlog | Performance dash (2.3 - obsolete) |

### Value Scoring Guidelines

| Value Score | Description | Criteria |
|-------------|-------------|----------|
| **9-10** | Critical | Solves major pain point, enables strategic capability |
| **7-8** | High | Significant improvement, high user value |
| **5-6** | Medium | Useful enhancement, clear benefit |
| **3-4** | Low | Nice-to-have, marginal improvement |
| **1-2** | Very Low | Minimal impact, questionable value |

### Effort Estimation Guidelines

| Effort | Duration | Complexity | Examples |
|--------|----------|------------|----------|
| **1-1.5 hours** | Quick win | Low | Documentation, config files |
| **1.5-2.5 hours** | Medium | Medium | CI/CD integration, testing framework |
| **2.5-4 hours** | Significant | High | GitHub integration, multi-agent coordination |
| **4+ hours** | Large | Very High | **Break down into smaller features** |

### Balancing the Backlog

**Ideal backlog composition:**
- **30% HIGH priority** (quick wins, immediate value)
- **50% MEDIUM priority** (strategic capabilities)
- **20% LOW priority** (future considerations, backlog)

**Red flags:**
- ⚠️ All features are LOW priority → backlog not valuable enough
- ⚠️ All features require 4+ hours → features too large, break them down
- ⚠️ No features in a category (e.g., no UI features) → gap in roadmap

---

## How to Maintain the Backlog

### Regular Reviews

**Frequency:** Every 5 Planner loops (~2-3 hours of executor work)

**Review Checklist:**
1. **Update Status:**
   - Move completed features from "Active" to "Completed"
   - Move started features from "Planned" to "Active"
   - Remove obsolete features (mark in change log)

2. **Re-prioritize:**
   - Re-calculate priority scores if context changed
   - Re-sort if scores changed
   - Mark if feature is no longer relevant

3. **Add New Features:**
   - If backlog < 5 features, add 2-3 new ones
   - If backlog > 15 features, remove/merge lowest priority

4. **Update Metrics:**
   - Increment "Features completed" if any completed
   - Update "Average cycle time" if data available
   - Update "Success rate" if any failed

### When to Remove Features

**Remove features that are:**
- **Obsolete:** Already implemented by another feature (e.g., F-003 Performance Dashboard → TASK-1769916005)
- **No Longer Relevant:** Strategic direction changed, problem solved
- **Too Low Value:** Score < 2 after 3 review cycles, no interest

**Removal process:**
1. Add note to feature: "**REMOVED:** [Reason], Date: YYYY-MM-DD"
2. Move to "Completed Features" with status=removed
3. Add entry to Change Log
4. Re-sort backlog

### When to Update Features

**Update feature details if:**
- **Scope Changed:** MVP expanded or reduced
- **Dependencies Resolved:** Blocking feature completed
- **Estimation Updated:** Effort estimate was wrong (track accuracy)

**Update process:**
1. Edit feature in BACKLOG.md
2. Re-calculate priority score if value/effort changed
3. Re-sort if score changed significantly
4. Add note to Change Log

---

## Feature Lifecycle

### Stage 1: Planned (Backlog)

**Location:** BACKLOG.md → Planned Features
**Status:** `status: planned`
**Actions:**
- Feature documented with value/effort assessment
- Prioritized by score
- Waiting for Planner to create task

### Stage 2: Task Created

**Location:** `.autonomous/tasks/active/TASK-XXX-feature-YYY.md`
**Status:** Feature remains `status: planned` in backlog
**Actions:**
- Planner creates task from feature spec
- Task appears in active/ directory
- Backlog note: "Task: TASK-XXX created"

### Stage 3: Active (Implementation)

**Location:** BACKLOG.md → Active Features
**Status:** `status: active`
**Actions:**
- Feature task claimed by executor
- Move feature from "Planned" to "Active"
- Track progress in feature spec

### Stage 4: Completed

**Location:** BACKLOG.md → Completed Features
**Status:** `status: completed`
**Actions:**
- All success criteria met
- Move feature from "Active" to "Completed"
- Update metrics (completion count, cycle time)
- Document learnings in feature spec

### Stage 5: Removed (Optional)

**Location:** BACKLOG.md → Completed Features
**Status:** `status: removed`
**Actions:**
- Feature obsolete or no longer relevant
- Mark as removed with reason
- Add to Change Log

---

## Best Practices

### 1. Keep Features Small

**Target:** 1-4 hours per feature
**Why:** Small features complete faster, provide value sooner, easier to estimate
**How:** Break down large features into smaller, testable chunks

**Example breakdown:**
- **Too large:** "GitHub Integration Suite" (4 hours)
- **Better:** "GitHub PR Auto-creation" (1.5 hours) + "GitHub Issue Sync" (1.5 hours) + "GitHub Release Notes" (1 hour)

### 2. Focus on User Value

**Question:** "Who benefits and how?"
**Answer format:** "[Who] can [do what] which [benefits]"

**Good examples:**
- "RALF operators can configure thresholds which enables personalized workflows"
- "RALF agents can auto-create PRs which speeds up development"

**Bad examples:**
- "Add GitHub integration" (no value stated)
- "Improve system" (too vague)

### 3. Be Specific About Success

**Good success criteria:**
- ✅ "Documentation auto-generated on task completion"
- ✅ "Config file created and parsed"
- ✅ "PRs created automatically on feature completion"

**Bad success criteria:**
- ❌ "Documentation improved" (how measured?)
- ❌ "System works better" (too vague)
- ❌ "Integration complete" (what does that mean?)

### 4. Update Metrics

**Track these metrics:**
- Features completed (last 30 days)
- Average cycle time (from active → completed)
- Success rate (completed / started)
- Planned features in backlog (target: 5-10)

**Why:** Data-driven decisions about feature delivery health

### 5. Review Regularly

**Every 5 planner loops:**
- Review backlog status
- Add new features if low
- Remove obsolete features
- Re-prioritize if context changed

**Why:** Backlog stays fresh, relevant, and actionable

---

## Troubleshooting

### Problem: Backlog Has Too Many Features (>15)

**Symptoms:**
- Backlog overwhelming, hard to prioritize
- Many low-priority features never get executed

**Solutions:**
1. Remove features with Score < 2
2. Merge related features
3. Move lowest priority to "Future Considerations" (external document)

### Problem: No Features in Backlog (<5)

**Symptoms:**
- Planner has no features to create tasks from
- Executor runs out of work

**Solutions:**
1. **Immediate:** Add 3-5 quick wins (1-2 hour features)
2. **Short-term:** Brainstorm feature ideas from pain points
3. **Long-term:** Establish continuous feature ideation process

### Problem: All Features Are High Priority

**Symptoms:**
- Priority score inflation (all features score ≥ 5)
- Can't distinguish what to do first

**Solutions:**
1. Re-calibrate value scores (should be bell curve, not all 9s)
2. Use tie-breakers: dependencies, category balance, strategic fit
3. Consider if effort estimates are too low

### Problem: Features Never Complete

**Symptoms:**
- Features stay "Active" for weeks
- Cycle time > 3 hours consistently

**Solutions:**
1. Break features into smaller chunks
2. Check if acceptance criteria too strict
3. Review if blockers present (dependencies, missing skills)
4. Consider if feature too complex (scale back MVP)

### Problem: Obsolete Features Remain

**Symptoms:**
- Feature backlog includes features already implemented
- Confusion about what's done vs. planned

**Solutions:**
1. Check each feature against current system state
2. Mark obsolete features as "REMOVED: [reason]"
3. Move to completed features with status=removed
4. Update change log

---

## Related Documents

- `BACKLOG.md` - Main feature backlog
- `.templates/tasks/feature-specification.md.template` - Feature task template
- `operations/.docs/feature-delivery-guide.md` - Feature delivery process
- `operations/metrics-dashboard.yaml` - System metrics

---

## Change Log

| Date | Change | Version |
|------|--------|---------|
| 2026-02-01 | Initial guide created for feature backlog maintenance | 1.0.0 |
