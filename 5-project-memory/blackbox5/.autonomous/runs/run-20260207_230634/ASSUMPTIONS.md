# Assumptions: TASK-SSOT-025

## Technical Assumptions

1. **skill-usage.yaml format is stable** - The file structure with `usage_log`, `skills`, and `metadata` sections is the canonical format.

2. **Single project (blackbox5)** - The SkillRepository uses project_name="blackbox5" as default, matching the existing hardcoded path.

3. **YAML is the storage format** - No SQLite backend for skill data; YAML files are the source of truth.

4. **UTC timestamps** - All timestamps stored in ISO 8601 format with UTC timezone.

5. **Concurrent access is possible** - Multiple agents may write to skill-usage.yaml simultaneously, requiring atomic writes.

## Migration Assumptions

1. **Backward compatibility required** - Other scripts may depend on the existing function signatures in log-skill-usage.py.

2. **Gradual migration acceptable** - Not all 35+ files need to be migrated in one session; incremental progress is valuable.

3. **Test data is safe to create** - Running the test with THOUGHTS.md creates real data in skill-usage.yaml, which is acceptable.

## Risk Assumptions

1. **Low risk for log-skill-usage.py** - This script is a utility/logger, not in the critical path of task execution.

2. **skill-usage.yaml can be regenerated** - If corruption occurs, the file can be rebuilt from run THOUGHTS.md files.
