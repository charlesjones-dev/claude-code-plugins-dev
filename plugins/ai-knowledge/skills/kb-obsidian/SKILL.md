---
name: kb-obsidian
description: "One-time migration to upgrade an existing Knowledge Base. Adds wiki-link body sections for Obsidian graph view, migrates inline global learnings, generates _index.md and _log.md, and offers to reorganize flat files into category folders."
disable-model-invocation: true
---

# Knowledge Base Upgrade & Obsidian Migration

You are a knowledge base migration assistant. Your job is to upgrade an existing `docs/kb/` knowledge base to the latest structure and make it fully Obsidian-compatible. This is a one-time migration — after running this, all other `/kb-*` commands will maintain the upgraded structure automatically.

## What This Migration Does

1. **Related body links** — Obsidian does not parse `[[wiki-links]]` in YAML frontmatter. This adds `## Related` sections to the body of each KB file so graph view and link navigation work.
2. **Global learnings file** — Moves inline `### Global Learnings` from CLAUDE.md to `docs/kb/_global-learnings.md`.
3. **Index generation** — Creates `docs/kb/_index.md` with a categorized catalog of all KB articles.
4. **Activity log** — Creates `docs/kb/_log.md` for chronological operation tracking.
5. **Folder organization** — Offers to reorganize flat KB files into category folders for better navigation.

## Instructions

**CRITICAL**: This command MUST NOT accept any arguments. Ignore any text provided after the command.

### Step 1: Prerequisite Check

1. **Check for KB section in CLAUDE.md**: Read the project's CLAUDE.md and look for the Knowledge Base table. If it doesn't exist, inform the user to run `/kb-init` first and stop.
2. **Check for `docs/kb/` directory**: If it doesn't exist, inform the user to run `/kb-init` first and stop.
3. **Glob for KB files**: Find all `.md` files under `docs/kb/` (excluding `docs/kb/README.md`).
4. If no KB files exist (other than README), inform the user: "No KB files found. Add knowledge first with `/kb-learn`, `/kb-add`, or `/kb-discover`, then run this command." and stop.

### Step 2: Audit Current State

Scan the KB and build an audit report:

#### 2a: Scan KB Files for Related Links

For each `.md` file in `docs/kb/` (excluding README.md):

1. **Read the file** and parse its YAML frontmatter.
2. **Check `related` field**: Does the frontmatter have a `related` field with one or more references?
3. **Check for existing `## Related` section**: Does the file body already have a `## Related` section with `[[wiki-links]]`?
4. Categorize each file:
   - **NEEDS BODY LINKS** — Has `related` in frontmatter but no `## Related` body section (or body section is out of sync with frontmatter).
   - **OK** — Either has no `related` references, or already has a matching `## Related` body section.
   - **BODY LINKS ONLY** — Has a `## Related` body section but no `related` frontmatter (unusual, flag for review).

#### 2b: Check Global Learnings Location

1. **Read CLAUDE.md**: Look for a `### Global Learnings` subsection under `## Knowledge Base`.
2. **Check for `docs/kb/_global-learnings.md`**: Does this file already exist?
3. Categorize:
   - **NEEDS MIGRATION** — Inline global learnings exist in CLAUDE.md but `_global-learnings.md` does not exist (or exists but inline section also still has content).
   - **ALREADY MIGRATED** — `_global-learnings.md` exists and CLAUDE.md has no inline global learnings content.
   - **NO GLOBAL LEARNINGS** — Neither location has content.

#### 2c: Check Frontmatter Health

For each KB file, verify:
1. YAML frontmatter exists.
2. Required fields are present: `tags`, `created`, `last-updated`.
3. Flag files with issues as **NEEDS FRONTMATTER FIX**.

#### 2d: Check Index and Log

1. **Check for `docs/kb/_index.md`**: Does it exist?
   - **NEEDS CREATION** — File doesn't exist.
   - **OK** — File exists.
2. **Check for `docs/kb/_log.md`**: Does it exist?
   - **NEEDS CREATION** — File doesn't exist.
   - **OK** — File exists.
