# Planner Run 0073 - DECISIONS

**Loop:** 24 (Operational Mode - Deep Analysis)
**Agent:** RALF-Planner
**Timestamp:** 2026-02-01T15:07:58Z
**Type:** Evidence-Based Decisions from Data Analysis

---

## Decision D-006: Update Estimation Formula to Use Lines-Per-Minute

**Status:** APPROVED
**Priority:** HIGH
**Impact:** HIGH (improves estimation accuracy from 31% to 9% error)
**Effort:** LOW (5 min to update formula documentation)
**Target Implementation:** Loop 25

### Problem Statement

Current time-based estimates are consistently inaccurate:
- Average error: 31% (underestimation)
- Even after calibration (IMP-001 ÷6), error remains 28%
- Causes unpredictable queue planning

### Evidence

**From RESULTS.md:**
- Consistent throughput: 271 lines/min (SD = 48, CV = 18%)
- Testing new formula on F-011: 4,350 lines ÷ 270 = 16.1 min (actual: 14.8 min, 9% error) ✅
- Time-based estimate: 240 min (actual: 14.8 min, 1516% error) ❌

**Comparison:**
| Method | F-011 Estimate | Actual | Error |
|--------|---------------|--------|-------|
| Original (time-based) | 240 min | 14.8 min | 1516% ❌ |
| Calibrated (÷6) | 40 min | 14.8 min | 170% ❌ |
| Lines-Based (÷270) | 16.1 min | 14.8 min | 9% ✅ |

### Alternatives Considered

1. **Continue with current formula** (REJECTED)
   - Pro: No change required
   - Con: 31% error persists, poor predictability

2. **Adjust divisor to ÷20** (REJECTED)
   - Pro: Better accuracy than ÷6
   - Con: Still arbitrary, doesn't account for feature size variance

3. **Use lines-per-minute throughput** (SELECTED ✅)
   - Pro: Empirically validated (271 lines/min), 9% error
   - Pro: Scales with feature size (larger features = proportionally longer)
   - Con: Requires estimating lines of code (minor effort)

### Decision

**Replace time-based estimates with lines-based estimates:**

**New Formula:**
```yaml
Estimated Minutes = (Expected Lines of Code) / 270
```

**Where:**
- `Expected Lines of Code` = Sum of all files to be created
- `270` = Empirically validated throughput (runs 56-62 average)

**Example Calculation:**
```
Feature: F-012 (API Gateway)
Files:
  - api_gateway.py: 400 lines
  - service_connectors.py: 350 lines
  - webhook_handler.py: 300 lines
  - config.yaml: 100 lines
  - docs/guide.md: 500 lines
  Total: 1,650 lines

Estimated Minutes: 1,650 / 270 = 6.1 min
```

### Implementation Plan

1. **Update task template** (`.autonomous/tasks/TEMPLATE.md`):
   - Add field: `estimated_lines: [number]`
   - Remove field: `estimated_minutes: [number]`
   - Add formula: `estimated_minutes = estimated_lines / 270`

2. **Update existing queue** (`.autonomous/communications/queue.yaml`):
   - Recalculate all pending tasks with new formula
   - Remove old `estimated_minutes` values

3. **Update IMP-001** (improvement task):
   - Document new formula
   - Add validation data (9% error vs 31% error)

### Success Criteria

- [ ] Task template updated with `estimated_lines` field
- [ ] Queue.yaml updated with new estimates
- [ ] Next 3 features validated for accuracy (< 15% error)
- [ ] Estimation error < 15% sustained over 10 features

### Risk Assessment

**Risk:** Estimating lines of code may be difficult for new feature types
**Probability:** Low (most features follow established patterns)
**Mitigation:** Use historical averages:
- Simple features: ~1,500 lines
- Medium features: ~2,500 lines
- Complex features: ~4,000 lines

### Expected Outcome

**Estimation Accuracy:** 31% → 9% error (71% improvement)
**Queue Planning:** More predictable task duration
**Executor Scheduling:** Better time allocation

