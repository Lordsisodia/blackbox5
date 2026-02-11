#!/bin/bash
# VPS Fix and Setup Script for BB5 Ralph Executor
# This script should be run on the VPS as the root user or with sudo

set -e

# Configuration
USER="bb5-runner"
USER_HOME="/home/$USER"
REPO_DIR="/opt/blackbox5"
SSH_DIR="$USER_HOME/.ssh"
KEY_TYPE="ed25519"
KEY_FILE="$SSH_DIR/id_ed25519"

echo "═══════════════════════════════════════════════════"
echo "  BB5 Ralph VPS Fix & Setup"
echo "═══════════════════════════════════════════════════"

# 1. Create User and SSH Directory if missing
echo "[1/5] Checking user and SSH directory..."
if ! id "$USER" &>/dev/null; then
    echo "User $USER does not exist! Please create it first."
    exit 1
fi

if [ ! -d "$SSH_DIR" ]; then
    echo "Creating .ssh directory..."
    mkdir -p "$SSH_DIR"
    chmod 700 "$SSH_DIR"
    chown "$USER:$USER" "$SSH_DIR"
fi

# 2. Generate SSH Key if missing
echo "[2/5] Checking SSH keys..."
if [ ! -f "$KEY_FILE" ]; then
    echo "Generating new $KEY_TYPE SSH key..."
    sudo -u "$USER" ssh-keygen -t "$KEY_TYPE" -f "$KEY_FILE" -N "" -C "$USER@$(hostname)"
    echo "SSH Key generated."
else
    echo "SSH Key already exists."
fi

# Ensure known_hosts exists and add GitHub
if [ ! -f "$SSH_DIR/known_hosts" ] || ! grep -q "github.com" "$SSH_DIR/known_hosts"; then
    echo "Adding GitHub to known_hosts..."
    ssh-keyscan github.com >> "$SSH_DIR/known_hosts"
    chown "$USER:$USER" "$SSH_DIR/known_hosts"
    chmod 600 "$SSH_DIR/known_hosts"
fi

# 3. Configure Git User
echo "[3/5] Configuring Git..."
sudo -u "$USER" git config --global user.name "BB5 RALF Executor" || true
sudo -u "$USER" git config --global user.email "$USER@blackbox5.local" || true
echo "Git user configured."

# 4. Clean Git Repository
echo "[4/5] Cleaning Git repository bloat (this may take a moment)..."
if [ -d "$REPO_DIR/.git" ]; then
    cd "$REPO_DIR"
    # Run aggressively to fix the "too many loose objects" error
    git gc --prune=now --aggressive
    # Remove the log file that blocks auto-gc
    rm -f .git/gc.log
    echo "Git repository cleaned."
else
    echo "Warning: Repository not found at $REPO_DIR"
fi

# 5. Display Public Key
echo "═══════════════════════════════════════════════════"
echo "  ACTION REQUIRED: ADD THIS KEY TO GITHUB"
echo "═══════════════════════════════════════════════════"
echo ""
cat "$KEY_FILE.pub"
echo ""
echo "═══════════════════════════════════════════════════"
echo "Copy the key above and add it to:"
echo "https://github.com/Lordsisodia/blackbox5/settings/keys"
echo "OR Repository Settings -> Deploy Keys -> Add deploy key"
echo "Make sure to allow write access if adding as a deploy key."
echo "═══════════════════════════════════════════════════"

# Only attempt to pull if we have access (which we likely don't yet)
echo "After adding the key, verify access with:"
echo "sudo -u $USER ssh -T git@github.com"
echo ""
echo "Then deploy the fixed ralf-core.sh script."
