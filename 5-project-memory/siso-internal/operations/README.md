# Operations

> Operational dashboards, monitoring, and procedures for SISO-Internal

## Overview

This directory contains operational dashboards, quality gates, metrics tracking, and procedures for maintaining and operating the SISO-Internal project.

## Dashboard Files

### Core Dashboards

| File | Purpose | Size |
|------|---------|------|
| `skill-registry.yaml` | Unified skill registry with metrics and usage tracking | 4.3KB |
| `quality-gates.yaml` | Quality gate definitions for task completion | 3.2KB |
| `metrics-dashboard.yaml` | Project and agent metrics tracking | 2.1KB |
| `executor-dashboard.yaml` | Run monitoring and performance metrics | 12KB |
| `improvement-pipeline.yaml` | Learning to implementation pipeline | 11KB |
| `project-map.yaml` | Cross-project dependencies and relationships | 14KB |

### Guidelines & Checklists

| File | Purpose | Size |
|------|---------|------|
| `testing-guidelines.yaml` | TDD workflow and testing standards | 12KB |
| `context-gathering.yaml` | Context optimization and path validation | 12KB |
| `estimation-guidelines.md` | Task time estimation with multipliers | 7.6KB |
| `validation-checklist.yaml` | Pre-execution validation checks | 6.3KB |
| `workflow-integration-checklist.yaml` | Workflow integration verification | 9.3KB |
| `agent-setup-checklist.yaml` | Agent version setup procedures | 8.6KB |

### Reports & Audits

| File | Purpose | Size |
|------|---------|------|
| `documentation-audit.yaml` | Documentation freshness and references | 5.4KB |
| `run-validation.yaml` | Run folder documentation validation | 4.7KB |
| `quality-gate-report.yaml` | CI/CD quality metrics tracking | 4.1KB |

## Quick Navigation

### For Task Execution

1. Start with `validation-checklist.yaml` - Pre-execution validation
2. Reference `estimation-guidelines.md` - Time estimation
3. Check `context-gathering.yaml` - Optimize context gathering
4. Follow `testing-guidelines.yaml` - Testing standards

### For Quality Assurance

1. Review `quality-gates.yaml` - Quality gate definitions
2. Check `quality-gate-report.yaml` - Current quality status
3. Reference `run-validation.yaml` - Run documentation validation

### For Process Improvement

1. Check `improvement-pipeline.yaml` - Improvement workflow
2. Review `executor-dashboard.yaml` - Performance metrics
3. Reference `metrics-dashboard.yaml` - Project metrics

### For Cross-Project Work

1. Check `project-map.yaml` - Project dependencies
2. Reference `context-gathering.yaml` - Cross-project heuristics

## Directory Structure

```
operations/
├── Dashboards
│   ├── skill-registry.yaml          # Skill metrics and registry
│   ├── metrics-dashboard.yaml       # Project metrics
│   ├── executor-dashboard.yaml      # Run monitoring
│   ├── improvement-pipeline.yaml    # Learning pipeline
│   └── quality-gate-report.yaml     # Quality metrics
│
├── Guidelines
│   ├── testing-guidelines.yaml      # TDD and testing
│   ├── estimation-guidelines.yaml   # Time estimation
│   └── context-gathering.yaml       # Context optimization
│
├── Checklists
│   ├── validation-checklist.yaml    # Pre-execution checks
│   ├── workflow-integration-checklist.yaml  # Workflow verification
│   └── agent-setup-checklist.yaml   # Agent setup
│
├── Reports
│   ├── documentation-audit.yaml     # Documentation health
│   ├── run-validation.yaml          # Run validation config
│   └── quality-gate-report.yaml     # Quality tracking
│
└── README.md                        # This file
```

## Usage Patterns

### Before Starting a Task

```bash
# 1. Check validation checklist
cat operations/validation-checklist.yaml

# 2. Review estimation guidelines
cat operations/estimation-guidelines.yaml

# 3. Check context gathering config
cat operations/context-gathering.yaml
```

### During Task Execution

```bash
# Check testing guidelines
cat operations/testing-guidelines.yaml

# Reference quality gates
cat operations/quality-gates.yaml
```

### After Task Completion

```bash
# Update metrics dashboard
# (Automated via task completion)

# Check improvement pipeline
cat operations/improvement-pipeline.yaml
```

## Integration with BlackBox5

SISO-Internal operations dashboards are designed to align with BlackBox5 structure while being specific to SISO-Internal needs:

- **Shared patterns**: Both use YAML for structured data
- **Cross-references**: `project-map.yaml` documents relationships
- **Consistent structure**: Similar file naming and organization
- **SISO-specific**: Tailored to SISO-Internal project requirements

## Maintenance

- **Update frequency**: Dashboards update per-run or as-needed
- **Version tracking**: Each file has version metadata
- **Changelog**: Major changes documented in file headers
- **Review cycle**: Review monthly for accuracy

## Related Documentation

- `STATE.yaml` - Project state and navigation
- `.autonomous/` - Autonomous task management
- `2-engine/.autonomous/` - BMAD skills and workflows
