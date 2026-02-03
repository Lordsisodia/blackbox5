# Claude Code Task System: ANTI-HYPE Agentic Coding (Advanced)

**Creator:** IndyDevDan
**Video ID:** 4_2j5wgt_ds
**URL:** https://youtube.com/watch?v=4_2j5wgt_ds
**Duration:** ~28 minutes (1706 seconds)
**Published:** February 2, 2026

---

## Executive Summary

This video by IndyDevDan introduces the Claude Code Task System as a paradigm shift in agentic coding that enables reliable multi-agent orchestration. Unlike hype-driven tools like "Moltbot" or "Clawdbot," the Task System provides engineers with foundational primitives (task create, task get, task list, task update) to build organized teams of specialized agents. The core innovation demonstrated is combining three powerful concepts: self-validation (agents checking their own work), agent orchestration (builder-validator agent pairs working in parallel with dependency management), and templating (metaprompts that generate consistent, vetted prompts). This approach represents "anti-hype" agentic engineering—teaching agents how to build as you would, rather than vibe-coding and hoping for the best. The video provides two production-ready prompts (a template metaprompt for planning and an orchestration prompt for team composition) that viewers can immediately deploy to create teams of builder and validator agents that communicate through the task system.

**Who this is for:** Engineers who want to move beyond simple prompting and build scalable, reliable multi-agent workflows. Those interested in the foundational primitives of agentic coding rather than hype-driven abstractions.

**What you'll learn:** How to use Claude Code's Task System tools (task create, task get, task list, task update) to orchestrate teams of specialized agents; how to implement builder-validator agent pairs for increased reliability; how to build self-validating agents with hooks; and how to create template metaprompts that generate consistent, reusable prompts.

---

## All Concepts Rated 0-100

### [98/100] Claude Code Task System
**One-sentence summary:** A standardized task management system within Claude Code that enables agents to create, update, list, and get tasks, facilitating reliable multi-agent communication and orchestration.

**Full explanation:** The Task System is the foundational infrastructure that makes multi-agent orchestration possible in Claude Code. It consists of four core tools: `task create`, `task get`, `task list`, and `task update`. These tools allow agents to communicate with each other through a shared task list, set up dependencies between tasks, and manage parallel execution. Unlike previous approaches that relied on ad-hoc subagent calls without coordination, the Task System provides structured communication channels. When a subagent completes work, it updates its task status, which can trigger dependent tasks to start. This eliminates the need for bash sleep loops and manual coordination. The system is particularly powerful because it enables massively longer-running threads of work—the primary agent can orchestrate a large task list, kick it off, and receive real-time events as subagents complete their work.

**Specific evidence from video:**
- "The new cla code task system is going under the radar in a massive way, probably because of all the cloud pot hype. But this feature hints at the future of engineering work."
- "You can see we have five more pending. So a lot of work is getting stacked up here. And now we're getting the dependency blockers."
- "Task update is obviously the big one. You'll create a task and then update the task with additional details. The powerful thing about this is that your primary agent and your sub agents can use these tools to communicate to each other."
- "This allows for massively longer running threads of work because your primary agent can orchestrate a massive task list, kick it off, and then as agents complete it will receive specific events."

---

### [97/100] Builder-Validator Agent Pattern
**One-sentence summary:** A foundational two-agent team structure where a builder agent performs work and a validator agent checks that work, effectively doubling compute to increase trust in outputs.

**Full explanation:** The builder-validator pattern is presented as the simplest yet most powerful team composition for agentic workflows. The builder agent focuses on one task: building the requested output and reporting its work. The validator agent then checks that the work was done properly. This pattern is described as "2xing the compute for every single task so that we build and then we validate." The builder can include micro-validation (like running ruff and ty on Python files via post-tool-use hooks), while the validator performs higher-level validation (like compilation checks). This creates a closed feedback loop where work is both produced and verified. The pattern is particularly effective because it separates concerns—builders can focus purely on creation while validators focus purely on quality assurance. This is analogous to human engineering workflows where code is written and then reviewed.

**Specific evidence from video:**
- "I have two specific agents that I'm using in this workflow. And I think this is going to be the most like foundational like bare minimum that you're going to want to have set up. A builder and a validator. An agent that does the work and an agent that checks the work."
- "We're basically increasing our compute to increase the trust we have that the work was delivered."
- "The purpose of the builder is just to focus on that one task to build it and then to report its work. But our builder goes a little further... it's going to run its own code checkers basically"
- "We have a builder and we have a validator. The purpose of the builder is just to focus on that one task to build it and then to report its work."
- "create groups of agents for each hook, one builder and one validator."

---

### [96/100] Template Metaprompt
**One-sentence summary:** A prompt that generates another prompt in a specific, highly vetted, consistent format—teaching agents to build as you would.

**Full explanation:** A template metaprompt is a higher-order prompt that outputs a fully-formed, structured prompt following a specific format. This is contrasted with "vibe coding" or "slop engineering" where you prompt a tool and hope for the best. The template approach ensures consistent, predictable outputs because the generated prompt follows a vetted structure. In the video, the template metaprompt includes embedded prompts within its plan format—the agent fills in variables to generate the final prompt. This allows engineers to encode their engineering knowledge into reusable formulas. The metaprompt demonstrated includes sections for purpose, variables, prompt format, orchestration instructions, team orchestration, workflow steps, and validation commands. By using templating, you ensure that every generated prompt follows your established best practices.

**Specific evidence from video:**
- "This metaprompt is actually a template metaprompt. This is a big idea we talk about in tactical agentic coding. We're teaching our agents how to build as we would."
- "You can see here we have a plan format and the plan format actually has embedded prompts inside of it. Replace nested content with the actual request inside of it."
- "This is a prompt that generates a new prompt in a very specific, highly vetted consistent format."
- "This is the big difference between a gentic engineering and vibe coding and slop engineering."
- "If you're doing real engineering work, you want to be going the opposite direction. You want to know the outcome that your agent is generating for you."

---

### [95/100] Task System Tools (task create, task get, task list, task update)
**One-sentence summary:** The four core functions that enable agent-to-agent communication through a shared task list.

**Full explanation:** These four tools form the API of the Claude Code Task System. `task create` initializes new tasks with properties like owner, status, and dependencies. `task get` retrieves specific task information. `task list` shows all tasks and their current states. `task update` is the most critical tool—it allows agents to update task status, add metadata, and communicate results. The primary agent uses these tools to orchestrate subagents, while subagents use them to report completion and unblock dependent tasks. This creates a communication protocol where agents don't need to directly message each other—they communicate through the shared task state. The dependency system allows tasks to be blocked by other tasks, creating ordered execution workflows.

**Specific evidence from video:**
- "There's task create, there's task get, we have task list, and we have task update. Task update is obviously the big one."
- "The powerful thing about this is that your primary agent and your sub agents can use these tools to communicate to each other. That's what's happening here with these four tools."
- "Not only is our agent planning out work, building a team, it's also setting up the tasks and the order that the tasks need to operate in."
- "Task update is going to be the big one because this allows the sub agents and the primary agent to communicate the work."

---

### [94/100] Self-Validation with Hooks
**One-sentence summary:** Embedding validation scripts into agent hooks (like stop hooks or post-tool-use hooks) so agents automatically verify their own work.

