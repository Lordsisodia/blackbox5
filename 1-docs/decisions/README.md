# Decisions

This directory contains Architecture Decision Records (ADRs) and design decisions for the Blackbox5 project.

## What are ADRs?

Architecture Decision Records capture:
- **Context**: Why a decision was needed
- **Decision**: What was decided
- **Consequences**: Trade-offs and impacts

## Naming Convention

Decision files follow the pattern:
```
NNNN-title-in-kebab-case.md
```

Where `NNNN` is a sequential number (e.g., `0001`, `0002`).

## Structure

Each decision should include:
1. **Status**: proposed, accepted, deprecated, superseded
2. **Context**: Background and problem statement
3. **Decision**: The decision that was made
4. **Consequences**: Positive and negative impacts
5. **Alternatives**: Options considered and why rejected

## Current Decisions

### adr/
Architecture Decision Records.
- [README](adr/README.md) - ADR overview

### infrastructure/
Infrastructure and deployment decisions.
- [HYBRID-MCP-ARCHITECTURE.md](infrastructure/HYBRID-MCP-ARCHITECTURE.md) - Hybrid MCP architecture
- [HYBRID-MCP-IMPLEMENTATION.md](infrastructure/HYBRID-MCP-IMPLEMENTATION.md) - Hybrid MCP implementation
- [CORE-COMPONENTS.md](infrastructure/CORE-COMPONENTS.md) - Core components
- [EXECUTION-STATUS.md](infrastructure/EXECUTION-STATUS.md) - Execution status
- [Airis-resource-usage.md](infrastructure/Airis-resource-usage.md) - Airis resource usage

### mcp/
Model Context Protocol decisions.
- [MCP-STRATEGY-DECISION.md](mcp/MCP-STRATEGY-DECISION.md) - MCP strategy
- [MCP-GATEWAY-SOLUTION.md](mcp/MCP-GATEWAY-SOLUTION.md) - MCP gateway
- [MCP-CONTEXT-OPTIMIZATION.md](mcp/MCP-CONTEXT-OPTIMIZATION.md) - Context optimization
- [ONE-MCP-SMART-GATEWAY.md](mcp/ONE-MCP-SMART-GATEWAY.md) - Smart gateway
- [MCP-TOKEN-OPTIMIZATION-BEST-FRAMEWORK.md](mcp/MCP-TOKEN-OPTIMIZATION-BEST-FRAMEWORK.md) - Token optimization
- And more...

### process/
Decision-making processes.
- [README](process/README.md) - Decision process overview

### rfcs/
Requests for Comments.
- [README](rfcs/README.md) - RFC overview

### roadmap/
Roadmap and planning decisions.
- [ROADMAP-MEMORY-REORGANIZATION.md](roadmap/ROADMAP-MEMORY-REORGANIZATION.md) - Memory reorganization
- [ROADMAP-TO-MEMORY-MIGRATION-MAP.md](roadmap/ROADMAP-TO-MEMORY-MIGRATION-MAP.md) - Migration map

## Contributing

When recording a decision:
1. Use the next available number
2. Follow the template structure
3. Link to related decisions
4. Update status when decisions change
