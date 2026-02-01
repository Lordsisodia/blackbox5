# MCP Context Optimization Strategy

## Your Assumptions - First Principles Analysis

### Assumption 1: "Multiple MCPs increase context length"
**Status:** ✅ TRUE - But there's nuance

**How MCP Actually Works:**
1. Claude sends `tools/list` request to each MCP
2. MCP returns ALL tool definitions
3. Claude loads ALL tools into context
4. Every tool has: name, description, input schema

**Example from real data:**
- Before optimization: 51,000 tokens for all MCP tools
- After optimization: 8,500 tokens
- **Per MCP: ~1,000-2,000 tokens typically**

### Assumption 2: "One master MCP reduces context"
**Status:** ❌ FALSE - It would ADD context

**Why:**
```
Current: 4 MCPs → ~8,500 tokens (after optimization)

With "master MCP":
┌─────────────────────────────────┐
│ Claude                          │
│   ↓ tools/list                  │
│ Master MCP                      │
│   ├─ Supabase tools (~2k)      │
│   ├─ Filesystem tools (~1.5k)   │
│   ├─ Memory tools (~1k)         │
│   └─ Serena tools (~1.5k)       │
│   Total: ~6k tokens             │
│   PLUS routing overhead (~500)  │
└─────────────────────────────────┘

Result: 6.5k tokens vs current 8.5k
Savings: ~2k tokens (23% reduction)
BUT: Adds complexity, latency, single point of failure
```

### Assumption 3: "MCP content takes significant context"
**Status:** ✅ TRUE - But Claude already optimized this

