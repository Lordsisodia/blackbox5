---
{
  "fetch": {
    "url": "https://docs.openclaw.ai/providers/synthetic",
    "fetched_at": "2026-02-07T10:21:14.980105",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 562166
  },
  "metadata": {
    "title": "Synthetic",
    "section": "synthetic",
    "tier": 3,
    "type": "reference"
  }
}
---

- Synthetic - OpenClaw[Skip to main content](#content-area)[OpenClaw home page](/)EnglishSearch...⌘K[GitHub](https://github.com/openclaw/openclaw)- [Releases](https://github.com/openclaw/openclaw/releases)Search...NavigationProvidersSynthetic[Get started](/)[Install](/install)[Channels](/channels)[Agents](/concepts/architecture)[Tools](/tools)[Models](/providers)[Platforms](/platforms)[Gateway & Ops](/gateway)[Reference](/cli)[Help](/help)Overview- [Model Providers](/providers)- [Model Provider Quickstart](/providers/models)- [Models CLI](/concepts/models)Configuration- [Model Providers](/concepts/model-providers)- [Model Failover](/concepts/model-failover)Providers- [Anthropic](/providers/anthropic)- [OpenAI](/providers/openai)- [OpenRouter](/providers/openrouter)- [Amazon Bedrock](/bedrock)- [Vercel AI Gateway](/providers/vercel-ai-gateway)- [Moonshot AI](/providers/moonshot)- [MiniMax](/providers/minimax)- [OpenCode Zen](/providers/opencode)- [GLM Models](/providers/glm)- [Z.AI](/providers/zai)- [Synthetic](/providers/synthetic)On this page- [Synthetic](#synthetic)- [Quick setup](#quick-setup)- [Config example](#config-example)- [Model catalog](#model-catalog)- [Notes](#notes)Providers# Synthetic# [​](#synthetic)Synthetic

Synthetic exposes Anthropic-compatible endpoints. OpenClaw registers it as the

`synthetic` provider and uses the Anthropic Messages API.

## [​](#quick-setup)Quick setup

- Set `SYNTHETIC_API_KEY` (or run the wizard below).

- Run onboarding:

Copy```

openclaw onboard --auth-choice synthetic-api-key

```

The default model is set to:

Copy```

synthetic/hf:MiniMaxAI/MiniMax-M2.1

```

## [​](#config-example)Config example

Copy```

{

env: { SYNTHETIC_API_KEY: "sk-..." },

agents: {

defaults: {

model: { primary: "synthetic/hf:MiniMaxAI/MiniMax-M2.1" },

models: { "synthetic/hf:MiniMaxAI/MiniMax-M2.1": { alias: "MiniMax M2.1" } },

},

},

models: {

mode: "merge",

providers: {

synthetic: {

baseUrl: "https://api.synthetic.new/anthropic",

apiKey: "${SYNTHETIC_API_KEY}",

api: "anthropic-messages",

models: [

{

id: "hf:MiniMaxAI/MiniMax-M2.1",

name: "MiniMax M2.1",

reasoning: false,

input: ["text"],

cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },

contextWindow: 192000,

maxTokens: 65536,

},

],

},

},

},

}

```

Note: OpenClaw’s Anthropic client appends `/v1` to the base URL, so use

`https://api.synthetic.new/anthropic` (not `/anthropic/v1`). If Synthetic changes

its base URL, override `models.providers.synthetic.baseUrl`.

## [​](#model-catalog)Model catalog

All models below use cost `0` (input/output/cache).

Model IDContext windowMax tokensReasoningInput`hf:MiniMaxAI/MiniMax-M2.1`19200065536falsetext`hf:moonshotai/Kimi-K2-Thinking`2560008192truetext`hf:zai-org/GLM-4.7`198000128000falsetext`hf:deepseek-ai/DeepSeek-R1-0528`1280008192falsetext`hf:deepseek-ai/DeepSeek-V3-0324`1280008192falsetext`hf:deepseek-ai/DeepSeek-V3.1`1280008192falsetext`hf:deepseek-ai/DeepSeek-V3.1-Terminus`1280008192falsetext`hf:deepseek-ai/DeepSeek-V3.2`1590008192falsetext`hf:meta-llama/Llama-3.3-70B-Instruct`1280008192falsetext`hf:meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8`5240008192falsetext`hf:moonshotai/Kimi-K2-Instruct-0905`2560008192falsetext`hf:openai/gpt-oss-120b`1280008192falsetext`hf:Qwen/Qwen3-235B-A22B-Instruct-2507`2560008192falsetext`hf:Qwen/Qwen3-Coder-480B-A35B-Instruct`2560008192falsetext`hf:Qwen/Qwen3-VL-235B-A22B-Instruct`2500008192falsetext + image`hf:zai-org/GLM-4.5`128000128000falsetext`hf:zai-org/GLM-4.6`198000128000falsetext`hf:deepseek-ai/DeepSeek-V3`1280008192falsetext`hf:Qwen/Qwen3-235B-A22B-Thinking-2507`2560008192truetext

## [​](#notes)Notes

- Model refs use `synthetic/<modelId>`.

- If you enable a model allowlist (`agents.defaults.models`), add every model you

plan to use.

- See [Model providers](/concepts/model-providers) for provider rules.

[Z.AI](/providers/zai)⌘I[Powered by](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=clawdhub)