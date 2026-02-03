---
{
  "fetch": {
    "url": "https://code.claude.com/docs/en/keybindings",
    "fetched_at": "2026-02-04T00:53:46.931351",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 760239
  },
  "metadata": {
    "title": "Customize keyboard shortcuts",
    "section": "keybindings",
    "tier": 3,
    "type": "reference"
  }
}
---

- Customize keyboard shortcuts - Claude Code Docs[Skip to main content](#content-area)[Claude Code Docs home page](/docs)EnglishSearch...⌘KAsk AI[Claude Developer Platform](https://platform.claude.com/)- [Claude Code on the Web](https://claude.ai/code)- [Claude Code on the Web](https://claude.ai/code)Search...NavigationConfigurationCustomize keyboard shortcuts[Getting started](/docs/en/overview)[Build with Claude Code](/docs/en/sub-agents)[Deployment](/docs/en/third-party-integrations)[Administration](/docs/en/setup)[Configuration](/docs/en/settings)[Reference](/docs/en/cli-reference)[Resources](/docs/en/legal-and-compliance)Configuration- [Settings](/docs/en/settings)- [Permissions](/docs/en/permissions)- [Sandboxing](/docs/en/sandboxing)- [Terminal configuration](/docs/en/terminal-config)- [Model configuration](/docs/en/model-config)- [Memory management](/docs/en/memory)- [Status line configuration](/docs/en/statusline)- [Customize keyboard shortcuts](/docs/en/keybindings)On this page- [Configuration file](#configuration-file)- [Contexts](#contexts)- [Available actions](#available-actions)- [App actions](#app-actions)- [History actions](#history-actions)- [Chat actions](#chat-actions)- [Autocomplete actions](#autocomplete-actions)- [Confirmation actions](#confirmation-actions)- [Permission actions](#permission-actions)- [Transcript actions](#transcript-actions)- [History search actions](#history-search-actions)- [Task actions](#task-actions)- [Theme actions](#theme-actions)- [Help actions](#help-actions)- [Tabs actions](#tabs-actions)- [Attachments actions](#attachments-actions)- [Footer actions](#footer-actions)- [Message selector actions](#message-selector-actions)- [Diff actions](#diff-actions)- [Model picker actions](#model-picker-actions)- [Select actions](#select-actions)- [Plugin actions](#plugin-actions)- [Settings actions](#settings-actions)- [Keystroke syntax](#keystroke-syntax)- [Modifiers](#modifiers)- [Uppercase letters](#uppercase-letters)- [Chords](#chords)- [Special keys](#special-keys)- [Unbind default shortcuts](#unbind-default-shortcuts)- [Reserved shortcuts](#reserved-shortcuts)- [Terminal conflicts](#terminal-conflicts)- [Vim mode interaction](#vim-mode-interaction)- [Validation](#validation)Configuration# Customize keyboard shortcutsCopy pageCustomize keyboard shortcuts in Claude Code with a keybindings configuration file.Copy pageClaude Code supports customizable keyboard shortcuts. Run `/keybindings` to create or open your configuration file at `~/.claude/keybindings.json`.

## [​](#configuration-file)Configuration file

The keybindings configuration file is an object with a `bindings` array. Each block specifies a context and a map of keystrokes to actions.

Changes to the keybindings file are automatically detected and applied without restarting Claude Code.

FieldDescription`$schema`Optional JSON Schema URL for editor autocompletion`$docs`Optional documentation URL`bindings`Array of binding blocks by context

This example binds `Ctrl+E` to open an external editor in the chat context, and unbinds `Ctrl+U`:

CopyAsk AI```

{

"$schema": "https://www.schemastore.org/claude-code-keybindings.json",

"$docs": "https://code.claude.com/docs/en/keybindings",

"bindings": [

{

"context": "Chat",

"bindings": {

"ctrl+e": "chat:externalEditor",

"ctrl+u": null

}

}

]

}

```

## [​](#contexts)Contexts

Each binding block specifies a **context** where the bindings apply:

ContextDescription`Global`Applies everywhere in the app`Chat`Main chat input area`Autocomplete`Autocomplete menu is open`Settings`Settings menu (escape-only dismiss)`Confirmation`Permission and confirmation dialogs`Tabs`Tab navigation components`Help`Help menu is visible`Transcript`Transcript viewer`HistorySearch`History search mode (Ctrl+R)`Task`Background task is running`ThemePicker`Theme picker dialog`Attachments`Image/attachment bar navigation`Footer`Footer indicator navigation (tasks, teams, diff)`MessageSelector`Rewind dialog message selection`DiffDialog`Diff viewer navigation`ModelPicker`Model picker effort level`Select`Generic select/list components`Plugin`Plugin dialog (browse, discover, manage)

## [​](#available-actions)Available actions

Actions follow a `namespace:action` format, such as `chat:submit` to send a message or `app:toggleTodos` to show the task list. Each context has specific actions available.

### [​](#app-actions)App actions

Actions available in the `Global` context:

ActionDefaultDescription`app:interrupt`Ctrl+CCancel current operation`app:exit`Ctrl+DExit Claude Code`app:toggleTodos`Ctrl+TToggle task list visibility`app:toggleTranscript`Ctrl+OToggle verbose transcript

### [​](#history-actions)History actions

Actions for navigating command history:

ActionDefaultDescription`history:search`Ctrl+ROpen history search`history:previous`UpPrevious history item`history:next`DownNext history item

### [​](#chat-actions)Chat actions

Actions available in the `Chat` context:

ActionDefaultDescription`chat:cancel`EscapeCancel current input`chat:cycleMode`Shift+Tab*Cycle permission modes`chat:modelPicker`Cmd+P / Meta+POpen model picker`chat:thinkingToggle`Cmd+T / Meta+TToggle extended thinking`chat:submit`EnterSubmit message`chat:undo`Ctrl+_Undo last action`chat:externalEditor`Ctrl+GOpen in external editor`chat:stash`Ctrl+SStash current prompt`chat:imagePaste`Ctrl+V (Alt+V on Windows)Paste image

*On Windows without VT mode (Node <24.2.0/<22.17.0, Bun <1.2.23), defaults to Meta+M.

### [​](#autocomplete-actions)Autocomplete actions

Actions available in the `Autocomplete` context:

ActionDefaultDescription`autocomplete:accept`TabAccept suggestion`autocomplete:dismiss`EscapeDismiss menu`autocomplete:previous`UpPrevious suggestion`autocomplete:next`DownNext suggestion

### [​](#confirmation-actions)Confirmation actions

Actions available in the `Confirmation` context:

ActionDefaultDescription`confirm:yes`Y, EnterConfirm action`confirm:no`N, EscapeDecline action`confirm:previous`UpPrevious option`confirm:next`DownNext option`confirm:nextField`TabNext field`confirm:previousField`(unbound)Previous field`confirm:cycleMode`Shift+TabCycle permission modes`confirm:toggleExplanation`Ctrl+EToggle permission explanation

### [​](#permission-actions)Permission actions

Actions available in the `Confirmation` context for permission dialogs:

ActionDefaultDescription`permission:toggleDebug`Ctrl+DToggle permission debug info

### [​](#transcript-actions)Transcript actions

Actions available in the `Transcript` context:

ActionDefaultDescription`transcript:toggleShowAll`Ctrl+EToggle show all content`transcript:exit`Ctrl+C, EscapeExit transcript view

### [​](#history-search-actions)History search actions

Actions available in the `HistorySearch` context:

ActionDefaultDescription`historySearch:next`Ctrl+RNext match`historySearch:accept`Escape, TabAccept selection`historySearch:cancel`Ctrl+CCancel search`historySearch:execute`EnterExecute selected command

### [​](#task-actions)Task actions

Actions available in the `Task` context:

ActionDefaultDescription`task:background`Ctrl+BBackground current task

### [​](#theme-actions)Theme actions

Actions available in the `ThemePicker` context:

ActionDefaultDescription`theme:toggleSyntaxHighlighting`Ctrl+TToggle syntax highlighting

### [​](#help-actions)Help actions

Actions available in the `Help` context:

ActionDefaultDescription`help:dismiss`EscapeClose help menu

### [​](#tabs-actions)Tabs actions

Actions available in the `Tabs` context:

ActionDefaultDescription`tabs:next`Tab, RightNext tab`tabs:previous`Shift+Tab, LeftPrevious tab

### [​](#attachments-actions)Attachments actions

Actions available in the `Attachments` context:

ActionDefaultDescription`attachments:next`RightNext attachment`attachments:previous`LeftPrevious attachment`attachments:remove`Backspace, DeleteRemove selected attachment`attachments:exit`Down, EscapeExit attachment bar

### [​](#footer-actions)Footer actions

Actions available in the `Footer` context:

ActionDefaultDescription`footer:next`RightNext footer item`footer:previous`LeftPrevious footer item`footer:openSelected`EnterOpen selected footer item`footer:clearSelection`EscapeClear footer selection

### [​](#message-selector-actions)Message selector actions

Actions available in the `MessageSelector` context:

ActionDefaultDescription`messageSelector:up`Up, KMove up in list`messageSelector:down`Down, JMove down in list`messageSelector:top`Ctrl+Up, Shift+Up, Meta+Up, Shift+KJump to top`messageSelector:bottom`Ctrl+Down, Shift+Down, Meta+Down, Shift+JJump to bottom`messageSelector:select`EnterSelect message

### [​](#diff-actions)Diff actions

Actions available in the `DiffDialog` context:

ActionDefaultDescription`diff:dismiss`EscapeClose diff viewer`diff:previousSource`LeftPrevious diff source`diff:nextSource`RightNext diff source`diff:previousFile`UpPrevious file in diff`diff:nextFile`DownNext file in diff`diff:viewDetails`EnterView diff details`diff:back`(context-specific)Go back in diff viewer

### [​](#model-picker-actions)Model picker actions

Actions available in the `ModelPicker` context:

ActionDefaultDescription`modelPicker:decreaseEffort`LeftDecrease effort level`modelPicker:increaseEffort`RightIncrease effort level

### [​](#select-actions)Select actions

Actions available in the `Select` context:

ActionDefaultDescription`select:next`Down, J, Ctrl+NNext option`select:previous`Up, K, Ctrl+PPrevious option`select:accept`EnterAccept selection`select:cancel`EscapeCancel selection

### [​](#plugin-actions)Plugin actions

Actions available in the `Plugin` context:

ActionDefaultDescription`plugin:toggle`SpaceToggle plugin selection`plugin:install`IInstall selected plugins

### [​](#settings-actions)Settings actions

Actions available in the `Settings` context:

ActionDefaultDescription`settings:search`/Enter search mode`settings:retry`RRetry loading usage data (on error)

## [​](#keystroke-syntax)Keystroke syntax

### [​](#modifiers)Modifiers

Use modifier keys with the `+` separator:

- `ctrl` or `control` - Control key

- `alt`, `opt`, or `option` - Alt/Option key

- `shift` - Shift key

- `meta`, `cmd`, or `command` - Meta/Command key

For example:

CopyAsk AI```

ctrl+k          Single key with modifier

shift+tab       Shift + Tab

meta+p          Command/Meta + P

ctrl+shift+c    Multiple modifiers

```

### [​](#uppercase-letters)Uppercase letters

A standalone uppercase letter implies Shift. For example, `K` is equivalent to `shift+k`. This is useful for vim-style bindings where uppercase and lowercase keys have different meanings.

Uppercase letters with modifiers (e.g., `ctrl+K`) are treated as stylistic and do **not** imply Shift — `ctrl+K` is the same as `ctrl+k`.

### [​](#chords)Chords

Chords are sequences of keystrokes separated by spaces:

CopyAsk AI```

ctrl+k ctrl+s   Press Ctrl+K, release, then Ctrl+S

```

### [​](#special-keys)Special keys

- `escape` or `esc` - Escape key

- `enter` or `return` - Enter key

- `tab` - Tab key

- `space` - Space bar

- `up`, `down`, `left`, `right` - Arrow keys

- `backspace`, `delete` - Delete keys

## [​](#unbind-default-shortcuts)Unbind default shortcuts

Set an action to `null` to unbind a default shortcut:

CopyAsk AI```

{

"bindings": [

{

"context": "Chat",

"bindings": {

"ctrl+s": null

}

}

]

}

```

## [​](#reserved-shortcuts)Reserved shortcuts

These shortcuts cannot be rebound:

ShortcutReasonCtrl+CHardcoded interrupt/cancelCtrl+DHardcoded exit

## [​](#terminal-conflicts)Terminal conflicts

Some shortcuts may conflict with terminal multiplexers:

ShortcutConflictCtrl+Btmux prefix (press twice to send)Ctrl+AGNU screen prefixCtrl+ZUnix process suspend (SIGTSTP)

## [​](#vim-mode-interaction)Vim mode interaction

When vim mode is enabled (`/vim`), keybindings and vim mode operate independently:

- **Vim mode** handles input at the text input level (cursor movement, modes, motions)

- **Keybindings** handle actions at the component level (toggle todos, submit, etc.)

- The Escape key in vim mode switches INSERT to NORMAL mode; it does not trigger `chat:cancel`

- Most Ctrl+key shortcuts pass through vim mode to the keybinding system

- In vim NORMAL mode, `?` shows the help menu (vim behavior)

## [​](#validation)Validation

Claude Code validates your keybindings and shows warnings for:

- Parse errors (invalid JSON or structure)

- Invalid context names

- Reserved shortcut conflicts

- Terminal multiplexer conflicts

- Duplicate bindings in the same context

Run `/doctor` to see any keybinding warnings.Was this page helpful?YesNo[Status line configuration](/docs/en/statusline)⌘I[Claude Code Docs home page](/docs)[x](https://x.com/AnthropicAI)[linkedin](https://www.linkedin.com/company/anthropicresearch)Company[Anthropic](https://www.anthropic.com/company)[Careers](https://www.anthropic.com/careers)[Economic Futures](https://www.anthropic.com/economic-futures)[Research](https://www.anthropic.com/research)[News](https://www.anthropic.com/news)[Trust center](https://trust.anthropic.com/)[Transparency](https://www.anthropic.com/transparency)Help and security[Availability](https://www.anthropic.com/supported-countries)[Status](https://status.anthropic.com/)[Support center](https://support.claude.com/)Learn[Courses](https://www.anthropic.com/learn)[MCP connectors](https://claude.com/partners/mcp)[Customer stories](https://www.claude.com/customers)[Engineering blog](https://www.anthropic.com/engineering)[Events](https://www.anthropic.com/events)[Powered by Claude](https://claude.com/partners/powered-by-claude)[Service partners](https://claude.com/partners/services)[Startups program](https://claude.com/programs/startups)Terms and policies[Privacy policy](https://www.anthropic.com/legal/privacy)[Disclosure policy](https://www.anthropic.com/responsible-disclosure-policy)[Usage policy](https://www.anthropic.com/legal/aup)[Commercial terms](https://www.anthropic.com/legal/commercial-terms)[Consumer terms](https://www.anthropic.com/legal/consumer-terms)