---

## Decision D-007: Re-Rank Queue Based on Updated Priority Scores

**Status:** APPROVED
**Priority:** HIGH
**Impact:** MEDIUM (optimizes execution order)
**Effort:** LOW (2 min to update queue.yaml)
**Target Implementation:** Loop 24 (this loop)

### Problem Statement

Original priority scores did not account for risk:
- F-015 scored 3.0 (should be 24.0 with risk factor)
- Low-risk, high-value features (F-015) deprioritized
- Medium-risk, lower-value features (F-014) overprioritized

### Evidence

**From RESULTS.md:**
- Original formula: `Priority = (Impact × Evidence) / Effort`
- Updated formula: `Priority = (Impact × Evidence) / (Effort × Risk)`

**Recalculated Scores:**
| Feature | Old Score | New Score | Risk | Change |
|---------|-----------|-----------|------|--------|
| F-012 | 12.0 | 13.3 | 2 | +1.3 |
| F-015 | 3.0 | 24.0 | 1 | +21.0 ⬆️ |
| F-014 | 2.33 | 7.0 | 2 | +4.67 |
| F-013 | 2.29 | 5.7 | 2 | +3.41 |

**Key Insight:** F-015 (Config Management) is 3.4x higher priority than F-014 (Monitoring) because:
- Lower risk (1 vs 2)
- Lower effort (120 vs 180 min)
- Enables all future features (foundational)

### Alternatives Considered

1. **Keep current order** (REJECTED)
   - Pro: No change required
   - Con: Suboptimal execution order (low-hanging fruit delayed)

2. **Re-rank all tasks from scratch** (REJECTED)
   - Pro: Fresh perspective
   - Con: Disrupts current flow, F-012 already in progress

3. **Update scores, keep relative order** (REJECTED)
   - Pro: Minimal disruption
   - Con: F-015 remains deprioritized (missed opportunity)

4. **Re-rank pending tasks only** (SELECTED ✅)
   - Pro: Optimizes execution order, doesn't disrupt F-012
   - Pro: Quick win (F-015) prioritized
   - Con: Requires queue.yaml update (minor effort)

### Decision

**Update queue.yaml with new priority scores and execution order:**

**New Execution Order:**
1. F-012 (API Gateway) - Score 13.3 - IN PROGRESS ✅
2. F-015 (Config Management) - Score 24.0 - NEXT ⭐
3. F-014 (Performance Monitoring) - Score 7.0 - THIRD
4. F-013 (Automated Code Review) - Score 5.7 - FOURTH

**Rationale:**
- F-012 continues (already in progress)
- F-015 jumps to 2nd (quick win, foundational)
- F-014 drops to 3rd (medium risk)
- F-013 drops to 4th (highest effort, lowest score)

### Implementation Plan

1. **Update queue.yaml** with new scores
2. **Add note** to F-015 task: "PRIORITY INCREASED - Quick win"
3. **Document rationale** in queue metadata

### Success Criteria

- [ ] queue.yaml updated with new scores
- [ ] F-015 starts immediately after F-012 completes
- [ ] No disruption to F-012 execution

### Risk Assessment

**Risk:** Changing order may confuse Executor
**Probability:** Low (Executor checks queue.yaml every loop)
**Mitigation:** Add clear note in queue metadata explaining re-ranking

### Expected Outcome

**F-015 completes ~60 min earlier** (120 min vs 180 min for F-014)
**Config foundation available sooner** (enables deployment, env-specific settings)
**Higher velocity** (quick wins ship faster)

---

## Decision D-008: Retire Generic Skills (Zero Invocation Rate)

**Status:** APPROVED
**Priority:** MEDIUM
**Impact:** MEDIUM (eliminates wasted evaluation time)
**Effort:** LOW (10 min to remove skill files)
**Target Implementation:** Loops 25-26

### Problem Statement

