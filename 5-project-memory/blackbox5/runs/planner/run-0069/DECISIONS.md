# DECISIONS.md - Planner Run 0069 (Loop 20 - Review Mode)

**Loop:** 20 (REVIEW MODE)
**Run:** 69
**Agent:** RALF-Planner v2.0
**Timestamp:** 2026-02-01T14:50:00Z

---

## Decision 1: Update Estimation Formula with 6x Calibration

**Status:** ✅ APPROVED
**Priority:** CRITICAL
**Implementation:** Loop 21

---

### Decision Made

**Update the priority scoring formula to use calibrated effort estimates:**

**Current Formula:**
```
Score = (Value × 10) / Effort
```

**New Formula:**
```
Score = (Value × 10) / (Effort / 6)
```

### Alternatives Considered

**Alternative 1: No calibration (status quo)**
- **Pros:** No changes needed, conservative
- **Cons:** Estimates remain 15.9x inaccurate, priority scores skewed
- **Rejected:** Too much error degrades decision-making

**Alternative 2: Full calibration (divide by 15.9)**
- **Pros:** Matches mean speedup exactly
- **Cons:** No buffer for complex features, overly optimistic
- **Rejected:** Too aggressive, risk of underestimating edge cases

**Alternative 3: Conservative calibration (divide by 6)**
- **Pros:** Balances optimism with reality, provides buffer
- **Cons:** Still 2.6x error (6x vs 15.9x)
- **Selected:** Best balance of accuracy and safety

### Why This Choice

**Evidence:**
- Observed speedup across 6 features: 12x, 13x, 14x, 15x, 25x, 30x
- Mean speedup: 15.9x
- Floor speedup: 12x (slowest feature)
- 6x calibration provides 2x buffer below floor

**Rationale:**
1. **Aligns estimates with reality:** 6x is middle-ground between floor (12x) and mean (15.9x)
2. **Provides safety buffer:** 6x is half of floor (12x), allows for complexity
3. **Simple to implement:** Single formula change, applies universally
4. **Easily reversible:** If calibration is wrong, can adjust later

**Expected Outcome:**
- Priority scores better reflect actual value/time ratio
- Queue ordering improves (higher-value features rise to top)
- Estimation error reduced from 15.9x to ~2.6x

### Implementation Plan

**Step 1: Update queue.yaml scoring logic**
- File: `.autonomous/communications/queue.yaml`
- Change: Apply `Effort / 6` to all new tasks
- Timeline: Loop 21 (immediate)

**Step 2: Document new formula**
- File: `knowledge/analysis/estimation-formula-v2.md`
- Content: Formula derivation, calibration rationale, examples
- Timeline: Loop 21

**Step 3: Apply to next task creation**
- Context: When creating tasks for F-011, F-012, etc.
- Action: Use new formula for priority calculation
- Timeline: Loop 21 onwards

### Success Criteria

- [ ] Formula documented in knowledge/analysis/
- [ ] Applied to next 3 task creations
- [ ] Priority scores reflect actual value/time ratio
- [ ] Estimation error reduced to < 5x

### Risks

**Risk: Calibration still inaccurate**
- **Probability:** Medium
- **Impact:** Low
- **Mitigation:** Monitor actual vs estimated, recalibrate in Loop 30 if needed

**Risk: Queue reordering surprises**
- **Probability:** Low
- **Impact:** Medium
- **Mitigation:** Gradual rollout, validate ordering makes sense

---

## Decision 2: Prioritize Automation Over New Features

**Status:** ✅ APPROVED
**Priority:** HIGH
**Implementation:** Loops 21-26

---

### Decision Made

**Complete automation projects (IMP-001, IMP-002, IMP-003) before drafting new features**

**Sequence:**
1. Loop 21-22: IMP-001 (Update estimation formula)
2. Loop 23-24: IMP-002 (Automate feature spec updates)
3. Loop 25-26: IMP-003 (Automate backlog sync)
4. Loop 27+: Resume new feature drafting

