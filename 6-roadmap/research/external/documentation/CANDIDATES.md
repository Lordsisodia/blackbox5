# Documentation Candidates

List of potential documentation sources to ingest, with research notes and rankings.

## Format

```yaml
- name: "Source Name"
  url: "https://docs.example.com"
  category: "api|framework|tool|protocol"
  research_status: "pending|in_progress|complete"
  llms_txt: null  # URL if found
  sitemap: null   # URL if found
  estimated_pages: null
  ranking:
    score: 0-100
    relevance: 0-100  # How relevant to Blackbox5/Claude Code work
    quality: 0-100    # Documentation quality
    freshness: 0-100  # How often updated
    automation: 0-100 # How easy to automate
  notes: ""
  decision: "pending|approve|reject|deferred"
```

## Candidates

### AI/LLM Core

- name: "MCP Specification"
  url: "https://modelcontextprotocol.io"
  category: "protocol"
  research_status: "pending"
  llms_txt: null
  sitemap: null
  estimated_pages: null
  ranking:
    score: 0
    relevance: 0
    quality: 0
    freshness: 0
    automation: 0
  notes: "Core protocol for Claude Code integrations. Anthropic project."
  decision: "pending"

- name: "Anthropic API"
  url: "https://docs.anthropic.com/en/api"
  category: "api"
  research_status: "pending"
  llms_txt: null
  sitemap: null
  estimated_pages: null
  ranking:
    score: 0
    relevance: 0
    quality: 0
    freshness: 0
    automation: 0
  notes: "Core Claude API - messages, streaming, tools, vision"
  decision: "pending"

- name: "Claude Code CLI"
  url: "https://code.claude.com/docs"
  category: "tool"
  research_status: "complete"
  llms_txt: "https://code.claude.com/docs/llms.txt"
  sitemap: null
  estimated_pages: 53
  ranking:
    score: 95
    relevance: 100
    quality: 95
    freshness: 90
    automation: 95
  notes: "Already ingested. 53 pages, 1.2MB."
  decision: "done"

- name: "Vercel AI SDK"
  url: "https://sdk.vercel.ai/docs"
  category: "framework"
  research_status: "pending"
  llms_txt: null
  sitemap: null
  estimated_pages: null
  ranking:
    score: 0
    relevance: 0
    quality: 0
    freshness: 0
    automation: 0
  notes: "Popular LLM abstraction layer. Multi-provider support."
  decision: "pending"

- name: "OpenAI API"
  url: "https://platform.openai.com/docs"
  category: "api"
  research_status: "pending"
  llms_txt: null
  sitemap: null
  estimated_pages: null
  ranking:
    score: 0
    relevance: 0
    quality: 0
    freshness: 0
    automation: 0
  notes: "Industry standard. GPT-4, assistants, fine-tuning."
  decision: "pending"

### Blackbox5 Stack

- name: "Supabase"
  url: "https://supabase.com/docs"
  category: "tool"
  research_status: "pending"
  llms_txt: null
  sitemap: null
  estimated_pages: null
  ranking:
    score: 0
    relevance: 0
    quality: 0
    freshness: 0
    automation: 0
  notes: "Database + auth. Already used in Blackbox5. Large docs."
  decision: "pending"

- name: "n8n"
  url: "https://docs.n8n.io"
  category: "tool"
  research_status: "pending"
  llms_txt: null
  sitemap: null
  estimated_pages: null
  ranking:
    score: 0
    relevance: 0
    quality: 0
    freshness: 0
    automation: 0
  notes: "Workflow automation. Already used in Blackbox5."
  decision: "pending"

- name: "GitHub Actions"
  url: "https://docs.github.com/en/actions"
  category: "tool"
  research_status: "pending"
  llms_txt: null
  sitemap: null
  estimated_pages: null
  ranking:
    score: 0
    relevance: 0
    quality: 0
    freshness: 0
    automation: 0
  notes: "CI/CD. Used for Blackbox5 automation."
  decision: "pending"

