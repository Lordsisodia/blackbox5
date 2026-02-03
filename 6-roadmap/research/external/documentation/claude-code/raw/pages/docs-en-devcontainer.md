---
{
  "fetch": {
    "url": "https://code.claude.com/docs/en/devcontainer",
    "fetched_at": "2026-02-04T00:53:39.730131",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 494046
  },
  "metadata": {
    "title": "Development containers",
    "section": "devcontainer",
    "tier": 3,
    "type": "reference"
  }
}
---

- Development containers - Claude Code Docs[Skip to main content](#content-area)[Claude Code Docs home page](/docs)EnglishSearch...⌘KAsk AI[Claude Developer Platform](https://platform.claude.com/)- [Claude Code on the Web](https://claude.ai/code)- [Claude Code on the Web](https://claude.ai/code)Search...NavigationDeploymentDevelopment containers[Getting started](/docs/en/overview)[Build with Claude Code](/docs/en/sub-agents)[Deployment](/docs/en/third-party-integrations)[Administration](/docs/en/setup)[Configuration](/docs/en/settings)[Reference](/docs/en/cli-reference)[Resources](/docs/en/legal-and-compliance)Deployment- [Overview](/docs/en/third-party-integrations)- [Amazon Bedrock](/docs/en/amazon-bedrock)- [Google Vertex AI](/docs/en/google-vertex-ai)- [Microsoft Foundry](/docs/en/microsoft-foundry)- [Network configuration](/docs/en/network-config)- [LLM gateway](/docs/en/llm-gateway)- [Development containers](/docs/en/devcontainer)On this page- [Key features](#key-features)- [Getting started in 4 steps](#getting-started-in-4-steps)- [Configuration breakdown](#configuration-breakdown)- [Security features](#security-features)- [Customization options](#customization-options)- [Example use cases](#example-use-cases)- [Secure client work](#secure-client-work)- [Team onboarding](#team-onboarding)- [Consistent CI/CD environments](#consistent-ci%2Fcd-environments)- [Related resources](#related-resources)Deployment# Development containersCopy pageLearn about the Claude Code development container for teams that need consistent, secure environments.Copy pageThe reference [devcontainer setup](https://github.com/anthropics/claude-code/tree/main/.devcontainer) and associated [Dockerfile](https://github.com/anthropics/claude-code/blob/main/.devcontainer/Dockerfile) offer a preconfigured development container that you can use as is, or customize for your needs. This devcontainer works with the Visual Studio Code [Dev Containers extension](https://code.visualstudio.com/docs/devcontainers/containers) and similar tools.

The container’s enhanced security measures (isolation and firewall rules) allow you to run `claude --dangerously-skip-permissions` to bypass permission prompts for unattended operation.

While the devcontainer provides substantial protections, no system is completely immune to all attacks.

When executed with `--dangerously-skip-permissions`, devcontainers don’t prevent a malicious project from exfiltrating anything accessible in the devcontainer including Claude Code credentials.

We recommend only using devcontainers when developing with trusted repositories.

Always maintain good security practices and monitor Claude’s activities.

## [​](#key-features)Key features

- **Production-ready Node.js**: Built on Node.js 20 with essential development dependencies

- **Security by design**: Custom firewall restricting network access to only necessary services

- **Developer-friendly tools**: Includes git, ZSH with productivity enhancements, fzf, and more

- **Seamless VS Code integration**: Pre-configured extensions and optimized settings

- **Session persistence**: Preserves command history and configurations between container restarts

- **Works everywhere**: Compatible with macOS, Windows, and Linux development environments

## [​](#getting-started-in-4-steps)Getting started in 4 steps

- Install VS Code and the Remote - Containers extension

- Clone the [Claude Code reference implementation](https://github.com/anthropics/claude-code/tree/main/.devcontainer) repository

- Open the repository in VS Code

- When prompted, click “Reopen in Container” (or use Command Palette: Cmd+Shift+P → “Remote-Containers: Reopen in Container”)

## [​](#configuration-breakdown)Configuration breakdown

The devcontainer setup consists of three primary components:

- [**devcontainer.json**](https://github.com/anthropics/claude-code/blob/main/.devcontainer/devcontainer.json): Controls container settings, extensions, and volume mounts

- [**Dockerfile**](https://github.com/anthropics/claude-code/blob/main/.devcontainer/Dockerfile): Defines the container image and installed tools

- [**init-firewall.sh**](https://github.com/anthropics/claude-code/blob/main/.devcontainer/init-firewall.sh): Establishes network security rules

## [​](#security-features)Security features

The container implements a multi-layered security approach with its firewall configuration:

- **Precise access control**: Restricts outbound connections to whitelisted domains only (npm registry, GitHub, Claude API, etc.)

- **Allowed outbound connections**: The firewall permits outbound DNS and SSH connections

- **Default-deny policy**: Blocks all other external network access

- **Startup verification**: Validates firewall rules when the container initializes

- **Isolation**: Creates a secure development environment separated from your main system

## [​](#customization-options)Customization options

The devcontainer configuration is designed to be adaptable to your needs:

- Add or remove VS Code extensions based on your workflow

- Modify resource allocations for different hardware environments

- Adjust network access permissions

- Customize shell configurations and developer tooling

## [​](#example-use-cases)Example use cases

### [​](#secure-client-work)Secure client work

Use devcontainers to isolate different client projects, ensuring code and credentials never mix between environments.

### [​](#team-onboarding)Team onboarding

New team members can get a fully configured development environment in minutes, with all necessary tools and settings pre-installed.

### [​](#consistent-ci/cd-environments)Consistent CI/CD environments

Mirror your devcontainer configuration in CI/CD pipelines to ensure development and production environments match.

## [​](#related-resources)Related resources

- [VS Code devcontainers documentation](https://code.visualstudio.com/docs/devcontainers/containers)

- [Claude Code security best practices](/docs/en/security)

- [Enterprise network configuration](/docs/en/network-config)

Was this page helpful?YesNo[LLM gateway](/docs/en/llm-gateway)⌘I[Claude Code Docs home page](/docs)[x](https://x.com/AnthropicAI)[linkedin](https://www.linkedin.com/company/anthropicresearch)Company[Anthropic](https://www.anthropic.com/company)[Careers](https://www.anthropic.com/careers)[Economic Futures](https://www.anthropic.com/economic-futures)[Research](https://www.anthropic.com/research)[News](https://www.anthropic.com/news)[Trust center](https://trust.anthropic.com/)[Transparency](https://www.anthropic.com/transparency)Help and security[Availability](https://www.anthropic.com/supported-countries)[Status](https://status.anthropic.com/)[Support center](https://support.claude.com/)Learn[Courses](https://www.anthropic.com/learn)[MCP connectors](https://claude.com/partners/mcp)[Customer stories](https://www.claude.com/customers)[Engineering blog](https://www.anthropic.com/engineering)[Events](https://www.anthropic.com/events)[Powered by Claude](https://claude.com/partners/powered-by-claude)[Service partners](https://claude.com/partners/services)[Startups program](https://claude.com/programs/startups)Terms and policies[Privacy policy](https://www.anthropic.com/legal/privacy)[Disclosure policy](https://www.anthropic.com/responsible-disclosure-policy)[Usage policy](https://www.anthropic.com/legal/aup)[Commercial terms](https://www.anthropic.com/legal/commercial-terms)[Consumer terms](https://www.anthropic.com/legal/consumer-terms)