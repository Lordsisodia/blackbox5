# Archived Files

These files were moved during rapid implementation on 2026-02-10.
They are preserved for reference but not actively used.

## Moved Files

- agent-spawner.py.LEGACY - Fake agent spawning (creates files only, never spawns agents)
- ralf-core-with-agent-teams.sh.LEGACY - References non-existent agents
- ralf-six-agent-pipeline.sh.LEGACY - References non-existent agents

## Why Moved

These files created confusion by appearing functional but not actually working.
The new system uses real agent spawning via Task tool.

## New System

See: bin/ralf-executor/ci-orchestrator.py
