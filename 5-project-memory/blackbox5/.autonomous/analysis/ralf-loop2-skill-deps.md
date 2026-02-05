# RALF Loop 2 Analysis: Skill System Dependencies

## Executive Summary

RALF has **deep, hardcoded dependencies** on BlackBox5's skill system structure that Loop 1 completely missed. The skill system is not merely configured by BlackBox5—it is **embedded throughout RALF's improvement loop agents**.

## Critical Findings

### 1. Hardcoded Skill File Paths (8 files affected)

| File | Lines | Hardcoded Path |
|------|-------|----------------|
| `scout-intelligent.py` | 44-46 | `{project_dir}/operations/skill-*.yaml` |
| `scout-task-based.py` | 37-39 | `operations/skill-*.yaml` |
| `scout-analyze.py` | 77 | `operations/skill-metrics.yaml` |
| `executor-implement.py` | 99, 212 | `operations/skill-selection.yaml` |
| `verifier-validate.py` | 72 | `operations/skill-selection.yaml` |
| `collect-skill-metrics.py` | 11, 17 | Absolute path to `skill-metrics.yaml` |
| `log-skill-usage.py` | 28 | Absolute path to `skill-usage.yaml` |
| `validate-skill-usage.py` | 31-34 | Hardcoded `PROJECT_ROOT`, `OPERATIONS_DIR` |

### 2. YAML Structure Assumptions

**skill-selection.yaml structure expected:**
```yaml
auto_trigger_rules:
  - rule_id: "ATR-001"
    name: "Implementation Tasks"
    condition: "Task contains 'implement' + domain keyword"
    keywords: ["implement", "create", "build", "develop"]

domain_mapping:
  - domain: "Product Management"
    keywords: ["PRD", "requirements"]
    primary_skill: bmad-pm
    confidence_threshold: 70
```

**verifier-validate.py lines 198-206** validates specific sections:
- `auto_trigger_rules`
- `domain_mapping`
- `selection_process`
- `confidence_calculation`

### 3. Task ID Hardcoding

**executor-implement.py lines 286-293:**
```python
if task_id == "TASK-SKIL-005" or "threshold" in task.get("action", "").lower():
    return self.execute_threshold_fix(task)
elif task_id == "TASK-SKIL-008" or "standardize" in task.get("action", "").lower():
    return self.execute_standardize_thresholds(task)
```

These task IDs are BB5-specific conventions.

### 4. Absolute Path Critical Bug

**collect-skill-metrics.py line 11:**
```python
metrics_path = Path('/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/operations/skill-metrics.yaml')
```

**This is an absolute hardcoded path that will fail on any other system!**

### 5. What Happens Without Skill System

| Component | Failure Mode |
|-----------|--------------|
| Scout agents | Fail - expect skill YAML files |
| Executor | Crash - no existence check before opening files |
| Verifier | Fail - no fallback if files missing |
| Metrics collection | Fail - absolute path won't exist |

## Decoupling Recommendations

### Immediate (High Priority)
1. **Extract skill configuration interface** - Create `SkillConfigProvider` abstract class
2. **Move skill registry to RALF** - Make `skill-registry.yaml` in 2-engine the canonical source
3. **Parameterize all file paths** - Use environment variables or config injection

### Medium Priority
4. **Create skill metrics API** - Define interface, let BB5 provide implementation
5. **Decouple task execution** - Remove hardcoded task IDs, use capability-based execution
6. **Skill validation abstraction** - Validate against interface, not specific YAML

### Long Term
7. **Skill system as plugin** - Make it optional, projects can enable/disable
8. **Configuration schema versioning** - Version YAML schemas, check compatibility

## Summary Table: What Loop 1 Missed

| Issue | Severity | Files Affected |
|-------|----------|----------------|
| Hardcoded skill file paths | CRITICAL | 8 files |
| YAML structure assumptions | HIGH | 6 files |
| Task ID hardcoding | MEDIUM | executor-implement.py |
| Absolute path in collect-skill-metrics.py | CRITICAL | collect-skill-metrics.py |
| Skill selection framework validation | HIGH | verifier-validate.py |
| Scout analyzer prompts reference BB5 | MEDIUM | scout-intelligent.py, scout-task-based.py |
| Metrics calculation tied to BB5 schema | HIGH | calculate-skill-metrics.py |

## Bottom Line

**RALF cannot function without BlackBox5's skill system.** The coupling is structural, not just configurational. This is a fundamental architectural dependency.
