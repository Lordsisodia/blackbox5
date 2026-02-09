#!/bin/bash
# RALF Agent Entrypoint
# Runs the autonomous RALF improvement loop

set -e

echo "═══════════════════════════════════════════════════════════"
echo "  RALF Agent Starting"
echo "  Project: $RALF_PROJECT_DIR"
echo "  Mode: $RALF_MODE"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Verify required environment
if [[ -z "$ANTHROPIC_API_KEY" ]]; then
    echo "ERROR: ANTHROPIC_API_KEY not set"
    exit 1
fi

# Setup SSH for GitHub
if [[ -d "$HOME/.ssh" ]]; then
    chmod 700 "$HOME/.ssh"
    if [[ -f "$HOME/.ssh/id_ed25519" ]]; then
        chmod 600 "$HOME/.ssh/id_ed25519"
        # Add GitHub to known hosts
        ssh-keyscan github.com >> "$HOME/.ssh/known_hosts" 2>/dev/null || true
    fi
fi

# Configure git
git config --global user.email "ralf@blackbox5.local"
git config --global user.name "RALF Agent"
git config --global init.defaultBranch main

# Wait for Blackbox5 code to be available (mounted via PVC)
echo "Waiting for Blackbox5 code..."
for i in {1..30}; do
    if [[ -f "$RALF_BLACKBOX5_DIR/bin/ralf" ]]; then
        echo "✓ Blackbox5 found"
        break
    fi
    echo "  ($i/30) Waiting..."
    sleep 2
done

if [[ ! -f "$RALF_BLACKBOX5_DIR/bin/ralf" ]]; then
    echo "ERROR: Blackbox5 not found at $RALF_BLACKBOX5_DIR"
    echo "Expected bin/ralf to exist"
    exit 1
fi

# Create required directories
mkdir -p "$RALF_PROJECT_DIR/.autonomous/runs"
mkdir -p "$RALF_PROJECT_DIR/.autonomous/LOGS"
mkdir -p "$RALF_PROJECT_DIR/.autonomous/memory"
mkdir -p "$RALF_PROJECT_DIR/.autonomous/tasks/active"
mkdir -p "$RALF_PROJECT_DIR/.autonomous/tasks/completed"

echo ""
echo "Starting RALF loop..."
echo "This will run continuously, improving Blackbox5"
echo ""

# Change to Blackbox5 directory
cd "$RALF_BLACKBOX5_DIR"

# Run RALF in daemon mode
# The ralf script will use claude-code with the prompt file
exec bash "$RALF_BLACKBOX5_DIR/bin/ralf" "$RALF_PROJECT_DIR"
