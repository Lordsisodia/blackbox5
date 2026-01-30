# PLAN-001: Fix Skills System Critical Issues

**Priority:** 🔴 CRITICAL
**Status:** Planned
**Estimated Effort:** 1-2 days
**Dependencies:** None
**Blocks:** PLAN-002, PLAN-003

---

## Executive Summary

The skills system has **3 different implementations** causing:
- Agent skill loading completely broken
- 101 total skills, 68 unique, **33 duplicates**
- Path mismatches prevent skill attachment
- SkillManager can't find skills

**Impact:** Agents cannot attach skills, crippling agent capabilities

---

## Quick Stats

| Metric | Value |
|--------|-------|
| Total Skills | 101 |
| Unique Skills | 68 |
| Duplicates | 33 |
| Systems Found | 3 |
| Skill Loading | Broken |
| Agent Attachment | 0/5 agents |

---

## The Problem

Three skills systems exist:
```
blackbox5/2-engine/02-agents/capabilities/
├── skills-cap/          # OLD SYSTEM (101 skills)
├── .skills-new/         # NEW SYSTEM (converted)
└── skills/              # UNCLEAR
```

Path mismatch example:
```
Expected: skills-cap/development-workflow/...
Actual:   skills-dev/coding/development-workflow/...
```

---

## The Solution

**4-Phase Consolidation:**

1. **Audit** (2 hours) - Analyze all 3 systems, choose canonical one
2. **Consolidation** (4-6 hours) - Archive old systems, keep one
3. **Path Updates** (2-3 hours) - Update all references
4. **Testing** (1-2 hours) - Verify SkillManager works

---

## Files to Change

- `skill_manager.py` - Update skills path
- `base_agent.py` - Update SKILLS_BASE
- All skill references - Find and replace

---

## Success Criteria

✅ Single skills/ directory
✅ 0 duplicate skills
✅ SkillManager loads 50+ skills
✅ Agents can attach skills
✅ All tests pass (5/5)

---

## Next Steps

1. Execute audit (30 min)
2. Make decision (30 min)
3. Execute consolidation (2-4 hours)
4. Update paths (1 hour)
5. Test and verify (1 hour)

**Total:** 1-2 days

---

**Ready to Execute:** Yes
**Confidence:** High
