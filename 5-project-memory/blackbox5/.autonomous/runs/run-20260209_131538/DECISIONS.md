# DECISIONS - Memory Structure Improvement

## Decision 1: Create Root README

**Context:** The memory directory lacked a central documentation file.

**Options:**
1. Create comprehensive README with full structure documentation
2. Create minimal README with just links
3. Update existing files only

**Selected:** Option 1 - Comprehensive README

**Rationale:**
- Provides single source of truth for memory structure
- Helps new developers understand the system
- Documents the 4-network architecture clearly
- Includes usage examples

---

## Decision 2: Fix Hardcoded Paths

**Context:** `extraction/README.md` contained `/Users/shaansisodia/.blackbox5/` path.

**Options:**
1. Replace with relative path `.autonomous/memory/`
2. Use environment variable reference
3. Remove the reference entirely

**Selected:** Option 1 - Relative path

**Rationale:**
- Makes documentation portable across environments
- Follows existing conventions in other docs
- Simple and clear

---

## Decision 3: Update Decision Registry

**Context:** `decisions/registry.md` had outdated RALF references.

**Options:**
1. Update to BB5 references
2. Delete the deprecated file
3. Leave as-is with note

**Selected:** Option 1 - Update references

**Rationale:**
- Maintains the deprecation notice
- Updates the project name for consistency
- Keeps the format template which is still useful

---

## Decision 4: Create Insights Index

**Context:** The insights directory was referenced but didn't exist.

**Options:**
1. Create directory with index.md
2. Create directory only
3. Update references to remove insights mention

**Selected:** Option 1 - Directory with index.md

**Rationale:**
- Provides documentation for the learning index
- Explains the 4-network memory types with examples
- Documents usage and maintenance procedures
