---
name: kb-harvest
description: "Harvest knowledge from external sources — sibling repos, local directories, individual files, or web URLs — and distill them into the KB system with provenance tracking."
disable-model-invocation: true
---

# Knowledge Base Harvest

You are a cross-source knowledge harvester. Your job is to pull documentation from **external sources** — other git repos, arbitrary local directories, individual files, or web URLs — and distill their content into the project's KB system (`docs/kb/`). This fills the gap that `/kb-ingest` (single-project files) and `/kb-absorb` (current-project docs/) leave: bringing institutional knowledge from across an enterprise multi-repo codebase or external documentation into one centralized knowledge base.

## Frontmatter Schema

Every KB file MUST have valid YAML frontmatter. This skill adds a `source` field for provenance tracking:

```yaml
---
tags: [topic-tag-1, module:module-name]    # Required: lowercase tags for discovery. Auto-add module tag.
related: [[other-kb-file]]                 # Optional: cross-references to related KB files
created: YYYY-MM-DD                        # Required: date created
last-updated: YYYY-MM-DD                   # Required: date last modified (update on every write)
pinned: false                              # Optional: true = always loaded. Default false
scope: "src/api/**"                        # Optional: glob pattern(s) for auto-matching. String or array.
source: "C:/Source/billing-module/docs/api-conventions.md"  # Required for harvested content: original source path or URL
---
```

The `source` field is what distinguishes harvested KB entries from organically captured ones. It enables future re-harvesting if source docs are updated.

**Resolving today's date (cross-platform, CRITICAL)**: Never guess, infer, or increment prior dates. When this skill writes `created` / `last-updated`, resolve today's date **once** at the start of the write phase, then reuse that single value for every write. Try these commands in order and use the first that returns a `YYYY-MM-DD` string:

- **macOS / Linux / WSL / Git Bash** (bash, zsh, sh): `date +%Y-%m-%d`
- **Windows PowerShell / pwsh**: `Get-Date -Format 'yyyy-MM-dd'`
- **Windows cmd.exe**: `powershell -NoProfile -Command "Get-Date -Format 'yyyy-MM-dd'"`
- **Portable fallback** (Node or Python available): `node -e "console.log(new Date().toISOString().slice(0,10))"` or `python -c "import datetime; print(datetime.date.today().isoformat())"`

Only update `last-updated` when the file's content actually changed. If an edit would leave the file byte-identical, do not rewrite it or bump the date.

## Obsidian-Compatible Related Links

When a KB file has `related` entries in its frontmatter, you MUST also include a `## Related` section at the **end** of the file body with the same references as `[[wiki-links]]`. This enables Obsidian graph view and link navigation. Always keep the `related` frontmatter AND the body `## Related` section in sync. If there are no related files, omit the section entirely.

## Instructions

### Step 1: Determine Input Sources

Check if the user provided source(s) after the command. Sources can be **mixed** — any combination of:

- **Directory paths** (local): e.g., `C:/Source/billing-module/docs/` or `/repos/auth-service/docs`
- **File paths** (local): e.g., `C:/Source/billing-module/docs/api-guide.md`
- **Glob patterns** (local): e.g., `C:/Source/*/docs/**/*.md`
- **Web URLs**: e.g., `https://wiki.internal.company.com/billing/api-patterns`

**If source(s) provided**: Parse and categorize each as directory, file, glob, or URL.
**If no source provided**: Ask the user using AskUserQuestion:
- Header: "KB Harvest — Sources"
- Question: "What would you like to harvest? You can provide any mix of:\n- **Directory paths** to scan for markdown files (e.g., `C:/Source/billing/docs/`)\n- **File paths** for specific files (e.g., `C:/Source/billing/docs/api-guide.md`)\n- **Glob patterns** (e.g., `C:/Source/*/docs/**/*.md`)\n- **Web URLs** to fetch and distill (e.g., `https://wiki.example.com/some-page`)\n\nEnter one or more sources (space-separated or one per line):"

### Step 2: Prerequisite Check

1. **Check for KB section in CLAUDE.md**: Read the project's CLAUDE.md and look for the Knowledge Base table. If it doesn't exist, inform the user to run `/kb-init` first and stop.
2. **Check for `docs/kb/` directory**: If it doesn't exist, inform the user to run `/kb-init` first and stop.

### Step 3: Discovery

Process each source and build a discovery report:

#### 3a: Local Directories

1. Use Glob to find all `.md` files recursively within the directory.
2. Exclude common non-documentation files: `CHANGELOG.md`, `LICENSE.md`, `node_modules/`, `.git/`, `dist/`, `build/`, `coverage/`.
3. For each file found, read the first ~30 lines to get a title/summary.
4. **Infer module name** from the directory structure:
   - If the path looks like `{base}/{module-name}/docs/...`, use `{module-name}` as the module tag.
   - If the path looks like `{base}/{module-name}/...`, use `{module-name}`.
   - If ambiguous, use the immediate parent directory of the docs folder.

#### 3b: Individual Files

1. Verify the file exists and is readable.
2. Read the first ~30 lines for title/summary.
3. Infer module name from the file's directory path (same logic as 3a).

