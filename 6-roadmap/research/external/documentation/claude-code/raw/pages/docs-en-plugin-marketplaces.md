---
{
  "fetch": {
    "url": "https://code.claude.com/docs/en/plugin-marketplaces",
    "fetched_at": "2026-02-04T00:53:57.092971",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 1117623
  },
  "metadata": {
    "title": "Create and distribute a plugin marketplace",
    "section": "plugin-marketplaces",
    "tier": 3,
    "type": "reference"
  }
}
---

- Create and distribute a plugin marketplace - Claude Code Docs[Skip to main content](#content-area)[Claude Code Docs home page](/docs)EnglishSearch...⌘KAsk AI[Claude Developer Platform](https://platform.claude.com/)- [Claude Code on the Web](https://claude.ai/code)- [Claude Code on the Web](https://claude.ai/code)Search...NavigationAdministrationCreate and distribute a plugin marketplace[Getting started](/docs/en/overview)[Build with Claude Code](/docs/en/sub-agents)[Deployment](/docs/en/third-party-integrations)[Administration](/docs/en/setup)[Configuration](/docs/en/settings)[Reference](/docs/en/cli-reference)[Resources](/docs/en/legal-and-compliance)Administration- [Advanced installation](/docs/en/setup)- [Authentication](/docs/en/authentication)- [Security](/docs/en/security)- [Data usage](/docs/en/data-usage)- [Monitoring](/docs/en/monitoring-usage)- [Costs](/docs/en/costs)- [Track team usage with analytics](/docs/en/analytics)- [Create and distribute a plugin marketplace](/docs/en/plugin-marketplaces)On this page- [Overview](#overview)- [Walkthrough: create a local marketplace](#walkthrough%3A-create-a-local-marketplace)- [Create the marketplace file](#create-the-marketplace-file)- [Marketplace schema](#marketplace-schema)- [Required fields](#required-fields)- [Owner fields](#owner-fields)- [Optional metadata](#optional-metadata)- [Plugin entries](#plugin-entries)- [Required fields](#required-fields-2)- [Optional plugin fields](#optional-plugin-fields)- [Plugin sources](#plugin-sources)- [Relative paths](#relative-paths)- [GitHub repositories](#github-repositories)- [Git repositories](#git-repositories)- [Advanced plugin entries](#advanced-plugin-entries)- [Host and distribute marketplaces](#host-and-distribute-marketplaces)- [Host on GitHub (recommended)](#host-on-github-recommended)- [Host on other git services](#host-on-other-git-services)- [Private repositories](#private-repositories)- [Test locally before distribution](#test-locally-before-distribution)- [Require marketplaces for your team](#require-marketplaces-for-your-team)- [Managed marketplace restrictions](#managed-marketplace-restrictions)- [Common configurations](#common-configurations)- [How restrictions work](#how-restrictions-work)- [Validation and testing](#validation-and-testing)- [Troubleshooting](#troubleshooting)- [Marketplace not loading](#marketplace-not-loading)- [Marketplace validation errors](#marketplace-validation-errors)- [Plugin installation failures](#plugin-installation-failures)- [Private repository authentication fails](#private-repository-authentication-fails)- [Plugins with relative paths fail in URL-based marketplaces](#plugins-with-relative-paths-fail-in-url-based-marketplaces)- [Files not found after installation](#files-not-found-after-installation)- [See also](#see-also)Administration# Create and distribute a plugin marketplaceCopy pageBuild and host plugin marketplaces to distribute Claude Code extensions across teams and communities.Copy pageA plugin marketplace is a catalog that lets you distribute plugins to others. Marketplaces provide centralized discovery, version tracking, automatic updates, and support for multiple source types (git repositories, local paths, and more). This guide shows you how to create your own marketplace to share plugins with your team or community.

Looking to install plugins from an existing marketplace? See [Discover and install prebuilt plugins](/docs/en/discover-plugins).

## [​](#overview)Overview

Creating and distributing a marketplace involves:

- **Creating plugins**: build one or more plugins with commands, agents, hooks, MCP servers, or LSP servers. This guide assumes you already have plugins to distribute; see [Create plugins](/docs/en/plugins) for details on how to create them.

- **Creating a marketplace file**: define a `marketplace.json` that lists your plugins and where to find them (see [Create the marketplace file](#create-the-marketplace-file)).

- **Host the marketplace**: push to GitHub, GitLab, or another git host (see [Host and distribute marketplaces](#host-and-distribute-marketplaces)).

- **Share with users**: users add your marketplace with `/plugin marketplace add` and install individual plugins (see [Discover and install plugins](/docs/en/discover-plugins)).

Once your marketplace is live, you can update it by pushing changes to your repository. Users refresh their local copy with `/plugin marketplace update`.

## [​](#walkthrough:-create-a-local-marketplace)Walkthrough: create a local marketplace

This example creates a marketplace with one plugin: a `/review` skill for code reviews. You’ll create the directory structure, add a skill, create the plugin manifest and marketplace catalog, then install and test it.

1[](#)Create the directory structureCopyAsk AI```

mkdir -p my-marketplace/.claude-plugin

mkdir -p my-marketplace/plugins/review-plugin/.claude-plugin

mkdir -p my-marketplace/plugins/review-plugin/skills/review

```2[](#)Create the skillCreate a `SKILL.md` file that defines what the `/review` skill does.my-marketplace/plugins/review-plugin/skills/review/SKILL.mdCopyAsk AI```

---

description: Review code for bugs, security, and performance

disable-model-invocation: true

---

Review the code I've selected or the recent changes for:

- Potential bugs or edge cases

- Security concerns

- Performance issues

- Readability improvements

Be concise and actionable.

```3[](#)Create the plugin manifestCreate a `plugin.json` file that describes the plugin. The manifest goes in the `.claude-plugin/` directory.my-marketplace/plugins/review-plugin/.claude-plugin/plugin.jsonCopyAsk AI```

{

"name": "review-plugin",

"description": "Adds a /review skill for quick code reviews",

"version": "1.0.0"

}

```4[](#)Create the marketplace fileCreate the marketplace catalog that lists your plugin.my-marketplace/.claude-plugin/marketplace.jsonCopyAsk AI```

{

"name": "my-plugins",

"owner": {

"name": "Your Name"

},

"plugins": [

{

"name": "review-plugin",

"source": "./plugins/review-plugin",

"description": "Adds a /review skill for quick code reviews"

}

]

}

```5[](#)Add and installAdd the marketplace and install the plugin.CopyAsk AI```

/plugin marketplace add ./my-marketplace

/plugin install review-plugin@my-plugins

```6[](#)Try it outSelect some code in your editor and run your new command.CopyAsk AI```

/review

```

To learn more about what plugins can do, including hooks, agents, MCP servers, and LSP servers, see [Plugins](/docs/en/plugins).

**How plugins are installed**: When users install a plugin, Claude Code copies the plugin directory to a cache location. This means plugins can’t reference files outside their directory using paths like `../shared-utils`, because those files won’t be copied.If you need to share files across plugins, use symlinks (which are followed during copying) or restructure your marketplace so the shared directory is inside the plugin source path. See [Plugin caching and file resolution](/docs/en/plugins-reference#plugin-caching-and-file-resolution) for details.

## [​](#create-the-marketplace-file)Create the marketplace file

Create `.claude-plugin/marketplace.json` in your repository root. This file defines your marketplace’s name, owner information, and a list of plugins with their sources.

Each plugin entry needs at minimum a `name` and `source` (where to fetch it from). See the [full schema](#marketplace-schema) below for all available fields.

CopyAsk AI```

{

"name": "company-tools",

"owner": {

"name": "DevTools Team",

"email": "[[email protected]](/cdn-cgi/l/email-protection)"

},

"plugins": [

{

"name": "code-formatter",

"source": "./plugins/formatter",

"description": "Automatic code formatting on save",

"version": "2.1.0",

"author": {

"name": "DevTools Team"

}

},

{

"name": "deployment-tools",

"source": {

"source": "github",

"repo": "company/deploy-plugin"

},

"description": "Deployment automation tools"

}

]

}

```

## [​](#marketplace-schema)Marketplace schema

### [​](#required-fields)Required fields

FieldTypeDescriptionExample`name`stringMarketplace identifier (kebab-case, no spaces). This is public-facing: users see it when installing plugins (for example, `/plugin install my-tool@your-marketplace`).`"acme-tools"``owner`objectMarketplace maintainer information ([see fields below](#owner-fields))`plugins`arrayList of available pluginsSee below

**Reserved names**: The following marketplace names are reserved for official Anthropic use and cannot be used by third-party marketplaces: `claude-code-marketplace`, `claude-code-plugins`, `claude-plugins-official`, `anthropic-marketplace`, `anthropic-plugins`, `agent-skills`, `life-sciences`. Names that impersonate official marketplaces (like `official-claude-plugins` or `anthropic-tools-v2`) are also blocked.

### [​](#owner-fields)Owner fields

FieldTypeRequiredDescription`name`stringYesName of the maintainer or team`email`stringNoContact email for the maintainer

### [​](#optional-metadata)Optional metadata

FieldTypeDescription`metadata.description`stringBrief marketplace description`metadata.version`stringMarketplace version`metadata.pluginRoot`stringBase directory prepended to relative plugin source paths (for example, `"./plugins"` lets you write `"source": "formatter"` instead of `"source": "./plugins/formatter"`)

## [​](#plugin-entries)Plugin entries

Each plugin entry in the `plugins` array describes a plugin and where to find it. You can include any field from the [plugin manifest schema](/docs/en/plugins-reference#plugin-manifest-schema) (like `description`, `version`, `author`, `commands`, `hooks`, etc.), plus these marketplace-specific fields: `source`, `category`, `tags`, and `strict`.

### [​](#required-fields-2)Required fields

FieldTypeDescription`name`stringPlugin identifier (kebab-case, no spaces). This is public-facing: users see it when installing (for example, `/plugin install my-plugin@marketplace`).`source`string|objectWhere to fetch the plugin from (see [Plugin sources](#plugin-sources) below)

### [​](#optional-plugin-fields)Optional plugin fields

**Standard metadata fields:**

FieldTypeDescription`description`stringBrief plugin description`version`stringPlugin version`author`objectPlugin author information (`name` required, `email` optional)`homepage`stringPlugin homepage or documentation URL`repository`stringSource code repository URL`license`stringSPDX license identifier (for example, MIT, Apache-2.0)`keywords`arrayTags for plugin discovery and categorization`category`stringPlugin category for organization`tags`arrayTags for searchability`strict`booleanControls whether plugins need their own `plugin.json` file. When `true` (default), the plugin source must contain a `plugin.json`, and any fields you add here in the marketplace entry get merged with it. When `false`, the plugin doesn’t need its own `plugin.json`; the marketplace entry itself defines everything about the plugin. Use `false` when you want to define simple plugins entirely in your marketplace file.

**Component configuration fields:**

FieldTypeDescription`commands`string|arrayCustom paths to command files or directories`agents`string|arrayCustom paths to agent files`hooks`string|objectCustom hooks configuration or path to hooks file`mcpServers`string|objectMCP server configurations or path to MCP config`lspServers`string|objectLSP server configurations or path to LSP config

## [​](#plugin-sources)Plugin sources

### [​](#relative-paths)Relative paths

For plugins in the same repository:

CopyAsk AI```

{

"name": "my-plugin",

"source": "./plugins/my-plugin"

}

```

Relative paths only work when users add your marketplace via Git (GitHub, GitLab, or git URL). If users add your marketplace via a direct URL to the `marketplace.json` file, relative paths will not resolve correctly. For URL-based distribution, use GitHub, npm, or git URL sources instead. See [Troubleshooting](#plugins-with-relative-paths-fail-in-url-based-marketplaces) for details.

### [​](#github-repositories)GitHub repositories

CopyAsk AI```

{

"name": "github-plugin",

"source": {

"source": "github",

"repo": "owner/plugin-repo"

}

}

```

You can pin to a specific branch, tag, or commit:

CopyAsk AI```

{

"name": "github-plugin",

"source": {

"source": "github",

"repo": "owner/plugin-repo",

"ref": "v2.0.0",

"sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"

}

}

```

FieldTypeDescription`repo`stringRequired. GitHub repository in `owner/repo` format`ref`stringOptional. Git branch or tag (defaults to repository default branch)`sha`stringOptional. Full 40-character git commit SHA to pin to an exact version

### [​](#git-repositories)Git repositories

CopyAsk AI```

{

"name": "git-plugin",

"source": {

"source": "url",

"url": "https://gitlab.com/team/plugin.git"

}

}

```

You can pin to a specific branch, tag, or commit:

CopyAsk AI```

{

"name": "git-plugin",

"source": {

"source": "url",

"url": "https://gitlab.com/team/plugin.git",

"ref": "main",

"sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"

}

}

```

FieldTypeDescription`url`stringRequired. Full git repository URL (must end with `.git`)`ref`stringOptional. Git branch or tag (defaults to repository default branch)`sha`stringOptional. Full 40-character git commit SHA to pin to an exact version

### [​](#advanced-plugin-entries)Advanced plugin entries

This example shows a plugin entry using many of the optional fields, including custom paths for commands, agents, hooks, and MCP servers:

CopyAsk AI```

{

"name": "enterprise-tools",

"source": {

"source": "github",

"repo": "company/enterprise-plugin"

},

"description": "Enterprise workflow automation tools",

"version": "2.1.0",

"author": {

"name": "Enterprise Team",

"email": "[[email protected]](/cdn-cgi/l/email-protection)"

},

"homepage": "https://docs.example.com/plugins/enterprise-tools",

"repository": "https://github.com/company/enterprise-plugin",

"license": "MIT",

"keywords": ["enterprise", "workflow", "automation"],

"category": "productivity",

"commands": [

"./commands/core/",

"./commands/enterprise/",

"./commands/experimental/preview.md"

],

"agents": ["./agents/security-reviewer.md", "./agents/compliance-checker.md"],

"hooks": {

"PostToolUse": [

{

"matcher": "Write|Edit",

"hooks": [

{

"type": "command",

"command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"

}

]

}

]

},

"mcpServers": {

"enterprise-db": {

"command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",

"args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]

}

},

"strict": false

}

```

Key things to notice:

- **`commands` and `agents`**: You can specify multiple directories or individual files. Paths are relative to the plugin root.

- **`${CLAUDE_PLUGIN_ROOT}`**: Use this variable in hooks and MCP server configs to reference files within the plugin’s installation directory. This is necessary because plugins are copied to a cache location when installed.

- **`strict: false`**: Since this is set to false, the plugin doesn’t need its own `plugin.json`. The marketplace entry defines everything.

## [​](#host-and-distribute-marketplaces)Host and distribute marketplaces

### [​](#host-on-github-recommended)Host on GitHub (recommended)

GitHub provides the easiest distribution method:

- **Create a repository**: Set up a new repository for your marketplace

- **Add marketplace file**: Create `.claude-plugin/marketplace.json` with your plugin definitions

- **Share with teams**: Users add your marketplace with `/plugin marketplace add owner/repo`

**Benefits**: Built-in version control, issue tracking, and team collaboration features.

### [​](#host-on-other-git-services)Host on other git services

Any git hosting service works, such as GitLab, Bitbucket, and self-hosted servers. Users add with the full repository URL:

CopyAsk AI```

/plugin marketplace add https://gitlab.com/company/plugins.git

```

### [​](#private-repositories)Private repositories

Claude Code supports installing plugins from private repositories. For manual installation and updates, Claude Code uses your existing git credential helpers. If `git clone` works for a private repository in your terminal, it works in Claude Code too. Common credential helpers include `gh auth login` for GitHub, macOS Keychain, and `git-credential-store`.

Background auto-updates run at startup without credential helpers, since interactive prompts would block Claude Code from starting. To enable auto-updates for private marketplaces, set the appropriate authentication token in your environment:

ProviderEnvironment variablesNotesGitHub`GITHUB_TOKEN` or `GH_TOKEN`Personal access token or GitHub App tokenGitLab`GITLAB_TOKEN` or `GL_TOKEN`Personal access token or project tokenBitbucket`BITBUCKET_TOKEN`App password or repository access token

Set the token in your shell configuration (for example, `.bashrc`, `.zshrc`) or pass it when running Claude Code:

CopyAsk AI```

export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx

```

For CI/CD environments, configure the token as a secret environment variable. GitHub Actions automatically provides `GITHUB_TOKEN` for repositories in the same organization.

### [​](#test-locally-before-distribution)Test locally before distribution

Test your marketplace locally before sharing:

CopyAsk AI```

/plugin marketplace add ./my-local-marketplace

/plugin install test-plugin@my-local-marketplace

```

For the full range of add commands (GitHub, Git URLs, local paths, remote URLs), see [Add marketplaces](/docs/en/discover-plugins#add-marketplaces).

### [​](#require-marketplaces-for-your-team)Require marketplaces for your team

You can configure your repository so team members are automatically prompted to install your marketplace when they trust the project folder. Add your marketplace to `.claude/settings.json`:

CopyAsk AI```

{

"extraKnownMarketplaces": {

"company-tools": {

"source": {

"source": "github",

"repo": "your-org/claude-plugins"

}

}

}

}

```

You can also specify which plugins should be enabled by default:

CopyAsk AI```

{

"enabledPlugins": {

"code-formatter@company-tools": true,

"deployment-tools@company-tools": true

}

}

```

For full configuration options, see [Plugin settings](/docs/en/settings#plugin-settings).

### [​](#managed-marketplace-restrictions)Managed marketplace restrictions

For organizations requiring strict control over plugin sources, administrators can restrict which plugin marketplaces users are allowed to add using the [`strictKnownMarketplaces`](/docs/en/settings#strictknownmarketplaces) setting in managed settings.

When `strictKnownMarketplaces` is configured in managed settings, the restriction behavior depends on the value:

ValueBehaviorUndefined (default)No restrictions. Users can add any marketplaceEmpty array `[]`Complete lockdown. Users cannot add any new marketplacesList of sourcesUsers can only add marketplaces that match the allowlist exactly

#### [​](#common-configurations)Common configurations

Disable all marketplace additions:

CopyAsk AI```

{

"strictKnownMarketplaces": []

}

```

Allow specific marketplaces only:

CopyAsk AI```

{

"strictKnownMarketplaces": [

{

"source": "github",

"repo": "acme-corp/approved-plugins"

},

{

"source": "github",

"repo": "acme-corp/security-tools",

"ref": "v2.0"

},

{

"source": "url",

"url": "https://plugins.example.com/marketplace.json"

}

]

}

```

Allow all marketplaces from an internal git server using regex pattern matching:

CopyAsk AI```

{

"strictKnownMarketplaces": [

{

"source": "hostPattern",

"hostPattern": "^github\\.example\\.com$"

}

]

}

```

#### [​](#how-restrictions-work)How restrictions work

Restrictions are validated early in the plugin installation process, before any network requests or filesystem operations occur. This prevents unauthorized marketplace access attempts.

The allowlist uses exact matching for most source types. For a marketplace to be allowed, all specified fields must match exactly:

- For GitHub sources: `repo` is required, and `ref` or `path` must also match if specified in the allowlist

- For URL sources: the full URL must match exactly

- For `hostPattern` sources: the marketplace host is matched against the regex pattern

Because `strictKnownMarketplaces` is set in [managed settings](/docs/en/settings#settings-files), individual users and project configurations cannot override these restrictions.

For complete configuration details including all supported source types and comparison with `extraKnownMarketplaces`, see the [strictKnownMarketplaces reference](/docs/en/settings#strictknownmarketplaces).

## [​](#validation-and-testing)Validation and testing

Test your marketplace before sharing.

Validate your marketplace JSON syntax:

CopyAsk AI```

claude plugin validate .

```

Or from within Claude Code:

CopyAsk AI```

/plugin validate .

```

Add the marketplace for testing:

CopyAsk AI```

/plugin marketplace add ./path/to/marketplace

```

Install a test plugin to verify everything works:

CopyAsk AI```

/plugin install test-plugin@marketplace-name

```

For complete plugin testing workflows, see [Test your plugins locally](/docs/en/plugins#test-your-plugins-locally). For technical troubleshooting, see [Plugins reference](/docs/en/plugins-reference).

## [​](#troubleshooting)Troubleshooting

### [​](#marketplace-not-loading)Marketplace not loading

**Symptoms**: Can’t add marketplace or see plugins from it

**Solutions**:

- Verify the marketplace URL is accessible

- Check that `.claude-plugin/marketplace.json` exists at the specified path

- Ensure JSON syntax is valid using `claude plugin validate` or `/plugin validate`

- For private repositories, confirm you have access permissions

### [​](#marketplace-validation-errors)Marketplace validation errors

Run `claude plugin validate .` or `/plugin validate .` from your marketplace directory to check for issues. Common errors:

ErrorCauseSolution`File not found: .claude-plugin/marketplace.json`Missing manifestCreate `.claude-plugin/marketplace.json` with required fields`Invalid JSON syntax: Unexpected token...`JSON syntax errorCheck for missing commas, extra commas, or unquoted strings`Duplicate plugin name "x" found in marketplace`Two plugins share the same nameGive each plugin a unique `name` value`plugins[0].source: Path traversal not allowed`Source path contains `..`Use paths relative to marketplace root without `..`

**Warnings** (non-blocking):

- `Marketplace has no plugins defined`: add at least one plugin to the `plugins` array

- `No marketplace description provided`: add `metadata.description` to help users understand your marketplace

- `Plugin "x" uses npm source which is not yet fully implemented`: use `github` or local path sources instead

### [​](#plugin-installation-failures)Plugin installation failures

**Symptoms**: Marketplace appears but plugin installation fails

**Solutions**:

- Verify plugin source URLs are accessible

- Check that plugin directories contain required files

- For GitHub sources, ensure repositories are public or you have access

- Test plugin sources manually by cloning/downloading

### [​](#private-repository-authentication-fails)Private repository authentication fails

**Symptoms**: Authentication errors when installing plugins from private repositories

**Solutions**:

For manual installation and updates:

- Verify you’re authenticated with your git provider (for example, run `gh auth status` for GitHub)

- Check that your credential helper is configured correctly: `git config --global credential.helper`

- Try cloning the repository manually to verify your credentials work

For background auto-updates:

- Set the appropriate token in your environment: `echo $GITHUB_TOKEN`

- Check that the token has the required permissions (read access to the repository)

- For GitHub, ensure the token has the `repo` scope for private repositories

- For GitLab, ensure the token has at least `read_repository` scope

- Verify the token hasn’t expired

### [​](#plugins-with-relative-paths-fail-in-url-based-marketplaces)Plugins with relative paths fail in URL-based marketplaces

**Symptoms**: Added a marketplace via URL (such as `https://example.com/marketplace.json`), but plugins with relative path sources like `"./plugins/my-plugin"` fail to install with “path not found” errors.

**Cause**: URL-based marketplaces only download the `marketplace.json` file itself. They do not download plugin files from the server. Relative paths in the marketplace entry reference files on the remote server that were not downloaded.

**Solutions**:

- **Use external sources**: Change plugin entries to use GitHub, npm, or git URL sources instead of relative paths:

CopyAsk AI```

{ "name": "my-plugin", "source": { "source": "github", "repo": "owner/repo" } }

```

- **Use a Git-based marketplace**: Host your marketplace in a Git repository and add it with the git URL. Git-based marketplaces clone the entire repository, making relative paths work correctly.

### [​](#files-not-found-after-installation)Files not found after installation

**Symptoms**: Plugin installs but references to files fail, especially files outside the plugin directory

**Cause**: Plugins are copied to a cache directory rather than used in-place. Paths that reference files outside the plugin’s directory (such as `../shared-utils`) won’t work because those files aren’t copied.

**Solutions**: See [Plugin caching and file resolution](/docs/en/plugins-reference#plugin-caching-and-file-resolution) for workarounds including symlinks and directory restructuring.

For additional debugging tools and common issues, see [Debugging and development tools](/docs/en/plugins-reference#debugging-and-development-tools).

## [​](#see-also)See also

- [Discover and install prebuilt plugins](/docs/en/discover-plugins) - Installing plugins from existing marketplaces

- [Plugins](/docs/en/plugins) - Creating your own plugins

- [Plugins reference](/docs/en/plugins-reference) - Complete technical specifications and schemas

- [Plugin settings](/docs/en/settings#plugin-settings) - Plugin configuration options

- [strictKnownMarketplaces reference](/docs/en/settings#strictknownmarketplaces) - Managed marketplace restrictions

Was this page helpful?YesNo[Track team usage with analytics](/docs/en/analytics)⌘I[Claude Code Docs home page](/docs)[x](https://x.com/AnthropicAI)[linkedin](https://www.linkedin.com/company/anthropicresearch)Company[Anthropic](https://www.anthropic.com/company)[Careers](https://www.anthropic.com/careers)[Economic Futures](https://www.anthropic.com/economic-futures)[Research](https://www.anthropic.com/research)[News](https://www.anthropic.com/news)[Trust center](https://trust.anthropic.com/)[Transparency](https://www.anthropic.com/transparency)Help and security[Availability](https://www.anthropic.com/supported-countries)[Status](https://status.anthropic.com/)[Support center](https://support.claude.com/)Learn[Courses](https://www.anthropic.com/learn)[MCP connectors](https://claude.com/partners/mcp)[Customer stories](https://www.claude.com/customers)[Engineering blog](https://www.anthropic.com/engineering)[Events](https://www.anthropic.com/events)[Powered by Claude](https://claude.com/partners/powered-by-claude)[Service partners](https://claude.com/partners/services)[Startups program](https://claude.com/programs/startups)Terms and policies[Privacy policy](https://www.anthropic.com/legal/privacy)[Disclosure policy](https://www.anthropic.com/responsible-disclosure-policy)[Usage policy](https://www.anthropic.com/legal/aup)[Commercial terms](https://www.anthropic.com/legal/commercial-terms)[Consumer terms](https://www.anthropic.com/legal/consumer-terms)