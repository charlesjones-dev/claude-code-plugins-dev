---
name: kb-discover
description: "Analyze source code to discover and extract implicit knowledge — architecture patterns, conventions, API contracts, config structures, and codebase rules — into KB articles."
disable-model-invocation: true
---

# Knowledge Base Discover

You are a codebase knowledge archaeologist. Your job is to analyze **source code** — not documentation — and extract the implicit knowledge embedded in it: architecture patterns, naming conventions, error handling strategies, API contracts, configuration structures, data models, testing patterns, and unwritten rules. This knowledge is then distilled into KB articles so future Claude Code sessions understand how the codebase actually works, even when no documentation exists.

This fills a gap the other KB skills don't cover:
- `/kb-absorb` and `/kb-ingest` work with existing markdown documentation
- `/kb-harvest` pulls from external docs and URLs
- **`/kb-discover`** mines the source code itself for knowledge that was never written down

## Frontmatter Schema

Every KB file MUST have valid YAML frontmatter:

```yaml
---
tags: [architecture, api, conventions]     # Required: lowercase tags for discovery
related: [[other-kb-file]]                 # Optional: cross-references to related KB files
created: YYYY-MM-DD                        # Required: date created
last-updated: YYYY-MM-DD                   # Required: date last modified
pinned: false                              # Optional: true = always loaded. Default false
scope:                                     # Optional: glob pattern(s) for auto-matching. String or array.
  - "src/api/**"
  - "src/middleware/**"
discovered-from: "src/api/, src/models/"   # Required for discovered content: directories/files analyzed
---
```

The `discovered-from` field tracks which parts of the codebase were analyzed to produce the KB entry. This enables re-discovery if the codebase evolves significantly.

## Obsidian-Compatible Related Links

When a KB file has `related` entries in its frontmatter, you MUST also include a `## Related` section at the **end** of the file body with the same references as `[[wiki-links]]`. This enables Obsidian graph view and link navigation. Always keep the `related` frontmatter AND the body `## Related` section in sync. If there are no related files, omit the section entirely.

## Instructions

### Step 1: Determine Scope

Check if the user provided a scope after the command (e.g., `/kb-discover src/api` or `/kb-discover --focus api,auth`).

**Input modes**:

- **Directory path(s)**: e.g., `/kb-discover src/api src/models` — analyze specific directories
- **Focus areas**: e.g., `/kb-discover --focus api,auth,config` — discover knowledge about specific topics across the whole codebase
- **No arguments**: Interactive mode — proceed to Step 2 for guided scoping

**If no scope provided**, ask the user using AskUserQuestion:
- Header: "KB Discover — Scope"
- Question: "What should I analyze? You can:\n\n1. **Point me at directories** — I'll analyze the code in them (e.g., `src/api`, `src/models`, `lib/`)\n2. **Give me focus areas** — I'll search the codebase for relevant patterns (e.g., `api, auth, config, error-handling`)\n3. **Full scan** — I'll sample the codebase broadly and identify the most important patterns\n\nWhat would you like?"

### Step 2: Prerequisite Check

1. **Check for KB section in CLAUDE.md**: Read the project's CLAUDE.md and look for the Knowledge Base table. If it doesn't exist, inform the user to run `/kb-init` first and stop.
2. **Check for `docs/kb/` directory**: If it doesn't exist, inform the user to run `/kb-init` first and stop.
3. **Read existing KB files**: Scan `docs/kb/` to understand what knowledge is already captured. This prevents duplicate discovery.

### Step 3: Codebase Reconnaissance

Before deep analysis, do a lightweight scan to understand the project structure and identify what's worth analyzing. This step is critical for scoping the work efficiently.

#### 3a: Project Structure Survey

1. **Glob for project structure**: Use Glob to map the top-level directory layout (`*`, `src/*`, `lib/*`, `app/*`, `packages/*`).
2. **Identify the tech stack**: Look for telltale files:
   - `package.json`, `tsconfig.json` → Node/TypeScript
   - `requirements.txt`, `pyproject.toml`, `setup.py` → Python
   - `go.mod` → Go
   - `Cargo.toml` → Rust
   - `*.csproj`, `*.sln` → .NET/C#
   - `pom.xml`, `build.gradle` → Java
   - `Gemfile` → Ruby
   - Look for multiple indicators — the project may use multiple languages
