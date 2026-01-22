# MCP Gateway - BEST Options Quick Start

## The Top 3 Working Solutions (Ranked by Ease of Use)

---

## 🥇 Option 1: Airis MCP Gateway (EASIEST - One Command)

**60+ AI tools, 98% token reduction, docker-compose ready**

```bash
git clone https://github.com/agiletec-inc/airis-mcp-gateway.git
cd airis-mcp-gateway
docker compose up -d
claude mcp add --scope user --transport sse airis-mcp-gateway http://localhost:9400/sse
```

That's it! You now have 60+ tools available through 3 meta-tools:
- `airis-find` - Search tools
- `airis-exec` - Execute tools
- `airis-schema` - Get tool schemas

**Token impact: 600 tokens vs 42,000 (98% reduction)**

### Add Your Own MCPs

Edit `docker-compose.yml` or use the built-in `/troubleshoot` command in Claude.

---

## 🥈 Option 2: Docker MCP Gateway (Official Docker)

**Built into Docker Desktop - just enable it**

### Step 1: Enable Docker MCP Toolkit

1. Open Docker Desktop
2. Go to Settings
3. Select **Beta features**
4. Check **Enable Docker MCP Toolkit**
5. Restart Docker Desktop

### Step 2: Use the CLI

```bash
# Enable a server
docker mcp server enable github

# Connect your client
docker mcp client connect claude

# Run the gateway
docker mcp gateway run
```

**No installation needed - it's built into Docker Desktop!**

---

## 🥉 Option 3: Enkrypt AI Secure Gateway

**Most feature-rich: authentication, guardrails, caching, observability**

```bash
# Install via pip
pip install secure-mcp-gateway
secure-mcp-gateway generate-config
secure-mcp-gateway install --client claude-desktop
```

Or with Docker:
```bash
docker build -t secure-mcp-gateway https://github.com/enkryptai/secure-mcp-gateway.git
docker run --rm -e HOST_OS=macos -v ~/.enkrypt:/app/.enkrypt secure-mcp-gateway
```

### Features:
- API key authentication
- Input/output guardrails (PII redaction, NSFW filtering)
- Tool caching
- OpenTelemetry observability
- OAuth support

---

## Which One Should You Use?

| Feature | Airis | Docker MCP | Enkrypt |
|---------|-------|------------|---------|
| **Setup Time** | 1 min | 2 min (enable) | 5 min |
| **Servers Included** | 60+ | From catalog | Add your own |
| **Token Reduction** | 98% | ~95% | ~95% |
| **Authentication** | API key | Built-in | API key + OAuth |
| **Guardrails** | No | No | Yes (PII, NSFW) |
| **Observability** | Prometheus | Basic | Full (Grafana, Jaeger) |
| **Best For** | Quick start | Docker users | Enterprise |

### My Recommendation: Start with Airis

**Why:**
- One command and you're done
- 60+ tools immediately available
- 98% token reduction
- Actively maintained
- Easy to add your own MCPs

---

## Quick Start: Run This NOW

```bash
# Clone and start Airis
git clone https://github.com/agiletec-inc/airis-mcp-gateway.git
cd airis-mcp-gateway
docker compose up -d

# Add to Claude Desktop
claude mcp add --scope user --transport sse airis-mcp-gateway http://localhost:9400/sse

# Test it - ask Claude: "list all available tools"
```

---

## Verify It's Working

After starting, ask Claude:
```
"List all servers and tools available through the gateway"
```

You should see 60+ tools from servers like:
- memory
- github
- stripe
- puppeteer
- filesystem
- fetch
- postgres
- slack
- google-drive
- And 50+ more

---

## Docker Compose Reference (Airis)

```yaml
# From airis-mcp-gateway/docker-compose.yml
version: '3.8'
services:
  gateway:
    image: ghcr.io/agiletec-inc/airis-mcp-gateway:latest
    ports:
      - "9400:9400"
    environment:
      - GATEWAY_PORT=9400
      - API_KEY=your-key-here
    restart: unless-stopped
```

---

## Troubleshooting

### Port 9400 already in use?
```bash
# Change port in docker-compose.yml or stop conflicting service
lsof -i :9400
```

### Can't connect to gateway?
```bash
# Check if gateway is running
docker compose ps
docker compose logs gateway
```

### Tools not showing in Claude?
```bash
# Restart Claude Desktop after adding gateway
# Use Claude command: "list all available tools"
```

---

## Resources

- [Airis MCP Gateway GitHub](https://github.com/agiletec-inc/airis-mcp-gateway)
- [Docker MCP Gateway GitHub](https://github.com/docker/mcp-gateway)
- [Docker MCP Docs](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/)
- [Enkrypt Secure Gateway GitHub](https://github.com/enkryptai/secure-mcp-gateway)
- [MCP Gateway Registry](https://agentic-community.github.io/mcp-gateway-registry/)
