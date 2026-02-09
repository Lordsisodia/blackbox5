---
{
  "fetch": {
    "url": "https://code.claude.com/docs/en/terminal-config",
    "fetched_at": "2026-02-04T00:54:00.427561",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 494664
  },
  "metadata": {
    "title": "Optimize your terminal setup",
    "section": "terminal-config",
    "tier": 3,
    "type": "guide"
  }
}
---

- Optimize your terminal setup - Claude Code Docs[Skip to main content](#content-area)[Claude Code Docs home page](/docs)EnglishSearch...⌘KAsk AI[Claude Developer Platform](https://platform.claude.com/)- [Claude Code on the Web](https://claude.ai/code)- [Claude Code on the Web](https://claude.ai/code)Search...NavigationConfigurationOptimize your terminal setup[Getting started](/docs/en/overview)[Build with Claude Code](/docs/en/sub-agents)[Deployment](/docs/en/third-party-integrations)[Administration](/docs/en/setup)[Configuration](/docs/en/settings)[Reference](/docs/en/cli-reference)[Resources](/docs/en/legal-and-compliance)Configuration- [Settings](/docs/en/settings)- [Permissions](/docs/en/permissions)- [Sandboxing](/docs/en/sandboxing)- [Terminal configuration](/docs/en/terminal-config)- [Model configuration](/docs/en/model-config)- [Memory management](/docs/en/memory)- [Status line configuration](/docs/en/statusline)- [Customize keyboard shortcuts](/docs/en/keybindings)On this page- [Themes and appearance](#themes-and-appearance)- [Line breaks](#line-breaks)- [Notification setup](#notification-setup)- [iTerm 2 system notifications](#iterm-2-system-notifications)- [Custom notification hooks](#custom-notification-hooks)- [Handling large inputs](#handling-large-inputs)- [Vim Mode](#vim-mode)Configuration# Optimize your terminal setupCopy pageClaude Code works best when your terminal is properly configured. Follow these guidelines to optimize your experience.Copy page### [​](#themes-and-appearance)Themes and appearance

Claude cannot control the theme of your terminal. That’s handled by your terminal application. You can match Claude Code’s theme to your terminal any time via the `/config` command.

For additional customization of the Claude Code interface itself, you can configure a [custom status line](/docs/en/statusline) to display contextual information like the current model, working directory, or git branch at the bottom of your terminal.

### [​](#line-breaks)Line breaks

You have several options for entering line breaks into Claude Code:

- **Quick escape**: Type `\` followed by Enter to create a newline

- **Shift+Enter**: Works out of the box in iTerm2, WezTerm, Ghostty, and Kitty

- **Keyboard shortcut**: Set up a keybinding to insert a newline in other terminals

**Set up Shift+Enter for other terminals**

Run `/terminal-setup` within Claude Code to automatically configure Shift+Enter for VS Code, Alacritty, Zed, and Warp.

The `/terminal-setup` command is only visible in terminals that require manual configuration. If you’re using iTerm2, WezTerm, Ghostty, or Kitty, you won’t see this command because Shift+Enter already works natively.

**Set up Option+Enter (VS Code, iTerm2 or macOS Terminal.app)**

**For Mac Terminal.app:**

- Open Settings → Profiles → Keyboard

- Check “Use Option as Meta Key”

**For iTerm2 and VS Code terminal:**

- Open Settings → Profiles → Keys

- Under General, set Left/Right Option key to “Esc+“

### [​](#notification-setup)Notification setup

Never miss when Claude completes a task with proper notification configuration:

#### [​](#iterm-2-system-notifications)iTerm 2 system notifications

For iTerm 2 alerts when tasks complete:

- Open iTerm 2 Preferences

- Navigate to Profiles → Terminal

- Enable “Silence bell” and Filter Alerts → “Send escape sequence-generated alerts”

- Set your preferred notification delay

Note that these notifications are specific to iTerm 2 and not available in the default macOS Terminal.

#### [​](#custom-notification-hooks)Custom notification hooks

For advanced notification handling, you can create [notification hooks](/docs/en/hooks#notification) to run your own logic.

### [​](#handling-large-inputs)Handling large inputs

When working with extensive code or long instructions:

- **Avoid direct pasting**: Claude Code may struggle with very long pasted content

- **Use file-based workflows**: Write content to a file and ask Claude to read it

- **Be aware of VS Code limitations**: The VS Code terminal is particularly prone to truncating long pastes

### [​](#vim-mode)Vim Mode

Claude Code supports a subset of Vim keybindings that can be enabled with `/vim` or configured via `/config`.

The supported subset includes:

- Mode switching: `Esc` (to NORMAL), `i`/`I`, `a`/`A`, `o`/`O` (to INSERT)

- Navigation: `h`/`j`/`k`/`l`, `w`/`e`/`b`, `0`/`$`/`^`, `gg`/`G`, `f`/`F`/`t`/`T` with `;`/`,` repeat

- Editing: `x`, `dw`/`de`/`db`/`dd`/`D`, `cw`/`ce`/`cb`/`cc`/`C`, `.` (repeat)

- Yank/paste: `yy`/`Y`, `yw`/`ye`/`yb`, `p`/`P`

- Text objects: `iw`/`aw`, `iW`/`aW`, `i"`/`a"`, `i'`/`a'`, `i(`/`a(`, `i[`/`a[`, `i{`/`a{`

- Indentation: `>>`/`<<`

- Line operations: `J` (join lines)

See [Interactive mode](/docs/en/interactive-mode#vim-editor-mode) for the complete reference.Was this page helpful?YesNo[Sandboxing](/docs/en/sandboxing)[Model configuration](/docs/en/model-config)⌘I[Claude Code Docs home page](/docs)[x](https://x.com/AnthropicAI)[linkedin](https://www.linkedin.com/company/anthropicresearch)Company[Anthropic](https://www.anthropic.com/company)[Careers](https://www.anthropic.com/careers)[Economic Futures](https://www.anthropic.com/economic-futures)[Research](https://www.anthropic.com/research)[News](https://www.anthropic.com/news)[Trust center](https://trust.anthropic.com/)[Transparency](https://www.anthropic.com/transparency)Help and security[Availability](https://www.anthropic.com/supported-countries)[Status](https://status.anthropic.com/)[Support center](https://support.claude.com/)Learn[Courses](https://www.anthropic.com/learn)[MCP connectors](https://claude.com/partners/mcp)[Customer stories](https://www.claude.com/customers)[Engineering blog](https://www.anthropic.com/engineering)[Events](https://www.anthropic.com/events)[Powered by Claude](https://claude.com/partners/powered-by-claude)[Service partners](https://claude.com/partners/services)[Startups program](https://claude.com/programs/startups)Terms and policies[Privacy policy](https://www.anthropic.com/legal/privacy)[Disclosure policy](https://www.anthropic.com/responsible-disclosure-policy)[Usage policy](https://www.anthropic.com/legal/aup)[Commercial terms](https://www.anthropic.com/legal/commercial-terms)[Consumer terms](https://www.anthropic.com/legal/consumer-terms)