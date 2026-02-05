# SSOT External Integrations Violations Report

**Scout:** Architecture Analysis Agent
**Date:** 2026-02-06
**Status:** Complete

---

## Summary

External integration configuration is scattered with **CRITICAL security issues** including hardcoded credentials. **MCP server configs in 3+ places**, GitHub config in **4+ files**.

---

## 1. CRITICAL: Hardcoded Credentials (SECURITY RISK)

**Hardcoded API keys/tokens found:**

| Location | Credential | Risk Level |
|----------|------------|------------|
| `bin/telegram-notify.sh` | Telegram bot token | **CRITICAL** |
| `.claude/settings.json` | Telegram bot token | **CRITICAL** |
| `2-engine/.autonomous/config/secrets.yaml` | ZAI API key | **CRITICAL** |
| `.mcp.json` | Various API keys | **HIGH** |

**Specific Finding:**
```bash
# bin/telegram-notify.sh
TELEGRAM_BOT_TOKEN="759xxxxxxx:xxxxxxxxxxxxxxxxxxxxxxxxxx"
CHAT_ID="xxxxxxxxx"
```

**Violation:** Credentials should NEVER be hardcoded. Should use environment variables or secret management.

---

## 2. MCP Server Configuration Duplication

**MCP servers configured in 3+ places:**

| Location | Servers | Issue |
|----------|---------|-------|
| `.mcp.json` (root) | 5+ servers | Should be SSOT |
| `2-engine/.mcp.json` | 3+ servers | Engine-specific |
| `.claude/settings.json` | MCP references | Indirect config |
| `CLAUDE.md` | MCP documentation | Docs, not config |

**Example Duplication:**
```json
// .mcp.json (root)
{
  "mcpServers": {
    "supabase": { ... },
    "notion": { ... }
  }
}

// 2-engine/.mcp.json
{
  "mcpServers": {
    "supabase": { ... }  // Different config!
  }
}
```

**Issue:** Same MCP servers configured differently in engine vs project.

---

## 3. GitHub Integration Scattered

**GitHub configuration in 4+ files:**

| Location | Config |
|----------|--------|
| `.claude/settings.json` | GitHub CLI settings |
| `CLAUDE.md` | Git workflow documentation |
| `bin/bb5-*` scripts | Git commands hardcoded |
| `.github/workflows/` | CI/CD config |
| `2-engine/.autonomous/` | Engine git config |

**Issue:** Git operations documented in CLAUDE.md but also in scripts, with different patterns.

---

## 4. Supabase Configuration Duplication

**Supabase configured in multiple places:**

| Location | Config |
|----------|--------|
| `.mcp.json` | MCP server config |
| `CLAUDE.md` | Supabase operations skill |
| `skills/supabase-operations/SKILL.md` | Skill documentation |
| `2-engine/` | Engine supabase integration |

**Issue:** Supabase connection details in MCP config, but operations documented in skill.

---

## 5. Notification System Duplication

**Notifications configured in:**

| Location | Purpose |
|----------|---------|
| `bin/telegram-notify.sh` | Telegram notifications |
| `bin/notifications.sh` | General notifications |
| `.claude/hooks/ralf-stop-hook.sh` | Stop notifications |
| `CLAUDE.md` | Notification documentation |

**Issue:** Multiple notification scripts with overlapping functionality.

---

## 6. Web Search Configuration

**Web search configured in:**

| Location | Config |
|----------|--------|
| `CLAUDE.md` | web-search skill reference |
| `skills/web-search/SKILL.md` | Skill documentation |
| `.mcp.json` | May have search MCP |
| `2-engine/` | Engine search integration |

---

## 7. External API Keys Management

**API keys scattered:**

| Service | Locations |
|---------|-----------|
| Telegram | 2 files |
| ZAI | 1 file |
| OpenAI | Unknown (may be in env) |
| Anthropic | Unknown (may be in env) |
| GitHub | 2+ files |
| Supabase | 2+ files |

**No centralized secret management.**

