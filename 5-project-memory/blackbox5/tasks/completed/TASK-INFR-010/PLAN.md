# PLAN.md: Learning Index Shows Zero Learnings Despite 80+ Claimed

**Task ID:** TASK-INFR-010  
**Status:** In Progress  
**Priority:** HIGH  
**Importance Rating:** 85/100  
**Estimated Timeline:** 4-6 hours

---

## 1. First Principles Analysis

### Why is Learning Indexing Important?

1. **Knowledge Loss**: THOUGHTS.md and DECISIONS.md insights lost after each session
2. **Repeated Mistakes**: Same errors recur without surfacing past learnings
3. **Inefficiency**: Rediscover solutions already found
4. **No Pattern Recognition**: Cannot identify recurring patterns

### What Happens Without Indexing?

- **learning-index.yaml** shows `total_learnings: 0`
- Header claims auto-populated by `learning_extractor.py`
- **No learning_extractor.py exists**
- **60+ run directories** contain valuable learnings

### How Can We Fix Indexing?

1. **Create learning_extractor.py**
2. **Implement extraction logic**
3. **Integrate with task completion**
4. **Backfill existing runs**
5. **Add monitoring**

---

## 2. Current State Assessment

### Existing Infrastructure

| Component | Status | Location |
|-----------|--------|----------|
| Learning Index | Empty | `memory/insights/learning-index.yaml` |
| RETAIN Engine | Exists | `.autonomous/memory/operations/retain.py` |
| Run Directories | 60+ with data | `.autonomous/agents/executor/runs/` |
| Feature F-010 Spec | Complete | `plans/features/FEATURE-010-knowledge-base.md` |

### Root Cause

learning-index.yaml header states:
```yaml
# Auto-populated by learning_extractor.py
```

**However:**
- No `learning_extractor.py` exists
- RETAIN uses different memory model
- Feature F-010 spec calls for it but never implemented

---

## 3. Proposed Solution

### Architecture Decision

Implement YAML-based learning-index.yaml as originally designed:
- Human-readable, git-friendly
- Simple CLI interfaces
- No external dependencies

### Solution Components

1. **learning_extractor.py** - Core extraction library
2. **Integration with retain-on-complete.py** - Hook integration
3. **Backfill script** - Recovery tool
4. **Validation and monitoring**

---

## 4. Implementation Plan

### Phase 1: Debug Extraction (60 min)

1. Analyze 5-10 run directories
2. Identify learning patterns
3. Define extraction regex
4. Create test cases

### Phase 2: Implement learning_extractor.py (90 min)

1. Define data structures
2. Implement THOUGHTS.md parser
3. Implement DECISIONS.md parser
4. Add categorization logic
5. Implement index update

### Phase 3: Integrate Hooks (30 min)

1. Modify `retain-on-complete.py`
2. Add learning extraction call
3. Test integration
4. Handle errors

### Phase 4: Backfill Historical Data (45 min)

1. Create `backfill_learnings.py`
2. Process all 60+ run directories
3. Deduplicate by content hash
4. Verify results

### Phase 5: Add Monitoring (30 min)

1. Create health check script
2. Add metrics collection
3. Create validation tests

---

## 5. Success Criteria

### Phase 1
- [ ] Extraction patterns documented
- [ ] Test cases created
- [ ] >80% expected accuracy

### Phase 2
- [ ] learning_extractor.py created
- [ ] Can extract from single run
- [ ] CLI interface working
- [ ] Unit tests passing

### Phase 3
- [ ] Hook calls learning_extractor
- [ ] Index updates automatically
- [ ] Error handling prevents failures

### Phase 4
- [ ] All 60+ runs processed
- [ ] Index shows >50 learnings
- [ ] No duplicates

### Phase 5
- [ ] Health check validates integrity
- [ ] Monitoring alerts if stopped
- [ ] Tests run successfully

---

## 6. Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Debug | 60 min | 60 min |
| Phase 2: Implement | 90 min | 150 min |
| Phase 3: Integrate | 30 min | 180 min |
| Phase 4: Backfill | 45 min | 225 min |
| Phase 5: Monitor | 30 min | 255 min |
| **Buffer** | 30 min | **285 min** |
| **Total** | **~5 hours** | |

---

*Plan created based on learning system analysis*
