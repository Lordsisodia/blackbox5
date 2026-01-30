# PLAN-001: Fix Skills System Critical Issues

**Priority:** 🔴 CRITICAL
**Status:** Planned
**Estimated Effort:** 1-2 days
**Dependencies:** None
**Validation Agent:** Agent 4 (Skills & Capabilities)

---

## Problem Statement

The skills system is in chaos with **3 different implementations**, causing:
- Agent skill loading completely broken
- 101 total skills, 68 unique, **33 duplicates**
- Path mismatches prevent skill attachment
- SkillManager can't find skills

**Impact:** Agents cannot attach skills, crippling agent capabilities

---

## Current State

### Three Skills Systems Found

```
blackbox5/2-engine/02-agents/capabilities/
├── skills-cap/          # OLD SYSTEM (101 skills)
│   ├── development-workflow/
│   ├── skills-dev/      # Duplicate path
│   └── [100+ skill directories]
├── .skills-new/         # NEW SYSTEM (converted skills)
│   └── [converted from skills-cap]
└── skills/              # UNCLEAR (not fully explored)
```

### Broken Path Example

```
Expected: skills-cap/development-workflow/autonomous/agent-orchestration/SKILL.md
Actual:   skills-dev/coding/development-workflow/autonomous/agent-orchestration/SKILL.md
```

### Evidence of Breakage

```python
# SkillManager test results
ERROR: Path mismatch - skills-dev vs skills-cap
WARNING: 33 duplicate skills found
FAILED: Agent skill attachment test (0/5 agents)
```

---

## Solution Design

### Phase 1: Audit & Decision (2 hours)

**Task:** Analyze all 3 systems and choose canonical one

**Steps:**
1. Count and categorize skills in each system
2. Compare skill metadata and quality
3. Identify which system is most complete
4. Document pros/cons of each

**Decision Framework:**
- Which has most complete skill definitions?
- Which has best documentation?
- Which has active usage in codebase?
- Which is easiest to maintain?

**Expected Outcome:** Decision on which system to keep

---

### Phase 2: Consolidation (4-6 hours)

**Option A: Keep `.skills-new/` (Recommended)**

**Rationale:**
- Already converted/cleaned
- Likely newer format
- "new" in name suggests it's the replacement

**Actions:**
1. Archive `skills-cap/` → `archived/skills-cap-old/`
2. Archive `skills/` → `archived/skills-legacy/` (if confirmed duplicate)
3. Rename `.skills-new/` → `skills/`
4. Update all import paths

**Option B: Keep `skills-cap/`**

**Rationale:**
- 101 skills (most complete)
- May have more mature definitions

**Actions:**
1. Archive `.skills-new/` → `archived/skills-new-attempt/`
2. Archive `skills/` → `archived/skills-legacy/`
3. Keep `skills-cap/` as `skills/`
4. Deduplicate 33 duplicate skills

**Option C: Merge Best of Both**

**Rationale:**
- Keep best definitions from each system
- Create ultimate consolidated system

**Actions:**
1. Compare skill definitions across all 3
2. For each skill, keep best version
3. Create new `skills/` with merged content
4. Archive all 3 old systems

**Effort:** 1-2 days (vs 4-6 hours for A or B)

---

### Phase 3: Path Updates (2-3 hours)

**Files to Update:**

```python
# SkillManager
blackbox5/2-engine/01-core/agents/core/skill_manager.py
- skills_path = "capabilities/skills-cap/"
+ skills_path = "capabilities/skills/"
```

```python
# Agent skill attachment
blackbox5/2-engine/01-core/agents/core/base_agent.py
- SKILLS_BASE = "skills-cap/"
+ SKILLS_BASE = "skills/"
```

```bash
# All skill references
find blackbox5 -type f \( -name "*.py" -o -name "*.md" \) -exec sed -i '' 's/skills-cap/skills/g' {} +
find blackbox5 -type f \( -name "*.py" -o -name "*.md" \) -exec sed -i '' 's/skills-dev/skills/g' {} +
find blackbox5 -type f \( -name "*.py" -o -name "*.md" \) -exec sed -i '' 's/\.skills-new/skills/g' {} +
```

