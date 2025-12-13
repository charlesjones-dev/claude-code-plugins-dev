---
name: plan-phases
description: "Use when creating implementation plans, phase planning documents, breaking features into phases, or when /workflow-plan-phases command is invoked. Provides methodology for context-efficient phase sizing and dependency analysis."
---

# Phase Planning Skill

This skill provides methodology for creating implementation plans that are optimized for sub-agent execution, with properly sized phases that respect context window constraints.

## Overview

A good phase plan:
1. Breaks work into independently executable chunks
2. Sizes phases to fit within sub-agent context budgets
3. Minimizes dependencies between phases where possible
4. Provides clear acceptance criteria for verification
5. Uses whole number phases only (no 1.1, 1.2 sub-phases)

---

## Step 1: Gather Requirements (Always Ask Questions)

**Never skip this step.** Even if the description seems complete, clarifying questions:
- Reveal implicit assumptions
- Uncover edge cases
- Establish scope boundaries
- Identify existing constraints

### Question Categories

**Scope & Boundaries**
- What's explicitly OUT of scope?
- Is this greenfield or integrating with existing code?
- Are there existing patterns/conventions to follow?
- What's the target completion state? MVP or production-ready?

**Technical Context**
- What's the tech stack? (language, framework, database)
- Are there existing models/services this builds on?
- What authentication/authorization exists?
- Are there performance requirements?

**Integration Points**
- What external services/APIs are involved?
- Are there existing interfaces to conform to?
- What other systems will consume this?
- Are there upstream dependencies not yet built?

**User Experience**
- Who are the users? (end users, admins, developers, APIs)
- What's the primary workflow/happy path?
- What error states need handling?
- Are there accessibility requirements?

**Constraints**
- Security requirements? (OWASP, compliance, data sensitivity)
- Testing requirements? (coverage, E2E, specific frameworks)
- Documentation requirements?
- Deployment constraints?

### Question Presentation Format

Present 3-5 targeted questions based on the description:

```markdown
Before I create the implementation plan, I have a few questions:

1. **Existing Code**: Is this a new feature in an existing codebase, or greenfield?
   If existing, what patterns should I follow?

2. **Auth Context**: You mentioned user roles - is there an existing auth system
   to integrate with, or is that part of this work?

3. **Data Layer**: What database are you using? Are there existing models
   this relates to?

4. **Scope Boundary**: Should this include the admin UI for managing X,
   or just the core functionality?

5. **Testing**: What level of test coverage do you need? Unit only,
   or integration/E2E as well?
```

Wait for answers before proceeding.

---

## Step 2: Phase Sizing Guidelines

### Context Budget Per Phase

Target each phase to consume **30-50k tokens** of sub-agent context:
- ~10k tokens: Phase spec + project context (CLAUDE.md, conventions)
- ~15-25k tokens: File reads and code analysis
- ~10-15k tokens: Implementation work and verification

### Sizing Heuristics

**RIGHT-SIZED Phase** (~30-50k tokens):
- Creates/modifies 2-5 files
- Implements 1-2 closely related features
- Can be verified with a clear test or check
- Completes in one sub-agent session without compacting

**TOO LARGE Phase** (>60k tokens - split it):
- Creates/modifies 6+ files
- Implements multiple unrelated features
- Requires reading large portions of codebase
- Description exceeds ~500 words
- Contains words like "and also", "as well as", "plus"

**TOO SMALL Phase** (<15k tokens - combine it):
- Single file change
- Config-only changes
- Simple additions with no logic
- Could be done in 5 minutes manually

### Splitting Strategy

When a phase is too large, split by:

1. **Layer**: Separate data model, business logic, API, UI
2. **Entity**: One phase per core entity/resource
3. **Operation**: Separate CRUD operations if complex
4. **Concern**: Separate core logic from error handling, logging, etc.

**Example - Too Large:**
```
Phase 1: Build user management with registration, login, profile
editing, password reset, email verification, and admin user listing
```

**Split Into:**
```
Phase 1: User model and registration endpoint
Phase 2: Login and session management
Phase 3: Password reset flow
Phase 4: Email verification
Phase 5: Profile editing
Phase 6: Admin user listing
```

---

## Step 3: Dependency Planning

### Dependency Types to Track

**Hard Dependencies** (must complete first):
- Schema/model that other phases import
- Auth middleware other phases use
- Shared utilities or helpers
- Base classes being extended

**Soft Dependencies** (preferred order, but parallelizable):
- Related features that share patterns
- Test setup that other tests use
- Documentation that references implementation

**No Dependencies** (fully parallel):
- Isolated features
- Different layers of same feature (if interfaces defined upfront)
- Independent utilities

### Minimizing Dependencies

Strategies to reduce coupling between phases:

1. **Define interfaces early**: First phase exports types/interfaces,
   later phases implement against them

2. **Stub dependencies**: Phase can stub what it needs, later phase
   replaces stub with real implementation

3. **Feature flags**: Phases can merge independently, enable via flag

4. **Vertical slices**: Each phase is a thin vertical slice through all
   layers rather than horizontal layers

---

## Step 4: Plan Document Structure

### File Location

```
docs/plans/{feature-name}.md
```

Slugify the feature name:
- "User Authentication System" -> `user-authentication-system.md`
- "API Rate Limiting" -> `api-rate-limiting.md`

### Document Template

