# DECISIONS - Run 1769800176

**Task:** TASK-1769800176 - Create Workflow Loader Library

## Decision 1: Use Dataclasses for Workflow Structure

**Context:** Need to represent workflow YAML structure in Python

**Options Considered:**
1. Plain dictionaries - Simple but no type safety
2. Named tuples - Immutable but hard to extend
3. Classes with __init__ - Verbose boilerplate
4. Dataclasses - Clean, type-safe, extensible

**Decision:** Use Python dataclasses

**Rationale:**
- Type hints provide documentation
- Automatic __init__, __repr__, __eq__
- Easy to add methods
- Works well with serialization

**Reversibility:** HIGH - Could convert to classes later

## Decision 2: Separate Loader from Data Classes

**Context:** Need to load workflows from files

**Options Considered:**
1. Static methods on Workflow class - Tight coupling
2. Separate loader class - Loose coupling
3. Module-level functions - No state management

**Decision:** Create separate WorkflowLoader class

**Rationale:**
- Loader maintains state (caching, indexing)
- Multiple loader instances possible (different directories)
- Clear separation of concerns
- Easier to test

**Reversibility:** HIGH - Could merge later if needed

## Decision 3: Lazy Loading Pattern

**Context:** When should workflows be loaded from disk?

**Options Considered:**
1. Load all on initialization - Predictable but slow
2. Load on first query - Efficient but first query slower
3. Explicit load call - Requires user to remember

**Decision:** Lazy loading (load on first query)

**Rationale:**
- Avoids I/O if workflows not used
- Caches after first load
- Transparent to users

**Reversibility:** MEDIUM - Could add eager loading option

## Decision 4: Comprehensive Validation

**Context:** Need to ensure workflow files are valid

**Options Considered:**
1. Schema validation only - Catches structure issues
2. Business logic validation - Catches semantic issues
3. Both - Most thorough

**Decision:** Implement both structural and business validation

**Validation Rules:**
- Required fields: name, command, skill, agent
- Command must be exactly 2 letters
- Steps must have name and title
- Workflows must have at least one step

**Reversibility:** HIGH - Can relax rules if too strict

## Decision 5: Include Test File Co-Located

**Context:** Where to put unit tests?

**Options Considered:**
1. Separate tests/ directory - Traditional approach
2. Co-located with source - Easier discovery
3. Both - Redundant

**Decision:** Co-located test file (test_workflow_loader.py)

**Rationale:**
- Tests are documentation
- Easy to find when reading code
- Simpler import paths
- BMAD convention

**Reversibility:** HIGH - Can move to tests/ later

## Decision 6: Support JSON Export

**Context:** Other tools may need workflow data

**Options Considered:**
1. YAML only - Native format
2. JSON export - Universal format
3. Both - Maximum compatibility

**Decision:** Support JSON export via export_to_json()

**Rationale:**
- JSON is universal
- Easy integration with other tools
- Useful for caching
- Web APIs prefer JSON

**Reversibility:** HIGH - Could remove if not used