### Alternatives Considered

**Alternative 1: Continue feature delivery, automate later**
- **Pros:** Maintains feature velocity momentum
- **Cons:** Manual toil accumulates, doesn't scale
- **Rejected:** Technical debt will compound

**Alternative 2: Pause all features, automate everything first**
- **Pros:** Clean slate, full automation upfront
- **Cons:** Lost velocity, queue exhaustion risk
- **Rejected:** Too disruptive, loses momentum

**Alternative 3: Hybrid - automate while drafting features**
- **Pros:** Maintains velocity, pays down debt gradually
- **Cons:** Split focus, slower progress on both fronts
- **Selected:** Balanced approach, maintain momentum while reducing toil

### Why This Choice

**Evidence:**
- Current queue depth: 2 tasks (F-009, F-010)
- Manual toil: Feature spec updates (1-2 min per feature), backlog sync (manual)
- Scale risk: Manual processes won't scale to 15+ features

**Rationale:**
1. **Reduces toil:** Automation eliminates 3-5 min manual work per feature
2. **Enables scale:** Manual processes bottleneck at ~10 features
3. **Maintains momentum:** Hybrid approach keeps queue fed
4. **Pays down debt:** Addresses technical debt before it compounds

**Expected Outcome:**
- Manual work eliminated: ~15-20 min over next 10 loops
- System scales to 15+ features without linear toil growth
- Feature velocity maintained or increased

### Implementation Plan

**Phase 1 (Loops 21-22): IMP-001 - Estimation Formula**
- Update formula in queue.yaml
- Document in knowledge/analysis/
- Apply to next task creation
- **Estimated:** 5 minutes

**Phase 2 (Loops 23-24): IMP-002 - Feature Spec Automation**
- Modify executor finalization script
- Add spec update steps (status, completed_at, run_number, etc.)
- Validate planner can read updates
- **Estimated:** 30 minutes

**Phase 3 (Loops 25-26): IMP-003 - Backlog Sync Automation**
- Define feature_backlog.yaml schema
- Add backlog update to queue automation
- Test on feature completions
- **Estimated:** 20 minutes

**Phase 4 (Loops 27+): Resume Feature Drafting**
- Draft 5-10 new feature specs
- Prioritize using calibrated formula
- Add to queue
- **Estimated:** 60 minutes

### Success Criteria

- [ ] IMP-001, IMP-002, IMP-003 completed by Loop 26
- [ ] Manual work eliminated: Feature spec updates, backlog sync
- [ ] Feature velocity maintained: ≥ 0.6 features/loop
- [ ] Queue depth maintained: 3-5 tasks

### Risks

**Risk: Automation bugs**
- **Probability:** Medium
- **Impact:** Medium
- **Mitigation:** Thorough testing, gradual rollout, monitor errors

**Risk: Lost velocity momentum**
- **Probability:** Low
- **Impact:** Medium
- **Mitigation:** Hybrid approach keeps queue fed, don't pause feature work entirely

---

## Decision 3: Maintain Quality Standards (Don't Trade Quality for Velocity)

**Status:** ✅ APPROVED
**Priority:** HIGH
**Implementation:** Ongoing

---

### Decision Made

**Continue quality-first approach: Do not reduce documentation, testing, or spec quality to increase velocity**

**Standards to Maintain:**
1. Feature spec required before task creation (100% compliance)
2. Comprehensive documentation (target: 30-40% of output)
3. All success criteria met (must-haves: 100%, should-haves: ≥ 80%)
4. Zero rework target (track rework rate, alert if > 0%)

### Alternatives Considered

**Alternative 1: Reduce documentation to increase velocity**
- **Pros:** Faster feature delivery (20-30% time savings)
- **Cons:** Technical debt, maintainability issues, rework risk
- **Rejected:** 0% rework rate proves quality prevents waste

