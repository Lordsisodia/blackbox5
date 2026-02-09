# Decisions - TASK-1769952151

## D1: Simple Template System
**Context:** Need to choose between external template engines (Jinja2, Mako) vs. simple string replacement.
**Selected:** String-based variable replacement (`{{var}}`)
**Rationale:**
1. **No dependencies:** Works with Python stdlib only
2. **Sufficient for MVP:** Current needs are simple variable substitution
3. **Easy to understand:** No complex template syntax to learn
4. **Fast to implement:** `str.replace()` is all that's needed
5. **Future path:** Can upgrade to Jinja2 if conditionals/loops needed

**Reversibility:** HIGH - Can replace template engine without changing API surface. Template format (`{{var}}`) is compatible with Jinja2.

---

## D2: String-Based Docstring Extraction
**Context:** Regex pattern `r'^[^"\n]*"""(.+?)"""'` failed to match module docstrings due to shebang line.
**Selected:** String-based approach using `content.find('"""')`
**Rationale:**
1. **Simpler:** No complex regex patterns
2. **Handles edge cases:** Works with shebang, comments before docstring
3. **Reliable:** String find is deterministic
4. **Fast:** O(n) string search

**Reversibility:** LOW - Changing extraction logic affects all parsing. However, function signature remains same, so impact is isolated to parser internals.

---

## D3: Non-Blocking Integration
**Context:** Documentation generation could fail (parser error, template error, file permissions). Should this prevent task completion?
**Selected:** Non-blocking integration with error suppression
**Rationale:**
1. **Documentation is nice-to-have:** Not critical for system operation
2. **Prevents delays:** Doc generation failures don't block task completion
3. **Graceful degradation:** System continues without docs if generation fails
4. **Manual fallback:** Can generate docs manually if auto-generation fails

**Implementation:**
```bash
python3 doc_generator.py feature "[TASK-ID]" 2>&1 || echo "Doc generation skipped (non-fatal)"
```

**Reversibility:** LOW - Changing to blocking would slow down task completion for every task. Non-blocking is the right choice for documentation.

---

## D4: Regex for Function Extraction
**Context:** Need to extract function definitions and docstrings from Python code. Multiple approaches: regex, AST parsing, external libraries.
**Selected:** Regex `def\s+(\w+)\s*\(([\s\S]*?)\)\s*:`
**Rationale:**
1. **Handles multi-line args:** `[\s\S]*?` matches newlines
2. **Simple to implement:** Single regex pattern
3. **No dependencies:** Works with Python stdlib `re`
4. **Good enough for MVP:** Covers most common function definitions

**Known Limitations:**
- May not handle decorators correctly
- May fail on nested parentheses in default arguments
- May extract function-like strings (comments, strings)

**Reversibility:** HIGH - Can improve regex or switch to AST parsing without changing API surface. `parse_code_files()` interface remains stable.

---

## D5: Template Location
**Context:** Templates could be stored in project memory (`5-project-memory/blackbox5/.templates/docs/`) or shared location (`/workspaces/blackbox5/.templates/docs/`).
**Selected:** Shared location at `/workspaces/blackbox5/.templates/docs/`
**Rationale:**
1. **Accessible to all agents:** Planner, executor, and future agents can use templates
2. **Separation of concerns:** Templates not tied to project memory structure
3. **Standard location:** `/workspaces/blackbox5/` is root for shared resources
4. **Easier path:** Shorter absolute paths in code

**Reversibility:** MEDIUM - Changing requires updating `DEFAULT_TEMPLATES_DIR` in generator. However, path is configurable via function parameter.

---

## D6: Output Directory Structure
**Context:** Generated documentation could be stored in multiple locations: project docs (`plans/features/docs/`), run directories, or separate output dir.
**Selected:** `plans/features/docs/` for generated documentation
**Rationale:**
1. **Logical grouping:** Feature docs belong with feature specifications
2. **Discoverable:** Users expect docs in `plans/features/`
3. **Git-tracked:** Generated docs are committed alongside feature specs
4. **GitHub compatible:** Renders properly in repository

**Reversibility:** MEDIUM - Changing requires updating `DEFAULT_OUTPUT_DIR` in generator. Path is configurable via function parameter.

---

## D7: Skill Selection Decision (Phase 1.5)
**Context:** Task matched "Implementation" domain (bmad-dev skill) with 53% confidence.
**Selected:** No skill invocation (standard execution)
**Rationale:**
1. **Below threshold:** 53% < 70% confidence threshold
2. **Detailed approach:** Task file provided step-by-step implementation plan
3. **Marginal value:** bmad-dev skill would add minimal value over following task instructions
4. **Skill is documentation-based:** Not executable, principles applied manually

**Confidence Calculation:**
- Keyword match: 35% (implement, create, write keywords present)
- Task type alignment: 90% (clearly an implementation task)
- Complexity fit: 60% (moderate complexity, multiple components)
- Historical success: 0% (no prior data)
- **Total: 53%**

**Reversibility:** N/A - This was an evaluation decision, not a technical implementation choice.
