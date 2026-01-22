# Agent Output Format Specification

## Overview

This specification defines how Blackbox5 agents should format their outputs for maximum clarity, parsability, and user experience. Based on best practices from OpenAI, Anthropic, LangChain, and production AI systems.

## Core Principles

1. **Structured First** - Outputs should be machine-parseable (JSON/Markdown structure)
2. **Executive Summary** - Start with a concise summary for quick understanding
3. **Visual Clarity** - Use formatting to make key information stand out
4. **Actionable** - Every output should include clear next steps or deliverables

## Required Output Format

Every agent response must follow this structure:

```markdown
# Summary

[One paragraph, 2-3 sentences maximum, summarizing what was done and the key outcome]

---

## Result Box

┌─────────────────────────────────────────────────────────────┐
│  🎯 STATUS: [✅ Success | ⚠️ Partial | ❌ Failed]              │
│                                                              │
│  📊 OUTCOME: [Clear one-line outcome statement]             │
│                                                              │
│  📁 DELIVERABLES:                                            │
│  • [File/Artifact created or modified]                       │
│  • [Key changes made]                                        │
│  • [Any issues or caveats]                                   │
│                                                              │
│  ➡️ NEXT STEPS: [What should happen next, if anything]       │
└─────────────────────────────────────────────────────────────┘

---

## Details

[Full explanation, code, analysis, or other content here]

### Subsection 1
[Organize details with clear headers]

### Subsection 2
[Use bullet points, code blocks, tables as appropriate]

---

## Technical Notes

[Optional: Technical details, implementation notes, edge cases handled]

---

## Related Files

- `path/to/file1.ts` - [Brief description]
- `path/to/file2.ts` - [Brief description]
```

## Section Guidelines

### 1. Summary (REQUIRED)

**Purpose:** Quick understanding for users and downstream systems

**Rules:**
- Maximum 2-3 sentences
- Focus on WHAT was done, not HOW
- Include the key outcome or result
- No technical jargon unless necessary

**Examples:**
```
✅ Good:
"Successfully implemented user authentication API with JWT tokens. Created 5 new endpoints, added middleware, and wrote comprehensive tests. All tests passing."

❌ Bad:
"I worked on implementing the authentication system by first creating a new folder structure and then adding various files for the JWT implementation which involved..."
```

### 2. Result Box (REQUIRED)

**Purpose:** Visual, scannable summary of key information

**Format:** ASCII box with clear sections

**Fields:**
- **STATUS:** ✅ Success | ⚠️ Partial | ❌ Failed
- **OUTCOME:** One-line clear statement
- **DELIVERABLES:** Bullet list of what was produced
- **NEXT STEPS:** What should happen next (or "None - complete")

**Example:**
```
┌─────────────────────────────────────────────────────────────┐
│  🎯 STATUS: ✅ Success                                       │
│                                                              │
│  📊 OUTCOME: REST API with 5 endpoints fully implemented     │
│                                                              │
│  📁 DELIVERABLES:                                            │
│  • api/users.ts - User CRUD operations                       │
│  • api/auth.ts - JWT authentication                          │
│  • middleware/auth.ts - Auth verification                    │
│  • tests/auth.test.ts - 12 tests, all passing               │
│                                                              │
│  ➡️ NEXT STEPS: Deploy to staging environment               │
└─────────────────────────────────────────────────────────────┘
```

### 3. Details (REQUIRED)

**Purpose:** Full explanation, code, or content

