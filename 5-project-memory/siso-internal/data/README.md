# Data

**Purpose:** Project-specific data storage and working files

## Structure

```
data/
├── archival/          # Archived historical data
│   ├── projects/      # Archived project snapshots
│   └── sessions/      # Archived session data
├── brain/             # Knowledge graph data
│   ├── databases/     # Graph database files
│   └── metadata/      # Knowledge metadata
├── embeddings/        # Vector embeddings storage
│   ├── chroma-db/     # Chroma vector database
│   └── entities/      # Entity embeddings
├── episodes/          # Episodic memory data
├── memory-bank/       # Memory bank storage
└── working/           # Working data
    ├── agents/        # Agent working data
    ├── compact/       # Compact/compressed data
    ├── handoffs/      # Handoff data
    ├── kanban/        # Kanban board data
    └── shared/        # Shared working data
```

## Usage

### Archival
Store historical snapshots and session data that is no longer active but may be needed for reference.

### Brain
Knowledge graph storage for entity relationships and semantic connections.

### Embeddings
Vector embeddings for semantic search and similarity matching.

### Episodes
Episodic memory storage for agent experiences and interactions.

### Memory Bank
Active memory bank files for the autonomous agent system.

### Working
Temporary and working data that changes frequently during operations.

## Quick Navigation

```bash
# List all data folders
ls -la data/

# Check archival storage
ls -la data/archival/

# View memory bank
ls -la data/memory-bank/
```
