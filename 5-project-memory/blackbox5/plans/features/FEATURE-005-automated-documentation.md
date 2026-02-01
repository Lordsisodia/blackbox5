# FEATURE-005: Automated Documentation Generator

**Status:** active
**Priority:** high
**Type:** feature
**Estimated:** 90 minutes (~1.5 hours)

---

## User Value

**Who benefits:** RALF operators and developers
**What problem does it solve:** Documentation generation is manual and inconsistent. RALF produces task output (THOUGHTS.md, RESULTS.md, DECISIONS.md) and code, but documentation must be manually created and maintained.
**What value does it create:** Self-updating documentation, API docs, user guides, and technical specs generated automatically from code and task completions. Eliminates manual documentation overhead.

**Example:**
- Who: BlackBox5 operators (RALF maintainers)
- Problem: Feature documentation requires manual summarization from RESULTS.md, API docs outdated as code changes
- Value: Auto-generated feature docs from task output, API docs from code docstrings, README updates from recent activity

---

## Feature Scope

**MVP (Minimum Viable Product):**
- [ ] Parse task completion output (RESULTS.md, THOUGHTS.md, DECISIONS.md)
- [ ] Generate feature documentation from templates
- [ ] Generate API documentation from code docstrings
- [ ] Update README with recent activity summary
- [ ] Template-based generation (customizable markdown templates)

**Future Enhancements (out of scope for this feature):**
- [ ] Generate diagrams from code structure
- [ ] Multi-format output (PDF, HTML)
- [ ] Documentation quality scoring
- [ ] Auto-documentation of documentation system (meta-docs)

**Scope Boundaries:**
- **IN SCOPE:** Generate markdown documentation from existing task output and code files
- **OUT OF SCOPE:** Creating original content (documentation summarizes existing content), documentation review/quality assurance

---

## Context & Background

**Why this feature matters:**
- Documentation is a perennial maintenance burden, often outdated or missing
- Manual documentation creation is time-consuming and error-prone
- As RALF evolves, keeping docs in sync requires significant effort
- Automated documentation ensures docs are always current without manual effort

**Related Features:**
- Previous: TASK-1769916004 (Feature Framework) - Provides feature delivery template
- Previous: TASK-1769916006 (Feature Backlog) - Provides 12 planned features
- Current: F-005 enables automated documentation for all features

**Current State:**
- Documentation must be manually written after each task
- API docs require manual extraction from code
- README updates are manual, often forgotten
- No documentation generation automation exists

**Desired State:**
- Feature docs auto-generated from task RESULTS.md
- API docs auto-generated from code docstrings
- README auto-updated with recent activity
- Documentation always in sync with system state

---

## Success Criteria

### Must-Have (Required for completion)
- [ ] Documentation parser implemented - parse_task_output() extracts key sections from RESULTS.md
- [ ] Code parser implemented - parse_code_files() extracts docstrings and comments
- [ ] Documentation generator implemented - generate_feature_doc() creates docs from templates
- [ ] API docs generator implemented - generate_api_docs() creates API documentation
- [ ] Template system working - Feature doc, API doc, README update templates functional
- [ ] Integration working - Docs generated on task completion (async, non-blocking)
- [ ] User documentation complete - auto-docs guide exists (operations/.docs/auto-docs-guide.md)

### Should-Have (Important but not blocking)
- [ ] Markdown rendering validation - Generated docs render properly on GitHub
- [ ] Template customization - Template editing doesn't break generation
- [ ] Error handling - Invalid markdown, missing files handled gracefully

### Nice-to-Have (If time permits)
- [ ] Documentation generation on-demand - CLI command to regenerate docs
- [ ] Incremental updates - Only regenerate changed sections
- [ ] Documentation versioning - Track doc history

### Verification Method
- [ ] Manual testing: Generate docs for last 3 tasks, verify quality
- [ ] Integration testing: Complete a task, verify docs auto-generated
- [ ] Documentation review: auto-docs guide covers all functionality

---

## Technical Approach

### Implementation Plan

**Phase 1: Feature Specification Creation**
- [ ] Read backlog entry for F-005
- [ ] Create feature specification (this file)
- [ ] Document user value, MVP scope, success criteria, technical approach

**Phase 2: Architecture Design**
- [ ] Analyze existing documentation sources (RESULTS.md, code files)
- [ ] Design documentation pipeline (parser → generator → templates)
- [ ] Document architecture decision

**Phase 3: Implementation**
- [ ] Create doc_parser.py (parse task output, code files)
- [ ] Create doc_generator.py (generate docs from templates)
- [ ] Create templates (feature doc, API doc, README update)

**Phase 4: Integration**
- [ ] Integrate with RALF-Executor post-completion workflow
- [ ] Test: Complete task, verify docs generated
- [ ] Validate: Async generation doesn't block completion signal

**Phase 5: Documentation**
- [ ] Create operations/.docs/auto-docs-guide.md
- [ ] Document architecture, usage, configuration, troubleshooting

### Architecture & Design

**Key Components:**

1. **Documentation Parser (doc_parser.py)**
   - `parse_task_output(task_id)` - Extracts key sections from RESULTS.md, THOUGHTS.md, DECISIONS.md
   - `parse_code_files(file_paths)` - Extracts docstrings and comments from Python files
   - `extract_metadata(run_dir)` - Extracts metadata.yaml information

