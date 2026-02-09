---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/install/hetzner",
    "fetched_at": "2026-02-07T10:19:04.414362",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 712845
  },
  "metadata": {
    "title": "Hetzner",
    "section": "hetzner",
    "tier": 3,
    "type": "reference"
  }
}
---

- Hetzner - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationHosting and deploymentHetzner[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Install overview- [Install](/install)- [Installer Internals](/install/installer)Other install methods- [Docker](/install/docker)- [Nix](/install/nix)- [Ansible](/install/ansible)- [Bun (Experimental)](/install/bun)Maintenance- [Updating](/install/updating)- [Migration Guide](/install/migrating)- [Uninstall](/install/uninstall)Hosting and deployment- [Fly.io](/install/fly)- [Hetzner](/install/hetzner)- [GCP](/install/gcp)- [macOS VMs](/install/macos-vm)- [exe.dev](/install/exe-dev)- [Deploy on Railway](/install/railway)- [Deploy on Render](/install/render)- [Deploy on Northflank](/install/northflank)Advanced- [Development Channels](/install/development-channels)On this page- [OpenClaw on Hetzner (Docker, Production VPS Guide)](#openclaw-on-hetzner-docker-production-vps-guide)- [Goal](#goal)- [What are we doing (simple terms)?](#what-are-we-doing-simple-terms-)- [Quick path (experienced operators)](#quick-path-experienced-operators)- [What you need](#what-you-need)- [1) Provision the VPS](#1-provision-the-vps)- [2) Install Docker (on the VPS)](#2-install-docker-on-the-vps)- [3) Clone the OpenClaw repository](#3-clone-the-openclaw-repository)- [4) Create persistent host directories](#4-create-persistent-host-directories)- [5) Configure environment variables](#5-configure-environment-variables)- [6) Docker Compose configuration](#6-docker-compose-configuration)- [7) Bake required binaries into the image (critical)](#7-bake-required-binaries-into-the-image-critical)- [8) Build and launch](#8-build-and-launch)- [9) Verify Gateway](#9-verify-gateway)- [What persists where (source of truth)](#what-persists-where-source-of-truth)Hosting and deployment# Hetzner# [​](#openclaw-on-hetzner-docker-production-vps-guide)OpenClaw on Hetzner (Docker, Production VPS Guide)

## [​](#goal)Goal

Run a persistent OpenClaw Gateway on a Hetzner VPS using Docker, with durable state, baked-in binaries, and safe restart behavior.

If you want “OpenClaw 24/7 for ~$5”, this is the simplest reliable setup.

Hetzner pricing changes; pick the smallest Debian/Ubuntu VPS and scale up if you hit OOMs.

## [​](#what-are-we-doing-simple-terms-)What are we doing (simple terms)?

- Rent a small Linux server (Hetzner VPS)

- Install Docker (isolated app runtime)

- Start the OpenClaw Gateway in Docker

- Persist `~/.openclaw` + `~/.openclaw/workspace` on the host (survives restarts/rebuilds)

- Access the Control UI from your laptop via an SSH tunnel

The Gateway can be accessed via:

- SSH port forwarding from your laptop

- Direct port exposure if you manage firewalling and tokens yourself

This guide assumes Ubuntu or Debian on Hetzner.

If you are on another Linux VPS, map packages accordingly.

For the generic Docker flow, see [Docker](/install/docker).

## [​](#quick-path-experienced-operators)Quick path (experienced operators)

- Provision Hetzner VPS

- Install Docker

- Clone OpenClaw repository

- Create persistent host directories

- Configure `.env` and `docker-compose.yml`

- Bake required binaries into the image

- `docker compose up -d`

- Verify persistence and Gateway access

## [​](#what-you-need)What you need

- Hetzner VPS with root access

- SSH access from your laptop

- Basic comfort with SSH + copy/paste

- ~20 minutes

- Docker and Docker Compose

- Model auth credentials

- Optional provider credentials

WhatsApp QR

- Telegram bot token

- Gmail OAuth

## [​](#1-provision-the-vps)1) Provision the VPS

Create an Ubuntu or Debian VPS in Hetzner.

Connect as root:

Copy```

ssh root@YOUR_VPS_IP

```

This guide assumes the VPS is stateful.

Do not treat it as disposable infrastructure.

## [​](#2-install-docker-on-the-vps)2) Install Docker (on the VPS)

Copy```

apt-get update

apt-get install -y git curl ca-certificates

curl -fsSL https://get.docker.com | sh

```

Verify:

Copy```

docker --version

docker compose version

```

## [​](#3-clone-the-openclaw-repository)3) Clone the OpenClaw repository

Copy```

git clone https://github.com/openclaw/openclaw.git

cd openclaw

```

This guide assumes you will build a custom image to guarantee binary persistence.

## [​](#4-create-persistent-host-directories)4) Create persistent host directories

Docker containers are ephemeral.

All long-lived state must live on the host.

Copy```

mkdir -p /root/.openclaw

mkdir -p /root/.openclaw/workspace

# Set ownership to the container user (uid 1000):

chown -R 1000:1000 /root/.openclaw

chown -R 1000:1000 /root/.openclaw/workspace

```

## [​](#5-configure-environment-variables)5) Configure environment variables

Create `.env` in the repository root.

Copy```

OPENCLAW_IMAGE=openclaw:latest

OPENCLAW_GATEWAY_TOKEN=change-me-now

OPENCLAW_GATEWAY_BIND=lan

OPENCLAW_GATEWAY_PORT=18789

OPENCLAW_CONFIG_DIR=/root/.openclaw

OPENCLAW_WORKSPACE_DIR=/root/.openclaw/workspace

GOG_KEYRING_PASSWORD=change-me-now

XDG_CONFIG_HOME=/home/node/.openclaw

```

Generate strong secrets:

Copy```

openssl rand -hex 32

```

**Do not commit this file.**

## [​](#6-docker-compose-configuration)6) Docker Compose configuration

Create or update `docker-compose.yml`.

Copy```

services:

openclaw-gateway:

image: ${OPENCLAW_IMAGE}

build: .

restart: unless-stopped

env_file:

- .env

environment:

- HOME=/home/node

- NODE_ENV=production

- TERM=xterm-256color

- OPENCLAW_GATEWAY_BIND=${OPENCLAW_GATEWAY_BIND}

- OPENCLAW_GATEWAY_PORT=${OPENCLAW_GATEWAY_PORT}

- OPENCLAW_GATEWAY_TOKEN=${OPENCLAW_GATEWAY_TOKEN}

- GOG_KEYRING_PASSWORD=${GOG_KEYRING_PASSWORD}

- XDG_CONFIG_HOME=${XDG_CONFIG_HOME}

- PATH=/home/linuxbrew/.linuxbrew/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

volumes:

- ${OPENCLAW_CONFIG_DIR}:/home/node/.openclaw

- ${OPENCLAW_WORKSPACE_DIR}:/home/node/.openclaw/workspace

ports:

# Recommended: keep the Gateway loopback-only on the VPS; access via SSH tunnel.

# To expose it publicly, remove the `127.0.0.1:` prefix and firewall accordingly.

- "127.0.0.1:${OPENCLAW_GATEWAY_PORT}:18789"

# Optional: only if you run iOS/Android nodes against this VPS and need Canvas host.

# If you expose this publicly, read /gateway/security and firewall accordingly.

# - "18793:18793"

command:

[

"node",

"dist/index.js",

"gateway",

"--bind",

"${OPENCLAW_GATEWAY_BIND}",

"--port",

"${OPENCLAW_GATEWAY_PORT}",

]

```

## [​](#7-bake-required-binaries-into-the-image-critical)7) Bake required binaries into the image (critical)

Installing binaries inside a running container is a trap.

Anything installed at runtime will be lost on restart.

All external binaries required by skills must be installed at image build time.

The examples below show three common binaries only:

- `gog` for Gmail access

- `goplaces` for Google Places

- `wacli` for WhatsApp

These are examples, not a complete list.

You may install as many binaries as needed using the same pattern.

If you add new skills later that depend on additional binaries, you must:

- Update the Dockerfile

- Rebuild the image

- Restart the containers

**Example Dockerfile**

Copy```

FROM node:22-bookworm

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

# Example binary 1: Gmail CLI

RUN curl -L https://github.com/steipete/gog/releases/latest/download/gog_Linux_x86_64.tar.gz \

| tar -xz -C /usr/local/bin && chmod +x /usr/local/bin/gog

# Example binary 2: Google Places CLI

RUN curl -L https://github.com/steipete/goplaces/releases/latest/download/goplaces_Linux_x86_64.tar.gz \

| tar -xz -C /usr/local/bin && chmod +x /usr/local/bin/goplaces

# Example binary 3: WhatsApp CLI

RUN curl -L https://github.com/steipete/wacli/releases/latest/download/wacli_Linux_x86_64.tar.gz \

| tar -xz -C /usr/local/bin && chmod +x /usr/local/bin/wacli

# Add more binaries below using the same pattern

WORKDIR /app

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml .npmrc ./

COPY ui/package.json ./ui/package.json

COPY scripts ./scripts

RUN corepack enable

RUN pnpm install --frozen-lockfile

COPY . .

RUN pnpm build

RUN pnpm ui:install

RUN pnpm ui:build

ENV NODE_ENV=production

CMD ["node","dist/index.js"]

```

## [​](#8-build-and-launch)8) Build and launch

Copy```

docker compose build

docker compose up -d openclaw-gateway

```

Verify binaries:

Copy```

docker compose exec openclaw-gateway which gog

docker compose exec openclaw-gateway which goplaces

docker compose exec openclaw-gateway which wacli

```

Expected output:

Copy```

/usr/local/bin/gog

/usr/local/bin/goplaces

/usr/local/bin/wacli

```

## [​](#9-verify-gateway)9) Verify Gateway

Copy```

docker compose logs -f openclaw-gateway

```

Success:

Copy```

[gateway] listening on ws://0.0.0.0:18789

```

From your laptop:

Copy```

ssh -N -L 18789:127.0.0.1:18789 root@YOUR_VPS_IP

```

Open:

`http://127.0.0.1:18789/`

Paste your gateway token.

## [​](#what-persists-where-source-of-truth)What persists where (source of truth)

OpenClaw runs in Docker, but Docker is not the source of truth.

All long-lived state must survive restarts, rebuilds, and reboots.

ComponentLocationPersistence mechanismNotesGateway config`/home/node/.openclaw/`Host volume mountIncludes `openclaw.json`, tokensModel auth profiles`/home/node/.openclaw/`Host volume mountOAuth tokens, API keysSkill configs`/home/node/.openclaw/skills/`Host volume mountSkill-level stateAgent workspace`/home/node/.openclaw/workspace/`Host volume mountCode and agent artifactsWhatsApp session`/home/node/.openclaw/`Host volume mountPreserves QR loginGmail keyring`/home/node/.openclaw/`Host volume + passwordRequires `GOG_KEYRING_PASSWORD`External binaries`/usr/local/bin/`Docker imageMust be baked at build timeNode runtimeContainer filesystemDocker imageRebuilt every image buildOS packagesContainer filesystemDocker imageDo not install at runtimeDocker containerEphemeralRestartableSafe to destroy[Fly.io](/install/fly)[GCP](/install/gcp)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)