---
{
  "fetch": {
    "url": "https://code.claude.com/docs/en/checkpointing",
    "fetched_at": "2026-02-04T00:53:35.929876",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 491831
  },
  "metadata": {
    "title": "Checkpointing",
    "section": "checkpointing",
    "tier": 3,
    "type": "reference"
  }
}
---

- Checkpointing - Claude Code Docs[Skip to main content](#content-area)[Claude Code Docs home page](/docs)EnglishSearch...⌘KAsk AI[Claude Developer Platform](https://platform.claude.com/)- [Claude Code on the Web](https://claude.ai/code)- [Claude Code on the Web](https://claude.ai/code)Search...NavigationReferenceCheckpointing[Getting started](/docs/en/overview)[Build with Claude Code](/docs/en/sub-agents)[Deployment](/docs/en/third-party-integrations)[Administration](/docs/en/setup)[Configuration](/docs/en/settings)[Reference](/docs/en/cli-reference)[Resources](/docs/en/legal-and-compliance)Reference- [CLI reference](/docs/en/cli-reference)- [Interactive mode](/docs/en/interactive-mode)- [Checkpointing](/docs/en/checkpointing)- [Hooks reference](/docs/en/hooks)- [Plugins reference](/docs/en/plugins-reference)On this page- [How checkpoints work](#how-checkpoints-work)- [Automatic tracking](#automatic-tracking)- [Rewinding changes](#rewinding-changes)- [Common use cases](#common-use-cases)- [Limitations](#limitations)- [Bash command changes not tracked](#bash-command-changes-not-tracked)- [External changes not tracked](#external-changes-not-tracked)- [Not a replacement for version control](#not-a-replacement-for-version-control)- [See also](#see-also)Reference# CheckpointingCopy pageAutomatically track and rewind Claude’s edits to quickly recover from unwanted changes.Copy pageClaude Code automatically tracks Claude’s file edits as you work, allowing you to quickly undo changes and rewind to previous states if anything gets off track.

## [​](#how-checkpoints-work)How checkpoints work

As you work with Claude, checkpointing automatically captures the state of your code before each edit. This safety net lets you pursue ambitious, wide-scale tasks knowing you can always return to a prior code state.

### [​](#automatic-tracking)Automatic tracking

Claude Code tracks all changes made by its file editing tools:

- Every user prompt creates a new checkpoint

- Checkpoints persist across sessions, so you can access them in resumed conversations

- Automatically cleaned up along with sessions after 30 days (configurable)

### [​](#rewinding-changes)Rewinding changes

Press `Esc` twice (`Esc` + `Esc`) or use the `/rewind` command to open up the rewind menu. You can choose to restore:

- **Conversation only**: Rewind to a user message while keeping code changes

- **Code only**: Revert file changes while keeping the conversation

- **Both code and conversation**: Restore both to a prior point in the session

## [​](#common-use-cases)Common use cases

Checkpoints are particularly useful when:

- **Exploring alternatives**: Try different implementation approaches without losing your starting point

- **Recovering from mistakes**: Quickly undo changes that introduced bugs or broke functionality

- **Iterating on features**: Experiment with variations knowing you can revert to working states

## [​](#limitations)Limitations

### [​](#bash-command-changes-not-tracked)Bash command changes not tracked

Checkpointing does not track files modified by bash commands. For example, if Claude Code runs:

CopyAsk AI```

rm file.txt

mv old.txt new.txt

cp source.txt dest.txt

```

These file modifications cannot be undone through rewind. Only direct file edits made through Claude’s file editing tools are tracked.

### [​](#external-changes-not-tracked)External changes not tracked

Checkpointing only tracks files that have been edited within the current session. Manual changes you make to files outside of Claude Code and edits from other concurrent sessions are normally not captured, unless they happen to modify the same files as the current session.

### [​](#not-a-replacement-for-version-control)Not a replacement for version control

Checkpoints are designed for quick, session-level recovery. For permanent version history and collaboration:

- Continue using version control (ex. Git) for commits, branches, and long-term history

- Checkpoints complement but don’t replace proper version control

- Think of checkpoints as “local undo” and Git as “permanent history”

## [​](#see-also)See also

- [Interactive mode](/docs/en/interactive-mode) - Keyboard shortcuts and session controls

- [Built-in commands](/docs/en/interactive-mode#built-in-commands) - Accessing checkpoints using `/rewind`

- [CLI reference](/docs/en/cli-reference) - Command-line options

Was this page helpful?YesNo[Interactive mode](/docs/en/interactive-mode)[Hooks reference](/docs/en/hooks)⌘I[Claude Code Docs home page](/docs)[x](https://x.com/AnthropicAI)[linkedin](https://www.linkedin.com/company/anthropicresearch)Company[Anthropic](https://www.anthropic.com/company)[Careers](https://www.anthropic.com/careers)[Economic Futures](https://www.anthropic.com/economic-futures)[Research](https://www.anthropic.com/research)[News](https://www.anthropic.com/news)[Trust center](https://trust.anthropic.com/)[Transparency](https://www.anthropic.com/transparency)Help and security[Availability](https://www.anthropic.com/supported-countries)[Status](https://status.anthropic.com/)[Support center](https://support.claude.com/)Learn[Courses](https://www.anthropic.com/learn)[MCP connectors](https://claude.com/partners/mcp)[Customer stories](https://www.claude.com/customers)[Engineering blog](https://www.anthropic.com/engineering)[Events](https://www.anthropic.com/events)[Powered by Claude](https://claude.com/partners/powered-by-claude)[Service partners](https://claude.com/partners/services)[Startups program](https://claude.com/programs/startups)Terms and policies[Privacy policy](https://www.anthropic.com/legal/privacy)[Disclosure policy](https://www.anthropic.com/responsible-disclosure-policy)[Usage policy](https://www.anthropic.com/legal/aup)[Commercial terms](https://www.anthropic.com/legal/commercial-terms)[Consumer terms](https://www.anthropic.com/legal/consumer-terms)