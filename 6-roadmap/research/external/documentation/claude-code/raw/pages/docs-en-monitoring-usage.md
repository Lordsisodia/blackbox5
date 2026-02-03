---
{
  "fetch": {
    "url": "https://code.claude.com/docs/en/monitoring-usage",
    "fetched_at": "2026-02-04T00:53:52.926067",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 871018
  },
  "metadata": {
    "title": "Monitoring",
    "section": "monitoring-usage",
    "tier": 3,
    "type": "reference"
  }
}
---

- Monitoring - Claude Code Docs[Skip to main content](#content-area)[Claude Code Docs home page](/docs)EnglishSearch...⌘KAsk AI[Claude Developer Platform](https://platform.claude.com/)- [Claude Code on the Web](https://claude.ai/code)- [Claude Code on the Web](https://claude.ai/code)Search...NavigationAdministrationMonitoring[Getting started](/docs/en/overview)[Build with Claude Code](/docs/en/sub-agents)[Deployment](/docs/en/third-party-integrations)[Administration](/docs/en/setup)[Configuration](/docs/en/settings)[Reference](/docs/en/cli-reference)[Resources](/docs/en/legal-and-compliance)Administration- [Advanced installation](/docs/en/setup)- [Authentication](/docs/en/authentication)- [Security](/docs/en/security)- [Data usage](/docs/en/data-usage)- [Monitoring](/docs/en/monitoring-usage)- [Costs](/docs/en/costs)- [Track team usage with analytics](/docs/en/analytics)- [Create and distribute a plugin marketplace](/docs/en/plugin-marketplaces)On this page- [Quick start](#quick-start)- [Administrator configuration](#administrator-configuration)- [Configuration details](#configuration-details)- [Common configuration variables](#common-configuration-variables)- [Metrics cardinality control](#metrics-cardinality-control)- [Dynamic headers](#dynamic-headers)- [Settings configuration](#settings-configuration)- [Script requirements](#script-requirements)- [Refresh behavior](#refresh-behavior)- [Multi-team organization support](#multi-team-organization-support)- [Example configurations](#example-configurations)- [Available metrics and events](#available-metrics-and-events)- [Standard attributes](#standard-attributes)- [Metrics](#metrics)- [Metric details](#metric-details)- [Session counter](#session-counter)- [Lines of code counter](#lines-of-code-counter)- [Pull request counter](#pull-request-counter)- [Commit counter](#commit-counter)- [Cost counter](#cost-counter)- [Token counter](#token-counter)- [Code edit tool decision counter](#code-edit-tool-decision-counter)- [Active time counter](#active-time-counter)- [Events](#events)- [User prompt event](#user-prompt-event)- [Tool result event](#tool-result-event)- [API request event](#api-request-event)- [API error event](#api-error-event)- [Tool decision event](#tool-decision-event)- [Interpreting metrics and events data](#interpreting-metrics-and-events-data)- [Usage monitoring](#usage-monitoring)- [Cost monitoring](#cost-monitoring)- [Alerting and segmentation](#alerting-and-segmentation)- [Event analysis](#event-analysis)- [Backend considerations](#backend-considerations)- [For metrics](#for-metrics)- [For events/logs](#for-events%2Flogs)- [Service information](#service-information)- [ROI measurement resources](#roi-measurement-resources)- [Security/privacy considerations](#security%2Fprivacy-considerations)- [Monitoring Claude Code on Amazon Bedrock](#monitoring-claude-code-on-amazon-bedrock)Administration# MonitoringCopy pageLearn how to enable and configure OpenTelemetry for Claude Code.Copy pageClaude Code supports OpenTelemetry (OTel) metrics and events for monitoring and observability.

All metrics are time series data exported via OpenTelemetry’s standard metrics protocol, and events are exported via OpenTelemetry’s logs/events protocol. It is the user’s responsibility to ensure their metrics and logs backends are properly configured and that the aggregation granularity meets their monitoring requirements.

## [​](#quick-start)Quick start

Configure OpenTelemetry using environment variables:

CopyAsk AI```

# 1. Enable telemetry

export CLAUDE_CODE_ENABLE_TELEMETRY=1

# 2. Choose exporters (both are optional - configure only what you need)

export OTEL_METRICS_EXPORTER=otlp       # Options: otlp, prometheus, console

export OTEL_LOGS_EXPORTER=otlp          # Options: otlp, console

# 3. Configure OTLP endpoint (for OTLP exporter)

export OTEL_EXPORTER_OTLP_PROTOCOL=grpc

export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# 4. Set authentication (if required)

export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer your-token"

# 5. For debugging: reduce export intervals

export OTEL_METRIC_EXPORT_INTERVAL=10000  # 10 seconds (default: 60000ms)

export OTEL_LOGS_EXPORT_INTERVAL=5000     # 5 seconds (default: 5000ms)

# 6. Run Claude Code

claude

```

The default export intervals are 60 seconds for metrics and 5 seconds for logs. During setup, you may want to use shorter intervals for debugging purposes. Remember to reset these for production use.

For full configuration options, see the [OpenTelemetry specification](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/exporter.md#configuration-options).

## [​](#administrator-configuration)Administrator configuration

Administrators can configure OpenTelemetry settings for all users through the [managed settings file](/docs/en/settings#settings-files). This allows for centralized control of telemetry settings across an organization. See the [settings precedence](/docs/en/settings#settings-precedence) for more information about how settings are applied.

Example managed settings configuration:

CopyAsk AI```

{

"env": {

"CLAUDE_CODE_ENABLE_TELEMETRY": "1",

"OTEL_METRICS_EXPORTER": "otlp",

"OTEL_LOGS_EXPORTER": "otlp",

"OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",

"OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector.company.com:4317",

"OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer company-token"

}

}

```

Managed settings can be distributed via MDM (Mobile Device Management) or other device management solutions. Environment variables defined in the managed settings file have high precedence and cannot be overridden by users.

## [​](#configuration-details)Configuration details

### [​](#common-configuration-variables)Common configuration variables

Environment VariableDescriptionExample Values`CLAUDE_CODE_ENABLE_TELEMETRY`Enables telemetry collection (required)`1``OTEL_METRICS_EXPORTER`Metrics exporter type(s) (comma-separated)`console`, `otlp`, `prometheus``OTEL_LOGS_EXPORTER`Logs/events exporter type(s) (comma-separated)`console`, `otlp``OTEL_EXPORTER_OTLP_PROTOCOL`Protocol for OTLP exporter (all signals)`grpc`, `http/json`, `http/protobuf``OTEL_EXPORTER_OTLP_ENDPOINT`OTLP collector endpoint (all signals)`http://localhost:4317``OTEL_EXPORTER_OTLP_METRICS_PROTOCOL`Protocol for metrics (overrides general)`grpc`, `http/json`, `http/protobuf``OTEL_EXPORTER_OTLP_METRICS_ENDPOINT`OTLP metrics endpoint (overrides general)`http://localhost:4318/v1/metrics``OTEL_EXPORTER_OTLP_LOGS_PROTOCOL`Protocol for logs (overrides general)`grpc`, `http/json`, `http/protobuf``OTEL_EXPORTER_OTLP_LOGS_ENDPOINT`OTLP logs endpoint (overrides general)`http://localhost:4318/v1/logs``OTEL_EXPORTER_OTLP_HEADERS`Authentication headers for OTLP`Authorization=Bearer token``OTEL_EXPORTER_OTLP_METRICS_CLIENT_KEY`Client key for mTLS authenticationPath to client key file`OTEL_EXPORTER_OTLP_METRICS_CLIENT_CERTIFICATE`Client certificate for mTLS authenticationPath to client cert file`OTEL_METRIC_EXPORT_INTERVAL`Export interval in milliseconds (default: 60000)`5000`, `60000``OTEL_LOGS_EXPORT_INTERVAL`Logs export interval in milliseconds (default: 5000)`1000`, `10000``OTEL_LOG_USER_PROMPTS`Enable logging of user prompt content (default: disabled)`1` to enable`OTEL_LOG_TOOL_DETAILS`Enable logging of MCP server/tool names and skill names in tool events (default: disabled)`1` to enable`CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`Interval for refreshing dynamic headers (default: 1740000ms / 29 minutes)`900000`

### [​](#metrics-cardinality-control)Metrics cardinality control

The following environment variables control which attributes are included in metrics to manage cardinality:

Environment VariableDescriptionDefault ValueExample to Disable`OTEL_METRICS_INCLUDE_SESSION_ID`Include session.id attribute in metrics`true``false``OTEL_METRICS_INCLUDE_VERSION`Include app.version attribute in metrics`false``true``OTEL_METRICS_INCLUDE_ACCOUNT_UUID`Include user.account_uuid attribute in metrics`true``false`

These variables help control the cardinality of metrics, which affects storage requirements and query performance in your metrics backend. Lower cardinality generally means better performance and lower storage costs but less granular data for analysis.

### [​](#dynamic-headers)Dynamic headers

For enterprise environments that require dynamic authentication, you can configure a script to generate headers dynamically:

#### [​](#settings-configuration)Settings configuration

Add to your `.claude/settings.json`:

CopyAsk AI```

{

"otelHeadersHelper": "/bin/generate_opentelemetry_headers.sh"

}

```

#### [​](#script-requirements)Script requirements

The script must output valid JSON with string key-value pairs representing HTTP headers:

CopyAsk AI```

#!/bin/bash

# Example: Multiple headers

echo "{\"Authorization\": \"Bearer $(get-token.sh)\", \"X-API-Key\": \"$(get-api-key.sh)\"}"

```

#### [​](#refresh-behavior)Refresh behavior

The headers helper script runs at startup and periodically thereafter to support token refresh. By default, the script runs every 29 minutes. Customize the interval with the `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS` environment variable.

### [​](#multi-team-organization-support)Multi-team organization support

Organizations with multiple teams or departments can add custom attributes to distinguish between different groups using the `OTEL_RESOURCE_ATTRIBUTES` environment variable:

CopyAsk AI```

# Add custom attributes for team identification

export OTEL_RESOURCE_ATTRIBUTES="department=engineering,team.id=platform,cost_center=eng-123"

```

These custom attributes will be included in all metrics and events, allowing you to:

- Filter metrics by team or department

- Track costs per cost center

- Create team-specific dashboards

- Set up alerts for specific teams

**Important formatting requirements for OTEL_RESOURCE_ATTRIBUTES:**The `OTEL_RESOURCE_ATTRIBUTES` environment variable follows the [W3C Baggage specification](https://www.w3.org/TR/baggage/), which has strict formatting requirements:

- **No spaces allowed**: Values cannot contain spaces. For example, `user.organizationName=My Company` is invalid

- **Format**: Must be comma-separated key=value pairs: `key1=value1,key2=value2`

- **Allowed characters**: Only US-ASCII characters excluding control characters, whitespace, double quotes, commas, semicolons, and backslashes

- **Special characters**: Characters outside the allowed range must be percent-encoded

**Examples:**CopyAsk AI```

# ❌ Invalid - contains spaces

export OTEL_RESOURCE_ATTRIBUTES="org.name=John's Organization"

# ✅ Valid - use underscores or camelCase instead

export OTEL_RESOURCE_ATTRIBUTES="org.name=Johns_Organization"

export OTEL_RESOURCE_ATTRIBUTES="org.name=JohnsOrganization"

# ✅ Valid - percent-encode special characters if needed

export OTEL_RESOURCE_ATTRIBUTES="org.name=John%27s%20Organization"

```Note: wrapping values in quotes doesn’t escape spaces. For example, `org.name="My Company"` results in the literal value `"My Company"` (with quotes included), not `My Company`.

### [​](#example-configurations)Example configurations

CopyAsk AI```

# Console debugging (1-second intervals)

export CLAUDE_CODE_ENABLE_TELEMETRY=1

export OTEL_METRICS_EXPORTER=console

export OTEL_METRIC_EXPORT_INTERVAL=1000

# OTLP/gRPC

export CLAUDE_CODE_ENABLE_TELEMETRY=1

export OTEL_METRICS_EXPORTER=otlp

export OTEL_EXPORTER_OTLP_PROTOCOL=grpc

export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Prometheus

export CLAUDE_CODE_ENABLE_TELEMETRY=1

export OTEL_METRICS_EXPORTER=prometheus

# Multiple exporters

export CLAUDE_CODE_ENABLE_TELEMETRY=1

export OTEL_METRICS_EXPORTER=console,otlp

export OTEL_EXPORTER_OTLP_PROTOCOL=http/json

# Different endpoints/backends for metrics and logs

export CLAUDE_CODE_ENABLE_TELEMETRY=1

export OTEL_METRICS_EXPORTER=otlp

export OTEL_LOGS_EXPORTER=otlp

export OTEL_EXPORTER_OTLP_METRICS_PROTOCOL=http/protobuf

export OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://metrics.company.com:4318

export OTEL_EXPORTER_OTLP_LOGS_PROTOCOL=grpc

export OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=http://logs.company.com:4317

# Metrics only (no events/logs)

export CLAUDE_CODE_ENABLE_TELEMETRY=1

export OTEL_METRICS_EXPORTER=otlp

export OTEL_EXPORTER_OTLP_PROTOCOL=grpc

export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Events/logs only (no metrics)

export CLAUDE_CODE_ENABLE_TELEMETRY=1

export OTEL_LOGS_EXPORTER=otlp

export OTEL_EXPORTER_OTLP_PROTOCOL=grpc

export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

```

## [​](#available-metrics-and-events)Available metrics and events

### [​](#standard-attributes)Standard attributes

All metrics and events share these standard attributes:

AttributeDescriptionControlled By`session.id`Unique session identifier`OTEL_METRICS_INCLUDE_SESSION_ID` (default: true)`app.version`Current Claude Code version`OTEL_METRICS_INCLUDE_VERSION` (default: false)`organization.id`Organization UUID (when authenticated)Always included when available`user.account_uuid`Account UUID (when authenticated)`OTEL_METRICS_INCLUDE_ACCOUNT_UUID` (default: true)`terminal.type`Terminal type (for example, `iTerm.app`, `vscode`, `cursor`, `tmux`)Always included when detected

### [​](#metrics)Metrics

Claude Code exports the following metrics:

Metric NameDescriptionUnit`claude_code.session.count`Count of CLI sessions startedcount`claude_code.lines_of_code.count`Count of lines of code modifiedcount`claude_code.pull_request.count`Number of pull requests createdcount`claude_code.commit.count`Number of git commits createdcount`claude_code.cost.usage`Cost of the Claude Code sessionUSD`claude_code.token.usage`Number of tokens usedtokens`claude_code.code_edit_tool.decision`Count of code editing tool permission decisionscount`claude_code.active_time.total`Total active time in secondss

### [​](#metric-details)Metric details

#### [​](#session-counter)Session counter

Incremented at the start of each session.

**Attributes**:

- All [standard attributes](#standard-attributes)

#### [​](#lines-of-code-counter)Lines of code counter

Incremented when code is added or removed.

**Attributes**:

- All [standard attributes](#standard-attributes)

- `type`: (`"added"`, `"removed"`)

#### [​](#pull-request-counter)Pull request counter

Incremented when creating pull requests via Claude Code.

**Attributes**:

- All [standard attributes](#standard-attributes)

#### [​](#commit-counter)Commit counter

Incremented when creating git commits via Claude Code.

**Attributes**:

- All [standard attributes](#standard-attributes)

#### [​](#cost-counter)Cost counter

Incremented after each API request.

**Attributes**:

- All [standard attributes](#standard-attributes)

- `model`: Model identifier (for example, “claude-sonnet-4-5-20250929”)

#### [​](#token-counter)Token counter

Incremented after each API request.

**Attributes**:

- All [standard attributes](#standard-attributes)

- `type`: (`"input"`, `"output"`, `"cacheRead"`, `"cacheCreation"`)

- `model`: Model identifier (for example, “claude-sonnet-4-5-20250929”)

#### [​](#code-edit-tool-decision-counter)Code edit tool decision counter

Incremented when user accepts or rejects Edit, Write, or NotebookEdit tool usage.

**Attributes**:

- All [standard attributes](#standard-attributes)

- `tool`: Tool name (`"Edit"`, `"Write"`, `"NotebookEdit"`)

- `decision`: User decision (`"accept"`, `"reject"`)

- `language`: Programming language of the edited file (for example, `"TypeScript"`, `"Python"`, `"JavaScript"`, `"Markdown"`). Returns `"unknown"` for unrecognized file extensions.

#### [​](#active-time-counter)Active time counter

Tracks actual time spent actively using Claude Code (not idle time). This metric is incremented during user interactions such as typing prompts or receiving responses.

**Attributes**:

- All [standard attributes](#standard-attributes)

### [​](#events)Events

Claude Code exports the following events via OpenTelemetry logs/events (when `OTEL_LOGS_EXPORTER` is configured):

#### [​](#user-prompt-event)User prompt event

Logged when a user submits a prompt.

**Event Name**: `claude_code.user_prompt`

**Attributes**:

- All [standard attributes](#standard-attributes)

- `event.name`: `"user_prompt"`

- `event.timestamp`: ISO 8601 timestamp

- `event.sequence`: monotonically increasing counter for ordering events within a session

- `prompt_length`: Length of the prompt

- `prompt`: Prompt content (redacted by default, enable with `OTEL_LOG_USER_PROMPTS=1`)

#### [​](#tool-result-event)Tool result event

Logged when a tool completes execution.

**Event Name**: `claude_code.tool_result`

**Attributes**:

- All [standard attributes](#standard-attributes)

- `event.name`: `"tool_result"`

- `event.timestamp`: ISO 8601 timestamp

- `event.sequence`: monotonically increasing counter for ordering events within a session

- `tool_name`: Name of the tool

- `success`: `"true"` or `"false"`

- `duration_ms`: Execution time in milliseconds

- `error`: Error message (if failed)

- `decision`: Either `"accept"` or `"reject"`

- `source`: Decision source - `"config"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"`, or `"user_reject"`

- `tool_parameters`: JSON string containing tool-specific parameters (when available)

For Bash tool: includes `bash_command`, `full_command`, `timeout`, `description`, `sandbox`

- For MCP tools (when `OTEL_LOG_TOOL_DETAILS=1`): includes `mcp_server_name`, `mcp_tool_name`

- For Skill tool (when `OTEL_LOG_TOOL_DETAILS=1`): includes `skill_name`

#### [​](#api-request-event)API request event

Logged for each API request to Claude.

**Event Name**: `claude_code.api_request`

**Attributes**:

- All [standard attributes](#standard-attributes)

- `event.name`: `"api_request"`

- `event.timestamp`: ISO 8601 timestamp

- `event.sequence`: monotonically increasing counter for ordering events within a session

- `model`: Model used (for example, “claude-sonnet-4-5-20250929”)

- `cost_usd`: Estimated cost in USD

- `duration_ms`: Request duration in milliseconds

- `input_tokens`: Number of input tokens

- `output_tokens`: Number of output tokens

- `cache_read_tokens`: Number of tokens read from cache

- `cache_creation_tokens`: Number of tokens used for cache creation

#### [​](#api-error-event)API error event

Logged when an API request to Claude fails.

**Event Name**: `claude_code.api_error`

**Attributes**:

- All [standard attributes](#standard-attributes)

- `event.name`: `"api_error"`

- `event.timestamp`: ISO 8601 timestamp

- `event.sequence`: monotonically increasing counter for ordering events within a session

- `model`: Model used (for example, “claude-sonnet-4-5-20250929”)

- `error`: Error message

- `status_code`: HTTP status code (if applicable)

- `duration_ms`: Request duration in milliseconds

- `attempt`: Attempt number (for retried requests)

#### [​](#tool-decision-event)Tool decision event

Logged when a tool permission decision is made (accept/reject).

**Event Name**: `claude_code.tool_decision`

**Attributes**:

- All [standard attributes](#standard-attributes)

- `event.name`: `"tool_decision"`

- `event.timestamp`: ISO 8601 timestamp

- `event.sequence`: monotonically increasing counter for ordering events within a session

- `tool_name`: Name of the tool (for example, “Read”, “Edit”, “Write”, “NotebookEdit”)

- `decision`: Either `"accept"` or `"reject"`

- `source`: Decision source - `"config"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"`, or `"user_reject"`

## [​](#interpreting-metrics-and-events-data)Interpreting metrics and events data

The metrics exported by Claude Code provide valuable insights into usage patterns and productivity. Here are some common visualizations and analyses you can create:

### [​](#usage-monitoring)Usage monitoring

MetricAnalysis Opportunity`claude_code.token.usage`Break down by `type` (input/output), user, team, or model`claude_code.session.count`Track adoption and engagement over time`claude_code.lines_of_code.count`Measure productivity by tracking code additions/removals`claude_code.commit.count` & `claude_code.pull_request.count`Understand impact on development workflows

### [​](#cost-monitoring)Cost monitoring

The `claude_code.cost.usage` metric helps with:

- Tracking usage trends across teams or individuals

- Identifying high-usage sessions for optimization

Cost metrics are approximations. For official billing data, refer to your API provider (Claude Console, AWS Bedrock, or Google Cloud Vertex).

### [​](#alerting-and-segmentation)Alerting and segmentation

Common alerts to consider:

- Cost spikes

- Unusual token consumption

- High session volume from specific users

All metrics can be segmented by `user.account_uuid`, `organization.id`, `session.id`, `model`, and `app.version`.

### [​](#event-analysis)Event analysis

The event data provides detailed insights into Claude Code interactions:

**Tool Usage Patterns**: analyze tool result events to identify:

- Most frequently used tools

- Tool success rates

- Average tool execution times

- Error patterns by tool type

**Performance Monitoring**: track API request durations and tool execution times to identify performance bottlenecks.

## [​](#backend-considerations)Backend considerations

Your choice of metrics and logs backends determines the types of analyses you can perform:

### [​](#for-metrics)For metrics

- **Time series databases (for example, Prometheus)**: Rate calculations, aggregated metrics

- **Columnar stores (for example, ClickHouse)**: Complex queries, unique user analysis

- **Full-featured observability platforms (for example, Honeycomb, Datadog)**: Advanced querying, visualization, alerting

### [​](#for-events/logs)For events/logs

- **Log aggregation systems (for example, Elasticsearch, Loki)**: Full-text search, log analysis

- **Columnar stores (for example, ClickHouse)**: Structured event analysis

- **Full-featured observability platforms (for example, Honeycomb, Datadog)**: Correlation between metrics and events

For organizations requiring Daily/Weekly/Monthly Active User (DAU/WAU/MAU) metrics, consider backends that support efficient unique value queries.

## [​](#service-information)Service information

All metrics and events are exported with the following resource attributes:

- `service.name`: `claude-code`

- `service.version`: Current Claude Code version

- `os.type`: Operating system type (for example, `linux`, `darwin`, `windows`)

- `os.version`: Operating system version string

- `host.arch`: Host architecture (for example, `amd64`, `arm64`)

- `wsl.version`: WSL version number (only present when running on Windows Subsystem for Linux)

- Meter Name: `com.anthropic.claude_code`

## [​](#roi-measurement-resources)ROI measurement resources

For a comprehensive guide on measuring return on investment for Claude Code, including telemetry setup, cost analysis, productivity metrics, and automated reporting, see the [Claude Code ROI Measurement Guide](https://github.com/anthropics/claude-code-monitoring-guide). This repository provides ready-to-use Docker Compose configurations, Prometheus and OpenTelemetry setups, and templates for generating productivity reports integrated with tools like Linear.

## [​](#security/privacy-considerations)Security/privacy considerations

- Telemetry is opt-in and requires explicit configuration

- Sensitive information like API keys or file contents are never included in metrics or events

- User prompt content is redacted by default, only prompt length is recorded. To enable user prompt logging, set `OTEL_LOG_USER_PROMPTS=1`

- MCP server/tool names and skill names are not logged by default because they can reveal user-specific configurations. To enable, set `OTEL_LOG_TOOL_DETAILS=1`

## [​](#monitoring-claude-code-on-amazon-bedrock)Monitoring Claude Code on Amazon Bedrock

For detailed Claude Code usage monitoring guidance for Amazon Bedrock, see [Claude Code Monitoring Implementation (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md).Was this page helpful?YesNo[Data usage](/docs/en/data-usage)[Costs](/docs/en/costs)⌘I[Claude Code Docs home page](/docs)[x](https://x.com/AnthropicAI)[linkedin](https://www.linkedin.com/company/anthropicresearch)Company[Anthropic](https://www.anthropic.com/company)[Careers](https://www.anthropic.com/careers)[Economic Futures](https://www.anthropic.com/economic-futures)[Research](https://www.anthropic.com/research)[News](https://www.anthropic.com/news)[Trust center](https://trust.anthropic.com/)[Transparency](https://www.anthropic.com/transparency)Help and security[Availability](https://www.anthropic.com/supported-countries)[Status](https://status.anthropic.com/)[Support center](https://support.claude.com/)Learn[Courses](https://www.anthropic.com/learn)[MCP connectors](https://claude.com/partners/mcp)[Customer stories](https://www.claude.com/customers)[Engineering blog](https://www.anthropic.com/engineering)[Events](https://www.anthropic.com/events)[Powered by Claude](https://claude.com/partners/powered-by-claude)[Service partners](https://claude.com/partners/services)[Startups program](https://claude.com/programs/startups)Terms and policies[Privacy policy](https://www.anthropic.com/legal/privacy)[Disclosure policy](https://www.anthropic.com/responsible-disclosure-policy)[Usage policy](https://www.anthropic.com/legal/aup)[Commercial terms](https://www.anthropic.com/legal/commercial-terms)[Consumer terms](https://www.anthropic.com/legal/consumer-terms)