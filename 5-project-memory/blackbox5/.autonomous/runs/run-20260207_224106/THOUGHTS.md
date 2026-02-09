# TASK-SSOT-020: Create Single Timeline Source

## Analysis

### Current State
- Root timeline.yaml: ~2500 lines, comprehensive events from 2026-01-20 to 2026-02-07
- 8 goal timelines in goals/active/IG-*/timeline.yaml with different formats:
  - IG-001: 15 lines, minimal events
  - IG-002: 13 lines, minimal events
  - IG-003: 11 lines, minimal events
  - IG-004: 11 lines, minimal events
  - IG-005: 11 lines, minimal events
  - IG-006: 71 lines, detailed events
  - IG-008: 34 lines, research events
  - IG-009: 21 lines, simple format (different structure)

### Problem
- Same events logged in both root and goal timelines
- Goal timelines use different formats (timestamp vs date, different field names)
- No single source of truth

### Solution Approach
Option C: Make root timeline.yaml canonical, convert goal events to root format, replace goal timelines with view definitions.

## Implementation Plan

1. Extract unique events from goal timelines
2. Convert to root timeline format
3. Add to root timeline.yaml with proper related_items
4. Create timeline-view.yaml for each goal (filtered view definition)
5. Document architecture

## Skill Usage for This Task
- Applicable skills: None (data consolidation task)
- Skill invoked: None
- Confidence: N/A
- Rationale: This is a straightforward data consolidation task without domain-specific complexity
