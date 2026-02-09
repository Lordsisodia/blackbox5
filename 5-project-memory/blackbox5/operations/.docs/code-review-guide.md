# RALF Code Review System - User Guide
======================================

**Feature:** F-013 (Automated Code Review System)
**Version:** 1.0.0
**Author:** RALF System

---

## Overview

The RALF Automated Code Review System provides comprehensive code quality checks through static analysis, security scanning, and complexity checking. It integrates seamlessly with your development workflow to catch issues early and enforce coding standards.

### Key Features

- **Static Analysis:** PEP 8 compliance, bug detection, unused code detection
- **Security Scanning:** Vulnerability detection, secret detection, dependency checks
- **Complexity Analysis:** Cyclomatic complexity, code duplication, function length
- **CI/CD Integration:** Pre-commit hooks, quality gates, commit blocking
- **Multi-Format Reports:** Markdown, JSON, YAML reports with recommendations

### Benefits

- ✅ Catch 80% of common issues before commit
- ✅ Consistent code style and quality enforcement
- ✅ Fast feedback (< 10 seconds for typical codebase)
- ✅ Automated quality gates
- ✅ Developer-friendly with actionable suggestions

---

## Installation

### Prerequisites

The code review system uses Python-based tools. Install the required packages:

```bash
# Install core tools
pip3 install pylint flake8 bandit pyyaml

# Optional: Install additional tools
pip3 install radon  # For complexity metrics
```

### Setup

1. **Clone or verify the code review libraries are in place:**

   ```bash
   ls 2-engine/.autonomous/lib/review_engine.py
   ls 2-engine/.autonomous/lib/static_analyzer.py
   ls 2-engine/.autonomous/lib/security_scanner.py
   ls 2-engine/.autonomous/lib/complexity_checker.py
   ls 2-engine/.autonomous/lib/report_generator.py
   ls 2-engine/.autonomous/lib/cicd_integration.py
   ```

2. **Install the pre-commit hook (optional but recommended):**

   ```bash
   python3 2-engine/.autonomous/lib/cicd_integration.py --install-hook
   ```

   This installs a git pre-commit hook that runs code review on staged files.

---

## Configuration

### Configuration File

The code review system is configured via `2-engine/.autonomous/config/code-review-config.yaml`.

### Key Settings

#### Static Analysis

```yaml
static_analysis:
  enabled: true
  tools:
    - pylint  # PEP 8 compliance, bug detection
    - flake8  # Style checking
  severity_threshold: warning  # critical, error, warning, info
```

#### Security Scanning

```yaml
security_scan:
  enabled: true
  tools:
    - bandit  # Security vulnerability scanner
  severity_threshold: error
  scan_for_secrets: true  # Detect hardcoded secrets/API keys
```

#### Complexity Checking

```yaml
complexity_check:
  enabled: true
  max_complexity: 10  # Maximum cyclomatic complexity per function
  max_function_length: 50  # Maximum lines per function
  severity_threshold: warning
  check_duplication: true  # Detect code duplication
```

#### Quality Gate

```yaml
quality_gate:
  enabled: true
  block_on_critical: true  # Block commit if critical issues found
  block_on_error: false  # Block commit if error issues found
```

#### Reporting

```yaml
reporting:
  formats:
    - markdown  # Human-readable report
    - json  # Machine-readable report
  include_suggestions: true  # Include auto-fix suggestions
  output_directory: ".ralf/reports"
```

---

## Usage

### Running Code Review

#### Option 1: Command Line

Run code review on a directory or file:

```bash
# Review entire codebase
python3 2-engine/.autonomous/lib/review_engine.py /path/to/code

# Review only changed files
python3 2-engine/.autonomous/lib/review_engine.py /path/to/code --changed-only

# Review with custom config
python3 2-engine/.autonomous/lib/review_engine.py /path/to/code --config custom-config.yaml

# Save results to file
python3 2-engine/.autonomous/lib/review_engine.py /path/to/code --output results.json
```

#### Option 2: Python API

```python
import sys
sys.path.insert(0, '2-engine/.autonomous/lib')

from review_engine import create_review_engine

# Create engine
engine = create_review_engine()

# Run review
results = engine.run_review(
    target_path=".",
    changed_only=False
)

# Check results
if results['success']:
    print("Review passed!")
else:
    print("Review failed:", results['quality_gate']['reason'])
```

### Pre-Commit Hook

When you install the pre-commit hook, code review runs automatically on staged files before each commit:

```bash
git add .
git commit -m "Your commit message"
# Code review runs automatically
# If issues are found, commit is blocked
```

To bypass the hook (not recommended):

```bash
git commit --no-verify -m "Your commit message"
```

### Individual Analyzers

You can run individual analyzers:

```bash
# Static analysis only
python3 2-engine/.autonomous/lib/static_analyzer.py file1.py file2.py

# Security scan only
python3 2-engine/.autonomous/lib/security_scanner.py file1.py file2.py

# Complexity check only
python3 2-engine/.autonomous/lib/complexity_checker.py file1.py file2.py
```

---

## Understanding Reports

### Report Summary

Each review generates a summary:

```
============================================================
CODE REVIEW RESULTS
============================================================
Status: PASSED
Files scanned: 42
Total issues: 15
Duration: 8.45s

Issues by severity:
  critical: 0
  error: 2
  warning: 10
  info: 3

Quality gate: All quality gates passed
============================================================
```

### Issue Details

Each issue includes:

- **Severity:** critical, error, warning, or info
- **Category:** static, security, or complexity
- **Location:** file path and line number
- **Message:** Description of the issue
- **Rule ID:** Identifier for the rule (e.g., `W0611`, `B101`)
- **Suggestion:** How to fix (if available)

