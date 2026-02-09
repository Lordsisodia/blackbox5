# Research Inbox

Quick capture zone for unprocessed research items.

## Philosophy

**Capture first, organize later.** Don't let organization friction stop you from saving valuable resources.

## Structure

```
_inbox/
├── external/           # External sources (GitHub, YouTube, articles)
│   ├── raw/           # Unprocessed captures
│   ├── processing/    # Currently being reviewed
│   └── archived/      # Processed and moved to main structure
│
├── internal/          # Internal thoughts, notes, ideas
│   ├── raw/
│   ├── processing/
│   └── archived/
│
└── unsorted/          # Don't know where it goes yet
    ├── raw/
    ├── processing/
    └── archived/
```

## How to Use

1. **Quick Capture**: Dump URLs, files, notes into `*/raw/`
2. **Tag it**: Add a markdown file with the same name containing metadata
3. **Process**: Move to `processing/` when reviewing
4. **Archive**: Move to `archived/` after reallocation

## Quick Capture Template

Create a `.md` file alongside captured content:

```markdown
---
captured_at: YYYY-MM-DDTHH:MM:SSZ
source: [github|youtube|article|other]
url: "..."
tags: [tag1, tag2]
status: [raw|processing|archived]
priority: [high|medium|low]
---

# Title

Quick notes about what this is and why it matters.

## Potential Classification

- Area: ...
- Topic: ...
- Suggested location: ...

## Action Items

- [ ] Review content
- [ ] Extract key insights
- [ ] Move to appropriate folder
```

## Current Inbox Items

| Item | Source | Captured | Status |
|------|--------|----------|--------|
| (empty) | - | - | - |