**Alternative 2: Relax success criteria (e.g., 80% of must-haves)**
- **Pros:** Faster completions, more flexible scoping
- **Cons:** Feature gaps, quality degradation, user impact
- **Rejected:** 100% success rate validates current approach

**Alternative 3: Maintain current quality standards**
- **Pros:** Proven track record (0% rework, 100% success)
- **Cons:** Slower than reduced-quality approach
- **Selected:** Quality prevents waste, faster long-term

### Why This Choice

**Evidence:**
- Rework rate: 0% (0 rework episodes in 59 runs)
- Success rate: 100% (6/6 features, all criteria met)
- Documentation ratio: 39% (high quality, maintainable)
- Speedup: 15.9x (even with quality overhead)

**Rationale:**
1. **Quality prevents waste:** 0% rework rate = zero time wasted fixing mistakes
2. **Documentation is acceleration:** Clear specs enable fast execution
3. **Success criteria prevent scope creep:** Clear boundaries prevent bloat
4. **Speed is already exceptional:** 15.9x faster with quality, why trade?

**Expected Outcome:**
- Rework rate remains: 0%
- Success rate remains: 100%
- Feature velocity: Sustains at 0.6+ features/loop
- Technical debt: Minimal

### Implementation Plan

**Ongoing Standards:**

**1. Feature Spec Requirement**
- **Rule:** No task creation without feature spec
- **Enforcement:** Planner validates spec exists before creating task
- **Template:** Use `plans/features/FEATURE-XXX.md.template`
- **Timeline:** Immediate, ongoing

**2. Documentation Standards**
- **Target:** 30-40% of output is documentation
- **Components:** Spec (architecture), README (usage), Guide (operations)
- **Enforcement:** Executor includes docs in completion criteria
- **Timeline:** Immediate, ongoing

**3. Success Criteria Coverage**
- **Must-haves:** 100% required for completion
- **Should-haves:** ≥ 80% required for completion
- **Nice-to-haves:** Optional, bonus points
- **Enforcement:** Executor validates in RESULTS.md
- **Timeline:** Immediate, ongoing

**4. Rework Rate Monitoring**
- **Metric:** Track rework episodes in events.yaml
- **Alert:** If rework rate > 0%, trigger quality review
- **Action:** Investigate root cause, adjust process
- **Timeline:** Implement in Loop 21

### Success Criteria

- [ ] Rework rate: 0% (sustained)
- [ ] Success rate: 100% (sustained)
- [ ] Documentation ratio: 30-40% (sustained)
- [ ] Feature velocity: ≥ 0.6 features/loop (sustained)

### Risks

**Risk: Quality overhead becomes bottleneck**
- **Probability:** Low
- **Impact:** Medium
- **Mitigation:** Monitor velocity, if < 0.5 features/loop, review standards

**Risk: Template compliance becomes ritual**
- **Probability:** Medium
- **Impact:** Low
- **Mitigation:** Review templates for bloat, remove non-essential fields

---

## Decision 4: Automate Queue Refilling (Depth < 3 Trigger)

**Status:** ✅ APPROVED
**Priority:** MEDIUM
**Implementation:** Loops 26-30

---

### Decision Made

**Implement automated queue refilling when depth drops below 3 tasks**

**Trigger Logic:**
```python
if queue_depth < 3:
    refill_to_depth = 5
    tasks_needed = refill_to_depth - queue_depth
    create_tasks(tasks_needed)
```

### Alternatives Considered

**Alternative 1: Manual queue refilling (status quo)**
- **Pros:** Human judgment, strategic control
- **Cons:** Delay (30 sec loop interval), toil, doesn't scale
- **Rejected:** Queue depth is bottleneck, need automation

**Alternative 2: Refill when queue empty (depth = 0)**
- **Pros:** Maximize throughput per refill
- **Cons:** Executor idle while refilling, lost velocity
- **Rejected:** Too late, causes gaps

