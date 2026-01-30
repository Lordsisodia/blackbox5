# 3-gui: GUI Layer

The GUI layer for Blackbox5 - containing applications, shared components, and integrations.

## Overview

This directory contains all user interface implementations for the Blackbox5 ecosystem. It follows a modular architecture separating applications, shared components, and external integrations.

## Directory Structure

```
3-gui/
├── README.md              # This file
├── apps/                  # GUI applications
│   └── vibe-kanban/       # Rust/Tauri Kanban board application
├── components/            # Shared UI components (future)
├── docs/                  # GUI-specific documentation
└── integrations/          # External GUI integrations
    └── auto-claude/       # Auto-Claude integration (external project)
```

## Applications

### vibe-kanban

**Location**: `apps/vibe-kanban/`

A full-featured Kanban board application built with:
- **Backend**: Rust (Tauri)
- **Frontend**: React + TypeScript
- **Build System**: Cargo + npm/pnpm

**Key Features**:
- Drag-and-drop task management
- Real-time collaboration support
- Cross-platform desktop app (via Tauri)
- Modern React patterns with TypeScript

**Development**:
```bash
cd apps/vibe-kanban
# Install dependencies
pnpm install
# Run development server
pnpm tauri dev
# Build for production
pnpm tauri build
```

**Documentation**: See `apps/vibe-kanban/README.md` and `apps/vibe-kanban/docs/`

## Shared Components

**Location**: `components/`

Future location for shared UI components that can be reused across multiple GUI applications. Currently empty - to be populated as the GUI ecosystem grows.

Planned components:
- Common UI primitives (buttons, inputs, modals)
- Blackbox5-specific widgets (agent status, task cards)
- Theme system and design tokens

## Integrations

**Location**: `integrations/`

External GUI projects and integrations that work with Blackbox5.

### auto-claude

**Location**: `integrations/auto-claude/`

External Auto-Claude project providing autonomous agent capabilities.

**Note**: This is an external project integrated into Blackbox5. See `integrations/README.md` for details.

## Documentation

**Location**: `docs/`

GUI-specific documentation including:
- Architecture decisions
- Component guidelines
- Integration patterns
- Development workflows

## Development Setup

### Prerequisites

- Node.js 18+ (for web-based apps)
- Rust toolchain (for Tauri apps)
- pnpm (preferred package manager)

### Getting Started

1. **For vibe-kanban development**:
   ```bash
   cd apps/vibe-kanban
   pnpm install
   pnpm tauri dev
   ```

2. **For integration development**:
   ```bash
   cd integrations/auto-claude
   # Follow integration-specific setup
   ```

## Architecture Notes

### Application Isolation

Each app in `apps/` is self-contained with its own:
- Build configuration
- Dependencies
- Documentation
- Testing setup

### Shared Resources

The `components/` directory will eventually house shared UI resources. Until then, apps should:
- Keep components internal
- Document any components that could be shared
- Follow consistent naming conventions

### Integration Boundaries

Integrations in `integrations/` are external projects:
- May have different licensing
- Have their own development workflows
- Should be treated as black boxes with defined interfaces

## Future Plans

- [ ] Populate `components/` with shared UI primitives
- [ ] Create design system documentation in `docs/`
- [ ] Add web-based GUI alternatives
- [ ] Implement component testing framework
- [ ] Create GUI development guidelines

## Related Documentation

- [vibe-kanban README](apps/vibe-kanban/README.md)
- [Integrations README](integrations/README.md)
- [System Map](../SYSTEM-MAP.yaml) - Complete system structure