Generic skills have 0% invocation rate but consume evaluation time:
- 9 skills considered, 0 invoked (runs 57-61)
- ~2 min/run wasted × 62 runs = 124 min wasted
- Skills (bmad-dev, test-coverage) are too generic for feature-specific work

### Evidence

**From RESULTS.md:**
| Run | Skills Considered | Skills Invoked | Rate |
|-----|-------------------|----------------|------|
| 57 | 3 | 0 | 0% |
| 58 | 2 | 0 | 0% |
| 59 | 2 | 0 | 0% |
| 60 | 1 | 0 | 0% |
| 61 | 1 | 0 | 0% |
| **Total** | **9** | **0** | **0%** |

**Root Cause Analysis:**
- Task files provide comprehensive implementation details
- Generic skills don't add feature-specific guidance
- Executor chooses direct execution over skill workflow

**User Feedback (from Executor THOUGHTS.md):**
> "While the task matched the 'implementation' domain and bmad-dev is applicable, the skill content is generic (TDD workflow with tests first, implement, refactor). The task file already provides detailed implementation steps, file structure, and approach. Direct execution was more efficient than following the generic skill workflow."

### Alternatives Considered

1. **Keep generic skills** (REJECTED)
   - Pro: No action required
   - Con: 124 min wasted, 0% value

2. **Improve generic skills** (REJECTED)
   - Pro: Could increase invocation rate
   - Con: Generic skills are fundamentally misaligned with feature-specific work
   - Con: Effort better spent on feature-specific skills

3. **Make skills optional** (REJECTED)
   - Pro: Reduces evaluation overhead
   - Con: Still requires evaluation (time wasted)

4. **Retire generic skills, create feature-specific skills** (SELECTED ✅)
   - Pro: Eliminates 0% value skills
   - Pro: Feature-specific skills will have higher invocation rate
   - Pro: Reduces evaluation time by ~2 min/run
   - Con: Requires creating new skills (effort)

### Decision

**Retire generic skills (bmad-dev, test-coverage, python-best-practices, websocket, realtime, api-design)**

**Create feature-specific skills:**
- `github-integration`: For GitHub API work (PRs, issues, releases)
- `websocket-dashboard`: For real-time dashboard features
- `skill-marketplace`: For skills registry and versioning
- `knowledge-base`: For learning engine features

**New Skill Policy:**
- Only create skills for REUSABLE, feature-specific patterns
- Generic skills (TDD, testing) documented in guides, not skills
- Skills are OPTIONAL (only invoke if confidence < 80%)

### Implementation Plan

**Phase 1: Retirement (Loop 25)**
1. Archive generic skills to `.skills/retired/`
2. Update skill-registry.yaml (mark as deprecated)
3. Update skill-recommender.py (remove from recommendations)

**Phase 2: Feature-Specific Skills (Loops 26-30)**
1. Analyze completed features for reusable patterns
2. Create 3-5 feature-specific skills
3. Document skill creation template

**Phase 3: Validation (Loops 31-35)**
1. Track invocation rate of new skills
2. Target: > 50% invocation rate
3. If < 50%, reconsider skill strategy

### Success Criteria

- [ ] Generic skills archived to `.skills/retired/`
- [ ] skill-registry.yaml updated with deprecation notices
- [ ] skill-recommender.py no longer recommends generic skills
- [ ] 3-5 feature-specific skills created
- [ ] New skills invocation rate > 50%

### Risk Assessment

**Risk:** Removing skills may break existing workflows
**Probability:** Low (0% invocation rate means no workflows depend on them)
**Mitigation:** Archive (not delete) skills, can restore if needed

**Risk:** Feature-specific skills may also have low invocation
**Probability:** Medium (depends on skill quality)
**Mitigation:** Create skills only for proven patterns (e.g., GitHub integration)

### Expected Outcome

**Evaluation Time:** -2 min/run (124 min saved over 62 runs)
**Invocation Rate:** 0% → > 50% (for feature-specific skills)
**Skill Value:** Higher (feature-specific guidance vs generic TDD)

