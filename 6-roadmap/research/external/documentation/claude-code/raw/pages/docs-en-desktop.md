---
{
  "fetch": {
    "url": "https://code.claude.com/docs/en/desktop",
    "fetched_at": "2026-02-04T00:53:08.095265",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 635574
  },
  "metadata": {
    "title": "Claude Code on desktop",
    "section": "desktop",
    "tier": 2,
    "type": "reference"
  }
}
---

- Claude Code on desktop - Claude Code Docs[Skip to main content](#content-area)[Claude Code Docs home page](/docs)EnglishSearch...⌘KAsk AI[Claude Developer Platform](https://platform.claude.com/)- [Claude Code on the Web](https://claude.ai/code)- [Claude Code on the Web](https://claude.ai/code)Search...NavigationOutside of the terminalClaude Code on desktop[Getting started](/docs/en/overview)[Build with Claude Code](/docs/en/sub-agents)[Deployment](/docs/en/third-party-integrations)[Administration](/docs/en/setup)[Configuration](/docs/en/settings)[Reference](/docs/en/cli-reference)[Resources](/docs/en/legal-and-compliance)Getting started- [Overview](/docs/en/overview)- [Quickstart](/docs/en/quickstart)- [Changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)Core concepts- [How Claude Code works](/docs/en/how-claude-code-works)- [Extend Claude Code](/docs/en/features-overview)- [Common workflows](/docs/en/common-workflows)- [Best practices](/docs/en/best-practices)Outside of the terminal- [Claude Code on the web](/docs/en/claude-code-on-the-web)- [Claude Code on desktop](/docs/en/desktop)- [Chrome extension (beta)](/docs/en/chrome)- [Visual Studio Code](/docs/en/vs-code)- [JetBrains IDEs](/docs/en/jetbrains)- [GitHub Actions](/docs/en/github-actions)- [GitLab CI/CD](/docs/en/gitlab-ci-cd)- [Claude Code in Slack](/docs/en/slack)On this page- [Installation and setup](#installation-and-setup)- [Getting started](#getting-started)- [What you can do](#what-you-can-do)- [Choose a permission mode](#choose-a-permission-mode)- [Work in parallel with sessions](#work-in-parallel-with-sessions)- [Run long-running tasks remotely](#run-long-running-tasks-remotely)- [Review changes with diff view](#review-changes-with-diff-view)- [Extend Claude Code](#extend-claude-code)- [Connect external tools](#connect-external-tools)- [Create custom skills](#create-custom-skills)- [Automate workflows with hooks](#automate-workflows-with-hooks)- [Environment configuration](#environment-configuration)- [How Desktop relates to CLI](#how-desktop-relates-to-cli)- [CLI flag equivalents](#cli-flag-equivalents)- [Shared configuration](#shared-configuration)- [What’s different](#what%E2%80%99s-different)- [Troubleshooting](#troubleshooting)- [Check your version](#check-your-version)- [”Branch doesn’t exist yet” when opening in CLI](#%E2%80%9Dbranch-doesn%E2%80%99t-exist-yet%E2%80%9D-when-opening-in-cli)- [“Failed to load session” error](#%E2%80%9Cfailed-to-load-session%E2%80%9D-error)- [App won’t quit](#app-won%E2%80%99t-quit)- [Windows installation issues](#windows-installation-issues)- [Session not finding installed tools](#session-not-finding-installed-tools)- [MCP servers not working (Windows)](#mcp-servers-not-working-windows)- [Git LFS errors](#git-lfs-errors)- [Enterprise configuration](#enterprise-configuration)- [Related resources](#related-resources)Outside of the terminal# Claude Code on desktopCopy pageRun Claude Code tasks locally or on secure cloud infrastructure with the Claude desktop appCopy pageClaude Code on desktop is currently in preview.

Claude Code is an AI coding assistant that works directly with your codebase. Unlike Claude.ai chat, it can read your project files, edit code, run terminal commands, and understand how different parts of your code connect. You watch changes happen in real time.

You can use Claude Code through the terminal ([CLI](/docs/en/quickstart)) or through the desktop app described here. Both provide the same core capabilities. The desktop app adds a graphical interface and visual session management.

[## New to Claude Code?Start here to install and make your first edit](#installation-and-setup)[## Coming from the CLI?See what’s shared and what’s different](#how-desktop-relates-to-cli)

The desktop app has three tabs:

- **Chat**: A conversational interface for general questions and tasks (like Claude.ai)

- **Cowork**: An autonomous agent that works on tasks in the background

- **Code**: An AI coding assistant that reads and edits your project files directly

This documentation covers the **Code** tab. For the chat interface, see the [Claude Desktop support articles](https://support.claude.com/en/collections/16163169-claude-desktop).

## [​](#installation-and-setup)Installation and setup

1[](#)Download the appDownload Claude for your platform. You’ll need an Anthropic account ([sign up at claude.ai](https://claude.ai) if you don’t have one).[## macOSUniversal build for Intel and Apple Silicon](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code&utm_medium=docs)[## WindowsFor x64 processors](https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code&utm_medium=docs)For Windows ARM64, [download here](https://claude.ai/api/desktop/win32/arm64/exe/latest/redirect?utm_source=claude_code&utm_medium=docs). Local sessions are not available on ARM64 devices, so use remote sessions instead.Linux is not currently supported.2[](#)Open the app and sign inLaunch Claude from your Applications folder (macOS) or Start menu (Windows). Sign in with your Anthropic account.3[](#)Select the Code tabClick the **Code** tab in the top left. If clicking Code prompts you to sign in online, complete the sign-in and restart the app.

## [​](#getting-started)Getting started

If you already use the CLI, you can skip to [How Desktop relates to CLI](#how-desktop-relates-to-cli) for a quick overview of differences.

1[](#)Choose a folder and environmentSelect **Local** to run Claude on your machine using your files directly. This is the best choice for getting started. Click **Select folder** and choose your project directory.You can also run [remote sessions](/docs/en/claude-code-on-the-web) that continue in the cloud even if you close the app.2[](#)Start a sessionType what you want Claude to do:

- “Find a TODO comment and fix it”

- “Add tests for the main function”

- “Create a CLAUDE.md with instructions for this codebase”

A **session** is a conversation with Claude about your code. Each session tracks its own context and changes, so you can work on multiple tasks without them interfering with each other.3[](#)Review and accept changesBy default, Code is in **Ask** mode, where Claude proposes changes and waits for your approval before applying them. You’ll see:

- **A diff view** showing exactly what will change in each file

- **Accept/Reject buttons** to approve or decline each change

- **Real-time updates** as Claude works through your request

If you reject a change, Claude will ask how you’d like to proceed differently. Your files aren’t modified until you accept.

The sections below cover commands, permission modes, parallel sessions, and ways to extend Claude Code with custom workflows and integrations.

## [​](#what-you-can-do)What you can do

Claude Code can edit files, run terminal commands, and understand how your code connects. Try prompts like:

- `Fix the bug in the login function`

- `Run the tests and fix any failures`

- `How does the authentication flow work?`

You can rename, resume, and archive sessions through the sidebar.

### [​](#choose-a-permission-mode)Choose a permission mode

Control how Claude works using the mode selector next to the send button:

- **Ask** (recommended for new users): Claude asks for your approval before each file edit or command. You see a diff view and can accept or reject each change.

- **Code**: Claude auto-accepts file edits but still asks before running terminal commands. Use this when you trust file changes and want faster iteration.

- **Plan**: Claude creates a detailed plan for your approval before making any changes. Good for complex tasks where you want to review the approach first.

To stop Claude mid-task, click the stop button.

Remote sessions only support **Code** and **Plan** modes because they continue running in the background without requiring your active participation. See [permission modes](/docs/en/permissions#permission-modes) for details on how these work internally.

### [​](#work-in-parallel-with-sessions)Work in parallel with sessions

Click **+ New session** in the sidebar to work on multiple tasks in parallel. For Git repositories, each session gets its own isolated copy of your project using worktrees, so changes in one session don’t affect another until you commit them. Worktrees are stored in `~/.claude-worktrees/` by default.

Session isolation requires [Git](https://git-scm.com/downloads). Without Git, sessions in the same directory edit the same files, so changes in one session are immediately visible in others.

To include files listed in your `.gitignore` (like `.env`) in new worktrees, create a `.worktreeinclude` file in your project root listing the file patterns to copy.

To manage a session, click its dropdown in the sidebar to rename it, archive it, or check context usage. When context fills up, Claude automatically summarizes the conversation. You can also ask Claude to compact if you want to free up space earlier.

### [​](#run-long-running-tasks-remotely)Run long-running tasks remotely

For large refactors, test suites, migrations, or other long-running tasks, select **Remote** instead of **Local** when starting a session. Remote sessions run on Anthropic’s cloud infrastructure and continue even if you close the app or shut down your computer. Check back anytime to see progress or steer Claude in a different direction.

Remote sessions support **Code** and **Plan** modes. See [Claude Code on the web](/docs/en/claude-code-on-the-web) for details on configuring remote environments.

### [​](#review-changes-with-diff-view)Review changes with diff view

After Claude makes changes to your code, the diff view lets you review modifications file by file before creating a pull request.

When Claude changes files, a diff stats indicator appears showing the number of lines added and removed (for example, `+12 -1`). Click this indicator to open the diff viewer, which displays a file list on the left and the changes for each file on the right.

To comment on specific lines, click any line in the diff to open a comment box. Type your feedback and press **Enter** to send. In the full diff view, press **Enter** to accept each comment, then **Cmd+Enter** to send them all. Claude reads your comments and makes the requested changes, which appear as a new diff you can review.

## [​](#extend-claude-code)Extend Claude Code

You can extend Claude Code with custom commands, automated workflows, and external integrations.

### [​](#connect-external-tools)Connect external tools

For local sessions, click the **…** button before starting and select **Connectors** to add integrations like Google Calendar, Slack, GitHub, Linear, Notion, and more. Connectors must be configured before the session starts and are only available for local sessions. Once connected, Claude can read your calendar, send messages, create issues, and interact with your tools directly. You can ask Claude what connectors are configured in your session.

Connectors are [MCP (Model Context Protocol) servers](/docs/en/mcp) with built-in setup. You can also [create custom connectors](https://support.claude.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp) or add MCP servers manually via [configuration files](/docs/en/mcp#configure-mcp-servers).

### [​](#create-custom-skills)Create custom skills

[Skills](/docs/en/skills) are reusable prompts that extend Claude’s capabilities. For example, you could create a `review` skill that runs your standard code review checklist, or a `deploy` skill that walks through your deployment steps. Skills are defined as markdown files in `.claude/skills/` and can include instructions, context, and even call other tools. Ask Claude what skills are available or to run a specific skill. Claude can also help you create a skill if you describe what you want, or see [skills](/docs/en/skills) to learn how to write them yourself.

### [​](#automate-workflows-with-hooks)Automate workflows with hooks

[Hooks](/docs/en/hooks) run shell commands automatically in response to Claude Code events. For example, you could run a linter after every file edit, auto-format code, or send notifications when tasks complete. Hooks are configured in your [settings files](/docs/en/settings). See [hooks](/docs/en/hooks) for available events and configuration examples.

## [​](#environment-configuration)Environment configuration

When starting a session, you choose between **Local** (runs on your machine) or **Remote** (runs on Anthropic’s cloud).

**Local sessions** inherit environment variables from your shell. If you need additional variables, set them in your shell profile (`~/.zshrc`, `~/.bashrc`) and restart the desktop app. See [environment variables](/docs/en/settings#environment-variables) for the full list of supported variables.

[Extended thinking](/docs/en/common-workflows#use-extended-thinking-thinking-mode) is enabled by default, which improves performance on complex reasoning tasks but uses additional tokens. The thinking process runs in the background but isn’t displayed in the Desktop interface. To disable it or adjust the budget, set `MAX_THINKING_TOKENS` in your shell profile (use `0` to disable).

**Remote sessions** run on Anthropic’s cloud infrastructure and continue even if you close the app. Usage counts toward your subscription plan limits with no separate compute charges. See [Claude Code on the web](/docs/en/claude-code-on-the-web) for details on configuring remote environments.

## [​](#how-desktop-relates-to-cli)How Desktop relates to CLI

If you already use the Claude Code CLI, Desktop runs the same underlying engine with a graphical interface. You can run both simultaneously on the same machine, even on the same project. Each maintains separate session history, but they share configuration and project memory (CLAUDE.md files).

### [​](#cli-flag-equivalents)CLI flag equivalents

If you’re used to CLI flags, the table below shows the Desktop equivalent for each. Some flags have no Desktop equivalent because they’re designed for scripting or automation.

CLIDesktop equivalent`--model sonnet`**…** menu > Model (before starting session)`--resume`, `--continue`Click a session in the sidebar`--allowedTools`, `--disallowedTools`Not available in Desktop`--dangerously-skip-permissions`Not available in Desktop`--print`Not available (Desktop is interactive)

### [​](#shared-configuration)Shared configuration

Desktop and CLI read the same configuration files, so your setup carries over:

- **[CLAUDE.md](/docs/en/memory)** and **CLAUDE.local.md** files in your project are used by both

- **[MCP servers](/docs/en/mcp)** configured in `~/.claude.json` or `.mcp.json` work in both

- **[Hooks](/docs/en/hooks)** and **[skills](/docs/en/skills)** defined in settings apply to both

- **[Settings](/docs/en/settings)** in `~/.claude.json` and `~/.claude/settings.json` are shared

- **Models** (Sonnet, Opus, Haiku) are available in both (Desktop requires selecting before starting a session)

MCP servers configured for the **Claude Desktop chat app** (in `claude_desktop_config.json`) are separate from Claude Code. To use MCP servers in Claude Code, configure them in `~/.claude.json` or your project’s `.mcp.json` file. See [MCP configuration](/docs/en/mcp#configure-mcp-servers) for details.

### [​](#what’s-different)What’s different

**Desktop adds:**

- Graphical interface with visual session management

- Built-in connectors for common integrations

- Automatic session isolation for Git repositories (each session gets its own worktree)

**CLI adds:**

- [Third-party API providers](/docs/en/third-party-integrations) (Bedrock, Vertex, Foundry). If you use these, continue using CLI for those projects.

- [CLI flags](/docs/en/cli-reference) for scripting (`--print`, `--resume`, `--continue`)

- [Programmatic usage](/docs/en/headless) via the Agent SDK

## [​](#troubleshooting)Troubleshooting

Solutions to common issues with the Claude desktop app. For CLI issues, see [CLI troubleshooting](/docs/en/troubleshooting).

### [​](#check-your-version)Check your version

To see which version of the desktop app you’re running:

- **macOS**: Click **Claude** in the menu bar, then **About Claude**

- **Windows**: Click **Help**, then **About**

Click the version number to copy it to your clipboard.

### [​](#”branch-doesn’t-exist-yet”-when-opening-in-cli)”Branch doesn’t exist yet” when opening in CLI

Remote sessions can create branches that don’t exist on your local machine. Click the branch name in the session toolbar to copy it, then fetch it locally:

CopyAsk AI```

git fetch origin <branch-name>

git checkout <branch-name>

```

### [​](#“failed-to-load-session”-error)“Failed to load session” error

This error can occur for several reasons:

- The selected folder no longer exists or is inaccessible

- A Git repository requires Git LFS but it’s not installed (see [Git LFS errors](#git-lfs-errors))

- File permissions prevent access to the project directory

Try selecting a different folder or restarting the desktop app.

### [​](#app-won’t-quit)App won’t quit

If the desktop app doesn’t close properly:

- **macOS**: Press Cmd+Q. If the app doesn’t respond, use Force Quit (Cmd+Option+Esc, select Claude, click Force Quit).

- **Windows**: Use Task Manager (Ctrl+Shift+Esc) to end the Claude process.

### [​](#windows-installation-issues)Windows installation issues

If the installer fails silently or doesn’t complete properly:

- **PATH not updated**: After installation, open a new terminal window. The PATH updates only apply to new terminal sessions.

- **Concurrent installation error**: If you see an error about another installation in progress but there isn’t one, try running the installer as Administrator.

### [​](#session-not-finding-installed-tools)Session not finding installed tools

If Claude can’t find tools like `npm`, `node`, or other CLI commands:

- Verify the tools work in your regular terminal

- Check that your shell profile (`~/.zshrc`, `~/.bashrc`) properly sets up PATH

- Restart the desktop app to reload environment variables

### [​](#mcp-servers-not-working-windows)MCP servers not working (Windows)

If MCP server toggles don’t respond or servers fail to connect on Windows:

- Check that the MCP server is properly configured in your settings

- Restart the desktop app after making changes

- Verify the MCP server process is running (check Task Manager)

- Review the server logs for connection errors

### [​](#git-lfs-errors)Git LFS errors

If you see “Git LFS is required by this repository but is not installed,” your repository uses Git Large File Storage for large binary files. Install Git LFS before opening this repository:

- Install Git LFS from [git-lfs.com](https://git-lfs.com/)

- Run `git lfs install` in your terminal

- Restart the desktop app

## [​](#enterprise-configuration)Enterprise configuration

Organizations can disable local Claude Code use in the desktop application with the `isClaudeCodeForDesktopEnabled` [enterprise policy option](https://support.claude.com/en/articles/12622667-enterprise-configuration#h_003283c7cb). Additionally, Claude Code on the web can be disabled in your [admin settings](https://claude.ai/admin-settings/claude-code).

## [​](#related-resources)Related resources

- [Claude Code on the web](/docs/en/claude-code-on-the-web): Run remote sessions that continue in the cloud

- [CLI reference](/docs/en/cli-reference): Use Claude Code in your terminal with flags and scripting

- [Common workflows](/docs/en/common-workflows): Tutorials for debugging, refactoring, testing, and more

- [Settings reference](/docs/en/settings): Configure Claude Code behavior with settings files

- [Claude Desktop support](https://support.claude.com/en/collections/16163169-claude-desktop): Help articles for the Chat tab and general desktop app usage

- [Enterprise configuration](https://support.claude.com/en/articles/12622667-enterprise-configuration): Admin policies for organizational deployments

Was this page helpful?YesNo[Claude Code on the web](/docs/en/claude-code-on-the-web)[Chrome extension (beta)](/docs/en/chrome)⌘I[Claude Code Docs home page](/docs)[x](https://x.com/AnthropicAI)[linkedin](https://www.linkedin.com/company/anthropicresearch)Company[Anthropic](https://www.anthropic.com/company)[Careers](https://www.anthropic.com/careers)[Economic Futures](https://www.anthropic.com/economic-futures)[Research](https://www.anthropic.com/research)[News](https://www.anthropic.com/news)[Trust center](https://trust.anthropic.com/)[Transparency](https://www.anthropic.com/transparency)Help and security[Availability](https://www.anthropic.com/supported-countries)[Status](https://status.anthropic.com/)[Support center](https://support.claude.com/)Learn[Courses](https://www.anthropic.com/learn)[MCP connectors](https://claude.com/partners/mcp)[Customer stories](https://www.claude.com/customers)[Engineering blog](https://www.anthropic.com/engineering)[Events](https://www.anthropic.com/events)[Powered by Claude](https://claude.com/partners/powered-by-claude)[Service partners](https://claude.com/partners/services)[Startups program](https://claude.com/programs/startups)Terms and policies[Privacy policy](https://www.anthropic.com/legal/privacy)[Disclosure policy](https://www.anthropic.com/responsible-disclosure-policy)[Usage policy](https://www.anthropic.com/legal/aup)[Commercial terms](https://www.anthropic.com/legal/commercial-terms)[Consumer terms](https://www.anthropic.com/legal/consumer-terms)