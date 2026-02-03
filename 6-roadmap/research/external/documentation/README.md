# External Documentation

Centralized storage for external documentation sources (API docs, SDK guides, specifications, etc.)

## Purpose

Provide agents with structured, searchable access to key external documentation for:
- API reference and integration patterns
- SDK usage and best practices
- Protocol specifications
- Framework guides

## Contents

| Source | Description | Status | Pages |
|--------|-------------|--------|-------|
| `claude-code/` | Claude Code official documentation | Active | 53/53 (100%) |

## Adding New Documentation

1. Create folder: `{source-name}/`
2. Copy `TEMPLATE/` structure
3. Update `SOURCES.yaml`
4. Run ingestion

## Quick Access

Agents should use this pattern:
```yaml
# 1. Check what's available
README.md (this file)

# 2. Go to specific source
{source}/README.md          # Source metadata
{source}/extracted/         # Processed content
{source}/quick-reference.md # Key facts
```

## Source Registry

See `SOURCES.yaml` for complete list of all documentation sources.
