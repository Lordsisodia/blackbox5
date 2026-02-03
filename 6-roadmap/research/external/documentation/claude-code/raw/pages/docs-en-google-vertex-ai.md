---
{
  "fetch": {
    "url": "https://code.claude.com/docs/en/google-vertex-ai",
    "fetched_at": "2026-02-04T00:53:42.404706",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 569797
  },
  "metadata": {
    "title": "Claude Code on Google Vertex AI",
    "section": "google-vertex-ai",
    "tier": 3,
    "type": "reference"
  }
}
---

- Claude Code on Google Vertex AI - Claude Code Docs[Skip to main content](#content-area)[Claude Code Docs home page](/docs)EnglishSearch...⌘KAsk AI[Claude Developer Platform](https://platform.claude.com/)- [Claude Code on the Web](https://claude.ai/code)- [Claude Code on the Web](https://claude.ai/code)Search...NavigationDeploymentClaude Code on Google Vertex AI[Getting started](/docs/en/overview)[Build with Claude Code](/docs/en/sub-agents)[Deployment](/docs/en/third-party-integrations)[Administration](/docs/en/setup)[Configuration](/docs/en/settings)[Reference](/docs/en/cli-reference)[Resources](/docs/en/legal-and-compliance)Deployment- [Overview](/docs/en/third-party-integrations)- [Amazon Bedrock](/docs/en/amazon-bedrock)- [Google Vertex AI](/docs/en/google-vertex-ai)- [Microsoft Foundry](/docs/en/microsoft-foundry)- [Network configuration](/docs/en/network-config)- [LLM gateway](/docs/en/llm-gateway)- [Development containers](/docs/en/devcontainer)On this page- [Prerequisites](#prerequisites)- [Region Configuration](#region-configuration)- [Setup](#setup)- [1. Enable Vertex AI API](#1-enable-vertex-ai-api)- [2. Request model access](#2-request-model-access)- [3. Configure GCP credentials](#3-configure-gcp-credentials)- [4. Configure Claude Code](#4-configure-claude-code)- [5. Model configuration](#5-model-configuration)- [IAM configuration](#iam-configuration)- [1M token context window](#1m-token-context-window)- [Troubleshooting](#troubleshooting)- [Additional resources](#additional-resources)Deployment# Claude Code on Google Vertex AICopy pageLearn about configuring Claude Code through Google Vertex AI, including setup, IAM configuration, and troubleshooting.Copy page## [​](#prerequisites)Prerequisites

Before configuring Claude Code with Vertex AI, ensure you have:

- A Google Cloud Platform (GCP) account with billing enabled

- A GCP project with Vertex AI API enabled

- Access to desired Claude models (for example, Claude Sonnet 4.5)

- Google Cloud SDK (`gcloud`) installed and configured

- Quota allocated in desired GCP region

## [​](#region-configuration)Region Configuration

Claude Code can be used with both Vertex AI [global](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai) and regional endpoints.

Vertex AI may not support the Claude Code default models on all regions. You may need to switch to a [supported region or model](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models).

Vertex AI may not support the Claude Code default models on global endpoints. You may need to switch to a regional endpoint or [supported model](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models).

## [​](#setup)Setup

### [​](#1-enable-vertex-ai-api)1. Enable Vertex AI API

Enable the Vertex AI API in your GCP project:

CopyAsk AI```

# Set your project ID

gcloud config set project YOUR-PROJECT-ID

# Enable Vertex AI API

gcloud services enable aiplatform.googleapis.com

```

### [​](#2-request-model-access)2. Request model access

Request access to Claude models in Vertex AI:

- Navigate to the [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)

- Search for “Claude” models

- Request access to desired Claude models (for example, Claude Sonnet 4.5)

- Wait for approval (may take 24-48 hours)

### [​](#3-configure-gcp-credentials)3. Configure GCP credentials

Claude Code uses standard Google Cloud authentication.

For more information, see [Google Cloud authentication documentation](https://cloud.google.com/docs/authentication).

When authenticating, Claude Code will automatically use the project ID from the `ANTHROPIC_VERTEX_PROJECT_ID` environment variable. To override this, set one of these environment variables: `GCLOUD_PROJECT`, `GOOGLE_CLOUD_PROJECT`, or `GOOGLE_APPLICATION_CREDENTIALS`.

### [​](#4-configure-claude-code)4. Configure Claude Code

Set the following environment variables:

CopyAsk AI```

# Enable Vertex AI integration

export CLAUDE_CODE_USE_VERTEX=1

export CLOUD_ML_REGION=global

export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID

# Optional: Disable prompt caching if needed

export DISABLE_PROMPT_CACHING=1

# When CLOUD_ML_REGION=global, override region for unsupported models

export VERTEX_REGION_CLAUDE_3_5_HAIKU=us-east5

# Optional: Override regions for other specific models

export VERTEX_REGION_CLAUDE_3_5_SONNET=us-east5

export VERTEX_REGION_CLAUDE_3_7_SONNET=us-east5

export VERTEX_REGION_CLAUDE_4_0_OPUS=europe-west1

export VERTEX_REGION_CLAUDE_4_0_SONNET=us-east5

export VERTEX_REGION_CLAUDE_4_1_OPUS=europe-west1

```

[Prompt caching](https://docs.claude.com/en/docs/build-with-claude/prompt-caching) is automatically supported when you specify the `cache_control` ephemeral flag. To disable it, set `DISABLE_PROMPT_CACHING=1`. For heightened rate limits, contact Google Cloud support.

When using Vertex AI, the `/login` and `/logout` commands are disabled since authentication is handled through Google Cloud credentials.

### [​](#5-model-configuration)5. Model configuration

Claude Code uses these default models for Vertex AI:

Model typeDefault valuePrimary model`claude-sonnet-4-5@20250929`Small/fast model`claude-haiku-4-5@20251001`

For Vertex AI users, Claude Code will not automatically upgrade from Haiku 3.5 to Haiku 4.5. To manually switch to a newer Haiku model, set the `ANTHROPIC_DEFAULT_HAIKU_MODEL` environment variable to the full model name (for example, `claude-haiku-4-5@20251001`).

To customize models:

CopyAsk AI```

export ANTHROPIC_MODEL='claude-opus-4-1@20250805'

export ANTHROPIC_SMALL_FAST_MODEL='claude-haiku-4-5@20251001'

```

## [​](#iam-configuration)IAM configuration

Assign the required IAM permissions:

The `roles/aiplatform.user` role includes the required permissions:

- `aiplatform.endpoints.predict` - Required for model invocation and token counting

For more restrictive permissions, create a custom role with only the permissions above.

For details, see [Vertex IAM documentation](https://cloud.google.com/vertex-ai/docs/general/access-control).

We recommend creating a dedicated GCP project for Claude Code to simplify cost tracking and access control.

## [​](#1m-token-context-window)1M token context window

Claude Sonnet 4 and Sonnet 4.5 support the [1M token context window](https://docs.claude.com/en/docs/build-with-claude/context-windows#1m-token-context-window) on Vertex AI.

The 1M token context window is currently in beta. To use the extended context window, include the `context-1m-2025-08-07` beta header in your Vertex AI requests.

## [​](#troubleshooting)Troubleshooting

If you encounter quota issues:

- Check current quotas or request quota increase through [Cloud Console](https://cloud.google.com/docs/quotas/view-manage)

If you encounter “model not found” 404 errors:

- Confirm model is Enabled in [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)

- Verify you have access to the specified region

- If using `CLOUD_ML_REGION=global`, check that your models support global endpoints in [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) under “Supported features”. For models that don’t support global endpoints, either:

Specify a supported model via `ANTHROPIC_MODEL` or `ANTHROPIC_SMALL_FAST_MODEL`, or

- Set a regional endpoint using `VERTEX_REGION_<MODEL_NAME>` environment variables

If you encounter 429 errors:

- For regional endpoints, ensure the primary model and small/fast model are supported in your selected region

- Consider switching to `CLOUD_ML_REGION=global` for better availability

## [​](#additional-resources)Additional resources

- [Vertex AI documentation](https://cloud.google.com/vertex-ai/docs)

- [Vertex AI pricing](https://cloud.google.com/vertex-ai/pricing)

- [Vertex AI quotas and limits](https://cloud.google.com/vertex-ai/docs/quotas)

Was this page helpful?YesNo[Amazon Bedrock](/docs/en/amazon-bedrock)[Microsoft Foundry](/docs/en/microsoft-foundry)⌘I[Claude Code Docs home page](/docs)[x](https://x.com/AnthropicAI)[linkedin](https://www.linkedin.com/company/anthropicresearch)Company[Anthropic](https://www.anthropic.com/company)[Careers](https://www.anthropic.com/careers)[Economic Futures](https://www.anthropic.com/economic-futures)[Research](https://www.anthropic.com/research)[News](https://www.anthropic.com/news)[Trust center](https://trust.anthropic.com/)[Transparency](https://www.anthropic.com/transparency)Help and security[Availability](https://www.anthropic.com/supported-countries)[Status](https://status.anthropic.com/)[Support center](https://support.claude.com/)Learn[Courses](https://www.anthropic.com/learn)[MCP connectors](https://claude.com/partners/mcp)[Customer stories](https://www.claude.com/customers)[Engineering blog](https://www.anthropic.com/engineering)[Events](https://www.anthropic.com/events)[Powered by Claude](https://claude.com/partners/powered-by-claude)[Service partners](https://claude.com/partners/services)[Startups program](https://claude.com/programs/startups)Terms and policies[Privacy policy](https://www.anthropic.com/legal/privacy)[Disclosure policy](https://www.anthropic.com/responsible-disclosure-policy)[Usage policy](https://www.anthropic.com/legal/aup)[Commercial terms](https://www.anthropic.com/legal/commercial-terms)[Consumer terms](https://www.anthropic.com/legal/consumer-terms)