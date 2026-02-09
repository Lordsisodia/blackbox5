---
{
  "fetch": {
    "url": "https://code.claude.com/docs/en/chrome",
    "fetched_at": "2026-02-04T00:53:06.992123",
    "status": 200,
    "content_type": "text/html; charset=utf-8",
    "size_bytes": 612136
  },
  "metadata": {
    "title": "Use Claude Code with Chrome (beta)",
    "section": "chrome",
    "tier": 2,
    "type": "reference"
  }
}
---

- Use Claude Code with Chrome (beta) - Claude Code Docs[Skip to main content](#content-area)[Claude Code Docs home page](/docs)EnglishSearch...⌘KAsk AI[Claude Developer Platform](https://platform.claude.com/)- [Claude Code on the Web](https://claude.ai/code)- [Claude Code on the Web](https://claude.ai/code)Search...NavigationOutside of the terminalUse Claude Code with Chrome (beta)[Getting started](/docs/en/overview)[Build with Claude Code](/docs/en/sub-agents)[Deployment](/docs/en/third-party-integrations)[Administration](/docs/en/setup)[Configuration](/docs/en/settings)[Reference](/docs/en/cli-reference)[Resources](/docs/en/legal-and-compliance)Getting started- [Overview](/docs/en/overview)- [Quickstart](/docs/en/quickstart)- [Changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)Core concepts- [How Claude Code works](/docs/en/how-claude-code-works)- [Extend Claude Code](/docs/en/features-overview)- [Common workflows](/docs/en/common-workflows)- [Best practices](/docs/en/best-practices)Outside of the terminal- [Claude Code on the web](/docs/en/claude-code-on-the-web)- [Claude Code on desktop](/docs/en/desktop)- [Chrome extension (beta)](/docs/en/chrome)- [Visual Studio Code](/docs/en/vs-code)- [JetBrains IDEs](/docs/en/jetbrains)- [GitHub Actions](/docs/en/github-actions)- [GitLab CI/CD](/docs/en/gitlab-ci-cd)- [Claude Code in Slack](/docs/en/slack)On this page- [What the integration enables](#what-the-integration-enables)- [Prerequisites](#prerequisites)- [How the integration works](#how-the-integration-works)- [Set up the integration](#set-up-the-integration)- [Try it out](#try-it-out)- [Example workflows](#example-workflows)- [Test a local web application](#test-a-local-web-application)- [Debug with console logs](#debug-with-console-logs)- [Automate form filling](#automate-form-filling)- [Draft content in Google Docs](#draft-content-in-google-docs)- [Extract data from web pages](#extract-data-from-web-pages)- [Run multi-site workflows](#run-multi-site-workflows)- [Record a demo GIF](#record-a-demo-gif)- [Best practices](#best-practices)- [Troubleshooting](#troubleshooting)- [Extension not detected](#extension-not-detected)- [Browser not responding](#browser-not-responding)- [First-time setup](#first-time-setup)- [Enable by default](#enable-by-default)- [See also](#see-also)Outside of the terminal# Use Claude Code with Chrome (beta)Copy pageConnect Claude Code to your browser to test web apps, debug with console logs, and automate browser tasks.Copy pageChrome integration is in beta and currently works with Google Chrome only. It is not yet supported on Brave, Arc, or other Chromium-based browsers. WSL (Windows Subsystem for Linux) is also not supported.

Claude Code integrates with the Claude in Chrome browser extension to give you browser automation capabilities directly from your terminal. Build in your terminal, then test and debug in your browser without switching contexts.

## [​](#what-the-integration-enables)What the integration enables

With Chrome connected, you can chain browser actions with terminal commands in a single workflow. For example: scrape documentation from a website, analyze it, generate code based on what you learned, and commit the result.

Key capabilities include:

- **Live debugging**: Claude reads console errors and DOM state directly, then fixes the code that caused them

- **Design verification**: Build a UI from a Figma mock, then have Claude open it in the browser and verify it matches

- **Web app testing**: Test form validation, check for visual regressions, or verify user flows work correctly

- **Authenticated web apps**: Interact with Google Docs, Gmail, Notion, or any app you’re logged into without needing API connectors

- **Data extraction**: Pull structured information from web pages and save it locally

- **Task automation**: Automate repetitive browser tasks like data entry, form filling, or multi-site workflows

- **Session recording**: Record browser interactions as GIFs to document or share what happened

## [​](#prerequisites)Prerequisites

Before using Claude Code with Chrome, you need:

- [Google Chrome](https://www.google.com/chrome/) browser

- [Claude in Chrome extension](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) version 1.0.36 or higher

- [Claude Code CLI](/docs/en/quickstart#step-1-install-claude-code) version 2.0.73 or higher

- A paid Claude plan (Pro, Team, or Enterprise)

## [​](#how-the-integration-works)How the integration works

Claude Code communicates with Chrome through the Claude in Chrome browser extension. The extension uses Chrome’s [Native Messaging API](https://developer.chrome.com/docs/extensions/develop/concepts/native-messaging) to receive commands from Claude Code and execute them in your browser. This architecture lets Claude Code control browser tabs, read page content, and perform actions while you continue working in your terminal.

When Claude encounters a login page, CAPTCHA, or other blocker, it pauses and asks you to handle it. You can provide credentials for Claude to enter, or log in manually in the browser. Once you’re past the blocker, tell Claude to continue and it picks up where it left off.

Claude opens new tabs for browser tasks rather than taking over existing ones. However, it shares your browser’s login state, so if you’re already signed into a site in Chrome, Claude can access it without re-authenticating.

The Chrome integration requires a visible browser window. When Claude performs browser actions, you’ll see Chrome open and navigate in real time. There’s no headless mode since the integration relies on your actual browser session with its login state.

## [​](#set-up-the-integration)Set up the integration

1[](#)Update Claude CodeChrome integration requires a recent version of Claude Code. If you installed using the [native installer](/docs/en/quickstart#step-1-install-claude-code), updates happen automatically. Otherwise, run:CopyAsk AI```

claude update

```2[](#)Start Claude Code with Chrome enabledLaunch Claude Code with the `--chrome` flag:CopyAsk AI```

claude --chrome

```3[](#)Verify the connectionRun `/chrome` to check the connection status and manage settings. If the extension isn’t detected, you’ll see a warning with a link to install it.

You can also enable Chrome integration from within an existing session using the `/chrome` command.

## [​](#try-it-out)Try it out

Once connected, type this into Claude to see the integration in action:

CopyAsk AI```

Go to code.claude.com/docs, click on the search box,

type "hooks", and tell me what results appear

```

Claude opens the page, clicks into the search field, types the query, and reports the autocomplete results. This shows navigation, clicking, and typing in a single workflow.

## [​](#example-workflows)Example workflows

Claude can navigate pages, click and type, fill forms, scroll, read console logs and network requests, manage tabs, resize windows, and record GIFs. Run `/mcp` and click into `claude-in-chrome` to see the full list of available tools.

The following examples show common patterns for browser automation.

### [​](#test-a-local-web-application)Test a local web application

When developing a web app, ask Claude to verify your changes work correctly:

CopyAsk AI```

I just updated the login form validation. Can you open localhost:3000,

try submitting the form with invalid data, and check if the error

messages appear correctly?

```

Claude navigates to your local server, interacts with the form, and reports what it observes.

### [​](#debug-with-console-logs)Debug with console logs

If your app has issues, Claude can read console output to help diagnose problems:

CopyAsk AI```

Open the dashboard page and check the console for any errors when

the page loads.

```

Claude reads the console messages and can filter for specific patterns or error types.

### [​](#automate-form-filling)Automate form filling

Speed up repetitive data entry tasks:

CopyAsk AI```

I have a spreadsheet of customer contacts in contacts.csv. For each row,

go to our CRM at crm.example.com, click "Add Contact", and fill in the

name, email, and phone fields.

```

Claude reads your local file, navigates the web interface, and enters the data for each record.

### [​](#draft-content-in-google-docs)Draft content in Google Docs

Use Claude to write directly in your documents without API setup:

CopyAsk AI```

Draft a project update based on our recent commits and add it to my

Google Doc at docs.google.com/document/d/abc123

```

Claude opens the document, clicks into the editor, and types the content. This works with any web app you’re logged into: Gmail, Notion, Sheets, and more.

### [​](#extract-data-from-web-pages)Extract data from web pages

Pull structured information from websites:

CopyAsk AI```

Go to the product listings page and extract the name, price, and

availability for each item. Save the results as a CSV file.

```

Claude navigates to the page, reads the content, and compiles the data into a structured format.

### [​](#run-multi-site-workflows)Run multi-site workflows

Coordinate tasks across multiple websites:

CopyAsk AI```

Check my calendar for meetings tomorrow, then for each meeting with

an external attendee, look up their company on LinkedIn and add a

note about what they do.

```

Claude works across tabs to gather information and complete the workflow.

### [​](#record-a-demo-gif)Record a demo GIF

Create shareable recordings of browser interactions:

CopyAsk AI```

Record a GIF showing how to complete the checkout flow, from adding

an item to the cart through to the confirmation page.

```

Claude records the interaction sequence and saves it as a GIF file.

## [​](#best-practices)Best practices

When using browser automation, keep these guidelines in mind:

- **Modal dialogs can interrupt the flow**: JavaScript alerts, confirms, and prompts block browser events and prevent Claude from receiving commands. If a dialog appears, dismiss it manually and tell Claude to continue.

- **Use fresh tabs**: Claude creates new tabs for each session. If a tab becomes unresponsive, ask Claude to create a new one.

- **Filter console output**: Console logs can be verbose. When debugging, tell Claude what patterns to look for rather than asking for all console output.

## [​](#troubleshooting)Troubleshooting

### [​](#extension-not-detected)Extension not detected

If Claude Code shows “Chrome extension not detected”:

- Verify the Chrome extension (version 1.0.36 or higher) is installed

- Verify Claude Code is version 2.0.73 or higher by running `claude --version`

- Check that Chrome is running

- Run `/chrome` and select “Reconnect extension” to re-establish the connection

- If the issue persists, restart both Claude Code and Chrome

### [​](#browser-not-responding)Browser not responding

If Claude’s browser commands stop working:

- Check if a modal dialog (alert, confirm, prompt) is blocking the page

- Ask Claude to create a new tab and try again

- Restart the Chrome extension by disabling and re-enabling it

### [​](#first-time-setup)First-time setup

The first time you use the integration, Claude Code installs a native messaging host that allows communication between the CLI and Chrome. If you encounter permission errors, you may need to restart Chrome for the installation to take effect.

## [​](#enable-by-default)Enable by default

Chrome integration requires the `--chrome` flag each time you start Claude Code. To enable it by default, run `/chrome` and select “Enabled by default”.

Enabling Chrome by default increases context usage since browser tools are always loaded. If you notice increased context consumption, disable this setting and use `--chrome` only when needed.

Site-level permissions are inherited from the Chrome extension. Manage permissions in the Chrome extension settings to control which sites Claude can browse, click, and type on. Run `/chrome` to see current permission settings.

## [​](#see-also)See also

- [CLI reference](/docs/en/cli-reference) - Command-line flags including `--chrome`

- [Common workflows](/docs/en/common-workflows) - More ways to use Claude Code

- [Getting started with Claude for Chrome](https://support.anthropic.com/en/articles/12012173-getting-started-with-claude-for-chrome) - Full documentation for the Chrome extension, including shortcuts, scheduling, and permissions

Was this page helpful?YesNo[Claude Code on desktop](/docs/en/desktop)[Visual Studio Code](/docs/en/vs-code)⌘I[Claude Code Docs home page](/docs)[x](https://x.com/AnthropicAI)[linkedin](https://www.linkedin.com/company/anthropicresearch)Company[Anthropic](https://www.anthropic.com/company)[Careers](https://www.anthropic.com/careers)[Economic Futures](https://www.anthropic.com/economic-futures)[Research](https://www.anthropic.com/research)[News](https://www.anthropic.com/news)[Trust center](https://trust.anthropic.com/)[Transparency](https://www.anthropic.com/transparency)Help and security[Availability](https://www.anthropic.com/supported-countries)[Status](https://status.anthropic.com/)[Support center](https://support.claude.com/)Learn[Courses](https://www.anthropic.com/learn)[MCP connectors](https://claude.com/partners/mcp)[Customer stories](https://www.claude.com/customers)[Engineering blog](https://www.anthropic.com/engineering)[Events](https://www.anthropic.com/events)[Powered by Claude](https://claude.com/partners/powered-by-claude)[Service partners](https://claude.com/partners/services)[Startups program](https://claude.com/programs/startups)Terms and policies[Privacy policy](https://www.anthropic.com/legal/privacy)[Disclosure policy](https://www.anthropic.com/responsible-disclosure-policy)[Usage policy](https://www.anthropic.com/legal/aup)[Commercial terms](https://www.anthropic.com/legal/commercial-terms)[Consumer terms](https://www.anthropic.com/legal/consumer-terms)