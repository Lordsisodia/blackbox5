# DECISIONS: TASK-1769861580 - Update Roadmap STATE

## Decision 1: Update STATE.yaml Instead of Moving Plan Folders

**Context:** PLAN-002 and PLAN-004 folders still exist in `03-planned/` but the work is done.

**Options:**
- **Option A:** Move plan folders to `05-completed/YYYY/`
- **Option B:** Only update STATE.yaml metadata
- **Option C:** Both move folders and update STATE.yaml

**Selected:** Option B - Only update STATE.yaml

**Rationale:**
- The plan folders contain useful reference documentation
- Moving folders requires creating year directories and updating paths
- STATE.yaml is the "single source of truth" - updating it is sufficient
- The folders in `03-planned/` don't block anything (they're just reference)

**Reversibility:** HIGH - Can move folders later if needed

---

## Decision 2: Update Dependencies for PLAN-003

**Context:** PLAN-003 was blocked by both PLAN-002 and PLAN-005. PLAN-002 is now complete.

**Options:**
- **Option A:** Remove PLAN-002 from PLAN-003's dependencies
- **Option B:** Keep both dependencies (even though one is complete)

**Selected:** Option A - Remove PLAN-002 from dependencies

**Rationale:**
- Accurate dependency tracking = fewer blockers
- PLAN-003 is now only blocked by PLAN-005
- This makes `next_action: PLAN-005` correct

**Reversibility:** LOW - If PLAN-002 wasn't actually complete, we'd need to re-add it

---

## Decision 3: Keep PLAN-007 in Completed Section

**Context:** PLAN-007 is marked completed in STATE.yaml but folder is still in `03-planned/`

**Options:**
- **Option A:** Move PLAN-007 folder to `05-completed/`
- **Option B:** Leave it and note the inconsistency
- **Option C:** Investigate PLAN-007's actual status

**Selected:** Option B - Leave as-is for now

**Rationale:**
- PLAN-007 was completed by a different agent (Ralphy v4.0.0)
- The completion metadata in STATE.yaml is detailed and credible
- Folder location doesn't affect the "single source of truth" status
- Can be cleaned up in a future cleanup task

**Reversibility:** HIGH - Can always move folders later