**Full explanation:** Self-validation is the practice of building validation directly into agent execution through hooks. The video demonstrates two validation scripts: `validate_new_file` (ensures a file of specific type was created in a specific directory) and `validate_file_contains` (ensures the file contains specific content). These run on the stop hook, meaning the agent validates its work immediately upon completion. Additionally, the builder agent example shows post-tool-use hooks that run ruff and ty on Python files after edits. This creates a micro-validation layer within the agent itself, catching errors immediately rather than waiting for a separate validation step. Self-validation ensures that agents don't just complete tasks—they complete them correctly.

**Specific evidence from video:**
- "This agent is self validating. In fact, it has specialized scripts that it uses to validate its own work. You can see here we have validate new file and we have validate file contains."
- "So on the stop hook once this agent finishes running, it's going to make sure that it created a file of a specific type in a specific directory and it's going to make sure that it contains specific content."
- "This is very powerful. Now we know for a fact that this plan was created."
- "You can now build specialized self validation into every one of your agents. You can see here my builder agent after it runs. So on post tool use, write edit, it's going to look to see if it's operating in a Python file and then it's going to run rough and ty."

---

### [93/100] Agent Orchestration / Primary Agent as Conductor
**One-sentence summary:** The pattern of having a primary agent that creates plans, builds teams, and conducts subagents through the task system rather than doing all work itself.

**Full explanation:** Agent orchestration is the practice of having a primary agent that doesn't do the actual building work itself, but instead creates plans, assembles teams of specialized agents, and coordinates their execution. The primary agent acts as a conductor, using the task system to delegate work to subagents and monitor their progress. This is a fundamental shift from single-agent workflows where one agent tries to do everything. The orchestration approach allows for parallel execution (multiple agents working simultaneously), specialized focus (each agent does one thing well), and better resource utilization (focused context windows). The primary agent can react to events in real-time as subagents complete tasks, making dynamic adjustments to the plan.

**Specific evidence from video:**
- "This primary agent that is actually creating this plan is going to build a team and then give each team member a task step by step."
- "Your primary agent when they're working with this task list, when they're working with your agent teams, they are orchestrating."
- "You have a base agent. Then you learn how to use it better by context engineering and prompt engineering. And then you add more agents. Very powerful. After you add more agents, you customize them. And then lastly, you add an orchestrator agent to help you conduct all of them."
- "This is a new paradigm of multi- aent orchestration that's emerging."

---

### [92/100] Orchestration Prompt
**One-sentence summary:** A high-level prompt passed to the planning agent that guides how it composes teams and assigns work.

**Full explanation:** The orchestration prompt is a meta-level instruction that tells the primary planning agent how to structure its teams. Unlike the template metaprompt (which defines the output format), the orchestration prompt defines team composition strategy. In the video example, the orchestration prompt instructs: "create groups of agents for each hook, one builder and one validator." This gives the planning agent constraints and guidance for team building without micromanaging the specific assignments. The orchestration prompt is passed alongside the user request, allowing flexibility in how teams are structured for different types of work. This separation of concerns (template format vs. team strategy) makes the system more reusable.

**Specific evidence from video:**
- "If the orchestration prompt is provided like we passed in, that orchestration prompt is actually going to help guide how the planner builds the team."
- "create groups of agents for each hook, one builder and one validator. All right, so this is our orchestration prompt. This is our highle prompt that gets boiled down into a low-level prompt thanks to our metaprompt."
- "In the orchestrator prompt, we're actually helping our agent guide how to build the team that does the work."

---

### [90/100] Task Dependencies and Blockers
**One-sentence summary:** The ability to specify that certain tasks cannot start until other tasks complete, enabling ordered execution workflows.

**Full explanation:** Task dependencies allow agents to define execution order through the `addBlockedBy` and `addBlocks` properties in the task system. When a task is created with blockers, it remains in a pending state until the blocking tasks are completed. This is essential for workflows where certain steps must happen before others (e.g., validation must happen after building). The video shows tasks 1-6 running in parallel (building hooks) while subsequent validation tasks are blocked until their corresponding build tasks complete. This dependency system enables complex workflows with parallel and sequential phases without manual coordination.

**Specific evidence from video:**
- "Not only is our agent planning out work, building a team, it's also setting up the tasks and the order that the tasks need to operate in."
- "So you can see here our first five or six tasks. These can run in parallel. They're building out the brand new hooks."
- "Your agents will start working on it. The agents will then complete their work and then the blocked tasks are now unblocked and the agents will continue working through those piece by piece"
- "This is vastly superior to the previous generation to-do list and previous generation sub aent colon via the task tool because you can set up tasks that run in specific order that block and that depend on other tasks to be complete."

---

### [88/100] Focused Context Windows (Lesson 6 Tactic)
**One-sentence summary:** The principle that agents with focused context windows doing one specific thing perform better than agents with broad contexts trying to do everything.

**Full explanation:** This is a fundamental principle of agentic engineering: specialization beats generalization. When each agent has a narrow, focused context window dedicated to a single task, it performs that task better than a generalist agent with a broad context. The multi-agent task system is perfect for this approach because it allows you to spin up many specialized agents rather than one agent trying to juggle everything. Each builder agent in the video example focuses on just one hook implementation, with only the relevant context for that specific task. This reduces cognitive load on each agent and improves output quality.

**Specific evidence from video:**
- "Every one of your agents has a focused context window doing one thing extraordinarily well. This is something we talk about all the time in tactical agentic coding. This is the lesson six tactic."
- "The more agents you have with focus context windows doing one specific thing, the better."
- "This multi- aent task system is perfect for that."

---

### [87/100] Team Task List with Owners
**One-sentence summary:** A task list where every task has a specific assigned owner (agent), enabling clear responsibility and parallel execution.

**Full explanation:** Unlike ordinary subagent prompts where work is assigned ad-hoc, the team task list explicitly assigns an owner to every task. This creates clear lines of responsibility and enables the system to track who is doing what. The video shows tasks with specific team members assigned: "Dan A4 EC 608 built out your post tool used failure hook," "A249 B56 built out the session end hook," etc. Each task owner is a specialized agent (either builder or validator) with a specific focus. This ownership model enables parallel execution because multiple agents can work on their assigned tasks simultaneously.

**Specific evidence from video:**
- "We have a team task list. Every task has an owner. All right. So this is not an ordinary sub aent prompt. This task list has specific team members doing specific work all the way through."
- "Dan A4 EC 608 built out your post tool used failure hook so error handling works smoothly now. A249 B56 built out the session end hook implementation and it's ready to go."
- "Every sub aent that completes is going to summarize their work as well."

---

### [85/100] Reusable Prompts / AI Developer Workflows (ADWs)
**One-sentence summary:** Building prompts as reusable assets that can be deployed repeatedly rather than one-off prompts for single tasks.

**Full explanation:** The video emphasizes building reusable prompts and skills rather than ad-hoc prompting. A reusable prompt is designed to be run "over and over and over" with different inputs. The template metaprompt is the ultimate example—it generates plans for any type of work following the same structure. This approach treats prompts as infrastructure rather than disposable commands. The concept of "AI Developer Workflows" (ADWs) from Tactical Agentic Coding is referenced—these are reusable, vetted workflows that encode engineering best practices. By investing upfront in building high-quality reusable prompts, engineers get compounding returns every time they use them.

**Specific evidence from video:**
- "It's always one thing to just open up a terminal and start prompting something, but we can do much much better than this, right? Build reusable prompts, build reusable skills."
- "It only takes one time to build out a great prompt, right? Just that upfront investment is really where you want to be spending more and more of your time."
- "As mentioned in tactical agentic coding, you want to be building the agentic layer of your code base. Don't work on the application anymore. Work on the agents that build the application for you."
- "Build reusable prompts, build reusable skills."

