---
{
  "fetch": {
    "url": "https://code.claude.com/docs/en/microsoft-foundry",
    "fetched_at": "2026-02-04T00:53:50.355656",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 534154
  },
  "metadata": {
    "title": "Claude Code on Microsoft Foundry",
    "section": "microsoft-foundry",
    "tier": 3,
    "type": "reference"
  }
}
---

- Claude Code on Microsoft Foundry - Claude Code Docs[Skip to main content](#content-area)[Claude Code Docs home page](/docs)EnglishSearch...⌘KAsk AI[Claude Developer Platform](https://platform.claude.com/)- [Claude Code on the Web](https://claude.ai/code)- [Claude Code on the Web](https://claude.ai/code)Search...NavigationDeploymentClaude Code on Microsoft Foundry[Getting started](/docs/en/overview)[Build with Claude Code](/docs/en/sub-agents)[Deployment](/docs/en/third-party-integrations)[Administration](/docs/en/setup)[Configuration](/docs/en/settings)[Reference](/docs/en/cli-reference)[Resources](/docs/en/legal-and-compliance)Deployment- [Overview](/docs/en/third-party-integrations)- [Amazon Bedrock](/docs/en/amazon-bedrock)- [Google Vertex AI](/docs/en/google-vertex-ai)- [Microsoft Foundry](/docs/en/microsoft-foundry)- [Network configuration](/docs/en/network-config)- [LLM gateway](/docs/en/llm-gateway)- [Development containers](/docs/en/devcontainer)On this page- [Prerequisites](#prerequisites)- [Setup](#setup)- [1. Provision Microsoft Foundry resource](#1-provision-microsoft-foundry-resource)- [2. Configure Azure credentials](#2-configure-azure-credentials)- [3. Configure Claude Code](#3-configure-claude-code)- [Azure RBAC configuration](#azure-rbac-configuration)- [Troubleshooting](#troubleshooting)- [Additional resources](#additional-resources)Deployment# Claude Code on Microsoft FoundryCopy pageLearn about configuring Claude Code through Microsoft Foundry, including setup, configuration, and troubleshooting.Copy page## [​](#prerequisites)Prerequisites

Before configuring Claude Code with Microsoft Foundry, ensure you have:

- An Azure subscription with access to Microsoft Foundry

- RBAC permissions to create Microsoft Foundry resources and deployments

- Azure CLI installed and configured (optional - only needed if you don’t have another mechanism for getting credentials)

## [​](#setup)Setup

### [​](#1-provision-microsoft-foundry-resource)1. Provision Microsoft Foundry resource

First, create a Claude resource in Azure:

- Navigate to the [Microsoft Foundry portal](https://ai.azure.com/)

- Create a new resource, noting your resource name

- Create deployments for the Claude models:

Claude Opus

- Claude Sonnet

- Claude Haiku

### [​](#2-configure-azure-credentials)2. Configure Azure credentials

Claude Code supports two authentication methods for Microsoft Foundry. Choose the method that best fits your security requirements.

**Option A: API key authentication**

- Navigate to your resource in the Microsoft Foundry portal

- Go to the **Endpoints and keys** section

- Copy **API Key**

- Set the environment variable:

CopyAsk AI```

export ANTHROPIC_FOUNDRY_API_KEY=your-azure-api-key

```

**Option B: Microsoft Entra ID authentication**

When `ANTHROPIC_FOUNDRY_API_KEY` is not set, Claude Code automatically uses the Azure SDK [default credential chain](https://learn.microsoft.com/en-us/azure/developer/javascript/sdk/authentication/credential-chains#defaultazurecredential-overview).

This supports a variety of methods for authenticating local and remote workloads.

On local environments, you commonly may use the Azure CLI:

CopyAsk AI```

az login

```

When using Microsoft Foundry, the `/login` and `/logout` commands are disabled since authentication is handled through Azure credentials.

### [​](#3-configure-claude-code)3. Configure Claude Code

Set the following environment variables to enable Microsoft Foundry. Note that your deployments’ names are set as the model identifiers in Claude Code (may be optional if using suggested deployment names).

CopyAsk AI```

# Enable Microsoft Foundry integration

export CLAUDE_CODE_USE_FOUNDRY=1

# Azure resource name (replace {resource} with your resource name)

export ANTHROPIC_FOUNDRY_RESOURCE={resource}

# Or provide the full base URL:

# export ANTHROPIC_FOUNDRY_BASE_URL=https://{resource}.services.ai.azure.com/anthropic

# Set models to your resource's deployment names

export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-5'

export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5'

export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-1'

```

For more details on model configuration options, see [Model configuration](/docs/en/model-config).

## [​](#azure-rbac-configuration)Azure RBAC configuration

The `Azure AI User` and `Cognitive Services User` default roles include all required permissions for invoking Claude models.

For more restrictive permissions, create a custom role with the following:

CopyAsk AI```

{

"permissions": [

{

"dataActions": [

"Microsoft.CognitiveServices/accounts/providers/*"

]

}

]

}

```

For details, see [Microsoft Foundry RBAC documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-azure-ai-foundry).

## [​](#troubleshooting)Troubleshooting

If you receive an error “Failed to get token from azureADTokenProvider: ChainedTokenCredential authentication failed”:

- Configure Entra ID on the environment, or set `ANTHROPIC_FOUNDRY_API_KEY`.

## [​](#additional-resources)Additional resources

- [Microsoft Foundry documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry)

- [Microsoft Foundry models](https://ai.azure.com/explore/models)

- [Microsoft Foundry pricing](https://azure.microsoft.com/en-us/pricing/details/ai-foundry/)

Was this page helpful?YesNo[Google Vertex AI](/docs/en/google-vertex-ai)[Network configuration](/docs/en/network-config)⌘I[Claude Code Docs home page](/docs)[x](https://x.com/AnthropicAI)[linkedin](https://www.linkedin.com/company/anthropicresearch)Company[Anthropic](https://www.anthropic.com/company)[Careers](https://www.anthropic.com/careers)[Economic Futures](https://www.anthropic.com/economic-futures)[Research](https://www.anthropic.com/research)[News](https://www.anthropic.com/news)[Trust center](https://trust.anthropic.com/)[Transparency](https://www.anthropic.com/transparency)Help and security[Availability](https://www.anthropic.com/supported-countries)[Status](https://status.anthropic.com/)[Support center](https://support.claude.com/)Learn[Courses](https://www.anthropic.com/learn)[MCP connectors](https://claude.com/partners/mcp)[Customer stories](https://www.claude.com/customers)[Engineering blog](https://www.anthropic.com/engineering)[Events](https://www.anthropic.com/events)[Powered by Claude](https://claude.com/partners/powered-by-claude)[Service partners](https://claude.com/partners/services)[Startups program](https://claude.com/programs/startups)Terms and policies[Privacy policy](https://www.anthropic.com/legal/privacy)[Disclosure policy](https://www.anthropic.com/responsible-disclosure-policy)[Usage policy](https://www.anthropic.com/legal/aup)[Commercial terms](https://www.anthropic.com/legal/commercial-terms)[Consumer terms](https://www.anthropic.com/legal/consumer-terms)