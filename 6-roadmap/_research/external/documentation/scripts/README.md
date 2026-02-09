# Documentation Scripts

Automation scripts for fetching and processing external documentation.

## Scripts

### 1. docs-discover.py

Discovers all documentation routes from a site's index.

```bash
python scripts/docs-discover.py \
  --url https://code.claude.com/docs \
  --name claude-code \
  --output claude-code/raw/index.json
```

**Features:**
- Auto-detects `llms.txt` or `sitemap.xml`
- Organizes routes into priority tiers
- Outputs structured index.json

### 2. docs-fetch.py

Fetches documentation pages and stores as markdown.

```bash
python scripts/docs-fetch.py \
  --index claude-code/raw/index.json \
  --output claude-code/raw/pages/ \
  --tier 1 \
  --delay 0.5
```

**Features:**
- Rate limiting (configurable delay)
- HTML to Markdown conversion
- YAML frontmatter with metadata
- Skips existing files
- Tier-based filtering

### 3. docs-extract.py

Processes fetched pages into agent-friendly formats.

```bash
python scripts/docs-extract.py \
  --input claude-code/raw/pages/ \
  --output claude-code/extracted/
```

**Features:**
- Generates quick-reference.md
- Creates search-index.json
- Extracts commands and code examples

## Complete Workflow

```bash
# 1. Discover routes
python scripts/docs-discover.py \
  --url https://code.claude.com/docs \
  --name claude-code \
  --output claude-code/raw/index.json

# 2. Fetch Tier 1 pages (critical)
python scripts/docs-fetch.py \
  --index claude-code/raw/index.json \
  --output claude-code/raw/pages/ \
  --tier 1

# 3. Fetch Tier 2 pages (important)
python scripts/docs-fetch.py \
  --index claude-code/raw/index.json \
  --output claude-code/raw/pages/ \
  --tier 2

# 4. Extract insights
python scripts/docs-extract.py \
  --input claude-code/raw/pages/ \
  --output claude-code/extracted/
```

## Requirements

```bash
pip install requests
```

Or use the built-in `venv`:

```bash
python3 -m venv venv
source venv/bin/activate
pip install requests
```

## Notes

- All scripts are idempotent (safe to run multiple times)
- Fetch script skips existing files
- Rate limiting prevents overwhelming target servers
- HTML conversion is basic but functional