---

### [84/100] Agentic Layer of Codebase
**One-sentence summary:** The concept of building infrastructure for agents (prompts, hooks, specialized agents) as a distinct layer of your codebase, separate from application code.

**Full explanation:** The "agentic layer" is the infrastructure and tooling built specifically to support agentic workflows. This includes reusable prompts, specialized agent definitions, hooks, validation scripts, and orchestration logic. Rather than just using agents to write application code, you invest in building systems that make agents more effective. The video's example of the `.claude/agents/team/` directory containing builder and validator agent definitions is part of the agentic layer. This layer is treated as first-class infrastructure that gets maintained and improved over time, just like any other part of the codebase.

**Specific evidence from video:**
- "As mentioned in tactical agentic coding, you want to be building the agentic layer of your code base. Don't work on the application anymore. Work on the agents that build the application for you."
- "If we open up this directory here.Cloud agents team, you can see I have just two teammates, right? Two specific types of agents that this codebase has access to."
- "This is a huge stepping stone from just calling ad hoc sub aents without a common mission without task dependencies and without a way to communicate to each agent that the work is or isn't done yet."

---

### [82/100] Text-to-Speech Subagent Responses
**One-sentence summary:** Configuring subagents to provide audio feedback when they complete tasks, giving real-time awareness of parallel work progress.

**Full explanation:** The video demonstrates a quality-of-life feature where subagents are configured to speak their completion status via text-to-speech. When a subagent finishes its task, it announces: "Dan A4 EC 608 built out your post tool used failure hook so error handling works smoothly now." This provides immediate auditory feedback about parallel work progress without needing to constantly check the terminal. While not core to the functionality, it demonstrates how the task system enables real-time awareness of distributed agent activity.

**Specific evidence from video:**
- "So, you're hearing our sub agent text to speech responses. Those are going to keep streaming in here."
- "Dan A4 EC 608 built out your post tool used failure hook so error handling works smoothly now. A249 B56 built out the session end hook implementation and it's ready to go."
- "Every sub aent that completes is going to summarize their work as well. So I have this built into the sub agent stop hook"

---

### [80/100] Planning vs. Reviewing as Primary Constraints
**One-sentence summary:** In agentic engineering, most time should be spent on planning (what to build and how) and reviewing (verifying outputs), with agents handling the actual building.

**Full explanation:** The video identifies planning and reviewing as the two primary constraints in agentic coding. Engineers should focus their energy on these activities rather than the actual building, which agents can handle. The Task System and template metaprompt directly address the planning constraint by enabling systematic, organized planning with specialized agents. The builder-validator pattern addresses the reviewing constraint by embedding validation into the workflow. This represents a shift in engineering work—humans focus on strategy and quality assurance while agents handle implementation.

**Specific evidence from video:**
- "Specifically with agentic coding there are two primary constraints. Planning and reviewing. you're probably spending most of your time planning or reviewing if you're doing things right, if you're doing true agentic engineering."
- "This prompt, this new set of tools really helps us in the planning phase. We can build out specialized agents that are again self- validating."

---

### [78/100] Thread-Based Engineering
**One-sentence summary:** A mental framework where work is organized into threads (parallel streams of execution) that can run simultaneously and communicate through shared state.

**Full explanation:** Thread-based engineering is presented as a powerful mental model for understanding multi-agent work. Just as software uses threads for parallel processing, agentic workflows can be thought of as threads of work that run concurrently. The Task System enables this by allowing multiple agents (threads) to work in parallel, with the ability to synchronize through task dependencies. This is contrasted with sequential workflows where one agent must finish before another starts. The thread model helps engineers think about how to decompose work into parallelizable units.

**Specific evidence from video:**
- "Notice how this is looking a lot like the agent threads that we talked about a couple of weeks ago. You know, thread-based engineering is a powerful mental framework to think about how work gets complete. And we're seeing that here with this multi- aent task system."
- "So, you know, same type of workflow, right? You kick off a larger plan, a larger set of work. Your agents will start working on it."

---

### [75/100] The Core Four (Context, Model, Prompt, Tools)
**One-sentence summary:** The four fundamental levers of agentic coding that engineers should master: context engineering, model selection, prompt engineering, and tool usage.

**Full explanation:** The video emphasizes understanding the foundational primitives of agentic coding rather than relying on high-level abstractions. The "Core Four" are: (1) Context—what information the agent has access to, (2) Model—which AI model is being used and its capabilities, (3) Prompt—the instructions given to the agent, and (4) Tools—the capabilities and functions available to the agent. Mastering these fundamentals allows engineers to move between tools and adapt to new features, rather than being locked into specific high-level abstractions.

**Specific evidence from video:**
- "if you're trying to learn how to build with agents, it's all about the core four context, model, prompt, and tools. And it's about learning to leverage these fundamental levers of agentic coding, the fundamental pieces of building with agents."
- "These are just tools and prompts. This entire feature set is just tools and prompts. So if we needed to, if you wanted to, we could step away from cloud code. We could build it into another tool if needed."

---

### [72/100] Validation Commands (validate_new_file, validate_file_contains)
**One-sentence summary:** Specific validation scripts that check for file existence, location, and content as part of self-validation.

**Full explanation:** The video shows two concrete validation commands used in the stop hook: `validate_new_file` checks that a file of a specific type was created in a specific directory, and `validate_file_contains` verifies that the file contains specific required content. These are implemented as shell scripts that return success or failure. If validation fails, the script provides feedback that the agent can use to correct its work. This creates a closed validation loop without human intervention.

**Specific evidence from video:**
- "You can see here we have validate new file and we have validate file contains. So on the stop hook once this agent finishes running, it's going to make sure that it created a file of a specific type in a specific directory and it's going to make sure that it contains specific content."
- "It's running validate file contains. It's making sure that it's in the specs directory, which obviously it is here. It's a markdown file and it contains these sub points."

---

### [70/100] /slash Commands (/plan, /bu)
**One-sentence summary:** Custom slash commands in Claude Code that trigger specific prompts or workflows.

**Full explanation:** The video references using `/plan` and `/bu` (build) as custom slash commands. These are shortcuts that invoke specific prompts—`/plan` triggers the planning metaprompt, and `/bu` triggers the build execution. Slash commands provide a convenient interface for triggering complex agentic workflows without pasting full prompts each time. They represent the user-facing entry points into the agentic layer.

**Specific evidence from video:**
- "We will slash plan, but this isn't an ordinary plan. We're going to plan with a team."
- "We're going to use a /bu prompt. And now you'll notice here it is building up that brand new task list."

---

### [68/100] Anti-Hype / Fundamentals-First Approach
**One-sentence summary:** The philosophy of focusing on foundational primitives and understanding how things work rather than using high-level hype-driven tools without comprehension.

**Full explanation:** The video takes a strong stance against "hype-driven" tools like Moltbot/Clawdbot that abstract away the underlying mechanics. The argument is that engineers who understand the fundamentals (the Core Four) can adapt to any tool, while those who rely on high-level abstractions without understanding will be limited. This "anti-hype" approach values knowing what your agents are doing and teaching them how to build as you would. It's about being a true "agentic engineer" rather than a "vibe coder."

**Specific evidence from video:**
- "I want to focus on this in a very anti-hype way."
- "This isn't about hype or vibe coding - this is ANTI-HYPE advanced agentic coding that actually works."
- "I think there's a lot of hype right now in the tech industry. There's a lot of slop engineering and just vibe slopping"
- "What I'm saying is know how to use the primitives and the leverage points of agentic coding, right? The foundational pieces that make it all up."

