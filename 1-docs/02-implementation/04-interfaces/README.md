# Interface Implementation

> System interfaces and APIs

## Overview

This directory documents the interfaces exposed by BlackBox5, including CLI tools, APIs, webhooks, and integration points.

## Files

| File | Purpose |
|------|---------|
| `cli-reference.md` | Command-line interface documentation |
| `api-reference.md` | REST/GraphQL API documentation |
| `webhook-system.md` | Webhook integration guide |
| `mcp-integration.md` | Model Context Protocol integration |
| `event-formats.md` | Event structure specifications |

## Interface Types

- **CLI** - Command-line tools (`bb5` command family)
- **API** - Programmatic interfaces
- **Webhooks** - Event-driven integrations
- **MCP** - Model Context Protocol servers
- **Files** - YAML-based inter-process communication

## Versioning

Interfaces follow semantic versioning:
- Major changes → Breaking changes
- Minor changes → New features, backward compatible
- Patch changes - Bug fixes only

## Related Documentation

- [../01-core/README.md](../01-core/README.md) - Core implementation
- [../../03-guides/04-usage/README.md](../../03-guides/04-usage/README.md) - Usage guides

## Usage

Reference when building integrations or extending interfaces.
