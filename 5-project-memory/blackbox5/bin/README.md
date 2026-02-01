# Blackbox5 Executables

This directory contains executable scripts and entry points for Blackbox5.

## Files

| File | Purpose |
|------|---------|
| `blackbox` | Bash wrapper for Blackbox5 CLI commands |
| `blackbox.py` | Main Python implementation |
| `start.sh` | Startup script for API and GUI servers |
| `ralf` | RALF daemon wrapper script |
| `ralf-loop.sh` | RALF autonomous loop implementation |
| `vibe_kanban_integration.py` | Vibe Kanban integration utilities |
| `ralf.md` | RALF prompt file (autonomous daemon) |

## Usage

### Blackbox5 CLI

```bash
./blackbox start          # Start Blackbox5
./blackbox stop           # Stop Blackbox5
./blackbox status         # Check status
./blackbox agents         # List all agents
./blackbox chat <msg>     # Send a message
```

### Start Script

```bash
./start.sh                # Start both API and GUI
./start.sh --api-only     # Start only API server
./start.sh --gui-only     # Start only Vibe Kanban GUI
./start.sh --full         # Start both (default)
```

### RALF Daemon

```bash
./ralf-loop.sh            # Run RALF autonomous loop
```

## Adding to PATH

To use these commands from anywhere:

```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="~/.blackbox5/bin:$PATH"
```

Then you can run:
```bash
blackbox start
start.sh --api-only
```

## Notes

- Scripts reference `../2-engine/`, `../3-gui/`, etc. (parent directory)
- Logs are written to `/tmp/blackbox5-*.log`
- PID tracking for background processes
