# Legacy Agent Container for Kubernetes
# Runs the autonomous Legacy improvement loop

FROM ubuntu:22.04

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Install dependencies
RUN apt-get update && apt-get install -y \
    git curl wget jq \
    python3 python3-pip \
    build-essential \
    netcat-openbsd \
    redis-tools \
    ca-certificates \
    gnupg \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (needed for Claude Code)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Claude Code CLI
RUN npm install -g @anthropic-ai/claude-code

# Create legacy user
RUN useradd -m -s /bin/bash legacy \
    && mkdir -p /home/legacy/.ssh /home/legacy/.config /home/legacy/.local/bin \
    && chown -R legacy:legacy /home/legacy

# Set up working directory
WORKDIR /opt/blackbox5

# Environment variables
ENV PATH="/home/legacy/.local/bin:$PATH"
ENV HOME="/home/legacy"
ENV LEGACY_MODE="daemon"
ENV LEGACY_PROJECT_DIR="/opt/blackbox5/5-project-memory/blackbox5"
ENV LEGACY_ENGINE_DIR="/opt/blackbox5/2-engine/.autonomous"
ENV LEGACY_BLACKBOX5_DIR="/opt/blackbox5"

# Switch to legacy user
USER legacy

# Entrypoint script
COPY --chown=legacy:legacy entrypoint.sh /home/legacy/entrypoint.sh
RUN chmod +x /home/legacy/entrypoint.sh

# Health check
HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=3 \
    CMD pgrep -f claude || exit 1

ENTRYPOINT ["/home/legacy/entrypoint.sh"]
