---
{
  "fetch": {
    "url": "https://code.claude.com/docs/en/amazon-bedrock",
    "fetched_at": "2026-02-04T00:53:31.959653",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 689550
  },
  "metadata": {
    "title": "Claude Code on Amazon Bedrock",
    "section": "amazon-bedrock",
    "tier": 3,
    "type": "reference"
  }
}
---

- Claude Code on Amazon Bedrock - Claude Code Docs[Skip to main content](#content-area)[Claude Code Docs home page](/docs)EnglishSearch...⌘KAsk AI[Claude Developer Platform](https://platform.claude.com/)- [Claude Code on the Web](https://claude.ai/code)- [Claude Code on the Web](https://claude.ai/code)Search...NavigationDeploymentClaude Code on Amazon Bedrock[Getting started](/docs/en/overview)[Build with Claude Code](/docs/en/sub-agents)[Deployment](/docs/en/third-party-integrations)[Administration](/docs/en/setup)[Configuration](/docs/en/settings)[Reference](/docs/en/cli-reference)[Resources](/docs/en/legal-and-compliance)Deployment- [Overview](/docs/en/third-party-integrations)- [Amazon Bedrock](/docs/en/amazon-bedrock)- [Google Vertex AI](/docs/en/google-vertex-ai)- [Microsoft Foundry](/docs/en/microsoft-foundry)- [Network configuration](/docs/en/network-config)- [LLM gateway](/docs/en/llm-gateway)- [Development containers](/docs/en/devcontainer)On this page- [Prerequisites](#prerequisites)- [Setup](#setup)- [1. Submit use case details](#1-submit-use-case-details)- [2. Configure AWS credentials](#2-configure-aws-credentials)- [Advanced credential configuration](#advanced-credential-configuration)- [3. Configure Claude Code](#3-configure-claude-code)- [4. Model configuration](#4-model-configuration)- [5. Output token configuration](#5-output-token-configuration)- [IAM configuration](#iam-configuration)- [AWS Guardrails](#aws-guardrails)- [Troubleshooting](#troubleshooting)- [Additional resources](#additional-resources)Deployment# Claude Code on Amazon BedrockCopy pageLearn about configuring Claude Code through Amazon Bedrock, including setup, IAM configuration, and troubleshooting.Copy page## [​](#prerequisites)Prerequisites

Before configuring Claude Code with Bedrock, ensure you have:

- An AWS account with Bedrock access enabled

- Access to desired Claude models (for example, Claude Sonnet 4.5) in Bedrock

- AWS CLI installed and configured (optional - only needed if you don’t have another mechanism for getting credentials)

- Appropriate IAM permissions

## [​](#setup)Setup

### [​](#1-submit-use-case-details)1. Submit use case details

First-time users of Anthropic models are required to submit use case details before invoking a model. This is done once per account.

- Ensure you have the right IAM permissions (see more on that below)

- Navigate to the [Amazon Bedrock console](https://console.aws.amazon.com/bedrock/)

- Select **Chat/Text playground**

- Choose any Anthropic model and you will be prompted to fill out the use case form

### [​](#2-configure-aws-credentials)2. Configure AWS credentials

Claude Code uses the default AWS SDK credential chain. Set up your credentials using one of these methods:

**Option A: AWS CLI configuration**

CopyAsk AI```

aws configure

```

**Option B: Environment variables (access key)**

CopyAsk AI```

export AWS_ACCESS_KEY_ID=your-access-key-id

export AWS_SECRET_ACCESS_KEY=your-secret-access-key

export AWS_SESSION_TOKEN=your-session-token

```

**Option C: Environment variables (SSO profile)**

CopyAsk AI```

aws sso login --profile=<your-profile-name>

export AWS_PROFILE=your-profile-name

```

**Option D: AWS Management Console credentials**

CopyAsk AI```

aws login

```

[Learn more](https://docs.aws.amazon.com/signin/latest/userguide/command-line-sign-in.html) about `aws login`.

**Option E: Bedrock API keys**

CopyAsk AI```

export AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key

```

Bedrock API keys provide a simpler authentication method without needing full AWS credentials. [Learn more about Bedrock API keys](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/).

#### [​](#advanced-credential-configuration)Advanced credential configuration

Claude Code supports automatic credential refresh for AWS SSO and corporate identity providers. Add these settings to your Claude Code settings file (see [Settings](/docs/en/settings) for file locations).

When Claude Code detects that your AWS credentials are expired (either locally based on their timestamp or when Bedrock returns a credential error), it will automatically run your configured `awsAuthRefresh` and/or `awsCredentialExport` commands to obtain new credentials before retrying the request.

Example configuration

CopyAsk AI```

{

"awsAuthRefresh": "aws sso login --profile myprofile",

"env": {

"AWS_PROFILE": "myprofile"

}

}

```

Configuration settings explained

**`awsAuthRefresh`**: Use this for commands that modify the `.aws` directory, such as updating credentials, SSO cache, or config files. The command’s output is displayed to the user, but interactive input isn’t supported. This works well for browser-based SSO flows where the CLI displays a URL or code and you complete authentication in the browser.

**`awsCredentialExport`**: Only use this if you can’t modify `.aws` and must directly return credentials. Output is captured silently and not shown to the user. The command must output JSON in this format:

CopyAsk AI```

{

"Credentials": {

"AccessKeyId": "value",

"SecretAccessKey": "value",

"SessionToken": "value"

}

}

```

### [​](#3-configure-claude-code)3. Configure Claude Code

Set the following environment variables to enable Bedrock:

CopyAsk AI```

# Enable Bedrock integration

export CLAUDE_CODE_USE_BEDROCK=1

export AWS_REGION=us-east-1  # or your preferred region

# Optional: Override the region for the small/fast model (Haiku)

export ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION=us-west-2

```

When enabling Bedrock for Claude Code, keep the following in mind:

- `AWS_REGION` is a required environment variable. Claude Code does not read from the `.aws` config file for this setting.

- When using Bedrock, the `/login` and `/logout` commands are disabled since authentication is handled through AWS credentials.

- You can use settings files for environment variables like `AWS_PROFILE` that you don’t want to leak to other processes. See [Settings](/docs/en/settings) for more information.

### [​](#4-model-configuration)4. Model configuration

Claude Code uses these default models for Bedrock:

Model typeDefault valuePrimary model`global.anthropic.claude-sonnet-4-5-20250929-v1:0`Small/fast model`us.anthropic.claude-haiku-4-5-20251001-v1:0`

For Bedrock users, Claude Code won’t automatically upgrade from Haiku 3.5 to Haiku 4.5. To manually switch to a newer Haiku model, set the `ANTHROPIC_DEFAULT_HAIKU_MODEL` environment variable to the full model name (for example, `us.anthropic.claude-haiku-4-5-20251001-v1:0`).

To customize models, use one of these methods:

CopyAsk AI```

# Using inference profile ID

export ANTHROPIC_MODEL='global.anthropic.claude-sonnet-4-5-20250929-v1:0'

export ANTHROPIC_SMALL_FAST_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'

# Using application inference profile ARN

export ANTHROPIC_MODEL='arn:aws:bedrock:us-east-2:your-account-id:application-inference-profile/your-model-id'

# Optional: Disable prompt caching if needed

export DISABLE_PROMPT_CACHING=1

```

[Prompt caching](https://docs.claude.com/en/docs/build-with-claude/prompt-caching) may not be available in all regions.

### [​](#5-output-token-configuration)5. Output token configuration

These are the recommended token settings for Claude Code with Amazon Bedrock:

CopyAsk AI```

# Recommended output token settings for Bedrock

export CLAUDE_CODE_MAX_OUTPUT_TOKENS=4096

export MAX_THINKING_TOKENS=1024

```

**Why these values:**

-

**`CLAUDE_CODE_MAX_OUTPUT_TOKENS=4096`**: Bedrock’s burndown throttling logic sets a minimum of 4096 tokens as the `max_token` penalty. Setting this lower won’t reduce costs but may cut off long tool uses, causing the Claude Code agent loop to fail persistently. Claude Code typically uses less than 4096 output tokens without extended thinking, but may need this headroom for tasks involving significant file creation or Write tool usage.

-

**`MAX_THINKING_TOKENS=1024`**: This provides space for extended thinking without cutting off tool use responses, while still maintaining focused reasoning chains. This balance helps prevent trajectory changes that aren’t always helpful for coding tasks specifically.

## [​](#iam-configuration)IAM configuration

Create an IAM policy with the required permissions for Claude Code:

CopyAsk AI```

{

"Version": "2012-10-17",

"Statement": [

{

"Sid": "AllowModelAndInferenceProfileAccess",

"Effect": "Allow",

"Action": [

"bedrock:InvokeModel",

"bedrock:InvokeModelWithResponseStream",

"bedrock:ListInferenceProfiles"

],

"Resource": [

"arn:aws:bedrock:*:*:inference-profile/*",

"arn:aws:bedrock:*:*:application-inference-profile/*",

"arn:aws:bedrock:*:*:foundation-model/*"

]

},

{

"Sid": "AllowMarketplaceSubscription",

"Effect": "Allow",

"Action": [

"aws-marketplace:ViewSubscriptions",

"aws-marketplace:Subscribe"

],

"Resource": "*",

"Condition": {

"StringEquals": {

"aws:CalledViaLast": "bedrock.amazonaws.com"

}

}

}

]

}

```

For more restrictive permissions, you can limit the Resource to specific inference profile ARNs.

For details, see [Bedrock IAM documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html).

We recommend creating a dedicated AWS account for Claude Code to simplify cost tracking and access control.

## [​](#aws-guardrails)AWS Guardrails

[Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) let you implement content filtering for Claude Code. Create a Guardrail in the [Amazon Bedrock console](https://console.aws.amazon.com/bedrock/), publish a version, then add the Guardrail headers to your [settings file](/docs/en/settings). Enable Cross-Region inference on your Guardrail if you’re using cross-region inference profiles.

Example configuration:

CopyAsk AI```

{

"env": {

"ANTHROPIC_CUSTOM_HEADERS": "X-Amzn-Bedrock-GuardrailIdentifier: your-guardrail-id\nX-Amzn-Bedrock-GuardrailVersion: 1"

}

}

```

## [​](#troubleshooting)Troubleshooting

If you encounter region issues:

- Check model availability: `aws bedrock list-inference-profiles --region your-region`

- Switch to a supported region: `export AWS_REGION=us-east-1`

- Consider using inference profiles for cross-region access

If you receive an error “on-demand throughput isn’t supported”:

- Specify the model as an [inference profile](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) ID

Claude Code uses the Bedrock [Invoke API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) and does not support the Converse API.

## [​](#additional-resources)Additional resources

- [Bedrock documentation](https://docs.aws.amazon.com/bedrock/)

- [Bedrock pricing](https://aws.amazon.com/bedrock/pricing/)

- [Bedrock inference profiles](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)

- [Claude Code on Amazon Bedrock: Quick Setup Guide](https://community.aws/content/2tXkZKrZzlrlu0KfH8gST5Dkppq/claude-code-on-amazon-bedrock-quick-setup-guide)- [Claude Code Monitoring Implementation (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md)

Was this page helpful?YesNo[Overview](/docs/en/third-party-integrations)[Google Vertex AI](/docs/en/google-vertex-ai)⌘I[Claude Code Docs home page](/docs)[x](https://x.com/AnthropicAI)[linkedin](https://www.linkedin.com/company/anthropicresearch)Company[Anthropic](https://www.anthropic.com/company)[Careers](https://www.anthropic.com/careers)[Economic Futures](https://www.anthropic.com/economic-futures)[Research](https://www.anthropic.com/research)[News](https://www.anthropic.com/news)[Trust center](https://trust.anthropic.com/)[Transparency](https://www.anthropic.com/transparency)Help and security[Availability](https://www.anthropic.com/supported-countries)[Status](https://status.anthropic.com/)[Support center](https://support.claude.com/)Learn[Courses](https://www.anthropic.com/learn)[MCP connectors](https://claude.com/partners/mcp)[Customer stories](https://www.claude.com/customers)[Engineering blog](https://www.anthropic.com/engineering)[Events](https://www.anthropic.com/events)[Powered by Claude](https://claude.com/partners/powered-by-claude)[Service partners](https://claude.com/partners/services)[Startups program](https://claude.com/programs/startups)Terms and policies[Privacy policy](https://www.anthropic.com/legal/privacy)[Disclosure policy](https://www.anthropic.com/responsible-disclosure-policy)[Usage policy](https://www.anthropic.com/legal/aup)[Commercial terms](https://www.anthropic.com/legal/commercial-terms)[Consumer terms](https://www.anthropic.com/legal/consumer-terms)