#### 3c: Glob Patterns

1. Execute the glob pattern using the Glob tool.
2. Apply the same exclusions as 3a.
3. For each matched file, read first ~30 lines.
4. Infer module name per file.

#### 3d: Web URLs

1. Use WebFetch to retrieve the page content for each URL.
2. If the fetch fails, report the error and mark the URL as FAILED in the discovery report.
3. Extract the page title and a brief summary from the fetched content.
4. **Infer a topic name** from the URL path segments and page title.

### Step 4: Present Discovery Report

Display a grouped report. Use AskUserQuestion after the report:

```
KB Harvest — Discovery Report
==============================

## Local Sources

### module-name (C:/Source/module-name/docs/) — {count} files
  1. [x] api-conventions.md — "API Conventions and Patterns"
  2. [x] deployment.md — "Deployment Procedures"
  3. [x] troubleshooting.md — "Common Issues and Fixes"

### other-module (C:/Source/other-module/docs/) — {count} files
  4. [x] data-model.md — "Data Model Reference"
  5. [ ] README.md — "Module README" (likely not KB material)

## Web Sources — {count} URLs
  6. [x] https://wiki.example.com/billing/api — "Billing API Integration Guide"
  7. [ ] https://wiki.example.com/onboarding — FAILED: 404 Not Found

Total: {count} sources ready for harvest
```

Pre-check files that look like they contain actionable knowledge. Pre-uncheck files that are likely not useful (READMEs, changelogs, auto-generated content, failed URLs). The user can toggle selections.

- Header: "KB Harvest — Select Sources"
- Question: "Which sources would you like to harvest? Enter the numbers to toggle (e.g., `1,3,5` or `all` or `none`), or confirm to proceed with the current selection."
- Options: "Proceed with selection" | "Select all" | "Deselect all" | "Let me pick" | "Cancel"

If "Let me pick", ask for comma-separated numbers.

### Step 5: Analyze Selected Sources

For each selected source:

1. **Read the full content** (local file) or **use the already-fetched content** (URL).
2. **Classify the content**:
   - **Actionable knowledge**: Rules, conventions, patterns, constraints, decisions, gotchas, architecture decisions, API contracts — things that change how Claude Code should work. This belongs in the KB.
   - **Reference material**: Tutorials, onboarding docs, API references that are informational but don't contain actionable rules. Flag but allow ingestion if the user wants.
   - **Not suitable**: Binary content, auto-generated docs, pure changelogs, or empty/trivial content. Inform the user and skip.
3. **Propose a KB destination**:
   - Suggest a file path under `docs/kb/` using subfolder organization based on the content topic and module name (e.g., `docs/kb/external/billing-api-conventions.md`, `docs/kb/conventions/auth-token-handling.md`). Use existing folder structure as a guide.
   - Check existing KB files for topic overlap — propose appending if a good match exists.
4. **Suggest tags**: Include `module:{module-name}` automatically for local sources. Add topic-specific tags inferred from content.
5. **Build "When to Load"**: Construct the structured loading context:
   - Extract or infer scope glob patterns from the content (e.g., `src/billing/**`).
   - Use the suggested tags as keywords.
   - Format as: `` `scope-glob1` — keyword1, keyword2 ``
   - Example: `` `src/billing/**` — module:billing, api, conventions ``

### Step 6: Present Ingestion Plan

Show a consolidated plan for all selected sources. Use AskUserQuestion:

