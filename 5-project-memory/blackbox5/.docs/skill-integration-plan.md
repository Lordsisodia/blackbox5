# Skill Integration Plan

**Version:** 1.0
**Created:** 2026-02-09
**Status:** Draft
**Task:** TASK-PROC-006

---

## Executive Summary

This document outlines the plan for integrating the skill system into the task execution workflow. Currently, the skill registry exists with 23 defined skills across 5 categories, but **skill invocation rate is 0%** despite 100% consideration rate. This plan addresses the gaps between skill definition and practical usage.

### Current State
- **Total Skills:** 23 (11 agent, 3 protocol, 3 utility, 4 core, 3 infrastructure)
- **Skill Consideration Rate:** 100% (Phase 1.5 compliance achieved)
- **Skill Invocation Rate:** 0% (threshold too high, no auto-trigger enforcement)
- **Average Effectiveness:** N/A (no invocation data)

### Target State
- **Skill Invocation Rate:** 40%+ (within 30 days)
- **Average Task Quality Improvement:** 20%+
- **Time Savings:** 15+ minutes per skill-invoked task

---

## 1. Problem Analysis

### 1.1 Why Skills Aren't Being Invoked

Based on analysis of the skill-registry.yaml and task outcomes:

| Issue | Evidence | Impact |
|-------|----------|--------|
| **Threshold Mismatch** | Confidence threshold lowered from 80% to 70%, but still no invocations | Skills identified but not triggered |
| **No Enforcement** | Auto-trigger rules exist but aren't mandatory | Agents skip skill invocation |
| **Missing Integration Points** | Skills checked in Phase 1.5 but not wired to execution | Gap between check and use |
| **No ROI Visibility** | All metrics null - no feedback loop | No incentive to use skills |
| **Low Confidence Scores** | All skills marked "confidence: low" | Self-fulfilling prophecy |

### 1.2 Task Outcome Analysis

From 4 tracked tasks post-Phase 1.5 implementation:

```yaml
TASK-1769909000: No skill invoked (documentation task - correct)
TASK-1769909001: bmad-analyst applicable at 70%, not invoked (should have been)
TASK-1769892006: No applicable skill (correct)
TASK-1769910000: bmad-analyst applicable but below threshold (threshold since lowered)
```

**Key Finding:** Skills are being correctly identified but not invoked due to lack of enforcement mechanism.

---

## 2. Integration Points Design

### 2.1 When Should Skills Be Auto-Suggested?

#### Current: Manual Check (Phase 1.5)
```yaml
Phase 1: Task Selection
Phase 1.5: Skill Check (MANUAL - read registry, calculate confidence)
Phase 2: Execution
```

#### Proposed: Auto-Suggestion with Override
```yaml
Phase 1: Task Selection
Phase 1.5: Auto-Skill Detection
  - Parse task description for trigger keywords
  - Calculate confidence using registry formula
  - Suggest top 1-3 skills if confidence >= 70%
  - Require explicit override to skip
Phase 2: Execution with Skill Context
```

### 2.2 Integration Points Map

```
┌─────────────────────────────────────────────────────────────────┐
│                    TASK EXECUTION WORKFLOW                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │ Task Start   │───▶│ Skill Check  │───▶│ Skill Load   │       │
│  │              │    │ (Auto)       │    │              │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │ Read task.md │    │ Match        │    │ Apply Skill  │       │
│  │              │    │ Triggers     │    │ Context      │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│                               │                   │               │
│                               ▼                   ▼               │
│                        ┌──────────────┐    ┌──────────────┐       │
│                        │ Calculate    │    │ Execute with │       │
│                        │ Confidence   │    │ Skill Guide  │       │
│                        └──────────────┘    └──────────────┘       │
│                               │                                   │
│                               ▼                                   │
│                        ┌──────────────┐                          │
│                        │ Suggest/     │                          │
│                        │ Require Skill│                          │
│                        └──────────────┘                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 Auto-Trigger Enhancement

Current 10 auto-trigger rules (ATR-001 to ATR-010) need enforcement:

| Rule | Trigger | Current | Proposed |
|------|---------|---------|----------|
| ATR-001 | implement + domain keyword | MUST check | MUST invoke if confidence >= 70% |
| ATR-002 | analyze/research | MUST check | MUST invoke bmad-analyst |
| ATR-003 | architecture/design | MUST check | MUST invoke bmad-architect |
| ATR-004 | "Should we"/"How should we" | MUST check | MUST invoke superintelligence-protocol |
| ATR-005 | PRD/requirements | MUST check | MUST invoke bmad-pm |
| ATR-006 | test/QA/quality | MUST check | MUST invoke bmad-qa |
| ATR-007 | multiple files/systems | MUST check | MUST check all relevant |
| ATR-008 | git operations | MUST check | MUST invoke git-commit |
| ATR-009 | database operations | MUST check | MUST invoke supabase-operations |
| ATR-010 | improve/optimize | MUST check | MUST invoke continuous-improvement |

**Key Change:** "MUST check" becomes "MUST invoke" for clear-cut cases.

---

## 3. Implementation Plan

### Phase 1: Foundation (Week 1)

#### 3.1.1 Update Rule 004-phase-1-5-skill-check.md
**File:** `.claude/rules/004-phase-1-5-skill-check.md`

Changes:
- Change "MUST check" to "MUST invoke" for clear trigger matches
- Add override process with required documentation
- Add skill execution workflow

#### 3.1.2 Create Skill Execution Wrapper
**File:** `.claude/skills/skill-executor/SKILL.md`

Purpose: Standardize how skills are invoked and tracked

Content outline:
```markdown
# Skill Executor

