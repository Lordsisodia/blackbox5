---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/providers/vercel-ai-gateway",
    "fetched_at": "2026-02-07T10:21:15.562188",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 493113
  },
  "metadata": {
    "title": "Vercel AI Gateway",
    "section": "vercel-ai-gateway",
    "tier": 3,
    "type": "reference"
  }
}
---

- Vercel AI Gateway - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationProvidersVercel AI Gateway[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Model Providers](/providers)- [Model Provider Quickstart](/providers/models)- [Models CLI](/concepts/models)Configuration- [Model Providers](/concepts/model-providers)- [Model Failover](/concepts/model-failover)Providers- [Anthropic](/providers/anthropic)- [OpenAI](/providers/openai)- [OpenRouter](/providers/openrouter)- [Amazon Bedrock](/bedrock)- [Vercel AI Gateway](/providers/vercel-ai-gateway)- [Moonshot AI](/providers/moonshot)- [MiniMax](/providers/minimax)- [OpenCode Zen](/providers/opencode)- [GLM Models](/providers/glm)- [Z.AI](/providers/zai)- [Synthetic](/providers/synthetic)On this page- [Vercel AI Gateway](#vercel-ai-gateway)- [Quick start](#quick-start)- [Non-interactive example](#non-interactive-example)- [Environment note](#environment-note)Providers# Vercel AI Gateway# [​](#vercel-ai-gateway)Vercel AI Gateway

The [Vercel AI Gateway](https://vercel.com/ai-gateway) provides a unified API to access hundreds of models through a single endpoint.

- Provider: `vercel-ai-gateway`

- Auth: `AI_GATEWAY_API_KEY`

- API: Anthropic Messages compatible

## [​](#quick-start)Quick start

- Set the API key (recommended: store it for the Gateway):

Copy```

openclaw onboard --auth-choice ai-gateway-api-key

```

- Set a default model:

Copy```

{

agents: {

defaults: {

model: { primary: "vercel-ai-gateway/anthropic/claude-opus-4.6" },

},

},

}

```

## [​](#non-interactive-example)Non-interactive example

Copy```

openclaw onboard --non-interactive \

--mode local \

--auth-choice ai-gateway-api-key \

--ai-gateway-api-key "$AI_GATEWAY_API_KEY"

```

## [​](#environment-note)Environment note

If the Gateway runs as a daemon (launchd/systemd), make sure `AI_GATEWAY_API_KEY`

is available to that process (for example, in `~/.openclaw/.env` or via

`env.shellEnv`).[Amazon Bedrock](/bedrock)[Moonshot AI](/providers/moonshot)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)