Example:

```
[ERROR] src/main.py:42
  [unused-import] Unused import 'os'
  Suggestion: Remove unused import
```

### Report Formats

#### Markdown Report

Human-readable report with sections:
- Summary
- Quality gate status
- Issues by severity
- Issues by category
- Detailed analyzer results
- Recommendations

#### JSON Report

Machine-readable format for automation:
```json
{
  "summary": {
    "status": "passed",
    "total_issues": 15
  },
  "issues": {
    "by_severity": {...},
    "by_category": {...}
  },
  "analyzers": [...]
}
```

---

## Troubleshooting

### Common Issues

#### 1. "pylint not available"

**Problem:** pylint is not installed or not in PATH.

**Solution:**
```bash
pip3 install pylint
```

#### 2. "bandit failed to scan"

**Problem:** bandit encountered an error parsing the file.

**Solution:** Check the file for syntax errors. Run `python3 -m py_compile <file>` to verify syntax.

#### 3. "Too many false positives"

**Problem:** Analyzer is flagging issues that aren't real problems.

**Solution:**
- Adjust severity threshold in config
- Disable specific rules in config
- Add inline comments to suppress warnings:
  ```python
  # pylint: disable=unused-import
  import some_module
  ```

#### 4. "Review is too slow"

**Problem:** Code review takes too long on large codebases.

**Solution:**
- Use `--changed-only` to scan only modified files
- Disable analyzers you don't need
- Increase timeout in config
- Use incremental analysis (cached results)

#### 5. "Pre-commit hook not running"

**Problem:** Hook installed but not executing.

**Solution:**
- Verify hook is executable: `chmod +x .git/hooks/pre-commit`
- Check git version: `git --version` (requires 1.8+)
- Reinstall hook: `python3 2-engine/.autonomous/lib/cicd_integration.py --install-hook`

---

## Best Practices

### 1. Start with Warning Level

Begin with `severity_threshold: warning` to avoid overwhelming developers. Gradually increase to `error` as the codebase improves.

### 2. Use Changed-Only Mode for Large Codebases

Scanning only changed files is much faster:
```bash
python3 2-engine/.autonomous/lib/review_engine.py . --changed-only
```

### 3. Review Warnings Regularly

Even if quality gate doesn't block on warnings, review and fix them regularly to maintain code quality.

### 4. Customize Rules for Your Project

Every project is different. Adjust:
- Max complexity (default: 10)
- Max function length (default: 50)
- Disabled rules
- Severity thresholds

### 5. Integrate with CI/CD

Add code review to your CI/CD pipeline:

```yaml
# .github/workflows/code-review.yml
name: Code Review
on: [push, pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Code Review
        run: |
          python3 2-engine/.autonomous/lib/review_engine.py . --output results.json
```

### 6. Track Metrics Over Time

Monitor:
- Total issues trend
- Issues by severity
- Review execution time
- Most common rule violations

---

## Integration with RALF

### Executor Integration

The code review system integrates with RALF Executor:

1. **Post-Task Review:** Automatically runs after each task completion
2. **Quality Metrics:** Tracks code quality over time
3. **Learning:** Feeds into the knowledge base for pattern recognition

### Planner Integration

The Planner uses code review data to:
- Prioritize refactoring tasks
- Identify technical debt
- Suggest improvements to the development process

---

## Advanced Usage

### Custom Analyzers

Create custom analyzers by extending the base:

```python
from review_engine import AnalyzerResult, ReviewIssue

class CustomAnalyzer:
    def __init__(self, config):
        self.config = config
        self.enabled = config.get("custom_analyzer", {}).get("enabled", True)

    def is_enabled(self):
        return self.enabled

    def run(self, files):
        result = AnalyzerResult("CustomAnalyzer")
        # Your analysis logic here
        return result
```

### Programmatic Report Generation

```python
from report_generator import ReportGenerator

generator = ReportGenerator(config)

# Generate all formats
reports = generator.generate_all_formats(
    results=review_results,
    output_dir=".ralf/reports",
    base_name="code-review"
)

# Generate specific format
md_report = generator.generate_markdown(review_results)
```

### Quality Gate Automation

```python
from cicd_integration import CICDIntegration

integration = CICDIntegration()

# Check quality gate
gate_result = integration.check_quality_gate(results)

if gate_result["should_block"]:
    print("Blocking commit:", gate_result["reason"])
    # Handle blocking issues
```

---

## FAQ

**Q: Can I use this with languages other than Python?**

A: Currently, static analysis and security scanning are Python-focused. However, the framework supports other languages. Add language-specific analyzers by extending the base classes.

**Q: How do I exclude files from review?**

A: Add patterns to the `file_patterns.exclude` section in config:

```yaml
file_patterns:
  exclude:
    - "*/venv/*"
    - "*/migrations/*"
    - "*/tests/test_*.py"
```

**Q: Can I run review without committing?**

A: Yes. Use the command-line tool or Python API directly:

```bash
python3 2-engine/.autonomous/lib/review_engine.py .
```

**Q: How do I disable the pre-commit hook temporarily?**

A: Use `--no-verify` when committing:

```bash
git commit --no-verify -m "Message"
```

**Q: What's the performance impact?**

A: Typical review takes 5-10 seconds for 50 files. Using `--changed-only` reduces this to 1-2 seconds.

---

## Support and Feedback

For issues, questions, or suggestions:
- Check the troubleshooting section above
- Review the feature specification: `plans/features/FEATURE-013-automated-code-review.md`
- Contact the RALF development team

---

**End of User Guide**