### Infrastructure

- name: "Docker"
  url: "https://docs.docker.com"
  category: "tool"
  research_status: "pending"
  llms_txt: null
  sitemap: null
  estimated_pages: null
  ranking:
    score: 0
    relevance: 0
    quality: 0
    freshness: 0
    automation: 0
  notes: "Containerization. Standard infrastructure."
  decision: "pending"

- name: "Kubernetes"
  url: "https://kubernetes.io/docs"
  category: "tool"
  research_status: "pending"
  llms_txt: null
  sitemap: null
  estimated_pages: null
  ranking:
    score: 0
    relevance: 0
    quality: 0
    freshness: 0
    automation: 0
  notes: "Orchestration. Complex, very large docs."
  decision: "pending"

### Development

- name: "TypeScript"
  url: "https://www.typescriptlang.org/docs"
  category: "language"
  research_status: "pending"
  llms_txt: null
  sitemap: null
  estimated_pages: null
  ranking:
    score: 0
    relevance: 0
    quality: 0
    freshness: 0
    automation: 0
  notes: "Primary language for many projects."
  decision: "pending"

- name: "React"
  url: "https://react.dev"
  category: "framework"
  research_status: "pending"
  llms_txt: null
  sitemap: null
  estimated_pages: null
  ranking:
    score: 0
    relevance: 0
    quality: 0
    freshness: 0
    automation: 0
  notes: "Frontend framework. New docs site (react.dev)."
  decision: "pending"

- name: "Tailwind CSS"
  url: "https://tailwindcss.com/docs"
  category: "framework"
  research_status: "pending"
  llms_txt: null
  sitemap: null
  estimated_pages: null
  ranking:
    score: 0
    relevance: 0
    quality: 0
    freshness: 0
    automation: 0
  notes: "Utility CSS. Very popular."
  decision: "pending"

### Cloud AI

- name: "AWS Bedrock"
  url: "https://docs.aws.amazon.com/bedrock"
  category: "api"
  research_status: "pending"
  llms_txt: null
  sitemap: null
  estimated_pages: null
  ranking:
    score: 0
    relevance: 0
    quality: 0
    freshness: 0
    automation: 0
  notes: "AWS managed Claude. Enterprise deployments."
  decision: "pending"

- name: "Google Vertex AI"
  url: "https://cloud.google.com/vertex-ai/docs"
  category: "api"
  research_status: "pending"
  llms_txt: null
  sitemap: null
  estimated_pages: null
  ranking:
    score: 0
    relevance: 0
    quality: 0
    freshness: 0
    automation: 0
  notes: "Google's AI platform. Claude available."
  decision: "pending"

### Databases

- name: "Pinecone"
  url: "https://docs.pinecone.io"
  category: "tool"
  research_status: "pending"
  llms_txt: null
  sitemap: null
  estimated_pages: null
  ranking:
    score: 0
    relevance: 0
    quality: 0
    freshness: 0
    automation: 0
  notes: "Vector database. For RAG applications."
  decision: "pending"

- name: "Neon"
  url: "https://neon.tech/docs"
  category: "tool"
  research_status: "pending"
  llms_txt: null
  sitemap: null
  estimated_pages: null
  ranking:
    score: 0
    relevance: 0
    quality: 0
    freshness: 0
    automation: 0
  notes: "Serverless Postgres. Alternative to Supabase."
  decision: "pending"

## Research Tasks

For each candidate, research:
1. Does it have `llms.txt`?
2. Does it have `sitemap.xml`?
3. How many pages (estimate)?
4. What's the content structure?
5. Any automation blockers?

Then rank 0-100 on:
- **Relevance** - How useful for Blackbox5/Claude Code work
- **Quality** - Documentation clarity and completeness
- **Freshness** - Update frequency
- **Automation** - Ease of scraping

Calculate weighted score and decide: approve/reject/defer
