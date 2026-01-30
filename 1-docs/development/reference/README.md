# Development Reference

Reference materials for Blackbox5 development including framework comparisons, research analysis, templates, and tools.

## Structure

```
reference/
├── frameworks/    # Framework comparisons and implementations
├── research/      # Research analysis and notes
├── templates/     # Document templates
└── tools/         # Development utilities
```

## Frameworks (`frameworks/`)

Comparative analysis of agent frameworks:

| Framework | Files | Description |
|-----------|-------|-------------|
| [1-bmad/](frameworks/1-bmad/) | ~15 | BlackBox Multi-Agent Development |
| [2-speckit/](frameworks/2-speckit/) | ~12 | Spec-driven development kit |
| [3-metagpt/](frameworks/3-metagpt/) | ~10 | Multi-agent framework analysis |
| [4-swarm/](frameworks/4-swarm/) | ~8 | OpenAI Swarm patterns |

Each framework includes:
- README.md - Overview and key concepts
- Research notes and analysis
- Implementation patterns
- Examples (where applicable)

## Research (`research/`)

Analysis of external frameworks and technologies (~60 files):

### Framework Analysis
- Agentscope, CrewAI, AutoGen comparisons
- BMAD method deep-dive
- DeerFlow, MetaGPT, Swarm analysis
- Google ADK, LangChain evaluations

### Snippets (`research/snippets/`)
Research artifacts organized by type:
- [feature-maps/](research/snippets/feature-maps/) - Feature mapping documents
- [query-banks/](research/snippets/query-banks/) - Query pattern collections

## Templates (`templates/`)

Document templates for scaffolding:

### Specs (`templates/specs/`)
- PRD template (Product Requirements Document)
- Epic template (Epic specifications)
- Task template (Task definitions)

### General (`templates/general/`)
- Agent context template
- GitHub templates (issues, progress, completion)

## Tools (`tools/`)

Development utility scripts:

### Setup (`tools/setup/`)
- setup-memory-bank.sh - Initialize memory bank

### Verification (`tools/verification/`)
- verify-setup.sh - Verify engine setup
- verify_skills.py - Verify skills configuration

## Usage

1. **Comparing frameworks**: Browse `frameworks/`
2. **Researching approaches**: Check `research/`
3. **Creating documents**: Use `templates/`
4. **Setting up environment**: Run `tools/setup/`

## File Count

- **Frameworks**: ~45 files
- **Research**: ~60 files
- **Templates**: ~15 files
- **Tools**: ~10 files
- **Total**: ~130 files