```
KB Harvest — Ingestion Plan
=============================

1. C:/Source/billing/docs/api-conventions.md
   → NEW: docs/kb/billing-api-conventions.md
   → Tags: [module:billing, api, conventions, rest]
   → When to Load: `src/billing/**` — module:billing, api, conventions
   → Content type: Actionable knowledge

2. C:/Source/billing/docs/deployment.md
   → APPEND: docs/kb/deployment-procedures.md (existing, topic overlap)
   → Tags: [module:billing, deployment] (merging with existing tags)
   → Content type: Actionable knowledge

3. https://wiki.example.com/billing/api
   → NEW: docs/kb/billing-api-integration.md
   → Tags: [module:billing, api, integration, external]
   → When to Load: — module:billing, api, integration
   → Content type: Reference material (user approved)
```

- Header: "KB Harvest — Confirm Plan"
- Question: "Review the ingestion plan above. Proceed?"
- Options: "Proceed with all" | "Let me adjust" | "Cancel"

If "Let me adjust", let the user modify destinations, tags, or skip individual items via free-text follow-up.

### Step 7: Execute Ingestion

For each approved source:

#### 7a: Draft and Approve New KB File

1. **Distill the content** into KB format:
   - Convert prose into concise, actionable rules in imperative voice.
   - Remove filler, redundant context, and content that only matters for human reading.
   - Organize under clear headings (`## Key Rules`, `## Conventions`, `## Gotchas`, etc.).
   - Keep the distilled content focused and scannable.
2. **Add proper frontmatter** with:
   - Confirmed tags (always include `module:{name}` for local sources)
   - Today's date (resolved once via the cross-platform command in the Frontmatter Schema section) for `created` and `last-updated`
   - `source` field set to the original file path or URL
   - `related` cross-references to existing KB files if applicable
   - `pinned` and `scope` as appropriate
3. **Present the complete draft** (frontmatter + body) for user review before writing. Use AskUserQuestion:
   - Header: "KB Harvest — Review: {destination filename}"
   - Question: "Here's the drafted KB article for **{topic}** (`{destination path}`), distilled from `{source path or URL}`. Review the content below and confirm:\n\n```yaml\n{full file content with frontmatter}\n```"
   - Options: "Approve" | "Edit and approve" | "Skip this file"
   - If "Edit and approve", accept free-text corrections, apply them, and show the updated draft for final confirmation.
4. **Only after approval**, write the file to the confirmed `docs/kb/` path.

**Processing order**: Present each file one at a time so the user can focus. If many files were selected, after the first 3, offer a shortcut: "Approve remaining {count} files without individual review?"

#### 7b: Draft and Approve Appending to Existing KB File

1. **Read the existing KB file**.
2. **Distill only new content** that isn't already covered.
3. **Present the diff** (new content being appended) for user review. Use AskUserQuestion:
   - Header: "KB Harvest — Append to: {existing filename}"
   - Question: "The following content will be appended to `{existing file path}`. Review and confirm:\n\n```\n{new content being added}\n```\n\nFrontmatter updates: {list tag/source/date changes}"
   - Options: "Approve" | "Edit and approve" | "Skip"
4. **Only after approval**, append new rules under the appropriate section. Do not duplicate existing entries.
5. **Update frontmatter** (only if content actually changed):
   - Update `last-updated` to the date resolved at the start of the write phase.
   - Merge new tags (preserving existing ones).
   - Add the new source to the `source` field. If `source` already has a value, convert to a list:
     ```yaml
     source:
       - "original/path.md"
       - "C:/Source/billing/docs/new-content.md"
     ```
   - Add new `related` cross-references if applicable.

#### 7c: Update CLAUDE.md Table

1. **Remove placeholder row** if present ("_No entries yet_").
2. **Add or update the row** with the confirmed Topic, File path, and When to Load.
   - For pinned KB files, set "When to Load" to "Always (pinned)".
   - For non-pinned files, format the "When to Load" column using the structured format: `` `scope-glob1`, `scope-glob2` — tag1, tag2 ``. Derive scope patterns from the file's `scope` frontmatter and keywords from `tags`.
3. **Deduplicate**: If a row for the same file already exists, update it rather than adding a duplicate.
4. **Sort the table** alphabetically by Topic.

#### 7d: Cross-References

After all ingestions are complete:
1. Scan newly created KB files for related topics with each other and with existing KB files.
2. Add `related` cross-references in frontmatter where there's clear topical overlap.
3. Add or update the `## Related` body section on any file whose `related` frontmatter was modified (keep them in sync).

### Step 8: Update Index and Log

1. **Update `docs/kb/_index.md`**: If this file exists, add entries for all newly created/updated KB files with one-line summaries. Update `last-updated` in its frontmatter.
2. **Append to `docs/kb/_log.md`**: If this file exists, append:
   ```
   ## [YYYY-MM-DD] harvest | Harvested {count} sources
   - Sources: {list of source paths/URLs}
   - Created: {list of new KB files}
   - Updated: {list of updated KB files}
   ```

### Step 9: Summary

Display a final summary:

```
KB Harvest — Complete
======================

Harvested {count} sources into the knowledge base:

## New KB Files Created ({count})
- docs/kb/billing-api-conventions.md ← C:/Source/billing/docs/api-conventions.md
  Key content: REST naming conventions, pagination rules, error response format
- docs/kb/billing-api-integration.md ← https://wiki.example.com/billing/api
  Key content: Authentication flow, rate limits, webhook setup

## Existing KB Files Updated ({count})
- docs/kb/deployment-procedures.md ← C:/Source/billing/docs/deployment.md
  Added: billing-specific deployment steps, environment variable requirements

## CLAUDE.md Table
- {count} rows added, {count} rows updated

## Provenance
All harvested entries have a `source` field in their frontmatter tracking the
original location. Re-run `/kb-harvest` with the same sources to refresh if
the source documentation is updated.

Source files/URLs were NOT modified or deleted.
```

## Quality Rules

- **Distill, don't copy-paste**: The KB file should be a concise, actionable version of the source. Long documentation should become focused rules. This is the single most important rule.
- **No secrets**: Never store API keys, tokens, passwords, connection strings, or internal hostnames/IPs. Store patterns/rules instead (e.g., "API keys must come from environment variables").
- **No duplication**: Check existing KB files before writing. If content already exists, skip it.
- **Maintain frontmatter**: Every KB file write must include valid, complete frontmatter with the `source` provenance field.
- **Preserve sources**: Never modify or delete source files. Never modify content at URLs. The user decides what to do with originals.
- **Module tagging**: Always add `module:{name}` tag for content harvested from local repos/directories. This enables filtering KB entries by module.
- **URL content safety**: When fetching URLs, do not store any authentication tokens, session data, or cookie values that may appear in the fetched content. Strip these before distilling.
