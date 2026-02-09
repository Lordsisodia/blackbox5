---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/providers/models",
    "fetched_at": "2026-02-07T10:21:12.059244",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 479568
  },
  "metadata": {
    "title": "Model Provider Quickstart",
    "section": "models",
    "tier": 3,
    "type": "reference"
  }
}
---

- Model Provider Quickstart - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationOverviewModel Provider Quickstart[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Model Providers](/providers)- [Model Provider Quickstart](/providers/models)- [Models CLI](/concepts/models)Configuration- [Model Providers](/concepts/model-providers)- [Model Failover](/concepts/model-failover)Providers- [Anthropic](/providers/anthropic)- [OpenAI](/providers/openai)- [OpenRouter](/providers/openrouter)- [Amazon Bedrock](/bedrock)- [Vercel AI Gateway](/providers/vercel-ai-gateway)- [Moonshot AI](/providers/moonshot)- [MiniMax](/providers/minimax)- [OpenCode Zen](/providers/opencode)- [GLM Models](/providers/glm)- [Z.AI](/providers/zai)- [Synthetic](/providers/synthetic)On this page- [Model Providers](#model-providers)- [Highlight: Venice (Venice AI)](#highlight-venice-venice-ai)- [Quick start (two steps)](#quick-start-two-steps)- [Supported providers (starter set)](#supported-providers-starter-set)Overview# Model Provider Quickstart# [​](#model-providers)Model Providers

OpenClaw can use many LLM providers. Pick one, authenticate, then set the default

model as `provider/model`.

## [​](#highlight-venice-venice-ai)Highlight: Venice (Venice AI)

Venice is our recommended Venice AI setup for privacy-first inference with an option to use Opus for the hardest tasks.

- Default: `venice/llama-3.3-70b`

- Best overall: `venice/claude-opus-45` (Opus remains the strongest)

See [Venice AI](/providers/venice).

## [​](#quick-start-two-steps)Quick start (two steps)

- Authenticate with the provider (usually via `openclaw onboard`).

- Set the default model:

Copy```

{

agents: { defaults: { model: { primary: "anthropic/claude-opus-4-6" } } },

}

```

## [​](#supported-providers-starter-set)Supported providers (starter set)

- [OpenAI (API + Codex)](/providers/openai)

- [Anthropic (API + Claude Code CLI)](/providers/anthropic)

- [OpenRouter](/providers/openrouter)

- [Vercel AI Gateway](/providers/vercel-ai-gateway)

- [Cloudflare AI Gateway](/providers/cloudflare-ai-gateway)

- [Moonshot AI (Kimi + Kimi Coding)](/providers/moonshot)

- [Synthetic](/providers/synthetic)

- [OpenCode Zen](/providers/opencode)

- [Z.AI](/providers/zai)

- [GLM models](/providers/glm)

- [MiniMax](/providers/minimax)

- [Venice (Venice AI)](/providers/venice)

- [Amazon Bedrock](/bedrock)

For the full provider catalog (xAI, Groq, Mistral, etc.) and advanced configuration,

see [Model providers](/concepts/model-providers).[Model Providers](/providers)[Models CLI](/concepts/models)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)