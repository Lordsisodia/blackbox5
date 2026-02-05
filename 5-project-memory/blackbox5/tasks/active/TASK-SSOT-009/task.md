# TASK-SSOT-009: Consolidate MCP Configuration

**Status:** pending
**Priority:** HIGH
**Created:** 2026-02-06
**Parent:** Issue #20 - SSOT External Integrations Violations

## Objective
Consolidate MCP server configuration from 3+ locations into single .mcp.json at project root.

## Success Criteria
- [ ] Audit all .mcp.json files
- [ ] Merge configurations (resolve conflicts)
- [ ] Choose canonical location: .mcp.json (root)
- [ ] Delete 2-engine/.mcp.json
- [ ] Update documentation
- [ ] Test all MCP servers still work

## Context
MCP servers configured in:
- .mcp.json (root) - 5+ servers
- 2-engine/.mcp.json - 3+ servers (different config!)
- .claude/settings.json - MCP references

Same servers (supabase) have different configurations.

## Approach
1. Read all .mcp.json files
2. Identify differences
3. Merge into root .mcp.json
4. Delete engine .mcp.json
5. Test MCP functionality

## Related Files
- .mcp.json
- 2-engine/.mcp.json
- .claude/settings.json

## Rollback Strategy
Keep backup of engine .mcp.json until verification complete.
