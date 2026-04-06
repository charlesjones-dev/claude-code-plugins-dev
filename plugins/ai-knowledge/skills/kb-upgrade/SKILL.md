---
name: kb-upgrade
description: "Upgrade an existing Knowledge Base to the latest plugin practices. Ensures Obsidian compatibility, structured 'When to Load' format, loading notifications, index schema, and frontmatter health. Safe and re-runnable."
disable-model-invocation: true
---

# Knowledge Base Upgrade

You are a knowledge base upgrade assistant. Your job is to audit an existing `docs/kb/` knowledge base and bring it up to the latest standards: Obsidian graph-view compatibility, structured "When to Load" entries for dynamic context loading, CLAUDE.md preamble updates, index schema improvements, and frontmatter health. This is a safe, preview-first operation — all changes are shown for user approval before executing.

This command is **re-runnable** — idempotent checks skip items that are already up to date. Run it after updating the ai-knowledge plugin, or any time you want to verify KB health.

## What This Upgrade Covers

1. **Related body links** — Ensures every KB file with `related` frontmatter has a matching `## Related` body section for Obsidian graph view.
2. **Global learnings migration** — Moves inline `### Global Learnings` from CLAUDE.md to `docs/kb/_global-learnings.md` if not already done.
3. **Index & log creation** — Creates `docs/kb/_index.md` and `docs/kb/_log.md` if missing.
4. **"When to Load" standardization** — Rewrites CLAUDE.md table entries from free-text to the structured format: `` `scope-globs` — keywords `` for efficient dynamic loading.
5. **CLAUDE.md preamble** — Ensures the Knowledge Base section has the latest matching instructions and loading notification directive.
6. **`_index.md` schema** — Adds a `Scope` column to the All Pages table for routing context.
7. **Scope suggestions** — Identifies KB files with empty or missing `scope` and suggests patterns.
8. **Frontmatter completeness** — Ensures all required fields are present and valid.
9. **Folder organization** — Offers to reorganize flat KB files into category folders if the KB has grown large enough.

## Instructions

**CRITICAL**: This command MUST NOT accept any arguments. Ignore any text provided after the command.

### Step 1: Prerequisite Check

1. **Check for KB section in CLAUDE.md**: Read the project's CLAUDE.md and look for the Knowledge Base table. If it doesn't exist, inform the user to run `/kb-init` first and stop.
2. **Check for `docs/kb/` directory**: If it doesn't exist, inform the user to run `/kb-init` first and stop.
3. **Glob for KB files**: Find all `.md` files under `docs/kb/` (excluding `docs/kb/README.md`).
4. If no KB files exist (other than README), inform the user: "No KB files found. Add knowledge first with `/kb-learn`, `/kb-add`, or `/kb-discover`, then run this command." and stop.

### Step 2: Audit Current State

Scan the KB and build a comprehensive audit report. All checks are **read-only** — nothing is modified in this step.

#### 2a: Related Links (Obsidian Graph View)

For each `.md` file in `docs/kb/` (excluding README.md):

1. **Read the file** and parse its YAML frontmatter.
2. **Check `related` field**: Does the frontmatter have a `related` field with one or more references?
3. **Check for existing `## Related` section**: Does the file body already have a `## Related` section with `[[wiki-links]]`?
4. Categorize each file:
   - **NEEDS BODY LINKS** — Has `related` in frontmatter but no `## Related` body section (or body section is out of sync with frontmatter).
   - **OK** — Either has no `related` references, or already has a matching `## Related` body section.
   - **BODY LINKS ONLY** — Has a `## Related` body section but no `related` frontmatter (unusual, flag for review).

#### 2b: Global Learnings Location

1. **Read CLAUDE.md**: Look for a `### Global Learnings` subsection under `## Knowledge Base`.
2. **Check for `docs/kb/_global-learnings.md`**: Does this file already exist?
3. Categorize:
   - **NEEDS MIGRATION** — Inline global learnings exist in CLAUDE.md but `_global-learnings.md` does not exist (or exists but inline section also still has content).
   - **ALREADY MIGRATED** — `_global-learnings.md` exists and CLAUDE.md has no inline global learnings content.
   - **NO GLOBAL LEARNINGS** — Neither location has content.

