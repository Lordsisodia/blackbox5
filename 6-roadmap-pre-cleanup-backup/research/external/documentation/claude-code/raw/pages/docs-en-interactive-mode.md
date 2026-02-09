---
{
  "fetch": {
    "url": "https://code.claude.com/docs/en/interactive-mode",
    "fetched_at": "2026-02-04T00:53:45.674766",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 704009
  },
  "metadata": {
    "title": "Interactive mode",
    "section": "interactive-mode",
    "tier": 3,
    "type": "reference"
  }
}
---

- Interactive mode - Claude Code Docs[Skip to main content](#content-area)[Claude Code Docs home page](/docs)EnglishSearch...⌘KAsk AI[Claude Developer Platform](https://platform.claude.com/)- [Claude Code on the Web](https://claude.ai/code)- [Claude Code on the Web](https://claude.ai/code)Search...NavigationReferenceInteractive mode[Getting started](/docs/en/overview)[Build with Claude Code](/docs/en/sub-agents)[Deployment](/docs/en/third-party-integrations)[Administration](/docs/en/setup)[Configuration](/docs/en/settings)[Reference](/docs/en/cli-reference)[Resources](/docs/en/legal-and-compliance)Reference- [CLI reference](/docs/en/cli-reference)- [Interactive mode](/docs/en/interactive-mode)- [Checkpointing](/docs/en/checkpointing)- [Hooks reference](/docs/en/hooks)- [Plugins reference](/docs/en/plugins-reference)On this page- [Keyboard shortcuts](#keyboard-shortcuts)- [General controls](#general-controls)- [Text editing](#text-editing)- [Theme and display](#theme-and-display)- [Multiline input](#multiline-input)- [Quick commands](#quick-commands)- [Built-in commands](#built-in-commands)- [MCP prompts](#mcp-prompts)- [Vim editor mode](#vim-editor-mode)- [Mode switching](#mode-switching)- [Navigation (NORMAL mode)](#navigation-normal-mode)- [Editing (NORMAL mode)](#editing-normal-mode)- [Text objects (NORMAL mode)](#text-objects-normal-mode)- [Command history](#command-history)- [Reverse search with Ctrl+R](#reverse-search-with-ctrl%2Br)- [Background bash commands](#background-bash-commands)- [How backgrounding works](#how-backgrounding-works)- [Bash mode with ! prefix](#bash-mode-with-prefix)- [Prompt suggestions](#prompt-suggestions)- [Task list](#task-list)- [PR review status](#pr-review-status)- [See also](#see-also)Reference# Interactive modeCopy pageComplete reference for keyboard shortcuts, input modes, and interactive features in Claude Code sessions.Copy page## [​](#keyboard-shortcuts)Keyboard shortcuts

Keyboard shortcuts may vary by platform and terminal. Press `?` to see available shortcuts for your environment.**macOS users**: Option/Alt key shortcuts (`Alt+B`, `Alt+F`, `Alt+Y`, `Alt+M`, `Alt+P`) require configuring Option as Meta in your terminal:

- **iTerm2**: Settings → Profiles → Keys → Set Left/Right Option key to “Esc+”

- **Terminal.app**: Settings → Profiles → Keyboard → Check “Use Option as Meta Key”

- **VS Code**: Settings → Profiles → Keys → Set Left/Right Option key to “Esc+”

See [Terminal configuration](/docs/en/terminal-config) for details.

### [​](#general-controls)General controls

ShortcutDescriptionContext`Ctrl+C`Cancel current input or generationStandard interrupt`Ctrl+D`Exit Claude Code sessionEOF signal`Ctrl+G`Open in default text editorEdit your prompt or custom response in your default text editor`Ctrl+L`Clear terminal screenKeeps conversation history`Ctrl+O`Toggle verbose outputShows detailed tool usage and execution`Ctrl+R`Reverse search command historySearch through previous commands interactively`Ctrl+V` or `Cmd+V` (iTerm2) or `Alt+V` (Windows)Paste image from clipboardPastes an image or path to an image file`Ctrl+B`Background running tasksBackgrounds bash commands and agents. Tmux users press twice`Left/Right arrows`Cycle through dialog tabsNavigate between tabs in permission dialogs and menus`Up/Down arrows`Navigate command historyRecall previous inputs`Esc` + `Esc`Rewind the code/conversationRestore the code and/or conversation to a previous point`Shift+Tab` or `Alt+M` (some configurations)Toggle permission modesSwitch between Auto-Accept Mode, Plan Mode, and normal mode`Option+P` (macOS) or `Alt+P` (Windows/Linux)Switch modelSwitch models without clearing your prompt`Option+T` (macOS) or `Alt+T` (Windows/Linux)Toggle extended thinkingEnable or disable extended thinking mode. Run `/terminal-setup` first to enable this shortcut

### [​](#text-editing)Text editing

ShortcutDescriptionContext`Ctrl+K`Delete to end of lineStores deleted text for pasting`Ctrl+U`Delete entire lineStores deleted text for pasting`Ctrl+Y`Paste deleted textPaste text deleted with `Ctrl+K` or `Ctrl+U``Alt+Y` (after `Ctrl+Y`)Cycle paste historyAfter pasting, cycle through previously deleted text. Requires [Option as Meta](#keyboard-shortcuts) on macOS`Alt+B`Move cursor back one wordWord navigation. Requires [Option as Meta](#keyboard-shortcuts) on macOS`Alt+F`Move cursor forward one wordWord navigation. Requires [Option as Meta](#keyboard-shortcuts) on macOS

### [​](#theme-and-display)Theme and display

ShortcutDescriptionContext`Ctrl+T`Toggle syntax highlighting for code blocksOnly works inside the `/theme` picker menu. Controls whether code in Claude’s responses uses syntax coloring

Syntax highlighting is only available in the native build of Claude Code.

### [​](#multiline-input)Multiline input

MethodShortcutContextQuick escape`\` + `Enter`Works in all terminalsmacOS default`Option+Enter`Default on macOSShift+Enter`Shift+Enter`Works out of the box in iTerm2, WezTerm, Ghostty, KittyControl sequence`Ctrl+J`Line feed character for multilinePaste modePaste directlyFor code blocks, logs

Shift+Enter works without configuration in iTerm2, WezTerm, Ghostty, and Kitty. For other terminals (VS Code, Alacritty, Zed, Warp), run `/terminal-setup` to install the binding.

### [​](#quick-commands)Quick commands

ShortcutDescriptionNotes`/` at startCommand or skillSee [built-in commands](#built-in-commands) and [skills](/docs/en/skills)`!` at startBash modeRun commands directly and add execution output to the session`@`File path mentionTrigger file path autocomplete

## [​](#built-in-commands)Built-in commands

Built-in commands are shortcuts for common actions. The table below covers commonly used commands but not all available options. Type `/` in Claude Code to see the full list, or type `/` followed by any letters to filter.

To create your own commands you can invoke with `/`, see [skills](/docs/en/skills).

CommandPurpose`/clear`Clear conversation history`/compact [instructions]`Compact conversation with optional focus instructions`/config`Open the Settings interface (Config tab)`/context`Visualize current context usage as a colored grid`/cost`Show token usage statistics. See [cost tracking guide](/docs/en/costs#using-the-cost-command) for subscription-specific details.`/doctor`Checks the health of your Claude Code installation`/exit`Exit the REPL`/export [filename]`Export the current conversation to a file or clipboard`/help`Get usage help`/init`Initialize project with `CLAUDE.md` guide`/mcp`Manage MCP server connections and OAuth authentication`/memory`Edit `CLAUDE.md` memory files`/model`Select or change the AI model`/permissions`View or update [permissions](/docs/en/permissions#manage-permissions)`/plan`Enter plan mode directly from the prompt`/rename <name>`Rename the current session for easier identification`/resume [session]`Resume a conversation by ID or name, or open the session picker`/rewind`Rewind the conversation and/or code`/stats`Visualize daily usage, session history, streaks, and model preferences`/status`Open the Settings interface (Status tab) showing version, model, account, and connectivity`/statusline`Set up Claude Code’s status line UI`/copy`Copy the last assistant response to clipboard`/tasks`List and manage background tasks`/teleport`Resume a remote session from claude.ai (subscribers only)`/theme`Change the color theme`/todos`List current TODO items`/usage`For subscription plans only: show plan usage limits and rate limit status

### [​](#mcp-prompts)MCP prompts

MCP servers can expose prompts that appear as commands. These use the format `/mcp__<server>__<prompt>` and are dynamically discovered from connected servers. See [MCP prompts](/docs/en/mcp#use-mcp-prompts-as-commands) for details.

## [​](#vim-editor-mode)Vim editor mode

Enable vim-style editing with `/vim` command or configure permanently via `/config`.

### [​](#mode-switching)Mode switching

CommandActionFrom mode`Esc`Enter NORMAL modeINSERT`i`Insert before cursorNORMAL`I`Insert at beginning of lineNORMAL`a`Insert after cursorNORMAL`A`Insert at end of lineNORMAL`o`Open line belowNORMAL`O`Open line aboveNORMAL

### [​](#navigation-normal-mode)Navigation (NORMAL mode)

CommandAction`h`/`j`/`k`/`l`Move left/down/up/right`w`Next word`e`End of word`b`Previous word`0`Beginning of line`$`End of line`^`First non-blank character`gg`Beginning of input`G`End of input`f{char}`Jump to next occurrence of character`F{char}`Jump to previous occurrence of character`t{char}`Jump to just before next occurrence of character`T{char}`Jump to just after previous occurrence of character`;`Repeat last f/F/t/T motion`,`Repeat last f/F/t/T motion in reverse

In vim normal mode, if the cursor is at the beginning or end of input and cannot move further, the arrow keys navigate command history instead.

### [​](#editing-normal-mode)Editing (NORMAL mode)

CommandAction`x`Delete character`dd`Delete line`D`Delete to end of line`dw`/`de`/`db`Delete word/to end/back`cc`Change line`C`Change to end of line`cw`/`ce`/`cb`Change word/to end/back`yy`/`Y`Yank (copy) line`yw`/`ye`/`yb`Yank word/to end/back`p`Paste after cursor`P`Paste before cursor`>>`Indent line`<<`Dedent line`J`Join lines`.`Repeat last change

### [​](#text-objects-normal-mode)Text objects (NORMAL mode)

Text objects work with operators like `d`, `c`, and `y`:

CommandAction`iw`/`aw`Inner/around word`iW`/`aW`Inner/around WORD (whitespace-delimited)`i"`/`a"`Inner/around double quotes`i'`/`a'`Inner/around single quotes`i(`/`a(`Inner/around parentheses`i[`/`a[`Inner/around brackets`i{`/`a{`Inner/around braces

## [​](#command-history)Command history

Claude Code maintains command history for the current session:

- History is stored per working directory

- Cleared with `/clear` command

- Use Up/Down arrows to navigate (see keyboard shortcuts above)

- **Note**: History expansion (`!`) is disabled by default

### [​](#reverse-search-with-ctrl+r)Reverse search with Ctrl+R

Press `Ctrl+R` to interactively search through your command history:

- **Start search**: Press `Ctrl+R` to activate reverse history search

- **Type query**: Enter text to search for in previous commands - the search term will be highlighted in matching results

- **Navigate matches**: Press `Ctrl+R` again to cycle through older matches

- **Accept match**:

Press `Tab` or `Esc` to accept the current match and continue editing

- Press `Enter` to accept and execute the command immediately

- **Cancel search**:

Press `Ctrl+C` to cancel and restore your original input

- Press `Backspace` on empty search to cancel

The search displays matching commands with the search term highlighted, making it easy to find and reuse previous inputs.

## [​](#background-bash-commands)Background bash commands

Claude Code supports running bash commands in the background, allowing you to continue working while long-running processes execute.

### [​](#how-backgrounding-works)How backgrounding works

When Claude Code runs a command in the background, it runs the command asynchronously and immediately returns a background task ID. Claude Code can respond to new prompts while the command continues executing in the background.

To run commands in the background, you can either:

- Prompt Claude Code to run a command in the background

- Press Ctrl+B to move a regular Bash tool invocation to the background. (Tmux users must press Ctrl+B twice due to tmux’s prefix key.)

**Key features:**

- Output is buffered and Claude can retrieve it using the TaskOutput tool

- Background tasks have unique IDs for tracking and output retrieval

- Background tasks are automatically cleaned up when Claude Code exits

To disable all background task functionality, set the `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` environment variable to `1`. See [Environment variables](/docs/en/settings#environment-variables) for details.

**Common backgrounded commands:**

- Build tools (webpack, vite, make)

- Package managers (npm, yarn, pnpm)

- Test runners (jest, pytest)

- Development servers

- Long-running processes (docker, terraform)

### [​](#bash-mode-with-prefix)Bash mode with `!` prefix

Run bash commands directly without going through Claude by prefixing your input with `!`:

CopyAsk AI```

! npm test

! git status

! ls -la

```

Bash mode:

- Adds the command and its output to the conversation context

- Shows real-time progress and output

- Supports the same `Ctrl+B` backgrounding for long-running commands

- Does not require Claude to interpret or approve the command

- Supports history-based autocomplete: type a partial command and press **Tab** to complete from previous `!` commands in the current project

This is useful for quick shell operations while maintaining conversation context.

## [​](#prompt-suggestions)Prompt suggestions

When you first open a session, a grayed-out example command appears in the prompt input to help you get started. Claude Code picks this from your project’s git history, so it reflects files you’ve been working on recently.

After Claude responds, suggestions continue to appear based on your conversation history, such as a follow-up step from a multi-part request or a natural continuation of your workflow.

- Press **Tab** to accept the suggestion, or press **Enter** to accept and submit

- Start typing to dismiss it

The suggestion runs as a background request that reuses the parent conversation’s prompt cache, so the additional cost is minimal. Claude Code skips suggestion generation when the cache is cold to avoid unnecessary cost.

Suggestions are automatically skipped after the first turn of a conversation, in non-interactive mode, and in plan mode.

To disable prompt suggestions entirely, set the environment variable or toggle the setting in `/config`:

CopyAsk AI```

export CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION=false

```

## [​](#task-list)Task list

When working on complex, multi-step work, Claude creates a task list to track progress. Tasks appear in the status area of your terminal with indicators showing what’s pending, in progress, or complete.

- Press `Ctrl+T` to toggle the task list view. The display shows up to 10 tasks at a time

- To see all tasks or clear them, ask Claude directly: “show me all tasks” or “clear all tasks”

- Tasks persist across context compactions, helping Claude stay organized on larger projects

- To share a task list across sessions, set `CLAUDE_CODE_TASK_LIST_ID` to use a named directory in `~/.claude/tasks/`: `CLAUDE_CODE_TASK_LIST_ID=my-project claude`

- To revert to the previous TODO list, set `CLAUDE_CODE_ENABLE_TASKS=false`.

## [​](#pr-review-status)PR review status

When working on a branch with an open pull request, Claude Code displays a clickable PR link in the footer (for example, “PR #446”). The link has a colored underline indicating the review state:

- Green: approved

- Yellow: pending review

- Red: changes requested

- Gray: draft

- Purple: merged

`Cmd+click` (Mac) or `Ctrl+click` (Windows/Linux) the link to open the pull request in your browser. The status updates automatically every 60 seconds.

PR status requires the `gh` CLI to be installed and authenticated (`gh auth login`).

## [​](#see-also)See also

- [Skills](/docs/en/skills) - Custom prompts and workflows

- [Checkpointing](/docs/en/checkpointing) - Rewind Claude’s edits and restore previous states

- [CLI reference](/docs/en/cli-reference) - Command-line flags and options

- [Settings](/docs/en/settings) - Configuration options

- [Memory management](/docs/en/memory) - Managing CLAUDE.md files

Was this page helpful?YesNo[CLI reference](/docs/en/cli-reference)[Checkpointing](/docs/en/checkpointing)⌘I[Claude Code Docs home page](/docs)[x](https://x.com/AnthropicAI)[linkedin](https://www.linkedin.com/company/anthropicresearch)Company[Anthropic](https://www.anthropic.com/company)[Careers](https://www.anthropic.com/careers)[Economic Futures](https://www.anthropic.com/economic-futures)[Research](https://www.anthropic.com/research)[News](https://www.anthropic.com/news)[Trust center](https://trust.anthropic.com/)[Transparency](https://www.anthropic.com/transparency)Help and security[Availability](https://www.anthropic.com/supported-countries)[Status](https://status.anthropic.com/)[Support center](https://support.claude.com/)Learn[Courses](https://www.anthropic.com/learn)[MCP connectors](https://claude.com/partners/mcp)[Customer stories](https://www.claude.com/customers)[Engineering blog](https://www.anthropic.com/engineering)[Events](https://www.anthropic.com/events)[Powered by Claude](https://claude.com/partners/powered-by-claude)[Service partners](https://claude.com/partners/services)[Startups program](https://claude.com/programs/startups)Terms and policies[Privacy policy](https://www.anthropic.com/legal/privacy)[Disclosure policy](https://www.anthropic.com/responsible-disclosure-policy)[Usage policy](https://www.anthropic.com/legal/aup)[Commercial terms](https://www.anthropic.com/legal/commercial-terms)[Consumer terms](https://www.anthropic.com/legal/consumer-terms)