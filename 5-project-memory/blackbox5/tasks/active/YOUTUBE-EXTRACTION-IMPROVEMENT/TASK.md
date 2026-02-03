# TASK: Improve YouTube Video Extraction Process

**Status:** in_progress
**Priority:** HIGH
**Created:** 2026-02-03
**Task ID:** YOUTUBE-EXTRACTION-IMPROVEMENT

---

## Objective

Improve the 3-iteration extraction process for YouTube video content by adding a meta-layer: run 3 parallel extractions (each with 3 iterations), then synthesize the results to achieve higher coverage and consistency.

---

## Background

Analysis of two separate extractions of the same video (IndyDevDan's "Claude Code Task System") revealed:
- **Raw miss rate:** 40-53% of concepts were unique to one extraction
- **After adjusting for renames:** 20-30% truly unique content in each extraction
- **Score inconsistency:** Same concepts rated 17 points differently between extractions

This indicates that a single 3-iteration extraction misses significant content.

---

## Success Criteria

- [ ] Document new 3x3 extraction process (3 parallel extractions × 3 iterations each)
- [ ] Document consolidation/synthesis methodology
- [ ] Create implementation script for the new process
- [ ] Run test extraction on IndyDevDan video using new process
- [ ] Compare coverage vs single 3-iteration extraction
- [ ] Measure score consistency improvement

---

## Approach

### Phase 1: Documentation
1. Update `CLAUDE-EXTRACTION-PROCESS.md` with new 3x3 methodology
2. Define consolidation rules for merging parallel extractions
3. Document score reconciliation process

### Phase 2: Implementation
1. Create `extract_claude_v2.py` script
2. Implement parallel extraction spawning
3. Implement synthesis/consolidation logic

### Phase 3: Validation
1. Run new process on test video
2. Compare output vs previous extractions
3. Measure improvement metrics

---

## Files to Modify

- `/Users/shaansisodia/.blackbox5/6-roadmap/research/external/YouTube/AI-Improvement-Research/.docs/CLAUDE-EXTRACTION-PROCESS.md`
- `/Users/shaansisodia/.blackbox5/6-roadmap/research/external/YouTube/AI-Improvement-Research/scripts/extract_claude.py` (or create v2)

---

## Rollback Strategy

- Keep original extraction script unchanged
- Version new process as v2
- Can fall back to single 3-iteration process if needed

---

## Notes

The 3x3 process:
1. Spawn 3 sub-agents, each running the full 3-iteration extraction
2. Collect 3 master documents
3. Run synthesis iteration to:
   - Merge unique concepts from all 3
   - Reconcile score differences (average or consensus)
   - Resolve naming inconsistencies
   - Create unified master document

---

## Timeline

- Documentation: In progress
- Implementation: Pending
- Testing: Pending
- Completion: Pending
