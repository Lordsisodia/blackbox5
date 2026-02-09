# Assumptions: TASK-AUTONOMY-001

1. **IG-010 hook infrastructure exists or will exist** - I'm building on top of their foundation
2. **Task directories follow BB5 convention** - tasks/active/TASK-XXX/task.md
3. **queue.yaml exists and is parseable** - For status synchronization
4. **Hooks can write to task files** - Need write permissions to update status
5. **SessionStart can detect task directory** - Using pwd and path matching
