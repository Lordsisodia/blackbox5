# TASK-20260210-192900: Fix YouTube Scraper

**Status:** pending
**Priority:** HIGH
**Type:** fix
**Created:** 2026-02-10T19:29:00Z
**Estimated Lines:** 1,200
**Estimated Minutes:** 3.8

---

## Objective

Fix the YouTube scraper that is failing to extract video metadata from YouTube watch pages.

---

## Research & Analysis Phase

- [ ] Reproduce the scraper failure with example YouTube URLs
- [ ] Analyze current scraper implementation to identify the root cause
- [ ] Check if YouTube page structure has changed (DOM elements, classes, API endpoints)
- [ ] Test current extraction patterns against a sample of videos
- [ ] Document findings: what changed, why it broke, and what needs updating

---

## Success Criteria

- [ ] Scraper successfully extracts video metadata from test URLs
- [ ] All required fields are captured (title, description, views, upload date, duration, etc.)
- [ ] Error handling gracefully manages rate limits and network issues
- [ ] Unit tests pass for all extraction functions
- [ ] Integration tests pass with real YouTube URLs
- [ ] Scraper processes at least 100 videos without errors
- [ ] Documentation updated with any new patterns or limitations

---

## Implementation Approach

1. **Diagnose the Issue**
   - Run scraper on known URLs and capture errors
   - Inspect HTML structure of current YouTube pages
   - Identify which selectors/patterns are no longer working

2. **Update Selectors and Patterns**
   - Update CSS selectors for title, description, views, etc.
   - Update regex patterns for extracting metadata
   - Handle new YouTube page layout changes (new DOM structure)

3. **Improve Error Handling**
   - Add better logging for debugging extraction failures
   - Implement retry logic for transient failures
   - Add fallback selectors for edge cases

4. **Add Monitoring**
   - Log extraction success/failure rates
   - Track which fields are missing when extraction fails
   - Add alerts for systematic failures

5. **Test Thoroughly**
   - Unit tests for each extraction function
   - Integration tests with real YouTube URLs
   - Test edge cases (age-restricted videos, deleted videos, live streams)

---

## Testing Checklist

- [ ] Unit tests pass for all extraction functions
- [ ] Integration tests pass with sample YouTube URLs
- [ ] Scraper handles rate limits gracefully
- [ ] Error handling works for network timeouts
- [ ] Missing metadata fields are logged appropriately
- [ ] Scraper recovers from partial extraction failures
- [ ] Tests include edge cases (deleted videos, private videos, live streams)

---

## Context

**Original Request:** "I need to fix the YouTube scraper"

**Inferred Priority:** HIGH (use of "need to" indicates urgency)

**Likely Cause:** YouTube may have updated their page structure or changed CSS class names, breaking existing selectors.

**Key Files to Investigate:**
- `bin/youtube-scraper.py` or similar
- Any configuration files with selectors/patterns
- Recent logs showing specific error messages

---

## Files to Modify

- `bin/youtube-scraper.py` (or main scraper file): Update selectors and extraction logic
- `tests/test-youtube-scraper.py`: Update tests to match new patterns
- `docs/youtube-scraper.md`: Document any changes or new limitations

---

## Files to Create

- `tests/fixtures/youtube-samples.html`: Sample HTML for testing (if needed)
- `logs/scraper-debug.log`: Detailed logging for debugging

---

## Rollback Strategy

If the fix causes issues:
1. Restore previous version of scraper from git
2. Keep detailed logs of what changed
3. Maintain a fallback extraction mode
4. Revert to previous selector set as emergency measure

---

## Notes

- YouTube changes frequently; consider using their API if available
- Rate limiting is important to avoid IP bans
- Video metadata extraction may require JavaScript rendering for some fields
- Consider using a library like `yt-dlp` as a reference or fallback

**Estimated Duration:** 30-45 minutes depending on the extent of changes
