# Session Capture System - Testing Guide

**Status**: ✅ Deployed to blackbox5 GitHub
**Date**: 2026-01-26

---

## What Was Deployed

The following files were added to the blackbox5 repository:

### New Hooks
- `blackbox5/.claude/hooks/create-session-record.sh` - Creates session folder structure
- `blackbox5/.claude/hooks/update-timeline.sh` - Updates timeline events array

### Documentation
- `2-engine/07-operations/integrations/claude-code/SESSION-REDESIGN.md` - Full architecture
- `2-engine/07-operations/integrations/claude-code/SESSION-CAPTURE-QUICKREF.md` - Quick reference

### Configuration
- `blackbox5/.claude/settings.json` - Updated with SessionEnd hooks and Haiku reflection

---

## How to Test

### Step 1: Verify Hooks Are Present

```bash
cd /Users/shaansisodia/DEV/client-projects/lumelle
ls -la blackbox5/.claude/hooks/ | grep -E "create-session|update-timeline"
```

Should see:
```
create-session-record.sh
update-timeline.sh
```

### Step 2: Verify Configuration

```bash
cat blackbox5/.claude/settings.json | jq '.hooks.SessionEnd'
cat blackbox5/.claude/settings.json | jq '.env.BLACKBOX5_MEMORY_PATH'
```

Should show:
- SessionEnd hooks include `create-session-record.sh` and `update-timeline.sh`
- Memory path is `./blackbox5/5-project-memory/lumelle`

### Step 3: Test Hook Execution

```bash
# Test session record creation
echo '{"session_id": "test-manual-123", "transcript_path": "/dev/null"}' | \
  blackbox5/.claude/hooks/create-session-record.sh

# Verify session folder was created
ls -la blackbox5/5-project-memory/lumelle/operations/sessions/ | tail -3
```

Should see a new `session-{timestamp}/` folder.

### Step 4: Test with Real Claude Code Session

**In this directory:**
```bash
cd /Users/shaansisodia/DEV/client-projects/lumelle
```

**Then:**
1. Start a Claude Code session (just open it in this directory)
2. Do some work (any small task)
3. Exit the session (Ctrl+D or `/exit`)
4. Check what was created:

```bash
# Check session folder
ls -la blackbox5/5-project-memory/lumelle/operations/sessions/

# Check latest session structure
ls -la blackbox5/5-project-memory/lumelle/operations/sessions/session-*/

# Check timeline was updated
cat blackbox5/5-project-memory/lumelle/project/timeline.yaml | grep -A5 "events:"

# Check reflection (may take 30s to appear)
sleep 35
ls -la blackbox5/5-project-memory/lumelle/operations/reflections/
```

---

## What Should Happen

### Immediately (SessionEnd hooks - fast)
1. Session folder created: `operations/sessions/session-{unix_timestamp}/`
2. Files created:
   - `transcript.jsonl` - Full conversation
   - `context.json` - Metadata (duration, git branch, etc.)
   - `metrics.json` - Stats
   - `README.md` - Human-readable summary
3. Timeline updated: `project/timeline.yaml` gets new event in `events: []` array

### After ~30s (Stop hook - async with Haiku)
1. Reflection created: `operations/reflections/reflection_{unix_timestamp}.md`
2. Contains: 2-3 sentence reflection on what was accomplished

---

## Troubleshooting

### Hook Not Running

Check settings.json:
```bash
cat blackbox5/.claude/settings.json | jq '.hooks.SessionEnd'
```

Should show our hooks in the list.

### Session Folder Not Created

Check hook is executable:
```bash
ls -la blackbox5/.claude/hooks/create-session-record.sh
```

Should show `-rwxr-xr-x` (executable).

### Wrong Memory Path

Check env var:
```bash
cat blackbox5/.claude/settings.json | jq '.env.BLACKBOX5_MEMORY_PATH'
```

Should be `./blackbox5/5-project-memory/lumelle` for this project.

### Timeline Not Updated

Check if yq is installed:
```bash
which yq
```

If not installed, hook uses fallback append method.

---

## Verification Checklist

- [ ] Hooks exist in `blackbox5/.claude/hooks/`
- [ ] Memory path points to correct project
- [ ] Manual test creates session folder
- [ ] Real session creates folder on exit
- [ ] Timeline gets updated with event
- [ ] Reflection appears after ~30s

---

## Success Indicators

✅ Session folders appear immediately on session end
✅ Each folder has JSON files (context, metrics, transcript)
✅ Timeline events array is updated
✅ Reflections appear asynchronously
✅ Everything uses cheap/fast operations (shell + Haiku)