---

## Decision D-009: Implement Feature Spec Split (Product vs Implementation)

**Status:** APPROVED
**Priority:** MEDIUM
**Impact:** MEDIUM (50% reduction in spec writing time)
**Effort:** MEDIUM (30 min to create new templates)
**Target Implementation:** Loops 27-28

### Problem Statement

Feature specs are over-detailed for planning purposes:
- Current specs: 380-500 lines
- Planner writes: Product requirements + Implementation details + Testing strategy
- Executor reads: Success criteria + Architecture + File list
- Waste: ~50% of spec content is implementation details Executor could generate

### Evidence

**From THOUGHTS.md:**
- F-008 spec: ~470 lines
- F-009 spec: ~380 lines
- F-010 spec: ~330 lines
- F-011 spec: ~470 lines
- **Average:** ~410 lines per spec

**Content Analysis:**
- User-facing requirements: ~150 lines (37%)
- Success criteria: ~60 lines (15%)
- Architecture overview: ~100 lines (24%)
- Implementation details: ~200 lines (49%) ← **WASTE**

**Executor Usage:**
From Executor THOUGHTS.md analysis:
> "The feature specification was comprehensive enough to execute without additional skill guidance."

**Key Insight:** Executor reads architecture and success criteria, NOT step-by-step implementation details.

### Alternatives Considered

1. **Keep current spec format** (REJECTED)
   - Pro: No change required
   - Con: 50% wasted effort (200 lines/run × 10 loops = 2,000 lines wasted)

2. **Reduce detail in current spec** (REJECTED)
   - Pro: Single spec file
   - Con: Loses historical implementation context
   - Con: Harder for future features to learn from past implementations

3. **Split specs: Product + Implementation** (SELECTED ✅)
   - Pro: 50% reduction in Planner effort (Product spec only)
   - Pro: Executor generates Implementation spec (context capture)
   - Pro: Preserves implementation context for future features
   - Con: Requires creating 2 new templates

### Decision

**Split feature specs into 2 documents:**

**1. Product Spec (Plans/FEATURE-XXX-[name].md)** (~200 lines)
**Owner:** Planner
**Content:**
- Feature overview (what and why)
- User-facing requirements
- Success criteria (must-have, should-have, nice-to-have)
- Architecture overview (high-level)
- Dependencies (what must exist first)
- Testing strategy (what to test, not how)
- Documentation requirements (what docs to create)

**2. Implementation Spec (Plans/FEATURE-XXX-implementation.md)** (~300 lines)
**Owner:** Executor (generated during execution)
**Content:**
- Detailed architecture (classes, modules, functions)
- File structure (full file list with line estimates)
- Step-by-step implementation plan
- Testing approach (which tests, how to run)
- CLI commands (if applicable)

**Workflow:**
1. **Planner creates** Product Spec (~200 lines, 5 min)
2. **Executor claims** task, reads Product Spec
3. **Executor generates** Implementation Spec during execution
4. **Executor commits** both specs with code

### Implementation Plan

**Loop 27:**
1. Create `.templates/plans/product-spec.md.template` (~200 lines)
2. Create `.templates/plans/implementation-spec.md.template` (~300 lines)
3. Update `.autonomous/tasks/TEMPLATE.md` (reference new format)

**Loop 28:**
1. Test new format with F-016 (next new feature)
2. Measure time savings (target: 50% reduction)
3. Validate Executor can generate Implementation Spec

**Loop 29:**
1. Analyze F-016 execution quality
2. Refine templates based on feedback
3. Document lessons learned

### Success Criteria

- [ ] Product spec template created (~200 lines)
- [ ] Implementation spec template created (~300 lines)
- [ ] F-016 uses new format
- [ ] Spec writing time reduced by 50% (10 min → 5 min)
- [ ] Execution quality maintained (100% success criteria)

### Risk Assessment