---

### [65/100] Claude-P (Permission/Log Commands)
**One-sentence summary:** Commands for checking permissions and viewing logs that can be integrated into validation workflows.

**Full explanation:** The video briefly mentions `claude-p` as a command that could be used for validation. While not deeply explained, it appears to be related to checking permissions or log files. The speaker notes a missed opportunity to use `claude-p` in the validation agents to check that log files were created properly. This suggests it's a utility command for introspecting Claude Code's operation.

**Specific evidence from video:**
- "If I search for claw-p, there's a huge opportunity for every validator agent to actually just fire off claw--pey all logs are created in logs slash. We could have built a more tighter closed loop where the agents were validating this log file."
- "We should have had cloud-p messages for every single validation agent."

---

### [60/100] Moltbot/Clawdbot Hype Concerns
**One-sentence summary:** Caution about over-reliance on viral high-level agent tools without understanding the underlying mechanics.

**Full explanation:** The video expresses concern about tools like Moltbot (referred to as "very powerful but very dangerous") that have gone viral. While acknowledging their power, the speaker warns that engineers who use these tools without understanding what's happening underneath are at a disadvantage. The concern is that high-level abstractions can mask important details and lead to over-reliance on black-box systems. This is contrasted with the Task System approach, which uses standardized, accessible primitives.

**Specific evidence from video:**
- "I'm not talking about the very powerful but very dangerous maltbot or previously cloudbot."
- "I am super concerned about an over reliance on tools like this without understanding the pieces of it."
- "I think if you're a agentic engineer, if you're an engineer that has been learning to really use agents and build proficient systems that operate with and without you, you know, go crazy with tools like this. You know what's happening underneath the hood. It's more of everyone else that I'm worried about"

---

## Complete Command Reference

| Rating | Command/Tool | Syntax/Usage | What It Does | When to Use |
|--------|--------------|--------------|--------------|-------------|
| 95 | task create | `task create` with subject, description, status | Creates a new task in the task system | When primary agent needs to assign work to subagents |
| 95 | task update | `task update` with taskId, status, metadata | Updates task status and adds details | When subagents complete work or need to communicate progress |
| 95 | task get | `task get` with taskId | Retrieves specific task information | When agent needs to check details of a specific task |
| 95 | task list | `task list` | Shows all tasks and their current states | When orchestrating to see overall progress |
| 90 | addBlockedBy | `addBlockedBy: ["task-id"]` in task create/update | Specifies tasks that must complete before this one starts | When setting up ordered execution workflows |
| 90 | addBlocks | `addBlocks: ["task-id"]` in task create/update | Specifies tasks that this task blocks | When defining task dependencies |
| 87 | validate_new_file | Shell script: validates file creation | Ensures file of specific type exists in specific directory | In stop hooks for self-validation |
| 87 | validate_file_contains | Shell script: validates file content | Ensures file contains required content/strings | In stop hooks for self-validation |
| 72 | ruff + ty | Post-tool-use hook commands | Runs Python linting and type checking | In builder agents after Python file edits |
| 70 | /plan | Slash command | Triggers the planning metaprompt | Starting a new planning workflow |
| 70 | /bu | Slash command | Triggers the build execution | Executing a generated plan |
| 65 | claude-p | Command (details unclear) | Checks permissions or logs | Potentially in validation workflows |
| 60 | gs | Git status shortcut | Shows git status | Checking what files changed |
| 60 | gdf | Git diff shortcut | Shows git diff | Reviewing changes made by agents |

---

## Key Techniques

### Technique 1: Setting Up Builder-Validator Agent Teams

**Prerequisites:**
- Claude Code with Task System enabled
- Agent definition files for builder and validator agents
- Validation scripts (validate_new_file, validate_file_contains)

**Steps:**
1. Create builder agent definition with post-tool-use hooks for micro-validation (e.g., ruff, ty for Python)
2. Create validator agent definition focused on checking work (compilation, tests, etc.)
3. Store agent definitions in `.claude/agents/team/` directory
4. Use orchestration prompt to instruct planner: "create groups of agents for each [work unit], one builder and one validator"
5. Execute planning metaprompt which will generate a plan with paired builder-validator tasks
6. Run the generated plan—the task system will handle parallel execution and dependency management

**Example from video:**
```
Team Members:
- session_end_builder: builds session end hook
- session_end_validator: validates session end hook
- permission_request_builder: builds permission request hook
- permission_request_validator: validates permission request hook
```

**Common pitfalls:**
- Not setting up proper task dependencies (validators should be blocked by builders)
- Insufficient validation in builder agents (missed opportunity to catch errors early)
- Not using orchestration prompt to guide team composition

---

### Technique 2: Creating a Template Metaprompt

**Prerequisites:**
- Understanding of your standard plan format
- Clear variable definitions for what changes between plans

**Steps:**
1. Define the fixed structure of your plans (purpose, variables, format, orchestration, workflow, validation)
2. Identify template variables (e.g., `{{TASK_NAME}}`, `{{OBJECTIVE}}`, `{{TEAM_MEMBERS}}`)
3. Create the metaprompt with explicit instructions to "replace nested content with actual request"
4. Include team orchestration section with task system tool descriptions
5. Add validation commands section with specific scripts to run
6. Test by running the metaprompt with sample inputs
7. Verify output format using validate_file_contains on the generated plan

**Example structure from video:**
```
## Plan Format

### {{TASK_NAME}}

**Objective:** {{OBJECTIVE}}

**Team Members:**
{{TEAM_MEMBERS}}

**Step-by-Step Tasks:**
{{TASKS}}

**Validation Commands:**
{{VALIDATION}}
```

**Common pitfalls:**
- Not making template variables explicit enough
- Forgetting to include task system tool descriptions
- Missing validation section in generated output

---

### Technique 3: Implementing Self-Validation with Hooks

**Prerequisites:**
- Claude Code hooks system enabled
- Validation scripts written and tested

**Steps:**
1. Write validation scripts (e.g., `validate_new_file.sh`, `validate_file_contains.sh`)
2. Configure stop hook to run validation scripts
3. Configure post-tool-use hooks for micro-validation (e.g., after Write or Edit tools)
4. Ensure validation scripts provide actionable feedback on failure
5. Test with intentional failures to verify feedback loop works

**Example from video:**
```yaml
hooks:
  post_tool_use:
    Write:
      - command: |
          if [[ "${file_path}" == *.py ]]; then
            ruff check "${file_path}"
            ty "${file_path}"
          fi
  stop:
    - command: validate_new_file
    - command: validate_file_contains
```

**Common pitfalls:**
- Validation scripts that don't provide clear feedback on failure
- Hooks that run on wrong triggers (e.g., validating before file is written)
- Not testing validation with intentional failures

---

### Technique 4: Orchestrating Multi-Agent Workflows

**Prerequisites:**
- Template metaprompt created
- Orchestration prompt prepared
- Agent team definitions ready

**Steps:**
1. Prepare user prompt describing what to build
2. Prepare orchestration prompt describing team composition strategy
3. Run planning metaprompt with both prompts
4. Review generated plan for proper task dependencies
5. Execute plan using /bu or equivalent command
6. Monitor task list for progress
7. Review completed work and validation results

