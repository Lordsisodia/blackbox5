# Decisions - TASK-1769958230

## Decision 1: Modular Architecture with Independent Analyzers

**Context:** The code review system needs to support multiple types of analysis (static, security, complexity) with the ability to add more in the future.

**Selected:** Modular architecture with independent analyzer modules

**Rationale:**
- **Separation of Concerns:** Each analyzer focuses on one type of analysis
- **Independent Testing:** Each module can be tested standalone
- **Easy Extension:** New analyzers can be added without modifying existing code
- **Graceful Degradation:** If one analyzer fails, others still work
- **Parallel Execution:** Independent analyzers can run in parallel (future enhancement)

**Alternatives Considered:**
1. **Monolithic Design:** All analysis in one file
   - Rejected: Hard to maintain, difficult to extend, single point of failure

2. **Plugin System:** Dynamically loaded analyzers
   - Rejected: Over-engineering for current needs, adds complexity

**Reversibility:** LOW - Changing architecture would require significant refactoring

**Impact:**
- Positive: Improved maintainability, extensibility, testability
- Negative: Slightly more complex file structure (6 files vs 1-2)

---

## Decision 2: Graceful Degradation for Missing Tools

**Context:** Not all systems have pylint, flake8, bandit installed. Users may not want to install all tools.

**Selected:** Check tool availability and skip if missing

**Rationale:**
- **Partial Value:** System still provides value with available tools
- **No Blocking:** Users can start using immediately without installing all tools
- **Flexibility:** Users can choose which tools to install
- **Better UX:** Clear warnings instead of cryptic errors

**Implementation:**
```python
def _check_tool_available(self, tool_name: str) -> bool:
    """Check if tool is available."""
    try:
        result = subprocess.run([tool_name, "--version"], ...)
        return result.returncode == 0
    except Exception:
        return False
```

**Alternatives Considered:**
1. **Fail Fast:** Raise error if tool missing
   - Rejected: Blocks usage, poor UX

2. **Auto-Install:** Automatically pip install missing tools
   - Rejected: Security risk, unexpected behavior, permission issues

**Reversibility:** LOW - Easy to change to fail-fast if needed

**Impact:**
- Positive: Better UX, partial functionality
- Negative: Users may not realize they're missing analysis

---

## Decision 3: YAML Configuration with Sensible Defaults

**Context:** Code review needs to be configurable for different projects, but should work out-of-the-box.

**Selected:** YAML configuration with comprehensive defaults

**Rationale:**
- **Human-Readable:** YAML is easy to edit and understand
- **Consistent:** Follows F-006 (ConfigManagerV2) pattern
- **Flexible:** Supports environment-specific overrides
- **Zero Config:** Sensible defaults work for most projects

**Configuration Structure:**
```yaml
static_analysis:
  enabled: true
  tools: [pylint, flake8]
  severity_threshold: warning

security_scan:
  enabled: true
  tools: [bandit]
  severity_threshold: error
```

**Alternatives Considered:**
1. **Environment Variables:** Use env vars for configuration
   - Rejected: Hard to manage complex configs, not human-readable

2. **Code-Based Config:** Python config files
   - Rejected: Less flexible, requires code changes

3. **JSON Configuration:** Use JSON instead of YAML
   - Rejected: Less readable, no comments

**Reversibility:** MEDIUM - Can switch to other formats, but YAML is optimal

**Impact:**
- Positive: Easy to configure, consistent with existing patterns
- Negative: One more config file to manage

---

## Decision 4: Multi-Format Reports (Markdown, JSON, YAML)

**Context:** Different stakeholders need different formats - developers want readable reports, CI/CD needs machine-readable data.

**Selected:** Generate all three formats by default

**Rationale:**
- **Human-Readable:** Markdown for developers, code review comments
- **Machine-Readable:** JSON for automation, APIs, custom analysis
- **Configuration:** YAML for config file generation
- **No Trade-Offs:** Generate all formats, let user choose

**Implementation:**
```python
def generate_all_formats(results, output_dir):
    formats = config.get("formats", ["markdown", "json", "yaml"])
    # Generate each requested format
```

**Alternatives Considered:**
1. **Single Format:** Generate only one format (e.g., JSON)
   - Rejected: Not human-readable, poor UX for developers

2. **User Choice:** Require user to specify format each time
   - Rejected: Extra friction, most users want all formats

**Reversibility:** LOW - Easy to add/remove formats

**Impact:**
- Positive: Flexibility for all use cases
- Negative: Slightly more code (3 report generators vs 1)

---

## Decision 5: Pre-Commit Hook with Optional Blocking

**Context:** Code review should run automatically, but shouldn't block all commits if users need to bypass.

**Selected:** Install pre-commit hook with quality gate blocking, but allow bypass via --no-verify

