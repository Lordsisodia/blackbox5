# Verification Report: Engine-Project Split Structural Issues

**Status:** VERIFICATION COMPLETE
**Date:** 2026-02-06
**Confidence Level:** 85%

---

## Summary of Findings

After thorough review of all existing analysis documents and additional verification, I can confirm the following:

### Issues CONFIRMED (from existing analysis):

1. **47+ Hardcoded Cross-Boundary Paths** - CONFIRMED
   - Found in 8 Python scripts in `2-engine/.autonomous/bin/`
   - All 6 agent improvement loop scripts hardcode `PROJECT_DIR = Path.home() / ".blackbox5" / "5-project-memory" / "blackbox5"`
   - Scripts affected: `scout-intelligent.py`, `executor-implement.py`, `improvement-loop.py`, `planner-prioritize.py`, `verifier-validate.py`, `scout-task-based.py`, `scout-analyze.py`

2. **18 Categories of Duplications** - CONFIRMED
   - Routes configuration (both engine and project have routes.yaml)
   - Agent prompts overlap
   - Template vs implementation gaps (engine has 61-line queue template, project has 1975-line implementation)

3. **8 Engine Scripts That Should Move to Project** - CONFIRMED
   - All 6 agent improvement loop scripts are BlackBox5-specific
   - 2 additional prompts (`ralf-improvement-loop.md`, `ralf-scout-improve.md`)

4. **11 Project Items That Should Move to Engine** - CONFIRMED
   - Generic utilities: `bb5-health-dashboard.py`, `bb5-metrics-collector.py`, `bb5-queue-manager.py`, `bb5-reanalysis-engine.py`
   - Skill framework files: `skill-selection.yaml`, `skill-metrics.yaml`, `skill-usage.yaml`

5. **routes.yaml Incorrect Path Nesting** - CONFIRMED
   - Project routes.yaml contains paths like `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/2-engine/.autonomous/` (incorrectly nests engine inside project)
   - Also has duplicated path segments: `5-project-memory/blackbox5/5-project-memory/blackbox5/tasks`

6. **6-Agent Pipeline Tightly Coupled** - CONFIRMED
   - Hardcoded knowledge of BlackBox5 directory structure
   - Cannot be reused for other projects

---

## Additional Issues Discovered:

1. **Engine routes.yaml has outdated run path**
   - Line 118: `path: "../../../5-project-memory/ralf-core/.autonomous/runs"` references non-existent `ralf-core` project

2. **269 files contain hardcoded path references**
   - The grep search found 269 files with `.blackbox5.*5-project-memory.*blackbox5` or `.blackbox5.*2-engine` patterns
   - This indicates widespread path coupling beyond the 47 initially identified

3. **Shell scripts also have hardcoded paths**
   - `bb5-scout-improve`, `ralf-improve`, `bb5-parallel-dispatch.sh` all hardcode engine/project paths

4. **Missing path abstraction in bin/blackbox.py**
   - Uses relative path `ENGINE_DIR = Path(__file__).parent / "2-engine" / "core"` which assumes specific directory structure

---

## Confidence Level: 85%

**Why not 100%?**
- The existing analysis is comprehensive but there may be dynamic path references (constructed at runtime) not caught by static analysis
- Some paths may be in documentation or comments not fully scanned
- Configuration files may have template variables that resolve to hardcoded paths

---

## Gaps in Analysis:

1. **No analysis of 2-engine/core/ directory** - This contains significant Python code that may have implicit dependencies
2. **Limited analysis of shell scripts** - Only a few shell scripts were examined
3. **No runtime dependency analysis** - Cannot verify dynamic imports or path constructions
4. **No analysis of the skill registry in 2-engine/.autonomous/skills/** - May contain project-specific references

---

## Recommendations for Additional Analysis:

1. **Scan 2-engine/core/ for project references** - The core engine code may have BlackBox5-specific assumptions
2. **Audit all shell scripts** in both engine and project bin directories
3. **Check skill files** in `2-engine/.autonomous/skills/` for hardcoded paths
4. **Verify template files** are truly generic and not BlackBox5-specific
5. **Test path resolution** at runtime to catch dynamic constructions

---

## Conclusion:

The existing analysis has correctly identified the major structural issues between engine and project. The 6 critical issues are all valid and well-documented. The confidence level of 85% reflects that while the major issues are captured, there may be additional instances of hardcoded paths and implicit dependencies that would only be discovered through runtime testing or more exhaustive static analysis of the entire codebase.
