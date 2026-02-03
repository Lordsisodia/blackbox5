# TASK: Set up YouTube Auto-Scraper on Render

Status: pending
Priority: HIGH
Created: 2026-02-03
Project: AI-Improvement-Research (YouTube Scraper)

## Objective

Set up automated YouTube video scraping system that runs 24/7 on Render (free tier), scraping 23+ channels every hour without running on local laptop.

## Context

Current State:
- 7,219 videos collected from 11 channels
- Scripts working locally: collect_channel_optimized.py
- Data stored in: database/channels/*.json (~3.5MB)
- Config in: config/sources.yaml

Requirements:
- Must run on Render (free tier)
- Must scrape every hour (cron job)
- Must use existing file-based structure (JSON + YAML)
- Must be easy to add new channels via Claude CLI
- Must be documented for Claude/agent use

## Success Criteria

- [ ] Scraper runs on Render (not local laptop)
- [ ] Scrapes all 23 configured channels every hour
- [ ] Updates JSON files in database/channels/
- [ ] Commits changes back to GitHub repo
- [ ] Documentation exists for adding new channels
- [ ] Documentation exists for querying data
- [ ] Claude can add channels via CLI command

## Technical Constraints

Render Free Tier Limits:
- 750 hours/month (31.25 days) - tight but workable
- No persistent disk (ephemeral only)
- No native cron jobs (need workaround)
- 512MB RAM, shared CPU

## Approach Options

Option A: Render Web Service + External Ping
- Render web service stays running
- External ping every 10 minutes (Cron-Job.org)
- Internal scheduler runs hourly scrape
- Risk: 750hr limit, complex

Option B: GitHub Actions Cron (Recommended)
- GitHub Actions triggers hourly (cron)
- Runs on GitHub runner (fresh each time)
- Scrapes and commits to repo
- Pros: No sleep issues, truly unlimited

Option C: Hybrid (GitHub + Render)
- GitHub Actions triggers hourly
- Calls Render API to do scraping
- Render can sleep between calls

## Implementation Notes

Key Scripts to Create:
1. scripts/collect_github.py - Optimized for GitHub Actions
2. scripts/add_channel.py - CLI to add new creators
3. scripts/query_local.py - Query data locally
4. .github/workflows/scrape.yml - Hourly workflow

Documentation to Create:
1. docs/AGENT_GUIDE.md - How Claude adds channels
2. docs/QUERY_GUIDE.md - How to search data
3. docs/ARCHITECTURE.md - System overview

