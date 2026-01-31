# Decisions - TASK-1738366801

## Decision 1: Manual Tracking Initially

**Context:** Need to decide between immediate automation vs manual tracking
**Selected:** Manual tracking with clear path to automation
**Rationale:** 
- Ensures accuracy while system matures
- Allows understanding of tracking patterns before automating
- Documented in automation roadmap (Phase 1 → 2 → 3)
**Reversibility:** HIGH - Can automate at any time without data loss

## Decision 2: Separate Aggregate Stats from Usage Log

**Context:** Whether to derive stats from log or maintain separate aggregates
**Selected:** Maintain both append-only log and separate aggregate stats
**Rationale:**
- Log preserves complete history for detailed analysis
- Aggregate stats allow quick overview without parsing entire log
- Monthly reviews update aggregates from log
**Reversibility:** MEDIUM - Could derive from log but would lose performance

## Decision 3: Include Trigger Accuracy Field

**Context:** How to track whether skills trigger when needed (key per goals.yaml IG-004)
**Selected:** Added `trigger_accuracy` enum field (high/medium/low/unknown)
**Rationale:**
- Directly addresses "Skill triggers may need tuning" from goals.yaml
- Allows identification of skills that don't trigger when they should
- Also captures false positives (triggering when not needed)
**Reversibility:** HIGH - Field can be removed or modified

## Decision 4: Skills Path Correction

**Context:** Task specified path `~/.blackbox5/5-project-memory/siso-internal/.Autonomous/.skills/` which doesn't exist
**Selected:** Used actual path `2-engine/.autonomous/skills/`
**Rationale:**
- README.md confirms this is the correct skills location
- All 22 skill directories found there
- Path matches the documented structure
**Reversibility:** N/A - Corrected to actual path

## Decision 5: YAML Over JSON

**Context:** Choice of file format for tracking data
**Selected:** YAML with clear schema
**Rationale:**
- Human-readable and editable
- Native comment support for documentation
- Consistent with other BlackBox5 configuration files
- Supports complex nested structures
**Reversibility:** MEDIUM - Could convert to JSON but would lose comments
