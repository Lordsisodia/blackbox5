---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/providers/openrouter",
    "fetched_at": "2026-02-07T10:21:14.343656",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 485362
  },
  "metadata": {
    "title": "OpenRouter",
    "section": "openrouter",
    "tier": 3,
    "type": "reference"
  }
}
---

- OpenRouter - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationProvidersOpenRouter[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Model Providers](/providers)- [Model Provider Quickstart](/providers/models)- [Models CLI](/concepts/models)Configuration- [Model Providers](/concepts/model-providers)- [Model Failover](/concepts/model-failover)Providers- [Anthropic](/providers/anthropic)- [OpenAI](/providers/openai)- [OpenRouter](/providers/openrouter)- [Amazon Bedrock](/bedrock)- [Vercel AI Gateway](/providers/vercel-ai-gateway)- [Moonshot AI](/providers/moonshot)- [MiniMax](/providers/minimax)- [OpenCode Zen](/providers/opencode)- [GLM Models](/providers/glm)- [Z.AI](/providers/zai)- [Synthetic](/providers/synthetic)On this page- [OpenRouter](#openrouter)- [CLI setup](#cli-setup)- [Config snippet](#config-snippet)- [Notes](#notes)Providers# OpenRouter# [​](#openrouter)OpenRouter

OpenRouter provides a **unified API** that routes requests to many models behind a single

endpoint and API key. It is OpenAI-compatible, so most OpenAI SDKs work by switching the base URL.

## [​](#cli-setup)CLI setup

Copy```

openclaw onboard --auth-choice apiKey --token-provider openrouter --token "$OPENROUTER_API_KEY"

```

## [​](#config-snippet)Config snippet

Copy```

{

env: { OPENROUTER_API_KEY: "sk-or-..." },

agents: {

defaults: {

model: { primary: "openrouter/anthropic/claude-sonnet-4-5" },

},

},

}

```

## [​](#notes)Notes

- Model refs are `openrouter/<provider>/<model>`.

- For more model/provider options, see [/concepts/model-providers](/concepts/model-providers).

- OpenRouter uses a Bearer token with your API key under the hood.

[OpenAI](/providers/openai)[Amazon Bedrock](/bedrock)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)