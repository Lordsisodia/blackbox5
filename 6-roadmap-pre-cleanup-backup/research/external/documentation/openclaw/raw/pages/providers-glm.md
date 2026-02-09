---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/providers/glm",
    "fetched_at": "2026-02-07T10:21:09.892283",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 480529
  },
  "metadata": {
    "title": "GLM Models",
    "section": "glm",
    "tier": 3,
    "type": "reference"
  }
}
---

- GLM Models - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationProvidersGLM Models[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Model Providers](/providers)- [Model Provider Quickstart](/providers/models)- [Models CLI](/concepts/models)Configuration- [Model Providers](/concepts/model-providers)- [Model Failover](/concepts/model-failover)Providers- [Anthropic](/providers/anthropic)- [OpenAI](/providers/openai)- [OpenRouter](/providers/openrouter)- [Amazon Bedrock](/bedrock)- [Vercel AI Gateway](/providers/vercel-ai-gateway)- [Moonshot AI](/providers/moonshot)- [MiniMax](/providers/minimax)- [OpenCode Zen](/providers/opencode)- [GLM Models](/providers/glm)- [Z.AI](/providers/zai)- [Synthetic](/providers/synthetic)On this page- [GLM models](#glm-models)- [CLI setup](#cli-setup)- [Config snippet](#config-snippet)- [Notes](#notes)Providers# GLM Models# [​](#glm-models)GLM models

GLM is a **model family** (not a company) available through the Z.AI platform. In OpenClaw, GLM

models are accessed via the `zai` provider and model IDs like `zai/glm-4.7`.

## [​](#cli-setup)CLI setup

Copy```

openclaw onboard --auth-choice zai-api-key

```

## [​](#config-snippet)Config snippet

Copy```

{

env: { ZAI_API_KEY: "sk-..." },

agents: { defaults: { model: { primary: "zai/glm-4.7" } } },

}

```

## [​](#notes)Notes

- GLM versions and availability can change; check Z.AI’s docs for the latest.

- Example model IDs include `glm-4.7` and `glm-4.6`.

- For provider details, see [/providers/zai](/providers/zai).

[OpenCode Zen](/providers/opencode)[Z.AI](/providers/zai)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)