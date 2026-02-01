#!/bin/bash
# RALF Agent Entrypoint for Kubernetes
# Handles initialization and runs the RALF loop

set -e

echo "═══════════════════════════════════════════════════════════"
echo "  Blackbox5 RALF Agent - Kubernetes"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Configuration
RALF_MODE="${RALF_MODE:-daemon}"
RALF_PROJECT_DIR="${RALF_PROJECT_DIR:-/opt/blackbox5/5-project-memory/blackbox5}"
RALF_ENGINE_DIR="${RALF_ENGINE_DIR:-/opt/blackbox5/2-engine/.autonomous}"
RALF_BLACKBOX5_DIR="${RALF_BLACKBOX5_DIR:-/opt/blackbox5}"
RALF_AGENT_ID="${RALF_AGENT_ID:-ralf-$(hostname)}"

echo "Agent ID: $RALF_AGENT_ID"
echo "Mode: $RALF_MODE"
echo "Project: $RALF_PROJECT_DIR"
echo ""

# Verify required environment variables
if [[ -z "$ANTHROPIC_API_KEY" ]]; then
    echo "ERROR: ANTHROPIC_API_KEY not set"
    exit 1
fi

if [[ -z "$GITHUB_TOKEN" ]]; then
    echo "WARNING: GITHUB_TOKEN not set - GitHub integration disabled"
fi

# Setup SSH for GitHub
if [[ -d "$HOME/.ssh" ]]; then
    echo "Setting up SSH..."
    chmod 700 "$HOME/.ssh"
    if [[ -f "$HOME/.ssh/id_ed25519" ]]; then
        chmod 600 "$HOME/.ssh/id_ed25519"
        ssh-keyscan github.com >> "$HOME/.ssh/known_hosts" 2>/dev/null || true
    fi
fi

# Verify Blackbox5 installation
echo "Verifying Blackbox5 installation..."
if [[ ! -f "$RALF_BLACKBOX5_DIR/bin/ralf" ]]; then
    echo "ERROR: Blackbox5 not found at $RALF_BLACKBOX5_DIR"
    echo "Waiting for code volume to be mounted..."
    sleep 10

    if [[ ! -f "$RALF_BLACKBOX5_DIR/bin/ralf" ]]; then
        echo "ERROR: Blackbox5 still not found after wait"
        exit 1
    fi
fi

echo "✓ Blackbox5 found"
echo ""

# Create required directories
mkdir -p "$RALF_PROJECT_DIR/.autonomous/runs"
mkdir -p "$RALF_PROJECT_DIR/.autonomous/LOGS"
mkdir -p "$RALF_PROJECT_DIR/.autonomous/memory"

# Set up git configuration
git config --global user.email "ralf@blackbox5.local"
git config --global user.name "RALF Agent ($RALF_AGENT_ID)"

# Run based on mode
case "$RALF_MODE" in
    daemon)
        echo "Starting RALF in daemon mode..."
        echo "This will run continuously, pulling tasks and executing them."
        echo ""

        # Check if ralf-daemon exists, otherwise use ralf-loop
        if [[ -f "$RALF_BLACKBOX5_DIR/5-project-memory/blackbox5/.autonomous/ralf-daemon.sh" ]]; then
            echo "Using ralf-daemon.sh"
            exec "$RALF_BLACKBOX5_DIR/5-project-memory/blackbox5/.autonomous/ralf-daemon.sh"
        else
            echo "Using ralf-loop.sh"
            cd "$RALF_BLACKBOX5_DIR"
            while true; do
                echo "$(date): Starting RALF loop iteration"

                # Run the RALF loop
                if bash "$RALF_ENGINE_DIR/shell/ralf-loop.sh"; then
                    echo "$(date): RALF loop completed successfully"
                else
                    echo "$(date): RALF loop failed, retrying in 60s"
                    sleep 60
                    continue
                fi

                # Brief pause between iterations
                echo "$(date): Sleeping before next iteration..."
                sleep 10
            done
        fi
        ;;

    single)
        echo "Running single RALF iteration..."
        cd "$RALF_BLACKBOX5_DIR"
        exec bash "$RALF_ENGINE_DIR/shell/ralf-loop.sh"
        ;;

    interactive)
        echo "Starting interactive shell..."
        echo "You can manually run: bash $RALF_ENGINE_DIR/shell/ralf-loop.sh"
        exec /bin/bash
        ;;

    *)
        echo "Unknown mode: $RALF_MODE"
        echo "Valid modes: daemon, single, interactive"
        exit 1
        ;;
esac