**Rationale:**
- **Automation:** Runs automatically on every commit
- **Quality Enforcement:** Blocks commits with critical issues
- **Flexibility:** Users can bypass if needed (rare cases)
- **Git Native:** Uses standard git hook mechanism

**Implementation:**
```python
def run_pre_commit(self):
    results = engine.run_review(".", changed_only=True)
    if self._should_block_commit(results):
        return False  # Block commit
    return True  # Allow commit
```

**Bypass:**
```bash
git commit --no-verify -m "Message"
```

**Alternatives Considered:**
1. **No Blocking:** Run review but never block commits
   - Rejected: Defeats purpose of quality gates

2. **Always Blocking:** No way to bypass
   - Rejected: Too restrictive, emergency situations

3. **CI/CD Only:** Only run in CI, not locally
   - Rejected: Slower feedback loop, wastes CI resources

**Reversibility:** LOW - Hook can be uninstalled or disabled in config

**Impact:**
- Positive: Automated quality enforcement
- Negative: One more thing developers need to know about

---

## Decision 6: Secret Detection with False Positive Filtering

**Context:** Security scanning should detect hardcoded secrets, but has high false positive rate (examples, placeholders).

**Selected:** Pattern-based secret detection with false positive filtering

**Rationale:**
- **Security Critical:** Hardcoded secrets are major security risk
- **High Value:** Catches secrets before they reach production
- **False Positive Management:** Filtering reduces noise
- **Configurable:** Users can add their own patterns

**Implementation:**
```python
SECRET_PATTERNS = {
    "AWS Access Key": r'AKIA[0-9A-Z]{16}',
    "API Key": r'(?i)api[_-]?key["\']?\s*[:=]\s*["\']?[A-Za-z0-9+/=]{20,}',
    # ... more patterns
}

def _is_false_positive(self, line):
    false_positive_patterns = [
        r'example', r'dummy', r'test', r'xxx',
        r'placeholder', r'your[_-]?key'
    ]
```

**Alternatives Considered:**
1. **No Secret Detection:** Only use bandit for security
   - Rejected: bandit doesn't catch all secret types

2. **No False Positive Filtering:** Flag everything
   - Rejected: Too much noise, users will ignore

**Reversibility:** LOW - Can be disabled in config

**Impact:**
- Positive: Catches secrets before they reach production
- Negative: May still have some false positives

---

## Decision 7: AST-Based Complexity Analysis (No External Tool)

**Context:** Need to measure cyclomatic complexity and function length. Tools like radon exist, but may not be installed.

**Selected:** Custom AST-based complexity calculation

**Rationale:**
- **No Dependency:** Uses Python stdlib (ast module)
- **Accurate:** Direct analysis of code structure
- **Extensible:** Easy to add custom metrics
- **Fast:** No subprocess overhead

**Implementation:**
```python
def _calculate_complexity(self, node: ast.AST) -> int:
    complexity = 1  # Base
    for child in ast.walk(node):
        if isinstance(child, (ast.If, ast.While, ast.For, ...)):
            complexity += 1
    return complexity
```

**Alternatives Considered:**
1. **Use radon:** Third-party tool for complexity
   - Rejected: Additional dependency, not always installed

2. **Simple Line Count:** Count lines per function
   - Rejected: Doesn't measure actual complexity

**Reversibility:** LOW - Can switch to radon if needed

**Impact:**
- Positive: No dependency, accurate metrics
- Negative: Custom code to maintain (but simple)

---

## Decision 8: Changed-Only Mode for Performance

**Context:** Large codebases take time to analyze. Most commits only change a few files.

**Selected:** Git integration to analyze only changed files

**Rationale:**
- **Performance:** 10-100x faster for typical commits
- **Relevant:** Only changed files matter for review
- **Git Native:** Uses standard git commands
- **Full Scan Option:** Still available when needed

**Implementation:**
```python
def _get_changed_files(self):
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD"],
        ...
    )
    return result.stdout.strip().split('\n')
```

**Alternatives Considered:**
1. **Always Scan All:** No changed-only mode
   - Rejected: Too slow for large codebases

2. **Timestamp-Based:** Use file modification times
   - Rejected: Less accurate, doesn't handle staged changes

**Reversibility:** LOW - Easy to disable or remove

**Impact:**
- Positive: Much faster for typical usage
- Negative: Misses issues in unchanged files (acceptable trade-off)

---

## Summary

All decisions prioritized:
- **Modularity** for maintainability
- **Graceful degradation** for usability
- **Flexibility** for different use cases
- **Performance** for practical usage

**Key Principles:**
1. Don't block users if tools missing
2. Provide value even with partial configuration
3. Support multiple workflows (local, CI/CD, pre-commit)
4. Make it easy to extend and customize

**Reversibility:** Most decisions are LOW to MEDIUM reversibility, meaning they could be changed if needed but would require some refactoring.

---

**End of Decisions Document**
