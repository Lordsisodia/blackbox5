# Video Ranking Criteria

**Purpose**: Distinguish useful AI content from hype/bullshit

**Context**: All sources are AI/tech channels, so "AI" and "tech" are meaningless keywords.

---

## What Makes Content USEFUL

### 1. ACTIONABILITY (Most Important)
Can you DO something with this information?

**Strong Signals**:
- "How to..." + specific tool/technique
- "Tutorial" + code/examples
- "Build..." + working system
- "Deploy..." + production-ready
- "Setup..." + configuration steps
- "Masterclass" + deep dive
- "Course" + structured learning
- "Workshop" + hands-on

**Examples from our data**:
- ✅ "How to Use Google's Antigravity Better than 99% of People" - Actionable
- ✅ "An MCP & Skills masterclass" - Deep learning
- ✅ "Build polished web apps using these UI libraries" - Specific output
- ❌ "Gemini 3.5 Is Google's Greatest Model Ever!" - Just hype
- ❌ "OpenAI is going to lose to..." - Clickbait, no action

### 2. SPECIFICITY
Does it mention concrete tools, techniques, or outcomes?

**Strong Signals**:
- Named tools: "Claude Code", "MCP", "Antigravity", "Stitch"
- Named techniques: "vibe coding", "agentic AI", "code execution"
- Named outcomes: "automate your life", "build apps", "deploy agents"

**Weak Signals** (vague hype):
- "Greatest Model Ever!"
- "INSANE!"
- "This Changes Everything!"
- "The Future of AI!"

### 3. DEPTH INDICATORS
Is this surface-level news or deep content?

**Deep Content Signals**:
- "Masterclass"
- "Deep dive"
- "Complete guide"
- "From scratch"
- "Architecture"
- "Implementation"
- "Case study"
- "$2.5M Process" (specific numbers)
- "24/7 AI Agent Employee" (specific use case)

**Surface Content Signals**:
- "News"
- "Update"
- "Announcement"
- "First look"
- "Impressions"
- "Reacting to..."
- "My thoughts on..."

### 4. NEGATIVE SIGNALS (Bullshit Detection)

**Hype Words** (penalize):
- "INSANE!"
- "GREATEST EVER!"
- "MIND-BLOWING!"
- "REVOLUTIONARY!"
- "GAME CHANGER!" (when not substantiated)
- "KILLS..." (when comparing tools)
- "DEAD" ("X is dead, long live Y")

**Clickbait Patterns** (penalize):
- "...you won't believe"
- "...they don't want you to know"
- "I might delete this"
- "...is a TRAP"
- "...is a SCAM"
- Open-ended questions without answers

**Vague Business Content** (penalize):
- Generic "AI Business Model"
- "How to get customers" without specifics
- "Secret to life" (philosophical, not actionable)

---

## Scoring Rubric

### Actionability (40 points)
```
+20: Step-by-step tutorial with code/examples
+15: How-to with specific tool/technique
+10: Build/deploy/setup guide
+5:  Workshop/masterclass/course
+0:  News/announcement/reaction
-10: Vague business advice
```

### Specificity (30 points)
```
+10: Names specific tool (Claude Code, MCP, Antigravity)
+10: Names specific technique (vibe coding, agentic)
+10: Names specific outcome (automate X, build Y)
+5:  Mentions code/implementation
+0:  Generic "AI" talk
-5:  Excessive hype words
```

### Depth (20 points)
```
+10: Masterclass/deep dive/architecture
+5:  Complete guide/from scratch
+5:  Case study/specific numbers
+0:  News/update/first look
-5:  Surface-level reaction
```

### Creator Tier (10 points)
```
+10: Tier 1 (David Ondrej, Anthropic, etc.)
+5:  Tier 2
+0:  Tier 3
```

---

## Examples from Our Data

| Title | Action | Specific | Depth | Tier | Total | Verdict |
|-------|--------|----------|-------|------|-------|---------|
| "How to Use Google's Antigravity Better than 99% of People" | 15 | 20 | 0 | 10 | 45 | ✅ Process |
| "An MCP & Skills masterclass" | 5 | 15 | 10 | 10 | 40 | ✅ Process |
| "ClawdBot The 24/7 AI Agent Employee That Can Automate Your Life!" | 10 | 15 | 5 | 10 | 40 | ✅ Process |
| "Gemini 3.5 Is Google's Greatest Model Ever! Most Powerful AI EVER!" | 0 | 0 | 0 | 5 | 5 | ❌ Filter |
| "OpenAI is going to lose to..." | 0 | 0 | 0 | 5 | 5 | ❌ Filter |
| "The secret to life from an AI Entrepreneur" | 0 | 0 | 0 | 10 | 10 | ❌ Filter |
| "Epic Mode: NEW Toolkit Ends Vibe Coding! 100x Better" | 10 | 15 | 0 | 10 | 35 | ⚠️ Borderline |

---

## Implementation Notes

### Current Keyword System Problems
1. "AI" matches everything (useless)
2. "Agent" matches everything (useless)
3. No penalty for hype words
4. No depth detection

### Proposed Improvements
1. **Remove generic keywords**: "AI", "tech", "future"
2. **Add actionability keywords**: "how to", "tutorial", "build", "deploy", "setup", "masterclass"
3. **Add specificity keywords**: Tool names (Claude Code, MCP, Antigravity, etc.)
4. **Add depth keywords**: "masterclass", "architecture", "implementation", "case study"
5. **Add hype penalties**: "INSANE", "GREATEST", "EVER", "MIND-BLOWING"
6. **Add clickbait penalties**: "...you won't believe", "secret", "TRAP", "SCAM"

### Alternative: Claude-Based Ranking
Instead of keywords, give Claude this spec and ask:
"Based on the criteria above, score this video title 0-100"

Cost: ~$0.002 per video
Accuracy: Likely 90%+

---

## Decision Matrix

| Approach | Accuracy | Cost | Speed | Maintenance |
|----------|----------|------|-------|-------------|
| Current keywords | 60% | Free | Fast | Hard |
| Improved keywords | 75% | Free | Fast | Medium |
| Claude ranking | 90% | $0.002/video | Medium | Low |

**Recommendation**: Try improved keywords first. If still missing too much, switch to Claude.
