# GitHub Agents Research Setup

Setup guide for tracking AI agent-related GitHub repositories.

## Quick Start

1. **Edit `config/sources.yaml`** - Add GitHub repos to track
2. **Set up GitHub token** - For API access
3. **Run ingestion** - `python scripts/ingest.py`
4. **Process repos** - `python scripts/extract.py --pending`

## GitHub-Specific Structure

```
Agents/
├── data/
│   └── repos/
│       └── {owner}/
│           └── {repo}/
│               ├── metadata.yaml       # Stars, forks, description
│               ├── releases/
│               │   └── {tag}.yaml      # Release notes
│               ├── commits/
│               │   └── {sha}.yaml      # Significant commits
│               ├── readme_history/     # README versions
│               └── issues/             # Key issues (optional)
├── extracted/
│   ├── by_date/
│   ├── by_area/                       # e.g., frameworks, tools, platforms
│   └── by_topic/                      # e.g., mcp, autogen, crewai
└── ...
```

## Raw Data Format (data/repos/{owner}/{repo}/)

### metadata.yaml
```yaml
---
repo:
  owner: "microsoft"
  name: "autogen"
  url: "https://github.com/microsoft/autogen"
  description: "..."
  language: "Python"
  license: "MIT"

created_at: YYYY-MM-DDTHH:MM:SSZ
last_updated: YYYY-MM-DDTHH:MM:SSZ

collection:
  stars: 12345
  forks: 2345
  watchers: 567
  collected_at: YYYY-MM-DDTHH:MM:SSZ

processing:
  status: pending_extraction
  priority: [critical|high|medium|low]
---
```

### releases/{tag}.yaml
```yaml
---
release:
  tag: "v0.4.0"
  name: "Release 0.4.0"
  published_at: YYYY-MM-DDTHH:MM:SSZ
  url: "https://github.com/.../releases/tag/v0.4.0"

content:
  body: "..."
  is_prerelease: false
  is_draft: false

collection:
  collected_at: YYYY-MM-DDTHH:MM:SSZ

processing:
  status: pending_extraction
---
```

### commits/{sha}.yaml
```yaml
---
commit:
  sha: "abc123"
  message: "feat: add new feature"
  author: "username"
  committed_at: YYYY-MM-DDTHH:MM:SSZ
  url: "https://github.com/.../commit/abc123"

stats:
  additions: 100
  deletions: 50
  files_changed: 5

collection:
  collected_at: YYYY-MM-DDTHH:MM:SSZ
  significance: [major|minor|patch]
---
```

## Extracted Intelligence Format

```yaml
---
extraction:
  repo: "owner/repo"
  item_type: [release|commit|readme]
  item_id: "v0.4.0"
  extracted_at: YYYY-MM-DDTHH:MM:SSZ

classification:
  areas: [agent-frameworks, multi-agent]
  topics: [autogen, mcp, llm-orchestration]

summary:
  overview: "..."
  novelty_score: 8
  impact_score: 9

key_changes:
  - change: "Added MCP server support"
    type: feature
    breaking: false

actionable_takeaways:
  - action: "Upgrade to v0.4.0 for MCP support"
    difficulty: medium
    impact: high

ranking:
  composite: 85
---
```

## Source Tiers for Repos

- **Tier 1**: Core frameworks (AutoGen, CrewAI, LangGraph, etc.)
- **Tier 2**: Popular tools and integrations
- **Tier 3**: Experimental/new repos

## Areas

- `agent-frameworks`: Core agent building frameworks
- `mcp-servers`: Model Context Protocol servers
- `orchestration`: Multi-agent orchestration
- `tools`: Agent tools and capabilities
- `platforms`: Hosted agent platforms

## Topics

- `autogen`, `crewai`, `langgraph`, `llamaindex`
- `mcp`, `function-calling`, `rag`
- `multi-agent`, `autonomous`, `workflow`
