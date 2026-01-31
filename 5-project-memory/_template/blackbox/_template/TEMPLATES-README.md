# BlackBox5 Templates

Global templates for the BlackBox5 autonomous agent system.

## Directory Structure

```
3-templates/
├── project-autonomous/          # Project initialization templates
│   ├── routes.yaml.template
│   ├── decision_registry.md.template
│   ├── communications/
│   │   ├── protocol.yaml.template
│   │   ├── queue.yaml.template
│   │   ├── events.yaml.template
│   │   ├── heartbeat.yaml.template
│   │   └── chat-log.yaml.template
│   ├── runs/
│   │   ├── THOUGHTS.md.template
│   │   ├── DECISIONS.md.template
│   │   ├── ASSUMPTIONS.md.template
│   │   ├── LEARNINGS.md.template
│   │   └── RESULTS.md.template
│   └── [directory structure only]
│       ├── tasks/active/
│       ├── tasks/completed/
│       ├── goals/completed/
│       ├── goals/templates/
│       ├── memory/insights/
│       ├── feedback/incoming/
│       ├── validations/
│       ├── workspaces/
│       └── timeline/
├── tasks/                       # Task templates (from BlackBox5)
│   ├── task-specification.md.template
│   ├── task-context-bundle.md.template
│   └── task-completion.md.template
├── epic/                        # Epic planning templates
│   ├── epic.md.template
│   ├── README.md.template
│   ├── ARCHITECTURE.md.template
│   └── ...
├── research/                    # 4D Research framework
│   ├── STACK.md.template
│   ├── FEATURES.md.template
│   ├── ARCHITECTURE.md.template
│   ├── PITFALLS.md.template
│   └── SUMMARY.md.template
├── decisions/                   # Decision record templates
│   ├── architectural.md.template
│   ├── technical.md.template
│   └── scope.md.template
└── root/                        # Project root file templates
    ├── STATE.yaml.template
    ├── ACTIVE.md.template
    └── ...
```

## Usage

### Initialize a New Project

```bash
# From anywhere
init-autonomous-project /path/to/your/project

# Or in current directory
init-autonomous-project
```

This creates the `.autonomous/` directory structure with all necessary files.

### Manual Template Usage

Copy and customize templates as needed:

```bash
cp ~/.blackbox5/3-templates/tasks/task-specification.md.template \
   ./TASK-001-my-task.md
```

## Template Variables

Templates use `{{VARIABLE_NAME}}` for substitution:

| Variable | Description |
|----------|-------------|
| `{{PROJECT_NAME}}` | Name of the project |
| `{{PROJECT_PATH}}` | Absolute path to project |
| `{{GITHUB_OWNER}}` | GitHub organization/user |
| `{{GITHUB_REPO}}` | GitHub repository name |
| `{{RUN_ID}}` | Unique run identifier |
| `{{TASK_ID}}` | Task identifier |
| `{{START_TIME}}` | ISO timestamp |

## Creating New Templates

1. Create `.template` file in appropriate directory
2. Use descriptive variable names
3. Include comments explaining purpose
4. Add example usage in this README

## Migration Notes

These templates were extracted from the BlackBox5 project structure and generalized for use across all projects in the SISO ecosystem.

### Key Differences from Legacy Structure

- **Unified naming**: All templates use `.template` extension
- **Consistent structure**: Same layout across all projects
- **Documented variables**: Clear substitution markers
- **Initialization script**: One-command project setup
