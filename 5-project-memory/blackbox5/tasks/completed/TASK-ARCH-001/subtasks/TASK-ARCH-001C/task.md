# TASK-ARCH-001C: Create First Principles Validation Checklist

**Status:** pending
**Priority:** HIGH
**Parent Task:** TASK-ARCH-001
**Created:** 2026-02-04
**Estimated:** 15 minutes

---

## Objective

Create a concrete, actionable checklist for validating any architectural improvement against the four first principles.

---

## Success Criteria

- [ ] Four first principles documented with definitions
- [ ] Each principle has 3-5 validation questions
- [ ] Scoring rubric defined (1-5 scale)
- [ ] Examples provided for each principle
- [ ] Checklist is usable by AI agents

---

## First Principles

### 1. Single Source of Truth

**Definition:** One canonical location for each piece of information. No duplicates, no conflicting versions.

**Validation Questions:**
- Does this information exist in only one place?
- If someone needs this info, do they know exactly where to look?
- Are there any other docs that might contain similar/conflicting info?
- Is there a clear "owner" document for this information?

**Scoring:**
- 5: Perfect - exactly one canonical location
- 4: Good - mostly single source, minor overlaps
- 3: Okay - some duplication but manageable
- 2: Poor - significant duplication exists
- 1: Bad - information scattered everywhere

**Example:**
- Good: "All architecture decisions live in decisions/architectural/"
- Bad: "Architecture info in README.md, ARCHITECTURE.md, and decisions/"

---

### 2. Convention over Configuration

**Definition:** Standard naming, standard locations, standard structures. Don't make people guess.

**Validation Questions:**
- Does this follow established naming conventions?
- Is the location predictable based on the content type?
- Would a new team member know where to put this?
- Are there documented conventions for this type of file?

**Scoring:**
- 5: Perfect - follows all conventions perfectly
- 4: Good - follows conventions with minor deviations
- 3: Okay - mostly conventional but some inconsistency
- 2: Poor - inconsistent with established patterns
- 1: Bad - completely unconventional

**Example:**
- Good: "task.md in every task folder"
- Bad: "Some tasks use TASK.md, some use task.md, some use README.md"

---

### 3. Minimal Viable Documentation

**Definition:** Only document what's needed. Delete obsolete docs. Don't maintain what you don't need.

**Validation Questions:**
- Is this documentation actually being used?
- Would anyone miss this if it were deleted?
- Is there a simpler way to convey this information?
- Does this duplicate information found elsewhere?

**Scoring:**
- 5: Perfect - lean, essential docs only
- 4: Good - mostly minimal, minor bloat
- 3: Okay - some unnecessary docs but not excessive
- 2: Poor - significant documentation bloat
- 1: Bad - documentation graveyard, lots of obsolete content

**Example:**
- Good: "3 root files: README.md, STATE.yaml, Ralf-context.md"
- Bad: "14 root files, many overlapping, several obsolete"

---

### 4. Hierarchy of Information

**Definition:** Clear levels - Project → Plans → Tasks. No overlap between levels.

**Validation Questions:**
- Does this belong at this level of the hierarchy?
- Is there a clear parent/child relationship?
- Does this overlap with information at another level?
- Can you trace from Goal → Plan → Task → Subtask?

**Scoring:**
- 5: Perfect - crystal clear hierarchy, no overlap
- 4: Good - clear hierarchy, minor overlaps
- 3: Okay - hierarchy exists but some confusion
- 2: Poor - hierarchy unclear, significant overlap
- 1: Bad - no clear hierarchy, everything mixed together

**Example:**
- Good: "Goal defines WHY, Plan defines HOW, Task defines WHAT"
- Bad: "Goals have implementation details, tasks have strategic decisions"

---

## Combined Scoring

**Formula:**
```
Weighted Score =
  (Single Source × 0.25) +
  (Convention × 0.25) +
  (Minimal × 0.25) +
  (Hierarchy × 0.25)
```

**Interpretation:**
- 4.0-5.0: Excellent - proceed with confidence
- 3.0-3.9: Good - minor concerns, proceed with notes
- 2.0-2.9: Okay - significant concerns, consider alternatives
- 1.0-1.9: Poor - major issues, don't proceed without redesign

---

## Deliverable

Document at: `knowledge/architecture/first-principles-checklist.md`
