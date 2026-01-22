# Agent Output Format Specification (Agent-to-Agent + Human)

## Purpose

Enable reliable agent-to-agent communication while keeping outputs human-readable.

## Core Format

Every agent output has TWO parts:

```markdown
<output>
{
  "status": "success|partial|failed",
  "summary": "One sentence outcome",
  "deliverables": ["file1.ts", "file2.ts"],
  "next_steps": ["action1", "action2"],
  "metadata": {
    "agent": "coder",
    "task_id": "123",
    "duration_seconds": 45
  }
}

---
[HUMAN-READABLE EXPLANATION]
[Full details, code, reasoning, etc.]
</output>
```

### Part 1: JSON Block (For Agents)

- **Machine-parseable**
- **At the very top** (agents can read and stop there)
- **All key info in structured format**
- **Agents don't need to parse natural language**

### Part 2: Natural Language (For Humans)

- **After the JSON**
- **Full explanation**
- **Code blocks**
- **Reasoning**
- **Context**

## Why This Works

**For Agents:**
```python
# Agent receives output
response = from_agent(response)
data = json.loads(response.split('---')[0])

# Can immediately use:
if data["status"] == "success":
    for file in data["deliverables"]:
        process_file(file)
```

**For Humans:**
```markdown
{
  "status": "success",
  "summary": "Created auth API with JWT"
}
---
I implemented the authentication system by creating a new endpoint
that validates JWT tokens... [full explanation with code]
```

Humans see: Clear status + full explanation

## Example Outputs

### Example 1: Code Agent

```markdown
<output>
{
  "status": "success",
  "summary": "Implemented JWT authentication with 3 endpoints",
  "deliverables": [
    "api/auth.ts",
    "middleware/jwt.ts",
    "tests/auth.test.ts"
  ],
  "next_steps": [
    "connect to frontend",
    "deploy to staging"
  ],
  "metadata": {
    "agent": "coder",
    "task_id": "task-456",
    "duration_seconds": 180,
    "lines_written": 245,
    "tests_passing": 12
  }
}

---

## Implementation Details

I created a JWT-based authentication system with the following components:

### Endpoints Created

**POST /api/auth/login**
```typescript
export async function login(req: Request, res: Response) {
  const { email, password } = req.body;
  const user = await authenticate(email, password);
  const token = jwt.sign({ userId: user.id }, SECRET);
  res.json({ token, user });
}
```

**GET /api/auth/verify**
Validates token and returns user data.

**POST /api/auth/refresh**
Refreshes expired tokens.

### Security Considerations

- Tokens expire after 24 hours
- Passwords hashed with bcrypt (salt rounds: 10)
- Rate limiting on login endpoint (5 req/min)

### Test Results

All 12 tests passing:
- ✅ Valid login returns token
- ✅ Invalid login returns 401
- ✅ Token verification works
- ✅ Refresh token extends expiration
</output>
```

### Example 2: Manager Agent Coordinating

```markdown
<output>
{
  "status": "success",
  "summary": "Coordinated 3 agents to build user management API",
  "deliverables": [
    "execution-manifest.md",
    "api/users.ts"
  ],
  "next_steps": [
    "review implementation",
    "deploy to staging"
  ],
  "metadata": {
    "agent": "manager",
    "task_id": "coord-123",
    "duration_seconds": 600,
    "subtasks_completed": 5,
    "specialists_used": ["architect", "coder", "tester"]
  },
  "subtasks": [
    {
      "id": "sub-1",
      "agent": "architect",
      "status": "success",
      "output": "API design document"
    },
    {
      "id": "sub-2",
      "agent": "coder",
      "status": "success",
      "output": "Implementation complete"
    },
    {
      "id": "sub-3",
      "agent": "tester",
      "status": "success",
      "output": "All tests passing"
    }
  ]
}

---

## Coordination Details

### Task Decomposition

The original task "Build user management API" was broken into 3 subtasks:

1. **Architect** → Design API structure and endpoints
2. **Coder** → Implement the endpoints
3. **Tester** → Write and run tests

### Execution Timeline

| Subtask | Agent | Start | Duration | Status |
|---------|-------|-------|----------|--------|
| API Design | architect | 10:00 | 120s | ✅ |
| Implementation | coder | 10:02 | 300s | ✅ |
| Testing | tester | 10:07 | 180s | ✅ |

### Integration Results

All specialist outputs integrated successfully. The API includes:
- 5 CRUD endpoints for users
- JWT authentication
- Input validation
- Comprehensive test coverage (95%)

### Issues Encountered

- **Issue:** Coder initially missed input validation
- **Resolution:** Tester caught this, Coder fixed in follow-up
- **Impact:** Added 2 minutes to timeline, no blocker

</output>
```

### Example 3: Research Agent