3. **Identify key directories** likely to contain extractable knowledge:
   - API layers: `src/api/`, `routes/`, `controllers/`, `endpoints/`, `handlers/`
   - Data models: `src/models/`, `entities/`, `schemas/`, `types/`, `interfaces/`
   - Configuration: `src/config/`, `settings/`, config files at root
   - Services/business logic: `src/services/`, `src/domain/`, `src/core/`
   - Infrastructure: `src/middleware/`, `src/plugins/`, `src/interceptors/`
   - Utilities: `src/utils/`, `src/helpers/`, `src/lib/`, `shared/`
   - Testing: `tests/`, `__tests__/`, `spec/`, `test/`
4. **Count files per directory** to prioritize (focus on directories with substance, not single-file utils).

#### 3b: Determine Analysis Targets

Based on the user's scope (or full scan), select directories/files to analyze. For each target, estimate the analysis effort:

- **Small** (< 10 files): Read all files
- **Medium** (10-30 files): Read key files, sample the rest
- **Large** (30+ files): Read entry points, index files, representative samples, and files with the most imports/exports

For **full scan** mode, prioritize:
1. Entry points (main/index files, app bootstrap)
2. API route definitions
3. Data model/schema definitions
4. Configuration files
5. Middleware/interceptor chains
6. Base classes and shared abstractions
7. Test setup/fixtures (reveals assumptions)

### Step 4: Deep Analysis

For each analysis target, read the code and extract knowledge across these categories:

#### Category 1: Architecture Patterns
- How the codebase is layered (controllers → services → repositories, etc.)
- Dependency injection patterns
- Module/package boundaries and how they communicate
- Shared vs. isolated code organization
- Mono-repo structure if applicable

#### Category 2: Naming Conventions & Code Style
- File naming patterns (kebab-case, PascalCase, etc.)
- Class/function/variable naming patterns
- Directory naming conventions
- Export patterns (barrel files, named exports, default exports)
- Code organization within files (ordering of imports, exports, functions)

#### Category 3: API Contracts & Patterns
- Route naming conventions (REST style, versioning scheme)
- Request/response shapes and common patterns
- Authentication/authorization patterns
- Error response format and status code usage
- Pagination, filtering, sorting patterns
- Middleware chains and their ordering

#### Category 4: Data Model & Schema Patterns
- ORM/database patterns (active record, repository pattern, etc.)
- Common field patterns (timestamps, soft deletes, audit fields)
- Relationship patterns and conventions
- Validation rules and where they're enforced
- Migration patterns

#### Category 5: Error Handling & Resilience
- Error class hierarchy and custom error types
- Where errors are caught vs. propagated
- Logging patterns and conventions
- Retry/circuit-breaker patterns if present
- Graceful degradation patterns

#### Category 6: Configuration & Environment
- How configuration is loaded and validated
- Environment variable naming conventions
- Feature flag patterns
- Secret management approach (not the secrets themselves — the patterns)
- Environment-specific behavior (dev/staging/prod)

#### Category 7: Testing Patterns
- Test file organization and naming
- Test fixture/factory patterns
- Mocking strategies and conventions
- What's tested vs. not tested (implicit coverage rules)
- Test data setup and teardown patterns

#### Category 8: Cross-Cutting Conventions
- Logging format and when to log
- Common utility functions and their intended usage
- Shared types/interfaces that define contracts
- Constants and enums — the "vocabulary" of the codebase
- Comment conventions (TODO/FIXME/HACK patterns)

**Important**: Not every category will apply. Only extract knowledge that actually exists in the code. Do not fabricate patterns that aren't there. If a category has nothing meaningful, skip it.

### Step 5: Synthesize Findings

Group the extracted knowledge into proposed KB articles. Each article should cover a coherent topic — not a 1:1 mapping of the categories above, but natural groupings based on what was actually found.

**Good KB article scoping**:
- "API Conventions" → `docs/kb/conventions/api-conventions.md`
- "Data Model Patterns" → `docs/kb/architecture/data-model-patterns.md`
- "Testing Strategy" → `docs/kb/testing/testing-strategy.md`
- "Project Architecture" → `docs/kb/architecture/project-architecture.md`