#### 2c: Frontmatter Completeness

For each KB file, verify:
1. YAML frontmatter exists.
2. Required fields are present: `tags`, `created`, `last-updated`.
3. **Check `scope` field**: Is it present? Is it empty (`""` or `[]`)? Could a meaningful scope be inferred from the file's content, tags, or path?
4. Flag files with issues as **NEEDS FRONTMATTER FIX**.
5. Flag files with empty/missing scope where scope could be inferred as **SCOPE SUGGESTED**.

#### 2d: Index & Log

1. **Check for `docs/kb/_index.md`**: Does it exist?
   - If it exists, check whether its "All Pages" table has a **Scope** column.
   - **NEEDS CREATION** — File doesn't exist.
   - **NEEDS SCOPE COLUMN** — File exists but All Pages table lacks Scope column.
   - **OK** — File exists with Scope column.
2. **Check for `docs/kb/_log.md`**: Does it exist?
   - **NEEDS CREATION** — File doesn't exist.
   - **OK** — File exists.
3. **Check CLAUDE.md table**: Is `_index.md` registered as pinned?

#### 2e: "When to Load" Format

1. **Read the CLAUDE.md Knowledge Base table**.
2. For each non-pinned entry, check if the "When to Load" value follows the structured format:
   - **Structured format**: Contains backtick-wrapped glob patterns (e.g., `` `src/api/**` ``) and/or keywords after an em dash (`—`).
   - **Free-text format**: Natural language like "When working in packages/api/" or "When modifying database schemas".
3. Categorize entries:
   - **NEEDS FORMAT UPDATE** — Uses free-text instead of structured format.
   - **OK** — Already uses the structured format or is `Always (pinned)`.
4. For entries that NEED FORMAT UPDATE, read the corresponding KB file's frontmatter to get `scope` and `tags`, and draft the new structured value:
   - If `scope` is a string, treat as a single-element array.
   - If `scope` is an array, use all elements.
   - Format: `` `scope-glob1`, `scope-glob2` — tag1, tag2 ``
   - If no scope: `— tag1, tag2`
   - If no tags: `` `scope-glob1` ``

#### 2f: CLAUDE.md Preamble

Check the Knowledge Base section's introductory text:
1. Does it contain the **4-point matching instructions** (pinned entries, scope patterns, keywords, _index.md fallback)?
2. Does it contain the **loading notification instruction** (telling Claude to notify the user when loading a KB file)?
3. Categorize:
   - **NEEDS UPDATE** — Missing matching instructions or loading notification.
   - **OK** — Has both.

#### 2g: Folder Organization

1. **Count flat files**: How many KB articles (excluding `_`-prefixed files and README.md) are directly in `docs/kb/` root?
2. **Count subfolder files**: How many are in subfolders?
3. If there are **5 or more flat files**, flag as **REORGANIZATION SUGGESTED**.
4. For each flat file, propose a category folder based on its tags:
   - Architecture, patterns, system design → `architecture/`
   - Conventions, naming, coding style, API contracts → `conventions/`
   - Tools, workflow, infrastructure, deployment → `tools/`
   - Testing, test patterns → `testing/`
   - External, harvested, module-specific → `external/`
   - Other → suggest based on the dominant tag
5. If fewer than 5 flat files, skip reorganization.

### Step 3: Present Upgrade Report

Display the audit results:

