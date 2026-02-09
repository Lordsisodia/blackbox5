---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/providers/zai",
    "fetched_at": "2026-02-07T10:21:16.141729",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 484099
  },
  "metadata": {
    "title": "Z.AI",
    "section": "zai",
    "tier": 3,
    "type": "reference"
  }
}
---

- Z.AI - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationProvidersZ.AI[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Model Providers](/providers)- [Model Provider Quickstart](/providers/models)- [Models CLI](/concepts/models)Configuration- [Model Providers](/concepts/model-providers)- [Model Failover](/concepts/model-failover)Providers- [Anthropic](/providers/anthropic)- [OpenAI](/providers/openai)- [OpenRouter](/providers/openrouter)- [Amazon Bedrock](/bedrock)- [Vercel AI Gateway](/providers/vercel-ai-gateway)- [Moonshot AI](/providers/moonshot)- [MiniMax](/providers/minimax)- [OpenCode Zen](/providers/opencode)- [GLM Models](/providers/glm)- [Z.AI](/providers/zai)- [Synthetic](/providers/synthetic)On this page- [Z.AI](#z-ai)- [CLI setup](#cli-setup)- [Config snippet](#config-snippet)- [Notes](#notes)Providers# Z.AI# [​](#z-ai)Z.AI

Z.AI is the API platform for **GLM** models. It provides REST APIs for GLM and uses API keys

for authentication. Create your API key in the Z.AI console. OpenClaw uses the `zai` provider

with a Z.AI API key.

## [​](#cli-setup)CLI setup

Copy```

openclaw onboard --auth-choice zai-api-key

# or non-interactive

openclaw onboard --zai-api-key "$ZAI_API_KEY"

```

## [​](#config-snippet)Config snippet

Copy```

{

env: { ZAI_API_KEY: "sk-..." },

agents: { defaults: { model: { primary: "zai/glm-4.7" } } },

}

```

## [​](#notes)Notes

- GLM models are available as `zai/<model>` (example: `zai/glm-4.7`).

- See [/providers/glm](/providers/glm) for the model family overview.

- Z.AI uses Bearer auth with your API key.

[GLM Models](/providers/glm)[Synthetic](/providers/synthetic)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)