```markdown
# {Feature Name} Implementation Plan

## Overview
{2-3 sentence summary of what this plan delivers}

## Goals
- {Primary goal}
- {Secondary goal}
- {Tertiary goal}

## Non-Goals (Out of Scope)
- {Explicit exclusion 1}
- {Explicit exclusion 2}

## Technical Context
- **Stack**: {language, framework, database}
- **Existing Code**: {relevant existing modules/patterns}
- **Integration Points**: {external services, APIs}

---

## Phase 1: {Phase Name}

### Objective
{One sentence describing what this phase accomplishes}

### Specification
{Detailed description of the work. Include:}
- What to create/modify
- Specific requirements
- Edge cases to handle
- Error handling expectations

### Files to Create/Modify
- `path/to/file.ts` - {purpose}
- `path/to/other.ts` - {purpose}

### Acceptance Criteria
- [ ] {Verifiable criterion 1}
- [ ] {Verifiable criterion 2}
- [ ] {Verifiable criterion 3}

### Dependencies
- **Requires**: {None | Phase X}
- **Blocks**: {Phase Y, Phase Z}

### Estimated Scope
- Files: {2-5}
- Complexity: {Low | Medium | High}

---

## Phase 2: {Phase Name}

{Same structure as Phase 1}

---

## Execution Strategy

### Dependency Graph
```
Phase 1 --+-- Phase 3
          |
Phase 2 --+
          |
Phase 4 <-+-- Phase 5
```

### Recommended Execution
- **Parallel Group 1**: Phase 1, Phase 2
- **Sequential**: Phase 3 (after Phase 1)
- **Parallel Group 2**: Phase 4, Phase 5 (after Phase 3)

---

## Verification Checklist

After all phases complete:
- [ ] {Integration verification 1}
- [ ] {Integration verification 2}
- [ ] {End-to-end test}

## Open Questions

- {Any unresolved decisions to revisit}
```

---

## Step 5: Phase Writing Guidelines

### Phase Names

Use action-oriented names:
```
Good:
- "Create User Model and Repository"
- "Implement JWT Authentication"
- "Add Rate Limiting Middleware"
- "Build Password Reset Flow"

Bad:
- "User Stuff"
- "Part 1"
- "Backend Work"
- "Misc Improvements"
```

### Specification Writing

Be specific enough that a sub-agent can implement without guessing:

```
Vague:
"Add user authentication"

Specific:
"Create POST /api/auth/login endpoint that:
- Accepts { email, password } body
- Validates against User model
- Returns JWT token with 24h expiry on success
- Returns 401 with { error: 'Invalid credentials' } on failure
- Rate limits to 5 attempts per 15 minutes per IP
- Logs failed attempts with IP and email (not password)"
```

### Acceptance Criteria

Write testable criteria:

```
Not Testable:
- "Works correctly"
- "Handles errors"
- "Is secure"

Testable:
- "POST /api/users returns 201 with user object (excluding password)"
- "Invalid email format returns 400 with validation error"
- "Passwords are hashed with bcrypt cost factor 12"
- "JWT tokens expire after 24 hours"
```

---

## Anti-Patterns to Avoid

### No Sub-Phases
```
Wrong:
Phase 1: Setup
  Phase 1.1: Database schema
  Phase 1.2: Model classes
  Phase 1.3: Repository layer

Right:
Phase 1: Database Schema and Migrations
Phase 2: User Model and Repository
Phase 3: Authentication Service
```

### No Kitchen Sink Phases
```
Wrong:
Phase 3: Implement all remaining features including search,
filtering, pagination, sorting, export, and batch operations

Right:
Phase 3: List Endpoint with Pagination
Phase 4: Search and Filtering
Phase 5: Sorting Options
Phase 6: Export Functionality
Phase 7: Batch Operations
```

### No Vague Phases
```
Wrong:
Phase 2: Handle edge cases and fix bugs

Right:
Phase 2: Input Validation and Error Handling
- Validate email format, password strength
- Handle duplicate email registration
- Return structured error responses
```

### No Dependency Spaghetti
```
Wrong:
Phase 1 depends on Phase 3
Phase 3 depends on Phase 2
Phase 2 depends on Phase 4
Phase 4 depends on Phase 1  (circular!)

Right:
Phase 1: Foundation (no dependencies)
Phase 2: Core Logic (depends on 1)
Phase 3: Extended Features (depends on 2)
Phase 4: Polish and Edge Cases (depends on 3)
```

---

## Final Checklist

Before delivering plan:

- [ ] Asked clarifying questions and incorporated answers
- [ ] Each phase is 30-50k tokens of work (2-5 files)
- [ ] No sub-phases (whole numbers only)
- [ ] Every phase has clear acceptance criteria
- [ ] Dependencies are explicit and acyclic
- [ ] Specifications are detailed enough to implement without guessing
- [ ] File saved to docs/plans/{feature-name}.md

---

## IMPORTANT: Planning Only — Do Not Implement

**This skill is for planning only. After creating the plan, STOP.**

Do NOT:
- Start implementing any phases
- Write any code
- Create any files other than the plan document
- Begin execution automatically

After the plan is complete:
1. Present the plan document to the user
2. Ask if they want to make any revisions
3. Inform them to use `/workflow-implement-phases` or the `implement-phases` skill when ready to execute

The user decides when to proceed with implementation.
