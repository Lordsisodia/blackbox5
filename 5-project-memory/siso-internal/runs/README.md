# Runs

**Purpose:** Execution run folders

## Structure

```
runs/
├── run-YYYYMMDD_HHMMSS/     # Individual run folders
│   ├── THOUGHTS.md          # Session thinking
│   ├── DECISIONS.md         # Decisions made
│   ├── RESULTS.md           # Outcomes
│   ├── LEARNINGS.md         # Insights
│   └── ASSUMPTIONS.md       # Assumptions made
├── archived/                # Archived runs
├── current/                 # Current active run
└── README.md               # This file
```

## Run Naming Convention

Format: `run-YYYYMMDD_HHMMSS`

Examples:
- `run-20260118_143000` - User Profile PRD Creation
- `run-20260118_160000` - User Profile Epic Creation
- `run-20260119_100000` - Project Memory Migration
- `run-20260119_140000` - GitHub Sync Operation
- `run-20260209_143000` - BlackBox5 Structure Alignment

## Run Types

### Feature Planning
Research and planning for new features. Creates PRDs, research documents.

**Example:** `run-20260118_143000` - User Profile PRD Creation
- Created comprehensive PRD with 8 FRs, 6 NFRs, 43 ACs
- 2 hours invested

### Architecture
Technical design and architecture decisions. Creates epics, task breakdowns.

**Example:** `run-20260118_160000` - User Profile Epic Creation
- Created technical specification
- Broke down into 18 atomic tasks

### Infrastructure
System and infrastructure changes. Reorganizations, migrations, setups.

**Example:** `run-20260119_100000` - Project Memory Migration
- Reorganized from 18 to 6 folders
- 67% reduction in folder count

### GitHub Integration
Sync operations with GitHub. Issue creation, PR management.

**Example:** `run-20260119_140000` - GitHub Sync Operation
- Synced epic and 18 tasks to GitHub
- Created 19 issues with labels

### Alignment
Bringing project structure in line with standards.

**Example:** `run-20260209_143000` - BlackBox5 Structure Alignment
- Created data/, learnings/, runs/ structures
- Populated with example content

## Run Files

### THOUGHTS.md
Session thinking, approach, progress tracking.

### DECISIONS.md
Technical, architectural, and scope decisions made during the run.

### RESULTS.md
Deliverables, metrics, validation checklist.

### LEARNINGS.md
What worked well, challenges, patterns discovered.

### ASSUMPTIONS.md
Assumptions made and validation needed.

## Quick Navigation

```bash
# List all runs
ls -la runs/

# View recent run
cat runs/run-20260209_143000/RESULTS.md

# Check current run
ls -la runs/current/

# View archived runs
ls -la runs/archived/
```

## Creating a New Run

1. Create folder: `mkdir runs/run-YYYYMMDD_HHMMSS`
2. Copy template files from `.templates/runs/`
3. Update THOUGHTS.md with initial context
4. Document decisions in DECISIONS.md
5. Record results in RESULTS.md
6. Capture learnings in LEARNINGS.md
7. Note assumptions in ASSUMPTIONS.md