**Key Finding:** [Claude cut MCP bloat by 46.9%](https://medium.com/@joe.njenga/claude-code-just-cut-mcp-context-bloat-by-46-9-51k-tokens-down-to-8-5k-with-new-tool-search-ddf9e905f734)

They now use **tool search** instead of loading all tools.

---

## What Actually Consumes Context

### 1. MCP Tool Definitions (After Optimization)
```
4 MCPs × ~2,000 tokens = 8,000 tokens (2k per MCP)
```

### 2. System Prompt
```
Claude base: ~2,000 tokens
Your instructions: ~1,000-5,000 tokens
```

### 3. Conversation History
```
Varies widely: 1,000-50,000+ tokens
```

### 4. Agent Output (responses)
```
Varies: 500-5,000 tokens per response
```

---

## The REAL Bottleneck

**It's NOT the MCPs.**

Your context usage breakdown:
- **MCP tools:** ~8,000 tokens (fixed)
- **System prompt:** ~3,000 tokens (fixed)
- **Conversation history:** VARIABLE (can be 50k+)
- **Agent outputs:** VARIABLE (can be huge)

**The conversation history is 80-90% of your context usage.**

---

## Better Strategies (Ranked by Impact)

### 🥇 Strategy 1: Conversation Management (Highest Impact)

**Problem:** Long conversations = huge context

**Solution:** Implement conversation summarization/compression

```python
# When context hits 50% threshold:
if token_count > 100000:
    summary = summarize_conversation(messages[:-10])
    messages = [system_msg, summary] + messages[-5:]
```

**Impact:** Reduces context by 60-80%

---

### 🥈 Strategy 2: Selective MCP Loading (Medium Impact)

**Instead of loading ALL MCPs, load only what's needed:**

```json
// Instead of this (always loads all):
{
  "mcpServers": {
    "supabase": {...},
    "filesystem": {...},
    "memory": {...},
    "serena": {...}
  }
}

// Do this (load on demand):
{
  "mcpServers": {
    "supabase": {...}
  },
  "mcpServersDynamic": {
    "filesystem": {
      "command": "enable-mcp",
      "args": ["filesystem"]
    }
  }
}
```

**Problem:** Claude doesn't support dynamic MCP loading yet.

---

### 🥉 Strategy 3: Hybrid Local + Railway (Low Impact)

**Your original idea:** Run some locally, some on Railway

**Analysis:**
- Local MCPs: Still load tools into context
- Railway MCPs: Still load tools into context
- **No context savings** - tools load either way

**Where Railway HELPS:**
- Persistent state across sessions
- Team sharing
- Reduced LOCAL resource usage (not context)

---

## The Winning Strategy

### Focus on What Matters:

#### 1. **Reduce MCP Tool Count** (Quick Win)
```
Current: 4 MCPs = ~8,000 tokens
Optimal: 2-3 MCPs = ~4,000-6,000 tokens

Ask yourself:
- Do I need BOTH filesystem AND Serena search?
- Can Supabase handle what Memory does?
- Which MCPs do I actually USE?
```

#### 2. **Compress Conversation History** (Huge Impact)
```
Implement rolling summary:
- Always keep last 10 messages
- Summarize everything older
- Replace summary every 20 messages

Impact: 60-80% context reduction
```

#### 3. **Clean MCP Tool Definitions** (Medium Impact)
```
Some MCPs return verbose schemas:
- Remove unused tools from MCPs
- Simplify input schemas
- Remove long descriptions

Impact: 20-30% MCP context reduction
```

---

## Recommended Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Claude Session                      │
├─────────────────────────────────────────────────────┤
│                                                             │
│  MCPs (Load Only What You Use):                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Supabase   │  │  Filesystem  │  │  Custom API  │ │
│  │  (Database)  │  │  (Local IO)  │  │  (Railway)   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│        ~2k tokens      ~1.5k tokens     ~2k tokens   │
│                                                             │
│  Total: ~5.5k tokens for MCPs                            │
│                                                             │
├─────────────────────────────────────────────────────┤
│  Conversation Management:                                 │
│  • Keep last 10 messages                                  │
│  • Summarize older messages                               │
│  • Rotate summary every 20 messages                       │
│                                                             │
├─────────────────────────────────────────────────────┤
│  Result: 5.5k + 3k (system) + 10k (recent)              │
│         + 2k (summary) = ~20k tokens                      │
│         vs 50k+ without management                       │
└─────────────────────────────────────────────────────┘
```

---

## Implementation Steps

### Step 1: Audit Your MCPs
```bash
# Check which MCPs you actually use
claude-resource-monitor usage

# Look at tool definitions
npx @modelcontextprotocol/inspect-server ~/.npm-global/bin/mcp-server-filesystem
```

### Step 2: Remove Unnecessary MCPs
```json
{
  "mcpServers": {
    "supabase": {
      "command": "node",
      "args": ["~/.npm-global/bin/mcp-server-supabase", "--project-ref", "avdgyrepwrvsvwgxrccr"]
    }
    // Remove filesystem (use Supabase storage)
    // Remove memory (use Supabase or in-memory)
    // Keep Serena for now (unique value)
  }
}
```

### Step 3: Railway for Specialized MCPs
```json
{
  "mcpServers": {
    "local-supabase": {
      "command": "node",
      "args": ["~/.npm-global/bin/mcp-server-supabase", "--project-ref", "avdgyrepwrvsvwgxrccr"]
    },
    "railway-analytics": {
      "url": "https://your-analytics.railway.app/sse",
      "transport": "sse"
    }
  }
}
```

---

## Summary

**Your Assumptions:**
1. ✅ Multiple MCPs = more context → TRUE
2. ❌ Master MCP = less context → FALSE (adds routing overhead)
3. ✅ MCPs take significant context → TRUE (but less than conversation)

**The Solution:**
1. **Reduce MCP count** (not multiplex)
2. **Manage conversation history** (biggest impact)
3. **Use Railway** for persistent/shared MCPs (but doesn't save context)

**Expected Results:**
- Reduce MCPs from 4 → 2: Saves ~4k tokens
- Add conversation compression: Saves ~30k tokens
- **Total savings: ~34k tokens per session**

**Resources:**
- [MCP Architecture Overview](https://modelcontextprotocol.io/docs/learn/architecture)
- [Claude MCP Integration](https://platform.claude.com/docs/en/agent-sdk/mcp)
- [Claude's MCP Optimization](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [Context Bloat Analysis](https://medium.com/@joe.njenga/claude-code-just-cut-mcp-context-bloat-by-46-9-51k-tokens-down-to-8-5k-with-new-tool-search-ddf9e905f734)
