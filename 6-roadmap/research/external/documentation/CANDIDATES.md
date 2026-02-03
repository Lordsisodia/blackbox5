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
  research_status: "complete"
  llms_txt: "https://docs.docker.com/llms.txt"
  sitemap: "https://docs.docker.com/sitemap.xml"
  estimated_pages: 2000
  ranking:
    score: 82
    relevance: 80
    quality: 90
    freshness: 90
    automation: 70
  notes: "Containerization. Has llms.txt AND llms-full.txt. 2,000-4,000 pages total. Early adopter of llms.txt standard. Hugo-based, well-organized."
  decision: "pending"

- name: "Kubernetes"
  url: "https://kubernetes.io/docs"
  category: "tool"
  research_status: "complete"
  llms_txt: null
  sitemap: "https://kubernetes.io/sitemap.xml (index with 16 languages)"
  estimated_pages: 1000
  ranking:
    score: 75
    relevance: 75
    quality: 95
    freshness: 90
    automation: 45
  notes: "Orchestration. NO llms.txt. Sitemap index with 16 languages. ~1,000 English pages. robots.txt blocks API reference. CC BY 4.0 license."
  decision: "pending"

### Development

- name: "TypeScript"
  url: "https://www.typescriptlang.org/docs"
  category: "language"
  research_status: "complete"
  llms_txt: null
  sitemap: null
  estimated_pages: 600
  ranking:
    score: 78
    relevance: 85
    quality: 92
    freshness: 88
    automation: 45
  notes: "Primary language. NO llms.txt or sitemap. ~120 markdown source files / ~600 rendered pages. GitHub source available (microsoft/TypeScript-Website). Gatsby-based SPA."
  decision: "pending"

- name: "React"
  url: "https://react.dev"
  category: "framework"
  research_status: "complete"
  llms_txt: null
  sitemap: "https://react.dev/sitemap.xml (likely exists)"
  estimated_pages: 125
  ranking:
    score: 80
    relevance: 82
    quality: 95
    freshness: 95
    automation: 58
  notes: "Frontend framework. NO llms.txt. ~70-125 pages. MDX format with interactive Sandpack examples. GitHub source available (reactjs/react.dev). Next.js-based."
  decision: "pending"

- name: "Tailwind CSS"
  url: "https://tailwindcss.com/docs"
  category: "framework"
  research_status: "pending"
  llms_txt: null
  sitemap: null
  estimated_pages: 80
  ranking:
    score: 58
    relevance: 60
    quality: 85
    freshness: 85
    automation: 45
  notes: "Utility CSS. Very popular. Only relevant for frontend work. Lower priority than core AI/LLM docs."
  decision: "deferred"

### Cloud AI

- name: "AWS Bedrock"
  url: "https://docs.aws.amazon.com/bedrock"
  category: "api"
  research_status: "pending"
  llms_txt: null
  sitemap: null
  estimated_pages: 150
  ranking:
    score: 60
    relevance: 65
    quality: 80
    freshness: 75
    automation: 35
  notes: "AWS managed Claude. Enterprise deployments. Only relevant if deploying to AWS. Large AWS docs structure."
  decision: "deferred"

- name: "Google Vertex AI"
  url: "https://cloud.google.com/vertex-ai/docs"
  category: "api"
  research_status: "pending"
  llms_txt: null
  sitemap: null
  estimated_pages: 200
  ranking:
    score: 55
    relevance: 60
    quality: 80
    freshness: 75
    automation: 35
  notes: "Google's AI platform. Claude available. Only relevant if deploying to GCP. Large docs structure."
  decision: "deferred"

### Databases

- name: "Pinecone"
  url: "https://docs.pinecone.io"
  category: "tool"
  research_status: "pending"
  llms_txt: null
  sitemap: null
  estimated_pages: 60
  ranking:
    score: 50
    relevance: 55
    quality: 82
    freshness: 80
    automation: 50
  notes: "Vector database. For RAG applications. Currently using Supabase for storage. Lower priority unless adding RAG features."
  decision: "deferred"

