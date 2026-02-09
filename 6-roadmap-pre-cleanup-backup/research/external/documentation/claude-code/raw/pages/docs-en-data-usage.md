---
{
  "fetch": {
    "url": "https://code.claude.com/docs/en/data-usage",
    "fetched_at": "2026-02-04T00:53:38.875413",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 524059
  },
  "metadata": {
    "title": "Data usage",
    "section": "data-usage",
    "tier": 3,
    "type": "reference"
  }
}
---

- Data usage - Claude Code Docs[Skip to main content](#content-area)[Claude Code Docs home page](/docs)EnglishSearch...⌘KAsk AI[Claude Developer Platform](https://platform.claude.com/)- [Claude Code on the Web](https://claude.ai/code)- [Claude Code on the Web](https://claude.ai/code)Search...NavigationAdministrationData usage[Getting started](/docs/en/overview)[Build with Claude Code](/docs/en/sub-agents)[Deployment](/docs/en/third-party-integrations)[Administration](/docs/en/setup)[Configuration](/docs/en/settings)[Reference](/docs/en/cli-reference)[Resources](/docs/en/legal-and-compliance)Administration- [Advanced installation](/docs/en/setup)- [Authentication](/docs/en/authentication)- [Security](/docs/en/security)- [Data usage](/docs/en/data-usage)- [Monitoring](/docs/en/monitoring-usage)- [Costs](/docs/en/costs)- [Track team usage with analytics](/docs/en/analytics)- [Create and distribute a plugin marketplace](/docs/en/plugin-marketplaces)On this page- [Data policies](#data-policies)- [Data training policy](#data-training-policy)- [Development Partner Program](#development-partner-program)- [Feedback using the /bug command](#feedback-using-the-%2Fbug-command)- [Session quality surveys](#session-quality-surveys)- [Data retention](#data-retention)- [Data access](#data-access)- [Local Claude Code: Data flow and dependencies](#local-claude-code%3A-data-flow-and-dependencies)- [Cloud execution: Data flow and dependencies](#cloud-execution%3A-data-flow-and-dependencies)- [Telemetry services](#telemetry-services)- [Default behaviors by API provider](#default-behaviors-by-api-provider)Administration# Data usageCopy pageLearn about Anthropic’s data usage policies for ClaudeCopy page## [​](#data-policies)Data policies

### [​](#data-training-policy)Data training policy

**Consumer users (Free, Pro, and Max plans)**:

We give you the choice to allow your data to be used to improve future Claude models. We will train new models using data from Free, Pro, and Max accounts when this setting is on (including when you use Claude Code from these accounts).

**Commercial users**: (Team and Enterprise plans, API, 3rd-party platforms, and Claude Gov) maintain existing policies: Anthropic does not train generative models using code or prompts sent to Claude Code under commercial terms, unless the customer has chosen to provide their data to us for model improvement (for example, the [Developer Partner Program](https://support.claude.com/en/articles/11174108-about-the-development-partner-program)).

### [​](#development-partner-program)Development Partner Program

If you explicitly opt in to methods to provide us with materials to train on, such as via the [Development Partner Program](https://support.claude.com/en/articles/11174108-about-the-development-partner-program), we may use those materials provided to train our models. An organization admin can expressly opt-in to the Development Partner Program for their organization. Note that this program is available only for Anthropic first-party API, and not for Bedrock or Vertex users.

### [​](#feedback-using-the-/bug-command)Feedback using the `/bug` command

If you choose to send us feedback about Claude Code using the `/bug` command, we may use your feedback to improve our products and services. Transcripts shared via `/bug` are retained for 5 years.

### [​](#session-quality-surveys)Session quality surveys

When you see the “How is Claude doing this session?” prompt in Claude Code, responding to this survey (including selecting “Dismiss”), only your numeric rating (1, 2, 3, or dismiss) is recorded. We do not collect or store any conversation transcripts, inputs, outputs, or other session data as part of this survey. Unlike thumbs up/down feedback or `/bug` reports, this session quality survey is a simple product satisfaction metric. Your responses to this survey do not impact your data training preferences and cannot be used to train our AI models.

To disable these surveys, set `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1`. The survey is also automatically disabled when using third-party providers (Bedrock, Vertex, Foundry) or when telemetry is disabled.

### [​](#data-retention)Data retention

Anthropic retains Claude Code data based on your account type and preferences.

**Consumer users (Free, Pro, and Max plans)**:

- Users who allow data use for model improvement: 5-year retention period to support model development and safety improvements

- Users who don’t allow data use for model improvement: 30-day retention period

- Privacy settings can be changed at any time at [claude.ai/settings/data-privacy-controls](https://claude.ai/settings/data-privacy-controls).

**Commercial users (Team, Enterprise, and API)**:

- Standard: 30-day retention period

- Zero data retention: Available with appropriately configured API keys - Claude Code will not retain chat transcripts on servers

- Local caching: Claude Code clients may store sessions locally for up to 30 days to enable session resumption (configurable)

Learn more about data retention practices in our [Privacy Center](https://privacy.anthropic.com/).

For full details, please review our [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms) (for Team, Enterprise, and API users) or [Consumer Terms](https://www.anthropic.com/legal/consumer-terms) (for Free, Pro, and Max users) and [Privacy Policy](https://www.anthropic.com/legal/privacy).

## [​](#data-access)Data access

For all first party users, you can learn more about what data is logged for [local Claude Code](#local-claude-code-data-flow-and-dependencies) and [remote Claude Code](#cloud-execution-data-flow-and-dependencies). Note for remote Claude Code, Claude accesses the repository where you initiate your Claude Code session. Claude does not access repositories that you have connected but have not started a session in.

## [​](#local-claude-code:-data-flow-and-dependencies)Local Claude Code: Data flow and dependencies

The diagram below shows how Claude Code connects to external services during installation and normal operation. Solid lines indicate required connections, while dashed lines represent optional or user-initiated data flows.

Claude Code is installed from [NPM](https://www.npmjs.com/package/@anthropic-ai/claude-code). Claude Code runs locally. In order to interact with the LLM, Claude Code sends data over the network. This data includes all user prompts and model outputs. The data is encrypted in transit via TLS and is not encrypted at rest. Claude Code is compatible with most popular VPNs and LLM proxies.

Claude Code is built on Anthropic’s APIs. For details regarding our API’s security controls, including our API logging procedures, please refer to compliance artifacts offered in the [Anthropic Trust Center](https://trust.anthropic.com).

### [​](#cloud-execution:-data-flow-and-dependencies)Cloud execution: Data flow and dependencies

When using [Claude Code on the web](/docs/en/claude-code-on-the-web), sessions run in Anthropic-managed virtual machines instead of locally. In cloud environments:

- **Code and data storage:** Your repository is cloned to an isolated VM. Code and session data are subject to the retention and usage policies for your account type (see Data retention section above)

- **Credentials:** GitHub authentication is handled through a secure proxy; your GitHub credentials never enter the sandbox

- **Network traffic:** All outbound traffic goes through a security proxy for audit logging and abuse prevention

- **Session data:** Prompts, code changes, and outputs follow the same data policies as local Claude Code usage

For security details about cloud execution, see [Security](/docs/en/security#cloud-execution-security).

## [​](#telemetry-services)Telemetry services

Claude Code connects from users’ machines to the Statsig service to log operational metrics such as latency, reliability, and usage patterns. This logging does not include any code or file paths. Data is encrypted in transit using TLS and at rest using 256-bit AES encryption. Read more in the [Statsig security documentation](https://www.statsig.com/trust/security). To opt out of Statsig telemetry, set the `DISABLE_TELEMETRY` environment variable.

Claude Code connects from users’ machines to Sentry for operational error logging. The data is encrypted in transit using TLS and at rest using 256-bit AES encryption. Read more in the [Sentry security documentation](https://sentry.io/security/). To opt out of error logging, set the `DISABLE_ERROR_REPORTING` environment variable.

When users run the `/bug` command, a copy of their full conversation history including code is sent to Anthropic. The data is encrypted in transit and at rest. Optionally, a Github issue is created in our public repository. To opt out of bug reporting, set the `DISABLE_BUG_COMMAND` environment variable.

## [​](#default-behaviors-by-api-provider)Default behaviors by API provider

By default, we disable all non-essential traffic (including error reporting, telemetry, bug reporting functionality, and session quality surveys) when using Bedrock, Vertex, or Foundry. You can also opt out of all of these at once by setting the `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` environment variable. Here are the full default behaviors:

ServiceClaude APIVertex APIBedrock APIFoundry API**Statsig (Metrics)**Default on.`DISABLE_TELEMETRY=1` to disable.Default off.`CLAUDE_CODE_USE_VERTEX` must be 1.Default off.`CLAUDE_CODE_USE_BEDROCK` must be 1.Default off.`CLAUDE_CODE_USE_FOUNDRY` must be 1.**Sentry (Errors)**Default on.`DISABLE_ERROR_REPORTING=1` to disable.Default off.`CLAUDE_CODE_USE_VERTEX` must be 1.Default off.`CLAUDE_CODE_USE_BEDROCK` must be 1.Default off.`CLAUDE_CODE_USE_FOUNDRY` must be 1.**Claude API (`/bug` reports)**Default on.`DISABLE_BUG_COMMAND=1` to disable.Default off.`CLAUDE_CODE_USE_VERTEX` must be 1.Default off.`CLAUDE_CODE_USE_BEDROCK` must be 1.Default off.`CLAUDE_CODE_USE_FOUNDRY` must be 1.**Session quality surveys**Default on.`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` to disable.Default off.`CLAUDE_CODE_USE_VERTEX` must be 1.Default off.`CLAUDE_CODE_USE_BEDROCK` must be 1.Default off.`CLAUDE_CODE_USE_FOUNDRY` must be 1.

All environment variables can be checked into `settings.json` ([read more](/docs/en/settings)).Was this page helpful?YesNo[Security](/docs/en/security)[Monitoring](/docs/en/monitoring-usage)⌘I[Claude Code Docs home page](/docs)[x](https://x.com/AnthropicAI)[linkedin](https://www.linkedin.com/company/anthropicresearch)Company[Anthropic](https://www.anthropic.com/company)[Careers](https://www.anthropic.com/careers)[Economic Futures](https://www.anthropic.com/economic-futures)[Research](https://www.anthropic.com/research)[News](https://www.anthropic.com/news)[Trust center](https://trust.anthropic.com/)[Transparency](https://www.anthropic.com/transparency)Help and security[Availability](https://www.anthropic.com/supported-countries)[Status](https://status.anthropic.com/)[Support center](https://support.claude.com/)Learn[Courses](https://www.anthropic.com/learn)[MCP connectors](https://claude.com/partners/mcp)[Customer stories](https://www.claude.com/customers)[Engineering blog](https://www.anthropic.com/engineering)[Events](https://www.anthropic.com/events)[Powered by Claude](https://claude.com/partners/powered-by-claude)[Service partners](https://claude.com/partners/services)[Startups program](https://claude.com/programs/startups)Terms and policies[Privacy policy](https://www.anthropic.com/legal/privacy)[Disclosure policy](https://www.anthropic.com/responsible-disclosure-policy)[Usage policy](https://www.anthropic.com/legal/aup)[Commercial terms](https://www.anthropic.com/legal/commercial-terms)[Consumer terms](https://www.anthropic.com/legal/consumer-terms)