2. **Documentation Generator (doc_generator.py)**
   - `generate_feature_doc(task_id, template)` - Creates feature documentation from task output
   - `generate_api_docs(code_paths, template)` - Creates API documentation from code
   - `update_readme(recent_activity, template)` - Updates README with recent activity

3. **Template System (.templates/docs/)**
   - `feature-doc.md.template` - Feature documentation template
   - `api-doc.md.template` - API documentation template
   - `readme-update.md.template` - README update template

**Integration Points:**
- RALF-Executor: Post-completion workflow (after writing THOUGHTS.md, RESULTS.md, DECISIONS.md)
- Roadmap sync: Auto-doc generation runs after queue sync

**Data Flow:**
```
Task Completion → RESULTS.md + THOUGHTS.md + DECISIONS.md
                                    ↓
                            doc_parser.py (extract key sections)
                                    ↓
                            doc_generator.py (fill templates)
                                    ↓
                    Feature Doc + API Doc + README Update
```

---

## Dependencies

### Requires (Prerequisites)
- [x] TASK-1769916004 (Feature Framework) - COMPLETE - Provides feature delivery template
- [x] TASK-1769916006 (Feature Backlog) - COMPLETE - Provides 12 planned features
- [ ] Existing task output format (RESULTS.md, THOUGHTS.md, DECISIONS.md) - STABLE

### Blocks (Dependents)
- [None identified]

### External Dependencies
- [ ] Python standard library (yaml, markdown, re, pathlib)
- [ ] No external packages required (uses stdlib only)

---

## Rollout Plan

### Testing Strategy
**Unit Tests:**
- [Test 1]: parse_task_output() extracts task_id, status, what_was_done from RESULTS.md
- [Test 2]: parse_code_files() extracts docstrings from Python files
- [Test 3]: generate_feature_doc() produces valid markdown

**Integration Tests:**
- [Test 1]: Complete task, verify feature doc generated in correct location
- [Test 2]: Modify code, verify API docs updated
- [Test 3]: Generate README update, verify format correct

**User Acceptance Tests:**
- [Test 1]: Generate docs for last 3 tasks, verify quality and completeness
- [Test 2]: Customize template, verify generation still works
- [Test 3]: Invalid markdown in source, verify error handled gracefully

### Deployment Strategy
- **Deployment Method:** Direct deployment (no feature flags needed)
- **Rollback Plan:** Remove doc generation call from executor workflow
- **Monitoring:** Track doc generation time, error rate

---

## Files to Modify

### New Files (Create)
- `plans/features/FEATURE-005-automated-documentation.md` - Feature specification (this file)
- `2-engine/.autonomous/lib/doc_parser.py` - Documentation parser (210 lines est.)
- `2-engine/.autonomous/lib/doc_generator.py` - Documentation generator (370 lines est.)
- `.templates/docs/feature-doc.md.template` - Feature doc template (80 lines est.)
- `.templates/docs/api-doc.md.template` - API doc template (60 lines est.)
- `.templates/docs/readme-update.md.template` - README update template (40 lines est.)
- `operations/.docs/auto-docs-guide.md` - User documentation (450 lines est.)

### Existing Files (Modify)
- `2-engine/.autonomous/prompts/ralf-executor.md` - Add doc generation to post-completion workflow
- `README.md` - Add "Recent Activity" section (auto-updated by doc_generator)

---

## Risk Assessment

### Technical Risks
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Generated docs low quality | Medium | Medium | Start with task-generated docs (high quality source), expand to code later |
| Templates require maintenance | Low | Low | Keep templates simple, use standard markdown |
| Integration adds overhead | Low | Low | Run async, don't block task completion signaling |
| Markdown parsing errors | Medium | Low | Validate output, handle errors gracefully |

### Operational Risks
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Doc generation fails silently | Low | Low | Log errors, validate output exists |
| Template syntax errors | Medium | Low | Template validation before use |
| File permission issues | Low | Low | Check write permissions before generation |

---

## Effort Estimation

**Estimated Breakdown:**
- Design: 15 minutes (read existing docs, design pipeline)
- Implementation: 45 minutes (parser: 15, generator: 20, templates: 10)
- Testing: 20 minutes (test parser, generator, integration)
- Documentation: 10 minutes (auto-docs guide)
- **Total:** 90 minutes (~1.5 hours)

**Complexity Factors:**
- [x] Integration complexity (low/med/high) - Medium (executor integration)
- [x] Technical uncertainty (low/med/high) - Low (stdlib only, clear requirements)
- [x] Dependencies (low/med/high) - Low (no external dependencies)

---

## Dates

**Created:** 2026-02-01T13:41:00Z
**Started:** 2026-02-01T13:41:00Z
**Completed:** PENDING

---

## Notes

**Strategic Value:**
This feature enables "documentation as a byproduct" - documentation is generated automatically from normal RALF operations, not as a separate manual task. This reduces documentation friction and ensures docs stay in sync with system evolution.

**Success Metrics:**
- [Feature Documentation]: 100% of tasks have auto-generated feature docs
- [API Documentation]: API docs reflect current codebase state
- [README Freshness]: README updated with last 24 hours of activity
- [Time Saved]: ~15 minutes per task saved (no manual doc writing)

**Open Questions:**
- [Template Location]: Where to store generated docs? → Answer: plans/features/docs/ (auto-generated)
- [Generation Frequency]: When to generate docs? → Answer: On task completion (async)
- [README Updates]: How often to update README? → Answer: Daily (via cron or planner loop)

**Learnings (to be filled after completion):**
- [What went well]
- [What could be improved]
- [Recommendations for future features]
