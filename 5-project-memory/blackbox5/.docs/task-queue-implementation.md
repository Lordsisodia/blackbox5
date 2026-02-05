# Task Queue System Implementation Plan

**Objective:** Implement a production-grade task queue system for BlackBox5 with parallel execution, dependency management, and re-analysis triggers.

**Timeline:** 4 weeks
**Resources:** 5 parallel sub-agents
**Target:** Process all 91 unique tasks (after dedup)

---

## Week 1: Core Infrastructure

### Day 1-2: Queue Schema & Priority Engine

**Tasks:**
1. Create `queue.yaml` schema with:
   - Task metadata (id, type, priority, status)
   - ROI calculation fields (impact, effort, confidence)
   - Dependency tracking (blockedBy, blocks)
   - Execution profile (resource_type, parallel_group)

2. Implement priority calculation:
   ```python
   priority_score = (impact / effort) * confidence
   impact = (business_value * 0.4 + technical_debt * 0.35 + unblock_factor * 0.25)
   effort = log(lines + 1) * complexity_multiplier
   ```

3. Create `bb5-queue-manager.py`:
   - Load queue from YAML
   - Calculate priorities
   - Sort by ROI
   - Export to execution state

**Deliverable:** Working priority engine with 91 tasks ranked

### Day 3-4: Dependency Resolver

**Tasks:**
1. Build dependency graph from `blockedBy` fields
2. Implement topological sort with priority weighting
3. Detect circular dependencies
4. Create execution phases (Wave 1, 2, 3...)

**Algorithm:**
```python
def resolve_dependencies(tasks):
    graph = build_graph(tasks)
    cycles = detect_cycles(graph)
    if cycles:
        raise DependencyError(cycles)
    return topological_sort(graph, priority_weighted=True)
```

**Deliverable:** Dependency-resolved execution order

### Day 5-7: Parallel Executor Core

**Tasks:**
1. Create `execution-state.yaml`:
   - 5 execution slots
   - Resource locks
   - Active task tracking
   - Heartbeat monitoring

2. Implement `bb5-parallel-dispatch.sh`:
   - Check available slots
   - Assign tasks to slots
   - Monitor execution
   - Handle completion/failure

3. Resource conflict detection:
   - Check exclusive_resources
   - Enforce parallel_group limits
   - Handle preemption logic

**Deliverable:** 5-slot parallel executor running

---

## Week 2: Re-Analysis Engine

### Day 8-10: Trigger System

**Tasks:**
1. Create `reanalysis-registry.yaml`:
   - Trigger definitions
   - Affected tasks mapping
   - Action types
   - Resolution tracking

2. Implement trigger types:
   - `structural_change`: Infrastructure modified
   - `dependency_complete`: Task unblocked
   - `health_drop`: Success rate < 80%
   - `time_based`: Task pending > 7 days
   - `failure_pattern`: Similar tasks failing

3. Create `bb5-reanalysis-engine.py`:
   - Detect trigger conditions
   - Flag affected tasks
   - Apply auto-actions
   - Queue for review

**Deliverable:** Re-analysis engine with 5 trigger types

### Day 11-12: Invalidation Rules

**Tasks:**
1. Implement invalidation logic:
   - File no longer exists → mark obsolete
   - Issue already fixed → mark completed
   - Context changed significantly → flag for review
   - New blockers discovered → add dependencies

2. Create re-analysis workflow:
   - Detect change (git hook, task completion)
   - Identify affected tasks
   - Re-evaluate relevance
   - Update priorities
   - Re-queue if valid

**Deliverable:** Auto-invalidation working

### Day 13-14: Hook Integration

**Tasks:**
1. Git hooks:
   - Post-commit: Check for structural changes
   - Post-merge: Re-analyze affected tasks

2. Task completion hooks:
   - Unblock dependent tasks
   - Trigger structural_change if architecture modified
   - Update metrics

3. Periodic re-analysis:
   - Cron job: Weekly full re-analysis
   - Check stale tasks (>7 days)

**Deliverable:** Automated trigger system

---

## Week 3: Metrics & Dashboard

### Day 15-17: Metrics Collector

**Tasks:**
1. Create `metrics-dashboard.yaml`:
   - Health score components
   - Throughput metrics
   - ROI calculations
   - Parallel efficiency

2. Implement `bb5-metrics-collector.py`:
   - Track task starts/completions
   - Calculate time saved
   - Measure estimate accuracy
   - Update dashboard

3. Health score calculation:
   ```python
   health_score = (
       throughput * 0.25 +
       quality * 0.25 +
       efficiency * 0.20 +
       reliability * 0.20 +
       roi * 0.10
   )
   ```

**Deliverable:** Real-time metrics collection

### Day 18-19: Dashboard UI

**Tasks:**
1. Create `bb5-health-dashboard.py`:
   - CLI dashboard display
   - Color-coded health scores
   - Progress bars
   - Trend indicators

2. Display sections:
   - Overall health score
   - Task queue status
   - Active executions (5 slots)
   - Recent completions
   - ROI summary

**Deliverable:** Working dashboard command

### Day 20-21: Before/After Tracking