## Invocation Process
1. Load skill from registry
2. Apply skill context to session
3. Execute task with skill guidance
4. Track outcome metrics

## Tracking
- Log invocation in skill-registry.yaml
- Update usage_history
- Capture outcome data
```

#### 3.1.3 Update CLAUDE.md Skill Section
**File:** `5-project-memory/blackbox5/.claude/CLAUDE.md`

Changes:
- Add mandatory skill invocation for clear triggers
- Add override documentation requirements
- Add skill outcome tracking requirements

### Phase 2: Automation (Week 2)

#### 3.2.1 Create Skill Auto-Detection Script
**File:** `bin/detect-skill.py`

Purpose: Automatically detect applicable skills from task description

Features:
- Parse task.md for keywords
- Match against skill-registry.yaml triggers
- Calculate confidence score
- Return recommended skill(s)

#### 3.2.2 Create Skill Invocation Hook
**File:** `.claude/hooks/pre-execution/skill-invocation.sh`

Purpose: Hook into execution phase to enforce skill usage

Logic:
```bash
# 1. Detect applicable skills
SKILLS=$(detect-skill.py --task-file=$TASK_FILE)

# 2. If clear match (confidence >= 70%), require invocation
if [ "$CONFIDENCE" -ge 70 ]; then
  echo "Skill $SKILL recommended with $CONFIDENCE% confidence"
  echo "Override required to proceed without skill"