**Example workflow from video:**
```
User: "Update documentation for new Claude Code hooks"
Orchestration: "create groups of agents for each hook, one builder and one validator"

→ Planner generates plan with 6 builder tasks + 6 validator tasks
→ Builders run in parallel (tasks 1-6)
→ Validators blocked until builders complete
→ Final documentation update task blocked until all validation passes
```

**Common pitfalls:**
- Not setting up proper blocking dependencies
- Primary agent trying to do work instead of orchestrating
- Not monitoring task list for blocked or failed tasks

---

### Technique 5: Building the Agentic Layer

**Prerequisites:**
- Existing codebase to enhance
- Commitment to treating agent infrastructure as first-class

**Steps:**
1. Create `.claude/agents/` directory structure
2. Define specialized agents (builder, validator, etc.) with focused purposes
3. Create `.claude/prompts/` directory for reusable prompts
4. Build template metaprompts for common workflows
5. Create validation scripts in `.claude/scripts/`
6. Document the agentic layer (how to use prompts, available agents, etc.)
7. Iterate on prompts based on usage patterns

**Directory structure from video:**
```
.claude/
├── agents/
│   └── team/
│       ├── builder.md
│       └── validator.md
├── prompts/
│   ├── plan-with-team.md
│   └── orchestrator.md
└── scripts/
    ├── validate_new_file.sh
    └── validate_file_contains.sh
```

**Common pitfalls:**
- Treating prompts as disposable rather than reusable assets
- Not versioning agent definitions
- Not documenting how to use the agentic layer

---

## Synthesis: What Matters Most

### Tier 1 (90-100): Must Know

These concepts are fundamental to effective use of the Claude Code Task System:

1. **Claude Code Task System (98/100)** - The core infrastructure enabling multi-agent orchestration through task create/get/list/update tools.

2. **Builder-Validator Agent Pattern (97/100)** - The foundational team structure: one agent builds, another validates. Doubles compute for increased trust.

3. **Template Metaprompt (96/100)** - Prompts that generate prompts in consistent, vetted formats. Essential for reusable, predictable workflows.

4. **Task System Tools (95/100)** - task create, task get, task list, task update. The API for agent-to-agent communication.

5. **Self-Validation with Hooks (94/100)** - Embedding validation into agent execution through stop hooks and post-tool-use hooks.

6. **Agent Orchestration (93/100)** - Primary agent as conductor, creating plans and coordinating subagents rather than doing all work itself.

7. **Orchestration Prompt (92/100)** - High-level guidance for how the planner should compose teams.

8. **Task Dependencies and Blockers (90/100)** - Setting up ordered execution where tasks wait for prerequisites to complete.

---

### Tier 2 (80-89): Very Important

These concepts significantly enhance effectiveness but build on Tier 1 fundamentals:

9. **Focused Context Windows (88/100)** - Specialized agents with narrow context perform better than generalists.

10. **Team Task List with Owners (87/100)** - Explicit task ownership enables clear responsibility and parallel execution.

11. **Reusable Prompts / ADWs (85/100)** - Building prompts as reusable infrastructure rather than disposable commands.

12. **Agentic Layer of Codebase (84/100)** - Treating agent infrastructure (prompts, hooks, agents) as first-class codebase components.

13. **Text-to-Speech Subagent Responses (82/100)** - Audio feedback for real-time awareness of parallel work.

14. **Planning vs. Reviewing Constraints (80/100)** - Engineers should focus on planning and reviewing; agents handle building.

---

### Tier 3 (70-79): Good to Know

These concepts provide useful context and mental models:

15. **Thread-Based Engineering (78/100)** - Mental model of parallel agent work as threads.

16. **The Core Four (75/100)** - Context, Model, Prompt, Tools—the fundamental levers of agentic coding.

17. **Validation Commands (72/100)** - Specific scripts like validate_new_file and validate_file_contains.

---

## Action Checklist

### Immediate Actions (Do Today)

- [ ] **Enable Task System in Claude Code** - Ensure you have access to task create, task get, task list, task update tools
- [ ] **Clone the Reference Codebase** - Get the hooks mastery codebase from https://github.com/disler/claude-code-hooks-mastery to see working examples
- [ ] **Create Builder Agent Definition** - Write a builder.md agent file with post-tool-use hooks for your language (e.g., ruff/ty for Python)
- [ ] **Create Validator Agent Definition** - Write a validator.md agent file focused on checking work
- [ ] **Write Validation Scripts** - Create validate_new_file.sh and validate_file_contains.sh scripts

### Short-term Actions (This Week)

- [ ] **Build Template Metaprompt** - Create a metaprompt that generates plans in your preferred format with team orchestration section
- [ ] **Create Orchestration Prompt** - Write a reusable orchestration prompt that guides team composition (e.g., "one builder and one validator per work unit")
- [ ] **Set Up Agent Directory Structure** - Create `.claude/agents/team/` and `.claude/prompts/` directories in your main codebase
- [ ] **Test End-to-End Workflow** - Run a small project through the full workflow: plan with team → build → validate
- [ ] **Document Your Agentic Layer** - Write documentation for your team on available agents, prompts, and how to use them

### Medium-term Actions (This Month)

- [ ] **Expand Agent Types** - Beyond builder/validator, consider QA tester agents, reviewer agents, deploy agents, documentation agents
- [ ] **Build Custom Slash Commands** - Set up /plan, /bu, and other shortcuts for your common workflows
- [ ] **Create Validation Library** - Build a library of validation scripts for different file types and requirements
- [ ] **Iterate on Prompts** - Based on usage, refine your metaprompts to improve output quality
- [ ] **Share with Team** - Ensure team members understand and can use the agentic layer

### Ongoing Practices

- [ ] **Invest in Prompts** - Spend more time upfront building great reusable prompts
- [ ] **Focus on Planning and Reviewing** - Let agents handle building; focus your energy on planning and quality assurance
- [ ] **Stay Close to Fundamentals** - Understand the Core Four (Context, Model, Prompt, Tools) rather than relying on black-box abstractions
- [ ] **Build the Agentic Layer** - Continuously improve your agent infrastructure as a first-class part of your codebase
- [ ] **Teach Agents to Build as You Would** - Use templating to encode your engineering knowledge into reusable formulas

---

## Full Transcript

<details>
<summary>Click to expand full transcript (851 segments)</summary>