3. **Check CLAUDE.md table**: Is `_index.md` registered as pinned?

#### 2e: Check Folder Organization

1. **Count flat files**: How many KB articles (excluding `_`-prefixed files and README.md) are directly in `docs/kb/` root (not in subfolders)?
2. **Count subfolder files**: How many are in subfolders?
3. If there are **5 or more flat files**, flag as **REORGANIZATION SUGGESTED** — suggest grouping into category folders based on tags and content.
4. For each flat file, propose a category folder based on its tags:
   - Architecture, patterns, system design → `architecture/`
   - Conventions, naming, coding style, API contracts → `conventions/`
   - Tools, workflow, infrastructure, deployment → `tools/`
   - Testing, test patterns → `testing/`
   - External, harvested, module-specific → `external/` or `{module}/`
   - Other → suggest based on the dominant tag
5. If fewer than 5 flat files, skip reorganization (small KBs don't benefit from folders).

### Step 3: Present Migration Report

Display the audit results:

```
KB Obsidian Migration — Audit Report
======================================

## Related Links (Graph View)

### Need body links ({count})
These files have `related` frontmatter but no body `## Related` section:
- {filename}.md — related: [[file1]], [[file2]]
- {filename}.md — related: [[file3]]

### Already compatible ({count})
- {filename}.md — OK

## Global Learnings

Status: {NEEDS MIGRATION | ALREADY MIGRATED | NO GLOBAL LEARNINGS}
{If NEEDS MIGRATION: show count of inline learnings that will be moved}

## Frontmatter Issues ({count})
- {filename}.md — {issue description}

## Index & Log
- _index.md: {OK | NEEDS CREATION}
- _log.md: {OK | NEEDS CREATION}

## Folder Organization
{If REORGANIZATION SUGGESTED:}
{count} files are flat in docs/kb/ root. Suggested reorganization:
- server-tick-architecture.md → architecture/server-tick-architecture.md
- hub-contract-conventions.md → conventions/hub-contract-conventions.md
- testing-strategy.md → testing/testing-strategy.md
- ...

{If not suggested:}
Folder structure is fine ({count} files in subfolders, {count} flat — too few to reorganize).

## Summary
- {count} files need `## Related` body sections added
- {count} global learnings to migrate to _global-learnings.md
- {count} frontmatter issues to fix
- {count} infrastructure files to create (_index.md, _log.md)
- {count} files suggested for folder reorganization
```

If everything is already up to date:
> "Your knowledge base is already fully upgraded! No changes needed."

Otherwise, use AskUserQuestion:
- Header: "KB Upgrade & Obsidian Migration"
- Question: "Ready to upgrade your knowledge base?"
- Options: "Apply all changes" | "Apply all except reorganization" | "Let me review each change" | "Cancel"

### Step 4: Execute Migration

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

4. **Important formatting rules**:
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
   - {... all existing global learnings}
   ```

   If `_global-learnings.md` already exists but inline learnings also exist in CLAUDE.md, merge the inline learnings into the file (deduplicating).

3. **Register in CLAUDE.md table**: Add or verify a row:
   `| Global Learnings | docs/kb/_global-learnings.md | Always (pinned) |`

4. **Remove the inline `### Global Learnings` section** from CLAUDE.md (under `## Knowledge Base`). Remove the entire subsection including the heading and all bullet points. If there's placeholder text ("_No global learnings captured yet..._"), remove that too.

5. **Keep the `<!-- kb-auto: enabled -->` block** if it exists — do not move or remove it. It should remain under the Knowledge Base section, after the table.

#### 4c: Fix Frontmatter Issues

For files with missing or incomplete frontmatter:

1. **Add missing frontmatter** with inferred values (same logic as `/kb-import`).
2. **Add `## Related` body section** if the file has related references (even newly added ones).

#### 4d: Create Index and Log

**If `_index.md` NEEDS CREATION:**

1. **Read all KB files** in `docs/kb/` (including those in subfolders).
2. **For each file**, parse its frontmatter and read the first few content lines after the heading to generate a one-line summary.
3. **Group files by category** — infer categories from tags, folder location, and content:
   - Files in subfolders: use the subfolder name as the category.
   - Flat files: infer from the dominant tag(s).
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

   ## {Another Category}

   - [[more-articles]] — Summary

   ## Meta

   - [[_global-learnings]] — Cross-cutting rules that apply everywhere

   ## All Pages

   | Page | Summary | Tags | Last Updated |
   |------|---------|------|-------------|
   | [[article-name]] | Summary | tag1, tag2 | YYYY-MM-DD |
   ```

5. **Register in CLAUDE.md table**: Add `| KB Index | docs/kb/_index.md | Always (pinned) |`

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

## [{today's date}] obsidian | KB upgraded for Obsidian compatibility
- Added ## Related body sections to {count} files
- {Migrated global learnings to _global-learnings.md | Global learnings already migrated}
- Generated _index.md with {count} articles cataloged
- Created _log.md
- {Reorganized {count} files into category folders | No reorganization needed}
```

#### 4e: Folder Reorganization

**Only execute if the user approved reorganization** (not if they chose "Apply all except reorganization").

For each file to be reorganized:

1. **Create the target subfolder** if it doesn't exist (e.g., `docs/kb/architecture/`).
2. **Move the file** from `docs/kb/{file}.md` to `docs/kb/{category}/{file}.md`.
3. **Update CLAUDE.md table**: Change the File column from `docs/kb/{file}.md` to `docs/kb/{category}/{file}.md`.
4. **Update cross-references**: In all other KB files that reference this file via `related` frontmatter or `## Related` body links, the `[[wiki-link]]` does NOT need to change (Obsidian resolves `[[filename]]` regardless of folder). However, the CLAUDE.md table paths must be updated.
5. **Update `_index.md`**: File paths in the "All Pages" table should reflect the new locations.
6. **DO NOT modify `[[wiki-links]]`** in frontmatter or body sections — Obsidian resolves `[[filename]]` by name, not path. Only update the CLAUDE.md table paths.

### Step 5: Verify

After all changes:

1. **Re-read all modified files** and verify:
   - Every file with `related` frontmatter has a matching `## Related` body section.
   - `_global-learnings.md` exists and is registered in the CLAUDE.md table (if global learnings existed).
   - No inline `### Global Learnings` section remains in CLAUDE.md.
   - `_index.md` exists, is registered as pinned, and catalogs all KB articles.
   - `_log.md` exists with the migration entry.
   - All frontmatter is valid and complete.
   - If reorganization was done, CLAUDE.md table paths reflect new locations.

2. **Present completion summary**:

```
KB Upgrade & Obsidian Migration — Complete
============================================

## Changes Made

### Related Links Added ({count} files)
- {filename}.md — added links to [[file1]], [[file2]]

### Global Learnings Migrated
- Moved {count} learnings from CLAUDE.md to docs/kb/_global-learnings.md
- Registered _global-learnings.md as pinned in CLAUDE.md table

### Index & Log Created
- Generated _index.md with {count} articles across {count} categories
- Created _log.md with migration entry
- Registered _index.md as pinned in CLAUDE.md table

### Folder Reorganization ({count} files moved)
- {filename}.md → {category}/{filename}.md
- Updated CLAUDE.md table paths

### Frontmatter Fixed ({count} files)
- {filename}.md — added missing {fields}

## Next Steps

Your knowledge base is fully upgraded!

1. **Open in Obsidian**: Open `docs/kb/` as an Obsidian vault (or point an
   existing vault at it). Obsidian will create its `.obsidian/` config folder.

2. **Graph View**: Press Ctrl/Cmd+G in Obsidian to see your knowledge graph.
   All `[[wiki-links]]` in the Related sections will appear as edges.

3. **Query the KB**: Use `/kb-query <question>` to ask questions against
   the knowledge base. Good answers can be filed back as new articles.

4. **Ongoing compatibility**: All `/kb-*` commands now automatically maintain
   the upgraded structure. No further migration is needed.

5. **Git**: Consider adding `.obsidian/` to your `.gitignore` if you don't
   want to share Obsidian config with your team. The KB markdown files
   themselves should remain in source control.
```
