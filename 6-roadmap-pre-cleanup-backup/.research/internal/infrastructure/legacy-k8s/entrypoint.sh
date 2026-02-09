#!/bin/bash
# Legacy Agent Entrypoint
# Runs the autonomous Legacy improvement loop with proper system prompt

set -e

echo "═══════════════════════════════════════════════════════════"
echo "  Legacy Agent Starting"
echo "  Project: $LEGACY_PROJECT_DIR"
echo "  Mode: $LEGACY_MODE"
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
        ssh-keyscan github.com >> "$HOME/.ssh/known_hosts" 2>/dev/null || true
    fi
fi

# Configure git
git config --global user.email "legacy@blackbox5.local"
git config --global user.name "Legacy Agent"
git config --global init.defaultBranch main

# Wait for Blackbox5 code to be available
echo "Waiting for Blackbox5 code..."
for i in {1..60}; do
    if [[ -f "$LEGACY_BLACKBOX5_DIR/bin/legacy" ]]; then
        echo "✓ Blackbox5 found"
        break
    fi
    echo "  ($i/60) Waiting..."
    sleep 2
done

if [[ ! -f "$LEGACY_BLACKBOX5_DIR/bin/legacy" ]]; then
    echo "ERROR: Blackbox5 not found at $LEGACY_BLACKBOX5_DIR"
    exit 1
fi

# Create required directories
mkdir -p "$LEGACY_PROJECT_DIR/.autonomous/runs"
mkdir -p "$LEGACY_PROJECT_DIR/.autonomous/LOGS"
mkdir -p "$LEGACY_PROJECT_DIR/.autonomous/memory"
mkdir -p "$LEGACY_PROJECT_DIR/.autonomous/tasks/active"
mkdir -p "$LEGACY_PROJECT_DIR/.autonomous/tasks/completed"

echo ""
echo "Starting Legacy loop..."
echo "This will run continuously, improving Blackbox5"
echo ""

# Change to Blackbox5 directory
cd "$LEGACY_BLACKBOX5_DIR"

# Check if system prompt file exists
SYSTEM_PROMPT_FILE="/etc/legacy/legacy.md"
if [[ -f "$SYSTEM_PROMPT_FILE" ]]; then
    echo "Using system prompt: $SYSTEM_PROMPT_FILE"
    echo ""
    # Run Legacy with system prompt
    exec claude -p --system-prompt "$SYSTEM_PROMPT_FILE" < /dev/null
else
    echo "No system prompt file found, using default"
    echo ""
    # Run Legacy without explicit system prompt
    exec bash "$LEGACY_BLACKBOX5_DIR/bin/legacy" "$LEGACY_PROJECT_DIR"
fi