```
KB Upgrade — Audit Report
==========================

## Related Links (Obsidian Graph View)

### Need body links ({count})
- {filename}.md — related: [[file1]], [[file2]]

### Already compatible ({count})
- {filename}.md — OK

## Global Learnings
Status: {NEEDS MIGRATION | ALREADY MIGRATED | NO GLOBAL LEARNINGS}

## Frontmatter Issues ({count})
- {filename}.md — {issue description}

## Scope Suggestions ({count})
- {filename}.md — suggested: `{inferred scope pattern}`

## Index & Log
- _index.md: {OK | NEEDS CREATION | NEEDS SCOPE COLUMN}
- _log.md: {OK | NEEDS CREATION}

## "When to Load" Format ({count} need update)
{If entries need update:}
- {Topic}: "{old value}" → `{new structured value}`

{If none need update:}
All entries already use the structured format.

## CLAUDE.md Preamble
Status: {NEEDS UPDATE | OK}

## Folder Organization
{If REORGANIZATION SUGGESTED:}
{count} files are flat in docs/kb/ root. Suggested reorganization:
- {filename}.md → {category}/{filename}.md

{If not suggested:}
Folder structure is fine.

## Summary
- {count} files need `## Related` body sections
- {count} global learnings to migrate
- {count} frontmatter issues to fix
- {count} scope suggestions
- {count} infrastructure files to create/update
- {count} "When to Load" entries to standardize
- CLAUDE.md preamble: {needs update | OK}
- {count} files suggested for folder reorganization
```

If everything is already up to date:
> "Your knowledge base is fully up to date! No changes needed."

Otherwise, use AskUserQuestion:
- Header: "KB Upgrade"
- Question: "Ready to upgrade your knowledge base?"
- Options: "Apply all" | "Apply all except reorganization" | "Let me review each change" | "Cancel"

### Step 4: Execute Upgrades

#### 4a: Add `## Related` Body Sections

For each file that NEEDS BODY LINKS:

1. **Read the file** fully.
2. **Parse the `related` frontmatter** to extract the list of referenced KB file names (without `.md` extension).
3. **Add a `## Related` section at the very end of the file**:

   ```markdown

   ## Related

   - [[referenced-file-1]]
   - [[referenced-file-2]]
   ```

4. **Formatting rules**:
   - Add one blank line before `## Related`.
   - Each reference is a bullet point with a `[[wiki-link]]` using the filename without `.md` extension.
   - The `## Related` section must be the **last section** in the file.
   - Do NOT remove or modify the `related` frontmatter — it is still used by Claude Code's loading logic.
   - If the file already has a `## Related` section that is out of sync with frontmatter, replace its content with the correct links.

5. **Update `last-updated`** in frontmatter to today's date.

#### 4b: Migrate Global Learnings

If global learnings NEED MIGRATION:

1. **Read the `### Global Learnings` section** from CLAUDE.md. Extract all bullet points.

2. **Create `docs/kb/_global-learnings.md`** (or update if it exists):

   ```markdown
   ---
   tags: [global, cross-cutting]
   related: []
   created: {today's date}
   last-updated: {today's date}
   pinned: true
   ---

   # Global Learnings

   Cross-cutting rules and insights that apply across the entire project.

   ## Key Rules

   - {migrated learning 1}
   - {migrated learning 2}
   ```

   If `_global-learnings.md` already exists but inline learnings also exist in CLAUDE.md, merge the inline learnings into the file (deduplicating).

3. **Register in CLAUDE.md table**: Add or verify a row:
   `| Global Learnings | docs/kb/_global-learnings.md | Always (pinned) |`

4. **Remove the inline `### Global Learnings` section** from CLAUDE.md (under `## Knowledge Base`). Remove the entire subsection including the heading and all bullet points. If there's placeholder text ("_No global learnings captured yet..._"), remove that too.

5. **Keep the `<!-- kb-auto: enabled -->` block** if it exists — do not move or remove it.

#### 4c: Fix Frontmatter Issues

For files with missing or incomplete frontmatter:

1. **Add missing frontmatter** with inferred values:
   - Infer `tags` from file content and path.
   - Set `created` and `last-updated` to today's date.
   - Set `pinned` to `false`.
   - Leave `related` empty initially.

2. **Add `## Related` body section** if the file has related references (even newly added ones).

For files flagged as **SCOPE SUGGESTED**:

3. **Present each suggestion** to the user via AskUserQuestion:
   - Header: "Scope Suggestion: {filename}"
   - Question: "This KB file has no `scope` patterns. Based on its content and tags, I suggest: `{inferred scope patterns}`. Accept?"
   - Options: "Accept" | "Different scope" (free-text) | "Skip"

4. **Update the file's frontmatter** with the accepted scope value. The `scope` field can be a string (single pattern) or array (multiple patterns).

#### 4d: Create/Update Index and Log

**If `_index.md` NEEDS CREATION:**

