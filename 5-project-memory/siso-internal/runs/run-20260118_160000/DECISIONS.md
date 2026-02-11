# DECISIONS - User Profile Epic Creation

**Run:** run-20260118_160000

---

## Architectural Decisions

### DEC-001: Component Structure
**Decision:** 3 main components + 2 hooks architecture
**Rationale:** Balances reusability with simplicity
**Components:** ProfileCard, ProfileForm, AvatarUpload
**Hooks:** useProfile, useAvatar

### DEC-002: State Management
**Decision:** React Query for server state, local state for forms
**Rationale:** Optimistic updates, caching, error handling built-in
**Impact:** Adds dependency on @tanstack/react-query

### DEC-003: Form Handling
**Decision:** React Hook Form with Zod validation
**Rationale:** Performance, type safety, minimal re-renders
**Impact:** Consistent validation across all forms

## Technical Decisions

### DEC-004: Avatar Processing
**Decision:** Client-side image compression before upload
**Rationale:** Reduce storage costs and bandwidth
**Library:** browser-image-compression

### DEC-005: RLS Strategy
**Decision:** Row-level security with user_id checks
**Rationale:** Database-level security guarantees
**Policies:** 5 policies for read/write scenarios
