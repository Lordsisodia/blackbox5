# GitHub Repository Analysis Process v1.0

Systematic extraction of valuable patterns from GitHub repositories.

## Overview

This process analyzes GitHub repositories to extract actionable patterns, configurations, and insights for the Blackbox5 system.

## When to Use

- Analyzing Claude Code related repositories
- Extracting patterns from open source projects
- Building pattern libraries
- Researching best practices

## Prerequisites

- Repository cloned locally
- Basic understanding of repository structure
- Clear goal for what to extract

## The Process

### Phase 1: Repository Scan (5-10 min)

1. **README Analysis**
   - What is this repo?
   - What's the main value proposition?
   - Who created it and why?
   - What are the key features?

2. **Structure Mapping**
   ```bash
   tree -L 3
   find . -type f -name "*.md" | head -20
   find . -type f -name "*.json" | head -20
   find . -type f -name "*.yaml" -o -name "*.yml" | head -20
   ```

3. **Key Files Identification**
   - Configuration files
   - Documentation
   - Examples
   - Core implementations

### Phase 2: Deep Dive (15-30 min per component)

1. **Pattern Extraction**
   - Read core files completely
   - Identify reusable patterns
   - Note unique approaches
   - Document file locations

2. **Value Assessment**
   - What can we use immediately?
   - What needs adaptation?
   - What's the innovation?
   - How does it compare to what we have?

3. **Cross-Reference**
   - How does this relate to other repos?
   - What patterns are repeated?
   - What's unique here?

### Phase 3: Documentation (10-15 min)

1. **Create Extraction File**
   ```markdown
   ---
   repo: owner/name
   url: https://github.com/owner/name
   analyzed_at: YYYY-MM-DDTHH:MM:SSZ
   analyst: Claude

   ratings:
     actionability: X/35
     bb5_relevance: X/30
     pattern_quality: X/20
     innovation: X/15
     total: X/100

   classification:
     type: [awesome-list|framework|tool|educational|showcase]
     areas: []
     topics: []
   ---

   # Repo Name Analysis

   ## Overview
   Brief description of what this repo is.

   ## Key Findings

   ### Pattern 1: Name
   - Location: `path/to/file`
   - Description: What it does
   - Value: Why it matters
   - Actionability: Can we use it now?

   ### Pattern 2: Name
   ...

   ## Extractable Assets

   | Asset | Location | Priority | Notes |
   |-------|----------|----------|-------|
   | Asset name | path | High/Med/Low | Description |

   ## Implementation Notes

   ### Immediate Actions
   - [ ] Action 1
   - [ ] Action 2

   ### Requires Adaptation
   - Adaptation needed

   ### Reference Only
   - Good to know

   ## Related Repos

   - Similar to: repo-name
   - Complements: repo-name
   - Contrasts with: repo-name
   ```

2. **Update Pattern Library**
   - Copy patterns to `by_pattern/{category}/`
   - Tag with source repository
   - Note any dependencies

### Phase 4: Synthesis (5 min)

1. **Update Master Ratings**
   - Add to REPO-RATINGS.md
   - Justify scores

2. **Update Sources Config**
   - Add to config/sources.yaml
   - Tag with areas/topics

3. **Queue Actions**
   - Add actionable items to todo list
   - Prioritize based on ratings

## Output Structure

```
repo-analysis/
├── extracted/
│   └── {owner}-{repo}.md          # Full analysis
├── by_pattern/
│   ├── hooks/
│   │   └── {pattern-name}.md      # Extracted patterns
│   ├── skills/
│   ├── agents/
│   └── ...
├── REPO-RATINGS.md                # All repo scores
└── config/sources.yaml            # Tracked repos
```

## Quality Checklist

- [ ] README fully understood
- [ ] Key files identified and read
- [ ] Patterns extracted with locations
- [ ] Actionability assessed
- [ ] Cross-references noted
- [ ] Documentation complete
- [ ] Pattern library updated
- [ ] Ratings justified

## Iteration Notes

### v1.0 (Current)
- Initial process
- 4-phase approach
- Rating system: Actionability (35%), BB5 Relevance (30%), Pattern Quality (20%), Innovation (15%)

### Future Improvements
- [ ] Add automated structure scanning
- [ ] Create pattern comparison matrix
- [ ] Build dependency mapping
- [ ] Add visual pattern diagrams