- name: "Neon"
  url: "https://neon.tech/docs"
  category: "tool"
  research_status: "pending"
  llms_txt: null
  sitemap: null
  estimated_pages: 50
  ranking:
    score: 45
    relevance: 50
    quality: 80
    freshness: 85
    automation: 50
  notes: "Serverless Postgres. Alternative to Supabase. Already committed to Supabase. Only relevant if considering migration."
  decision: "rejected"

- name: "Shadcn UI"
  url: "https://ui.shadcn.com"
  category: "framework"
  research_status: "complete"
  llms_txt: "https://ui.shadcn.com/llms.txt"
  sitemap: null
  estimated_pages: 94
  ranking:
    score: 88
    relevance: 88
    quality: 92
    freshness: 95
    automation: 90
  notes: "UI component library. Excellent llms.txt with 94 pages. 58 components, 10 framework guides. Active MCP server integration. Very automation-friendly."
  decision: "pending"

- name: "Next.js"
  url: "https://nextjs.org/docs"
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
  notes: "React framework from Vercel. App Router, Pages Router, full-stack capabilities."
  decision: "pending"

- name: "Node.js"
  url: "https://nodejs.org/docs"
  category: "runtime"
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
  notes: "JavaScript runtime. Core for backend development."
  decision: "pending"

- name: "Python"
  url: "https://docs.python.org/3"
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
  notes: "Primary language for AI/ML. Extensive standard library docs."
  decision: "pending"

- name: "FastAPI"
  url: "https://fastapi.tiangolo.com"
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
  notes: "Modern Python web framework. Popular for APIs."
  decision: "pending"

- name: "PostgreSQL"
  url: "https://www.postgresql.org/docs"
  category: "database"
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
  notes: "Open source relational database. Supabase is built on this."
  decision: "pending"

- name: "Redis"
  url: "https://redis.io/docs"
  category: "database"
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
  notes: "In-memory data store. Caching, sessions, real-time features."
  decision: "pending"

- name: "Terraform"
  url: "https://developer.hashicorp.com/terraform/docs"
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
  notes: "Infrastructure as Code. Multi-cloud provisioning."
  decision: "pending"

- name: "Ansible"
  url: "https://docs.ansible.com"
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
  notes: "Configuration management and automation."
  decision: "pending"

- name: "Prometheus"
  url: "https://prometheus.io/docs"
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
  notes: "Monitoring and alerting toolkit. Metrics collection."
  decision: "pending"

- name: "Grafana"
  url: "https://grafana.com/docs"
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
  notes: "Observability platform. Dashboards for metrics/logs."
  decision: "pending"

- name: "Elasticsearch"
  url: "https://www.elastic.co/guide/en/elasticsearch/reference"
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
  notes: "Search and analytics engine. Full-text search, logging."
  decision: "pending"

- name: "Kafka"
  url: "https://kafka.apache.org/documentation"
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
  notes: "Distributed event streaming platform. High-throughput messaging."
  decision: "pending"

- name: "GraphQL"
  url: "https://graphql.org/learn"
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
  notes: "API query language. Alternative to REST."
  decision: "pending"

- name: "tRPC"
  url: "https://trpc.io/docs"
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
  notes: "End-to-end typesafe APIs for TypeScript."
  decision: "pending"

- name: "Prisma"
  url: "https://www.prisma.io/docs"
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
  notes: "Next-gen ORM for Node.js and TypeScript."
  decision: "pending"

- name: "Drizzle"
  url: "https://orm.drizzle.team/docs"
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
  notes: "TypeScript ORM with SQL-like syntax. Lightweight alternative to Prisma."
  decision: "pending"

# BATCH 2 - EXPANDED CANDIDATES (User Requested + New Ideas)

## AI/LLM Platforms & SDKs

- name: "Anthropic Python SDK"
  url: "https://github.com/anthropics/anthropic-sdk-python"
  category: "sdk"
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
  notes: "Official Python SDK for Claude API. Essential for Python-based AI integrations in Blackbox5. Types, examples, async support."
  decision: "pending"

- name: "Anthropic TypeScript SDK"
  url: "https://github.com/anthropics/anthropic-sdk-typescript"
  category: "sdk"
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
  notes: "Official TypeScript SDK for Claude API. Streaming, tools, vision support. Critical for Node.js/TS AI implementations."
  decision: "pending"

