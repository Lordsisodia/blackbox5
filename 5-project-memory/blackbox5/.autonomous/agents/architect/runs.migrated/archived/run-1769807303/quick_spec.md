# TASK-1769807450: Quick Spec

## Goal
Fix import path errors throughout the codebase that prevent modules from being found and imported correctly.

## Files to Modify

### 1. `/Users/shaansisodia/.blackbox5/2-engine/core/interface/api/server.py`
**Issue:** Imports from non-existent `infrastructure` module
- `from infrastructure.kernel import kernel, SystemStatus, RunLevel`
- `from infrastructure.config import ConfigManager`
- `from infrastructure.health import HealthMonitor`
- `from infrastructure.registry import ServiceRegistry`
- `from infrastructure.lifecycle import LifecycleManager`
- `from infrastructure.boot_enhanced import initialize_core_systems, start_engine`
- `from core.boot_enhanced import shutdown_engine` (line 84)

**Action Needed:** Either:
- Option A: Create stub/no-op implementations of missing modules
- Option B: Comment out non-functional API server code
- Option C: Update imports to use existing modules

### 2. `/Users/shaansisodia/.blackbox5/2-engine/tools/integrations/_template/config.py`
**Issue:** Template file with invalid Python syntax (template placeholders not escaped)
- Line 14: `class {ServiceName}Config:` - invalid syntax

**Action Needed:**
- This is a template file that should be processed, not executed
- Add `.py.template` extension or move to templates directory
- Or use proper template syntax (e.g., `{{ ServiceName }}` for Jinja2)

## Tests Needed
1. Verify `server.py` can be imported without errors
2. Verify template files are not executed as Python
3. Check for other files with similar import issues

## Risk Assessment
- **Low Risk:** Template file issue (just rename/move)
- **Medium Risk:** server.py imports (affects API server functionality)

## Rollback Strategy
- Git revert if API server becomes non-functional
- Template file change is trivial to reverse

## Approach
1. Fix template file issue (rename)
2. Comment out or stub missing infrastructure imports in server.py
3. Test imports work
4. Commit changes
