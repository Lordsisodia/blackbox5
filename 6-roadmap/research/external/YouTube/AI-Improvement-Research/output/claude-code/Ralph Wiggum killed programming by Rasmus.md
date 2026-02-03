---
video_id: TJkxAJS34CQ
title: "Ralph Wiggum killed programming"
creator: Rasmus
creator_tier: 1
url: https://youtube.com/watch?v=TJkxAJS34CQ
published_at: 20260116
duration: 436
view_count: 15652
topics: ['claude_code']
tools_mentioned:
  - Claude Code
  - Ralph Plugin (Claude Code)
  - Open Code
  - TypeScript
  - Custom Ralph.sh script
difficulty: intermediate
extracted_at: 2026-02-02T07:25:36.496283
---

# Ralph Wiggum killed programming

**Creator:** Rasmus  
**Video:** [https://youtube.com/watch?v=TJkxAJS34CQ](https://youtube.com/watch?v=TJkxAJS34CQ)  
**Published:** 20260116  

## Summary

This video explains 'Ralph Wiggum,' a technique for running AI coding agents in an autonomous loop to build applications without constant human intervention. The creator demonstrates how to set up a PRD-driven development workflow where an AI agent continuously builds features, runs tests, and tracks progress until completion.

## Key Insights

- Ralph Wiggum is not a tool but a technique/pattern for autonomous AI coding agents that loop until a PRD is complete
- The two essential files are prd.md (defines end state with implementation steps) and progress.txt (tracks completed work)
- Plan quality dramatically impacts output quality—detailed, precise PRDs produce better software than vague ones
- Human taste and direction still matter; the surrounding tools and planning determine whether output is valuable or 'AI slop'
- Running with 'fast' flag skips tests and linting for rapid feature building, while default mode includes quality checks
- The progress.txt file enables resumability—agents can pick up where they left off after interruptions
- Cost can be extremely low (fractions of a penny) for simple applications when using this loop pattern
- The official Anthropic Ralph plugin in Claude Code exists but is considered inferior to custom implementations by the technique's originator

## Tools Covered

### Claude Code
Anthropic's coding agent/IDE with plan mode and plugin system

**Use Case:** Used to create PRDs in plan mode and run the Ralph loop via custom script or official plugin

### Ralph Plugin (Claude Code)
Official Anthropic plugin for Ralph Wiggum workflow

**Use Case:** Installed via /plugins command, though creator recommends custom scripts over this official version

### Open Code
Alternative AI coding agent

**Use Case:** Mentioned as viable alternative to Claude for running Ralph loops

### TypeScript
Typed JavaScript superset

**Use Case:** Used for type safety; linter runs automatically in Ralph loop to catch errors

### Custom Ralph.sh script
Bash script that orchestrates the AI agent loop

**Use Case:** Creator's preferred implementation with flags for fast mode (no tests/linting) or full mode with quality checks

## Techniques

### Ralph Wiggum Loop
Autonomous AI coding pattern where agent continuously builds features until PRD completion

**Steps:**
1. Create detailed PRD.md with phased implementation steps
2. Create empty progress.txt file
3. Run Ralph.sh script to start loop
4. Agent reads PRD and progress.txt each iteration
5. Agent implements next unchecked feature
6. Agent documents work in progress.txt
7. Loop continues until all features marked complete

### PRD-Driven Development
Using a detailed product requirements document as the single source of truth for AI development

**Steps:**
1. Use Claude Code plan mode to generate structured PRD
2. Include overview, features, and detailed implementation phases
3. Format as checklist/todo list for easy progress tracking
4. Make implementation steps specific and actionable

### Checkpoint-Based Progress Tracking
Using a progress file to enable resumable, stateful AI development sessions

**Steps:**
1. Initialize empty progress.txt before first run
2. Configure agent to append completed work descriptions after each feature
3. Agent reads progress.txt at loop start to identify last completed item
4. Enables stopping and restarting without losing context

### Quality-Gated Automation
Embedding automated tests and linting into the autonomous loop

**Steps:**
1. Configure Ralph.sh to run test generation after each feature
2. Execute tests and verify passing status
3. Run TypeScript linter for type checking
4. Only proceed to next feature when all checks pass

## Code Examples

### Ralph.sh script structure with flags for normal and fast modes

```
# Normal mode: ralph.sh
# - Generates tests after each feature
# - Runs tests and verifies passing
# - Runs TypeScript linter
# - Proceeds only on success

# Fast mode: ralph.sh fast
# - Skips test generation
# - Skips linting
# - Rapid feature building only
```

### PRD structure using plan mode output

```
# prd.md structure:
# - Overview
# - Features
# - Implementation Steps (phased checklist)
#   - Phase 1: [todo items]
#   - Phase 2: [todo items]
#   - etc.
```

### Progress.txt evolution

```
# Initial state: empty file
# After running Ralph loop:
# - Documents all code changes
# - Lists completed features with timestamps
# - Serves as checkpoint for resume
```

## Resources Mentioned

- [Ralph.sh script file for download](In video description (not specified in transcript))

## Prerequisites

- Familiarity with Claude Code or similar AI coding agents
- Basic bash/shell scripting
- Understanding of software testing and linting
- TypeScript or JavaScript project experience
- Ability to write detailed technical specifications/PRDs

## Project Ideas

- Apple Reminders-style todo app (demoed in video)
- Personal finance tracker with categorized transactions
- Habit tracker with streak visualization
- Simple CRM with contact management
- Markdown note-taking app with tagging
- URL bookmark manager with search
- Personal blog generator with RSS feed
- Expense splitter for group trips

## Full Transcript

<details>
<summary>Click to expand</summary>

Who the heck is Ralph Wigum? It's all everyone is talking about. I was on vacation for the last two weeks enjoying the beautiful Ethiopia, the sun, the food, the people, family. It was a great time. But the last week and a half, all everyone's talking about is Ralph. And I thought Ralph was a character from Simpsons. But really, what it is is it's a robust way to let AI autonomously build applications. And in this video, not only am I going to show you how it works, but I'm also going to show you my setup. 2026 is going to be a fun year. Sit back, relax, let's get into it. So, when building an application with AI, we've sort of been following this flow this last, I would say, year and some change where we have an idea and we're going to break down that idea into a list of features, right? And it's in such a way that each feature when it's complete is going to be some sort of finished product. Now, a smart way of going about this when building with AI is to have some sort of feedback loop for the AI to recognize whether a feature is complete or not. And that's where we include a test, right? So, I'll build feature one and then I'll ask the AI to build test one. And if test one passes, we move on to feature two. And then test two passes feature three. And at some point, we'll reach a finished product. But here's the thing. This setup has a lot of human involvement. And although for most people this is better than writing code by hand, um there should be a better way, a more autonomous way, a way for AI to continuously run through and build said application. And that's where Ralph comes in. The question that Ralph solves is what if instead of manually prompting each feature, AI can continuously build out the features until it's done. So when someone asks you what Ralph is, Ralph is essentially a technique for running AI coding agents in a loop. Now, Enthropic has a plugin that you use, which is their official Ralph plugin. And the way you would set it up is /plugins, and then you can search for Ralph. I already have it installed. So, you can see it here, the Ralph plugin installed. You can use the Ralph plugin that's set up in Claude Code. But to be honest with you, it's actually not the best iteration. The actual developer who came up with the concept of Ralph Wiggum is not pro the way Claude Code has the plug-in set up. But how does Ralph work? It's as simple as this. You're going to need a prd and then you're going to need a progress.txt file. These two files are quintessential. What's going to happen then is we're going to be running whether it be claude or open code or whatever agent in a loop. And in each loop, what the agent is going to do is it's going to review the prd.md file. It's going to review what features it has to build. It's going to build those features. And then it's going to document the work it's done in the progress.txt file. And then it's going to continue that loop again and again and again until the prd file is complete until all the features are fully built up. So step by step, how do we run Ralph? We create a plan and save it as prd.mmd. I'm going to show you an example. We're going to create a progress.txt file. And I want you to realize this. The prd defines the end state. The progress file tracks what's done. Claude reads both on each loop iteration, finds the next unchecked item, implements it, and updates the progress. We're going to create a simple Ralph.sh script. I'm going to show you the one I have working right now. I'm continuing to iterate this. And another thing I would highly suggest is you customize it to your liking. So, I used Cloud Codes plan mode to build this PRDMD. And essentially what I wanted to build was an Apple reminder style to-do app. And as you can see, it has an overview, the features, but really the most important part was the implementation steps. It created four or five phases, sorry, each in a to-do list style. And then I created a progress.txt file. And this originally was empty. But then I ran my Ralph loop and the agent essentially after every checkpoint, after every single to-do list item was fulfilled, it would document all the changes, all the code it made. The progress.txt txt file is exactly that, the progress checkpoint where the agent can check where it left off. So let's say you end the loop and you rerun the loop, then the agent knows exactly what the last thing it is it worked on and it can continue off that versus having to rebuild everything again. Here is my Ralph script. And here's the thing, I used AI to write this. I did not write this by hand. I worked with Claude code to make sure it's exactly to my liking. Now, here's how my setup works. I basically call Ralph.sh and then I have a couple flags. If I just run it as it is, there's a couple things that are going to go on in the background. After every feature, the claw agent is going to write tests. It's going to run the test and check that the test pass. And then it's going to ru...
</details>
