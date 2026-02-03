---
video_id: FsDYk0WqBt0
title: "An MCP & Skills masterclass"
creator: Rasmus
creator_tier: 1
url: https://youtube.com/watch?v=FsDYk0WqBt0
published_at: 20260129
duration: 773
view_count: 6585
topics: ['mcp', 'claude_code', 'business_automation']
overall_importance: MEDIUM
tools_mentioned:
  - MCP (Model Context Protocol)
  - Anthropic Skills
  - Grapile
  - Claude Code
  - Daytona
frameworks:
  - MCP + Skills Architecture
difficulty: intermediate
extracted_at: 2026-02-02T07:41:03.801964
---

# [MEDIUM] An MCP & Skills masterclass

**Creator:** Rasmus  
**Video:** [https://youtube.com/watch?v=FsDYk0WqBt0](https://youtube.com/watch?v=FsDYk0WqBt0)  
**Published:** 20260129  
**Overall Importance:** [MEDIUM]  

## Summary

Rasmus explains that MCP servers and Anthropic Skills are complementary rather than competing technologies: MCP provides raw tool access to external systems, while Skills provide structured workflow logic, domain expertise, and step-by-step procedures. Skills use a progressive disclosure architecture (YAML metadata → full skill.md → referenced files) to solve context bloat issues when agents access many tools.

## Key Insights

**[MEDIUM]** MCP servers provide tool access; Skills provide workflow logic and domain expertise. They are complementary, not replacements.

**[HIGH]** Skills use progressive disclosure with three levels: (1) YAML name/description preloaded into system prompt, (2) full skill.md loaded when relevant, (3) referenced files loaded only when specifically needed.

**[MEDIUM]** MCP instructions should cover 'how to use the server correctly'; Skills instructions cover 'how to use them for a given purpose or in multi-server workflows'.

**[MEDIUM]** A single skill can coordinate multiple MCP servers, and multiple skills can enhance a single MCP server.

**[MEDIUM]** Conflicting instructions between MCP servers and Skills (e.g., JSON vs markdown output) cause Claude to guess—let MCP handle connectivity, Skills handle presentation and workflow logic.

## Frameworks & Patterns

### [HIGH] MCP + Skills Architecture
**Type:** architecture  
Two-layer system where MCP provides raw tool access and Skills provide structured workflow execution

**Components:**
- MCP servers (connectivity layer)
- Skills (orchestration layer)
- Progressive disclosure mechanism
- Conflict resolution heuristics

## Tools Covered

### [HIGH] MCP (Model Context Protocol)
Protocol for connecting AI agents to external tools, data sources, and APIs

**Use Case:** Giving agents access to Notion, Gmail, calendars, Stripe, GitHub, etc.

### [HIGH] Anthropic Skills
Structured workflow definitions with progressive disclosure for Claude Code/Desktop

**Use Case:** Encapsulating multi-step procedures, domain expertise, and SOPs as reusable instructions

### [LOW] Grapile
AI-powered code review tool

**Use Case:** Reviewing PRs with confidence scores, catching issues like race conditions, curbing 'slop' from AI-generated code

### [LOW] Claude Code
Anthropic's CLI coding agent

**Use Case:** Generating code with Opus, integrated with Grapile for review

### [LOW] Daytona
Development sandbox platform

**Use Case:** Example of MCP server providing API access to sandbox stats and management

## Techniques

### [HIGH] Progressive Disclosure in Skills
Three-tier context loading to minimize token usage while maintaining capability

**Steps:**
1. Create skill.md with YAML frontmatter (name, description)
2. System prompt loads only name/description at startup
3. When skill is relevant, load full skill.md body
4. For specific sub-tasks, reference and load additional files

### [MEDIUM] Skill-MCP Coordination
Architectural pattern for combining tool access with workflow logic

**Steps:**
1. Use MCP server for tool connectivity and data access
2. Use Skills for sequencing, presentation, and domain-specific procedures
3. Avoid conflicting instructions between layers
4. Design skills that orchestrate multiple MCP servers when needed

## Resources Mentioned

**[LOW]** [Ralphie](mentioned in description) - Rasmus's open-source Ralph Wigum implementation using Grapile for PR reviews

**[MEDIUM]** [AI MCP Builder](mentioned in description) - Open source tool for generating MCP servers from codebases using AI

**[MEDIUM]** [Skills Marketplace](skills.sh) - Repository of pre-built skills for common workflows (React best practices, web design guidelines, Remotion, etc.)

**[LOW]** [Grapile](not provided) - AI code review tool with confidence scoring

## Prerequisites

- Understanding of AI agents and tool use
- Familiarity with MCP servers
- Basic knowledge of Claude Code or similar agentic coding tools
- YAML and Markdown for skill file creation

## Project Ideas

- Build a 'Meeting Prep' skill that queries Notion notes, checks Gmail for context, and generates agenda via coordinated MCP servers
- Create an MCP server generator tool for internal APIs
- Develop a skills library for your team's specific domain workflows
- Implement progressive disclosure pattern for complex multi-step agent workflows

## Full Transcript

<details>
<summary>Click to expand</summary>

There's been a lot of discourse on MCPs and skills in particular. Most people think skills are meant to replace MCP or vice versa. And that could be further from the truth. They're actually very complimentary and that's what we're going to talk about in today's video. So when we think of MCPs and skills, let's first understand what they're supposed to do. So there's you, you're communicating with this model and you're telling this model to send you a report, right? You have connected your external tools using MCP, right? your notion account, your Gmail account, your Cali, and your Stripe. And you've given the model access to these tools, the agent access to these tools via MCP. So, it should be able to generate a report for you. Now, one thing that we've realized early on in MCP land is that the agents were terrible at this. When you gave an agent access to many tools, it would just hallucinate. It would pick the wrong one. It was not a great experience. And this is where skills come in. skills handle the expertise, the domain knowledge, the workflow logic and turn raw tool access into reliable outcomes. What does that mean? Let's say uh you and I go to a hardware store. We go to Home Depot and we are supposed to build out a new patio at my house. We're supposed to build a new backyard, right? We go to Home Depot. We buy all these tools. We come back to my house. So, we have these tools, but no one knows how to use them. We don't know how to use the tools. We don't know what goes first. We don't know how to what type of wood we need. Like we have all these tools, but you and I are just developers. We don't go outside. We don't work with our hands. We work with our minds. Speaking on working with our brains, one of the smartest decisions I made was adding today's sponsor to my workflow, and that's Gravile. Now, I can tell you Grapile is being used by some of the best companies like Brex, Mintlifi, Substack, Browserbase, Clavio, Post Hog, or what I can show you is how we've been using Grapile in my product studio and my open source repos and my personal side projects. First, let's look at my open-source project Ralphie, which is a Ralph Wigum implementation. Literally, if you look at all the closed PRs, one thing that they all have in common is the confidence score was either a four out of five or a five out of five. Meaning, every PR that's made is reviewed by Gravile. And if Grapile doesn't give you a minimum of four out of five, it is not getting merged. That's how good Grapile is. In my product studio, one of the products we're developing for a customer, I told our developer after every PR, you can fire grabile review. I would say aim for a four out of five or a five out of five. Then I can review. And in our latest PR, he tells me finally got a five out of five. And finally, for my side projects, I'm using Claw Code a lot. And even though Opus is great at shipping go, there are a lot of mistakes. There's a lot of slop that it generates. But with Gravile, I'm able to curb the slop down. I'm able to make sure that the code is functional, clean, and it actually works. For example, in this pull request, the PR that Claude Code made, there was a race condition in it, but Cloud Code said the code was fine. It was perfect. I tested it out. It looked good, but there was a race condition that I did not see. But because I have Gravile reviewing my PRs, not only did it catch the race condition, it offered a suggestion to fix it. And now I have a confident score of a four out of five. And Gravile also gives you the power on how serious you want these reviews to be. I have it on low, meaning I wanted to find even the most minute issue because I want my code to be perfect. That's why I use Reptile everywhere. If you want to check them out, the link will be in the description down below. They have a twoe free trial. Make sure you take it for a spin. Thank you to Reptile for sponsoring this video. Now, let's get back to it. How am I supposed to take these tools and build a backyard, right? This is where skills come in. Skills give the agent the exact step by step, the exact SOP standard or procedure to take when doing a certain action. So let's say in this case I have a skill that's called send a report skill and this skill tells the model first you go to notion you query uh the last five meeting notes and then you summarize those notes and then you send emails to whoever needs to send emails and then you book a call and then you send an invoice to a client. So you can think of skills as a way of training your model, training your agent to do the exact step by step that you wanted to do instead of like cuz can you imagine if we had no skills here and we told the agent send a report. What does that even mean? How do I send a report? A report of what? I have all these tools, right? This is why the models were hallucinating back when it was just MCPs. But now that you have skills in the picture, MCPs become a lot more usef...
</details>
