---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/providers/index",
    "fetched_at": "2026-02-07T10:21:10.742458",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 485454
  },
  "metadata": {
    "title": "Model Providers",
    "section": "index",
    "tier": 3,
    "type": "reference"
  }
}
---

- Model Providers - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationOverviewModel Providers[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Model Providers](/providers)- [Model Provider Quickstart](/providers/models)- [Models CLI](/concepts/models)Configuration- [Model Providers](/concepts/model-providers)- [Model Failover](/concepts/model-failover)Providers- [Anthropic](/providers/anthropic)- [OpenAI](/providers/openai)- [OpenRouter](/providers/openrouter)- [Amazon Bedrock](/bedrock)- [Vercel AI Gateway](/providers/vercel-ai-gateway)- [Moonshot AI](/providers/moonshot)- [MiniMax](/providers/minimax)- [OpenCode Zen](/providers/opencode)- [GLM Models](/providers/glm)- [Z.AI](/providers/zai)- [Synthetic](/providers/synthetic)On this page- [Model Providers](#model-providers)- [Highlight: Venice (Venice AI)](#highlight-venice-venice-ai)- [Quick start](#quick-start)- [Provider docs](#provider-docs)- [Transcription providers](#transcription-providers)- [Community tools](#community-tools)Overview# Model Providers# [​](#model-providers)Model Providers

OpenClaw can use many LLM providers. Pick a provider, authenticate, then set the

default model as `provider/model`.

Looking for chat channel docs (WhatsApp/Telegram/Discord/Slack/Mattermost (plugin)/etc.)? See [Channels](/channels).

## [​](#highlight-venice-venice-ai)Highlight: Venice (Venice AI)

Venice is our recommended Venice AI setup for privacy-first inference with an option to use Opus for hard tasks.

- Default: `venice/llama-3.3-70b`

- Best overall: `venice/claude-opus-45` (Opus remains the strongest)

See [Venice AI](/providers/venice).

## [​](#quick-start)Quick start

- Authenticate with the provider (usually via `openclaw onboard`).

- Set the default model:

Copy```

{

agents: { defaults: { model: { primary: "anthropic/claude-opus-4-6" } } },

}

```

## [​](#provider-docs)Provider docs

- [OpenAI (API + Codex)](/providers/openai)

- [Anthropic (API + Claude Code CLI)](/providers/anthropic)

- [Qwen (OAuth)](/providers/qwen)

- [OpenRouter](/providers/openrouter)

- [Vercel AI Gateway](/providers/vercel-ai-gateway)

- [Cloudflare AI Gateway](/providers/cloudflare-ai-gateway)

- [Moonshot AI (Kimi + Kimi Coding)](/providers/moonshot)

- [OpenCode Zen](/providers/opencode)

- [Amazon Bedrock](/bedrock)

- [Z.AI](/providers/zai)

- [Xiaomi](/providers/xiaomi)

- [GLM models](/providers/glm)

- [MiniMax](/providers/minimax)

- [Venice (Venice AI, privacy-focused)](/providers/venice)

- [Ollama (local models)](/providers/ollama)

## [​](#transcription-providers)Transcription providers

- [Deepgram (audio transcription)](/providers/deepgram)

## [​](#community-tools)Community tools

- [Claude Max API Proxy](/providers/claude-max-api-proxy) - Use Claude Max/Pro subscription as an OpenAI-compatible API endpoint

For the full provider catalog (xAI, Groq, Mistral, etc.) and advanced configuration,

see [Model providers](/concepts/model-providers).[Model Provider Quickstart](/providers/models)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)