---

## Specific Examples

### Example 1: Telegram Token Duplication
```bash
# bin/telegram-notify.sh (line 12)
TELEGRAM_BOT_TOKEN="759xxxxxxx:xxxxxxxxxxxxxxxxxxxxxxxxxx"

# .claude/settings.json
{
  "telegram": {
    "bot_token": "759xxxxxxx:xxxxxxxxxxxxxxxxxxxxxxxxxx"
  }
}

# Same token in 2 places - if rotated, one will break
```

### Example 2: MCP Server Inconsistency
```json
// .mcp.json - Supabase config
"supabase": {
  "command": "npx",
  "args": ["-y", "@anthropic-ai/mcp-supabase"]
}

// 2-engine/.mcp.json - Different supabase config
"supabase": {
  "command": "node",
  "args": ["/path/to/supabase-mcp"]
}
```

### Example 3: GitHub Config Scattered
```yaml
# CLAUDE.md
Git workflow: Use `gh` CLI

# bin/bb5-create
Uses git commands directly

# .github/workflows/
Uses GitHub Actions

# No unified GitHub integration strategy
```

---

## Recommendations for SSOT

### 1. Secret Management (CRITICAL)
**Canonical Source:** Environment variables or secret vault

```bash
# .env (gitignored)
TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
ZAI_API_KEY=${ZAI_API_KEY}
OPENAI_API_KEY=${OPENAI_API_KEY}
```

**Actions:**
- Remove all hardcoded credentials IMMEDIATELY
- Rotate exposed credentials
- Use environment variables
- Consider secret management tool (1Password, Vault)

### 2. MCP Configuration SSOT
**Canonical Source:** `.mcp.json` (root only)
- Delete `2-engine/.mcp.json`
- Engine uses root config
- Document in CLAUDE.md, don't duplicate config

### 3. Integration Documentation SSOT
**Canonical Source:** `docs/INTEGRATIONS.md`
- All integration docs in one place
- Per-integration sections
- CLAUDE.md references only

### 4. Notification System Consolidation
**Canonical Source:** `bin/notify.sh` (single script)
- Merge telegram-notify.sh
- Merge notifications.sh
- Support multiple channels via config

### 5. Configuration Hierarchy
```
config/
├── integrations.yaml      # All integration settings
├── secrets.env            # Environment variables (gitignored)
├── secrets.env.example    # Template
└── mcp.json               # MCP servers (root only)
```

---

## Security Action Items (URGENT)

1. **IMMEDIATE:** Remove hardcoded Telegram token from:
   - `bin/telegram-notify.sh`
   - `.claude/settings.json`

2. **IMMEDIATE:** Remove hardcoded ZAI API key from:
   - `2-engine/.autonomous/config/secrets.yaml`

3. **IMMEDIATE:** Rotate exposed credentials

4. **SHORT-TERM:** Implement environment variable pattern

5. **SHORT-TERM:** Add `.env` to `.gitignore`

6. **LONG-TERM:** Consider secret management solution

---

## Critical Files Requiring Immediate Attention

1. `bin/telegram-notify.sh` - **HARDCODED TOKEN**
2. `.claude/settings.json` - **HARDCODED TOKEN**
3. `2-engine/.autonomous/config/secrets.yaml` - **HARDCODED API KEY**
4. `2-engine/.mcp.json` - Duplicate MCP config
5. Multiple notification scripts - Consolidate

---

## Task Creation Checklist

- [ ] TASK-SSOT-026: **URGENT** Remove hardcoded credentials
- [ ] TASK-SSOT-027: **URGENT** Rotate exposed API keys
- [ ] TASK-SSOT-028: Implement environment variable pattern
- [ ] TASK-SSOT-029: Consolidate MCP configuration
- [ ] TASK-SSOT-030: Create integrations.yaml
- [ ] TASK-SSOT-031: Merge notification scripts
- [ ] TASK-SSOT-032: Create secret management strategy
- [ ] TASK-SSOT-033: Document all integrations
