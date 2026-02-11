# Agent Base Integration Research

> **Research ID**: RESEARCH-001
> **Status**: Active
> **Created**: 2026-02-10
> **Updated**: 2026-02-10

---

## Executive Summary

Agent Base is a multi-agent orchestration canvas tool that we're integrating into BlackBox5. It provides a visual canvas for managing multiple AI coding agents (Claude Code, Cursor, etc.) with parallel execution, isolated edits, and progress tracking.

**Repository**: https://github.com/AgentOrchestrator/AgentBase
**Local Path**: `/Users/shaansisodia/agentbase`

---

## Current State

### Installation Status
- ✅ Cloned to `/Users/shaansisodia/agentbase`
- ✅ Built and packaged as macOS app
- ✅ Installed to `/Applications/Agent Base.app`
- ✅ Added Frame node feature (Figma-style colored backgrounds)

### Key Features (Out of Box)
- Visual canvas for agent organization
- Terminal nodes for shell access
- Agent nodes for Claude Code/Cursor integration
- Browser nodes for web browsing
- Session forking with git worktree isolation
- Canvas persistence (nodes, positions, viewport)

### Customizations Made

#### 1. Frame Node (NEW)
- Figma-style colored background containers
- 8 preset colors (Gray, Blue, Green, Purple, Red, Orange, Yellow, Pink)
- Resizable via corner handles
- Editable labels (click to rename)
- Color picker when selected
- Persists with canvas (position, size, color, label)

**Files Modified**:
- `apps/desktop/src/renderer/nodes/FrameNode/` (new)
- `apps/desktop/src/renderer/nodes/schemas.ts` (added FrameNodeDataSchema)
- `apps/desktop/src/renderer/nodes/registry.tsx` (registered frame type)
- `apps/desktop/src/renderer/services/CanvasNodeService.ts` (added createFrameNode)
- `apps/desktop/src/renderer/features/canvas/hooks/useCanvasActions.ts` (added addFrameNode)
- `apps/desktop/src/renderer/features/canvas/components/ContextMenu.tsx` (added menu item)

---

## Proposed Features

Based on user feedback and research, here are the features to implement:

### High Priority (Quick Wins)

#### 1. Global Agent Status Bar
**Purpose**: Show all active agents at a glance without switching views

**Features**:
- Fixed header showing color-coded status dots
- Quick hover preview showing current tool/operation
- Aggregate metrics (X running, Y awaiting input, Z errors)
- Click to jump to agent or center on canvas

**Status**: Planned

#### 2. Agent Grouping/Clusters
**Purpose**: Organize agents by project or task

**Features**:
- Visual grouping of related agents (e.g., "Feature X" containing 3 agents)
- Collapsible clusters showing aggregate status
- Group-level actions (pause all, resume all)
- Color-coded by project (use existing Frame colors)

**Status**: Planned - Use Frame nodes as project containers

#### 3. One-Click Terminal Creation
**Purpose**: Faster terminal creation

**Features**:
- Toolbar button to add terminal instantly
- Optional: Custom command on creation (e.g., auto-run `claude`)

**Status**: Planned

#### 4. Color-Coded Agent Status Indicators
**Purpose**: Visual feedback on agent state

**States**:
- 🟢 Green (running) - with pulse animation
- 🟡 Yellow (awaiting input)
- 🔴 Red (error)
- ⚪ Gray (idle)
- 🔵 Blue (thinking/streaming)

**Status**: Planned

#### 5. Editable Agent Names
**Purpose**: Easy identification of agents

**Features**:
- Click agent title to edit
- Auto-title from first prompt
- Manual override persists

**Status**: Already implemented in code, needs UI polish

### Medium Priority

#### 6. Minimap Navigation
**Purpose**: Navigate large canvases easily

**Features**:
- Small overview of canvas in corner
- Click to jump to location
- Shows viewport rectangle
- Zoom controls

**Status**: Research phase

#### 7. Canvas Search
**Purpose**: Find agents by name, status, or content

**Features**:
- Global search (Cmd+Shift+F)
- Filter by status type
- Highlight matching nodes
- Jump to results

**Status**: Research phase

#### 8. Quick Command Templates
**Purpose**: Pre-configured terminal commands

**Features**:
- Template list (e.g., "Claude Code", "Python REPL", "Node Console")
- Select on terminal creation
- User can add custom templates

**Status**: Planned

### Advanced (Future)

#### 9. Tmux Integration
**Purpose**: Keep terminals alive when app closes

**Features**:
- Each terminal runs in tmux session
- Sessions persist across app restarts
- Attach/detach from tmux sessions
- Session list view

**Status**: Research phase

#### 10. Context Linking
**Purpose**: Share context between agents

**Features**:
- Drag connections between agents
- "Share context" button
- Automatic context propagation
- Context diff view

**Status**: Research phase

#### 11. Diff View for Forked Agents
**Purpose**: Compare outputs from parallel agents

**Features**:
- Side-by-side comparison
- Highlight differences
- Merge UI
- Vote on best solution

**Status**: Research phase

---

## Technical Notes

### Build Process
```bash
# From /Users/shaansisodia/agentbase/apps/desktop
npm run build          # Build renderer
npm run build:main     # Build main process
npm run dist           # Package as .app
```

### Running
```bash
# Launch app
open -a "Agent Base"

# Or from terminal
~/agentbase/apps/desktop && npm run dev
```

### Database Location
- Production: `~/Library/Application Support/desktop/canvas-state.db`
- Stores: canvases, nodes, edges, viewport, settings

### Environment Configuration
- `.env.local` in app directory
- Configures AI data paths (Cursor, VS Code, Claude Code)

---

## Known Issues

1. **Canvas Persistence**: Nodes/positions not saving consistently
   - Database exists but nodes table is empty
   - May need to verify save trigger timing
   - Check if debounced save is firing

2. **Terminal Persistence**: Terminals close when app quits
   - This is by design (child process termination)
   - Tmux integration planned for v2

3. **App Icon**: Default Electron icon in use
   - Need to design and add custom icon

---

## Dependencies

### External
- Electron 39.0.0
- React 18.2.0
- @xyflow/react 12.9.2 (canvas)
- node-pty 1.1.0-beta35 (terminals)
- sqlite3 5.1.7 (persistence)

### Internal
- @agent-orchestrator/shared (shared types)

---

## Next Steps

1. ✅ Frame node - COMPLETED
2. 🔨 Global Agent Status Bar - Design UI
3. 🔨 Agent Grouping - Design using Frames
4. 🔨 One-Click Terminal - Add toolbar button
5. 🔨 Color-Coded Status - Add status indicators
6. 📋 Fix canvas persistence - Debug save mechanism
7. 📋 Tmux integration - Research approach

---

## References

- Agent Base Repo: https://github.com/AgentOrchestrator/AgentBase
- Multi-Agent Workflow Research: (see agent output above)
- Canvas App Patterns: (pending research)

---

**Last Updated**: 2026-02-10
**Next Review**: After implementing Status Bar
