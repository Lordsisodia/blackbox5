# LEARNINGS.md - Insights and Discoveries

## Key Learnings

### 1. Version Synchronization Gap
**Issue:** Agent-2.4 AGENT.md was created but supporting infrastructure wasn't updated.

**Learning:** When creating a new agent version, a checklist is needed:
- [ ] Create AGENT.md
- [ ] Update bin/ralf.md (if entry point)
- [ ] Copy/update templates
- [ ] Create supporting files (metrics.jsonl)
- [ ] Update scripts (dashboard, etc.)
- [ ] Update all version references

**Future Action:** Create agent-version-checklist.md

---

### 2. Documentation Coverage Reality
**Issue:** Dashboard shows 37-82% coverage across 29 runs.

**Learning:**
- LOOP COMPLETION CHECKLIST was added to 2.4 but previous runs didn't follow it
- System was working without 100% documentation
- 2.4's enforcement is new and critical

**Implication:** Previous 29 runs are "legacy" - 2.4+ will have 100% coverage.

---

### 3. Metrics System Was Non-Functional
**Issue:** ralf-metrics.jsonl didn't exist, so dashboard always showed "no metrics yet."

**Learning:**
- Agent-2.4 spec required metrics file
- Without it, performance tracking is broken
- Initialization should be part of agent setup

**Future Action:** Add metrics initialization to setup scripts

---

### 4. Dashboard Syntax Error Impact
**Issue:** Line 78 had `echo "$line" jq` instead of `echo "$line" | jq`

**Learning:**
- Error prevented recent activity display
- Rest of dashboard still worked
- Shell syntax errors are silent until that line executes

**Prevention:** Add shellcheck to CI/CD pipeline

---

### 5. Git Status Snapshot is Point-in-Time
**Issue:** Git status in ralf.md showed `feature/tier2-skills-integration` but actual branch is `feature/ralf-dev-workflow`

**Learning:**
- ralf.md documentation was stale
- Git branch names change over time
- Documentation should use dynamic checks or be version-controlled

**Implication:** Branch references in docs may become outdated.

---

## Discoveries

### 1. Previous Runs Structure
29 runs exist but most have 0 documentation files. This confirms:
- LOOP COMPLETION CHECKLIST is new in 2.4
- Previous agents didn't enforce documentation
- Documentation coverage metric in dashboard is valuable

### 2. Project Memory Structure
4 project memories exist but only RALF-CORE has active autonomous structure:
- `5-project-memory/ralf-core/.autonomous/` - Full structure
- `5-project-memory/blackbox5/` - Has .autonomous but empty tasks
- `5-project-memory/siso-internal/` - Uses `.Autonomous` (different case)
- `5-project-memory/management/` - No .autonomous directory

### 3. Agent Version Progression
```
v2.2 (Enforcement) -> v2.3 (Integration) -> v2.4 (Measurement)
- Phase gates added in 2.2
- Multi-project memory added in 2.3
- Performance tracking added in 2.4
```

Each version builds on previous. Templates should be inherited.

---

## Recommendations

### Immediate
1. Create agent-version-setup-checklist.md
2. Verify all v2.4 components are in place

### Short-term
3. Add shellcheck to CI/CD
4. Consider script to auto-update version references

### Long-term
5. Audit historical runs - determine if backfilling docs is valuable
6. Standardize project memory structure across all 4 projects
7. Create metrics migration script for future format changes
