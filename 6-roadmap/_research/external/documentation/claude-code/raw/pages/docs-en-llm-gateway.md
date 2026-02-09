---
{
  "fetch": {
    "url": "https://code.claude.com/docs/en/llm-gateway",
    "fetched_at": "2026-02-04T00:53:49.160602",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 608010
  },
  "metadata": {
    "title": "LLM gateway configuration",
    "section": "llm-gateway",
    "tier": 3,
    "type": "reference"
  }
}
---

- LLM gateway configuration - Claude Code Docs[Skip to main content](#content-area)[Claude Code Docs home page](/docs)EnglishSearch...⌘KAsk AI[Claude Developer Platform](https://platform.claude.com/)- [Claude Code on the Web](https://claude.ai/code)- [Claude Code on the Web](https://claude.ai/code)Search...NavigationDeploymentLLM gateway configuration[Getting started](/docs/en/overview)[Build with Claude Code](/docs/en/sub-agents)[Deployment](/docs/en/third-party-integrations)[Administration](/docs/en/setup)[Configuration](/docs/en/settings)[Reference](/docs/en/cli-reference)[Resources](/docs/en/legal-and-compliance)Deployment- [Overview](/docs/en/third-party-integrations)- [Amazon Bedrock](/docs/en/amazon-bedrock)- [Google Vertex AI](/docs/en/google-vertex-ai)- [Microsoft Foundry](/docs/en/microsoft-foundry)- [Network configuration](/docs/en/network-config)- [LLM gateway](/docs/en/llm-gateway)- [Development containers](/docs/en/devcontainer)On this page- [Gateway requirements](#gateway-requirements)- [Configuration](#configuration)- [Model selection](#model-selection)- [LiteLLM configuration](#litellm-configuration)- [Prerequisites](#prerequisites)- [Basic LiteLLM setup](#basic-litellm-setup)- [Authentication methods](#authentication-methods)- [Unified endpoint (recommended)](#unified-endpoint-recommended)- [Provider-specific pass-through endpoints (alternative)](#provider-specific-pass-through-endpoints-alternative)- [Additional resources](#additional-resources)Deployment# LLM gateway configurationCopy pageLearn how to configure Claude Code to work with LLM gateway solutions. Covers gateway requirements, authentication configuration, model selection, and provider-specific endpoint setup.Copy pageLLM gateways provide a centralized proxy layer between Claude Code and model providers, often providing:

- **Centralized authentication** - Single point for API key management

- **Usage tracking** - Monitor usage across teams and projects

- **Cost controls** - Implement budgets and rate limits

- **Audit logging** - Track all model interactions for compliance

- **Model routing** - Switch between providers without code changes

## [​](#gateway-requirements)Gateway requirements

For an LLM gateway to work with Claude Code, it must meet the following requirements:

**API format**

The gateway must expose to clients at least one of the following API formats:

-

**Anthropic Messages**: `/v1/messages`, `/v1/messages/count_tokens`

Must forward request headers: `anthropic-beta`, `anthropic-version`

-

**Bedrock InvokeModel**: `/invoke`, `/invoke-with-response-stream`

Must preserve request body fields: `anthropic_beta`, `anthropic_version`

-

**Vertex rawPredict**: `:rawPredict`, `:streamRawPredict`, `/count-tokens:rawPredict`

Must forward request headers: `anthropic-beta`, `anthropic-version`

Failure to forward headers or preserve body fields may result in reduced functionality or inability to use Claude Code features.

Claude Code determines which features to enable based on the API format. When using the Anthropic Messages format with Bedrock or Vertex, you may need to set environment variable `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1`.

## [​](#configuration)Configuration

### [​](#model-selection)Model selection

By default, Claude Code will use standard model names for the selected API format.

If you have configured custom model names in your gateway, use the environment variables documented in [Model configuration](/docs/en/model-config) to match your custom names.

## [​](#litellm-configuration)LiteLLM configuration

LiteLLM is a third-party proxy service. Anthropic doesn’t endorse, maintain, or audit LiteLLM’s security or functionality. This guide is provided for informational purposes and may become outdated. Use at your own discretion.

### [​](#prerequisites)Prerequisites

- Claude Code updated to the latest version

- LiteLLM Proxy Server deployed and accessible

- Access to Claude models through your chosen provider

### [​](#basic-litellm-setup)Basic LiteLLM setup

**Configure Claude Code**:

#### [​](#authentication-methods)Authentication methods

Static API key

Simplest method using a fixed API key:

CopyAsk AI```

# Set in environment

export ANTHROPIC_AUTH_TOKEN=sk-litellm-static-key

# Or in Claude Code settings

{

"env": {

"ANTHROPIC_AUTH_TOKEN": "sk-litellm-static-key"

}

}

```

This value will be sent as the `Authorization` header.

Dynamic API key with helper

For rotating keys or per-user authentication:

- Create an API key helper script:

CopyAsk AI```

#!/bin/bash

# ~/bin/get-litellm-key.sh

# Example: Fetch key from vault

vault kv get -field=api_key secret/litellm/claude-code

# Example: Generate JWT token

jwt encode \

--secret="${JWT_SECRET}" \

--exp="+1h" \

'{"user":"'${USER}'","team":"engineering"}'

```

- Configure Claude Code settings to use the helper:

CopyAsk AI```

{

"apiKeyHelper": "~/bin/get-litellm-key.sh"

}

```

- Set token refresh interval:

CopyAsk AI```

# Refresh every hour (3600000 ms)

export CLAUDE_CODE_API_KEY_HELPER_TTL_MS=3600000

```

This value will be sent as `Authorization` and `X-Api-Key` headers. The `apiKeyHelper` has lower precedence than `ANTHROPIC_AUTH_TOKEN` or `ANTHROPIC_API_KEY`.

#### [​](#unified-endpoint-recommended)Unified endpoint (recommended)

Using LiteLLM’s [Anthropic format endpoint](https://docs.litellm.ai/docs/anthropic_unified):

CopyAsk AI```

export ANTHROPIC_BASE_URL=https://litellm-server:4000

```

**Benefits of the unified endpoint over pass-through endpoints:**

- Load balancing

- Fallbacks

- Consistent support for cost tracking and end-user tracking

#### [​](#provider-specific-pass-through-endpoints-alternative)Provider-specific pass-through endpoints (alternative)

Claude API through LiteLLM

Using [pass-through endpoint](https://docs.litellm.ai/docs/pass_through/anthropic_completion):

CopyAsk AI```

export ANTHROPIC_BASE_URL=https://litellm-server:4000/anthropic

```

Amazon Bedrock through LiteLLM

Using [pass-through endpoint](https://docs.litellm.ai/docs/pass_through/bedrock):

CopyAsk AI```

export ANTHROPIC_BEDROCK_BASE_URL=https://litellm-server:4000/bedrock

export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1

export CLAUDE_CODE_USE_BEDROCK=1

```

Google Vertex AI through LiteLLM

Using [pass-through endpoint](https://docs.litellm.ai/docs/pass_through/vertex_ai):

CopyAsk AI```

export ANTHROPIC_VERTEX_BASE_URL=https://litellm-server:4000/vertex_ai/v1

export ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id

export CLAUDE_CODE_SKIP_VERTEX_AUTH=1

export CLAUDE_CODE_USE_VERTEX=1

export CLOUD_ML_REGION=us-east5

```

For more detailed information, refer to the [LiteLLM documentation](https://docs.litellm.ai/).

## [​](#additional-resources)Additional resources

- [LiteLLM documentation](https://docs.litellm.ai/)

- [Claude Code settings](/docs/en/settings)

- [Enterprise network configuration](/docs/en/network-config)

- [Third-party integrations overview](/docs/en/third-party-integrations)

Was this page helpful?YesNo[Network configuration](/docs/en/network-config)[Development containers](/docs/en/devcontainer)⌘I[Claude Code Docs home page](/docs)[x](https://x.com/AnthropicAI)[linkedin](https://www.linkedin.com/company/anthropicresearch)Company[Anthropic](https://www.anthropic.com/company)[Careers](https://www.anthropic.com/careers)[Economic Futures](https://www.anthropic.com/economic-futures)[Research](https://www.anthropic.com/research)[News](https://www.anthropic.com/news)[Trust center](https://trust.anthropic.com/)[Transparency](https://www.anthropic.com/transparency)Help and security[Availability](https://www.anthropic.com/supported-countries)[Status](https://status.anthropic.com/)[Support center](https://support.claude.com/)Learn[Courses](https://www.anthropic.com/learn)[MCP connectors](https://claude.com/partners/mcp)[Customer stories](https://www.claude.com/customers)[Engineering blog](https://www.anthropic.com/engineering)[Events](https://www.anthropic.com/events)[Powered by Claude](https://claude.com/partners/powered-by-claude)[Service partners](https://claude.com/partners/services)[Startups program](https://claude.com/programs/startups)Terms and policies[Privacy policy](https://www.anthropic.com/legal/privacy)[Disclosure policy](https://www.anthropic.com/responsible-disclosure-policy)[Usage policy](https://www.anthropic.com/legal/aup)[Commercial terms](https://www.anthropic.com/legal/commercial-terms)[Consumer terms](https://www.anthropic.com/legal/consumer-terms)