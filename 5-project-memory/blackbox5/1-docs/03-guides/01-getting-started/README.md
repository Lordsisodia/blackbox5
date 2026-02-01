# Getting Started Guides

**Last Updated**: 2026-01-30
**Status**: Quick start resources consolidated

---

## Overview

This directory contains quick start guides and getting started resources for BlackBox5. Multiple quick start documents have been consolidated here to serve as the entry point for new users.

## Primary Quick Start

### 🚀 START-NOW.md (Recommended First Read)
**File**: `quickstart/START-NOW.md`

**Purpose**: Get started in 3 steps - the fastest path to using BlackBox5

**Contents**:
- 3-step quick start
- Available agents overview
- Real examples (fix bugs, add features, code review)
- Project context (what agents know)
- Troubleshooting

**Time to Read**: 2 minutes
**Use This For**: Your very first interaction with BlackBox5

---

### 📋 QUICKSTART.md (Comprehensive Guide)
**File**: `quickstart/QUICKSTART.md`

**Purpose**: Complete quick start guide with detailed examples

**Contents**:
- Getting started in 30 seconds
- Interactive mode (recommended)
- Common use cases
- Available agents with examples
- Workflow examples
- Pro tips
- Configuration
- Project context
- Troubleshooting
- Example session walkthrough

**Time to Read**: 5 minutes
**Use This For**: Understanding full capabilities after first use

---

## Additional Quick Start Resources

### Implementation Quick Starts

| Resource | Location | Purpose |
|----------|----------|---------|
| Skills Quick Start | `../../02-implementation/06-tools/skills/QUICK-START.md` | Skills system setup |
| Context Extraction | `../../02-implementation/05-memory-implementation/context/CONTEXT-EXTRACTION-QUICKSTART.md` | Memory context setup |
| MCP Quickstart | `../../02-implementation/04-integrations/mcp/MCP-QUICKSTART.md` | MCP integration |
| AgentClient Quickstart | `../../02-implementation/01-core/general/AgentClient-QUICKSTART.md` | Agent client usage |
| Anti-Pattern Quickstart | `../../02-implementation/01-core/resilience/ANTI-PATTERN-QUICKSTART.md` | Resilience patterns |
| Pipeline Quick Start | `../../02-implementation/03-pipeline/feature/PIPELINE-QUICK-START.md` | Feature pipeline |

### Development Quick Starts

| Resource | Location | Purpose |
|----------|----------|---------|
| Unified Test Quickstart | `../../development/tests/unified/QUICKSTART.md` | Testing framework |
| MCP Gateway Quickstart | `../../decisions/mcp/MCP-GATEWAY-QUICKSTART.md` | MCP gateway setup |

---

## Quick Start by Use Case

### I Want to Fix a Bug
```bash
# Fastest way
python .blackbox5/bb5.py --agent bug_fixer "The reward catalog shows undefined"

# Or interactive mode
python .blackbox5/bb5.py --interactive
bb5> --agent bug_fixer Fix the null reference in RewardCatalog.tsx
```

### I Want to Add a Feature
```bash
# With specific agent
python .blackbox5/bb5.py --agent frontend_developer "Add loading state to dashboard"

# Or workflow for complex features
python .blackbox5/bb5.py --workflow "Design, implement, test the new feature"
```

### I Want a Code Review
```bash
python .blackbox5/bb5.py --agent code_reviewer "Review the recent analytics changes"
```

### I Want to Run Tests
```bash
# All orchestrator tests
cd .blackbox5/tests && python -m pytest test_orchestrator.py -v

# All tests
python -m pytest .blackbox5/tests/ -v
```

---

## Available Agents Quick Reference

| Agent | Best For | Example Task |
|-------|----------|--------------|
| `developer` | General tasks | "Add a new button" |
| `frontend_developer` | React/TypeScript/UI | "Update dashboard layout" |
| `backend_developer` | Supabase/API/DB | "Create rewards table" |
| `analytics_specialist` | Gamification/Dashboards | "Add engagement tracking" |
| `bug_fixer` | Debugging/Errors | "Fix type error in line 45" |
| `code_reviewer` | Quality/Security | "Review PR changes" |
| `documentation` | Docs/Guides | "Document reward API" |

