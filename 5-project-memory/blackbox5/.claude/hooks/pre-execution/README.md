# Pre-Execution Hooks

Hooks that run before task execution begins.

## skill-enforcement.sh

**Purpose:** Enforces skill invocation based on confidence scores from `detect-skill.py`.

**Behavior:**

### Clear Trigger (>=85% confidence)
- **Action:** Blocks execution until skill is invoked
- **Output:** Shows required skill and instructions
- **Exit Code:** 1 (blocked)

### Discretionary Trigger (70-84% confidence)
- **Action:** Warns but allows execution
- **Output:** Shows recommended skill and override template
- **Exit Code:** 0 (allowed)

### No Match (<70% confidence)
- **Action:** Allows execution normally
- **Output:** Shows brief confirmation
- **Exit Code:** 0 (allowed)

## Bypassing Enforcement

To bypass skill enforcement (not recommended):

```bash
# Set environment variable
export BB5_SKIP_SKILL_ENFORCEMENT=1

# Or for single command
BB5_SKIP_SKILL_ENFORCEMENT=1 bb5 task:run TASK-xxx
```

## Troubleshooting

### Hook not running
- Check permissions: `ls -l /opt/blackbox5/5-project-memory/blackbox5/.claude/hooks/pre-execution/skill-enforcement.sh`
- Should be executable: `-rwxr-xr-x`

### detect-skill.py not found
- Verify path: `/opt/blackbox5/5-project-memory/blackbox5/bin/detect-skill.py`
- Check executable: `ls -l /opt/blackbox5/5-project-memory/blackbox5/bin/detect-skill.py`

### Task file not found
- Set TASK_FILE environment variable: `export TASK_FILE=/path/to/task.md`
- Hook looks for `TASK.md` in `.claude/` by default

### Enforcement log location
- Log file: `/opt/blackbox5/5-project-memory/blackbox5/logs/skill-enforcement.log`
- Skill metrics: `/opt/blackbox5/5-project-memory/blackbox5/operations/skill-metrics.yaml`

## Integration

The hook integrates with:

1. **detect-skill.py** - Analyzes task and returns recommended skills
2. **skill-registry.yaml** - Contains skill definitions and triggers
3. **skill-metrics.yaml** - Logs enforcement actions
4. **THOUGHTS.md** - Where agents document override justifications

## Testing

Test the hook manually:

```bash
# Test with a clear trigger
cd /opt/blackbox5
export TASK_FILE=/opt/blackbox5/5-project-memory/blackbox5/tasks/active/TASK-xxx/task.md
./5-project-memory/blackbox5/.claude/hooks/pre-execution/skill-enforcement.sh

# Test with bypass
export BB5_SKIP_SKILL_ENFORCEMENT=1
./5-project-memory/blackbox5/.claude/hooks/pre-execution/skill-enforcement.sh
```

## Rollback

To disable the hook temporarily:

```bash
# Rename to disable
mv /opt/blackbox5/5-project-memory/blackbox5/.claude/hooks/pre-execution/skill-enforcement.sh \
   /opt/blackbox5/5-project-memory/blackbox5/.claude/hooks/pre-execution/skill-enforcement.sh.disabled
```

To re-enable:

```bash
# Rename back
mv /opt/blackbox5/5-project-memory/blackbox5/.claude/hooks/pre-execution/skill-enforcement.sh.disabled \
   /opt/blackbox5/5-project-memory/blackbox5/.claude/hooks/pre-execution/skill-enforcement.sh
chmod +x /opt/blackbox5/5-project-memory/blackbox5/.claude/hooks/pre-execution/skill-enforcement.sh
```
