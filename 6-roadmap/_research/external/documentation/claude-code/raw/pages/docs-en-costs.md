---
{
  "fetch": {
    "url": "https://code.claude.com/docs/en/costs",
    "fetched_at": "2026-02-04T00:53:37.865724",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 634309
  },
  "metadata": {
    "title": "Manage costs effectively",
    "section": "costs",
    "tier": 3,
    "type": "reference"
  }
}
---

- Manage costs effectively - Claude Code Docs[Skip to main content](#content-area)[Claude Code Docs home page](/docs)EnglishSearch...⌘KAsk AI[Claude Developer Platform](https://platform.claude.com/)- [Claude Code on the Web](https://claude.ai/code)- [Claude Code on the Web](https://claude.ai/code)Search...NavigationAdministrationManage costs effectively[Getting started](/docs/en/overview)[Build with Claude Code](/docs/en/sub-agents)[Deployment](/docs/en/third-party-integrations)[Administration](/docs/en/setup)[Configuration](/docs/en/settings)[Reference](/docs/en/cli-reference)[Resources](/docs/en/legal-and-compliance)Administration- [Advanced installation](/docs/en/setup)- [Authentication](/docs/en/authentication)- [Security](/docs/en/security)- [Data usage](/docs/en/data-usage)- [Monitoring](/docs/en/monitoring-usage)- [Costs](/docs/en/costs)- [Track team usage with analytics](/docs/en/analytics)- [Create and distribute a plugin marketplace](/docs/en/plugin-marketplaces)On this page- [Track your costs](#track-your-costs)- [Using the /cost command](#using-the-%2Fcost-command)- [Managing costs for teams](#managing-costs-for-teams)- [Rate limit recommendations](#rate-limit-recommendations)- [Reduce token usage](#reduce-token-usage)- [Manage context proactively](#manage-context-proactively)- [Choose the right model](#choose-the-right-model)- [Reduce MCP server overhead](#reduce-mcp-server-overhead)- [Install code intelligence plugins for typed languages](#install-code-intelligence-plugins-for-typed-languages)- [Offload processing to hooks and skills](#offload-processing-to-hooks-and-skills)- [Move instructions from CLAUDE.md to skills](#move-instructions-from-claude-md-to-skills)- [Adjust extended thinking](#adjust-extended-thinking)- [Delegate verbose operations to subagents](#delegate-verbose-operations-to-subagents)- [Write specific prompts](#write-specific-prompts)- [Work efficiently on complex tasks](#work-efficiently-on-complex-tasks)- [Background token usage](#background-token-usage)- [Understanding changes in Claude Code behavior](#understanding-changes-in-claude-code-behavior)Administration# Manage costs effectivelyCopy pageTrack token usage, set team spend limits, and reduce Claude Code costs with context management, model selection, extended thinking settings, and preprocessing hooks.Copy pageClaude Code consumes tokens for each interaction. Costs vary based on codebase size, query complexity, and conversation length. The average cost is $6 per developer per day, with daily costs remaining below $12 for 90% of users.

For team usage, Claude Code charges by API token consumption. On average, Claude Code costs ~$100-200/developer per month with Sonnet 4.5 though there is large variance depending on how many instances users are running and whether they’re using it in automation.

This page covers how to [track your costs](#track-your-costs), [manage costs for teams](#managing-costs-for-teams), and [reduce token usage](#reduce-token-usage).

## [​](#track-your-costs)Track your costs

### [​](#using-the-/cost-command)Using the `/cost` command

The `/cost` command shows API token usage and is intended for API users. Claude Max and Pro subscribers have usage included in their subscription, so `/cost` data isn’t relevant for billing purposes. Subscribers can use `/stats` to view usage patterns.

The `/cost` command provides detailed token usage statistics for your current session:

CopyAsk AI```

Total cost:            $0.55

Total duration (API):  6m 19.7s

Total duration (wall): 6h 33m 10.2s

Total code changes:    0 lines added, 0 lines removed

```

## [​](#managing-costs-for-teams)Managing costs for teams

When using Claude API, you can [set workspace spend limits](https://platform.claude.com/docs/en/build-with-claude/workspaces#workspace-limits) on the total Claude Code workspace spend. Admins can [view cost and usage reporting](https://platform.claude.com/docs/en/build-with-claude/workspaces#usage-and-cost-tracking) in the Console.

When you first authenticate Claude Code with your Claude Console account, a workspace called “Claude Code” is automatically created for you. This workspace provides centralized cost tracking and management for all Claude Code usage in your organization. You cannot create API keys for this workspace; it is exclusively for Claude Code authentication and usage.

On Bedrock, Vertex, and Foundry, Claude Code does not send metrics from your cloud. To get cost metrics, several large enterprises reported using [LiteLLM](/docs/en/llm-gateway#litellm-configuration), which is an open-source tool that helps companies [track spend by key](https://docs.litellm.ai/docs/proxy/virtual_keys#tracking-spend). This project is unaffiliated with Anthropic and we have not audited its security.

### [​](#rate-limit-recommendations)Rate limit recommendations

When setting up Claude Code for teams, consider these Token Per Minute (TPM) and Request Per Minute (RPM) per-user recommendations based on your organization size:

Team sizeTPM per userRPM per user1-5 users200k-300k5-75-20 users100k-150k2.5-3.520-50 users50k-75k1.25-1.7550-100 users25k-35k0.62-0.87100-500 users15k-20k0.37-0.47500+ users10k-15k0.25-0.35

For example, if you have 200 users, you might request 20k TPM for each user, or 4 million total TPM (200*20,000 = 4 million).

The TPM per user decreases as team size grows because we expect fewer users to use Claude Code concurrently in larger organizations. These rate limits apply at the organization level, not per individual user, which means individual users can temporarily consume more than their calculated share when others aren’t actively using the service.

If you anticipate scenarios with unusually high concurrent usage (such as live training sessions with large groups), you may need higher TPM allocations per user.

## [​](#reduce-token-usage)Reduce token usage

Token costs scale with context size: the more context Claude processes, the more tokens you use. Claude Code automatically optimizes costs through prompt caching (which reduces costs for repeated content like system prompts) and auto-compaction (which summarizes conversation history when approaching context limits).

The following strategies help you keep context small and reduce per-message costs.

### [​](#manage-context-proactively)Manage context proactively

Use `/cost` to check your current token usage, or [configure your status line](/docs/en/statusline#context-window-usage) to display it continuously.

- **Clear between tasks**: Use `/clear` to start fresh when switching to unrelated work. Stale context wastes tokens on every subsequent message. Use `/rename` before clearing so you can easily find the session later, then `/resume` to return to it.

- **Add custom compaction instructions**: `/compact Focus on code samples and API usage` tells Claude what to preserve during summarization.

You can also customize compaction behavior in your CLAUDE.md:

CopyAsk AI```

# Compact instructions

When you are using compact, please focus on test output and code changes

```

### [​](#choose-the-right-model)Choose the right model

Sonnet handles most coding tasks well and costs less than Opus. Reserve Opus for complex architectural decisions or multi-step reasoning. Use `/model` to switch models mid-session, or set a default in `/config`. For simple subagent tasks, specify `model: haiku` in your [subagent configuration](/docs/en/sub-agents#choose-a-model).

### [​](#reduce-mcp-server-overhead)Reduce MCP server overhead

Each MCP server adds tool definitions to your context, even when idle. Run `/context` to see what’s consuming space.

- **Prefer CLI tools when available**: Tools like `gh`, `aws`, `gcloud`, and `sentry-cli` are more context-efficient than MCP servers because they don’t add persistent tool definitions. Claude can run CLI commands directly without the overhead.

- **Disable unused servers**: Run `/mcp` to see configured servers and disable any you’re not actively using.

- **Tool search is automatic**: When MCP tool descriptions exceed 10% of your context window, Claude Code automatically defers them and loads tools on-demand via [tool search](/docs/en/mcp#scale-with-mcp-tool-search). Since deferred tools only enter context when actually used, a lower threshold means fewer idle tool definitions consuming space. Set a lower threshold with `ENABLE_TOOL_SEARCH=auto:<N>` (for example, `auto:5` triggers when tools exceed 5% of your context window).

### [​](#install-code-intelligence-plugins-for-typed-languages)Install code intelligence plugins for typed languages

[Code intelligence plugins](/docs/en/discover-plugins#code-intelligence) give Claude precise symbol navigation instead of text-based search, reducing unnecessary file reads when exploring unfamiliar code. A single “go to definition” call replaces what might otherwise be a grep followed by reading multiple candidate files. Installed language servers also report type errors automatically after edits, so Claude catches mistakes without running a compiler.

### [​](#offload-processing-to-hooks-and-skills)Offload processing to hooks and skills

Custom [hooks](/docs/en/hooks) can preprocess data before Claude sees it. Instead of Claude reading a 10,000-line log file to find errors, a hook can grep for `ERROR` and return only matching lines, reducing context from tens of thousands of tokens to hundreds.

A [skill](/docs/en/skills) can give Claude domain knowledge so it doesn’t have to explore. For example, a “codebase-overview” skill could describe your project’s architecture, key directories, and naming conventions. When Claude invokes the skill, it gets this context immediately instead of spending tokens reading multiple files to understand the structure.

For example, this PreToolUse hook filters test output to show only failures:

-  settings.json-  filter-test-output.shAdd this to your [settings.json](/docs/en/settings#settings-files) to run the hook before every Bash command:CopyAsk AI```

{

"hooks": {

"PreToolUse": [

{

"matcher": "Bash",

"hooks": [

{

"type": "command",

"command": "~/.claude/hooks/filter-test-output.sh"

}

]

}

]

}

}

```The hook calls this script, which checks if the command is a test runner and modifies it to show only failures:CopyAsk AI```

#!/bin/bash

input=$(cat)

cmd=$(echo "$input" | jq -r '.tool_input.command')

# If running tests, filter to show only failures

if [[ "$cmd" =~ ^(npm test|pytest|go test) ]]; then

filtered_cmd="$cmd 2>&1 | grep -A 5 -E '(FAIL|ERROR|error:)' | head -100"

echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\",\"updatedInput\":{\"command\":\"$filtered_cmd\"}}}"

else

echo "{}"

fi

```

### [​](#move-instructions-from-claude-md-to-skills)Move instructions from CLAUDE.md to skills

Your [CLAUDE.md](/docs/en/memory) file is loaded into context at session start. If it contains detailed instructions for specific workflows (like PR reviews or database migrations), those tokens are present even when you’re doing unrelated work. [Skills](/docs/en/skills) load on-demand only when invoked, so moving specialized instructions into skills keeps your base context smaller. Aim to keep CLAUDE.md under ~500 lines by including only essentials.

### [​](#adjust-extended-thinking)Adjust extended thinking

Extended thinking is enabled by default with a budget of 31,999 tokens because it significantly improves performance on complex planning and reasoning tasks. However, thinking tokens are billed as output tokens, so for simpler tasks where deep reasoning isn’t needed, you can reduce costs by disabling it in `/config` or lowering the budget (for example, `MAX_THINKING_TOKENS=8000`).

### [​](#delegate-verbose-operations-to-subagents)Delegate verbose operations to subagents

Running tests, fetching documentation, or processing log files can consume significant context. Delegate these to [subagents](/docs/en/sub-agents#isolate-high-volume-operations) so the verbose output stays in the subagent’s context while only a summary returns to your main conversation.

### [​](#write-specific-prompts)Write specific prompts

Vague requests like “improve this codebase” trigger broad scanning. Specific requests like “add input validation to the login function in auth.ts” let Claude work efficiently with minimal file reads.

### [​](#work-efficiently-on-complex-tasks)Work efficiently on complex tasks

For longer or more complex work, these habits help avoid wasted tokens from going down the wrong path:

- **Use plan mode for complex tasks**: Press Shift+Tab to enter [plan mode](/docs/en/common-workflows#use-plan-mode-for-safe-code-analysis) before implementation. Claude explores the codebase and proposes an approach for your approval, preventing expensive re-work when the initial direction is wrong.

- **Course-correct early**: If Claude starts heading the wrong direction, press Escape to stop immediately. Use `/rewind` or double-tap Escape to restore conversation and code to a previous checkpoint.

- **Give verification targets**: Include test cases, paste screenshots, or define expected output in your prompt. When Claude can verify its own work, it catches issues before you need to request fixes.

- **Test incrementally**: Write one file, test it, then continue. This catches issues early when they’re cheap to fix.

## [​](#background-token-usage)Background token usage

Claude Code uses tokens for some background functionality even when idle:

- **Conversation summarization**: Background jobs that summarize previous conversations for the `claude --resume` feature

- **Command processing**: Some commands like `/cost` may generate requests to check status

These background processes consume a small amount of tokens (typically under $0.04 per session) even without active interaction.

## [​](#understanding-changes-in-claude-code-behavior)Understanding changes in Claude Code behavior

Claude Code regularly receives updates that may change how features work, including cost reporting. Run `claude --version` to check your current version. For specific billing questions, contact Anthropic support through your [Console account](https://platform.claude.com/login). For team deployments, start with a small pilot group to establish usage patterns before wider rollout.Was this page helpful?YesNo[Monitoring](/docs/en/monitoring-usage)[Track team usage with analytics](/docs/en/analytics)⌘I[Claude Code Docs home page](/docs)[x](https://x.com/AnthropicAI)[linkedin](https://www.linkedin.com/company/anthropicresearch)Company[Anthropic](https://www.anthropic.com/company)[Careers](https://www.anthropic.com/careers)[Economic Futures](https://www.anthropic.com/economic-futures)[Research](https://www.anthropic.com/research)[News](https://www.anthropic.com/news)[Trust center](https://trust.anthropic.com/)[Transparency](https://www.anthropic.com/transparency)Help and security[Availability](https://www.anthropic.com/supported-countries)[Status](https://status.anthropic.com/)[Support center](https://support.claude.com/)Learn[Courses](https://www.anthropic.com/learn)[MCP connectors](https://claude.com/partners/mcp)[Customer stories](https://www.claude.com/customers)[Engineering blog](https://www.anthropic.com/engineering)[Events](https://www.anthropic.com/events)[Powered by Claude](https://claude.com/partners/powered-by-claude)[Service partners](https://claude.com/partners/services)[Startups program](https://claude.com/programs/startups)Terms and policies[Privacy policy](https://www.anthropic.com/legal/privacy)[Disclosure policy](https://www.anthropic.com/responsible-disclosure-policy)[Usage policy](https://www.anthropic.com/legal/aup)[Commercial terms](https://www.anthropic.com/legal/commercial-terms)[Consumer terms](https://www.anthropic.com/legal/consumer-terms)