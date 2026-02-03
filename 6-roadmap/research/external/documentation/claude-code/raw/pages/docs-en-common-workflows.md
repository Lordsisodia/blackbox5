---
{
  "fetch": {
    "url": "https://code.claude.com/docs/en/common-workflows",
    "fetched_at": "2026-02-04T00:52:58.358653",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 1234877
  },
  "metadata": {
    "title": "Common workflows",
    "section": "common-workflows",
    "tier": 1,
    "type": "guide"
  }
}
---

- Common workflows - Claude Code Docs[Skip to main content](#content-area)[Claude Code Docs home page](/docs)EnglishSearch...⌘KAsk AI[Claude Developer Platform](https://platform.claude.com/)- [Claude Code on the Web](https://claude.ai/code)- [Claude Code on the Web](https://claude.ai/code)Search...NavigationCore conceptsCommon workflows[Getting started](/docs/en/overview)[Build with Claude Code](/docs/en/sub-agents)[Deployment](/docs/en/third-party-integrations)[Administration](/docs/en/setup)[Configuration](/docs/en/settings)[Reference](/docs/en/cli-reference)[Resources](/docs/en/legal-and-compliance)Getting started- [Overview](/docs/en/overview)- [Quickstart](/docs/en/quickstart)- [Changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)Core concepts- [How Claude Code works](/docs/en/how-claude-code-works)- [Extend Claude Code](/docs/en/features-overview)- [Common workflows](/docs/en/common-workflows)- [Best practices](/docs/en/best-practices)Outside of the terminal- [Claude Code on the web](/docs/en/claude-code-on-the-web)- [Claude Code on desktop](/docs/en/desktop)- [Chrome extension (beta)](/docs/en/chrome)- [Visual Studio Code](/docs/en/vs-code)- [JetBrains IDEs](/docs/en/jetbrains)- [GitHub Actions](/docs/en/github-actions)- [GitLab CI/CD](/docs/en/gitlab-ci-cd)- [Claude Code in Slack](/docs/en/slack)On this page- [Understand new codebases](#understand-new-codebases)- [Get a quick codebase overview](#get-a-quick-codebase-overview)- [Find relevant code](#find-relevant-code)- [Fix bugs efficiently](#fix-bugs-efficiently)- [Refactor code](#refactor-code)- [Use specialized subagents](#use-specialized-subagents)- [Use Plan Mode for safe code analysis](#use-plan-mode-for-safe-code-analysis)- [When to use Plan Mode](#when-to-use-plan-mode)- [How to use Plan Mode](#how-to-use-plan-mode)- [Example: Planning a complex refactor](#example%3A-planning-a-complex-refactor)- [Configure Plan Mode as default](#configure-plan-mode-as-default)- [Work with tests](#work-with-tests)- [Create pull requests](#create-pull-requests)- [Handle documentation](#handle-documentation)- [Work with images](#work-with-images)- [Reference files and directories](#reference-files-and-directories)- [Use extended thinking (thinking mode)](#use-extended-thinking-thinking-mode)- [Configure thinking mode](#configure-thinking-mode)- [How extended thinking token budgets work](#how-extended-thinking-token-budgets-work)- [Resume previous conversations](#resume-previous-conversations)- [Name your sessions](#name-your-sessions)- [Use the session picker](#use-the-session-picker)- [Run parallel Claude Code sessions with Git worktrees](#run-parallel-claude-code-sessions-with-git-worktrees)- [Use Claude as a unix-style utility](#use-claude-as-a-unix-style-utility)- [Add Claude to your verification process](#add-claude-to-your-verification-process)- [Pipe in, pipe out](#pipe-in%2C-pipe-out)- [Control output format](#control-output-format)- [Ask Claude about its capabilities](#ask-claude-about-its-capabilities)- [Example questions](#example-questions)- [Next steps](#next-steps)Core concepts# Common workflowsCopy pageStep-by-step guides for exploring codebases, fixing bugs, refactoring, testing, and other everyday tasks with Claude Code.Copy pageThis page covers practical workflows for everyday development: exploring unfamiliar code, debugging, refactoring, writing tests, creating PRs, and managing sessions. Each section includes example prompts you can adapt to your own projects. For higher-level patterns and tips, see [Best practices](/docs/en/best-practices).

## [​](#understand-new-codebases)Understand new codebases

### [​](#get-a-quick-codebase-overview)Get a quick codebase overview

Suppose you’ve just joined a new project and need to understand its structure quickly.

1[](#)Navigate to the project root directoryCopyAsk AI```

cd /path/to/project

```2[](#)Start Claude CodeCopyAsk AI```

claude

```3[](#)Ask for a high-level overviewCopyAsk AI```

> give me an overview of this codebase

```4[](#)Dive deeper into specific componentsCopyAsk AI```

> explain the main architecture patterns used here

```CopyAsk AI```

> what are the key data models?

```CopyAsk AI```

> how is authentication handled?

```

Tips:

- Start with broad questions, then narrow down to specific areas

- Ask about coding conventions and patterns used in the project

- Request a glossary of project-specific terms

### [​](#find-relevant-code)Find relevant code

Suppose you need to locate code related to a specific feature or functionality.

1[](#)Ask Claude to find relevant filesCopyAsk AI```

> find the files that handle user authentication

```2[](#)Get context on how components interactCopyAsk AI```

> how do these authentication files work together?

```3[](#)Understand the execution flowCopyAsk AI```

> trace the login process from front-end to database

```

Tips:

- Be specific about what you’re looking for

- Use domain language from the project

- Install a [code intelligence plugin](/docs/en/discover-plugins#code-intelligence) for your language to give Claude precise “go to definition” and “find references” navigation

## [​](#fix-bugs-efficiently)Fix bugs efficiently

Suppose you’ve encountered an error message and need to find and fix its source.

1[](#)Share the error with ClaudeCopyAsk AI```

> I'm seeing an error when I run npm test

```2[](#)Ask for fix recommendationsCopyAsk AI```

> suggest a few ways to fix the @ts-ignore in user.ts

```3[](#)Apply the fixCopyAsk AI```

> update user.ts to add the null check you suggested

```

Tips:

- Tell Claude the command to reproduce the issue and get a stack trace

- Mention any steps to reproduce the error

- Let Claude know if the error is intermittent or consistent

## [​](#refactor-code)Refactor code

Suppose you need to update old code to use modern patterns and practices.

1[](#)Identify legacy code for refactoringCopyAsk AI```

> find deprecated API usage in our codebase

```2[](#)Get refactoring recommendationsCopyAsk AI```

> suggest how to refactor utils.js to use modern JavaScript features

```3[](#)Apply the changes safelyCopyAsk AI```

> refactor utils.js to use ES2024 features while maintaining the same behavior

```4[](#)Verify the refactoringCopyAsk AI```

> run tests for the refactored code

```

Tips:

- Ask Claude to explain the benefits of the modern approach

- Request that changes maintain backward compatibility when needed

- Do refactoring in small, testable increments

## [​](#use-specialized-subagents)Use specialized subagents

Suppose you want to use specialized AI subagents to handle specific tasks more effectively.

1[](#)View available subagentsCopyAsk AI```

> /agents

```This shows all available subagents and lets you create new ones.2[](#)Use subagents automaticallyClaude Code automatically delegates appropriate tasks to specialized subagents:CopyAsk AI```

> review my recent code changes for security issues

```CopyAsk AI```

> run all tests and fix any failures

```3[](#)Explicitly request specific subagentsCopyAsk AI```

> use the code-reviewer subagent to check the auth module

```CopyAsk AI```

> have the debugger subagent investigate why users can't log in

```4[](#)Create custom subagents for your workflowCopyAsk AI```

> /agents

```Then select “Create New subagent” and follow the prompts to define:

- A unique identifier that describes the subagent’s purpose (for example, `code-reviewer`, `api-designer`).

- When Claude should use this agent

- Which tools it can access

- A system prompt describing the agent’s role and behavior

Tips:

- Create project-specific subagents in `.claude/agents/` for team sharing

- Use descriptive `description` fields to enable automatic delegation

- Limit tool access to what each subagent actually needs

- Check the [subagents documentation](/docs/en/sub-agents) for detailed examples

## [​](#use-plan-mode-for-safe-code-analysis)Use Plan Mode for safe code analysis

Plan Mode instructs Claude to create a plan by analyzing the codebase with read-only operations, perfect for exploring codebases, planning complex changes, or reviewing code safely. In Plan Mode, Claude uses [`AskUserQuestion`](/docs/en/settings#tools-available-to-claude) to gather requirements and clarify your goals before proposing a plan.

### [​](#when-to-use-plan-mode)When to use Plan Mode

- **Multi-step implementation**: When your feature requires making edits to many files

- **Code exploration**: When you want to research the codebase thoroughly before changing anything

- **Interactive development**: When you want to iterate on the direction with Claude

### [​](#how-to-use-plan-mode)How to use Plan Mode

**Turn on Plan Mode during a session**

You can switch into Plan Mode during a session using **Shift+Tab** to cycle through permission modes.

If you are in Normal Mode, **Shift+Tab** first switches into Auto-Accept Mode, indicated by `⏵⏵ accept edits on` at the bottom of the terminal. A subsequent **Shift+Tab** will switch into Plan Mode, indicated by `⏸ plan mode on`.

**Start a new session in Plan Mode**

To start a new session in Plan Mode, use the `--permission-mode plan` flag:

CopyAsk AI```

claude --permission-mode plan

```

**Run “headless” queries in Plan Mode**

You can also run a query in Plan Mode directly with `-p` (that is, in [“headless mode”](/docs/en/headless)):

CopyAsk AI```

claude --permission-mode plan -p "Analyze the authentication system and suggest improvements"

```

### [​](#example:-planning-a-complex-refactor)Example: Planning a complex refactor

CopyAsk AI```

claude --permission-mode plan

```

CopyAsk AI```

> I need to refactor our authentication system to use OAuth2. Create a detailed migration plan.

```

Claude analyzes the current implementation and create a comprehensive plan. Refine with follow-ups:

CopyAsk AI```

> What about backward compatibility?

> How should we handle database migration?

```

Press `Ctrl+G` to open the plan in your default text editor, where you can edit it directly before Claude proceeds.

### [​](#configure-plan-mode-as-default)Configure Plan Mode as default

CopyAsk AI```

// .claude/settings.json

{

"permissions": {

"defaultMode": "plan"

}

}

```

See [settings documentation](/docs/en/settings#available-settings) for more configuration options.

## [​](#work-with-tests)Work with tests

Suppose you need to add tests for uncovered code.

1[](#)Identify untested codeCopyAsk AI```

> find functions in NotificationsService.swift that are not covered by tests

```2[](#)Generate test scaffoldingCopyAsk AI```

> add tests for the notification service

```3[](#)Add meaningful test casesCopyAsk AI```

> add test cases for edge conditions in the notification service

```4[](#)Run and verify testsCopyAsk AI```

> run the new tests and fix any failures

```

Claude can generate tests that follow your project’s existing patterns and conventions. When asking for tests, be specific about what behavior you want to verify. Claude examines your existing test files to match the style, frameworks, and assertion patterns already in use.

For comprehensive coverage, ask Claude to identify edge cases you might have missed. Claude can analyze your code paths and suggest tests for error conditions, boundary values, and unexpected inputs that are easy to overlook.

## [​](#create-pull-requests)Create pull requests

You can create pull requests by asking Claude directly (“create a pr for my changes”) or by using the `/commit-push-pr` skill, which commits, pushes, and opens a PR in one step.

CopyAsk AI```

> /commit-push-pr

```

If you have a Slack MCP server configured and specify channels in your CLAUDE.md (for example, “post PR URLs to #team-prs”), the skill automatically posts the PR URL to those channels.

For more control over the process, guide Claude through it step-by-step or [create your own skill](/docs/en/skills):

1[](#)Summarize your changesCopyAsk AI```

> summarize the changes I've made to the authentication module

```2[](#)Generate a pull requestCopyAsk AI```

> create a pr

```3[](#)Review and refineCopyAsk AI```

> enhance the PR description with more context about the security improvements

```

When you create a PR using `gh pr create`, the session is automatically linked to that PR. You can resume it later with `claude --from-pr <number>`.

Review Claude’s generated PR before submitting and ask Claude to highlight potential risks or considerations.

## [​](#handle-documentation)Handle documentation

Suppose you need to add or update documentation for your code.

1[](#)Identify undocumented codeCopyAsk AI```

> find functions without proper JSDoc comments in the auth module

```2[](#)Generate documentationCopyAsk AI```

> add JSDoc comments to the undocumented functions in auth.js

```3[](#)Review and enhanceCopyAsk AI```

> improve the generated documentation with more context and examples

```4[](#)Verify documentationCopyAsk AI```

> check if the documentation follows our project standards

```

Tips:

- Specify the documentation style you want (JSDoc, docstrings, etc.)

- Ask for examples in the documentation

- Request documentation for public APIs, interfaces, and complex logic

## [​](#work-with-images)Work with images

Suppose you need to work with images in your codebase, and you want Claude’s help analyzing image content.

1[](#)Add an image to the conversationYou can use any of these methods:

- Drag and drop an image into the Claude Code window

- Copy an image and paste it into the CLI with ctrl+v (Do not use cmd+v)

- Provide an image path to Claude. E.g., “Analyze this image: /path/to/your/image.png”

2[](#)Ask Claude to analyze the imageCopyAsk AI```

> What does this image show?

```CopyAsk AI```

> Describe the UI elements in this screenshot

```CopyAsk AI```

> Are there any problematic elements in this diagram?

```3[](#)Use images for contextCopyAsk AI```

> Here's a screenshot of the error. What's causing it?

```CopyAsk AI```

> This is our current database schema. How should we modify it for the new feature?

```4[](#)Get code suggestions from visual contentCopyAsk AI```

> Generate CSS to match this design mockup

```CopyAsk AI```

> What HTML structure would recreate this component?

```

Tips:

- Use images when text descriptions would be unclear or cumbersome

- Include screenshots of errors, UI designs, or diagrams for better context

- You can work with multiple images in a conversation

- Image analysis works with diagrams, screenshots, mockups, and more

- When Claude references images (for example, `[Image #1]`), `Cmd+Click` (Mac) or `Ctrl+Click` (Windows/Linux) the link to open the image in your default viewer

## [​](#reference-files-and-directories)Reference files and directories

Use @ to quickly include files or directories without waiting for Claude to read them.

1[](#)Reference a single fileCopyAsk AI```

> Explain the logic in @src/utils/auth.js

```This includes the full content of the file in the conversation.2[](#)Reference a directoryCopyAsk AI```

> What's the structure of @src/components?

```This provides a directory listing with file information.3[](#)Reference MCP resourcesCopyAsk AI```

> Show me the data from @github:repos/owner/repo/issues

```This fetches data from connected MCP servers using the format @server:resource. See [MCP resources](/docs/en/mcp#use-mcp-resources) for details.

Tips:

- File paths can be relative or absolute

- @ file references add `CLAUDE.md` in the file’s directory and parent directories to context

- Directory references show file listings, not contents

- You can reference multiple files in a single message (for example, “@file1.js and @file2.js”)

## [​](#use-extended-thinking-thinking-mode)Use extended thinking (thinking mode)

[Extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) is enabled by default, reserving a portion of the output token budget (up to 31,999 tokens) for Claude to reason through complex problems step-by-step. This reasoning is visible in verbose mode, which you can toggle on with `Ctrl+O`.

Extended thinking is particularly valuable for complex architectural decisions, challenging bugs, multi-step implementation planning, and evaluating tradeoffs between different approaches. It provides more space for exploring multiple solutions, analyzing edge cases, and self-correcting mistakes.

Phrases like “think”, “think hard”, “ultrathink”, and “think more” are interpreted as regular prompt instructions and don’t allocate thinking tokens.

### [​](#configure-thinking-mode)Configure thinking mode

Thinking is enabled by default, but you can adjust or disable it.

ScopeHow to configureDetails**Toggle shortcut**Press `Option+T` (macOS) or `Alt+T` (Windows/Linux)Toggle thinking on/off for the current session. May require [terminal configuration](/docs/en/terminal-config) to enable Option key shortcuts**Global default**Use `/config` to toggle thinking modeSets your default across all projects.Saved as `alwaysThinkingEnabled` in `~/.claude/settings.json`**Limit token budget**Set [`MAX_THINKING_TOKENS`](/docs/en/settings#environment-variables) environment variableLimit the thinking budget to a specific number of tokens. Example: `export MAX_THINKING_TOKENS=10000`

To view Claude’s thinking process, press `Ctrl+O` to toggle verbose mode and see the internal reasoning displayed as gray italic text.

### [​](#how-extended-thinking-token-budgets-work)How extended thinking token budgets work

Extended thinking uses a **token budget** that controls how much internal reasoning Claude can perform before responding.

A larger thinking token budget provides:

- More space to explore multiple solution approaches step-by-step

- Room to analyze edge cases and evaluate tradeoffs thoroughly

- Ability to revise reasoning and self-correct mistakes

Token budgets for thinking mode:

- When thinking is **enabled**, Claude can use up to **31,999 tokens** from your output budget for internal reasoning

- When thinking is **disabled** (via toggle or `/config`), Claude uses **0 tokens** for thinking

**Limit the thinking budget:**

- Use the [`MAX_THINKING_TOKENS` environment variable](/docs/en/settings#environment-variables) to cap the thinking budget

- When set, this value limits the maximum tokens Claude can use for thinking

- See the [extended thinking documentation](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for valid token ranges

You’re charged for all thinking tokens used, even though Claude 4 models show summarized thinking

## [​](#resume-previous-conversations)Resume previous conversations

When starting Claude Code, you can resume a previous session:

- `claude --continue` continues the most recent conversation in the current directory

- `claude --resume` opens a conversation picker or resumes by name

- `claude --from-pr 123` resumes sessions linked to a specific pull request

From inside an active session, use `/resume` to switch to a different conversation.

Sessions are stored per project directory. The `/resume` picker shows sessions from the same git repository, including worktrees.

### [​](#name-your-sessions)Name your sessions

Give sessions descriptive names to find them later. This is a best practice when working on multiple tasks or features.

1[](#)Name the current sessionUse `/rename` during a session to give it a memorable name:CopyAsk AI```

> /rename auth-refactor

```You can also rename any session from the picker: run `/resume`, navigate to a session, and press `R`.2[](#)Resume by name laterFrom the command line:CopyAsk AI```

claude --resume auth-refactor

```Or from inside an active session:CopyAsk AI```

> /resume auth-refactor

```

### [​](#use-the-session-picker)Use the session picker

The `/resume` command (or `claude --resume` without arguments) opens an interactive session picker with these features:

**Keyboard shortcuts in the picker:**

ShortcutAction`↑` / `↓`Navigate between sessions`→` / `←`Expand or collapse grouped sessions`Enter`Select and resume the highlighted session`P`Preview the session content`R`Rename the highlighted session`/`Search to filter sessions`A`Toggle between current directory and all projects`B`Filter to sessions from your current git branch`Esc`Exit the picker or search mode

**Session organization:**

The picker displays sessions with helpful metadata:

- Session name or initial prompt

- Time elapsed since last activity

- Message count

- Git branch (if applicable)

Forked sessions (created with `/rewind` or `--fork-session`) are grouped together under their root session, making it easier to find related conversations.

Tips:

- **Name sessions early**: Use `/rename` when starting work on a distinct task—it’s much easier to find “payment-integration” than “explain this function” later

- Use `--continue` for quick access to your most recent conversation in the current directory

- Use `--resume session-name` when you know which session you need

- Use `--resume` (without a name) when you need to browse and select

- For scripts, use `claude --continue --print "prompt"` to resume in non-interactive mode

- Press `P` in the picker to preview a session before resuming it

- The resumed conversation starts with the same model and configuration as the original

How it works:

- **Conversation Storage**: All conversations are automatically saved locally with their full message history

- **Message Deserialization**: When resuming, the entire message history is restored to maintain context

- **Tool State**: Tool usage and results from the previous conversation are preserved

- **Context Restoration**: The conversation resumes with all previous context intact

## [​](#run-parallel-claude-code-sessions-with-git-worktrees)Run parallel Claude Code sessions with Git worktrees

Suppose you need to work on multiple tasks simultaneously with complete code isolation between Claude Code instances.

1[](#)Understand Git worktreesGit worktrees allow you to check out multiple branches from the same

repository into separate directories. Each worktree has its own working

directory with isolated files, while sharing the same Git history. Learn

more in the [official Git worktree

documentation](https://git-scm.com/docs/git-worktree).2[](#)Create a new worktreeCopyAsk AI```

# Create a new worktree with a new branch

git worktree add ../project-feature-a -b feature-a

# Or create a worktree with an existing branch

git worktree add ../project-bugfix bugfix-123

```This creates a new directory with a separate working copy of your repository.3[](#)Run Claude Code in each worktreeCopyAsk AI```

# Navigate to your worktree

cd ../project-feature-a

# Run Claude Code in this isolated environment

claude

```4[](#)Run Claude in another worktreeCopyAsk AI```

cd ../project-bugfix

claude

```5[](#)Manage your worktreesCopyAsk AI```

# List all worktrees

git worktree list

# Remove a worktree when done

git worktree remove ../project-feature-a

```

Tips:

- Each worktree has its own independent file state, making it perfect for parallel Claude Code sessions

- Changes made in one worktree won’t affect others, preventing Claude instances from interfering with each other

- All worktrees share the same Git history and remote connections

- For long-running tasks, you can have Claude working in one worktree while you continue development in another

- Use descriptive directory names to easily identify which task each worktree is for

- Remember to initialize your development environment in each new worktree according to your project’s setup. Depending on your stack, this might include:

JavaScript projects: Running dependency installation (`npm install`, `yarn`)

- Python projects: Setting up virtual environments or installing with package managers

- Other languages: Following your project’s standard setup process

## [​](#use-claude-as-a-unix-style-utility)Use Claude as a unix-style utility

### [​](#add-claude-to-your-verification-process)Add Claude to your verification process

Suppose you want to use Claude Code as a linter or code reviewer.

**Add Claude to your build script:**

CopyAsk AI```

// package.json

{

...

"scripts": {

...

"lint:claude": "claude -p 'you are a linter. please look at the changes vs. main and report any issues related to typos. report the filename and line number on one line, and a description of the issue on the second line. do not return any other text.'"

}

}

```

Tips:

- Use Claude for automated code review in your CI/CD pipeline

- Customize the prompt to check for specific issues relevant to your project

- Consider creating multiple scripts for different types of verification

### [​](#pipe-in,-pipe-out)Pipe in, pipe out

Suppose you want to pipe data into Claude, and get back data in a structured format.

**Pipe data through Claude:**

CopyAsk AI```

cat build-error.txt | claude -p 'concisely explain the root cause of this build error' > output.txt

```

Tips:

- Use pipes to integrate Claude into existing shell scripts

- Combine with other Unix tools for powerful workflows

- Consider using —output-format for structured output

### [​](#control-output-format)Control output format

Suppose you need Claude’s output in a specific format, especially when integrating Claude Code into scripts or other tools.

1[](#)Use text format (default)CopyAsk AI```

cat data.txt | claude -p 'summarize this data' --output-format text > summary.txt

```This outputs just Claude’s plain text response (default behavior).2[](#)Use JSON formatCopyAsk AI```

cat code.py | claude -p 'analyze this code for bugs' --output-format json > analysis.json

```This outputs a JSON array of messages with metadata including cost and duration.3[](#)Use streaming JSON formatCopyAsk AI```

cat log.txt | claude -p 'parse this log file for errors' --output-format stream-json

```This outputs a series of JSON objects in real-time as Claude processes the request. Each message is a valid JSON object, but the entire output is not valid JSON if concatenated.

Tips:

- Use `--output-format text` for simple integrations where you just need Claude’s response

- Use `--output-format json` when you need the full conversation log

- Use `--output-format stream-json` for real-time output of each conversation turn

## [​](#ask-claude-about-its-capabilities)Ask Claude about its capabilities

Claude has built-in access to its documentation and can answer questions about its own features and limitations.

### [​](#example-questions)Example questions

CopyAsk AI```

> can Claude Code create pull requests?

```

CopyAsk AI```

> how does Claude Code handle permissions?

```

CopyAsk AI```

> what skills are available?

```

CopyAsk AI```

> how do I use MCP with Claude Code?

```

CopyAsk AI```

> how do I configure Claude Code for Amazon Bedrock?

```

CopyAsk AI```

> what are the limitations of Claude Code?

```

Claude provides documentation-based answers to these questions. For executable examples and hands-on demonstrations, refer to the specific workflow sections above.

Tips:

- Claude always has access to the latest Claude Code documentation, regardless of the version you’re using

- Ask specific questions to get detailed answers

- Claude can explain complex features like MCP integration, enterprise configurations, and advanced workflows

## [​](#next-steps)Next steps

[## Best practicesPatterns for getting the most out of Claude Code](/docs/en/best-practices)[## How Claude Code worksUnderstand the agentic loop and context management](/docs/en/how-claude-code-works)[## Extend Claude CodeAdd skills, hooks, MCP, subagents, and plugins](/docs/en/features-overview)[## Reference implementationClone our development container reference implementation](https://github.com/anthropics/claude-code/tree/main/.devcontainer)Was this page helpful?YesNo[Extend Claude Code](/docs/en/features-overview)[Best practices](/docs/en/best-practices)⌘I[Claude Code Docs home page](/docs)[x](https://x.com/AnthropicAI)[linkedin](https://www.linkedin.com/company/anthropicresearch)Company[Anthropic](https://www.anthropic.com/company)[Careers](https://www.anthropic.com/careers)[Economic Futures](https://www.anthropic.com/economic-futures)[Research](https://www.anthropic.com/research)[News](https://www.anthropic.com/news)[Trust center](https://trust.anthropic.com/)[Transparency](https://www.anthropic.com/transparency)Help and security[Availability](https://www.anthropic.com/supported-countries)[Status](https://status.anthropic.com/)[Support center](https://support.claude.com/)Learn[Courses](https://www.anthropic.com/learn)[MCP connectors](https://claude.com/partners/mcp)[Customer stories](https://www.claude.com/customers)[Engineering blog](https://www.anthropic.com/engineering)[Events](https://www.anthropic.com/events)[Powered by Claude](https://claude.com/partners/powered-by-claude)[Service partners](https://claude.com/partners/services)[Startups program](https://claude.com/programs/startups)Terms and policies[Privacy policy](https://www.anthropic.com/legal/privacy)[Disclosure policy](https://www.anthropic.com/responsible-disclosure-policy)[Usage policy](https://www.anthropic.com/legal/aup)[Commercial terms](https://www.anthropic.com/legal/commercial-terms)[Consumer terms](https://www.anthropic.com/legal/consumer-terms)