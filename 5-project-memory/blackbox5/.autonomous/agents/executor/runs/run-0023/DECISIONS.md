# Decisions - TASK-1769892006

## Reference Counting Method

**Context:** Needed to determine how to count references to documentation files

**Selected:** Count both basename and relative path matches across .md, .yaml, .yml, .json files

**Rationale:**
- Documents can be referenced by filename alone or full path
- Different file types may reference documentation
- Provides comprehensive count of document usage

**Reversibility:** HIGH - Can recalculate with different method if needed

## Stale Threshold Definition

**Context:** Task specified ">30 days = stale"

**Selected:** Used strict 30-day threshold based on git last modified date

**Rationale:**
- Git provides accurate modification tracking
- 30 days is reasonable for active project
- All docs were within 2 days, so threshold wasn't critical

**Reversibility:** HIGH - Can adjust threshold in future audits

## Document Categories

**Context:** Needed to organize 32 documents for analysis

**Selected:** Grouped by directory location (.docs/, decisions/, knowledge/, operations/)

**Rationale:**
- Directory structure reflects document purpose
- Enables category-level metrics
- Aligns with project organization

**Reversibility:** MEDIUM - Could regroup by content type if needed
