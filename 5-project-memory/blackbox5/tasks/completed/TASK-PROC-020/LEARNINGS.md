# LEARNINGS.md - TASK-PROC-020: Duplicate Task Detection

## What Worked Well

1. **Multi-algorithm approach**: Using a combination of exact matching, title similarity, and objective similarity catches duplicates even when wording varies slightly.

2. **Normalization is key**: Stripping task IDs and common prefixes before comparison revealed many "hidden" duplicates that looked different at first glance.

3. **Integration point**: Hooking into the `bb5 task:create` workflow ensures duplicate detection runs automatically without requiring users to remember to check.

4. **Confidence scoring**: Providing a confidence percentage helps users understand the severity of the potential duplicate.

## What Was Harder Than Expected

1. **Parsing inconsistent formats**: Tasks have varying formats (some with YAML frontmatter, some without), making consistent extraction of titles and objectives challenging.

2. **Threshold tuning**: Setting the right similarity thresholds required balancing false positives vs false negatives. 85% for high confidence and 70% for medium seems to work well.

3. **Content comparison**: Comparing full task content is expensive and can be misleading for longer tasks that share boilerplate text.

## What Would I Do Differently

1. **Standardize task format**: Enforce a consistent task template to make parsing more reliable.

2. **Add semantic similarity**: Use embeddings/vector similarity for better semantic matching beyond string similarity.

3. **Track duplicate decisions**: When a user confirms "yes, create anyway" despite warning, store this decision to avoid prompting again for similar tasks.

## Patterns Detected

1. **Common duplicate patterns**:
   - Same task created via different naming conventions (TASK-AUTO-021 vs TASK-MEMORY-001)
   - Scout process creating tasks that already exist
   - Tasks with identical titles but different IDs

2. **Root causes**:
   - No centralized task registry during creation
   - Multiple entry points for task creation (manual, scout, RALF)
   - Lack of search before create workflow

## Recommendations

1. Run `detect-duplicate-tasks.py --report` monthly to catch duplicates early
2. Archive completed duplicates to reduce noise
3. Consider adding a "duplicate-of" field to task metadata for tracking