- name: "LangChain"
  url: "https://python.langchain.com/docs"
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
  notes: "Popular AI orchestration framework. Chains, agents, RAG, memory. Industry standard for complex AI workflows."
  decision: "pending"

- name: "LangChain JS"
  url: "https://js.langchain.com/docs"
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
  notes: "JavaScript/TypeScript version of LangChain. Same patterns as Python version but for Node.js environments."
  decision: "pending"

- name: "LlamaIndex"
  url: "https://docs.llamaindex.ai"
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
  notes: "RAG-focused framework. Data ingestion, indexing, querying. Best-in-class for retrieval-augmented generation."
  decision: "pending"

- name: "CrewAI"
  url: "https://docs.crewai.com"
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
  notes: "Multi-agent orchestration framework. Role-based agents, tasks, crews. Good for autonomous agent systems like RALF."
  decision: "pending"

- name: "AutoGen"
  url: "https://microsoft.github.io/autogen/docs"
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
  notes: "Microsoft's multi-agent conversation framework. Agent-to-agent communication, code execution, group chats."
  decision: "pending"

## Chatbot & Automation Platforms

- name: "ManyChat"
  url: "https://manychat.com/help"
  category: "platform"
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
  notes: "Chatbot platform for Instagram, Facebook, WhatsApp. Flow builder, automation rules. Useful for social media automation workflows."
  decision: "pending"

- name: "ChatGPT"
  url: "https://help.openai.com"
  category: "platform"
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
  notes: "OpenAI's consumer platform docs. GPTs, custom instructions, plugins. Reference for OpenAI ecosystem."
  decision: "pending"

- name: "Zapier"
  url: "https://help.zapier.com"
  category: "platform"
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
  notes: "Workflow automation platform. 5,000+ app integrations. Alternative/complement to n8n for business automation."
  decision: "pending"

- name: "Make"
  url: "https://www.make.com/en/help"
  category: "platform"
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
  notes: "Visual automation platform (formerly Integromat). More powerful than Zapier, visual scenario builder."
  decision: "pending"

## Core Development

- name: "Redis"
  url: "https://redis.io/docs"
  category: "database"
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
  notes: "In-memory data store. Caching, session storage, real-time features, message broker. Essential for high-performance apps."
  decision: "pending"

- name: "PostgreSQL"
  url: "https://www.postgresql.org/docs"
  category: "database"
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
  notes: "Open source relational database. Supabase is built on this. Advanced features: JSONB, full-text search, extensions."
  decision: "pending"

- name: "Next.js"
  url: "https://nextjs.org/docs"
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
  notes: "React framework from Vercel. App Router, Server Components, API routes, full-stack TypeScript. Industry standard."
  decision: "pending"

- name: "Node.js"
  url: "https://nodejs.org/docs"
  category: "runtime"
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
  notes: "JavaScript runtime. Event-driven, non-blocking I/O. Core for backend development, CLI tools, automation scripts."
  decision: "pending"

- name: "FastAPI"
  url: "https://fastapi.tiangolo.com"
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
  notes: "Modern Python web framework. Async, automatic OpenAPI docs, type hints. Fastest Python framework, great for APIs."
  decision: "pending"

- name: "Django"
  url: "https://docs.djangoproject.com"
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
  notes: "Batteries-included Python web framework. Admin, ORM, auth, security. Good for rapid full-stack development."
  decision: "pending"

- name: "Flask"
  url: "https://flask.palletsprojects.com"
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
  notes: "Lightweight Python web framework. Microframework, extensible. Good for simple APIs and microservices."
  decision: "pending"

## Cloud & Infrastructure

- name: "AWS"
  url: "https://docs.aws.amazon.com"
  category: "cloud"
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
  notes: "Amazon Web Services documentation. EC2, S3, Lambda, RDS, 200+ services. Massive but essential for cloud deployments."
  decision: "pending"

- name: "Google Cloud"
  url: "https://cloud.google.com/docs"
  category: "cloud"
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
  notes: "Google Cloud Platform docs. Compute Engine, Cloud Run, BigQuery, Firebase. Alternative to AWS."
  decision: "pending"