**Organization:**
- Use clear subsection headers (###)
- Include code blocks with syntax highlighting
- Use bullet points for lists
- Add tables for structured data when helpful
- Include inline code for file paths, function names, etc.

### 4. Technical Notes (OPTIONAL)

**Purpose:** Implementation details for technical audiences

**When to include:**
- Complex implementation details
- Edge cases handled
- Performance considerations
- Security considerations
- Known limitations

### 5. Related Files (OPTIONAL)

**Purpose:** Quick reference to files touched

**Format:** Markdown list with brief descriptions

## Visual Formatting Guidelines

### Code Blocks

Always specify language for syntax highlighting:

````markdown
```typescript
function authenticateUser(token: string): User {
  // Code here
}
```
````

### Emojis for Scannability

Use emojis consistently:
- 🎯 Status/Outcome
- ✅ Success/Complete
- ⚠️ Partial/Warning
- ❌ Failed/Error
- 📊 Data/Metrics
- 📁 Files/Deliverables
- ➡️ Next Steps
- 💡 Tip/Suggestion
- 🔧 Technical/Implementation

### Tables for Structured Data

```markdown
| Endpoint | Method | Status | Description |
|----------|--------|--------|-------------|
| /users | GET | ✅ | List all users |
| /users/:id | GET | ✅ | Get user by ID |
```

## Output Examples

### Example 1: Code Implementation Task

```markdown
# Summary

Successfully implemented the user profile CRUD API with TypeScript and Express. Created 4 new endpoints, added input validation, and wrote comprehensive unit tests achieving 95% code coverage.

---

## Result Box

┌─────────────────────────────────────────────────────────────┐
│  🎯 STATUS: ✅ Success                                       │
│                                                              │
│  📊 OUTCOME: User profile API fully implemented              │
│                                                              │
│  📁 DELIVERABLES:                                            │
│  • api/profiles.ts - 4 CRUD endpoints                        │
│  • middleware/validate.ts - Request validation               │
│  • tests/profiles.test.ts - 15 tests passing                 │
│  • types/profile.ts - TypeScript interfaces                  │
│                                                              │
│  ➡️ NEXT STEPS: Integrate with frontend components          │
└─────────────────────────────────────────────────────────────┘

---

## Details

### Implemented Endpoints

#### GET /api/profiles/:userId
Retrieves user profile by ID with error handling.

```typescript
export async function getProfile(req: Request, res: Response) {
  const { userId } = req.params;
  const profile = await db.profiles.findById(userId);
  if (!profile) {
    return res.status(404).json({ error: 'Profile not found' });
  }
  return res.json(profile);
}
```

#### POST /api/profiles
Creates new user profile with validation:

- Validates required fields (email, name)
- Checks for duplicate emails
- Returns created profile with ID

#### PUT /api/profiles/:userId
Updates existing profile.

#### DELETE /api/profiles/:userId
Deletes profile with cascade to user data.

### Test Coverage

All endpoints tested with:
- Valid input scenarios
- Error handling (404, 400, 500)
- Edge cases (empty requests, malformed data)

---

## Technical Notes

**Authentication:** All endpoints require valid JWT token
**Validation:** Uses Zod schemas for runtime validation
**Performance:** Queries optimized with proper indexes
**Security:** Input sanitization to prevent SQL injection

---

## Related Files

- `api/profiles.ts` - Main endpoint handlers
- `types/profile.ts` - TypeScript interfaces
- `tests/profiles.test.ts` - Test suite
- `middleware/validate.ts` - Validation middleware
```

### Example 2: Analysis Task

```markdown
# Summary

Analyzed 50K+ lines of codebase for performance bottlenecks. Identified 3 critical issues and provided actionable recommendations. Estimated performance improvement: 40-60% after implementing all fixes.

---

## Result Box

┌─────────────────────────────────────────────────────────────┐
│  🎯 STATUS: ✅ Analysis Complete                             │
│                                                              │
│  📊 OUTCOME: 3 critical issues found, 5 recommendations       │
│                                                              │
│  📁 DELIVERABLES:                                            │
│  • PERFORMANCE_ANALYSIS.md - Detailed report                 │
│  • Identified 3 critical bottlenecks                         │
│  • 5 prioritized recommendations                             │
│  • Estimated 40-60% performance gain                         │
│                                                              │
│  ➡️ NEXT STEPS: Review findings with team                    │
└─────────────────────────────────────────────────────────────┘

---

## Details

### Critical Issues Found

| Issue | Impact | Location | Priority |
|-------|--------|----------|----------|
| N+1 Query Problem | 5s → 200ms | api/users.ts | 🔴 Critical |
| Missing Index | 3s → 100ms | database/schema | 🔴 Critical |
| Unnecessary Re-renders | 2s → 50ms | frontend/App.tsx | 🟡 High |

### Recommendations

1. **Implement query batching** (Priority: 🔴 Critical)
   - Use DataLoader for batch queries
   - Estimated effort: 4 hours
   - Impact: 5s → 200ms

2. **Add database indexes** (Priority: 🔴 Critical)
   - Index on `users.email` and `posts.created_at`
   - Estimated effort: 30 minutes
   - Impact: 3s → 100ms

3. **Optimize React renders** (Priority: 🟡 High)
   - Memoize expensive computations
   - Estimated effort: 2 hours
   - Impact: 2s → 50ms

---

## Technical Notes

**Analysis Method:** Static code analysis + runtime profiling
**Measurement:** Average response time over 1000 requests
**Baseline:** Current production metrics from last 7 days

---

## Related Files

- `PERFORMANCE_ANALYSIS.md` - Full detailed report
- `api/users.ts` - Line 45: N+1 query issue
- `database/schema.sql` - Missing indexes
```

### Example 3: Research Task

```markdown
# Summary

Researched best practices for implementing WebSocket authentication in Node.js applications. Analyzed 5 production systems, documented 3 approaches with pros/cons. Recommended JWT-based approach for this use case.

---

## Result Box

┌─────────────────────────────────────────────────────────────┐
│  🎯 STATUS: ✅ Research Complete                             │
│                                                              │
│  📊 OUTCOME: JWT-based auth recommended                      │
│                                                              │
│  📁 DELIVERABLES:                                            │
│  • websocket-auth-research.md - Full analysis                │
│  • 3 authentication approaches compared                      │
│  • Implementation guide with code examples                   │
│  • Security considerations documented                        │
│                                                              │
│  ➡️ NEXT STEPS: Implement recommended approach              │
└─────────────────────────────────────────────────────────────┘

---

## Details

### Approaches Compared

| Approach | Complexity | Security | Scalability | Score |
|----------|-----------|----------|-------------|-------|
| JWT Handshake | Medium | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 9/10 |
| Session Token | Low | ⭐⭐⭐⭐ | ⭐⭐⭐ | 7/10 |
| API Key + TLS | Low | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 6/10 |

### Recommendation: JWT-Based Authentication

**Why:**
- ✅ Best security with token expiration
- ✅ Scalable (no server-side session storage)
- ✅ Industry standard (used by Slack, Discord)
- ✅ Easy to implement with existing JWT setup

**Implementation:**
```typescript
// Validate JWT on WebSocket upgrade
server.on('upgrade', (request, socket, head) => {
  const token = request.headers['sec-websocket-protocol'];
  const decoded = jwt.verify(token, SECRET);
  if (!decoded) {
    socket.close();
    return;
  }
  // Proceed with connection
});
```

---

## Technical Notes

**Sources Analyzed:**
- Slack Engineering Blog
- Discord Engineering Blog
- Socket.io documentation
- 3 GitHub production examples

**Security Considerations:**
- Always use WSS (WebSocket over TLS)
- Implement token refresh mechanism
- Rate limit connection attempts

---

## Related Files

- `websocket-auth-research.md` - Full research document
- `examples/jwt-websocket.ts` - Code example
```

## Agent-Specific Customization

Different agent types may emphasize different sections:

### Code Agents
- Emphasize: Files created, code changes
- Result Box focus: Deliverables
- Details focus: Code blocks

### Research Agents
- Emphasize: Findings, sources, conclusions
- Result Box focus: Key insights
- Details focus: Analysis, comparisons

### Architecture Agents
- Emphasize: Design decisions, trade-offs
- Result Box focus: Recommendations
- Details focus: Diagrams, rationale

### Manager Agent
- Emphasize: Coordination, delegation, outcomes
- Result Box focus: Tasks completed
- Details focus: Execution summary

## Implementation in agent.md

Add this section to each agent's agent.md file:

```markdown
## Output Format

This agent follows the Blackbox5 Output Format Specification:

1. **Summary** - One paragraph, 2-3 sentences max
2. **Result Box** - Visual ASCII box with status, outcome, deliverables, next steps
3. **Details** - Full explanation with code, analysis, or content
4. **Technical Notes** - Optional implementation details
5. **Related Files** - Optional file reference list

[Agent-specific customization here]

Example:
┌─────────────────────────────────────────────────────────────┐
│  🎯 STATUS: ✅ Success                                       │
│  📊 OUTCOME: [Clear outcome statement]                       │
│  📁 DELIVERABLES: [What was produced]                       │
│  ➡️ NEXT STEPS: [What happens next]                         │
└─────────────────────────────────────────────────────────────┘
```