**Alternative 3: Refill when depth < 3 (proactive)**
- **Pros:** Prevents queue exhaustion, smooth throughput
- **Cons:** May over-refill occasionally
- **Selected:** Best balance, proactive vs reactive

### Why This Choice

**Evidence:**
- Executor speed: 9.3 min/feature
- Queue turnover: Every 9.3 minutes
- Current risk: Queue depth 2, vulnerable window
- Vulnerability: Queue empty for ~2 minutes between refills

**Rationale:**
1. **Prevents queue exhaustion:** Refill before empty, not after
2. **Smooths throughput:** Executor always has work
3. **Buffer for complexity:** 3-task minimum accounts for unexpected complexity
4. **Scalable:** Automation works at any velocity

**Expected Outcome:**
- Queue depth never drops below 3
- Executor idle time: ~0 minutes
- Feature velocity: Increases (no gaps)

### Implementation Plan

**Step 1: Add depth check to planner loop**
- File: Planner loop script
- Logic: Check queue depth at start of loop
- Trigger: If depth < 3, initiate refill
- Timeline: Loop 26

**Step 2: Implement task creation pipeline**
- Input: Number of tasks needed (3 - current_depth)
- Process: Draft specs, create tasks, add to queue
- Output: Tasks in queue.yaml
- Timeline: Loop 27

**Step 3: Test and validate**
- Scenario: Queue depth drops to 2
- Action: Automation creates 3 tasks
- Validation: Depth returns to 5
- Timeline: Loop 28

**Step 4: Document and monitor**
- File: `knowledge/analysis/queue-automation.md`
- Metrics: Refill frequency, depth distribution, executor idle time
- Timeline: Loop 29

### Success Criteria

- [ ] Queue depth never drops below 3
- [ ] Executor idle time: < 1 minute per feature
- [ ] Refill frequency: 1-2 times per hour
- [ ] Feature velocity: ≥ 0.7 features/loop (improved)

### Risks

**Risk: Over-refilling (queue too deep)**
- **Probability:** Medium
- **Impact:** Low
- **Mitigation:** Cap at 5 tasks, monitor depth distribution

**Risk: Poor task quality (automated drafting)**
- **Probability:** Medium
- **Impact:** High
- **Mitigation:** Use templates, validate specs before task creation

---

## Decision 5: Expand Feature Pipeline (5-10 New Specs)

**Status:** ✅ APPROVED
**Priority:** HIGH
**Implementation:** Loops 27-30

---

### Decision Made

**Draft 5-10 new feature specifications by Loop 30 to prevent pipeline exhaustion**

**Current State:**
- Features completed: 6
- Features in queue: 2 (F-009, F-010)
- Pipeline risk: Medium (50% chance of exhaustion)

**Target State:**
- Features completed: 10-12
- Features in queue: 5-10
- Pipeline risk: Low

### Alternatives Considered

**Alternative 1: Reactive drafting (draft when queue low)**
- **Pros:** Just-in-time, no wasted effort
- **Cons:** Rushed specs, quality risk, queue gaps
- **Rejected:** Reactive causes delays

**Alternative 2: Proactive drafting (maintain buffer)**
- **Pros:** Smooth pipeline, quality specs, no gaps
- **Cons:** Upfront effort, may not use all specs
- **Selected:** Prevents bottlenecks, quality-first

**Alternative 3: Batch drafting (draft 20+ specs upfront)**
- **Pros:** Large buffer, long runway
- **Cons:** Waste (specs may change), upfront effort
- **Rejected:** Over-investment, specs may become stale

### Why This Choice

**Evidence:**
- Current velocity: 0.63 features/loop
- Pipeline size: 2 tasks (3.2 loops of work)
- Time to exhaustion: ~3 loops
- Drafting time: ~10 min per spec

**Rationale:**
1. **Prevents queue exhaustion:** 5-10 specs = 8-16 loops of work
2. **Quality over rush:** Proactive drafting allows thorough specs
3. **Buffer for complexity:** Extra specs account for rework or complexity
4. **Scalable:** Template-based drafting is efficient