- name: "Azure"
  url: "https://learn.microsoft.com/azure"
  category: "cloud"
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
  notes: "Microsoft Azure documentation. VMs, Functions, DevOps, AI services. Enterprise cloud platform."
  decision: "pending"

- name: "Vercel"
  url: "https://vercel.com/docs"
  category: "platform"
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
  notes: "Deployment platform for frontend. Serverless functions, edge network, preview deployments. Next.js hosting."
  decision: "pending"

- name: "Netlify"
  url: "https://docs.netlify.com"
  category: "platform"
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
  notes: "Static site hosting and serverless platform. Git-based CI/CD, forms, identity. Alternative to Vercel."
  decision: "pending"

- name: "Cloudflare"
  url: "https://developers.cloudflare.com"
  category: "platform"
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
  notes: "CDN, DNS, security, Workers (edge compute). Edge deployment, DDoS protection, R2 storage."
  decision: "pending"

## Security & Auth

- name: "Auth0"
  url: "https://auth0.com/docs"
  category: "service"
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
  notes: "Identity platform. Authentication, authorization, SSO. Universal login, MFA, social connections."
  decision: "pending"

- name: "Clerk"
  url: "https://clerk.com/docs"
  category: "service"
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
  notes: "Modern auth for React/Next.js. User management, sessions, organizations. Developer-friendly alternative to Auth0."
  decision: "pending"

- name: "Lucia"
  url: "https://lucia-auth.com"
  category: "library"
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
  notes: "Lightweight auth library for TypeScript. Session-based, framework agnostic. Minimal, flexible approach."
  decision: "pending"

## Testing & Quality

- name: "Jest"
  url: "https://jestjs.io/docs"
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
  notes: "JavaScript testing framework. Unit tests, snapshots, coverage. Most popular JS testing tool."
  decision: "pending"

- name: "Vitest"
  url: "https://vitest.dev/guide"
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
  notes: "Fast Vite-native testing. Jest-compatible, ESM-first, TypeScript support. Modern alternative to Jest."
  decision: "pending"

- name: "Playwright"
  url: "https://playwright.dev/docs"
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
  notes: "End-to-end testing. Cross-browser, auto-wait, codegen. Microsoft's modern alternative to Selenium."
  decision: "pending"

- name: "Cypress"
  url: "https://docs.cypress.io"
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
  notes: "E2E testing framework. Real-time reloads, debuggability, network stubbing. Popular for frontend testing."
  decision: "pending"

- name: "Pytest"
  url: "https://docs.pytest.org"
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
  notes: "Python testing framework. Fixtures, plugins, parametrize. Standard for Python testing."
  decision: "pending"

## Data & Analytics

- name: "Pandas"
  url: "https://pandas.pydata.org/docs"
  category: "library"
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
  notes: "Python data analysis library. DataFrames, data manipulation, analysis. Essential for data science."
  decision: "pending"

- name: "NumPy"
  url: "https://numpy.org/doc"
  category: "library"
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
  notes: "Python numerical computing. Arrays, matrices, math functions. Foundation of Python data science stack."
  decision: "pending"

- name: "Apache Arrow"
  url: "https://arrow.apache.org/docs"
  category: "library"
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
  notes: "Columnar data format for analytics. Cross-language, zero-copy reads. Used by Polars, DuckDB, pandas 2.0."
  decision: "pending"

- name: "DuckDB"
  url: "https://duckdb.org/docs"
  category: "database"
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
  notes: "In-process analytical database. SQL queries on DataFrames, CSV, Parquet. Fast analytics without server."
  decision: "pending"

- name: "dbt"
  url: "https://docs.getdbt.com"
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
  notes: "Data transformation tool. SQL-based analytics engineering. Models, tests, documentation."
  decision: "pending"

## Message Queues & Streaming

- name: "RabbitMQ"
  url: "https://www.rabbitmq.com/docs"
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
  notes: "Message broker. AMQP protocol, reliable messaging, routing. Traditional enterprise messaging."
  decision: "pending"

- name: "Apache Kafka"
  url: "https://kafka.apache.org/documentation"
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
  notes: "Distributed event streaming. High-throughput, fault-tolerant. Real-time data pipelines, event sourcing."
  decision: "pending"

