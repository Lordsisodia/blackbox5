# ASSUMPTIONS

## Technical Assumptions
- GitHub public repo provides unlimited Actions minutes
- yt-dlp continues to work without API keys
- 7,219 videos (3.5MB) fits in GitHub repo (2GB limit)
- Hourly scraping won't hit rate limits with 2-sec delays

## User Assumptions
- User has GitHub account (lordsisodia)
- User will make repo public for free Actions
- User will add GITHUB_TOKEN secret for pushes

## Scope Assumptions
- 23 channels configured in config/sources.yaml
- Data format: JSON files in database/channels/
- No transcripts (metadata only for now)
- No ranking/analysis in Phase 1
