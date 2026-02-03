---
video_id: XuSFUvUdvQA
title: "Anthropic's 7 Hour Claude Code Course in 27 Minutes"
creator: David Ondrej
creator_tier: 1
url: https://youtube.com/watch?v=XuSFUvUdvQA
published_at: 2026-01-20
duration: 1662
view_count: 24756
topics:
  - claude_code
  - ai_agents
  - coding_tools
  - mcp_servers
  - automation
overall_importance: critical
tools_mentioned:
  - Claude Code
  - n8n
  - Playwright
  - GitHub
  - Hostinger VPS
  - Cursor
  - VS Code
  - AgentZero
  - Jupyter Notebook
  - Bash/Terminal
frameworks:
  - MCP (Model Context Protocol)
  - CI/CD pipelines
  - Agent SDK
difficulty: beginner
extracted_at: 2026-02-02
---

# [CRITICAL] Anthropic's 7 Hour Claude Code Course in 27 Minutes

**Creator:** David Ondrej
**Video:** [https://youtube.com/watch?v=XuSFUvUdvQA](https://youtube.com/watch?v=XuSFUvUdvQA)
**Published:** 2026-01-20
**Overall Importance:** CRITICAL

## Course Overview

This video is a condensed summary of Anthropic's official 7-hour Claude Code course, distilled into 27 minutes by David Ondrej, who has spent over 500 hours using Claude Code. The course is organized into four sections: what is a coding assistant, why Claude Code, how to work with Claude Code as your partner, and how to get the most out of Claude Code. Each section builds on the previous one, providing a comprehensive understanding of Claude Code's capabilities and best practices.

## Key Concepts from the Course

### [CRITICAL] What is a Coding Assistant?
A coding assistant is not just a tool that writes code - it is a language model with access to a set of tools that follows a three-step loop:
1. **Gather context** - Read files, understand the codebase
2. **Formulate a plan** - Reason about the task
3. **Take action** - Edit files, run commands

**Why it matters:** Understanding this loop helps you work more effectively with Claude Code. The assistant cannot gather context or take actions just by thinking - it needs tools to interact with the environment.

**Key insight:** To have a strong coding assistant, you need both a powerful language model AND powerful tools. Claude Code has built-in tools including:
- Agent (launch sub-agents)
- Bash (run shell commands)
- Edit (edit files)
- And many more

### [CRITICAL] Claude Code Installation and Setup

**Installation:**
```bash
# Copy command from anthropic.com/cloud
# Paste in terminal
curl -sSL https://claude.ai/install | sh
```

**Launch:**
```bash
claude
```

**Why it matters:** Claude Code runs entirely in the terminal - no IDE or fancy UI needed. You can type in plain English, making it accessible to non-developers.

**Best practice:** Run Claude Code in a specific project folder using `cd /path/to/project` before launching. This prevents Claude from modifying files in other directories.

### [CRITICAL] The `/init` Command
The `/init` command analyzes your entire codebase and creates a `claude.md` file that acts as the system prompt for Claude Code.

**What it includes:**
- Summary of architecture
- Key files
- Conventions
- Environment variables
- Project-specific context

**Why it matters:** The `claude.md` file is included in every request, so Claude always knows what project it's working with. This is especially important for existing codebases.

**Usage:**
```
/init
```

### [HIGH] Context Engineering with `@` and `#`

**Using `@` to add files to context:**
- `@schema.prisma` - Include the database schema
- `@package.json` - Include package dependencies
- `@filename` - Include any specific file

**Using `#` for memories (DEPRECATED):**
The `#` convention for creating memories has been replaced with the `/memory` command.

**Current approach:**
```
/memory
```
This opens project memory or user memory where you can add persistent instructions.

**Pro tip:** Mention critical files in your `claude.md` so every Claude Code instance is aware of them (e.g., external documentation, Supabase schema files).

### [CRITICAL] MCP Servers (Model Context Protocol)
MCP servers extend Claude Code's capabilities by adding new tools.

**Examples:**
- **Playwright MCP** - Control browser, navigate, click, screenshot, test UI
- **n8n MCP** - Access up-to-date documentation for n8n nodes, build automations

**Why it matters:** MCP servers transform Claude Code from a coding assistant into a multi-tool agent that can interact with external systems, databases, APIs, and more.

**Real-world example:** With n8n MCP, Claude built a complete automation from a single plain English prompt:
> "Build me a full n8n automation for analyzing the user's calendar and creating a separate Google doc for every sales call that is booked there, matching the data from the leads in the user's Airtable."

Result: A 329-line JSON file with the complete n8n automation that could be imported directly.

### [HIGH] Plan Mode vs. Thinking Mode

**Plan Mode (Shift+Tab to toggle):**
- Handles **breadth**
- Researches more files
- Puts more effort into reasoning and planning
- Does NOT touch anything - only plans

**Thinking Mode (DEPRECATED):**
- Previously handled **depth** with four levels: think, think hard, think harder, ultra think
- **OUTDATED:** As of recent updates, thinking budget is always maxed by default
- You no longer need to add "ultra think" to prompts

**Current behavior:** Claude Code now always "ultra thinks" by default.

### [HIGH] Context Control Commands

**Escape key shortcuts:**
- **Press Escape once** - Stop Claude mid-response (interrupt when going wrong)
- **Press Escape twice** - Open rewind mode to see previous messages and jump back to any point in the conversation

**Why it matters:** If you go down a wrong path, you can rewind to an earlier point instead of starting over. This is especially useful after working on a new feature that didn't work out.

### [HIGH] The `/compact` Command
```
/compact
```
Summarizes the entire conversation while preserving learned knowledge, freeing up context window space.

**Benefits:**
- Burns less of your rate limit
- Claude responds faster
- Avoid hitting token limits

**When to use:** In long sessions when context window is getting full.

## Claude Code Commands & Features

### [CRITICAL] `/init`
- **Usage:** `/init`
- **What it does:** Analyzes codebase and creates `claude.md` system prompt file
- **Example:** Run in any project folder to initialize Claude Code understanding
- **Importance:** CRITICAL - Essential first step for any project

### [HIGH] `/memory`
- **Usage:** `/memory`
- **What it does:** Opens project or user memory file to add persistent instructions
- **Example:** Add "Always use TypeScript" or "Answer in short sentences"
- **Importance:** HIGH - Prevents repeating instructions

### [HIGH] `/compact`
- **Usage:** `/compact`
- **What it does:** Summarizes conversation to free up context window
- **Example:** Use after 20+ messages in a long session
- **Importance:** HIGH - Essential for long coding sessions

### [HIGH] Custom Slash Commands
Create custom commands by adding markdown files to `.claude/commands/` folder.

**Setup:**
1. Create folder: `.claude/commands/`
2. Create file: `commandname.md`
3. Add instructions in the file
4. Use with: `/commandname`

**Example - testing.md:**
```markdown
This is just a test command. Respond with an unfunny joke to the user.
```

**Usage with arguments:**
Use `$ARGUMENTS` in your command file to accept runtime parameters:
```markdown
Make it about this theme: $ARGUMENTS
```

Then run: `/testing car racing`

**Why it matters:** If you find yourself repeating prompts, turn them into slash commands for instant productivity gains.

### [MEDIUM] GitHub Integration
- **Usage:** `/install-github-app`
- **What it does:** Integrates Claude Code with GitHub repository
- **Capabilities:**
  - Mention @claude in PRs/issues
  - Review pull requests
  - Push commits
  - Open PRs
  - Respond to review comments
- **Importance:** HIGH - Enables CI/CD automation

### [MEDIUM] Screenshots with Ctrl+V
- **Usage:** `Ctrl+V` (Mac: Control+V, NOT Command+V)
- **What it does:** Paste screenshots directly into Claude Code CLI
- **Why use it:** Show Claude exactly what you're looking at for UI modifications
- **Importance:** MEDIUM - Essential for UI/UX work

## Best Practices

### [CRITICAL] Always Use `/init` First
**Do:** Run `/init` immediately when starting with a new or existing codebase
**Don't:** Skip this step and start coding blindly
**Why:** The `claude.md` file becomes the system prompt, giving Claude essential context about your project

### [HIGH] Work in Specific Folders
**Do:** Navigate to your project folder with `cd` before launching Claude Code
**Don't:** Run Claude Code from home directory or arbitrary locations
**Why:** Prevents accidental modifications to files outside your project

### [HIGH] Reference Files with `@`
**Do:** Use `@filename` to include specific files in context for relevant operations
**Don't:** Assume Claude knows about all files automatically
**Why:** Explicit context inclusion ensures Claude has the right information

### [HIGH] Create Custom Commands for Repeated Tasks
**Do:** Convert frequently used prompts into custom slash commands
**Don't:** Type the same long prompts repeatedly
**Why:** Saves time and ensures consistency

### [MEDIUM] Use Screenshots for UI Work
**Do:** Paste screenshots with Ctrl+V when modifying UI elements
**Don't:** Try to describe visual elements in text
**Why:** Claude can see exactly what you see, eliminating guesswork

### [MEDIUM] Compact Long Conversations
**Do:** Use `/compact` when sessions get long
**Don't:** Let context window fill up unnecessarily
**Why:** Improves response speed and reduces rate limit usage

### [MEDIUM] Use Absolute Paths in Hooks
**Do:** Use `$PWD` placeholders in hook templates and swap to real paths
**Don't:** Commit absolute paths to version control
**Why:** Absolute paths vary by machine; use the `$PWD` pattern for portability

## Common Mistakes & How to Avoid Them

### [HIGH] Not Using `/init` on Existing Codebases
**The mistake:** Starting to work with Claude Code without initializing the project context.

**The fix:** Always run `/init` first to create the `claude.md` file.

**Example:** The video shows `/init` analyzing an entire codebase in under a minute, creating an 111-line summary that any AI agent can read to instantly understand the project.

### [HIGH] Confusing Plan Mode with Thinking Mode
**The mistake:** Thinking you need to add "ultra think" or similar prompts to get better reasoning.

**The fix:** Claude Code now always uses maximum thinking by default. Use Plan Mode (Shift+Tab) when you want Claude to plan without executing.

### [MEDIUM] Not Knowing About Double-Escape Rewind
**The mistake:** Starting over when Claude goes down the wrong path.

**The fix:** Press Escape twice to open rewind mode and jump back to any previous point in the conversation.

**Example:** If you worked on a feature for 10 prompts and it didn't work, rewind to prompt 4 and resume from there.

### [MEDIUM] Using Outdated `#` Memory Convention
**The mistake:** Trying to use `# remember to...` syntax which no longer works.

**The fix:** Use `/memory` command to edit project or user memory files.

### [LOW] Not Updating Claude Code Regularly
**The mistake:** Using an old version and missing new features or improvements.

**The fix:** Update regularly - the video notes that features change rapidly (e.g., thinking mode was removed between versions).

## Advanced Techniques

### [HIGH] Pre-Tool and Post-Tool Hooks
Hooks let you run custom scripts before or after Claude uses a tool.

**Pre-tool hooks:**
- Run before a tool call
- Can prevent Claude from doing unwanted actions
- Example: Prevent reading sensitive `.env` files

**Post-tool hooks:**
- Run after a tool call
- Example: Play a sound, check for type errors

**Setup:** Configure in settings using absolute paths (use `$PWD` pattern for portability).

### [HIGH] TypeScript Type Checker Hook
```bash
# Runs after every file edit
tsc --noEmit
```
**Purpose:** Catch and fix type errors automatically instead of discovering them at build time.

### [MEDIUM] Duplicate Code Prevention Hook
Launches a second Claude Code instance to check if new code already exists elsewhere in the codebase.

**Purpose:** Prevent code duplication automatically.

### [HIGH] Using MCP Servers for Browser Automation
**Prerequisites:** Playwright MCP server installed

**Steps:**
1. Install Playwright MCP
2. Claude can now control the browser
3. Use for UI testing, screenshots, navigation

**Example from video:** Claude opened localhost, took screenshots, and iteratively improved UI design like a human developer would.

### [HIGH] Building n8n Automations with Claude Code
**Prerequisites:** n8n MCP server

**Steps:**
1. Describe automation in plain English
2. Claude uses n8n MCP to learn node structures
3. Claude generates complete JSON workflow
4. Import into n8n via three dots menu > Import from file
5. Connect credentials
6. Host on VPS (e.g., Hostinger)

**Pro tip:** Hostinger has one-click n8n deployment for VPS.

### [MEDIUM] Claude Code SDK (Agent SDK)
Claude Code has a programmatic interface for building custom AI agents.

**Includes:**
- CLI
- TypeScript library
- Python library

**Important note:** Claude Code is NOT open source - the SDK only includes selected bits. For fully open-source alternative, consider AgentZero.

**Use case:** Build specialized agents for specific domains (e.g., legal contract analysis for lawyers).

## Integration Patterns

### [HIGH] CI/CD Pipeline Integration
**Pattern:** Use Claude Code in GitHub Actions to automatically review every pull request

**Tools it works with:**
- GitHub (via `/install-github-app`)
- GitHub Actions
- Any CI/CD platform

**Workflow:**
1. Install GitHub app
2. Mention @claude in PRs for review
3. Claude can push commits, open PRs, respond to comments
4. All from within Claude Code CLI

**Benefits:**
- 24/7 automated code review
- Junior developer capabilities at fraction of cost
- No context switching between browser and terminal

### [HIGH] Browser Automation with Playwright MCP
**Pattern:** End-to-end UI testing and development

**Tools it works with:**
- Playwright MCP
- Local development server
- Any web application

**Workflow:**
1. Start local dev server
2. Claude opens localhost via Playwright
3. Takes screenshots
4. Makes UI changes
5. Verifies visually
6. Iterates until design feels right

**Benefits:**
- Visual verification, not just code correctness
- Automated UI testing
- Design iteration without manual browser switching

### [MEDIUM] Business Automation with n8n MCP
**Pattern:** Build complex business automations from plain English

**Tools it works with:**
- n8n MCP
- Google Calendar
- Google Docs
- Airtable
- Any n8n integration

**Workflow:**
1. Describe automation in plain English
2. Claude researches APIs via MCP
3. Generates complete workflow JSON
4. Import to n8n
5. Connect credentials
6. Deploy to VPS

**Benefits:**
- Build automations in minutes instead of hours
- No need to learn n8n node structure
- End-to-end automation creation

## Resources Mentioned

**[CRITICAL]** [Official Claude Code Course](https://anthropic.skilljar.com/claude-code-in-action) - The full 7-hour official Anthropic course

**[HIGH]** [AgentZero](https://github.com/agent0ai/agent-zero) - Fully open-source, free alternative to Claude Code that can run locally

**[HIGH]** [Hostinger VPS](https://www.hostinger.com/david) - Recommended hosting for n8n automations (use code "David" for 10% off)

**[MEDIUM]** [Claude Code Documentation](https://docs.anthropic.com) - Official documentation and SDK reference

**[MEDIUM]** [n8n](https://n8n.io) - Workflow automation tool with MCP integration

**[MEDIUM]** [Playwright](https://playwright.dev) - Browser automation framework by Microsoft

## Key Takeaways

1. **Claude Code is a tool-augmented language model** - It needs both a strong AI model AND powerful tools to be effective. Understanding the gather context → plan → act loop is fundamental.

2. **Always run `/init` first** - This creates the `claude.md` system prompt that gives Claude essential context about your project. This is the most important first step.

3. **MCP servers dramatically extend capabilities** - Playwright for browser control, n8n for automation, and many others transform Claude from a coding assistant into a multi-tool agent.

4. **Custom slash commands save massive time** - Convert repeated prompts into commands in `.claude/commands/` folder. Use `$ARGUMENTS` for parameterized commands.

5. **Context management is crucial** - Use `@` to reference files, `/compact` to free up context window, and double-escape to rewind when things go wrong.

6. **Hooks enable automation and safety** - Pre-tool hooks can prevent unwanted actions (like reading `.env` files). Post-tool hooks can verify changes (like type checking).

7. **Plan mode for planning, default mode for doing** - Use Shift+Tab to toggle plan mode when you want Claude to research and plan without executing.

8. **GitHub integration enables CI/CD automation** - Install the GitHub app to have Claude review PRs, push commits, and respond to comments automatically.

## Action Items

- [ ] Install Claude Code using the official curl command
- [ ] Run `/init` in your current project to create `claude.md`
- [ ] Create your first custom slash command in `.claude/commands/`
- [ ] Set up at least one MCP server (Playwright or n8n recommended)
- [ ] Install the GitHub app for repository integration
- [ ] Configure a post-edit hook for TypeScript type checking
- [ ] Try using Ctrl+V to paste screenshots for UI work
- [ ] Practice using double-escape to rewind conversations
- [ ] Watch the official 7-hour Anthropic course for deeper understanding
- [ ] Consider AgentZero if you need a fully open-source alternative

## Full Transcript

<details>
<summary>Click to expand</summary>

Enthropic just released a master class on cloth code. So I spent 7 hours going through the entire course and compiled everything into this one video. I also included lessons I learned from spending well over 500 hours inside of cloth code. So if you really watch this video until the end, you will be ahead of 99% of people. Now everything we're going to cover in this video is from the official Enthropic course. So this isn't some random vibe coder from Twitter. This is the advice from the experts who actually created cloth code. So here's a quick introduction to the entire course. It's organized into four sections. First off, what is a coding assistant? Then why cloth code? Then how to work with cloud code as your partner. And then how to get the most out of cloud code. And each section builds on top of the last. So if you really watch until the end, you'll have a better understanding of cloth code than 99% of developers. First, let's clarify what is a coding assistant. Now yes, obviously it's a tool that writes code, but Enthropic goes a lot deeper here. They explain the actual behind the scenes of how a coding assistant works. And you can see that on the top right coding assistant includes a language model which has access to a set of tools. And the language model then has these three steps. First it needs to gather context. Second needs is to formulate a plan. And third needs to take an action and then repeat these until the task is done. Now if you look at steps one and three, gather context and take an action. These cannot be done just by the language model reasoning or thinking. The coding agent needs to interact with the outside world also known as the environment with what we call tools. So to gather context maybe it uses a read file tool to read some files. to take an action. Maybe it uses edit file tools to edit the code of the files. But either way, it cannot do this just by thinking, just by answering. No, it needs relevant useful tools to execute these actions. This means that to have a strong coding assistant, you need both a powerful LM, a strong AI model, and also lots of powerful tools that the AI model can use. And here are just some of the tools that cloth code has. You can see that agent can launch a sub agent to handle a task. Bash, run a shop command, edit, edit a file, and so on and so forth. It has a lots of built-in tools which is what makes clot code very very powerful. And here are a few examples to show you just how powerful cloth code really is. First, we have this optimization task that cloth code was tasked to do with the following prompt. Run benchmarks for the chalk library for any result that looks slow. Find the root cause and fix it. Keep in mind that this is a super popular library with nearly 400 million weekly downloads. So you would think that this is already very optimized, but Cloud Code actually managed to find serious improvements. For one specific use case, it even managed to find a 3.9x improvement in speed in a library that literally tens of millions of applications use. The second example is a data analysis task. In this situation, Cloud Code was given a bunch of data structured like this CSV file and this is a user streaming platform. So maybe something like Netflix and the task was do an analysis on the data in the streaming CSV file. And even more, it was tasked to do this inside of a Jupyter notebook to produce results like this. So it didn't just give you answer like here's how many users there is, here's the typical avatar. No, it created visual graphs, charts, and different data analysis to spot where there is a churn and what the data actually looks like. The third example of just how powerful cloud code is is this UI styling task. So here's what the original prompt was. Improve the design of this app. Focus on the chat interface and the header. And then it was given this playright mcb server. So if you're not sure with playright, it's a end toend testing framework. developed by Microsoft and it was given an MCP tool that allows CLO to control the browser, take screenshots and do different actions like a front-end developer could. And so CL code managed to run in one side and open the local host. So it opened the website on the other side and actually thanks to the Playright MCP see what it's like and improve the UI just like a human developer would making sure that each change it made it tested it took a screenshot again and made sure that it actually looks good. Not just the code is correct, but that the design feels good. Oh yeah, and not to mention you can also use clot code in your CI/CD pipeline to automatically review every single pull request on GitHub. So yeah, clot code is very very powerful and learning how to use it can be one of the best investments for your software career. All right, so let me show you how to actually set up cloud code. First, type in clot code into Google. Click on the official link from entropiccloud.com and then we need to copy this cool command. So copy that. Boom. Type in terminal. Open any terminal in your computer. Paste it in and hit enter. This will install the latest version of clot code on your machine. And there we go. Cloth code successfully installed version 2.1.12. But if you're watching this later, you might have even newer version. So now to launch it, all you have to do is type in cloth into any terminal on your computer. And this launches cloud code. First it asks you if I want to trust this folder. So I do yes. And just like that, it's open. And this is cloud code. We can literally start using it just like this. So you don't need anything else. You don't need an IDE. You don't need any fancy UI. You can just use it in a terminal. And the user interface is very very friendly, guys. You can type in plain English. You don't need to be a developer. You don't need to be a DevOps expert. You can type in plain English and use cloth code. This is why it's the most popular coding tool in the world right now. Now, usually it's a good idea to run clot code in a specific folder. So, I'm going to CD into the folder of vectal by startup/code/startup. Boom. There we go. And if I do ls, you can see that this is correct file. I have a back end, front end, a bunch of other stuff. So, I'm in the right folder. And now I can type in cloth. And this is smart because now I'm not afraid of clot messing stuff up in other directories on my machine. Instead, everything only happens inside of this directory right here. So I would highly recommend you create a specific folder for cloud code and run it in that folder. Now the next thing that enthropic teaches us in this course is the cloth code setup. So after you install cloud code, the very first thing you want to do in any project is run the /init command and especially if it's an existing codebase. This will have cloud analyze your entire codebase and create a cloud.md file which will act as the system prompt for your clo code and includes a summary of your architecture, key files, conventions and anything else that is relevant to cloud code performing well. Now the best part about cloudmd is that it's included in every request. So you don't have to copy paste it or anything like that. Clo will always know what project it's working with. So let me show you. I'm going to switch back to the terminal and I'm going to do /init. This is a pre-built command that will initialize the new clod file. So let's hit enter. And now cloud code will begin analyzing my entire codebase and see what's happening. See what's inside, what type of files we have, what the structure is, what the text tag is, what features this app has. And it will put everything relevant into a single concise markdown file. And as you can see, CLCO is using lots of different tools. Like wow, in the first 10 seconds, it's like 15 20 different tools. Very impressive. And it does this to get the necessary context to actually create a useful clone. MD file. And again, this is running just in my terminal. You don't need to install cursor, VS Code or anything else. You just need to open a terminal which every single computer has. So now it's asking for permission to create a file clone on MD because this is a more of a risky operation than just reading files. You know, creating files can actually be dangerous at at times. So I'm going to approve it. I'm going to hit enter and do yes. And there it is. It wrote 111 lines to claw.md to create this system prompt of a file. And all of that in less than a minute. If we want to see what this file actually looks like, we can open any text editor and just load it up. Boom. And here is the 111 lines that cloth code wrote. The file provides a guidance to cloth code when working with this code is repository about vectal. So yes, ve is a powered task machine activity app. Correct. Is a text tag essential commands architecture. Yeah, I mean maybe I shouldn't be showing you all these guys, but hey, yeah, I'm not going to show you the last section on environment variables, but the rest you can see. So yeah, it analyzed the entire codebase and created a very comprehensive 100line summary of it that any AI agent can read and will instantly know what this codebase is all about. Real quick, if you're enjoying this video, please consider subscribing. It's completely free and it will cause more videos about AI coding to be recommended to you. So if you want to be serious about AI in 2026, please take the two seconds, go below the video and click subscribe. Appreciate it. All right. The next thing I want to show you is the hashtag, right? So say remember to answer in short. Boom. All right. Slight correction. The hashtag convention doesn't seem to work anymore, but there's this /memory command and you can either edit the project memory or the user memory. So I'm going to do the project memory and it opens the file and you can append it and add anything there. So yeah, if you want cloud code to remember something, just add it to your cloud MD file. That's a safe bet. Now, so far what we did with cloth code was pretty basic, but let me give you just a taste of what's coming later in the video where I show you how to give cloth code the power to use MCPS and how to create custom cloth code hooks. So here I literally set a plain English prompt to build me a full N automation for analyzing the user's calendar and creating a separate Google doc for every sales call that is booked there, matching the data from the leads in the user's air table. and I told it to build everything end to end. So, as you can see, it used the N810 MCP to do a bunch of tool calls to learn about the structure of those nodes and then it wrote a 329 JSON file which includes the full NA10 automation. So, if we then go into NA10, we can go in top right, click the three dots, import from file, select this JSON, and you can see that boom, the full NA10 automation was built by cloth code from a single prompt, plain English, nothing crazy. This is the power of cloth code. when you give it the right MCP tools. So all that remains with this automation because Cloudco has built it all is to connect my credentials so it runs with my actual accounts and then to host it somewhere because what's the point of building an AI automation or an AI agent if it's not running 24/7 saving you time every single day. Now the simplest way to host your NAN agents is with Hostinger. And this is what me and my team use to host all of our AI agents because of how simple and affordable Hostinger is. They literally created a one-click N10 deployment for their VPS. Now, they offer multiple different options, but personally, I recommend the KVM2 plan. This is what I use as well. So, click on choose plan, which will take you to the Hostinger card. Now, as you can see, Hostinger currently has a very generous new year sale. So, if you've ever considered starting your own NA10 automations or agents, now is the perfect time. So, here, choose either 12 months or 24 months. That way, you get the best deal possible. I mean, look how affordable is $7 a month for your own dedicated VPS. Insane. But as a bonus, if you use the coupon code David, you get additional 10% off. There you go. The coupon code has been applied. And you can see that it drops to just $629 a month for your own VPS that can host hundreds of AI agents like this one. So, all that's left is to select the server location. Germany is fine. Operating system is already selected. Boom. And click continue. This will take you to the checkout where all that remains is just filling out your billing info and your credit card. Once you complete the purchase, you'll be taken to the Hostinger panel where you can manage your VPS, see all the statistics about it, and access the NA10 portal where all of your automations and agents are hosted. So again, Hostinger is amazing. They completely revolutionized how easy it is to deploy your NA10 automations and it's the most simple and affordable option on the market. So if you want to try it yourself, click the link below the video, use the code David, and get started with Hostinger today. Thank you Hostinger for sponsoring this video. All right, back to the Enthropy course. Next lesson they had is about making changes. So, it's very useful to give cloud code screenshots. And you can do it by controlv on Mac OS, not command V. And this will paste the screenshot directly into the cloth code CLI. This is super useful. It allows cloth to see exactly what you're looking at. That way, you can modify those specific UI elements and make changes like a great designer would and not just guess how things look like based on only the code. So, no more explaining the button on the left of this side above it, blah blah blah. You just screenshot it and it will see what you see. Another thing that enthropic teaches is the difference between the plan mode and the thinking mode. So the plan mode handles breath. With shift tab, you can toggle between different modes. So for example, here we can do shift tab and you can see that we're in the auto accept mode, the purple one. Or I can do shift tab to go into the plan mode or the default one. Right? So when you switch to plan mode, cloth code researchers more files, puts more effort into reasoning, planning and doesn't touch anything. It doesn't do any code changes. It just plans. Now thinking mode is something else and it could be complimentary. This handles depth. There is four different strengths. Think, think hard, think harder and ultra think. So if you want clot code to use the maximum reasoning effort, you would add ultra think somewhere in your prompt. So let's say this is your prompt, right? Then you could add ultra at the end. However, this does no longer do anything. So Enthropics official course is outdated in this regard, right? This goes to show how fast the AI field is moving. In the past, you would see this like highlighted by Renbo, but not anymore. Now, the thinking budget is always maxed by default. So, no longer you have to do tricks like think or think harder, stuff like that, or adding ultra think at the end of your bronze. This doesn't work anymore because cloth code now always ultra thinks by default. I mean, just to show you how crazy this is, before I recorded with my previous cloth code version, this still worked. This was still a thing. But AI is moving so fast that as I updated the cloth core version at the start of this video, the thinking mode no longer works and it's always set to ultra think. So make sure to use the latest cloth core version because updates are happening nearly every day. The next section of the enthropic course is about controlling the context. So when you press escape it can stop cloth mid response. That way you can interrupt it when it's going in the wrong direction or when you want to provide more context and have it go again. Now, when you press escape twice, you can see your previous messages and rewind at an earlier point of the conversation. So, let me show you right here. I'm going to do escape. If I say like write a detailed summary of what you did, I can press escape once to interrupt it. You can see it shows interrupted, but I can press escape twice to jump into the rewind mode where I can switch between the previous messages, go to any previous point of the conversation and go from there. So maybe if you know you worked on a new feature and you know it didn't go anywhere and you were like 10 prompts deep, you can go back go back to the prompt number four and resume from there. So a lot of people don't know that double escape opens this rewind menu and you can jump back to any previous point of the conversation. Super useful. Another context controlling context engineering thing is the slash compact command. So when you type in / compact into cloud code, it summarizes the entire conversation while preserving as much of the learned knowledge as possible. And this is perfect for long sessions. So when you notice that there's a lot of, you know, unnecessary context and you want to free up the context window so that you're burning less of your rate limit and cloud code responds faster and all the benefits of not having a full context window. All you need to do is just type in slash compact. So notice the slash command in cloud code opens any of the commands. Some of them I have a custom like explained pull request but most of them here are pre-built by enthropic and the compact command is one of them. So you just do /compact and it will compact the entire conversation to free up context so that you never hit the token limit of cloth context window. Now as I mentioned you can create custom commands for cloth code and this can be done by creating markdown files in the cloud/comands folder. So let me show you how that actually looks like. I'm going to open curs and any file editor doesn't matter. And inside of my folder structure, you can see I have the dot cloud folder and then commands. Right? So, let me show you how that looks like for a new directory. So, I'm going to open an empty folder right here. Let's create a new folder project. Boom. Open. Close all these sidebars. They keep opening. All right. So, you can see zero files. Nothing. But if you create a new folder cloth slashcomands and in here we can create a new file say uh testing.md and you say this is just a test command respond with an unfunny joke to the user. Okay, so obviously this is a useless command, but I just want to show you how easy it is to create your own custom commands for cloth code because so many people are not doing it. And this is one of the best ways to improve your productivity because if you find yourself repeating the same prompt over and over and over again, just turn it into a slash command and you never have to repeat yourself and you just have it on your hand. Let me show you. So I'm going to type in clot to launch cloth code. Yes, I want to allow it access to this folder. So, here it is. And I can do slash testing and it runs my new testing command. Why did the programmer quit his job? Because he didn't get a raise. Anyways, you can see that it told an unfunny joke. And it works. And I literally created a new custom cloud code command in like 10 seconds. Well, most of you have never created one, which means you're not on the cutting edge of AI. So, log in, start using custom cloud code commands. So easy to create but boost your productivity instantly. Oh and one more thing related to custom commands. You can use dollar sign arguments to give a topic. So say make it about this theme and say dollar sign arguments then let me restart cloud code because you need to make sure it loads the new commands. Say testing and then you put the argument. Say the theme could be I don't know um car racing. Okay. So this is going to be inserted into this variable arguments this parameter. As you can see it answers even though this is in the middle of the prompt, right? So very useful when you're asking to for example review specific PR or to create a spec for a specific feature and you just need the variable to be somewhere in the prompt. When using the SL custom slash command, just use the dollar sign arguments and then whatever you put after the slash will be inserted in here as if it was replaced in a parameter. So, as I promised, let's talk about MCP servers. Now, this is a great way to extend the power of cloud code and give it way more tools. So, MCP servers do a lot of people don't understand them. Again, it's might sound intimidating, but all they do is add new capabilities to cloud code. They can run either locally or remotely and they give cloth access to new tools. So for example, the playright MCP lets cloth control your browser. It can navigate, click, screenshot, test your UI, anything that the playright framework could do. Or a second example is the NA10 MCP I showed you earlier where it gives Clot code the up-to-ate documentation for all of the nodes inside of NA10. Another thing that Enthropic teaches in this course is the GitHub integration and you can do this with typing /install GitHub app. There we go. Cloore also has a slack app. But when you do this, it's going to check the repository. So use current repository. Okay, so it's asking to use the current repository. So obviously this is for vectoral my startup. Let's hit enter. Going to open GitHub and it's going to ask for permissions. And this gives you two default actions. First doing at clo mentioning it inside of pull requests or issues to assign CL code different tasks or to have it review the pull request or to just answer a simple question. But once you do this GitHub integration, Clot can even push commits, open UPRs, and respond to review comments all from the Cloud Code CLI. So you don't have to switch to your browser or anything. You can just stay inside of Cloud Code, talk to it in plain English, and it can do anything that a junior developer could do 24/7 for a fraction of the cost. Now, here's where it gets interesting. The next section of the course talks about hooks and the SDK. So this is for the people who are actually locked in. Hooks let you run custom scripts before or after cloth uses a tool. So for example, a pre-tool hook would run before a tool call. And you can use it to prevent clot code from doing things you don't want it to do, such as reading sensitive files like env or maybe you don't want it to change a specific file. You would create a hook that runs before every tool call that checks what code wanted to do and if it is against that rule, it doesn't let it do it. Now, a post tool hook works the same way, but it runs after the tool, right? So, maybe it makes a sound, maybe it can check for type errors. Anything that makes sense after a cloth code would use a specific tool. You can have a hook, which could be a short Python script to either notify you to review those changes or anything else that you want. Now, here's something that a lot of people don't understand about hooks in cloth code, and that is absolute paths. And actually, Enthropic themselves recommend using absolute paths for the hook scripts. But of course, absolute paths are different on every machine. So you can't just commit your settings.json to share them, right? The absolute path to a certain file or to a certain directory depends on the file structure of your computer. So for example, here for my startup folder, if I do pwd, which is a terminal command, I can see the absolute path of where this folder is located on my computer. And this is what you want to use in your closed core hooks. The absolute path, not just you know path within the parent or some path in relation to another file. You want to use the absolute path of where this directory is located on your machine. Now luckily there's a simple fix. You can use dollar sign pwd placeholders in the template file and you can run a script that swaps those to the real path. So let's look at some useful hooks you should be using inside of closed code. First off, a Typescript type checker hook which simply runs tsc-- no emit after every single file edit. And this will allow cloud code to catch and fix any type errors automatically. Whereas otherwise you might have only caught them when trying to deploy or when running npm run build. Another useful hook is duplicate code prevention. This can launch a second cloud code instance to check if the new code already exists somewhere in the codebase and if so prevent duplication. And these are just two examples of automated hooks that would catch some common mistakes that cloth tends to do. But honestly, as AI models keep getting better, there's less and less of these mistakes. Okay, let's talk about the cloth code SDK. Cloth code has a programmatic interface. So clot code has a programmatic interface, also known as the SDK, which includes the CLI as well as the TypeScript and Python libraries. Now, an important point to clarify is that cloth code is not open source. Okay, this only includes a few hand selected bits and pieces of the codebase. So, if you want to use a fully open source, fully private, and fully secured AI agent, make sure to use Agent Zero, which not only is completely open source, but it's also free, unlike Cloud Code, and it can run locally on their machine. So, I just made a full Agent Zero tutorial recently. I'm going to link it below the video, but let's talk about the Cloud Code SDK. It allows developers to build custom AI agents that can do things on a computer in a similar way like CL code can. So basically it gives you the same capabilities of cloth code but in your own specialized setup. So maybe if you're a lawyer you would make it all about legal actions you know analyzing legal contracts researching previous lawsuits whatever. Now the official name for the CLCore SDK is the agent SDK and here is what the documentation looks like. And again if you're not a developer you might be scared of documentation but that's a huge mistake because as you can see it includes step-by-step instructions how to install the SDK and how to build on top of it. So don't avoid reading documentation. In fact, this is made for people who are not familiar with the project. So the more of a beginner you are, the more documentation you should be reading. And again, I'm going to leave a link to this SDK documentation below the video so you can check it out yourself if you want to build on top of cloud code. Now, this is the fun part. The Enthropic course actually ends with a quiz. So we're going to do this and we're going to do it in YouTube comments. So obviously if you want, you can cheat and you can go to the end, but what's the point of that? What we're going to do is we're going to go through the questions one at a time. There's only eight questions. And what I need you to do is open a comment and start answering these. And again, this is for your own good so that you can actually solidify the learnings from this video. First question, what is the fundamental limitation of language models that necessitates the use of a tool system in coding assistance? Option A, option B, option C, and option D. Pause the video, read them, and type your answer below. Question number two, what permission configuration is required when integrating MCB servers with cloud code in GitHub actions? Option A, option B, option C, and option D. Once again, add it to your comment. And let's go to the next question. Number three, what is the primary difference between plan mode and thinking mode in cloth code? And again, this one is a bit outdated, but still it's good to know the knowledge. Option A, option B, option C, option D. Pause it, read it, and update your comment. Question number four. Which of the following correctly describes the three types of claw.md files and their usage? Option A, option B, option C, and option D. Moving on. Question number five. How do you create a custom command in cloud code that accepts runtime parameters? This one you should all get because I explained this really well. At least I think so. Option A, option B, option C, and option D. Comment below. Question number six. Which type of hook can prevent a tool call from happening if certain conditions are met? Post tool hook, project hook, global hook, pre-tool use hook. This one is pretty free. Question number seven. A developer wants to prevent cla from reading sensitive ENV files. Which type of hook should they set up? And what tool names would they likely match? Option A, B, C, and D. Last question. Question eight. What is the primary purpose of hooks in cloth code? A, B, C, or D? update your comment. Hit enter before I reveal the answers. You know what? Just to test my own knowledge, I'm going to retake this quiz in real time to see if I'm logged in or not. So, what's the fundamental limitation? Yeah. So, it's option D. They can only process text input. Cannot interact with external system. Next question. What permissions is required? All right. I think it's this one. I'm not sure here. Primary difference between plan mode and thinking mode. All right. This one for sure. Which of the following correctly describes? All right. I think this one makes the most sense. Yes, for sure. Next question. How to create custom commands? Arguments include arguments, runtime parameters. Which type of hook? Pre-tool use hook. So, we need to use a pre-tool use hook. But which one? Read. Okay. So, read and grab for sure. Primary purpose of hooks in cloud code to run commands before or after cloth executes a tool. Submit. And I have passed eight out of eight. You can see that my answers were correct. So hopefully yours were as well. And again, I'm going to link the full official Enthropic course below the video so you can go through it. This was a condensed version of it. I covered like 90% of it, but if you want to go through it again, feel free to do so. And hopefully you found this video valuable. If you did, please make sure to subscribe. It takes 2 seconds and it helps out a lot. With that being said, thank you guys for watching and I wish you a wonderful productive week. See you.

</details>