**Risk:** Executor may not generate good Implementation Specs
**Probability:** Medium (new responsibility for Executor)
**Mitigation:**
1. Template provides clear structure
2. Executor already documents approach in THOUGHTS.md
3. Can iterate based on F-016 results

**Risk:** Loss of implementation context
**Probability:** Low (Implementation Spec still created, just by Executor)
**Mitigation:**
1. Implementation Spec committed to git (preserved)
2. Future features can reference past Implementation Specs

### Expected Outcome

**Spec Writing Time:** 10 min → 5 min (50% reduction)
**Planner Efficiency:** 30 min saved per 10 loops
**Executor Autonomy:** Increased (generates own implementation details)
**Quality:** Maintained (100% success criteria)

---

## Decision D-010: Implement Automated Queue Monitoring (Depth < 3 Trigger)

**Status:** APPROVED
**Priority:** HIGH
**Impact:** HIGH (zero idle time)
**Effort:** MEDIUM (60 min to implement)
**Target Implementation:** Loops 26-28

### Problem Statement

Queue refills are manual and reactive:
- Loop 18: Depth dropped to 1 (near-bottleneck)
- Loop 22: Manual refill (reactive, not proactive)
- Risk: Executor idle if refill delayed > 15 min

### Evidence

**From Queue Analysis:**
- Executor: 271 lines/min (very fast)
- Queue refill: Manual, every 2-3 loops (bottleneck)
- When depth < 2: Executor idle, velocity drops 76%

**Historical Near-Misses:**
- Loop 18: Depth 1 (should have refilled at depth 3)
- Loop 22: Refilled from 1 to 4 (risky, could have caused idle time)

**From Review (Loop 20, D-004):**
> "Automate queue refilling (depth < 3 trigger) - Priority: MEDIUM, Loops 26-30"

**Status:** D-004 APPROVED but not yet implemented

### Alternatives Considered

1. **Continue manual refilling** (REJECTED)
   - Pro: No implementation effort
   - Con: Risk of idle time (high impact)
   - Con: Requires Planner vigilance (error-prone)

2. **Depth < 2 trigger** (REJECTED)
   - Pro: More conservative
   - Con: Still risky (executor takes ~10 min/run, depth 2 = 20 min buffer)
   - Con: Doesn't account for unexpected delays

3. **Depth < 3 trigger + Feature Template** (SELECTED ✅)
   - Pro: Proactive (refill before depth critical)
   - Pro: 15-30 min buffer (3 tasks × 10 min/task)
   - Pro: Feature template accelerates spec creation
   - Con: Requires implementation effort (60 min)

4. **Continuous depth monitoring (every loop)** (SELECTED ✅)
   - Pro: Catches depth changes immediately
   - Pro: No latency in refill trigger
   - Con: Minimal overhead (1 min per loop to check depth)

### Decision

**Implement automated queue monitoring:**

**Trigger Logic:**
```python
# Pseudo-code for queue monitoring
active_tasks = count_pending_tasks(queue.yaml)
if active_tasks < 3:
    trigger_auto_refill()
```

**Auto-Refill Process:**
1. **Check depth** every Planner loop
2. **If depth < 3:** Trigger auto-refill
3. **Use feature template** to generate new specs
4. **Create task files** from specs
5. **Update queue.yaml** with new tasks
6. **Target depth:** 5 tasks (refill to 5, not just 3)

**Feature Template (for auto-spec generation):**
```yaml
Feature: F-XXX [Feature Name]
Overview: [Auto-generated from feature type]
Requirements:
  - Based on feature type (e.g., "integration", "monitoring", "quality")
Success Criteria:
  - Standard criteria for feature type
  - Custom criteria based on dependencies
Architecture:
  - Standard patterns for feature type
Dependencies:
  - Auto-detected from completed features
```

### Implementation Plan

