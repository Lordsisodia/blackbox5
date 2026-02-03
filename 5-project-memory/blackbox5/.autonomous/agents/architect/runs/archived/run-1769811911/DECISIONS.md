# DECISIONS.md

## Decision 1: Create Simplified Blackbox5 Implementation

**Context:** The original PLAN-008 described fixing API mismatches in code that didn't exist.

**Options:**
1. Skip the task (system non-functional but no clear path forward)
2. Fix all import dependencies in orchestration layer (high complexity, high risk)
3. Create simplified Blackbox5 that preserves interface contract (chosen)

**Selected:** Option 3

**Rationale:**
- Unblocks API and CLI immediately
- Preserves the interface contract expected by existing code
- Can be extended incrementally to integrate full orchestration
- Low risk, high value

## Decision 2: Use Self-Contained Implementation

**Context:** The orchestration layer has complex circular imports.

**Options:**
1. Fix all circular imports (time-consuming, high risk of breakage)
2. Make infrastructure module depend on orchestration (circular dependency)
3. Make infrastructure self-contained with optional components (chosen)

**Selected:** Option 3

**Rationale:**
- Infrastructure module can stand alone
- Optional components (skill_manager, guide_registry) loaded dynamically
- Avoids circular import issues
- Enables incremental integration later

## Decision 3: Fix Orchestration __init__.py

**Context:** The orchestration module __init__.py tried to import non-existent circuit breaker modules.

**Options:**
1. Create missing circuit breaker modules
2. Make imports optional with try/except (chosen)
3. Remove imports entirely

**Selected:** Option 2

**Rationale:**
- Preserves the interface for when modules are added
- Allows orchestration module to load without errors
- Minimal change, maximum compatibility
