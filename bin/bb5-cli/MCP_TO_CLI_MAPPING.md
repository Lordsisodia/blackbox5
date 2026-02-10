# BB5 MCP to CLI Mapping

Complete mapping of all MCP servers to CLI equivalents.

---

## 1. Supabase MCP → `bb5 db`

**MCP**: `@modelcontextprotocol/server-supabase`
**CLI**: `bb5 db <tool>`

| MCP Tool | CLI Command | Status |
|----------|-------------|--------|
| `list_tables` | `bb5 db tables list` | ⏳ |
| `list_extensions` | `bb5 db extensions list` | ⏳ |
| `list_migrations` | `bb5 db migrate list` | ⏳ |
| `apply_migration` | `bb5 db migrate up` | ⏳ |
| `execute_sql` | `bb5 db query -s "SQL"` | ✅ |
| `get_logs` | `bb5 db logs --service api` | ⏳ |
| `get_advisors` | `bb5 db advisors` | ⏳ |
| `get_project_url` | `bb5 db project url` | ⏳ |
| `get_publishable_keys` | `bb5 db project keys` | ⏳ |
| `generate_typescript_types` | `bb5 db types generate` | ⏳ |
| `list_edge_functions` | `bb5 db edge list` | ⏳ |
| `get_edge_function` | `bb5 db edge get <name>` | ⏳ |
| `deploy_edge_function` | `bb5 db edge deploy` | ⏳ |
| `list_projects` | `bb5 db projects list` | ⏳ |
| `get_project` | `bb5 db project get` | ⏳ |
| `create_project` | `bb5 db project create` | ⏳ |
| `pause_project` | `bb5 db project pause` | ⏳ |
| `restore_project` | `bb5 db project restore` | ⏳ |
| `list_organizations` | `bb5 db orgs list` | ⏳ |
| `get_organization` | `bb5 db org get` | ⏳ |
| `get_cost` | `bb5 db cost` | ⏳ |
| `confirm_cost` | `bb5 db cost confirm` | ⏳ |
| `search_docs` | `bb5 db docs search` | ⏳ |
| `create_branch` | `bb5 db branch create` | ⏳ |
| `list_branches` | `bb5 db branch list` | ⏳ |
| `delete_branch` | `bb5 db branch delete` | ⏳ |
| `merge_branch` | `bb5 db branch merge` | ⏳ |
| `reset_branch` | `bb5 db branch reset` | ⏳ |
| `rebase_branch` | `bb5 db branch rebase` | ⏳ |

**Total**: 29 tools

---

## 2. Filesystem MCP → `bb5 fs`

**MCP**: `@modelcontextprotocol/server-filesystem`
**CLI**: `bb5 fs <tool>`

| MCP Tool | CLI Command | Native Equivalent | Status |
|----------|-------------|-------------------|--------|
| `read_text_file` | `bb5 fs read <path>` | `cat <path>` | ⏳ |
| `read_media_file` | `bb5 fs read-media <path>` | `cat <path>` | ⏳ |
| `read_multiple_files` | `bb5 fs read-multi <paths>` | `cat <paths>` | ⏳ |
| `write_file` | `bb5 fs write <path> <content>` | `echo > <path>` | ⏳ |
| `edit_file` | `bb5 fs edit <path>` | `sed -i` | ⏳ |
| `create_directory` | `bb5 fs mkdir <path>` | `mkdir -p` | ⏳ |
| `list_directory` | `bb5 fs ls <path>` | `ls -la` | ⏳ |
| `search_files` | `bb5 fs find <pattern>` | `find . -name` | ⏳ |
| `grep_search` | `bb5 fs grep <pattern>` | `rg <pattern>` | ⏳ |
| `move_file` | `bb5 fs mv <src> <dst>` | `mv` | ⏳ |
| `delete_file` | `bb5 fs rm <path>` | `rm` | ⏳ |
| `get_file_info` | `bb5 fs stat <path>` | `stat` | ⏳ |
| `list_allowed_directories` | `bb5 fs allowed` | N/A | ⏳ |

**Total**: 13 tools

**Note**: Most filesystem operations can use native shell commands. The CLI wrapper adds:
- Path validation against allowed directories
- Batch operations
- Better error messages

---

## 3. Playwright MCP → `bb5 browser`

**MCP**: `@executeautomation/playwright-mcp-server`
**CLI**: `bb5 browser <tool>`

| MCP Tool | CLI Command | Status |
|----------|-------------|--------|
| `playwright_navigate` | `bb5 browser navigate --url <url>` | ⏳ |
| `playwright_click` | `bb5 browser click --selector <css>` | ⏳ |
| `playwright_screenshot` | `bb5 browser screenshot --output <file>` | ⏳ |
| `playwright_hover` | `bb5 browser hover --selector <css>` | ⏳ |
| `playwright_fill` | `bb5 browser fill --selector <css> --value <text>` | ⏳ |
| `playwright_select` | `bb5 browser select --selector <css> --value <option>` | ⏳ |
| `playwright_evaluate` | `bb5 browser eval --script <js>` | ⏳ |
| `playwright_resize` | `bb5 browser resize --width <w> --height <h>` | ⏳ |