1. **Read all KB files** in `docs/kb/` (including those in subfolders).
2. **For each file**, parse its frontmatter and read the first few content lines to generate a one-line summary.
3. **Group files by category** — infer categories from tags, folder location, and content.
4. **Generate `docs/kb/_index.md`**:

   ```markdown
   ---
   tags: [index, meta]
   created: {today's date}
   last-updated: {today's date}
   pinned: true
   ---

   # Knowledge Base Index

   Auto-generated catalog of all KB articles. Updated by `/kb-*` commands. Read this file first to find relevant pages before drilling into individual articles.

   ## {Category Name}

   - [[article-name]] — One-line summary of what this article covers
   - [[another-article]] — Another summary

   ## Meta

   - [[_global-learnings]] — Cross-cutting rules that apply everywhere

   ## All Pages

   | Page | Summary | Tags | Scope | Last Updated |
   |------|---------|------|-------|-------------|
   | [[article-name]] | Summary | tag1, tag2 | `src/api/**` | YYYY-MM-DD |
   ```

5. **Register in CLAUDE.md table**: Add `| KB Index | docs/kb/_index.md | Always (pinned) |`

**If `_index.md` NEEDS SCOPE COLUMN:**

1. Read the existing `_index.md`.
2. Find the "All Pages" table.
3. Add a `Scope` column header between `Tags` and `Last Updated`.
4. For each row, read the corresponding KB file's `scope` frontmatter and populate the Scope cell.
   - If scope is a string, wrap in backticks: `` `src/api/**` ``
   - If scope is an array, join with commas: `` `src/api/**`, `*.ts` ``
   - If scope is empty/missing, leave the cell empty.
   - If the file is pinned, put `_(pinned)_`.
5. Update `last-updated` in frontmatter.

**If `_log.md` NEEDS CREATION:**

Create `docs/kb/_log.md`:

```markdown
---
tags: [log, meta]
created: {today's date}
last-updated: {today's date}
---

# Knowledge Base Log

Chronological record of KB operations. Append-only — newest entries at the bottom.

## [{today's date}] upgrade | KB upgraded to latest practices
- Added ## Related body sections to {count} files
- {Migrated global learnings to _global-learnings.md | Global learnings already migrated}
- {Generated _index.md with {count} articles cataloged | Updated _index.md with Scope column}
- Created _log.md
- Standardized {count} "When to Load" entries
- Updated CLAUDE.md preamble
- {Reorganized {count} files into category folders | No reorganization needed}
```

#### 4e: Standardize "When to Load" Column

For each table entry flagged as NEEDS FORMAT UPDATE:

1. **Read the KB file's frontmatter** to get `scope` (handle string or array) and `tags`.
2. **Build the new "When to Load" value**:
   - If `pinned: true`: `Always (pinned)` (should already be correct).
   - If `scope` has values: format as backtick-wrapped globs, comma-separated.
   - If `tags` has values: append as keywords after em dash (`—`).
   - Full format: `` `scope-glob1`, `scope-glob2` — tag1, tag2 ``
   - No scope, has tags: `— tag1, tag2`
   - Has scope, no tags: `` `scope-glob1`, `scope-glob2` ``
3. **If the KB file has no `scope` and no `tags`**: Attempt to infer from the file content and old "When to Load" text. Extract directory references from the old text (e.g., "When working in packages/api/" → `packages/api/**`). Flag these for the user to review if the inference is uncertain.
4. **Update the CLAUDE.md table row** with the new "When to Load" value.

#### 4f: Update CLAUDE.md Preamble

Replace the Knowledge Base section's introductory text (between the `## Knowledge Base` heading and the table) with the latest version:

```markdown
Topic-specific knowledge is stored in `docs/kb/` and loaded contextually based on the table below.

**How to use the "When to Load" column:**
1. **Pinned entries** (`Always (pinned)`): Load at the start of every conversation.
2. **Scope patterns** (backtick-wrapped globs like `src/api/**`): Load when the files you are editing or creating match any of the listed glob patterns.
3. **Keywords** (after the `—` dash): Load when the current task involves these topics, even if no file path matches.
4. **When uncertain**: Read `docs/kb/_index.md` (pinned) for article summaries and scope patterns to help decide.

**Loading notifications**: When you load a KB file, briefly notify the user so they know what context is being applied. Example: `📖 Loading KB: api-conventions.md`. Keep notifications to a single line per file.

When a KB file's frontmatter contains `related: [[other-file]]` cross-references, also read the related file(s) for full context.
```

**Important**: Preserve the `<!-- kb-auto: enabled -->` block and any other content after the table. Only replace the introductory paragraph(s) before the table.

#### 4g: Folder Reorganization

**Only execute if the user approved reorganization** (not if they chose "Apply all except reorganization").

For each file to be reorganized:

1. **Create the target subfolder** if it doesn't exist (e.g., `docs/kb/architecture/`).
2. **Move the file** from `docs/kb/{file}.md` to `docs/kb/{category}/{file}.md`.
3. **Update CLAUDE.md table**: Change the File column from `docs/kb/{file}.md` to `docs/kb/{category}/{file}.md`.
4. **Refresh the "When to Load" column**: Read the moved file's `scope` and `tags` frontmatter and regenerate the structured "When to Load" value.
5. **Update `_index.md`**: File paths in the "All Pages" table should reflect the new locations.
6. **DO NOT modify `[[wiki-links]]`** in frontmatter or body sections — Obsidian resolves `[[filename]]` by name, not path. Only update the CLAUDE.md table paths.
7. **Update `last-updated`** in frontmatter of moved files.

### Step 5: Verify

After all changes:

1. **Re-read all modified files** and verify:
   - Every file with `related` frontmatter has a matching `## Related` body section.
   - `_global-learnings.md` exists and is registered in the CLAUDE.md table (if global learnings existed).
   - No inline `### Global Learnings` section remains in CLAUDE.md.
   - `_index.md` exists, is registered as pinned, has Scope column, and catalogs all KB articles.
   - `_log.md` exists with the upgrade entry.
   - All frontmatter is valid and complete.
   - All non-pinned CLAUDE.md table entries use the structured "When to Load" format.
   - CLAUDE.md preamble has the 4-point matching instructions and loading notification directive.
   - If reorganization was done, CLAUDE.md table paths reflect new locations.

### Step 6: Update Log

Append to `docs/kb/_log.md`:

```markdown
## [{today's date}] upgrade | KB upgraded to latest practices
- Related links: added to {count} files
- Global learnings: {migrated | already migrated | none}
- Index: {created | updated Scope column | already up to date}
- Log: {created | already existed}
- "When to Load": standardized {count} entries
- Preamble: {updated | already up to date}
- Frontmatter: fixed {count} files
- Scope: suggested for {count} files
- Reorganization: {moved {count} files | not needed | skipped by user}
```

### Step 7: Summary

```
KB Upgrade — Complete
======================

## Changes Made

### Related Links Added ({count} files)
- {filename}.md — added links to [[file1]], [[file2]]

### Global Learnings
- {Moved {count} learnings from CLAUDE.md to docs/kb/_global-learnings.md | Already migrated | No global learnings}

### Index & Log
- {Generated _index.md with {count} articles across {count} categories | Updated _index.md with Scope column | Already up to date}
- {Created _log.md | Already existed}

### "When to Load" Standardized ({count} entries)
- {Topic}: "{old}" → {new structured format}

### CLAUDE.md Preamble
- {Updated with matching instructions and loading notifications | Already up to date}

### Frontmatter Fixed ({count} files)
- {filename}.md — added missing {fields}

### Scope Suggestions Applied ({count} files)
- {filename}.md — scope set to {patterns}

### Folder Reorganization ({count} files moved)
- {filename}.md → {category}/{filename}.md
- Updated CLAUDE.md table paths and "When to Load" values

## Obsidian Setup

If you haven't already, you can open `docs/kb/` as an Obsidian vault:

1. Open Obsidian → "Open folder as vault" → select `docs/kb/`
2. Press Ctrl/Cmd+G to see your knowledge graph
3. All `[[wiki-links]]` in Related sections appear as graph edges
4. Consider adding `.obsidian/` to `.gitignore`

## Next Steps

- All `/kb-*` commands now maintain the upgraded structure automatically
- Run `/kb-upgrade` again any time to verify KB health
- Use `/kb-discover` to mine source code for implicit knowledge
- Use `/kb-prune` periodically to consolidate and clean up
```
