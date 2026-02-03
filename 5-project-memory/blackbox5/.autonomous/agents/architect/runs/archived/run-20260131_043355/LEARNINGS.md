# TASK-1769808835: Learnings

## What Was Learned

1. **Directory names matter**: Python can't import packages with hyphens in names (e.g., `2-engine` becomes problematic for `import` statements)

2. **`__init__.py` is critical**: Without these files, Python doesn't recognize directories as packages, causing relative imports to fail

3. **The error message was misleading**: "ImportError: attempted relative import beyond top-level package" suggested the imports were wrong, but the real issue was missing package markers

4. **The codebase already has workarounds**: Many demo files use `sys.path` manipulation to work around this issue, which suggests this has been a known problem

## Recommendations

1. Consider renaming `2-engine` to `engine` or `two_engine` for better Python compatibility
2. Add a linter rule to check for missing `__init__.py` files in new directories
3. Consider using `py.typed` files for type hints in the future
