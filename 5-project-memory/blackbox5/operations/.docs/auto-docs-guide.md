# Automated Documentation Generator - User Guide

**Feature:** F-005 Automated Documentation Generator
**Version:** 1.0.0
**Status:** Operational

---

## Overview

The Automated Documentation Generator (F-005) automatically generates and maintains documentation from code, task completions, and system activity. This eliminates manual documentation overhead and ensures documentation stays in sync with system evolution.

### What It Does

- **Feature Documentation:** Auto-generates feature docs from task completion output (RESULTS.md, THOUGHTS.md, DECISIONS.md)
- **API Documentation:** Extracts docstrings from Python code to create API documentation
- **README Updates:** Updates README with recent activity summary

### Benefits

- **Zero Manual Effort:** Documentation generated automatically from existing sources
- **Always Current:** Docs stay in sync with code and task completions
- **Consistent Format:** Template-based generation ensures consistent documentation structure
- **GitHub Compatible:** Markdown output renders properly on GitHub

---

## Architecture

### Components

1. **Documentation Parser** (`doc_parser.py`)
   - Parses task completion output (RESULTS.md, THOUGHTS.md, DECISIONS.md)
   - Extracts docstrings and comments from Python code
   - Extracts metadata from run directories

2. **Documentation Generator** (`doc_generator.py`)
   - Fills templates with parsed data
   - Generates feature documentation
   - Generates API documentation
   - Updates README with recent activity

3. **Template System** (`.templates/docs/`)
   - `feature-doc.md.template` - Feature documentation template
   - `api-doc.md.template` - API documentation template
   - `readme-update.md.template` - README update template

### Data Flow

```
Task Completion → RESULTS.md + THOUGHTS.md + DECISIONS.md
                                    ↓
                            doc_parser.py (extract key sections)
                                    ↓
                            doc_generator.py (fill templates)
                                    ↓
                    Feature Doc + API Doc + README Update
```

---

## Usage

### Automatic Generation (Recommended)

Documentation is automatically generated on task completion via the RALF-Executor integration.

**Workflow:**
1. Complete a task (executor writes RESULTS.md, THOUGHTS.md, DECISIONS.md)
2. Executor calls `doc_generator.py feature [TASK-ID]`
3. Feature documentation generated at `plans/features/docs/[FEATURE-ID].md`
4. Task committed to git with documentation included

**No manual intervention required.**

### Manual Generation

You can also generate documentation manually using the CLI.

#### Generate Feature Documentation

```bash
export PYTHONPATH="/workspaces/blackbox5/2-engine/.autonomous/lib:$PYTHONPATH"
python3 /workspaces/blackbox5/2-engine/.autonomous/lib/doc_generator.py feature TASK-1769916007
```

**Output:** `plans/features/docs/F-001.md`

#### Generate API Documentation

```bash
export PYTHONPATH="/workspaces/blackbox5/2-engine/.autonomous/lib:$PYTHONPATH"
python3 /workspaces/blackbox5/2-engine/.autonomous/lib/doc_generator.py api \
  /workspaces/blackbox5/2-engine/.autonomous/lib/agent_discovery.py \
  /workspaces/blackbox5/2-engine/.autonomous/lib/task_distribution.py
```

**Output:** `plans/features/docs/api-docs.md`

#### Update README with Recent Activity

```bash
export PYTHONPATH="/workspaces/blackbox5/2-engine/.autonomous/lib:$PYTHONPATH"
python3 /workspaces/blackbox5/2-engine/.autonomous/lib/doc_generator.py readme 7
```

**Parameters:**
- `7` - Number of days to include in activity summary (default: 7)

**Output:** Updates `README.md` with "Recent Activity" section

---

## Configuration

### Template Customization

Templates are stored in `/workspaces/blackbox5/.templates/docs/`:

1. **Feature Doc Template** (`feature-doc.md.template`)
   - Variables: `{{task_id}}`, `{{title}}`, `{{status}}`, `{{what_was_done}}`, `{{files_modified}}`, `{{impact_*}}`, `{{decisions}}`
   - Customize to change feature documentation format

2. **API Doc Template** (`api-doc.md.template`)
   - Variables: `{{api_content}}`
   - Customize to change API documentation format

3. **README Update Template** (`readme-update.md.template`)
   - Variables: `{{tasks}}`
   - Customize to change README update format

### Output Directory

Generated documentation is stored at:
- `plans/features/docs/` - Feature documentation and API docs

To change the output directory, modify `DEFAULT_OUTPUT_DIR` in `doc_generator.py`.

---

## Troubleshooting

### Common Issues

#### Issue: "ModuleNotFoundError: No module named 'yaml'"

**Solution:** The parser requires PyYAML. Install it:
```bash
pip install pyyaml
```

#### Issue: "Task output not found for TASK-XXX"

**Cause:** Task run directory not found or RESULTS.md missing.

**Solution:**
1. Verify task ID is correct
2. Check that task was completed (run directory exists)
3. Verify RESULTS.md exists in run directory

#### Issue: "No such file or directory: '.templates/docs/feature-doc.md.template'"

**Cause:** Templates not found at expected path.

**Solution:**
- Templates are at `/workspaces/blackbox5/.templates/docs/`
- Update `DEFAULT_TEMPLATES_DIR` in `doc_generator.py` if moved

#### Issue: Generated documentation is empty or incomplete

**Cause:** Parser regex patterns didn't match source format.

**Solution:**
1. Check source file format (RESULTS.md, code files)
2. For code: Ensure docstrings use `"""triple quotes"""`
3. For tasks: Ensure RESULTS.md follows expected format
4. Check parser error output for specific issues