**Total**: 8 tools

---

## 4. Sequential Thinking MCP → `bb5 think`

**MCP**: `@modelcontextprotocol/server-sequential-thinking`
**CLI**: `bb5 think <tool>`

| MCP Tool | CLI Command | Status |
|----------|-------------|--------|
| `sequentialthinking` | `bb5 think start --topic "..."` | ⏳ |
| (add thought) | `bb5 think add --content "..."` | ⏳ |
| (branch) | `bb5 think branch --from <n>` | ⏳ |
| (list) | `bb5 think list` | ⏳ |
| (show) | `bb5 think show --id <id>` | ⏳ |
| (export) | `bb5 think export --id <id>` | ⏳ |

**Total**: 6 commands

---

## 5. Fetch MCP → `bb5 http`

**MCP**: `@modelcontextprotocol/server-fetch`
**CLI**: `bb5 http <tool>` or native `curl`

| MCP Tool | CLI Command | Native Equivalent | Status |
|----------|-------------|-------------------|--------|
| `fetch` | `bb5 http get <url>` | `curl <url>` | ⏳ |
| (POST) | `bb5 http post <url> --data <data>` | `curl -X POST -d` | ⏳ |
| (with headers) | `bb5 http get <url> --header "Key: Val"` | `curl -H` | ⏳ |

**Recommendation**: Use native `curl` or `httpie` instead. The CLI wrapper only adds:
- Response formatting
- JSON pretty-printing

---

## 6. Code Parser MCP → `bb5 code`

**MCP**: `@boxabirds/mcp-code-parser`
**CLI**: `bb5 code <tool>`

| MCP Tool | CLI Command | Native Equivalent | Status |
|----------|-------------|-------------------|--------|
| `parse_code` | `bb5 code parse --content "..." --lang python` | N/A | ⏳ |
| `parse_file` | `bb5 code parse-file <path>` | `tree-sitter parse` | ⏳ |
| `list_languages` | `bb5 code languages` | N/A | ⏳ |
| `check_language` | `bb5 code check-lang <lang>` | N/A | ⏳ |

**Total**: 4 tools

**Note**: Can also use `tree-sitter` CLI directly.

---

## 7. Auto-Claude MCP → `bb5 auto`

**MCP**: Custom `08-integrations/auto-claude/mcp-server.py`
**CLI**: `bb5 auto <tool>`

| MCP Tool | CLI Command | Status |
|----------|-------------|--------|
| `create_spec` | `bb5 auto spec create` | ⏳ |
| `run_build` | `bb5 auto build` | ⏳ |
| `qa_validation` | `bb5 auto qa` | ⏳ |
| `git_operations` | `bb5 auto git <cmd>` | ⏳ |
| `task_management` | `bb5 auto task <cmd>` | ⏳ |

**Total**: 5 tools

---

## 8. MoltBot/VPS MCP → `bb5 remote`

**MCPs**: `ralf-vps`, `moltbot-macmini`, `moltbot-vps`, `macmini-clawdbot`
**CLI**: `bb5 remote <tool>`

| MCP Tool | CLI Command | Status |
|----------|-------------|--------|
| `moltbot_get_status` | `bb5 remote exec <host> "ps aux | grep openclaw"` | ✅ |
| `moltbot_send_message` | `bb5 remote claw <host> message send ...` | ⏳ |
| `moltbot_get_ralf_status` | `bb5 remote ralf <host> status` | ✅ |
| `moltbot_get_user_context` | `bb5 remote exec <host> "cat /opt/moltbot/user-context.json"` | ✅ |
| `moltbot_run_command` | `bb5 remote exec <host> "<cmd>"` | ✅ |

**Total**: 5 tools

---

## Summary

| MCP Server | Tools | CLI Status |
|------------|-------|------------|
| Supabase | 29 | 1 ✅, 28 ⏳ |
| Filesystem | 13 | 13 ⏳ |
| Playwright | 8 | 8 ⏳ |
| Sequential Thinking | 6 | 6 ⏳ |
| Fetch | 3 | Use `curl` |
| Code Parser | 4 | 4 ⏳ |
| Auto-Claude | 5 | 5 ⏳ |
| Remote/VPS | 5 | 5 ✅ |
| **TOTAL** | **73** | **6 ✅, 64 ⏳, 3 use native** |

---

## Priority Implementation Order

1. **Remote/VPS** ✅ - Already working
2. **Supabase query** ✅ - Already working
3. **Filesystem** - High priority (used frequently)
4. **Playwright** - Medium priority (browser automation)
5. **Sequential Thinking** - Low priority (can use native scripts)
6. **Code Parser** - Low priority (can use `tree-sitter` CLI)
7. **Auto-Claude** - Integrate with existing RALF
8. **Supabase others** - As needed
