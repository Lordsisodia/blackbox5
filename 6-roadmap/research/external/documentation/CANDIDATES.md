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
  research_status: "complete"
  llms_txt: "https://modelcontextprotocol.io/llms.txt"
  sitemap: "https://modelcontextprotocol.io/sitemap.xml"
  estimated_pages: 145
  ranking:
    score: 92
    relevance: 100
    quality: 90
    freshness: 85
    automation: 95
  notes: "Core protocol for Claude Code integrations. 5 spec versions (2024-11-05 to 2025-03-26). Full SDKs (TypeScript, Python, Java, Kotlin, C#). Excellent llms.txt with structured overview."
  decision: "approve"

- name: "Anthropic API"
  url: "https://docs.anthropic.com/en/api"
  category: "api"
  research_status: "complete"
  llms_txt: null
  sitemap: null
  estimated_pages: 60
  ranking:
    score: 78
    relevance: 95
    quality: 90
    freshness: 85
    automation: 40
  notes: "Core Claude API. Recently migrated to platform.claude.com. NO llms.txt or sitemap.xml - will need custom crawler. 60-80 pages. Well-organized reference docs."
  decision: "approve"

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
  research_status: "complete"
  llms_txt: "https://sdk.vercel.ai/llms.txt"
  sitemap: "https://sdk.vercel.ai/sitemap.xml"
  estimated_pages: 754
  ranking:
    score: 85
    relevance: 85
    quality: 88
    freshness: 90
    automation: 78
  notes: "754 pages total. llms.txt is 1.2MB raw MDX. 25+ AI providers supported. Very active development (AI SDK 4.0, AI SDK 3.0). Large scope - recommend selective ingestion of core sections."
  decision: "approve"

- name: "OpenAI API"
  url: "https://platform.openai.com/docs"
  category: "api"
  research_status: "pending"
  llms_txt: null
  sitemap: null
  estimated_pages: 80
  ranking:
    score: 70
    relevance: 75
    quality: 90
    freshness: 85
    automation: 40
  notes: "Industry standard. GPT-4, assistants, fine-tuning. No llms.txt detected. Good reference for multi-provider comparisons."
  decision: "deferred"

### Blackbox5 Stack

- name: "Supabase"
  url: "https://supabase.com/docs"
  category: "tool"
  research_status: "complete"
  llms_txt: "https://supabase.com/llms.txt (multi-file by language)"
  sitemap: "https://supabase.com/sitemap.xml"
  estimated_pages: 385
  ranking:
    score: 88
    relevance: 95
    quality: 85
    freshness: 90
    automation: 82
  notes: "385 pages. Multi-language llms.txt (JS, Python, Dart, Swift, Kotlin, C#, etc.). Already used in Blackbox5. Recommend selective ingestion of ~50-75 most relevant pages."
  decision: "approve"

- name: "n8n"
  url: "https://docs.n8n.io"
  category: "tool"
  research_status: "complete"
  llms_txt: "https://docs.n8n.io/llms.txt"
  sitemap: "https://docs.n8n.io/sitemap.xml"
  estimated_pages: 450
  ranking:
    score: 86
    relevance: 90
    quality: 82
    freshness: 85
    automation: 88
  notes: "400-500 pages. 400+ integrations documented. Already used in Blackbox5. Good llms.txt with clear structure. Recommend selective ingestion focusing on core workflow concepts."
  decision: "approve"

- name: "GitHub Actions"
  url: "https://docs.github.com/en/actions"
  category: "tool"
  research_status: "pending"
  llms_txt: null
  sitemap: null
  estimated_pages: 120
  ranking:
    score: 72
    relevance: 80
    quality: 85
    freshness: 80
    automation: 45
  notes: "CI/CD. Used for Blackbox5 automation. Large docs site. No llms.txt. Moderate priority given existing workflow knowledge."
  decision: "deferred"

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