---

### Phase 4: Testing (1-2 hours)

**Test Suite:**

```python
# test_skills_consolidation.py

def test_single_skills_directory():
    """Only one skills/ directory exists"""
    skills_dirs = glob("blackbox5/2-engine/02-agents/capabilities/*/SKILL.md")
    assert len(skills_dirs) == 1, f"Found {len(skills_dirs)} skills systems"

def test_no_duplicate_skills():
    """No duplicate skill names"""
    skills = load_all_skills()
    skill_names = [s.name for s in skills]
    assert len(skill_names) == len(set(skill_names)), "Duplicates found"

def test_skillmanager_finds_skills():
    """SkillManager can load all skills"""
    manager = SkillManager("blackbox5/2-engine/02-agents/capabilities/skills/")
    skills = await manager.load_all()
    assert len(skills) > 50, "Should load 50+ skills"

def test_agent_skill_attachment():
    """Agents can attach skills"""
    agent = DeveloperAgent(config)
    skill = manager.get_skill("tdd")
    agent.attach_skill(skill.name)
    assert "tdd" in agent.skills

def test_skill_paths_valid():
    """All skill paths exist"""
    skills = load_all_skills()
    for skill in skills:
        assert os.path.exists(skill.path), f"Missing: {skill.path}"
```

**Success Criteria:**
- ✅ Only 1 skills/ directory
- ✅ 0 duplicate skills
- ✅ SkillManager loads 50+ skills
- ✅ Agents can attach skills
- ✅ All skill paths valid

---

## Implementation Plan

### Step 1: Audit (30 minutes)

```bash
# Analyze skills-cap/
find blackbox5/2-engine/02-agents/capabilities/skills-cap/ -name "SKILL.md" | wc -l
find blackbox5/2-engine/02-agents/capabilities/skills-cap/ -type d | wc -l

# Analyze .skills-new/
find blackbox5/2-engine/02-agents/capabilities/.skills-new/ -name "SKILL.md" | wc -l

# Analyze skills/
find blackbox5/2-engine/02-agents/capabilities/skills/ -name "SKILL.md" | wc -l

# Compare
diff -r skills-cap/ .skills-new/ | head -20
```

### Step 2: Decision (30 minutes)

Review audit results, choose Option A, B, or C

### Step 3: Execute Consolidation (2-4 hours)

Based on decision, execute consolidation actions

### Step 4: Update Paths (1 hour)

Run sed commands to update all references

### Step 5: Test (1 hour)

Run test suite, verify all tests pass

---

## Success Metrics

- ✅ Single skills/ directory exists
- ✅ 0 duplicate skills
- ✅ SkillManager loads all skills successfully
- ✅ All agents can attach skills
- ✅ All skill paths valid and accessible
- ✅ Tests pass (5/5)

---

## Rollout Plan

### Pre-conditions
- [ ] Audit complete
- [ ] Decision made on which system to keep
- [ ] Backup created (git commit)

### Execution
1. Archive old skills systems (don't delete yet)
2. Update all path references
3. Run test suite
4. Fix any failures
5. Commit changes

### Post-conditions
- [ ] All tests passing
- [ ] SkillManager working
- [ ] Agent skill loading working
- [ ] Documentation updated

---

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Wrong system chosen | Medium | Medium | Keep archived systems for 1 week |
| Broken skill references | High | High | Comprehensive find-replace |
| Test failures | Medium | Low | Fix iteratively |
| Agent incompatibility | Low | Medium | Test all core agents |

---

## Dependencies

**Blocks:**
- PLAN-002: Fix YAML Agent Loading (skills need working)
- PLAN-003: Implement Planning Agent (needs skills)

**Blocked By:**
- None (can start immediately)

---

## Next Steps

1. Execute audit (30 min)
2. Make decision (30 min)
3. Execute consolidation (2-4 hours)
4. Update paths (1 hour)
5. Test and verify (1 hour)

**Total Estimated Time:** 1-2 days

---

**Status:** Planned
**Ready to Execute:** Yes
**Assigned To:** Unassigned
**Priority:** 🔴 CRITICAL (blocks multiple features)