**Expected Outcome:**
- Pipeline depth: 5-10 features
- Time to exhaustion: 8-16 loops (vs current 3 loops)
- Spec quality: High (thorough, not rushed)

### Implementation Plan

**Step 1: Review feature backlog** (Loop 27)
- Input: Existing feature ideas, stakeholder requests
- Process: Identify 10-15 candidates
- Output: Prioritized candidate list

**Step 2: Draft feature specs** (Loops 27-29)
- Template: `plans/features/FEATURE-XXX.md.template`
- Process: Draft 2-3 specs per loop
- Output: Complete feature specs

**Step 3: Validate and prioritize** (Loop 30)
- Criteria: Value score, effort estimate, dependencies
- Process: Score using calibrated formula
- Output: Prioritized feature list

**Step 4: Add to queue** (Loop 30+)
- Trigger: When queue depth < 3
- Process: Create tasks from top-priority specs
- Output: Queue replenished

### Success Criteria

- [ ] 5-10 feature specs drafted by Loop 30
- [ ] All specs follow template
- [ ] Prioritized using calibrated formula
- [ ] Queue depth: 5+ tasks

### Risks

**Risk: Specs become stale**
- **Probability:** Medium
- **Impact:** Medium
- **Mitigation:** Review specs in Loop 30, update as needed

**Risk: Low-value specs drafted**
- **Probability:** Medium
- **Impact:** High
- **Mitigation:** Prioritize using value score, stakeholder review

---

## Summary of Decisions

| Decision | Priority | Implementation | Impact |
|----------|----------|----------------|--------|
| **D-001:** Update estimation formula | CRITICAL | Loop 21 | High (better prioritization) |
| **D-002:** Prioritize automation | HIGH | Loops 21-26 | High (reduces toil) |
| **D-003:** Maintain quality standards | HIGH | Ongoing | High (prevents rework) |
| **D-004:** Automate queue refilling | MEDIUM | Loops 26-30 | Medium (smooths throughput) |
| **D-005:** Expand feature pipeline | HIGH | Loops 27-30 | High (prevents exhaustion) |

---

## Decision Log

**All decisions made in Loop 20:**

1. **D-001: Update Estimation Formula with 6x Calibration**
   - Status: Approved
   - Priority: CRITICAL
   - Rationale: Aligns estimates with 15.9x observed speedup
   - Expected Impact: Priority scores reflect actual value/time ratio

2. **D-002: Prioritize Automation Over New Features**
   - Status: Approved
   - Priority: HIGH
   - Rationale: Manual toil doesn't scale, automation enables 15+ features
   - Expected Impact: Eliminates 15-20 min manual work per 10 loops

3. **D-003: Maintain Quality Standards**
   - Status: Approved
   - Priority: HIGH
   - Rationale: 0% rework rate proves quality prevents waste
   - Expected Impact: Sustains 100% success rate, 0% rework

4. **D-004: Automate Queue Refilling**
   - Status: Approved
   - Priority: MEDIUM
   - Rationale: Queue depth is bottleneck, automation prevents gaps
   - Expected Impact: Executor idle time ~0, velocity increases

5. **D-005: Expand Feature Pipeline**
   - Status: Approved
   - Priority: HIGH
   - Rationale: Current pipeline (2 tasks) at risk of exhaustion
   - Expected Impact: 8-16 loops of work (vs current 3 loops)

---

## Next Steps

**For Loop 21:**
1. Implement D-001 (Update estimation formula)
2. Monitor F-009 completion
3. Refill queue if depth < 3

**For Loops 21-30:**
1. Complete D-002 (Automation projects)
2. Maintain D-003 (Quality standards)
3. Implement D-004 (Queue refilling)
4. Execute D-005 (Feature pipeline expansion)

---

**End of DECISIONS.md**
