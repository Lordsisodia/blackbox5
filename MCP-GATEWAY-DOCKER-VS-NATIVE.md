# MCP Gateway: Docker vs Native - What's Best For You?

## Quick Answer

**For your use case (local MCPs: filesystem, supabase, memory, serena): Native is BETTER than Docker.**

---

## Comparison: Docker vs Native

| Feature | Docker | Native (Binary) |
|---------|--------|-----------------|
| **Setup** | `docker compose up` | `cargo install` or download binary |
| **Resource usage** | Higher (container overhead) | Lower (direct process) |
| **Local MCPs** | ✅ Can run stdio | ✅ Better for stdio |
| **Startup time** | Slower (container boot) | Faster (native process) |
| **Port conflicts** | Possible (port binding) | Uses Unix sockets |
| **Debugging** | Harder (container logs) | Easier (direct logs) |
| **Updates** | Rebuild image | `cargo install` again |
| **Best for** | Cloud/Remote MCPs | Local MCPs |

---

## 🥇 Recommended: rmcp-mux (Native Rust Binary)

**Best for: Your local MCPs (filesystem, supabase, memory, serena)**

### Installation

```bash
# Option 1: Cargo install
cargo install rmcp-mux

# Option 2: One-liner install script
curl -fsSL https://raw.githubusercontent.com/Loctree/rmcp-mux/main/tools/install.sh | sh

# Option 3: Download binary from GitHub releases
# https://github.com/VetCoders/rmcp-mux/releases
```

### Configuration (mux.toml)

```toml
[servers.filesystem]
socket = "/tmp/mcp-fs.sock"
cmd = "node"
args = ["~/.npm-global/bin/mcp-server-filesystem", "/Users/shaansisodia"]

[servers.supabase]
socket = "/tmp/mcp-supabase.sock"
cmd = "node"
args = ["~/.npm-global/bin/mcp-server-supabase", "--project-ref", "avdgyrepwrvsvwgxrccr"]

[servers.memory]
socket = "/tmp/mcp-memory.sock"
cmd = "npx"
args = ["-y", "@modelcontextprotocol/server-memory"]

[servers.serena]
socket = "/tmp/mcp-serena.sock"
cmd = "uv"
args = ["serena-mcp-server"]
```

### Run

```bash
# Regular mode
rmcp-mux --config mux.toml

# With TUI dashboard
rmcp-mux --config mux.toml --tui

# Background with systemd/launchd (recommended)
nohup rmcp-mux --config mux.toml > /tmp/rmcp-mux.log 2>&1 &
```

### Connect Claude Desktop

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "rmcp-mux-proxy",
      "args": ["--socket", "/tmp/mcp-fs.sock"]
    },
    "supabase": {
      "command": "rmcp-mux-proxy",
      "args": ["--socket", "/tmp/mcp-supabase.sock"]
    },
    "memory": {
      "command": "rmcp-mux-proxy",
      "args": ["--socket", "/tmp/mcp-memory.sock"]
    },
    "serena": {
      "command": "rmcp-mux-proxy",
      "args": ["--socket", "/tmp/mcp-serena.sock"]
    }
  }
}
```

---

## 🥈 Alternative: Agent Gateway (Native Binary)

**Best for: Production-ready, enterprise features**

### Installation

```bash
# Download from releases
# https://github.com/agentgateway/agentgateway/releases

# Download darwin-arm64 binary for Apple Silicon
wget https://github.com/agentgateway/agentgateway/releases/latest/download/agentgateway-darwin-arm64
chmod +x agentgateway-darwin-arm64
mv agentgateway-darwin-arm64 ~/bin/agentgateway
```

### Configuration (config.yaml)

```yaml
binds:
- port: 3000
  listeners:
  - routes:
    - backends:
      - mcp:
          targets:
          - name: filesystem
            stdio:
              cmd: node
              args: ["~/.npm-global/bin/mcp-server-filesystem", "/Users/shaansisodia"]
          - name: supabase
            stdio:
              cmd: node
              args: ["~/.npm-global/bin/mcp-server-supabase", "--project-ref", "avdgyrepwrvsvwgxrccr"]
          - name: memory
            stdio:
              cmd: npx
              args: ["-y", "@modelcontextprotocol/server-memory"]
          - name: serena
            stdio:
              cmd: uv
              args: ["serena-mcp-server"]
