# Decisions - TASK-1769915000

## Decision 1: CI Enforcement Strategy

**Context:** Should shellcheck failures block CI or be warnings?

**Selected:** Block CI on shellcheck failures (`continue-on-error: false`)

**Rationale:**
- Shell script errors can cause production failures
- Low cost to fix (most warnings are simple quoting issues)
- High value to prevent (runtime errors are expensive)
- Establishes quality culture from the start
- All existing scripts fixed before enabling, so no CI failures

**Reversibility:** LOW
- Can change to `continue-on-error: true` if too disruptive
- Would require PR and discussion

---

## Decision 2: Shellcheck Version

**Context:** Which shellcheck version to use in CI?

**Selected:** Latest via `actions/setup-shellcheck@v2`

**Rationale:**
- GitHub action maintains latest stable version
- Automatic updates for bug fixes and new features
- No need to pin specific version
- Consistent with other GitHub Actions (checkout@v4, setup-python@v5)

**Reversibility:** LOW
- Can pin to specific version if needed: `shellcheck: stable` or `shellcheck: v0.9.0`
- Action supports version parameter

---

## Decision 3: Scope of Shellcheck Coverage

**Context:** Which shell scripts should be checked?

**Selected:** Explicitly check known scripts

**Rationale:**
- 5 known scripts in codebase
- Explicit list is clearer than glob patterns
- Avoids checking vendor/third-party scripts
- Easier to review and maintain
- Scripts covered:
  - bin/*.sh (3 scripts)
  - legacy-codespace-loop.sh (1 script)
  - 5-project-memory/blackbox5/.autonomous/ralf-daemon.sh (1 script)

**Alternatives Considered:**
- `find . -name "*.sh"` - Too broad, would check vendor scripts
- `find bin -name "*.sh"` - Would miss scripts outside bin/

**Reversibility:** LOW
- Easy to add more scripts to the list
- Can change to glob pattern if script count grows significantly

---

## Decision 4: Pre-Commit Hook

**Context:** Should pre-commit hook be required or optional?

**Selected:** Optional (documented but not enforced)

**Rationale:**
- CI already enforces shellcheck
- Pre-commit hooks can be bypassed
- Some contributors prefer CI feedback
- Documentation includes example for those who want it
- Avoids forcing local configuration on contributors

**Reversibility:** LOW
- Can add to template later if needed
- Individual contributors can install locally

---

## Decision 5: Documentation Detail Level

**Context:** How comprehensive should the shell script standards document be?

**Selected:** Comprehensive (250+ lines)

**Rationale:**
- Shell scripting has many pitfalls
- Contributors may not be shell experts
- Examples prevent confusion
- Covers all warnings found in codebase
- Includes script structure template
- Serves as reference for future development

**Sections Included:**
- Shellcheck integration (CI + local)
- 8 mandatory standards with examples
- 7 common shellcheck warnings with fixes
- Script structure template
- Testing checklist
- Resources and references

**Reversibility:** LOW
- Can add more sections as needed
- Content is additive, not breaking

---

## Decision 6: Fix Strategy

**Context:** Fix warnings before or after enabling CI?

**Selected:** Fix all warnings first, then enable CI

**Rationale:**
- Prevents CI failures on existing code
- Establishes clean baseline
- Demonstrates value before enforcement
- No disruption to existing workflows
- All scripts already pass, CI starts working immediately

**Process:**
1. Install shellcheck locally
2. Run on all scripts
3. Fix all 11 warnings
4. Verify zero warnings
5. Update CI workflow
6. Commit changes together

**Reversibility:** N/A
- This was a one-time setup decision
- Future changes follow CI enforcement

---

## Decision 7: Documentation Location

**Context:** Where to store shell script standards?

**Selected:** `operations/.docs/shell-script-standards.md`

**Rationale:**
- Consistent with other operational documentation
- `.docs/` directory pattern used elsewhere in project
- Easy to find and reference
- Separate from code (documentation)
- Can be linked from README or CONTRIBUTING.md

**Alternatives Considered:**
- `docs/` - Project uses `operations/.docs/` pattern
- `CONTRIBUTING.md` - Too long, would clutter guidelines
- Wiki - Not accessible in repo

**Reversibility:** LOW
- Can move file if directory structure changes
- Content remains valid regardless of location
