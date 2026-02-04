# TASK-CC-001A: Discover Claude Code Related GitHub Repos

**Status:** pending
**Priority:** high
**Parent:** TASK-CC-REPO-ANALYSIS-001
**Blocked By:** None (can start immediately)
**Blocks:** TASK-CC-001B-* (all repo analysis tasks)

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

- [ ] 5+ repos identified
- [ ] Each repo has metadata (stars, last commit, description)
- [ ] Relevance score assigned
- [ ] repo-list.yaml created and committed

## Next Steps After Completion

1. Create TASK-CC-001B-* subtasks for each repo
2. Set blockedBy dependencies
3. Update queue.yaml with new work items