#### Issue: Doc generation fails silently

**Cause:** Error in doc generation, but executor continues (non-blocking).

**Solution:**
1. Check executor run logs for error messages
2. Test doc generation manually (see Manual Generation above)
3. Verify PYTHONPATH includes `2-engine/.autonomous/lib`

---

## Examples

### Example 1: Feature Documentation

**Input:** Task completion output (RESULTS.md)

```markdown
# Results - TASK-1769916007

**Task:** TASK-1769916007: Implement Feature F-001
**Status:** completed

## What Was Done
Implemented the Multi-Agent Coordination System...
```

**Output:** Feature documentation

```markdown
# Feature Documentation: TASK-1769916007: Implement Feature F-001

**Task ID:** TASK-1769916007
**Status:** completed

## Summary
Implemented the Multi-Agent Coordination System...
```

### Example 2: API Documentation

**Input:** Python code with docstrings

```python
"""
Agent Discovery Service for RALF Multi-Agent Coordination

This module provides functionality to discover active RALF agents...
"""

def discover_agents(heartbeat_file: str = DEFAULT_HEARTBEAT_FILE) -> List[AgentInfo]:
    """
    Discover all active RALF agents from heartbeat.yaml.

    Args:
        heartbeat_file: Path to heartbeat.yaml file

    Returns:
        List of AgentInfo objects for active agents
    """
```

**Output:** API documentation

```markdown
# API Documentation

## /workspaces/blackbox5/2-engine/.autonomous/lib/agent_discovery.py

Agent Discovery Service for RALF Multi-Agent Coordination
This module provides functionality to discover active RALF agents...

### Functions

#### discover_agents(heartbeat_file: str = DEFAULT_HEARTBEAT_FILE)

Discover all active RALF agents from heartbeat.yaml.

Args:
    heartbeat_file: Path to heartbeat.yaml file

Returns:
    List of AgentInfo objects for active agents
```

---

## Advanced Usage

### Generate Documentation for Multiple Tasks

```bash
# Generate docs for last 3 completed tasks
for task_id in TASK-1769916007 TASK-1769916008 TASK-1769952151; do
    export PYTHONPATH="/workspaces/blackbox5/2-engine/.autonomous/lib:$PYTHONPATH"
    python3 /workspaces/blackbox5/2-engine/.autonomous/lib/doc_generator.py feature $task_id
done
```

### Generate API Docs for All Library Files

```bash
export PYTHONPATH="/workspaces/blackbox5/2-engine/.autonomous/lib:$PYTHONPATH"
python3 /workspaces/blackbox5/2-engine/.autonomous/lib/doc_generator.py api \
  /workspaces/blackbox5/2-engine/.autonomous/lib/*.py
```

### Custom Template Variables

Add custom variables to templates:

1. **Edit template** (e.g., `feature-doc.md.template`):
   ```markdown
   ## Custom Section
   {{custom_variable}}
   ```

2. **Update generator** (`doc_generator.py`):
   ```python
   content = content.replace("{{custom_variable}}", "custom value")
   ```

---

## Integration with RALF

### Executor Integration

The executor automatically generates documentation after task completion:

```bash
# From ralf-executor.md prompt
export PYTHONPATH="$RALF_ENGINE_DIR/lib:$PYTHONPATH"
python3 $RALF_ENGINE_DIR/lib/doc_generator.py feature "[TASK-ID]" 2>&1 || echo "Doc generation skipped (non-fatal)"
```

**Key Points:**
- Runs after queue sync, before git commit
- Non-blocking: Errors don't prevent task completion
- Async: Doesn't delay `<promise>COMPLETE</promise>` signal

### Planner Integration (Future)

The planner can trigger documentation generation:
- Daily README updates with recent activity
- API docs regeneration after code changes
- Feature docs for completed features

---

## Limitations

### Known Limitations

1. **Function Extraction:** Regex-based function extraction may not handle all Python syntax variations
   - **Impact:** Some functions may be missing from API docs
   - **Mitigation:** Use standard docstring format (`"""triple quotes"""`)

2. **Template Simplicity:** Current template system uses simple variable replacement
   - **Impact:** Cannot do conditional formatting or loops
   - **Mitigation:** Use Jinja2 templates for advanced needs (future enhancement)

3. **No Incremental Updates:** Full regeneration on each run
   - **Impact:** Slower for large codebases
   - **Mitigation:** Only regenerate changed files (future enhancement)

4. **Markdown Only:** Output is markdown only
   - **Impact:** Cannot generate HTML, PDF, etc.
   - **Mitigation:** Use markdown converters (pandoc, markdown-pdf) for other formats

---

## Future Enhancements

### Planned Improvements

1. **Jinja2 Templates:** More powerful templating with conditionals, loops, filters
2. **Incremental Updates:** Only regenerate changed documentation
3. **Multi-Format Output:** HTML, PDF, LaTeX generation
4. **Documentation Quality Scoring:** Auto-grade documentation completeness
5. **Diagram Generation:** Generate architecture diagrams from code structure
6. **Meta-Docs:** Self-documenting documentation system

---

## Related Documentation

- `plans/features/FEATURE-005-automated-documentation.md` - Feature specification
- `operations/.docs/feature-delivery-guide.md` - Feature delivery process
- `2-engine/.autonomous/lib/doc_parser.py` - Parser implementation
- `2-engine/.autonomous/lib/doc_generator.py` - Generator implementation

---

## Support

For issues or questions:
1. Check this guide's Troubleshooting section
2. Review parser/generator error output
3. Check template syntax
4. Verify source file format

**End of Guide**
