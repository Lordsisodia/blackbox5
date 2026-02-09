---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/providers/opencode",
    "fetched_at": "2026-02-07T10:21:13.766466",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 484275
  },
  "metadata": {
    "title": "OpenCode Zen",
    "section": "opencode",
    "tier": 3,
    "type": "reference"
  }
}
---

- OpenCode Zen - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationProvidersOpenCode Zen[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Model Providers](/providers)- [Model Provider Quickstart](/providers/models)- [Models CLI](/concepts/models)Configuration- [Model Providers](/concepts/model-providers)- [Model Failover](/concepts/model-failover)Providers- [Anthropic](/providers/anthropic)- [OpenAI](/providers/openai)- [OpenRouter](/providers/openrouter)- [Amazon Bedrock](/bedrock)- [Vercel AI Gateway](/providers/vercel-ai-gateway)- [Moonshot AI](/providers/moonshot)- [MiniMax](/providers/minimax)- [OpenCode Zen](/providers/opencode)- [GLM Models](/providers/glm)- [Z.AI](/providers/zai)- [Synthetic](/providers/synthetic)On this page- [OpenCode Zen](#opencode-zen)- [CLI setup](#cli-setup)- [Config snippet](#config-snippet)- [Notes](#notes)Providers# OpenCode Zen# [​](#opencode-zen)OpenCode Zen

OpenCode Zen is a **curated list of models** recommended by the OpenCode team for coding agents.

It is an optional, hosted model access path that uses an API key and the `opencode` provider.

Zen is currently in beta.

## [​](#cli-setup)CLI setup

Copy```

openclaw onboard --auth-choice opencode-zen

# or non-interactive

openclaw onboard --opencode-zen-api-key "$OPENCODE_API_KEY"

```

## [​](#config-snippet)Config snippet

Copy```

{

env: { OPENCODE_API_KEY: "sk-..." },

agents: { defaults: { model: { primary: "opencode/claude-opus-4-6" } } },

}

```

## [​](#notes)Notes

- `OPENCODE_ZEN_API_KEY` is also supported.

- You sign in to Zen, add billing details, and copy your API key.

- OpenCode Zen bills per request; check the OpenCode dashboard for details.

[MiniMax](/providers/minimax)[GLM Models](/providers/glm)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)