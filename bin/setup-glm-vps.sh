#!/bin/bash
# Setup GLM-4.7 on VPS for BB5 Agent Teams

set -e

echo "🚀 Setting up GLM-4.7 on VPS..."

# Check if already installed
if command -v glm &> /dev/null; then
    echo "✅ GLM already installed:"
    glm --version
    exit 0
fi

# Install GLM
echo "📥 Installing GLM..."

# Method 1: Try official installer
if curl -fsSL https://glm.ai/install.sh | sh 2>/dev/null; then
    echo "✅ GLM installed via official installer"
else
    echo "⚠️ Official installer failed, trying alternative..."

    # Method 2: Install via pip (if available)
    if command -v pip3 &> /dev/null; then
        pip3 install glm-cli 2>/dev/null || true
    fi

    # Method 3: Manual download
    echo "📥 Downloading GLM binary..."
    GLM_VERSION="4.7.0"
    ARCH=$(uname -m)

    case $ARCH in
        x86_64)
            GLM_ARCH="amd64"
            ;;
        aarch64)
            GLM_ARCH="arm64"
            ;;
        *)
            echo "❌ Unsupported architecture: $ARCH"
            exit 1
            ;;
    esac

    DOWNLOAD_URL="https://github.com/glm-ai/glm/releases/download/v${GLM_VERSION}/glm_${GLM_VERSION}_linux_${GLM_ARCH}.tar.gz"

    cd /tmp
    curl -L -o glm.tar.gz "$DOWNLOAD_URL" 2>/dev/null || {
        echo "❌ Failed to download GLM"
        echo "Please install manually from: https://glm.ai"
        exit 1
    }

    tar -xzf glm.tar.gz
    mv glm /usr/local/bin/
    chmod +x /usr/local/bin/glm
    rm -f glm.tar.gz

    echo "✅ GLM installed to /usr/local/bin/glm"
fi

# Verify installation
if command -v glm &> /dev/null; then
    echo ""
    echo "✅ GLM installation verified:"
    glm --version

    # Configure GLM for BB5
    echo ""
    echo "⚙️ Configuring GLM for BB5..."

    mkdir -p ~/.config/glm
    cat > ~/.config/glm/config.yaml << EOF
# GLM Configuration for BB5
model:
  default: 4.7
  temperature: 0.4

system_prompts:
  bb5: |
    You are a BB5 Core Agent Team member running on GLM-4.7.
    Your job is to autonomously improve BlackBox5 infrastructure.
    Always document your thinking, decisions, and learnings.

logging:
  level: info
  file: ~/.config/glm/glm.log
EOF

    echo "✅ GLM configured for BB5"
    echo ""
    echo "🎉 GLM-4.7 setup complete!"
    echo ""
    echo "Test with: glm chat --model 4.7 'Hello'"
    echo ""
else
    echo "❌ GLM installation failed"
    exit 1
fi
