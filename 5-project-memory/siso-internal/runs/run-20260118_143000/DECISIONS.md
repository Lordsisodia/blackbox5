# DECISIONS - User Profile PRD Creation

**Run:** run-20260118_143000

---

## Technical Decisions

### DEC-001: Avatar Storage Strategy
**Decision:** Store avatars in Supabase Storage with Clerk metadata reference
**Rationale:** Decouples avatar from auth provider, enables better caching
**Impact:** Requires webhook sync between Clerk and Supabase

### DEC-002: Profile Privacy Levels
**Decision:** Three privacy levels - Public, Team Only, Private
**Rationale:** Covers all use cases without excessive complexity
**Impact:** Requires RLS policy updates

### DEC-003: Preference Storage
**Decision:** JSONB column for user preferences
**Rationale:** Flexible schema for future preference types
**Impact:** Type safety handled at application layer

## Scope Decisions

### DEC-004: MVP Features
**Decision:** Include profile view, edit, avatar, basic preferences
**Rationale:** Core functionality for launch
**Out of scope:** Social features, advanced privacy, activity history