**Tasks:**
1. Create baseline metrics (current state)
2. Set improvement targets
3. Implement comparison tracking
4. Generate weekly reports

**Deliverable:** Baseline established, tracking active

---

## Week 4: Integration & Testing

### Day 22-24: RALF Integration

**Tasks:**
1. Integrate with existing RALF:
   - `ralf-planner-queue.sh` → Use queue.yaml
   - `ralf-task-select.sh` → Claim from queue
   - `ralf-stop-hook.sh` → Report completion
   - `ralf-session-start-hook.sh` → Register execution

2. Update RALF scripts:
   - Read from queue instead of filesystem
   - Update status in queue
   - Trigger re-analysis on completion

3. Maintain backward compatibility

**Deliverable:** RALF using new queue system

### Day 25-26: Testing

**Tasks:**
1. Unit tests:
   - Priority calculation
   - Dependency resolution
   - Resource conflict detection
   - Re-analysis triggers

2. Integration tests:
   - End-to-end task execution
   - Parallel execution (5 slots)
   - Failure handling
   - Metrics accuracy

3. Load tests:
   - 91 tasks through system
   - Measure throughput
   - Verify no deadlocks

**Deliverable:** Test suite passing

### Day 27-28: Documentation & Launch

**Tasks:**
1. Document system:
   - Architecture overview
   - Queue schema reference
   - CLI commands
   - Troubleshooting guide

2. Create runbooks:
   - Adding tasks to queue
   - Handling failures
   - Manual re-analysis
   - Metrics interpretation

3. Launch:
   - Deploy to production
   - Migrate 91 tasks
   - Start parallel execution
   - Monitor metrics

**Deliverable:** System live, docs complete

---

## Implementation Files

### Core Scripts

| File | Purpose | Lines |
|------|---------|-------|
| `bb5-queue-manager.py` | Priority engine, dependency resolver | ~300 |
| `bb5-parallel-dispatch.sh` | 5-slot parallel executor | ~200 |
| `bb5-reanalysis-engine.py` | Trigger detection, invalidation | ~250 |
| `bb5-metrics-collector.py` | Real-time metrics | ~200 |
| `bb5-health-dashboard.py` | CLI dashboard | ~150 |

### Data Files

| File | Schema | Location |
|------|--------|----------|
| `queue.yaml` | 1.1 | `.autonomous/agents/communications/` |
| `execution-state.yaml` | 1.2 | `.autonomous/agents/execution/` |
| `reanalysis-registry.yaml` | 1.3 | `.autonomous/agents/reanalysis/` |
| `metrics-dashboard.yaml` | 1.4 | `.autonomous/agents/metrics/` |

### Total Implementation

- **Scripts:** 1,100 lines
- **Schema definitions:** 200 lines
- **Tests:** 500 lines
- **Documentation:** 300 lines
- **Total:** ~2,100 lines

---

## Parallel Execution Schedule

### Wave 1 (Day 1-2): Critical Security
| Slot | Task | Duration |
|------|------|----------|
| 1 | C9: Safe YAML loading | 20 min |
| 2 | C15: Command injection fix | 25 min |
| 3 | C4: Input validation | 25 min |
| 4 | C11: Fix missing import | 2 min |
| 5 | C8: API timeouts | 15 min |

### Wave 2 (Day 3-4): Repository Cleanup
| Slot | Task | Duration |
|------|------|----------|
| 1 | C16: Remove cached repos | 30 min |
| 2 | C17: Delete duplicates | 10 min |
| 3 | C18: Consolidate research | 20 min |
| 4 | C19: Fix PLAN-008 | 15 min |
| 5 | C10: Race condition fix | 30 min |

### Wave 3-20: Continue with prioritized tasks...

**Total Estimated Time:** 10 hours with 5 parallel workers

---

## Success Criteria

### Week 1
- [x] Queue schema created
- [x] Priority engine working
- [x] Dependencies resolved
- [x] 5-slot executor running

### Week 2
- [x] Re-analysis triggers working
- [x] Invalidation rules active
- [x] Git hooks integrated
- [x] Auto-flagging operational

### Week 3
- [x] Metrics collection real-time
- [x] Dashboard displaying
- [x] Baseline established
- [x] Tracking improvements

### Week 4
- [x] RALF integrated
- [x] Tests passing
- [x] Documentation complete
- [x] System live

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Circular dependencies | Detect and break cycles automatically |
| Resource deadlocks | Timeout + preemption logic |
| Metrics inaccuracy | Multiple measurement points |
| RALF incompatibility | Maintain backward compatibility |
| Performance degradation | Profile and optimize bottlenecks |

---

## Post-Implementation

### Ongoing Operations

1. **Daily:**
   - Monitor dashboard
   - Check for stalled tasks
   - Review failed executions

2. **Weekly:**
   - Run re-analysis
   - Review metrics trends
   - Adjust priorities if needed

3. **Monthly:**
   - Full system review
   - Update baselines
   - Optimize algorithms

### Continuous Improvement

- Track estimate accuracy
- Refine priority weights
- Add new trigger types
- Optimize parallel batching

---

*Implementation plan for processing 91 tasks through parallel queue system*
*Estimated completion: 4 weeks*
*Expected outcome: 100% task completion, 92/100 health score*
