# PLAN-006: Remove Redundant Code and Systems

**Priority:** 🟡 MEDIUM
**Status:** Planned
**Estimated Effort:** 3-5 days
**Dependencies:** None (can parallel with most)
**Validation Agent:** Agent 8 (Documentation & Redundancy)

---

## Problem Statement

Significant **redundancy exists**, causing maintenance burden and confusion.

**Critical Redundancies:**
1. 2 duplicate event bus implementations
2. 2 duplicate boot files
3. 3 skills systems (handled in PLAN-001)
4. 3 duplicate code_index.md files (432KB each!)
5. 1,184+ files with outdated `.blackbox5` references

**Impact:**
- Maintenance burden
- Unclear which version is canonical
- Confusion for developers
- Wasted disk space

---

## Solution Design

### Phase 1: Consolidate Event Bus (1 day)

**Current State:**
```
blackbox5/2-engine/01-core/infrastructure/event_bus.py    (500+ lines)
blackbox5/2-engine/01-core/middleware/event_bus.py        (400+ lines)
```

**Analysis Required:**
1. Compare implementations
2. Identify differences
3. Determine which is more complete
4. Check which is used more

**Decision Framework:**
- Which has more features?
- Which has better tests?
- Which is imported more?
- Which is more recent?

**Consolidation Plan:**
```python
# Choose one as canonical
# Keep: infrastructure/event_bus.py (recommended)

# Archive: middleware/event_bus.py
mv blackbox5/2-engine/01-core/middleware/event_bus.py \
   blackbox5/archived/middleware-event-bus-old.py

# Update all imports
find blackbox5 -name "*.py" -exec sed -i '' \
  's|from.*middleware.event_bus|from blackbox5.engine.core.infrastructure.event_bus|g' {} +
```

---

### Phase 2: Consolidate Boot Files (2 hours)

**Current State:**
```
blackbox5/2-engine/01-core/infrastructure/boot.py
blackbox5/2-engine/01-core/infrastructure/boot_sequence.py
```

**Analysis:**
1. Compare both files
2. Identify differences
3. Merge if needed
4. Keep one

**Decision:**
- If `boot_sequence.py` is newer → merge into `boot.py`, delete `boot_sequence.py`
- If `boot.py` is newer → delete `boot_sequence.py`
- If both needed → rename to clarify: `boot.py` and `boot_advanced.py`

**Commands:**
```bash
# Compare files
diff blackbox5/2-engine/01-core/infrastructure/boot.py \
     blackbox5/2-engine/01-core/infrastructure/boot_sequence.py

# Or use visual diff
vimdiff blackbox5/2-engine/01-core/infrastructure/boot.py \
        blackbox5/2-engine/01-core/infrastructure/boot_sequence.py
```

---

### Phase 3: Delete Duplicate Code Index Files (5 min)

**Current State:**
```
.blackbox5/2-engine/docs/code_index.md           (432KB)
.blackbox5/2-engine/docs/reference/code_index.md (432KB)
.blackbox5/2-engine/DOCS/index.md                (432KB)
```

**Action:**
```bash
# Keep first one, delete others
# (After verifying they're identical)

# Check if identical
md5sum blackbox5/2-engine/docs/code_index.md \
        blackbox5/2-engine/docs/reference/code_index.md \
        blackbox5/2-engine/DOCS/index.md

# If identical, keep first, archive others
mkdir -p blackbox5/archived/duplicate-docs
mv blackbox5/2-engine/docs/reference/code_index.md \
   blackbox5/archived/duplicate-docs/code_index-reference.md
mv blackbox5/2-engine/DOCS/index.md \
   blackbox5/archived/duplicate-docs/code_index-docs.md

# Update references
find blackbox5 -name "*.md" -exec sed -i '' \
  's|/docs/reference/code_index\.md|/docs/code_index.md|g' {} +
find blackbox5 -name "*.md" -exec sed -i '' \
  's|/DOCS/index\.md|/docs/code_index.md|g' {} +
```

---

### Phase 4: Update `.blackbox5` References (2-3 hours)

**Problem:** Directory renamed from `.blackbox5` to `blackbox5`, but docs not updated

**Scope:** 1,184+ files with outdated references

**Solution:** Automated find-replace

```bash
# Create script
cat > /tmp/fix_docs.sh << 'EOF'
#!/bin/bash

# Find all markdown files
find blackbox5 -name "*.md" -type f | while read file; do
    # Replace .blackbox5 with blackbox5
    sed -i '' 's/\.blackbox5\//blackbox5\//g' "$file"
    sed -i '' 's/\.blackbox5\//blackbox5\//g' "$file"
    sed -i '' 's/\.blackbox5/blackbox5/g' "$file"

    # Fix code blocks
    sed -i '' 's|cd .*\.blackbox5|cd blackbox5|g' "$file"
    sed -i '' 's|path: .*\.blackbox5|path: blackbox5|g' "$file"
done

echo "✅ Updated all markdown files"
EOF

chmod +x /tmp/fix_docs.sh
/tmp/fix_docs.sh
```