fi
```

#### 3.2.3 Update Task Template
**File:** `.templates/task.md`

Add section:
```markdown
## Skill Usage
- **Applicable Skills:** [Detected skills or "None"]
- **Skill Invoked:** [Skill name or "None"]
- **Confidence:** [Percentage]
- **Override Reason:** [If applicable]
```

### Phase 3: Validation & ROI (Week 3)

#### 3.3.1 Create Skill Effectiveness Validator
**File:** `bin/validate-skill-effectiveness.py`

Purpose: Analyze skill usage and calculate effectiveness

Metrics to calculate:
- Success rate by skill
- Time efficiency vs baseline
- Trigger accuracy
- Quality score correlation

#### 3.3.2 Update Skill Registry with Real Data
**File:** `operations/skill-registry.yaml`

Populate from task outcomes:
- Update usage counts
- Calculate effectiveness scores
- Adjust confidence levels

#### 3.3.3 Create Skill ROI Dashboard
**File:** `.docs/skill-roi-dashboard.md`

Display:
- Time saved per skill
- Quality improvement per skill
- Cost-benefit ratio
- Skill recommendation accuracy

### Phase 4: Optimization (Week 4)

#### 3.4.1 Refine Trigger Keywords
Based on usage data, refine trigger keywords for better matching.

#### 3.4.2 Adjust Confidence Thresholds
Per-skill threshold adjustment based on effectiveness data.

#### 3.4.3 Create Skill Recommendation Engine
Suggest skills based on task history and patterns.

---

## 4. Success Metrics

### 4.1 Primary Metrics

| Metric | Current | Target (30d) | Target (90d) |
|--------|---------|--------------|--------------|
| Skill Invocation Rate | 0% | 40% | 60% |
| Phase 1.5 Compliance | 100% | 100% | 100% |
| Avg Task Quality | 4.0 | 4.2 | 4.5 |
| Time Saved/Task | 0 min | 10 min | 15 min |

### 4.2 Secondary Metrics

| Metric | Target |
|--------|--------|
| Skills with >5 Uses | 10 (was 0) |
| Skills with Effectiveness Score | 15 (was 0) |
| False Positive Rate | <10% |
| Override Rate | <20% |

### 4.3 Validation Method

Weekly skill report generation:
```bash
bin/generate-skill-report.py --period=weekly
```

Report includes:
- Invocation rate trend
- Effectiveness by skill
- ROI calculation
- Recommendations

---

## 5. Risk Mitigation

### 5.1 Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Over-reliance on skills** | Medium | Medium | Maintain override capability; track override reasons |
| **Wrong skill invoked** | Low | High | Confidence threshold; explicit override option |
| **Skill adds overhead** | Medium | Low | Time tracking; overhead vs value analysis |
| **Low adoption** | Medium | High | Mandatory for clear triggers; education |
| **Metrics gaming** | Low | Medium | Multi-factor scoring; quality validation |

### 5.2 Rollback Plan

If skill integration causes issues:

1. **Immediate:** Disable mandatory invocation, revert to suggestion-only
2. **Short-term:** Adjust confidence thresholds upward
3. **Long-term:** Revert rule changes, return to Phase 1.5 manual check

---

## 6. Task Breakdown

### TASK-PROC-006-1: Update Skill Check Rule
- **Scope:** Modify `.claude/rules/004-phase-1-5-skill-check.md`
- **Changes:** Mandatory invocation for clear triggers
- **Effort:** 30 minutes
- **Dependencies:** None

### TASK-PROC-006-2: Create Skill Executor
- **Scope:** Create `.claude/skills/skill-executor/SKILL.md`
- **Purpose:** Standardize skill invocation
- **Effort:** 60 minutes
- **Dependencies:** TASK-PROC-006-1

### TASK-PROC-006-3: Create Auto-Detection Script
- **Scope:** Create `bin/detect-skill.py`
- **Purpose:** Auto-detect skills from task description
- **Effort:** 90 minutes
- **Dependencies:** None

### TASK-PROC-006-4: Create Pre-Execution Hook
- **Scope:** Create `.claude/hooks/pre-execution/skill-invocation.sh`
- **Purpose:** Enforce skill invocation
- **Effort:** 60 minutes
- **Dependencies:** TASK-PROC-006-3

### TASK-PROC-006-5: Update Task Template
- **Scope:** Modify `.templates/task.md`
- **Changes:** Add skill usage section
- **Effort:** 15 minutes
- **Dependencies:** None

### TASK-PROC-006-6: Create Effectiveness Validator
- **Scope:** Create `bin/validate-skill-effectiveness.py`
- **Purpose:** Calculate skill metrics
- **Effort:** 90 minutes
- **Dependencies:** None

### TASK-PROC-006-7: Create ROI Dashboard
- **Scope:** Create `.docs/skill-roi-dashboard.md`
- **Purpose:** Display skill value
- **Effort:** 45 minutes
- **Dependencies:** TASK-PROC-006-6

---

## 7. Dependencies

### 7.1 Required
- skill-registry.yaml (exists)
- task execution workflow (exists)
- CLAUDE.md rule system (exists)

### 7.2 Nice to Have
- Automated skill report generation
- Integration with RALF workflow
- Skill marketplace for adding new skills

---

## 8. Appendix

### 8.1 Skill Registry Structure

Current structure supports:
- 23 skills across 5 categories
- Usage tracking
- ROI calculation
- Selection criteria
- Auto-trigger rules

### 8.2 Confidence Calculation Formula

```
confidence = (keyword_match * 0.40) +
             (type_alignment * 0.30) +
             (complexity_fit * 0.20) +
             (historical_success * 0.10)
```

Threshold: 70%

### 8.3 Quality Rating Scale

- 5: Excellent - Exceeded expectations
- 4: Good - Met all requirements
- 3: Acceptable - Met core requirements
- 2: Below Average - Partial completion
- 1: Poor - Failed requirements

---

## 9. Next Steps

1. **Immediate:** Review and approve this plan
2. **Day 1-2:** Implement TASK-PROC-006-1 (update rule)
3. **Day 3-4:** Implement TASK-PROC-006-3 (auto-detection)
4. **Day 5:** Implement TASK-PROC-006-4 (pre-execution hook)
5. **Week 2:** Monitor and adjust thresholds
6. **Week 3:** Implement validation and ROI tracking
7. **Week 4:** Optimize based on data

---

**Document Owner:** Process Improvement Team
**Review Cycle:** Weekly during implementation
**Approval Required:** Yes - before Phase 1 implementation
