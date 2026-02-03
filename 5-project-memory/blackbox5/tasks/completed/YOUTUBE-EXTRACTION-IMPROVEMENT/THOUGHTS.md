# Thoughts Log - YouTube Extraction Improvement

## 2026-02-03

### Initial Analysis

Ran two separate 3-iteration extractions on the same IndyDevDan video. Results were eye-opening:

**Coverage Gap:**
- v1: 21 concepts
- v2: 27 concepts
- Only 3 concepts overlapped exactly
- After accounting for renames: ~16 concepts were the same ideas with different names
- Truly unique: 2 in v1, 9 in v2

**Score Inconsistency:**
- Same concepts rated differently by 1-17 points
- Example: "Task System Tools" rated 95 in v1, 78 in v2

**Implication:**
A single extraction misses 20-30% of extractable concepts. This is significant for a research system aiming for comprehensive coverage.

### Solution Design

The 3x3 approach:
1. **Parallel Layer:** Run 3 independent extractions simultaneously
2. **Synthesis Layer:** Merge results into unified master document

Benefits:
- Catches different interpretations/framings of same content
- Identifies truly important concepts (appear in all 3)
- Provides score confidence intervals
- Reduces individual extraction bias

### Open Questions

1. How to handle score reconciliation? Average? Weight by confidence? Keep range?
2. Should concepts appearing in only 1 of 3 extractions be flagged as "uncertain"?
3. What's the cost tradeoff? 3x API calls for ~30% more coverage - worth it?
4. Could we do 2 extractions instead of 3? Diminishing returns?

### Next Steps

1. Document the new process formally
2. Build the synthesis/consolidation logic
3. Test on the same video to measure improvement
4. Decide on production rollout
