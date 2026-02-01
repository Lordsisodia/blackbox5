# Development Tests

Test suite for the Blackbox5 engine.

## Structure

```
tests/
├── unified/    # General test files (organized by type)
└── numbers/    # Ordered test suites (numbered execution)
```

## Unified Tests (`unified/`)

27 general test files organized by category:

### Agent Tests
- test_agent_client.py - Agent client functionality
- test_agent_integration.py - Agent integration tests
- test_agent_memory.py - Agent memory system tests

### Integration Tests
- test_github_integration.py - GitHub integration
- test_mcp_integration.py - MCP integration
- test_vibe_integration.py - Vibe integration
- test_blackbox5_integration.py - Blackbox5 integration

### System Tests
- test_glm_api.py - GLM API tests
- test_orchestrator.py - Orchestrator tests
- test_state_manager.py - State manager tests
- test_workflow.py - Workflow tests

### Utilities
- conftest.py - Pytest configuration
- pytest.ini - Pytest settings
- run_tests.sh - Test runner script

## Numbered Tests (`numbers/`)

11 numbered test suites for ordered execution:

1. test_anti_pattern_detection.py
2. test_atomic_commits.py
3. test_checkpoint_protocol.py
4. test_context_extraction.py
5. test_deviation_handling.py
6. test_memory_system.py
7. test_pipeline_integration.py
8. test_pipeline.py
9. test_state_manager.py
10. test_todo_manager.py
11. test_token_compression.py
12. test_wave_execution.py

## Running Tests

```bash
# Run all unified tests
cd tests/unified && pytest

# Run specific test
pytest tests/unified/test_agent_client.py

# Run numbered tests in order
pytest tests/numbers/ -v

# Run with coverage
pytest --cov=.
```

## Test Documentation

- [unified/README.md](unified/README.md) - Unified test documentation
- [TEST-SUMMARY.md](unified/TEST-SUMMARY.md) - Test summary (archived)

## File Count

- **Unified**: ~27 test files
- **Numbers**: 12 test files
- **Total**: ~39 test files