```

### Run

```bash
agentgateway -f config.yaml
```

---

## 🥉 Docker Options (When to Use)

**Best for: Cloud MCPs, Railway deployment, team sharing**

### Airis MCP Gateway

```bash
git clone https://github.com/agiletec-inc/airis-mcp-gateway.git
cd airis-mcp-gateway
docker compose up -d
```

### IBM Context Forge

```bash
docker run -d --name mcpgateway \
  -p 4444:4444 \
  -e MCPGATEWAY_UI_ENABLED=true \
  ghcr.io/ibm/mcp-context-forge:1.0.0-BETA-1
```

---

## Can Docker Run Local MCPs? Yes, But...

Docker CAN run local MCPs via stdio, but it has limitations:

```yaml
# Example docker-compose.yml for local MCPs
services:
  mcp-gateway:
    image: some-gateway-image
    volumes:
      - /Users/shaansisodia:/Users/shaansisodia:ro  # Mount filesystem
    environment:
      - MCP_FILESYSTEM_PATH=/Users/shaansisodia
```

**Problems with Docker for local MCPs:**
1. **Filesystem access** - Need to mount volumes
2. **Socket access** - Unix sockets don't cross container boundaries easily
3. **Performance** - Container overhead for every tool call
4. **Debugging** - Logs trapped in container

**When Docker IS good:**
- Cloud-hosted MCPs (Railway, AWS, GCP)
- Remote HTTP/SSE MCPs
- Team-shared gateway
- Production deployments

---

## My Recommendation: Hybrid Approach

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Setup                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Local MCPs (Native - rmcp-mux):                           │
│  ├─ Filesystem → Unix socket (fast, direct)                │
│  ├─ Supabase → Unix socket (fast, direct)                  │
│  ├─ Memory → Unix socket (fast, direct)                    │
│  └─ Serena → Unix socket (fast, direct)                    │
│                                                              │
│  Remote/Cloud MCPs (Docker - Airis or IBM):                │
│  ├─ GitHub (Railway)                                        │
│  ├─ Slack (Railway)                                         │
│  ├─ Custom APIs (Railway)                                   │
│  └─ External services                                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Step 1: Install rmcp-mux for local MCPs

```bash
cargo install rmcp-mux
```

### Step 2: Create mux.toml

```toml
[servers.filesystem]
socket = "/tmp/mcp-fs.sock"
cmd = "node"
args = ["~/.npm-global/bin/mcp-server-filesystem", "/Users/shaansisodia"]

[servers.supabase]
socket = "/tmp/mcp-supabase.sock"
cmd = "node"
args = ["~/.npm-global/bin/mcp-server-supabase", "--project-ref", "avdgyrepwrvsvwgxrccr"]

[servers.memory]
socket = "/tmp/mcp-memory.sock"
cmd = "npx"
args = ["-y", "@modelcontextprotocol/server-memory"]

[servers.serena]
socket = "/tmp/mcp-serena.sock"
cmd = "uv"
args = ["serena-mcp-server"]
```

### Step 3: Run it

```bash
rmcp-mux --config mux.toml --tui
```

### Step 4: (Optional) Add Airis for cloud MCPs

```bash
git clone https://github.com/agiletec-inc/airis-mcp-gateway.git
cd airis-mcp-gateway
docker compose up -d
```

---

## Summary

| Use Case | Recommended Solution |
|----------|---------------------|
| **Your local MCPs** | rmcp-mux (native) |
| **Cloud MCPs** | Docker (Airis/IBM) |
| **Production/Enterprise** | Agent Gateway (native) |
| **Quick testing** | Airis (Docker) |
| **Best of both worlds** | rmcp-mux (local) + Airis (cloud) |

---

## Resources

- [rmcp-mux GitHub](https://github.com/VetCoders/rmcp-mux) - Native Rust multiplexer
- [Agent Gateway GitHub](https://github.com/agentgateway/agentgateway) - Enterprise-grade gateway
- [Agent Gateway stdio docs](https://agentgateway.dev/docs/integrations/mcp-servers/stdio/) - Local MCP configuration
- [mcp-proxy GitHub](https://github.com/stephenlacy/mcp-proxy) - Simple stdio/SSE proxy
- [Airis Gateway](https://github.com/agiletec-inc/airis-mcp-gateway) - Docker-based