- name: "NATS"
  url: "https://docs.nats.io"
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
  notes: "Cloud-native messaging. Pub/sub, request/reply, streaming. Lightweight, fast alternative to Kafka."
  decision: "pending"

## API & Integration

- name: "GraphQL"
  url: "https://graphql.org/learn"
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
  notes: "API query language. Type-safe, precise data fetching. Alternative to REST, used by GitHub, Shopify."
  decision: "pending"

- name: "tRPC"
  url: "https://trpc.io/docs"
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
  notes: "End-to-end typesafe APIs. TypeScript inference from backend to frontend. No code generation needed."
  decision: "pending"

- name: "gRPC"
  url: "https://grpc.io/docs"
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
  notes: "High-performance RPC framework. Protocol Buffers, HTTP/2, streaming. Microservices communication."
  decision: "pending"

- name: "Postman"
  url: "https://learning.postman.com"
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
  notes: "API development platform. Testing, documentation, collaboration. Industry standard for API workflows."
  decision: "pending"

- name: "Stripe"
  url: "https://stripe.com/docs"
  category: "service"
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
  notes: "Payment processing platform. Subscriptions, invoicing, Connect. Best-in-class API documentation."
  decision: "pending"

- name: "Twilio"
  url: "https://www.twilio.com/docs"
  category: "service"
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
  notes: "Communications platform. SMS, voice, email, WhatsApp. Programmable communications."
  decision: "pending"

## Mobile & Desktop

- name: "React Native"
  url: "https://reactnative.dev/docs"
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
  notes: "Cross-platform mobile apps. iOS/Android with React. Single codebase for mobile."
  decision: "pending"

- name: "Expo"
  url: "https://docs.expo.dev"
  category: "platform"
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
  notes: "React Native toolchain. Managed workflow, OTA updates, native modules. Simplifies mobile development."
  decision: "pending"

- name: "Electron"
  url: "https://www.electronjs.org/docs"
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
  notes: "Desktop apps with web tech. VS Code, Slack built with this. Cross-platform desktop."
  decision: "pending"

- name: "Tauri"
  url: "https://tauri.app/v1/guides"
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
  notes: "Desktop apps with Rust backend. Smaller bundle size, better performance than Electron. Modern alternative."
  decision: "pending"

## Version Control & Collaboration

- name: "Git"
  url: "https://git-scm.com/doc"
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
  notes: "Distributed version control. Core dev tool. Branching, merging, history. Essential knowledge."
  decision: "pending"

- name: "GitHub"
  url: "https://docs.github.com"
  category: "platform"
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
  notes: "Git hosting and collaboration. Actions, Issues, PRs, Codespaces. Platform for open source."
  decision: "pending"

- name: "GitLab"
  url: "https://docs.gitlab.com"
  category: "platform"
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
  notes: "DevOps platform. Git hosting, CI/CD, registry. Self-hosted alternative to GitHub."
  decision: "pending"

## Package Management & Build Tools

- name: "npm"
  url: "https://docs.npmjs.com"
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
  notes: "Node.js package manager. Publishing, workspaces, scripts. Core to JavaScript ecosystem."
  decision: "pending"

- name: "pnpm"
  url: "https://pnpm.io/motivation"
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
  notes: "Fast disk-space efficient package manager. Content-addressable store, strict dependencies. npm alternative."
  decision: "pending"

- name: "Vite"
  url: "https://vitejs.dev/guide"
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
  notes: "Next-gen frontend tooling. Fast dev server, optimized builds. Replaces webpack, create-react-app."
  decision: "pending"

- name: "Turborepo"
  url: "https://turbo.build/repo/docs"
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
  notes: "Monorepo build system. Incremental builds, caching, task pipelines. Vercel's monorepo tool."
  decision: "pending"

- name: "Nx"
  url: "https://nx.dev/getting-started/intro"
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
  notes: "Smart monorepo tooling. Angular, React, Node. Code generation, testing, CI. Enterprise monorepos."
  decision: "pending"

## Documentation & Content