**Verification:**
```bash
# Check for remaining .blackbox5 references
grep -r "\.blackbox5" blackbox5 --include="*.md" | wc -l
# Expected: 0 (or close to it for legitimate dots)
```

---

### Phase 5: Remove Duplicate Documentation (1-2 days)

**Strategy:** Find and consolidate duplicate documentation

**Step 1: Find duplicate files by content hash**
```python
# find_duplicate_docs.py

import hashlib
from pathlib import Path
from collections import defaultdict

def find_duplicates():
    """Find duplicate files by content hash"""

    hashes = defaultdict(list)

    # Hash all markdown files
    for file in Path("blackbox5").rglob("*.md"):
        content = file.read_bytes()
        hash_val = hashlib.md5(content).hexdigest()
        hashes[hash_val].append(file)

    # Find duplicates
    duplicates = {h: files for h, files in hashes.items() if len(files) > 1}

    # Report
    print(f"Found {len(duplicates)} sets of duplicates:\n")

    for hash_val, files in duplicates.items():
        print(f"Hash: {hash_val}")
        for file in files:
            print(f"  - {file}")
        print()

    return duplicates

if __name__ == "__main__":
    duplicates = find_duplicates()
```

**Step 2: Archive duplicates**
```python
# archive_duplicates.py

import shutil
from pathlib import Path

def archive_duplicate(duplicate_files, canonical):
    """Archive duplicate files, keep canonical"""

    archive_dir = Path("blackbox5/archived/duplicate-docs")
    archive_dir.mkdir(parents=True, exist_ok=True)

    for file in duplicate_files:
        if file != canonical:
            # Create archive path
            archive_path = archive_dir / file.relative_to("blackbox5")
            archive_path.parent.mkdir(parents=True, exist_ok=True)

            # Archive
            shutil.move(str(file), str(archive_path))
            print(f"Archived: {file} → {archive_path}")
```

---

## Implementation Plan

### Wave 1: Quick Wins (1 day)

| Task | Effort | Impact |
|------|--------|--------|
| Delete duplicate code_index.md | 5 min | 1.3MB saved |
| Update `.blackbox5` references | 2-3 hours | Fixes 1,184+ files |
| Consolidate boot files | 2 hours | Removes confusion |

### Wave 2: Event Bus Consolidation (1 day)

1. Compare implementations (2 hours)
2. Make decision (30 min)
3. Update imports (2 hours)
4. Test (2 hours)
5. Archive old version (30 min)

### Wave 3: Documentation Cleanup (1-2 days)

1. Find all duplicates (2 hours)
2. Analyze and decide (2 hours)
3. Archive duplicates (4 hours)
4. Update references (4 hours)
5. Verify (2 hours)

---

## Success Criteria

- ✅ Only 1 event bus implementation
- ✅ Only 1 boot file (or clearly differentiated)
- ✅ No duplicate code_index.md files
- ✅ `.blackbox5` references updated (0 remaining)
- ✅ Duplicate documentation archived
- ✅ All imports updated
- ✅ All references updated
- ✅ No broken links

---

## Rollout Plan

### Pre-conditions
- [ ] Backup created
- [ ] All duplicates identified
- [ ] Decisions made (keep vs archive)

### Execution
1. Archive duplicate code_index.md (5 min)
2. Update `.blackbox5` references (2-3 hours)
3. Consolidate boot files (2 hours)
4. Consolidate event bus (1 day)
5. Clean up documentation (1-2 days)

### Post-conditions
- [ ] All duplicates removed or archived
- [ ] No broken imports
- [ ] No broken references
- [ ] Documentation clean
- [ ] Tests still passing

---

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Breaking imports | High | High | Update all imports first |
| Wrong canonical choice | Medium | Medium | Analyze before deleting |
| Broken references | Medium | High | Verify all references |
| Test failures | Low | Medium | Run tests after each change |

---

## Dependencies

**Blocks:**
- Clean codebase
- Easier maintenance
- Less confusion

**Blocked By:**
- None

**Can Parallel With:**
- PLAN-004: Fix Import Paths (coordinate carefully!)
- PLAN-001: Fix Skills System
- PLAN-002: Fix YAML Agent Loading

**Cannot Parallel With:**
- None, but coordinate with PLAN-004

---

## Next Steps

1. Quick wins (code_index.md, boot files) - 3 hours
2. Update `.blackbox5` references - 2-3 hours
3. Consolidate event bus - 1 day
4. Clean up documentation - 1-2 days

**Total Estimated Time:** 3-5 days

---

**Status:** Planned
**Ready to Execute:** Yes (but coordinate with PLAN-004)
**Assigned To:** Unassigned
**Priority:** 🟡 MEDIUM (maintenance and clarity)