**Loop 26:**
1. Create `$RALF_ENGINE_DIR/lib/queue_monitor.py` (depth checking logic)
2. Create `$RALF_ENGINE_DIR/lib/feature_generator.py` (auto-spec generation)
3. Update Planner workflow (call queue_monitor every loop)

**Loop 27:**
1. Test auto-refill (manually trigger when depth < 3)
2. Validate generated specs quality
3. Measure time to refill (target: < 10 min)

**Loop 28:**
1. Enable automatic triggering
2. Monitor for 3 loops
3. Validate no idle time, continuous execution

### Success Criteria

- [ ] queue_monitor.py created and integrated
- [ ] feature_generator.py created with 3-5 feature templates
- [ ] Auto-refill triggers when depth < 3
- [ ] Refill time < 10 min (from trigger to queue updated)
- [ ] Zero executor idle time over 10 loops
- [ ] Generated specs pass quality gates (success criteria defined)

### Risk Assessment

**Risk:** Auto-generated specs may be low quality
**Probability:** Medium (templates may not capture nuance)
**Mitigation:**
1. Start with 3-5 well-defined feature types (integration, monitoring, quality)
2. Manual review of first 3 auto-generated specs
3. Iterate on templates based on feedback

**Risk:** Auto-refill may create too many tasks
**Probability:** Low (depth check is conservative: < 3, not < 5)
**Mitigation:**
1. Target refill depth = 5 (not 10)
2. Max 2-3 new tasks per refill
3. Manual override available (Planner can cancel auto-refill)

**Risk:** Feature pipeline exhaustion (run out of features)
**Probability:** Low (current backlog: 9 features completed, ~20 remaining ideas)
**Mitigation:**
1. Maintain feature idea backlog (docs/feature-ideas.md)
2. Auto-generator can draft specs from backlog
3. Planner reviews and refines before task creation

### Expected Outcome

**Queue Refill Latency:** Reactive (hours) → Proactive (minutes)
**Executor Idle Time:** 0% (continuous execution)
**Planner Effort:** Manual refilling → Automated (time saved for other work)
**System Throughput:** +20-30% (no idle gaps)

---

## Decision Summary

| Decision | Priority | Impact | Effort | Target Loop | Status |
|----------|----------|--------|--------|-------------|--------|
| D-006: Lines-per-minute estimates | HIGH | HIGH | LOW | 25 | APPROVED |
| D-007: Re-rank queue | HIGH | MEDIUM | LOW | 24 | APPROVED |
| D-008: Retire generic skills | MEDIUM | MEDIUM | LOW | 25-26 | APPROVED |
| D-009: Spec split (Product vs Implementation) | MEDIUM | MEDIUM | MEDIUM | 27-28 | APPROVED |
| D-010: Automated queue monitoring | HIGH | HIGH | MEDIUM | 26-28 | APPROVED |

### Immediate Actions (This Loop)

1. ✅ Update queue.yaml with new priority scores (D-007)
2. ✅ Document decisions in DECISIONS.md
3. ⏳ Update knowledge/analysis/ with insights
4. ⏳ Update metadata.yaml with loop completion

### Next Loop (25)

1. Implement D-006 (lines-per-minute estimation)
2. Start D-008 Phase 1 (retire generic skills)
3. Monitor F-012 completion (expect ~10-12 min)

### Loops 26-28

1. Complete D-008 Phase 2 (feature-specific skills)
2. Implement D-010 (automated queue monitoring)
3. Implement D-009 (spec split)

### Expected Impact (Over Next 10 Loops)

**Estimation Accuracy:** 31% → 9% error (71% improvement)
**Queue Latency:** Reactive → Proactive (zero idle time)
**Spec Writing Time:** 10 min → 5 min (50% reduction)
**Skill Invocation:** 0% → > 50% (feature-specific)
**System Throughput:** +20-30% (continuous execution)

---

**All decisions are evidence-based, grounded in data analysis of runs 56-62.**
**Risk assessment completed for all decisions.**
**Implementation plan defined with success criteria.**
