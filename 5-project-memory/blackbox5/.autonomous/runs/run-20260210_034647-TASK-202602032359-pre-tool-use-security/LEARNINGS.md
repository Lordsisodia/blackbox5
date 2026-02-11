# LEARNINGS

## What Was Learned

1. **Exit Code Semantics**: Exit code 2 is the standard for blocking in Claude Code hooks. It shows error to stderr and prevents tool execution.

2. **Pattern Matching**: Regular expressions with word boundaries (\b) are critical for preventing false positives (e.g., "unrm" should not match).

3. **Command Normalization**: Converting to lowercase and normalizing spaces before pattern matching catches variations like "rm -RF", "rm -F R", etc.

4. **Dangerous Paths**: Simply blocking rm -rf is insufficient. Systems may reference /, ~, $HOME, .. which are just as dangerous.

5. **.env Exceptions**: Must explicitly allow .env.sample files, as these are legitimate template references used during development.

6. **Graceful Degradation**: Hook errors should not crash the entire system. Catch exceptions and exit 0 to allow normal operation.

7. **Audit Logging**: JSON logging is essential for debugging and security auditing in autonomous systems.

8. **Modularity**: Extracting shared patterns to a utility module improves maintainability and reduces code duplication.

## Key Insights

1. **Security Hooks are Critical**: For autonomous systems, security hooks are not optional - they prevent catastrophic accidents.

2. **Comprehensive Pattern Matching**: Multiple pattern variations are necessary because users can input commands in many forms.

3. **Future-Proofing**: Building a security_patterns.py module now allows other hooks (e.g., pre_message) to use these patterns.

4. **Testing is Essential**: Each hook should be tested with both dangerous and safe commands to verify correct behavior.

5. **Documentation Matters**: Clear documentation on rollback procedures ensures security hooks can be quickly disabled if needed.
