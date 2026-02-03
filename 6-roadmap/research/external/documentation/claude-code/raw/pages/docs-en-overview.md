---
{
  "fetch": {
    "url": "https://code.claude.com/docs/en/overview",
    "fetched_at": "2026-02-04T00:53:01.234259",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 580842
  },
  "metadata": {
    "title": "Claude Code overview",
    "section": "overview",
    "tier": 1,
    "type": "reference"
  }
}
---

- Claude Code overview - Claude Code Docs[Skip to main content](#content-area)[Claude Code Docs home page](/docs)EnglishSearch...⌘KAsk AI[Claude Developer Platform](https://platform.claude.com/)- [Claude Code on the Web](https://claude.ai/code)- [Claude Code on the Web](https://claude.ai/code)Search...NavigationGetting startedClaude Code overview[Getting started](/docs/en/overview)[Build with Claude Code](/docs/en/sub-agents)[Deployment](/docs/en/third-party-integrations)[Administration](/docs/en/setup)[Configuration](/docs/en/settings)[Reference](/docs/en/cli-reference)[Resources](/docs/en/legal-and-compliance)Getting started- [Overview](/docs/en/overview)- [Quickstart](/docs/en/quickstart)- [Changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)Core concepts- [How Claude Code works](/docs/en/how-claude-code-works)- [Extend Claude Code](/docs/en/features-overview)- [Common workflows](/docs/en/common-workflows)- [Best practices](/docs/en/best-practices)Outside of the terminal- [Claude Code on the web](/docs/en/claude-code-on-the-web)- [Claude Code on desktop](/docs/en/desktop)- [Chrome extension (beta)](/docs/en/chrome)- [Visual Studio Code](/docs/en/vs-code)- [JetBrains IDEs](/docs/en/jetbrains)- [GitHub Actions](/docs/en/github-actions)- [GitLab CI/CD](/docs/en/gitlab-ci-cd)- [Claude Code in Slack](/docs/en/slack)On this page- [Get started in 30 seconds](#get-started-in-30-seconds)- [What Claude Code does for you](#what-claude-code-does-for-you)- [Why developers love Claude Code](#why-developers-love-claude-code)- [Use Claude Code everywhere](#use-claude-code-everywhere)- [Next steps](#next-steps)- [Additional resources](#additional-resources)Getting started# Claude Code overviewCopy pageLearn about Claude Code, Anthropic’s agentic coding tool that lives in your terminal and helps you turn ideas into code faster than ever before.Copy page## [​](#get-started-in-30-seconds)Get started in 30 seconds

Prerequisites:

- A [Claude subscription](https://claude.com/pricing) (Pro, Max, Teams, or Enterprise) or [Claude Console](https://console.anthropic.com/) account

**Install Claude Code:**

To install Claude Code, use one of the following methods:

-  Native Install (Recommended)-  Homebrew-  WinGet**macOS, Linux, WSL:**CopyAsk AI```

curl -fsSL https://claude.ai/install.sh | bash

```**Windows PowerShell:**CopyAsk AI```

irm https://claude.ai/install.ps1 | iex

```**Windows CMD:**CopyAsk AI```

curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd

```Native installations automatically update in the background to keep you on the latest version.CopyAsk AI```

brew install --cask claude-code

```Homebrew installations do not auto-update. Run `brew upgrade claude-code` periodically to get the latest features and security fixes.CopyAsk AI```

winget install Anthropic.ClaudeCode

```WinGet installations do not auto-update. Run `winget upgrade Anthropic.ClaudeCode` periodically to get the latest features and security fixes.

**Start using Claude Code:**

CopyAsk AI```

cd your-project

claude

```

You’ll be prompted to log in on first use. That’s it! [Continue with Quickstart (5 minutes) →](/docs/en/quickstart)

See [advanced setup](/docs/en/setup) for installation options, manual updates, or uninstallation instructions. Visit [troubleshooting](/docs/en/troubleshooting) if you hit issues.

## [​](#what-claude-code-does-for-you)What Claude Code does for you

- **Build features from descriptions**: Tell Claude what you want to build in plain English. It will make a plan, write the code, and ensure it works.

- **Debug and fix issues**: Describe a bug or paste an error message. Claude Code will analyze your codebase, identify the problem, and implement a fix.

- **Navigate any codebase**: Ask anything about your team’s codebase, and get a thoughtful answer back. Claude Code maintains awareness of your entire project structure, can find up-to-date information from the web, and with [MCP](/docs/en/mcp) can pull from external data sources like Google Drive, Figma, and Slack.

- **Automate tedious tasks**: Fix fiddly lint issues, resolve merge conflicts, and write release notes. Do all this in a single command from your developer machines, or automatically in CI.

## [​](#why-developers-love-claude-code)Why developers love Claude Code

- **Works in your terminal**: Not another chat window. Not another IDE. Claude Code meets you where you already work, with the tools you already love.

- **Takes action**: Claude Code can directly edit files, run commands, and create commits. Need more? [MCP](/docs/en/mcp) lets Claude read your design docs in Google Drive, update your tickets in Jira, or use *your* custom developer tooling.

- **Unix philosophy**: Claude Code is composable and scriptable. `tail -f app.log | claude -p "Slack me if you see any anomalies appear in this log stream"` *works*. Your CI can run `claude -p "If there are new text strings, translate them into French and raise a PR for @lang-fr-team to review"`.

- **Enterprise-ready**: Use the Claude API, or host on AWS or GCP. Enterprise-grade [security](/docs/en/security), [privacy](/docs/en/data-usage), and [compliance](https://trust.anthropic.com/) is built-in.

## [​](#use-claude-code-everywhere)Use Claude Code everywhere

Claude Code works across your development environment: in your terminal, in your IDE, in the cloud, and in Slack.

- **[Terminal (CLI)](/docs/en/quickstart)**: the core Claude Code experience. Run `claude` in any terminal to start coding.

- **[Claude Code on the web](/docs/en/claude-code-on-the-web)**: use Claude Code from your browser at [claude.ai/code](https://claude.ai/code) or the Claude iOS app, with no local setup required. Run tasks in parallel, work on repos you don’t have locally, and review changes in a built-in diff view.

- **[Desktop app](/docs/en/desktop)**: a standalone application with diff review, parallel sessions via git worktrees, and the ability to launch cloud sessions.

- **[VS Code](/docs/en/vs-code)**: a native extension with inline diffs, @-mentions, and plan review.

- **[JetBrains IDEs](/docs/en/jetbrains)**: a plugin for IntelliJ IDEA, PyCharm, WebStorm, and other JetBrains IDEs with IDE diff viewing and context sharing.

- **[GitHub Actions](/docs/en/github-actions)**: automate code review, issue triage, and other workflows in CI/CD with `@claude` mentions.

- **[GitLab CI/CD](/docs/en/gitlab-ci-cd)**: event-driven automation for GitLab merge requests and issues.

- **[Slack](/docs/en/slack)**: mention Claude in Slack to route coding tasks to Claude Code on the web and get PRs back.

- **[Chrome](/docs/en/chrome)**: connect Claude Code to your browser for live debugging, design verification, and web app testing.

## [​](#next-steps)Next steps

[## QuickstartSee Claude Code in action with practical examples](/docs/en/quickstart)[## Common workflowsStep-by-step guides for common workflows](/docs/en/common-workflows)[## TroubleshootingSolutions for common issues with Claude Code](/docs/en/troubleshooting)[## Desktop appRun Claude Code as a standalone application](/docs/en/desktop)

## [​](#additional-resources)Additional resources

[## About Claude CodeLearn more about Claude Code on claude.com](https://claude.com/product/claude-code)[## Build with the Agent SDKCreate custom AI agents with the Claude Agent SDK](https://docs.claude.com/en/docs/agent-sdk/overview)[## Host on AWS or GCPConfigure Claude Code with Amazon Bedrock or Google Vertex AI](/docs/en/third-party-integrations)[## SettingsCustomize Claude Code for your workflow](/docs/en/settings)[## CommandsLearn about CLI commands and controls](/docs/en/cli-reference)[## Reference implementationClone our development container reference implementation](https://github.com/anthropics/claude-code/tree/main/.devcontainer)[## SecurityDiscover Claude Code’s safeguards and best practices for safe usage](/docs/en/security)[## Privacy and data usageUnderstand how Claude Code handles your data](/docs/en/data-usage)Was this page helpful?YesNo[Quickstart](/docs/en/quickstart)⌘I[Claude Code Docs home page](/docs)[x](https://x.com/AnthropicAI)[linkedin](https://www.linkedin.com/company/anthropicresearch)Company[Anthropic](https://www.anthropic.com/company)[Careers](https://www.anthropic.com/careers)[Economic Futures](https://www.anthropic.com/economic-futures)[Research](https://www.anthropic.com/research)[News](https://www.anthropic.com/news)[Trust center](https://trust.anthropic.com/)[Transparency](https://www.anthropic.com/transparency)Help and security[Availability](https://www.anthropic.com/supported-countries)[Status](https://status.anthropic.com/)[Support center](https://support.claude.com/)Learn[Courses](https://www.anthropic.com/learn)[MCP connectors](https://claude.com/partners/mcp)[Customer stories](https://www.claude.com/customers)[Engineering blog](https://www.anthropic.com/engineering)[Events](https://www.anthropic.com/events)[Powered by Claude](https://claude.com/partners/powered-by-claude)[Service partners](https://claude.com/partners/services)[Startups program](https://claude.com/programs/startups)Terms and policies[Privacy policy](https://www.anthropic.com/legal/privacy)[Disclosure policy](https://www.anthropic.com/responsible-disclosure-policy)[Usage policy](https://www.anthropic.com/legal/aup)[Commercial terms](https://www.anthropic.com/legal/commercial-terms)[Consumer terms](https://www.anthropic.com/legal/consumer-terms)