# BlackBox5 Architecture Migration Plan

**Date:** 2026-02-02
**Status:** Proposed
**Goal:** Clean up scattered .autonomous folders, establish clear separation between engine and project data

---

## Current State (Messy)

```
.blackbox5/
├── .autonomous/                    # ROOT LEVEL - Unknown purpose, DELETE
│   ├── communications/
│   ├── goals/
│   ├── tasks/
│   └── ...
│
├── 2-engine/
│   └── .autonomous/                # Engine infrastructure (MISNAMED)
│       ├── prompts/
│       ├── skills/
│       ├── lib/
│       └── ...
│
├── 5-project-memory/
│   ├── blackbox5/
│   │   └── .autonomous/            # Project data (CORRECT LOCATION)
│   │       ├── communications/
│   │       ├── tasks/
│   │       ├── runs/
│   │       └── ...
│   │
│   └── management/
│       └── .autonomous/            # UNKNOWN PURPOSE, DELETE
│
└── archived/
    └── duplicate-docs/
        └── 2-engine/.autonomous/   # ARCHIVED DUPLICATE, DELETE
```

**Problems:**
- 7 .autonomous folders scattered everywhere
- Root .autonomous purpose unclear
- 2-engine/.autonomous misnamed (it's the engine, not autonomous data)
- management/.autonomous unused
- Archived duplicates wasting space

---

## Target State (Clean)

```
.blackbox5/
├── 2-engine/
│   └── autonomous-core/            # RENAMED from .autonomous
│       ├── prompts/
│       ├── skills/
│       ├── lib/
│       ├── config/
│       └── workflows/
│
├── 5-project-memory/
│   ├── blackbox5/
│   │   ├── autonomous/             # KEEP (already correct)
│   │   │   ├── communications/
│   │   │   ├── tasks/
│   │   │   │   ├── active/
│   │   │   │   ├── completed/
│   │   │   │   └── improvements/
│   │   │   ├── runs/
│   │   │   │   ├── planner/
│   │   │   │   ├── executor/
│   │   │   │   └── architect/
│   │   │   └── context/
│   │   │       └── ARCHITECTURE_CONTEXT.md
│   │   │
│   │   ├── goals.yaml              # Project goals
│   │   ├── plans/                  # Project plans
│   │   │   ├── features/
│   │   │   └── prds/
│   │   └── ...
│   │
│   └── management/                 # NO .autonomous folder
│
└── [NO ROOT .autonomous]
```

---

## Migration Steps

### Phase 1: Delete Obsolete (Low Risk)

**Step 1.1: Delete Root .autonomous**
```bash
# BEFORE DELETING: Check what's there
ls -la ~/.blackbox5/.autonomous/

# If it contains anything not elsewhere, migrate it
# Then delete
rm -rf ~/.blackbox5/.autonomous/
```

**Step 1.2: Delete management/.autonomous**
```bash
ls -la ~/.blackbox5/5-project-memory/management/.autonomous/
rm -rf ~/.blackbox5/5-project-memory/management/.autonomous/
```

**Step 1.3: Delete Archived Duplicates**
```bash
rm -rf ~/.blackbox5/archived/duplicate-docs/2-engine/.autonomous/
```

**Verification:**
```bash
# Should only find 2 .autonomous folders now
find ~/.blackbox5 -type d -name ".autonomous" 2>/dev/null
# Expected: 2-engine/.autonomous and 5-project-memory/blackbox5/.autonomous
```

---

### Phase 2: Rename Engine (Medium Risk)

**Step 2.1: Rename 2-engine/.autonomous to autonomous-core**
```bash
cd ~/.blackbox5/2-engine/
mv .autonomous autonomous-core
```

**Step 2.2: Update All References**

Files that reference `2-engine/.autonomous`:
```bash
# Find all references
grep -r "2-engine/.autonomous" ~/.blackbox5 --include="*.sh" --include="*.md" --include="*.yaml" 2>/dev/null

# Expected files to update:
# - bin/ralf-planner
# - bin/ralf-executor
# - bin/ralf-architect
# - Any documentation
```

**Update bin/ralf-planner:**
```bash
sed -i 's|2-engine/.autonomous|2-engine/autonomous-core|g' ~/.blackbox5/bin/ralf-planner
```

**Update bin/ralf-executor:**
```bash
sed -i 's|2-engine/.autonomous|2-engine/autonomous-core|g' ~/.blackbox5/bin/ralf-executor
```

**Update bin/ralf-architect:**
```bash
sed -i 's|2-engine/.autonomous|2-engine/autonomous-core|g' ~/.blackbox5/bin/ralf-architect
```

**Verification:**
```bash
# Should find no references to old path
grep -r "2-engine/.autonomous" ~/.blackbox5 --include="*.sh" 2>/dev/null | grep -v ".git"
```

---

### Phase 3: Consolidate Tasks (Medium Risk)

**Current:** Two task systems
- `5-project-memory/blackbox5/tasks/` (legacy)
- `5-project-memory/blackbox5/.autonomous/tasks/` (current)

**Target:** Single task system in autonomous/

**Step 3.1: Migrate Legacy Tasks**
```bash
cd ~/.blackbox5/5-project-memory/blackbox5/

# Create manual folder for human tasks
mkdir -p autonomous/tasks/manual

# Move legacy tasks to manual folder
mv tasks/backlog/ autonomous/tasks/manual/ 2>/dev/null || true
mv tasks/working/ autonomous/tasks/manual/ 2>/dev/null || true

# Move completed legacy tasks
mv tasks/completed/ autonomous/tasks/manual/completed-legacy/ 2>/dev/null || true

# Remove empty tasks folder
rmdir tasks 2>/dev/null || echo "tasks folder not empty, check contents"
```

**Step 3.2: Update Task References**
```bash
# Find references to old tasks/ path
grep -r "blackbox5/tasks" ~/.blackbox5 --include="*.sh" --include="*.md" 2>/dev/null

# Update references to point to autonomous/tasks/
```

---

### Phase 4: Update Prompts (High Risk - Test Carefully)

**Step 4.1: Update Prompt References**

All prompts that reference paths need updating:
```bash
# Find prompts referencing old paths
grep -r "2-engine/.autonomous" ~/.blackbox5/2-engine/autonomous-core/prompts/ 2>/dev/null

# Update to new path
sed -i 's|2-engine/.autonomous|2-engine/autonomous-core|g' ~/.blackbox5/2-engine/autonomous-core/prompts/system/*/variations/*.md
```

**Step 4.2: Update RALF Scripts**

Update `RALF_ENGINE_DIR` references:
```bash
# In all bin/ scripts, update default path
sed -i 's|2-engine/.autonomous|2-engine/autonomous-core|g' ~/.blackbox5/bin/ralf-*
```

---

### Phase 5: Verification & Testing

**Step 5.1: Verify Structure**
```bash
echo "=== Checking Target Structure ==="
echo ""
echo "1. autonomous-core exists:"
ls -d ~/.blackbox5/2-engine/autonomous-core 2>/dev/null && echo "✓" || echo "✗"

echo ""
echo "2. Old .autonomous gone:"
ls -d ~/.blackbox5/2-engine/.autonomous 2>/dev/null && echo "✗ Still exists" || echo "✓ Gone"

echo ""
echo "3. Project autonomous exists:"
ls -d ~/.blackbox5/5-project-memory/blackbox5/autonomous 2>/dev/null && echo "✓" || echo "✗"

echo ""
echo "4. Root .autonomous gone:"
ls -d ~/.blackbox5/.autonomous 2>/dev/null && echo "✗ Still exists" || echo "✓ Gone"
```

**Step 5.2: Test Agent Launch**
```bash
# Dry run - check if scripts can find their prompts
~/.blackbox5/bin/ralf-planner --help 2>&1 | head -5
~/.blackbox5/bin/ralf-executor --help 2>&1 | head -5
```

**Step 5.3: Check Prompt Loading**
```bash
# Verify prompts are readable
cat ~/.blackbox5/2-engine/autonomous-core/prompts/system/planner/variations/v3-verification-aware.md | head -5
```

---

## Rollback Plan

If something breaks:

```bash
# Restore from git
cd ~/.blackbox5
git checkout -- .
git clean -fd

# Or manually rename back
mv 2-engine/autonomous-core 2-engine/.autonomous
```

---

## Post-Migration Cleanup

**Update Documentation:**
- Update README.md references
- Update any docs mentioning `.autonomous`
- Update CLAUDE.md if it references paths

**Update Environment Variables:**
If you have scripts setting `RALF_ENGINE_DIR`, update them:
```bash
# Old
export RALF_ENGINE_DIR="$HOME/.blackbox5/2-engine/.autonomous"

# New
export RALF_ENGINE_DIR="$HOME/.blackbox5/2-engine/autonomous-core"
```

---

## Success Criteria

- [ ] Only 2 autonomous locations exist (autonomous-core and project autonomous)
- [ ] All agents start successfully
- [ ] All prompts load correctly
- [ ] Tasks are consolidated in autonomous/tasks/
- [ ] No references to old paths in scripts
- [ ] Documentation updated

---

## Timeline

**Phase 1 (Delete obsolete):** 5 minutes
**Phase 2 (Rename engine):** 15 minutes
**Phase 3 (Consolidate tasks):** 10 minutes
**Phase 4 (Update prompts):** 20 minutes
**Phase 5 (Verification):** 10 minutes

**Total:** ~1 hour

---

## Notes

- Make sure to commit current state before starting
- Test each phase before moving to next
- Keep terminal open to root .blackbox5 for easy rollback
- Have git status ready to see what changed