- name: "Docusaurus"
  url: "https://docusaurus.io/docs"
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
  notes: "Documentation site generator. React-based, i18n, versioning. Used by many open source projects."
  decision: "pending"

- name: "MDX"
  url: "https://mdxjs.com/docs"
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
  notes: "Markdown + JSX. Interactive docs with React components. Modern documentation format."
  decision: "pending"

- name: "Storybook"
  url: "https://storybook.js.org/docs"
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
  notes: "UI component workshop. Develop, test, document components in isolation. Essential for design systems."
  decision: "pending"

- name: "Figma"
  url: "https://help.figma.com"
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
  notes: "Design and prototyping tool. Dev Mode, components, auto-layout. Design-to-code workflows."
  decision: "pending"

## Observability (Explained)

- name: "Prometheus"
  url: "https://prometheus.io/docs"
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
  notes: "Monitoring and alerting toolkit. Time-series metrics, PromQL queries. Cloud Native Computing Foundation project. Collects metrics from services."
  decision: "pending"

- name: "Grafana"
  url: "https://grafana.com/docs"
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
  notes: "Observability dashboards. Visualize metrics, logs, traces from multiple sources. Plugs into Prometheus, Loki, Tempo."
  decision: "pending"

- name: "Jaeger"
  url: "https://www.jaegertracing.io/docs"
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
  notes: "Distributed tracing system. Track requests across microservices. Performance analysis, root cause analysis."
  decision: "pending"

- name: "Loki"
  url: "https://grafana.com/docs/loki"
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
  notes: "Log aggregation system. Like Prometheus but for logs. Grafana Labs project. Cost-effective logging."
  decision: "pending"

## Infrastructure as Code (Explained)

- name: "Terraform"
  url: "https://developer.hashicorp.com/terraform/docs"
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
  notes: "Infrastructure as Code. Define cloud resources in HCL. Multi-cloud provisioning (AWS, Azure, GCP). State management."
  decision: "pending"

- name: "Ansible"
  url: "https://docs.ansible.com"
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
  notes: "Configuration management. YAML playbooks, agentless. Automate server setup, deployments. Red Hat project."
  decision: "pending"

- name: "Pulumi"
  url: "https://www.pulumi.com/docs"
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
  notes: "Infrastructure as Code in TypeScript/Python/Go. Real programming languages vs YAML. Modern Terraform alternative."
  decision: "pending"

- name: "CDK"
  url: "https://docs.aws.amazon.com/cdk"
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
  notes: "AWS Cloud Development Kit. Define AWS infra in TypeScript/Python. Constructs, stacks, CloudFormation generation."
  decision: "pending"

## Search & Discovery

- name: "Meilisearch"
  url: "https://www.meilisearch.com/docs"
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
  notes: "Lightning-fast search engine. Typo-tolerant, faceted search, synonyms. Developer-friendly alternative to Elasticsearch."
  decision: "pending"

- name: "Typesense"
  url: "https://typesense.org/docs"
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
  notes: "Open source typo-tolerant search. Instant search, geo-search, faceting. Algolia alternative, self-hostable."
  decision: "pending"

- name: "Algolia"
  url: "https://www.algolia.com/doc"
  category: "service"
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
  notes: "Hosted search platform. Instant search, AI search, analytics. Industry standard for site search."
  decision: "pending"

## Real-time & Collaboration

- name: "Socket.io"
  url: "https://socket.io/docs"
  category: "library"
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
  notes: "Real-time bidirectional communication. WebSockets with fallbacks. Chat, live updates, multiplayer."
  decision: "pending"

- name: "WebRTC"
  url: "https://webrtc.org/getting-started"
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
  notes: "Real-time communication for web. Video, audio, data channels. Browser-based peer-to-peer."
  decision: "pending"

- name: "Liveblocks"
  url: "https://liveblocks.io/docs"
  category: "service"
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
  notes: "Collaborative experiences SDK. Presence, multiplayer cursors, real-time sync. Figma-like collaboration."
  decision: "pending"

- name: "Yjs"
  url: "https://docs.yjs.dev"
  category: "library"
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
  notes: "CRDT framework for collaborative editing. Conflict-free replicated data types. Google Docs-style editing."
  decision: "pending"

## AI/ML Infrastructure

