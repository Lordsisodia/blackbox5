# Metadata Directory

This directory contains metadata for all Blackbox5 environment library artifacts following the AgentMD schema.

## Structure

```
.metadata/
├── INDEX.yaml                    # Master index of all artifacts
├── README.md                     # This file
├── generate-metadata.sh          # Metadata template generator
├── validate-metadata.sh          # Metadata validation script
├── auto-compact.sh.metadata.yaml
├── background-manager.sh.metadata.yaml
├── bmad-tracker.sh.metadata.yaml
└── ... (one per root-level script)
```

## AgentMD Schema

All metadata files follow the AgentMD schema defined at:
```
2-engine/03-knowledge/storage/brain/metadata/schema.yaml
```

## Using the Tools

### Generate New Metadata

```bash
# Generate metadata for a new library
./generate-metadata.sh -t library -n "My Library" -c utilities -p 2 -l execution my-lib

# Generate with dependencies
./generate-metadata.sh -t library -n "Analyzer" --depends-on context-vars my-analyzer

# Generate for a script
./generate-metadata.sh -t script -n "Build Script" -c build build-script
```

### Validate Metadata

```bash
# Validate all metadata in library
./validate-metadata.sh

# Validate recursively
./validate-metadata.sh -r

# Validate with verbose output
./validate-metadata.sh -v

# Fix common issues automatically
./validate-metadata.sh -f
```

## Metadata Organization

### Library Systems

Library systems have `metadata.yaml` in their own subdirectories:

```
lib/
├── context-variables/
│   └── metadata.yaml
├── hierarchical-tasks/
│   └── metadata.yaml
├── ralph-runtime/
│   └── metadata.yaml
└── ...
```

### Root-Level Scripts

Root-level scripts have metadata in `.metadata/` directory:

```
lib/
├── auto-compact.sh
├── background-manager.sh
└── .metadata/
    ├── auto-compact.sh.metadata.yaml
    ├── background-manager.sh.metadata.yaml
    └── ...
```

## Metadata Fields

Each metadata file includes:

- **Identification**: id, type, name, category, version
- **Location**: path, created, modified
- **Content**: description, tags, keywords
- **Relationships**: depends_on, used_by, relates_to
- **Classification**: phase, layer
- **Status**: status, stability
- **Ownership**: owner, maintainer
- **Documentation**: docs
- **Metrics**: usage_count, last_used, success_rate

## Artifact Types

Valid artifact types:
- agent, skill, plan, library, script, template
- document, test, config, module, framework, tool
- workspace, example

## Phases

- Phase 1: Foundation (context, utilities, shared libraries)
- Phase 2: Planning (task breakdown, spec creation, hierarchical tasks)
- Phase 3: Execution (circuit breaker, validation, integration)
- Phase 4: Autonomous (runtime, analysis, monitoring)

## Layers

- intelligence: Agent and skill definitions
- execution: Runtime and operational tools
- testing: Validation and testing utilities
- documentation: Documentation generation
- system: Core system utilities
- planning: Planning and workflow tools
- workspace: Workspace management

## Relationships

Relationship types between artifacts:
- implements: Implements a specification
- documents: Provides documentation
- tests: Tests or validates
- uses: Uses or depends on
- parallel: Parallel development
- extends: Extends functionality
- refines: Refines or improves
- deprecates: Replaces obsolete
- integrates: Integration point
- complements: Complementary functionality
- manages: Manages or controls

## Status Values

- active: In active use
- deprecated: Scheduled for removal
- archived: No longer maintained
- experimental: Experimental feature
- beta: Beta testing
- development: In development

## Stability Levels

- high: Production ready, stable API
- medium: Mostly stable, minor changes possible
- low: Under active development

## See Also

- AgentMD Schema: `2-engine/03-knowledge/storage/brain/metadata/schema.yaml`
- Metadata Examples: `2-engine/03-knowledge/storage/brain/metadata/examples/`
- Brain Storage: `2-engine/03-knowledge/storage/brain/README.md`
