# GUI Integrations

External GUI projects and integrations that extend Blackbox5 capabilities.

## Overview

This directory contains external projects that integrate with Blackbox5's GUI layer. These are standalone projects with their own repositories, development workflows, and potentially different licensing.

## Integrations

### auto-claude

**Location**: `./auto-claude/`

Autonomous agent system providing AI-powered automation capabilities.

**Description**:
Auto-Claude is an external project that provides autonomous agent functionality for Claude Code. It enables:
- Automated task execution
- Multi-step workflow automation
- Intelligent context management
- Self-directed problem solving

**Structure**:
```
auto-claude/
├── auto-claude/           # Main application code
├── auto-claude-config/    # Configuration files
├── .auto-claude-security.json
└── .claude_settings.json
```

**External Documentation**:
- Project repository: External (linked in project)
- Setup instructions: See `auto-claude/README.md`
- Configuration: See `auto-claude-config/`

**Integration Points**:
- Hooks into Claude Code workflow
- Uses Blackbox5 memory systems
- Respects Blackbox5 safety controls

**Note**: This is an external project. Do not modify core auto-claude code here - changes should be made in the upstream repository and synced.

## Adding New Integrations

When adding new GUI integrations:

1. **Create a subdirectory** with the integration name
2. **Add a README.md** explaining:
   - What the integration does
   - How it connects to Blackbox5
   - Setup instructions
   - External documentation links
3. **Document boundaries** - what is external vs internal
4. **Update this README** with the new integration

## Security Considerations

Integrations may have different security models than Blackbox5:
- Review `.auto-claude-security.json` for auto-claude security settings
- Verify integration permissions before enabling
- Keep integration configurations in version control

## Development Workflow

For external integrations:
1. Treat as read-only unless you're the maintainer
2. Make changes in upstream repository
3. Sync updates via git subtree or similar
4. Test integration after updates

## Support

For integration-specific issues:
- Check integration's own documentation first
- Review integration-specific configuration
- Consult external project maintainers for core issues