---

## Configuration

### Default Configuration
- **Model**: GLM-4.7
- **Config File**: `.blackbox5/engine/config.yml`
- **Memory Path**: `.blackbox5/memory/`

### Environment Variables
```bash
BLACKBOX5_ENGINE_PATH      # Path to engine (default: ./2-engine)
BLACKBOX5_MEMORY_PATH      # Path to memory (default: ./5-project-memory)
BLACKBOX5_CONTEXT_THRESHOLD # Warning threshold (default: 80)
BLACKBOX5_SESSION_TIMEOUT  # Session timeout in seconds (default: 14400)
GLM_API_KEY               # API key for GLM
```

---

## Project Structure

BlackBox5 automatically understands your project:

```
SISO-INTERNAL/
├── src/
│   ├── domains/
│   │   ├── analytics/          # Analytics domain
│   │   │   └── components/
│   │   │       └── GamificationDashboard.tsx
│   │   └── lifelock/
│   │       └── habits/
│   │           └── gamification/
│   │               ├── 2-spend/features/storefront/
│   │               │   └── RewardCatalog.tsx
│   │               └── 3-track/ui/pages/
│   │                   └── AnalyticsDashboard.tsx
│   └── lib/utils/
│       └── formatters.ts
├── .blackbox5/                 # BlackBox5 system
│   ├── engine/                 # Core engine
│   ├── custom_agents/          # Agent definitions
│   └── memory/                 # Project memory
└── 5-project-memory/           # Project state
    └── siso-internal/
        ├── STATE.yaml          # Project state
        ├── ACTIVE.md           # Active work dashboard
        └── decisions/          # Decision records
```

---

## Troubleshooting

### Issue: "Agent failed to start"
**Solution**: Check that Redis is running:
```bash
redis-cli ping  # Should return PONG
```

### Issue: "GLM API error"
**Solution**: Verify your API key:
```bash
echo $GLM_API_KEY
```

### Issue: "Import errors"
**Solution**: Make sure you're in the project directory:
```bash
cd /Users/shaansisodia/DEV/SISO-ECOSYSTEM/SISO-INTERNAL
```

### Issue: "Redis not running"
**Solution**: Start Redis:
```bash
brew services start redis
```

---

## Next Steps

After completing the quick start:

1. **Try Interactive Mode**
   ```bash
   python .blackbox5/bb5.py --interactive
   ```

2. **Read Full Documentation**
   - **Orchestrator**: `../../02-implementation/01-core/orchestration/`
   - **Memory**: `../../01-theory/02-memory/`
   - **Skills**: `../../02-implementation/06-tools/skills/`

3. **Run Examples**
   ```bash
   python .blackbox5/examples/orchestrator_demo.py
   ```

4. **Explore Project Memory**
   - Check `5-project-memory/siso-internal/STATE.yaml`
   - Review `5-project-memory/siso-internal/ACTIVE.md`

---

## Document Relationships

```
START-NOW.md (2 min read)
    ↓
QUICKSTART.md (5 min read)
    ↓
    ├─→ Skills Quick Start
    ├─→ Memory Quick Start
    ├─→ MCP Quickstart
    └─→ Full Documentation
```

---

## Summary

This directory is your **entry point for getting started with BlackBox5**:

1. **New to BlackBox5?** → Start with `START-NOW.md` (2 minutes)
2. **Want detailed guide?** → Read `QUICKSTART.md` (5 minutes)
3. **Need specific feature?** → Check additional quick starts table
4. **Having issues?** → See troubleshooting section

All quick start resources are organized here for easy discovery.

---

**Maintainer**: SISO Internal Team
**Last Review**: 2026-01-30
**Next Review**: As needed
