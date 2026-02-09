# Architecture Decision Records

> ADRs documenting major architectural decisions

## Overview

This directory contains Architecture Decision Records (ADRs) documenting significant architectural decisions made in the BlackBox5 project.

## Format

Each ADR follows this structure:
```markdown
# ADR-XXX: Title

## Status
Proposed | Accepted | Deprecated | Superseded

## Context
What is the issue that we're seeing?

## Decision
What is the change that we're proposing?

## Consequences
What becomes easier or more difficult?
```

## Current ADRs

| ADR | Title | Status |
|-----|-------|--------|
| ADR-001 | Use YAML for Agent Communication | Accepted |
| ADR-002 | Dual-Agent Architecture | Accepted |
| ADR-003 | File-Based Event System | Accepted |
| ADR-004 | Hierarchical Task Structure | Accepted |

## Creating New ADRs

1. Copy `adr-template.md`
2. Fill in all sections
3. Submit for review
4. Update status after decision

## Related Documentation

- [../rfcs/README.md](../rfcs/README.md) - Request for Comments
- [../../01-theory/03-patterns/README.md](../../01-theory/03-patterns/README.md) - Design patterns

## Usage

Read ADRs to understand why the system is designed the way it is.
