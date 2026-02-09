# 08-Development

Development, testing, and reference materials for the BlackBox5 Engine.

## Structure

This folder contains everything needed to develop with, test, and understand the engine.

```
development/
├── ci-cd/                  # CI/CD workflows and setup
├── examples/               # Usage examples
│   ├── agents/             # Agent examples
│   ├── basic/              # Basic examples
│   ├── integrations/       # Integration examples
│   └── workflows/          # Workflow examples
├── prompt-compression/     # LLMLingua and compression research
├── reference/              # Reference material
│   ├── frameworks/         # Framework comparisons (BMAD, SpecKit, MetaGPT, Swarm)
│   ├── templates/          # Document templates
│   │   ├── general/        # General templates
│   │   │   └── github/     # GitHub templates
│   │   └── specs/          # Specification templates
│   │       ├── epics/      # Epic templates
│   │       ├── prds/       # PRD templates
│   │       └── tasks/      # Task templates
│   └── tools/              # Development tools
│       ├── setup/          # Setup scripts
│       └── verification/   # Verification scripts
├── security/               # Security documentation
└── tests/                  # Test suite
    ├── numbers/            # Numbered test suites
    └── unified/            # Unified test suite
```

## Tests (`tests/`)

All testing for the engine, organized by type.

### Unified Tests (`tests/unified/`)
27 general test files covering:
- Agent tests (client, integration, memory)
- Integration tests (GitHub, MCP, Vibe, BlackBox5)
- System tests (GLM API, orchestrator, state manager, workflow)
- Utilities (conftest.py, pytest.ini, run_tests.sh)

### Numbered Tests (`tests/numbers/`)
11 numbered test suites for ordered execution:
- test_anti_pattern_detection.py
- test_atomic_commits.py
- test_checkpoint_protocol.py
- test_context_extraction.py
- test_deviation_handling.py
- test_memory_system.py
- test_pipeline_integration.py
- test_pipeline.py
- test_state_manager.py
- test_todo_manager.py
- test_token_compression.py
- test_wave_execution.py

### Running Tests

```bash
# Run all tests
cd tests/unified && pytest

# Run specific test
pytest tests/unified/test_agent_client.py

# Run numbered tests
pytest tests/numbers/
```

## Examples (`examples/`)

Code examples showing how to use the engine.

### Available Examples

**Basic** (`examples/basic/`)
- Getting started with engine tools

**Agents** (`examples/agents/`)
- Orchestrator demonstration

**Workflows** (`examples/workflows/`)
- Epic creation demo (PRD → Epic transformation)

**Integrations** (`examples/integrations/`)
- MCP integration example

**Advanced** (`examples/advanced/`)
- Complex usage patterns (to be populated)

## Reference (`reference/`)

Reference material for development.

### Frameworks (`reference/frameworks/`)

Reference implementations of agent frameworks:

1. **BMAD** - BlackBox Multi-Agent Development
2. **SpeckKit** - Spec-driven development kit
3. **MetaGPT** - Multi-agent framework
4. **Swarm** - OpenAI Swarm patterns

Each framework includes:
- README.md - Overview
- RESEARCH.md - Research notes
- Implementation files

### Templates (`reference/templates/`)

Document templates for scaffolding:

**Specs** (`templates/specs/`)
- PRD template (Product Requirements Document)
- Epic template (Epic specifications)
- Task template (Task definitions)

**General** (`templates/general/`)
- Agent context template
- GitHub templates (issues, progress, completion)

### Research (`reference/research/`)

Analysis of external frameworks (21 documents):
- Agentscope analysis
- BMAD method analysis
- DeerFlow analysis
- MetaGPT analysis
- Swarm analysis
- Google ADK analysis
- And more...

### Tools (`reference/tools/`)

Development utility scripts:

**Setup** (`tools/setup/`)
- setup-memory-bank.sh - Initialize memory bank

**Verification** (`tools/verification/`)
- verify-setup.sh - Verify engine setup
- verify_skills.py - Verify skills configuration

## Quick Start

1. **Run tests**: `cd tests/unified && pytest`
2. **Try an example**: `python examples/agents/orchestrator_demo.py`
3. **Use a template**: Copy from `reference/templates/specs/`
4. **Read framework docs**: Check `reference/frameworks/`

## File Counts

- **Tests**: 48 files
- **Examples**: 5 files (growing)
- **Reference**: 56 files

## Principles

1. **Three purposes**: Tests, Examples, Reference
2. **Clear names**: Each folder has one clear purpose
3. **No duplicates**: Everything has one place
4. **Scalable**: Easy to add new content

## Subsections

### ci-cd/
GitHub Actions workflows for CI/CD.
- [SETUP.md](ci-cd/SETUP.md) - CI/CD setup guide

### examples/
Code examples showing how to use the engine.
- [agents/](examples/agents/) - Agent examples
- [basic/](examples/basic/) - Basic examples
- [integrations/](examples/integrations/) - Integration examples
- [workflows/](examples/workflows/) - Workflow examples

### prompt-compression/
LLMLingua and prompt compression research.
- [HUGGINGFACE-SETUP.md](prompt-compression/HUGGINGFACE-SETUP.md)
- [LLMLINGUA-REQUIREMENTS.md](prompt-compression/LLMLINGUA-REQUIREMENTS.md)
- [LLMLINGUA-SETUP-GUIDE.md](prompt-compression/LLMLINGUA-SETUP-GUIDE.md)

### reference/
Reference material for development.
- [frameworks/](reference/frameworks/) - Framework comparisons (BMAD, SpecKit, MetaGPT, Swarm)
- [templates/](reference/templates/) - Document templates
- [tools/](reference/tools/) - Development utility scripts

### security/
Security documentation.
- [credential-management.md](security/credential-management.md)

### tests/
All testing for the engine.
- [numbers/](tests/numbers/) - Numbered test suites
- [unified/](tests/unified/) - Unified test suite

## Related

- Engine code: `../02-implementation/01-core/`, `../02-implementation/01-agents/`
- Project memory: `../../5-project-memory/`
- Documentation: `../../1-docs/`