```markdown
<output>
{
  "status": "success",
  "summary": "Researched WebSocket auth best practices, recommended JWT approach",
  "deliverables": [
    "docs/websocket-auth-research.md",
    "examples/jwt-handshake.ts"
  ],
  "next_steps": [
    "implement recommended approach",
    "security review"
  ],
  "metadata": {
    "agent": "researcher",
    "task_id": "research-789",
    "duration_seconds": 300,
    "sources_analyzed": 8
  }
}

---

## Research Findings

### Approaches Analyzed

| Approach | Security | Complexity | Scalability | Score |
|----------|----------|------------|-------------|-------|
| JWT Handshake | ⭐⭐⭐⭐⭐ | Medium | ⭐⭐⭐⭐ | 9/10 |
| Session Token | ⭐⭐⭐⭐ | Low | ⭐⭐⭐ | 7/10 |
| API Key + TLS | ⭐⭐⭐ | Low | ⭐⭐⭐⭐⭐ | 6/10 |

### Recommendation: JWT-Based Authentication

**Why:**
- Industry standard (Slack, Discord use this)
- No server-side session storage needed
- Scales horizontally
- Easy token revocation with blacklist

**Implementation:**

```typescript
// Validate JWT on WebSocket upgrade
server.on('upgrade', (request, socket, head) => {
  const token = request.headers['sec-websocket-protocol'];
  try {
    const decoded = jwt.verify(token, SECRET);
    socket.userId = decoded.userId;
  } catch {
    socket.close(4001, 'Authentication failed');
  }
});
```

### Sources Consulted

- Slack Engineering Blog: "How Slack Handles Websockets"
- Socket.io Documentation: Authentication Patterns
- 3 production GitHub repositories analyzed
- OWASP WebSocket Security Guidelines

</output>
```

### Example 4: Partial Success (With Caveats)

```markdown
<output>
{
  "status": "partial",
  "summary": "Implemented core features, pending edge case handling",
  "deliverables": [
    "api/users.ts"
  ],
  "next_steps": [
    "add error handling for edge cases",
    "write tests for edge cases"
  ],
  "metadata": {
    "agent": "coder",
    "task_id": "task-999",
    "duration_seconds": 240,
    "completion_percentage": 80
  },
  "issues": [
    {
      "type": "incomplete",
      "description": "Edge case: user with no email",
      "impact": "medium",
      "blocking": false
    }
  ]
}

---

## What's Working

✅ User CRUD operations implemented
✅ JWT authentication integrated
✅ Basic validation working

## What's Pending

⚠️ **Edge Case: Users without email addresses**
Current implementation assumes all users have emails. Need to handle:
- Users created via OAuth (might not have email)
- Admin-created users (email might be optional)

**Impact:** Medium - these users can't log in currently
**Blocking:** No - can be addressed in follow-up

## Code Created

**api/users.ts**
```typescript
export async function createUser(req: Request, res: Response) {
  const { email, name } = req.body;

  // TODO: Handle missing email
  if (!email) {
    return res.status(400).json({ error: 'Email required' });
  }

  const user = await db.users.create({ email, name });
  res.json(user);
}
```

</output>
```

### Example 5: Failed Task

```markdown
<output>
{
  "status": "failed",
  "summary": "Could not implement feature due to missing dependencies",
  "deliverables": [],
  "next_steps": [
    "install missing dependencies",
    "retry implementation"
  ],
  "metadata": {
    "agent": "coder",
    "task_id": "task-error-1",
    "duration_seconds": 60,
    "error_type": "dependency_missing"
  },
  "error": {
    "type": "DependencyError",
    "message": "Package 'bcrypt' not found",
    "resolution": "npm install bcrypt"
  }
}

---

## What Happened

Attempted to implement authentication but encountered missing dependency.

### Error Details

```
Error: Cannot find module 'bcrypt'
Require stack:
- /app/middleware/auth.ts
```

### Resolution Required

Run: `npm install bcrypt @types/bcrypt`

Then retry the implementation.

### Work Attempted

Created the authentication structure but couldn't complete without bcrypt package.
</output>
```

## JSON Schema Reference

### Base Schema (All Agents)

```typescript
{
  status: "success" | "partial" | "failed",
  summary: string,              // One sentence
  deliverables: string[],       // Files/artifacts created
  next_steps: string[],         // Recommended actions
  metadata: {
    agent: string,              // Agent ID
    task_id: string,            // Task identifier
    duration_seconds: number    // Time taken
  }
}
```

### Extended Schema (Manager Agent)

```typescript
{
  // ... base fields ...
  subtasks: Array<{
    id: string,
    agent: string,
    status: "success" | "partial" | "failed",
    output: string
  }>
}
```

### Extended Schema (Partial Status)

```typescript
{
  // ... base fields ...
  completion_percentage: number,
  issues: Array<{
    type: string,
    description: string,
    impact: "low" | "medium" | "high",
    blocking: boolean
  }>
}
```

### Extended Schema (Failed Status)

```typescript
{
  // ... base fields ...
  error: {
    type: string,
    message: string,
    resolution: string
  }
}
```

## Implementation Instructions for agent.md

Add this to each agent's agent.md:

```markdown
## Output Format

**CRITICAL:** All outputs must use this format for agent-to-agent communication:

```markdown
<output>
{
  "status": "success|partial|failed",
  "summary": "One sentence outcome",
  "deliverables": ["list of files/artifacts"],
  "next_steps": ["recommended actions"],
  "metadata": {
    "agent": "your-agent-id",
    "task_id": "from-task",
    "duration_seconds": 0
  }
}

---
[Your full explanation for humans here]
</output>
```

**The JSON block at top is for agents to parse.**
**The content after --- is for humans to read.**
```

## Parsing for Other Agents

```python
import json
import re

def parse_agent_output(output: str) -> dict:
    """
    Parse agent output, extract JSON block for agent use.
    """
    # Extract JSON from between <output> tags
    match = re.search(r'<output>\s*(\{.*?\})\s*---', output, re.DOTALL)
    if not match:
        raise ValueError("No valid JSON block found in output")

    json_str = match.group(1)
    return json.loads(json_str)

# Usage
response = await agent.execute(task)
data = parse_agent_output(response)

# Now you can use the data
if data["status"] == "success":
    print(f"Deliverables: {data['deliverables']}")
    for next_step in data["next_steps"]:
        await execute(next_step)
```
