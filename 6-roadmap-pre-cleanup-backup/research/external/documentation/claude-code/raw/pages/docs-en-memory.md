---
{
  "fetch": {
    "url": "https://code.claude.com/docs/en/memory",
    "fetched_at": "2026-02-04T00:53:24.478374",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 646737
  },
  "metadata": {
    "title": "Manage Claude's memory",
    "section": "memory",
    "tier": 2,
    "type": "reference"
  }
}
---

- Manage Claude's memory - Claude Code Docs[Skip to main content](#content-area)[Claude Code Docs home page](/docs)EnglishSearch...⌘KAsk AI[Claude Developer Platform](https://platform.claude.com/)- [Claude Code on the Web](https://claude.ai/code)- [Claude Code on the Web](https://claude.ai/code)Search...NavigationConfigurationManage Claude's memory[Getting started](/docs/en/overview)[Build with Claude Code](/docs/en/sub-agents)[Deployment](/docs/en/third-party-integrations)[Administration](/docs/en/setup)[Configuration](/docs/en/settings)[Reference](/docs/en/cli-reference)[Resources](/docs/en/legal-and-compliance)Configuration- [Settings](/docs/en/settings)- [Permissions](/docs/en/permissions)- [Sandboxing](/docs/en/sandboxing)- [Terminal configuration](/docs/en/terminal-config)- [Model configuration](/docs/en/model-config)- [Memory management](/docs/en/memory)- [Status line configuration](/docs/en/statusline)- [Customize keyboard shortcuts](/docs/en/keybindings)On this page- [Determine memory type](#determine-memory-type)- [CLAUDE.md imports](#claude-md-imports)- [How Claude looks up memories](#how-claude-looks-up-memories)- [Load memory from additional directories](#load-memory-from-additional-directories)- [Directly edit memories with /memory](#directly-edit-memories-with-%2Fmemory)- [Set up project memory](#set-up-project-memory)- [Modular rules with .claude/rules/](#modular-rules-with-claude%2Frules%2F)- [Basic structure](#basic-structure)- [Path-specific rules](#path-specific-rules)- [Glob patterns](#glob-patterns)- [Subdirectories](#subdirectories)- [Symlinks](#symlinks)- [User-level rules](#user-level-rules)- [Organization-level memory management](#organization-level-memory-management)- [Memory best practices](#memory-best-practices)Configuration# Manage Claude's memoryCopy pageLearn how to manage Claude Code’s memory across sessions with different memory locations and best practices.Copy pageClaude Code can remember your preferences across sessions, like style guidelines and common commands in your workflow.

## [​](#determine-memory-type)Determine memory type

Claude Code offers four memory locations in a hierarchical structure, each serving a different purpose:

Memory TypeLocationPurposeUse Case ExamplesShared With**Managed policy**• macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`• Linux: `/etc/claude-code/CLAUDE.md`• Windows: `C:\Program Files\ClaudeCode\CLAUDE.md`Organization-wide instructions managed by IT/DevOpsCompany coding standards, security policies, compliance requirementsAll users in organization**Project memory**`./CLAUDE.md` or `./.claude/CLAUDE.md`Team-shared instructions for the projectProject architecture, coding standards, common workflowsTeam members via source control**Project rules**`./.claude/rules/*.md`Modular, topic-specific project instructionsLanguage-specific guidelines, testing conventions, API standardsTeam members via source control**User memory**`~/.claude/CLAUDE.md`Personal preferences for all projectsCode styling preferences, personal tooling shortcutsJust you (all projects)**Project memory (local)**`./CLAUDE.local.md`Personal project-specific preferencesYour sandbox URLs, preferred test dataJust you (current project)

All memory files are automatically loaded into Claude Code’s context when launched. Files higher in the hierarchy take precedence and are loaded first, providing a foundation that more specific memories build upon.

CLAUDE.local.md files are automatically added to .gitignore, making them ideal for private project-specific preferences that shouldn’t be checked into version control.

## [​](#claude-md-imports)CLAUDE.md imports

CLAUDE.md files can import additional files using `@path/to/import` syntax. The following example imports 3 files:

CopyAsk AI```

See @README for project overview and @package.json for available npm commands for this project.

# Additional Instructions

- git workflow @docs/git-instructions.md

```

Both relative and absolute paths are allowed. Relative paths resolve relative to the file containing the import, not the working directory. For private per-project preferences that shouldn’t be checked into version control, prefer `CLAUDE.local.md`: it is automatically loaded and added to `.gitignore`.

If you work across multiple git worktrees, `CLAUDE.local.md` only exists in one. Use a home-directory import instead so all worktrees share the same personal instructions:

CopyAsk AI```

# Individual Preferences

- @~/.claude/my-project-instructions.md

```

The first time Claude Code encounters external imports in a project, it shows an approval dialog listing the specific files. Approve to load them; decline to skip them. This is a one-time decision per project: once declined, the dialog does not resurface and the imports remain disabled.

To avoid potential collisions, imports are not evaluated inside markdown code spans and code blocks.

CopyAsk AI```

This code span will not be treated as an import: `@anthropic-ai/claude-code`

```

Imported files can recursively import additional files, with a max-depth of 5 hops. You can see what memory files are loaded by running `/memory` command.

## [​](#how-claude-looks-up-memories)How Claude looks up memories

Claude Code reads memories recursively: starting in the cwd, Claude Code recurses up to (but not including) the root directory */* and reads any CLAUDE.md or CLAUDE.local.md files it finds. This is especially convenient when working in large repositories where you run Claude Code in *foo/bar/*, and have memories in both *foo/CLAUDE.md* and *foo/bar/CLAUDE.md*.

Claude will also discover CLAUDE.md nested in subtrees under your current working directory. Instead of loading them at launch, they are only included when Claude reads files in those subtrees.

### [​](#load-memory-from-additional-directories)Load memory from additional directories

The `--add-dir` flag gives Claude access to additional directories outside your main working directory. By default, CLAUDE.md files from these directories are not loaded.

To also load memory files (CLAUDE.md, .claude/CLAUDE.md, and .claude/rules/*.md) from additional directories, set the `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` environment variable:

CopyAsk AI```

CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir ../shared-config

```

## [​](#directly-edit-memories-with-/memory)Directly edit memories with `/memory`

Use the `/memory` command during a session to open any memory file in your system editor for more extensive additions or organization.

## [​](#set-up-project-memory)Set up project memory

Suppose you want to set up a CLAUDE.md file to store important project information, conventions, and frequently used commands. Project memory can be stored in either `./CLAUDE.md` or `./.claude/CLAUDE.md`.

Bootstrap a CLAUDE.md for your codebase with the following command:

CopyAsk AI```

> /init

```

Tips:

- Include frequently used commands (build, test, lint) to avoid repeated searches

- Document code style preferences and naming conventions

- Add important architectural patterns specific to your project

- CLAUDE.md memories can be used for both instructions shared with your team and for your individual preferences.

## [​](#modular-rules-with-claude/rules/)Modular rules with `.claude/rules/`

For larger projects, you can organize instructions into multiple files using the `.claude/rules/` directory. This allows teams to maintain focused, well-organized rule files instead of one large CLAUDE.md.

### [​](#basic-structure)Basic structure

Place markdown files in your project’s `.claude/rules/` directory:

CopyAsk AI```

your-project/

├── .claude/

│   ├── CLAUDE.md           # Main project instructions

│   └── rules/

│       ├── code-style.md   # Code style guidelines

│       ├── testing.md      # Testing conventions

│       └── security.md     # Security requirements

```

All `.md` files in `.claude/rules/` are automatically loaded as project memory, with the same priority as `.claude/CLAUDE.md`.

### [​](#path-specific-rules)Path-specific rules

Rules can be scoped to specific files using YAML frontmatter with the `paths` field. These conditional rules only apply when Claude is working with files matching the specified patterns.

CopyAsk AI```

---

paths:

- "src/api/**/*.ts"

---

# API Development Rules

- All API endpoints must include input validation

- Use the standard error response format

- Include OpenAPI documentation comments

```

Rules without a `paths` field are loaded unconditionally and apply to all files.

### [​](#glob-patterns)Glob patterns

The `paths` field supports standard glob patterns:

PatternMatches`**/*.ts`All TypeScript files in any directory`src/**/*`All files under `src/` directory`*.md`Markdown files in the project root`src/components/*.tsx`React components in a specific directory

You can specify multiple patterns:

CopyAsk AI```

---

paths:

- "src/**/*.ts"

- "lib/**/*.ts"

- "tests/**/*.test.ts"

---

```

Brace expansion is supported for matching multiple extensions or directories:

CopyAsk AI```

---

paths:

- "src/**/*.{ts,tsx}"

- "{src,lib}/**/*.ts"

---

# TypeScript/React Rules

```

This expands `src/**/*.{ts,tsx}` to match both `.ts` and `.tsx` files.

### [​](#subdirectories)Subdirectories

Rules can be organized into subdirectories for better structure:

CopyAsk AI```

.claude/rules/

├── frontend/

│   ├── react.md

│   └── styles.md

├── backend/

│   ├── api.md

│   └── database.md

└── general.md

```

All `.md` files are discovered recursively.

### [​](#symlinks)Symlinks

The `.claude/rules/` directory supports symlinks, allowing you to share common rules across multiple projects:

CopyAsk AI```

# Symlink a shared rules directory

ln -s ~/shared-claude-rules .claude/rules/shared

# Symlink individual rule files

ln -s ~/company-standards/security.md .claude/rules/security.md

```

Symlinks are resolved and their contents are loaded normally. Circular symlinks are detected and handled gracefully.

### [​](#user-level-rules)User-level rules

You can create personal rules that apply to all your projects in `~/.claude/rules/`:

CopyAsk AI```

~/.claude/rules/

├── preferences.md    # Your personal coding preferences

└── workflows.md      # Your preferred workflows

```

User-level rules are loaded before project rules, giving project rules higher priority.

Best practices for `.claude/rules/`:

- **Keep rules focused**: Each file should cover one topic (e.g., `testing.md`, `api-design.md`)

- **Use descriptive filenames**: The filename should indicate what the rules cover

- **Use conditional rules sparingly**: Only add `paths` frontmatter when rules truly apply to specific file types

- **Organize with subdirectories**: Group related rules (e.g., `frontend/`, `backend/`)

## [​](#organization-level-memory-management)Organization-level memory management

Organizations can deploy centrally managed CLAUDE.md files that apply to all users.

To set up organization-level memory management:

-

Create the managed memory file at the **Managed policy** location shown in the [memory types table above](#determine-memory-type).

-

Deploy via your configuration management system (MDM, Group Policy, Ansible, etc.) to ensure consistent distribution across all developer machines.

## [​](#memory-best-practices)Memory best practices

- **Be specific**: “Use 2-space indentation” is better than “Format code properly”.

- **Use structure to organize**: Format each individual memory as a bullet point and group related memories under descriptive markdown headings.

- **Review periodically**: Update memories as your project evolves to ensure Claude is always using the most up to date information and context.

Was this page helpful?YesNo[Model configuration](/docs/en/model-config)[Status line configuration](/docs/en/statusline)⌘I[Claude Code Docs home page](/docs)[x](https://x.com/AnthropicAI)[linkedin](https://www.linkedin.com/company/anthropicresearch)Company[Anthropic](https://www.anthropic.com/company)[Careers](https://www.anthropic.com/careers)[Economic Futures](https://www.anthropic.com/economic-futures)[Research](https://www.anthropic.com/research)[News](https://www.anthropic.com/news)[Trust center](https://trust.anthropic.com/)[Transparency](https://www.anthropic.com/transparency)Help and security[Availability](https://www.anthropic.com/supported-countries)[Status](https://status.anthropic.com/)[Support center](https://support.claude.com/)Learn[Courses](https://www.anthropic.com/learn)[MCP connectors](https://claude.com/partners/mcp)[Customer stories](https://www.claude.com/customers)[Engineering blog](https://www.anthropic.com/engineering)[Events](https://www.anthropic.com/events)[Powered by Claude](https://claude.com/partners/powered-by-claude)[Service partners](https://claude.com/partners/services)[Startups program](https://claude.com/programs/startups)Terms and policies[Privacy policy](https://www.anthropic.com/legal/privacy)[Disclosure policy](https://www.anthropic.com/responsible-disclosure-policy)[Usage policy](https://www.anthropic.com/legal/aup)[Commercial terms](https://www.anthropic.com/legal/commercial-terms)[Consumer terms](https://www.anthropic.com/legal/consumer-terms)