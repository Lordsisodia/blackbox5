# Ralph Autonomous Agent - Quick Start Guide

**Location**: `blackbox5/5-project-memory/siso-internal/ralph.p/`
**Purpose**: Autonomous multi-project management

---

## Prerequisites

1. **API Commands Configured**:
   ```bash
   which claude      # Should show path to GLM command
   which cso-kimi    # Should show path to Kimi command
   ```

2. **On Dev Branch**:
   ```bash
   git branch --show-current   # Should show "dev"
   ```

3. **Projects Configured**:
   - Edit `CONFIG.yaml` with your project paths
   - Add Supabase project refs

---

## Quick Commands

```bash
# Navigate to Ralph directory
cd blackbox5/ralph.p

# Check status
./SCRIPTS/status.sh

# Start Ralph (setup mode first)
./SCRIPTS/start-ralph.sh setup

# Start full autonomous loop
./SCRIPTS/start-ralph.sh full

# Stop Ralph
./SCRIPTS/stop-ralph.sh
```

---

## Modes

| Mode | Purpose | When to Use |
|------|---------|-------------|
| `setup` | Validate structure, check APIs | First run, after changes |
| `feature` | Build features from PRDs | When you have tasks ready |
| `idea` | Generate ideas from documents | Daily, or when stuck |
| `test` | Run tests, verify Supabase | After implementing features |
| `full` | Run all modes in loop | Normal autonomous operation |

---

## Configuration

Edit `CONFIG.yaml`:

```yaml
# Add your projects
projects:
  - id: "my-project"
    path: "../path/to/project"
    supabase:
      project_ref: "your-project-ref"

# Adjust timing
autonomous:
  check_interval: 300  # 5 minutes
  max_session_duration: 14400  # 4 hours

# API usage
api:
  glm:
    command: "claude"  # Your GLM command
  kimi:
    command: "cso-kimi"  # Your Kimi command
```

---

## Safety Features

- **Branch Protection**: Cannot run on main/master
- **API Rate Limiting**: Tracks GLM (2000/5h) and Kimi (500/5h)
- **Confirmation Required**: For git push, DB migrations, branch switches
- **Session Limits**: Max 4 hours per session

---

## Logs

```bash
# View latest session
tail -f LOGS/sessions/session-*.log

# View errors
cat LOGS/errors/$(date +%Y-%m-%d).log

# Check current session
cat STATE/current-session.yaml
```

---

## Troubleshooting

### "Cannot run on main/master branch"
```bash
git checkout dev
git pull origin dev
```

### "API not available"
- Verify `claude` and `cso-kimi` commands are in PATH
- Check API keys are configured

### "Project not found"
- Check `CONFIG.yaml` paths are correct
- Paths are relative to `blackbox5/ralph.p/`

---

## Next Steps

1. **Review PROJECT-SPEC.md** - Understand full specification
2. **Edit CONFIG.yaml** - Add your projects and API settings
3. **Run setup mode** - Validate everything works
4. **Start with feature mode** - Try implementing a small task
5. **Go full autonomous** - Run the complete loop

---

## Support

- **Spec**: `PROJECT-SPEC.md`
- **Config**: `CONFIG.yaml`
- **Workflows**: `WORKFLOWS/`
- **Logs**: `LOGS/`

---

**Remember**: All work stays on `dev` branch. Never commit to main/master.
