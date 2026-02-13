# TASK-CC-001A: Discover Claude Code Related GitHub Repos

**Status:** completed
**Priority:** high
**Parent:** TASK-CC-REPO-ANALYSIS-001
**Blocked By:** None (can start immediately)
**Blocks:** TASK-CC-001B-* (all repo analysis tasks)
**Completed:** 2026-02-13T03:30:00Z

---

## Goal

Search GitHub for repositories related to Claude Code and identify the top 5 most relevant repos for analysis.

## Criteria

1. **Relevance**: Must be related to Claude Code, Claude API, or Anthropic SDK
2. **Activity**: Last commit within 6 months
3. **Popularity**: >100 stars (or notable if <100)
4. **Diversity**: Mix of types (CLI tools, SDKs, integrations, examples)

## Search Queries

```
"Claude Code" CLI tool
anthropic claude sdk
claude-code plugin extension
anthropic claude api examples
claude code automation
```

## Output

Create `6-roadmap/.research/external/GitHub/repo-list.yaml`:

```yaml
discovered_repos:
  - owner: "..."
    repo: "..."
    url: "https://github.com/..."
    stars: 0
    last_commit: "..."
    relevance_score: 0  # 1-10
    analysis_priority: 1-5
    reason: "..."
```

## Success Criteria

- [x] 5+ repos identified (7 repos found)
- [x] Each repo has metadata (stars, last commit, description)
- [x] Relevance score assigned (scores 6-10)
- [x] repo-list.yaml created and committed

## Completion Summary ✅

**Date:** 2026-02-13T03:30:00Z
**Agent:** moltbot-vps-ai
**Work Session:** ~10 minutes

### Repositories Discovered

| Priority | Repo | Stars | Relevance | Category |
|----------|------|-------|-----------|----------|
| 1 | affaan-m/everything-claude-code | 45,144 | 10 | Config Collection |
| 2 | davila7/claude-code-templates | 20,197 | 9 | CLI Tooling |
| 3 | kodu-ai/claude-coder | 5,291 | 8 | VSCode Extension |
| 4 | coder/claudecode.nvim | 2,012 | 8 | Neovim Extension |
| 5 | tghamm/Anthropic.SDK | 210 | 7 | C# SDK |
| 6 | win4r/claude-code-clawdbot-skill | 67 | 7 | OpenClaw Skill |
| 7 | anthropics/anthropic-retrieval-demo | 178 | 6 | Official Demo |

### Files Created

- `6-roadmap/.research/external/GitHub/repo-list.yaml` (118 lines)
- Committed to git (commit: deece911a)

### Method

Used GitHub API to search for repos with keywords:
- "anthropic claude code"
- "claude code cli"
- "anthropic claude sdk"
- "claude code extension"
- "claude api examples"

### Diversity Achieved

✅ Configuration templates
✅ CLI tools
✅ IDE extensions (VSCode, Neovim)
✅ SDK implementations
✅ Official demos
✅ OpenClaw integrations

### Next Steps

1. Create TASK-CC-001B-* subtasks for each repo (7 repos × 3 cycles = 21 tasks)
2. Set blockedBy dependencies linking to TASK-CC-001A
3. Update queue.yaml with new work items
4. Begin Phase 2: Per-repo analysis cycles

## Next Steps After Completion

1. Create TASK-CC-001B-* subtasks for each repo
2. Set blockedBy dependencies
3. Update queue.yaml with new work items