We're entering a new paradigm of agentic coding. And I'm not talking about the very powerful but very dangerous maltbot or previously cloudbot. More on that later. I'm talking about new tools for engineers to orchestrate intelligence. The new cla code task system is going under the radar in a massive way, probably because of all the cloud pot hype. But this feature hints at the future of engineering work. I have two prompts to show you that you can use to extend your ability to build with agents and it's all based on this new cloud code task system. This changes the workflow of engineering in a pretty significant way and really it's not getting enough attention. So I want to focus on this in a very anti-hype way. I have one metaprompt and one plan to share with you that can really push what you can do with agents in a cloud code instance. We will slash plan, but this isn't an ordinary plan. We're going to plan with a team. We have a user prompt and an orchestrator prompt. I'm going to jump through this and fill this out. Paste and paste. I'll explain what this does further on. Feel free to pause the video if you want. I'll fire this off. This prompt will showcase you can now reliably and consistently create teams of agents. More agents, more autonomy, and more compute doesn't always mean better outcomes. What we want is more organized agents that can communicate together to work toward a common goal. If you want to understand how to use the cloud code task system at scale reliably and consistently to create teams of agents, stick around and let's jump right in. Let's take a look at plan with team. This isn't like most prompts you've seen. This prompt has three powerful components to it. Self- validation, agent orchestration, and templating. The first thing you'll notice here is that we have hooks in the front matter. This agent is self validating. In fact, it has specialized scripts that it uses to validate its own work. You can see here we have validate new file and we have validate file contains. So on the stop hook once this agent finishes running, it's going to make sure that it created a file of a specific type in a specific directory and it's going to make sure that it contains specific content. This is very powerful. Now we know for a fact that this plan was created. And in fact, we should be able to see that right now. If we close this, we can see that our plan has been created and it's been validated. And so now the next step is we're going to actually kick this off. And you can see our agent has done something really interesting here. We have a team task list. Every task has an owner. All right. So this is not an ordinary sub aent prompt. This task list has specific team members doing specific work all the way through. and we're using two specific types of agents. We're going to break down in just a second a builder agent and a validator agent. We're going to go ahead and kick off this prompt and we're going to actually start building this out. We'll look at the spec. This is the second prompt that we're going to look at and we're going to understand why this generated prompt from our meta prompt is so unique. Let's just go ahead and kick this off. Get this building in the background. We're going to use a /bu prompt. And now you'll notice here it is building up that brand new task list. And so it's just going to keep stacking on the brand new task list. We're also going to look at the actual tools that this agent is running to put together this team of agent and to communicate the results. You can see we have five more pending. So a lot of work is getting stacked up here. And now we're getting the dependency blockers. Not only is our agent planning out work, building a team, it's also setting up the tasks and the order that the tasks need to operate in. So you can see here our first five or six tasks. These can run in parallel. They're building out the brand new hooks. And so to be clear here, what we're doing is I have this code base on my repo cloud code hooks mastery. Last update was five or six months ago. So we're going to go ahead and update the documentation and update some of the code. Right? So this is a very common engineering workflow that you would run that you would enhance with agents. You need to update old code to update and reflect changes and new documentation. So that's what we're doing here. Right now we're kicking off a bunch of agents to run in parallel. >> Dan A4 EC 608 built out your post tool used failure hook so error handling works smoothly now. A249 B56 built out the session end hook implementation and it's ready to go. >> All right, so you're hearing our sub agent text to speech responses. Those are going to keep streaming in here. So it might be >> agent A7A 26A nailed it. >> It might be a little annoying. It's going to interrupt us a bunch here, but every sub aent that completes is going to summarize their work as well. So I have this built into the sub agent stop hook >> a356. Got your setup hook implementation done. Hook setup.py PI file is ready and Dan A1FA9A7 built your permission and it's ready to handle authorization. >> Awesome. This work is just going to continue to stream in. The next important piece is of course agent orchestration. If we collapse everything here, you can see a classic agentic prompt format. We have our purpose. We have our list of variables. You can see our prompt format and our orchestration prompt. We have our instructions. This is where things get really interesting. Inside of the instructions, we have an additional new block, team orchestration. And so here we're starting to detail these new task management tools. Task create, update, list, and git. This is how the task system works. This is everything that our primary agent needs to conduct, control, and orchestrate all possible sub aents, right? The communication happens through this task list. This is a huge stepping stone from just calling ad hoc sub aents without a common mission without task dependencies and without a way to communicate to each agent that the work is or isn't done yet. We're detailing some things there. But what's really important here is in our workflow. If we look at our agentic prompt format here where we're detailing the steps that we want our plan with team prompt to set up, um we can see something really interesting here. In step four and five, we're doing two important things. We're defining team members using the orchestration prompt if provided and we're defining stepby-step tasks. So our plan is going to use team orchestration. So this primary agent that is actually creating this plan is going to build a team and then give each team member a task step by step. All right. So this is, you know, unique in that our previous planning prompts that we would set up that create the plans for us that research the codebase, we would have to specify exactly what agent was running, exactly how we wanted to specialize that workflow, and then it would run in some topto bottom format that you would have to strictly organize. Now, with teams and with the task list, we can teach our primary agent how to create plans that also contain individual team members. And then the last very important piece of this prompt is that we are templating. So this metaprompt is actually a template metaprompt. This is a big idea we talk about in tactical agentic coding. We're teaching our agents how to build as we would. You can see here we have a plan format and the plan format actually has embedded prompts inside of it. Replace nested content with the actual request inside of it. So our plan is going to come out to task name. And we can pull up the plan that was generated side by side here. If we open up specs, you can see we have hooks update with team. And if we go side by side, you can see exactly how this is getting templated. Here's the plan name. Here's the task description. And then we're having our agent fill out the task description. So this agent is really building as we would. You want to be teaching your agents how to build like you would, right? This is the big difference between a gentic engineering and vibe coding and slop engineering. When you're running a prompt to a random tool like Clawbot or insert whatever tool, whatever agent, and you don't know what the agent is actually going to do or how it's going to do the work, the results can be anywhere from exactly what you wanted to not so great to this doesn't work at all. As models progress and become more proficient, of course, you'll be able to prompt with less effort, with less thought. But if you're doing real engineering work, you want to be going the opposite direction. You want to know the outcome that your agent is generating for you. And you can do that with the template prompt, right? specifically the template meta prompt. This is a prompt that generates a new prompt in a very specific, highly vetted consistent format. And so we can just continue down the line. You can see the objective on both sides here, right? We have our problem statement. We have the solution approach. So on and so forth. But where things get interesting is here. We have team orchestration. If we search for this uh I know for a fact that team orchestration will be inside the generated prompt. Why is that? It's because if we scroll up here, remember that this stop hook ran self validation. And check this out, right? It's running validate file contains. It's making sure that it's in the specs directory, which obviously it is here. It's a markdown file and it contains these sub points. So, I'm making absolute sure that the file that was generated has the correct section. If it doesn't, this script here, validate file contains, is going to spit back out instructions for this planner agent. Right? So, this is very, very powerful. We're combining specialized self validation, which we've covered in a previous video, with this new team orchestration with powerful templating. Okay? And again, templating is something we discuss at length in tactical agent coding because it allows you to teach your agents to build like you would. But this team orchestration section is very, very powerful. So, let's go and just take a look at this. You can see here this is part of a template, but it's, you know, just raw text. So, our agent copied it as is per the instructions. But then here our agent starts building out the team members. And so, you know, to be super clear here, just to reiterate this, on the left we have the template metaprompt. And on the right, we have the generated plan file that our agent is running and probably has completed it by now. Okay, look, it's it's already finished, right? 2 minutes of work thanks to that parallel setup. Everything's already done. Hooks configured, complete documentation in the readme. We'll check this out after we finish breaking down this powerful prompt. Right. So, team members, you can see builder, validator, builder, validator, builder, validator, on and on and on. Right? I have two specific agents that I'm using in this workflow. And I think this is going to be the most like foundational like bare minimum that you're going to want to have set up. A builder and a validator. An agent that does the work and an agent that checks the work. I'm 2xing the compute for every single task so that we build and then we validate. We actually push this further. I'll show you the agents in just a second here, but uh you can see here in our prompt template, we have our builder and then we're specifying the name, role, agent type, and if it should resume if something goes wrong. And this is all just about filling in the variables, filling in the specification for the team that's going to execute this work. Okay, we also have the step-by-step tasks, which breaks down the actual workflow. This is the part of the plan where we're just going through step by step and our agents are going through the work that they need to do. And so this is this task list. Just to make this super clear, this is the task list that we're building up, working step by step. And again, we built this into a reusable prompt that we can deploy over and over and over. And so, you know, it's always one thing to just open up a terminal and start prompting something, but we can do much much better than this, right? Build reusable prompts, build reusable skills. I think a lot of engineers in the space, you already understand this as a kind of foundational concept, but you can push it further. Remember this metaprompt has three powerful components. It is self- validating. It is building a team and it has specific instructions on how to build a team. And if the orchestration prompt is provided like we passed in, that orchestration prompt is actually going to help guide how the planner builds the team. All right, so that's where you solve that. And then we're also templating. So this is a template metaprompt. It might sound like a super fancy term, but it's it's not. It's a prompt that generates another prompt in a specific format. All right, it's actually quite simple, but it's very very powerful. This is advanced agentic prompt engineering. But once you see this and once you start building these out, it becomes second nature. Becomes very easy to build out these reusable formulas for success in your engineering work. All right. And you can see what it's built out here for us. Uh a huge prompt. You know, we have all of our validation commands at the bottom as you saw here. We have notes here. You know, again, this is a classic metaprompt. The big difference here is that we are instructing our metaprompt that's going to run over and over and over for us hundreds of times. We're instructing it how to build a team with the new cloud code task system. And so what does the new cloud code task system look like? How is this unique? As mentioned, what we're doing here is we're actually building up a task list and a dedicated team to handle the individual tasks. Now, this is vastly superior to the previous generation to-do list and previous generation sub aent colon via the task tool because you can set up tasks that run in specific order that block and that depend on other tasks to be complete. Okay. And not only that, this allows for massively longer running threads of work because your primary agent can orchestrate a massive task list, kick it off, and then as agents complete it will receive specific events. As sub agents complete work, they will actually ping back to the primary agent that accomplished the work. And the primary agent can react to it in real time. So you don't have to sit, you don't need to add bash, sleep, loops. The task system handles all of that. And now, you know, speaking of the task system, what are the task system key function? So let's just take a look at the key ones, right? There's task create, there's task get, we have task list, and we have task update. Task update is obviously the big one. You'll create a task and then update the task with additional details. The powerful thing about this is that your primary agent and your sub agents can use these tools to communicate to each other. That's what's happening here with these four tools. Task update is going to be the big one because this allows the sub agents and the primary agent to communicate the work. And this unlocks powerful workflows like this. We can now set up multi- aent teams with even more than one primary agent. So, you know, same type of workflow, right? You kick off a larger plan, a larger set of work. Your agents will start working on it. The agents will then complete their work and then the blocked tasks are now unblocked and the agents will continue working through those piece by piece, sending messages that they finished once the task list is complete. And really, as work completes, the primary agents will be alerted. So, you can spin up as many agents as you want. And notice how this is looking a lot like the agent threads that we talked about a couple of weeks ago. You know, thread-based engineering is a powerful mental framework to think about how work gets complete. And we're seeing that here with this multi- aent task system. So, just once again, you prompt your agents. Your agents create a large task list. Your agent teams, right? Your sub agents then accomplish the work in order reviewing, checking each other's work. If you set up the right reviewer agents, and then they unblock the next task, so on and so forth, right? They'll communicate when their work is done. The task list system will ping back to the agent and then your agent will respond to you once the work is done. So this is the powerful taskless system and it becomes even more powerful when you deploy it and build it into a reusable prompt that you can run over and over and over. So what did our agent do for us? It added and update the documentation for this codebase. Let's go ahead and check it out. Let's open up a terminal here. Let's run gs. So you can see all the files changed. You can see we have a bunch of new status lines. We got those new hooks that just weren't there. We updated the readme. We have that new spec. And we have our new JSON file. Let's go ahead and just diff this. And we can see those new hooks there. Session end, permission request, sub aent start, setup, and we have a bunch of new hooks. And every one of these hooks should have their own log file. So keep in mind if we open up this prompt here, let's just understand how these two agents work together. We had our planning agent build a team. Okay? And so why is this different? Why is this more powerful? because you can build specialized agents that do one thing extraordinarily well. All right. So, if we look at the team members here, uh where's that where's that note agent slash here we go. So, team members, this is a variable here and it's something that we detail inside of the workflow. In step four, we say this exactly, right? Use the orchestration prompt to guide team composition. Identify fromcloud agents team markdown. So we're looking at agents only in the specific directory or we're using a generalpurpose agent. And so if we open up this directory here.Cloud agents team, you can see I have just two teammates, right? Two specific types of agents that this codebase has access to. We have a builder and we have a validator. The purpose of the builder is just to focus on that one task to build it and then to report its work. But our builder goes a little further. We covered this in the previous video, but it's so important to keep mentioning this. You can now build specialized self validation into every one of your agents. You can see here my builder agent after it runs. So on post tool use, write edit, it's going to look to see if it's operating in a Python file and then it's going to run rough and ty. So it's going to run its own code checkers basically, right? And these can be any types of code validation that you want. The powerful thing here is that we've kind of built in a micro step of validation inside the builder on its own. And then we have a higher level validator agent that's just going to make sure that the task was done properly, right? Make sure that the code is complete, make sure that it can run whatever validation it needs to validate that the builder did actually do the work. Okay, so I really like this kind of two agent pairing. We're basically increasing our compute to increase the trust we have that the work was delivered. And if we had a specific type of validation, we could also build out tools to give this agent specialized tools to make sure that the builder did his job properly. I think this is probably the simplest team combination you can build. Of course, there are other things, you know, QA tester agents, reviewer agents, deploy agents, blog monitoring agents. You can build all types of agent teams, but I think these are the two most foundational. Have an agent build the thing and then have another agent validate the thing. Very powerful. This is what our primary agent that was doing the planning work, right, with the template metaprompt. This is what it used to actually put together the team. You know to be super clear if we search for team orchestration here we can see our team members but you can see here every one of these agents was unique. So we built a session end builder for this session end hook and then we built the corresponding validator. Same thing with permission request builder and then permission request validator. All right and this is where it gets really powerful. If we go to this step-by-step task, you can see here we have build workflows. So build build build. And then guess what happens after six? We have validators. is doing compilation on the code to make sure that it's legit. And then we have additional validation steps down here. And you know, looking back at this, I actually missed an opportunity here. If I search for claw-p, there's a huge opportunity for every validator agent to actually just fire off claw--pey all logs are created in logs slash. We could have built a more tighter closed loop where the agents were validating this log file. We have all of our logs for each one of these new methods. So, if we just search for one of our new ones, session end, we should see a session end file here now. Yeah, there's our session end. And so, we have some new logging files that just weren't there before, right? Permission request. Um, and one of the newer ones that I haven't really played with a lot, post tool use failure. And you can see that log file there. Fantastic. And then you can see here, step 15, step 16, we're going to update the readme. So, of course, you know, simple validation here. Just to quickly check this, we can open this. And then once again, we can just search for one of these tools that weren't previously documented, right? So, if I just search for post tool use, you can see all of our documentation got edited. And we can do this even faster if we just want to get the file path here. GDF, which is get diff, and then we can just see the overall diff there. We got a bunch of new status lines. We got our file references updated, yada yada yada. We have our new documentation for these hooks here. So, that's fantastic. We also got our GDF uh settings file got updated as well. And you can see new hooks were added. Nothing super novel there. This was a relatively simple task for Opus to handle, especially with it deployed across multiple agents, focusing on one specific task at a time. That's another huge value proposition of this system. Every one of your agents has a focused context window doing one thing extraordinarily well. This is something we talk about all the time in tactical agentic coding. This is the lesson six tactic. If you're interested, check that out. Link in the description. But basically, the more agents you have with focus context windows doing one specific thing, the better. And this multi- aent task system is perfect for that. Your top level planner orchestrator agent writes the plan. You want to refresh the context after that, kick it off in a new agent to do the building that was inside of the plan. But once they do that, your multi- aent systems task list and the individual agent teams that you assign the work to, they kind of take care of it from there. And that leads us to the question when should you use this task system? So this is on by default if you write a large enough prompt claude code and opus it knows it has access to these tools that in itself is like fine. It's like you know a little bit more valuable but I think if you're really pushing and you're really scaling what you can do with agents you're going to want to build out a meta prompt like this. Okay. It's a prompt that builds a prompt. Specifically with agentic coding there are two primary constraints. Planning and reviewing. you're probably spending most of your time planning or reviewing if you're doing things right, if you're doing true agentic engineering. Now, this prompt, this new set of tools really helps us in the planning phase. We can build out specialized agents that are again self- validating. So, every one of them is checking their own work. This is super important. I'll link previous videos on the channel where we talk about building out these embedded hooks so that your agents are validating specific work that they're designed to do. But what you can do with your team members, your agents that are, you know, built for specific purposes, is really build in unique workflows where you think about the combination of running multiple agents together that outperform a single one. And that's why, you know, we do build, we do test, we do build, we do review. We have a documentation agent that is just all about documenting. That's another direction we can go with this. You can see here our validator is just reporting if the thing was built right. If it was, we report success. If it wasn't, we report failure. Okay, so a very powerful dedicated agent just for validating work. And as mentioned here, you know, I could have pushed uh this validation a bit further. We should have had cloud-p messages for every single validation agent. Instead, we just got Python compile of the individual scripts. This is probably enough for Opus, though. If we open up any one of these files, right, we had the logs generated, too. But it's going to basically mirror and copy the previous format from all of the other hook scripts that were running. And yeah, just at a glance, I can see that this is right. So, we got our sub agent announce. This all looks great. But you get the point, right? We could have improved our validation there. And this is where that orchestrator prompt becomes even more important. If we go to plan with team here, remember we pass in two prompts. What we wanted to build and then the actual orchestration prompt. And I can pull that out here. I just copy pasted that in. Had that set up beforehand. So, you can just kind of see exactly what this looks like, right? create groups of agents for each hook, one builder and one validator. All right, so this is our orchestration prompt. This is our highle prompt that gets boiled down into a low-level prompt thanks to our metaprompt. Then in the orchestrator prompt, we're actually helping our agent guide how to build the team that does the work. This is a new paradigm of multi- aent orchestration that's emerging. This is one way you can use it repeatedly, consistently, and reliably. And it also gives you a little bit of flexibility because you can also pass in that orchestration prompt. So a couple big ideas we're hitting on here. Self- validation. We're hitting on multi- aent orchestration. And again, we're building it into our reusable prompts. A lot of engineers are going to miss this. Please don't be one of them. You can build team orchestration into your reusable prompt so you get the value every single time. Right? It only takes one time to build out a great prompt, right? Just that upfront investment is really where you want to be spending more and more of your time. As mentioned in tactical agentic coding, you want to be building the agentic layer of your code base. Don't work on the application anymore. Work on the agents that build the application for you. All right, big big idea there. Uh there's a lot of value embedded in that. A lot of what we're seeing coming out, you know, the Ralph Wickham technique, uh all of this stuff around multi- aent orchestration, which the cloud code team is not documenting very well. Oh, I wish they would really up their documentation on this stuff. This task feature is pushing in the direction of multi- aent orchestration. Remember, in the beginning, you have a base agent. Then you learn how to use it better by context engineering and prompt engineering. And then you add more agents. Very powerful. After you add more agents, you customize them. And then lastly, you add an orchestrator agent to help you conduct all of them. And that's what we're turning our primary agent into. Let's be super clear about this. your primary agent when they're working with this task list, when they're working with your agent teams, they are orchestrating. All right. Now, there's levels to this. We built our own multi- aent orchestration system inside of Agentic Horizon. Um, I'll link the course in the description obviously for you if you want to push what you can do with Agentic Engineering further beyond. I'll leave this prompt in the cloud code hooks mastery codebase for you. If you want to check it out, if you want to understand how you can build template meta prompts that encode your engineering, this is very, very powerful. I think there's a lot of hype right now in the tech industry. There's a lot of slop engineering and just vibe slopping and it's coming out by a lot of people just jumping onto these super super highle abstract tools like Moltbot. Now I have nothing against this thing. I can see why people are really interested. You know, it's very powerful. This thing's gone super viral, but I am super concerned about an over reliance on tools like this without understanding the pieces of it. Now I think if you're a agentic engineer, if you're an engineer that has been learning to really use agents and build proficient systems that operate with and without you, you know, go crazy with tools like this. You know what's happening underneath the hood. It's more of everyone else that I'm worried about, right? That uh really have no idea what's going on underneath the hood. When really, if you're trying to learn how to build with agents, it's all about the core four context, model, prompt, and tools. And it's about learning to leverage these fundamental levers of agentic coding, the fundamental pieces of building with agents. And that comes down to reusable prompts, building out your own specialized agents, and building out AI developer workflows, ADWs as we call them in TAC. It's all about knowing what you're doing and teaching your agents how to do it. All right. There's going to be a big gap between engineers that turn their brain off and engineers that keep learning and keep adding to their stack of agentics, their patterns and tools that they can use to teach their agents how to build on their behalf. I'm not saying don't use agents. I think this tool and other tools like it, they're incredible. What I'm saying is know how to use the primitives and the leverage points of agentic coding, right? The foundational pieces that make it all up. Because if you do that as I have, as many of us have that watch this channel, um you'll be able to hop from tool to tool to tool to feature to feature to feature. All right? And this tool is a great example, right? This system that the cloud code team has built out, it's not new, right? Open source tools have had this, but what they've done here is standardized it and made it accessible through the best agent coding tool. That's worth paying attention to. That's worth learning. These are just tools and prompts. This entire feature set is just tools and prompts. So if we needed to, if you wanted to, we could step away from cloud code. We could build it into another tool if needed. Thankfully, we don't have to. They built it in. This is the Claude Code task system. You can use this to build specialized agent teams when you combine it with a powerful meta prompt, a prompt that builds a prompt. And when you template and add self validation into your agentic systems, all right, these are powerful trends. We're starting to stack up on the channel. Make sure to like and comment. let the algorithm know you're interested in like real hands-on agentic engineering. I want to kind of push back against some of this, you know, insane AI hype that's going on right now. Let's stay close to the fundamentals. Let's stay close to what makes up the agent at a foundational level while increasing what we can do with this. All right, that's all for this one. You know where to find me every single Monday. Stay focused and keep building.

</details>

---

## References and Links

- **Tactical Agentic Coding Course:** https://agenticengineer.com/tactical-agentic-coding
- **Hook Mastery Codebase:** https://github.com/disler/claude-code-hooks-mastery
- **Specialized Self Validation Video:** https://youtu.be/u5GkG71PkR0
- **Claude Code Task Tools Documentation:** https://code.claude.com/docs/en/settings#tools-available-to-claude
- **Agentic Horizon Course:** (mentioned, link in video description)

---

*Document generated via 3-iteration extraction process on 2026-02-03*
*Source: YouTube video transcript processed through Iteration 1 (Initial Extraction), Iteration 2 (Deep Analysis), and Iteration 3 (Master Synthesis)*