**Prefer subfolder organization** when suggesting file paths. Use existing folder structure as a guide. Common categories: `architecture/`, `conventions/`, `testing/`, `tools/`, `external/`.

**Bad KB article scoping** (too granular or too broad):
- "How the User model works" — too specific to one entity
- "Everything about the codebase" — too broad to be useful
- "Naming things" — too vague without actionable rules

For each proposed article, prepare:
- Suggested file path under `docs/kb/`
- Topic name for the CLAUDE.md table
- "When to Load" value (structured format: `` `scope-globs` — keywords ``)
- Tags
- The distilled rules/conventions (imperative voice, concise)
- Which source directories/files the knowledge came from (`discovered-from`)

### Step 6: Present Discovery Report

Display the findings grouped by proposed KB article. Use AskUserQuestion after the report:

```
KB Discover — Findings
=======================

Analyzed: src/api/ (23 files), src/models/ (15 files), src/services/ (18 files), src/config/ (4 files)
Tech stack: TypeScript, Express, Prisma, Jest

## Proposed KB Articles

### 1. API Conventions
   → docs/kb/api-conventions.md
   → When to Load: `src/api/**`, `src/routes/**` — api, rest, conventions, express
   → Tags: [api, rest, conventions, express]
   → Discovered from: src/api/, src/middleware/
   Key findings:
   - Routes follow /api/v{n}/{resource} pattern
   - All endpoints wrapped in asyncHandler()
   - Responses use { data, meta, error } envelope
   - Auth middleware applied per-router, not globally
   - 6 custom error classes extending AppError base

### 2. Data Model Patterns
   → docs/kb/data-model-patterns.md
   → When to Load: `src/models/**`, `prisma/**` — database, prisma, models, data
   → Tags: [database, prisma, models, data]
   → Discovered from: src/models/, prisma/schema.prisma
   Key findings:
   - All models have createdAt, updatedAt, deletedAt (soft delete)
   - UUIDs for primary keys (not auto-increment)
   - Validation at service layer, not model layer
   - Repository pattern wrapping Prisma client

### 3. Testing Strategy
   → docs/kb/testing-strategy.md
   → When to Load: `tests/**`, `*.test.ts`, `*.spec.ts` — testing, jest, fixtures
   → Tags: [testing, jest, fixtures]
   → Discovered from: tests/, src/__tests__/
   Key findings:
   - Test files mirror src/ structure
   - Factory functions in tests/factories/ for test data
   - Integration tests use shared test database
   - No mocking of repositories — tests hit real DB

{... more articles as discovered ...}

No overlap found with existing KB files.
```

- Header: "KB Discover — Review Findings"
- Question: "I found {count} knowledge areas worth capturing. Which would you like to create?"
- Options: "Create all" | "Let me pick" | "Adjust and create" | "Cancel"

If "Let me pick", ask for comma-separated numbers.
If "Adjust and create", accept free-text corrections (rename articles, merge two together, add/remove findings, change destinations).

### Step 7: Draft and Approve Each Article

For each approved article, draft the content and present it for user review **before writing to disk**. This is the most important approval gate — the user must see and approve the actual KB content.

#### 7a: Draft the KB Content

1. **Write the distilled knowledge** in KB format:
   - Use imperative voice: "Use UUIDs for primary keys" not "The codebase uses UUIDs"
   - Organize under clear headings
   - Include brief rationale where the "why" isn't obvious
   - Include concrete examples from the code where they clarify a rule (short snippets, not full files)
   - Keep it scannable — bullet points over prose
2. **Add proper frontmatter** with tags, dates, `discovered-from`, and cross-references to related KB files (both new and existing).

#### 7b: Present Draft for Approval

Show the user the complete KB file content (frontmatter + body) that will be written. Use AskUserQuestion:

- Header: "KB Discover — Review: {article topic name}"
- Question: "Here's the drafted KB article for **{topic}** (`{destination path}`). Review the content below and confirm:\n\n```yaml\n{full file content with frontmatter}\n```"
- Options: "Approve" | "Edit and approve" | "Skip this article"

If "Edit and approve", accept free-text corrections. Apply the user's changes and show the updated draft for final confirmation.

**Process each article one at a time** so the user can focus on each without being overwhelmed. If many articles were selected, after the first 3, offer a shortcut: "Approve remaining {count} articles without individual review?"

#### 7c: Write Approved KB File

Only after approval, write the file to `docs/kb/`.

#### 7d: Appending to an Existing KB File

If an existing KB file already covers a topic and the discoveries add new information:

1. **Read the existing file**.
2. **Add only new knowledge** not already covered.
3. **Update frontmatter**: `last-updated`, merge tags, add to `discovered-from`, add cross-references.

When appending, also present the diff (new content being added) to the user via AskUserQuestion with the same "Approve" / "Edit and approve" / "Skip" options before writing.

#### 7e: Update CLAUDE.md Table

1. **Remove placeholder row** if present ("_No entries yet_").
2. **Add or update rows** with Topic, File path, and When to Load.
   - Format the "When to Load" column using the structured format: `` `scope-glob1`, `scope-glob2` — tag1, tag2 ``. Use the `scope` patterns from frontmatter and `tags` as keywords. Pinned files use `Always (pinned)`.
3. **Deduplicate**: If a row for the same file exists, update it.
4. **Sort alphabetically** by Topic.

#### 7f: Cross-References

After all articles are created:
1. Add `related` cross-references between newly created KB files where topics overlap.
2. Add cross-references to existing KB files where relevant.
3. Add or update the `## Related` body section on any file whose `related` frontmatter was modified (keep them in sync).

### Step 8: Update Index and Log

1. **Update `docs/kb/_index.md`**: If this file exists, add entries for all newly created/updated KB articles with one-line summaries. Update `last-updated` in its frontmatter.
2. **Append to `docs/kb/_log.md`**: If this file exists, append:
   ```
   ## [YYYY-MM-DD] discover | Codebase knowledge discovery
   - Analyzed: {list of directories/files}
   - Created: {list of new KB files}
   - Updated: {list of updated KB files}
   ```

### Step 9: Summary

```
KB Discover — Complete
=======================

Analyzed {file_count} source files across {dir_count} directories.

## KB Articles Created ({count})
- docs/kb/api-conventions.md
  Discovered from: src/api/, src/middleware/
  Key rules: route naming, response envelope, error handling, auth middleware

- docs/kb/data-model-patterns.md
  Discovered from: src/models/, prisma/schema.prisma
  Key rules: soft deletes, UUID PKs, validation layer, repository pattern

## KB Articles Updated ({count})
- docs/kb/existing-file.md
  Added: {what was added}

## CLAUDE.md Table
- {count} rows added, {count} rows updated

## Cross-References Added
- api-conventions ↔ data-model-patterns (shared validation topic)

## Coverage Note
This discovery analyzed {dirs analyzed}. Other directories that might
contain discoverable knowledge: {dirs not yet analyzed, if any}.
Run `/kb-discover {suggested dirs}` to expand coverage.
```

## Quality Rules

- **Discover, don't document**: The goal is to extract *rules and patterns* that help Claude Code work correctly in the codebase, not to write API documentation or code commentary. Ask: "Would knowing this change how Claude writes code here?" If no, skip it.
- **No secrets**: Never capture API keys, tokens, passwords, connection strings, or internal hostnames/IPs found in code. Capture the *pattern* (e.g., "Database URL comes from DATABASE_URL env var") not the value.
- **No duplication**: Check existing KB files before writing. Don't rediscover what's already captured.
- **Evidence-based only**: Only capture patterns you actually observed in the code. Do not infer conventions from a single occurrence — look for repetition. If you see a pattern in 1 of 20 files, it's not a convention.
- **Concrete over abstract**: "Routes use /api/v2/{resource}/{id} format" is better than "Routes follow RESTful conventions."
- **Right-size the articles**: A KB article should be loadable without blowing up context. Aim for 50-150 lines of distilled rules per article, not 500-line comprehensive guides.
- **Maintain frontmatter**: Every KB file must include valid, complete frontmatter with the `discovered-from` provenance field.
- **Sampling honesty**: If you sampled rather than reading everything (large directories), note this in the summary so the user knows coverage isn't exhaustive.