- name: "Hugging Face"
  url: "https://huggingface.co/docs"
  category: "platform"
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
  notes: "AI model hub and inference. Transformers, datasets, spaces. Open source models, fine-tuning, deployment."
  decision: "pending"

- name: "Ollama"
  url: "https://github.com/ollama/ollama/blob/main/docs"
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
  notes: "Run LLMs locally. Llama, Mistral, CodeLlama. Simple CLI for local AI. Private, offline inference."
  decision: "pending"

- name: "OpenRouter"
  url: "https://openrouter.ai/docs"
  category: "service"
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
  notes: "Unified API for LLMs. Access 100+ models with one API. Claude, GPT, Llama, Mistral. Model routing, fallbacks."
  decision: "pending"

- name: "LiteLLM"
  url: "https://docs.litellm.ai"
  category: "library"
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
  notes: "Call 100+ LLMs using OpenAI format. Proxy server, load balancing, cost tracking. Open source alternative to OpenRouter."
  decision: "pending"

## Workflow & BPM

- name: "Temporal"
  url: "https://docs.temporal.io"
  category: "platform"
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
  notes: "Durable execution platform. Reliable workflows, retries, state management. Microservices orchestration."
  decision: "pending"

- name: "Camunda"
  url: "https://docs.camunda.io"
  category: "platform"
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
  notes: "Process orchestration platform. BPMN workflows, decision automation. Enterprise business process management."
  decision: "pending"

- name: "Airflow"
  url: "https://airflow.apache.org/docs"
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
  notes: "Workflow orchestration platform. DAGs, scheduling, data pipelines. Apache project, Python-based."
  decision: "pending"

- name: "Prefect"
  url: "https://docs.prefect.io"
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
  notes: "Modern workflow orchestration. Python-native, observability, hybrid mode. Alternative to Airflow."
  decision: "pending"

## CMS & Content

- name: "Strapi"
  url: "https://docs.strapi.io"
  category: "cms"
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
  notes: "Open source headless CMS. Content types, API generation, plugins. Self-hosted content management."
  decision: "pending"

- name: "Sanity"
  url: "https://www.sanity.io/docs"
  category: "cms"
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
  notes: "Composable content platform. Real-time collaboration, structured content. Modern headless CMS."
  decision: "pending"

- name: "Contentful"
  url: "https://www.contentful.com/developers/docs"
  category: "cms"
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
  notes: "Headless CMS platform. Content model, APIs, webhooks. Enterprise content infrastructure."
  decision: "pending"

- name: "Notion API"
  url: "https://developers.notion.com"
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
  notes: "Notion as a CMS/database. Pages, databases, blocks API. Already using Notion - useful for integrations."
  decision: "pending"

## E-commerce

- name: "Shopify"
  url: "https://shopify.dev/docs"
  category: "platform"
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
  notes: "E-commerce platform. Storefront API, app development, themes. Leading e-commerce solution."
  decision: "pending"

- name: "WooCommerce"
  url: "https://woocommerce.com/documentation"
  category: "platform"
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
  notes: "WordPress e-commerce plugin. Open source, customizable. Popular for small-medium stores."
  decision: "pending"

- name: "Medusa"
  url: "https://docs.medusajs.com"
  category: "platform"
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
  notes: "Open source composable commerce. Headless e-commerce, modular. Modern Shopify alternative."
  decision: "pending"

## Low-code/No-code

- name: "Retool"
  url: "https://docs.retool.com"
  category: "platform"
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
  notes: "Internal tool builder. Drag-and-drop UI, database connections. Build admin panels fast."
  decision: "pending"

- name: "Bubble"
  url: "https://manual.bubble.io"
  category: "platform"
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
  notes: "No-code web app builder. Visual programming, workflows, database. Full apps without code."
  decision: "pending"

- name: "FlutterFlow"
  url: "https://docs.flutterflow.io"
  category: "platform"
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
  notes: "Low-code Flutter apps. Visual builder, Firebase integration. Mobile apps without coding."
  decision: "pending"

- name: "Framer"
  url: "https://www.framer.com/docs"
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
  notes: "Site builder with React. Design to production, CMS, effects. Figma-like to live site."
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
