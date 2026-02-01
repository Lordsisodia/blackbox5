# RALF Agent Container for Kubernetes
# Minimal image that runs the RALF autonomous loop

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

# Create ralf user
RUN useradd -m -s /bin/bash ralf \
    && mkdir -p /home/ralf/.ssh /home/ralf/.config /home/ralf/.local/bin \
    && chown -R ralf:ralf /home/ralf

# Set up working directory
WORKDIR /opt/blackbox5

# Environment variables
ENV PATH="/home/ralf/.local/bin:$PATH"
ENV HOME="/home/ralf"
ENV RALF_MODE="daemon"
ENV RALF_PROJECT_DIR="/opt/blackbox5/5-project-memory/blackbox5"
ENV RALF_ENGINE_DIR="/opt/blackbox5/2-engine/.autonomous"
ENV RALF_BLACKBOX5_DIR="/opt/blackbox5"

# Switch to ralf user
USER ralf

# Entrypoint script
COPY --chown=ralf:ralf entrypoint.sh /home/ralf/entrypoint.sh
RUN chmod +x /home/ralf/entrypoint.sh

# Health check - check if RALF is running
HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=3 \
    CMD pgrep -f "claude" || exit 1

ENTRYPOINT ["/home/ralf/entrypoint.sh"]
