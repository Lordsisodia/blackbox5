---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/providers/openai",
    "fetched_at": "2026-02-07T10:21:13.207807",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 515664
  },
  "metadata": {
    "title": "OpenAI",
    "section": "openai",
    "tier": 3,
    "type": "reference"
  }
}
---

- OpenAI - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationProvidersOpenAI[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Model Providers](/providers)- [Model Provider Quickstart](/providers/models)- [Models CLI](/concepts/models)Configuration- [Model Providers](/concepts/model-providers)- [Model Failover](/concepts/model-failover)Providers- [Anthropic](/providers/anthropic)- [OpenAI](/providers/openai)- [OpenRouter](/providers/openrouter)- [Amazon Bedrock](/bedrock)- [Vercel AI Gateway](/providers/vercel-ai-gateway)- [Moonshot AI](/providers/moonshot)- [MiniMax](/providers/minimax)- [OpenCode Zen](/providers/opencode)- [GLM Models](/providers/glm)- [Z.AI](/providers/zai)- [Synthetic](/providers/synthetic)On this page- [OpenAI](#openai)- [Option A: OpenAI API key (OpenAI Platform)](#option-a-openai-api-key-openai-platform)- [CLI setup](#cli-setup)- [Config snippet](#config-snippet)- [Option B: OpenAI Code (Codex) subscription](#option-b-openai-code-codex-subscription)- [CLI setup (Codex OAuth)](#cli-setup-codex-oauth)- [Config snippet (Codex subscription)](#config-snippet-codex-subscription)- [Notes](#notes)Providers# OpenAI# [​](#openai)OpenAI

OpenAI provides developer APIs for GPT models. Codex supports **ChatGPT sign-in** for subscription

access or **API key** sign-in for usage-based access. Codex cloud requires ChatGPT sign-in.

## [​](#option-a-openai-api-key-openai-platform)Option A: OpenAI API key (OpenAI Platform)

**Best for:** direct API access and usage-based billing.

Get your API key from the OpenAI dashboard.

### [​](#cli-setup)CLI setup

Copy```

openclaw onboard --auth-choice openai-api-key

# or non-interactive

openclaw onboard --openai-api-key "$OPENAI_API_KEY"

```

### [​](#config-snippet)Config snippet

Copy```

{

env: { OPENAI_API_KEY: "sk-..." },

agents: { defaults: { model: { primary: "openai/gpt-5.1-codex" } } },

}

```

## [​](#option-b-openai-code-codex-subscription)Option B: OpenAI Code (Codex) subscription

**Best for:** using ChatGPT/Codex subscription access instead of an API key.

Codex cloud requires ChatGPT sign-in, while the Codex CLI supports ChatGPT or API key sign-in.

### [​](#cli-setup-codex-oauth)CLI setup (Codex OAuth)

Copy```

# Run Codex OAuth in the wizard

openclaw onboard --auth-choice openai-codex

# Or run OAuth directly

openclaw models auth login --provider openai-codex

```

### [​](#config-snippet-codex-subscription)Config snippet (Codex subscription)

Copy```

{

agents: { defaults: { model: { primary: "openai-codex/gpt-5.3-codex" } } },

}

```

## [​](#notes)Notes

- Model refs always use `provider/model` (see [/concepts/models](/concepts/models)).

- Auth details + reuse rules are in [/concepts/oauth](/concepts/oauth).

[Anthropic](/providers/anthropic)[OpenRouter](/providers/openrouter)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)