# TASK-RALF-001: Extract Hardcoded Paths from RALF Agent Scripts

**Status:** completed
**Priority:** CRITICAL
**Parent:** Issue #4 - RALF Knows Project Structure
**Completed:** 2026-02-08

## Objective
Remove all hardcoded paths from the 6 RALF agent scripts and replace with configuration.

## Files Modified

All 6 scripts now use environment variables with fallback to default paths:

1. **scout-intelligent.py** - Uses `PathResolver` from lib/paths (already supported env vars via BB5_PROJECT, BLACKBOX5_HOME)
2. **scout-task-based.py** - Uses `RALF_ENGINE_DIR` env var with fallback (line 24)
3. **planner-prioritize.py** - Uses `PathResolver` from lib/paths (already supported env vars)
4. **executor-implement.py** - Uses `validate_ralf_paths()` which checks `RALF_PROJECT_DIR` and `RALF_ENGINE_DIR` env vars
5. **verifier-validate.py** - Uses `RALF_ENGINE_DIR` env var with fallback (line 25), fixed hardcoded path at line 30
6. **improvement-loop.py** - Uses `PathResolver` from lib/paths (already supported env vars)

## Changes Made

### 1. verifier-validate.py - Fixed Hardcoded Path
```python
# Before (line 30):
_project_lib = Path.home() / '.blackbox5' / '5-project-memory' / 'blackbox5' / '.autonomous' / 'lib'

# After:
_project_lib = get_ralf_project_dir() / '.autonomous' / 'lib'
```

### 2. Created Configuration Files

**~/.blackbox5/.ralf/config.yaml**
- Documents all RALF configuration options
- Shows default paths and environment variable names
- Provides usage examples

**~/.blackbox5/.ralf/.env.example**
- Shell environment variable template
- Lists all supported environment variables:
  - `RALF_PROJECT_DIR` - Project directory path
  - `RALF_ENGINE_DIR` - Engine directory path
  - `RALF_PROJECT_NAME` - Project name
  - `BLACKBOX5_HOME` - BB5 root directory
  - Legacy: `BB5_PROJECT_ROOT`, `BB5_ENGINE_ROOT`, `BB5_HOME`, `BB5_PROJECT`

## Environment Variable Support

The `paths.py` library supports these environment variables:

| Variable | Purpose | Fallback |
|----------|---------|----------|
| `RALF_PROJECT_DIR` | Project directory | `~/.blackbox5/5-project-memory/{project}` |
| `RALF_ENGINE_DIR` | Engine directory | `~/.blackbox5/2-engine` |
| `RALF_PROJECT_NAME` | Default project name | `blackbox5` |
| `BLACKBOX5_HOME` | BB5 root directory | `~/.blackbox5` |
| `BB5_PROJECT_ROOT` | Alternative project path | Same as RALF_PROJECT_DIR |
| `BB5_ENGINE_ROOT` | Alternative engine path | Same as RALF_ENGINE_DIR |

## Success Criteria

- [x] All 6 scripts use environment variables for paths
- [x] Scripts fall back to current hardcoded paths (backward compatibility)
- [x] Scripts validate paths exist on startup (via `validate_ralf_paths()`)
- [x] Scripts provide helpful error messages if paths invalid
- [x] Create `.env.example` documenting required variables

## Testing

Verified path resolution works correctly:
```bash
# Default paths (no env vars)
python3 -c "from paths import get_ralf_project_dir; print(get_ralf_project_dir())"
# Output: /Users/shaansisodia/.blackbox5/5-project-memory/blackbox5

# With custom paths
export RALF_PROJECT_DIR=/tmp/my-project
python3 -c "from paths import get_ralf_project_dir; print(get_ralf_project_dir())"
# Output: /tmp/my-project
```

## Rollback Strategy

If issues arise, revert the single change in verifier-validate.py (line 30) or use the original hardcoded paths by not setting environment variables.

## Files Created

- `/Users/shaansisodia/.blackbox5/.ralf/config.yaml` - YAML configuration template
- `/Users/shaansisodia/.blackbox5/.ralf/.env.example` - Shell environment template

## Files Modified

- `/Users/shaansisodia/.blackbox5/5-project-memory/blackbox5/.autonomous/bin/verifier-validate.py` - Fixed hardcoded path at line 30
