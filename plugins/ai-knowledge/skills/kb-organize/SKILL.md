---
name: kb-organize
description: "Reorganize flat KB files into category folders based on tags and content. Updates CLAUDE.md paths and _index.md. Safe — previews all moves before executing."
disable-model-invocation: true
---

# Knowledge Base Organize

You are a knowledge base organization assistant. Your job is to reorganize KB files from a flat structure into category folders for better navigation and scalability. This is a safe, preview-first operation — no files are moved without user approval.

## Date Resolution

**Resolving today's date (cross-platform, CRITICAL)**: Never guess, infer, or increment prior dates. When this skill writes `last-updated`, resolve today's date **once** at the start of the write phase, then reuse that single value for every write. Try these commands in order and use the first that returns a `YYYY-MM-DD` string:

- **macOS / Linux / WSL / Git Bash** (bash, zsh, sh): `date +%Y-%m-%d`
- **Windows PowerShell / pwsh**: `Get-Date -Format 'yyyy-MM-dd'`
- **Windows cmd.exe**: `powershell -NoProfile -Command "Get-Date -Format 'yyyy-MM-dd'"`
- **Portable fallback** (Node or Python available): `node -e "console.log(new Date().toISOString().slice(0,10))"` or `python -c "import datetime; print(datetime.date.today().isoformat())"`

A moved file's `last-updated` should only be bumped if its path changed AND its frontmatter was actually rewritten (path changes alone do not bump `last-updated` unless frontmatter was edited). Never bump dates on untouched files.

## Instructions

**CRITICAL**: This command MUST NOT accept any arguments. Ignore any text provided after the command.

### Step 1: Prerequisite Check

1. **Check for `docs/kb/` directory**: If it doesn't exist, inform the user to run `/kb-init` first and stop.
2. **Check for KB section in CLAUDE.md**: Read the project's CLAUDE.md and look for the Knowledge Base table. If it doesn't exist, inform the user to run `/kb-init` first and stop.

### Step 2: Analyze Current Structure

1. **Glob for all `.md` files** under `docs/kb/` recursively.
2. **Categorize files** by location:
   - **Flat files**: `.md` files directly in `docs/kb/` root (excluding `_`-prefixed files like `_global-learnings.md`, `_index.md`, `_log.md`, and `README.md`).
   - **Already organized**: `.md` files in subfolders (e.g., `docs/kb/architecture/server-tick.md`).
   - **Special files**: `_`-prefixed files and `README.md` — these stay at the root and are never moved.

3. **If no flat files exist**: Inform the user: "All KB files are already organized in subfolders. Nothing to reorganize." and stop.
4. **If fewer than 3 flat files**: Inform the user: "Only {count} flat file(s) found — too few to benefit from folder organization. Run this again when the KB grows." and stop.

### Step 3: Propose Folder Organization

For each flat file:

1. **Read the file** and parse its YAML frontmatter (tags, scope, content).
2. **Suggest a category folder** based on tags and content. Common categories:

   | Category | Folder | When to use |
   |----------|--------|-------------|
   | Architecture & Design | `architecture/` | System design, patterns, data flow, module boundaries |
   | Conventions & Style | `conventions/` | Naming, coding style, API contracts, DTO rules |
   | Testing | `testing/` | Test patterns, fixtures, mocking, coverage |
   | Tools & Workflow | `tools/` | Build tools, deployment, CI/CD, dev environment |
   | External & Harvested | `external/` | Knowledge harvested from other repos or URLs |
   | Domain & Business | `domain/` | Domain-specific rules, business logic patterns |

   These are suggestions — create different categories if the content warrants it. Match existing subfolder names if some organization already exists.

3. **If existing subfolders exist**, prefer placing files in those folders when the content fits. Don't create new categories that duplicate existing ones.

### Step 4: Present Reorganization Plan

Display the proposed moves:

```
KB Organize — Proposed Changes
=================================

## Files to Move ({count})

| Current Location | New Location | Reason |
|-----------------|-------------|--------|
| docs/kb/server-tick-architecture.md | docs/kb/architecture/server-tick-architecture.md | Tags: gameserver, tick-loop |
| docs/kb/hub-contract-conventions.md | docs/kb/conventions/hub-contract-conventions.md | Tags: contracts, signalr |
| docs/kb/testing-strategy.md | docs/kb/testing/testing-strategy.md | Tags: testing, jest |
| docs/kb/editor-toolkit.md | docs/kb/tools/editor-toolkit.md | Tags: editor, tooling |

## New Folders to Create
- docs/kb/architecture/
- docs/kb/conventions/
- docs/kb/testing/
- docs/kb/tools/

## Staying in Place ({count})
- docs/kb/_global-learnings.md (special file)
- docs/kb/_index.md (special file)
- docs/kb/_log.md (special file)
- docs/kb/README.md (special file)
- docs/kb/architecture/existing-file.md (already organized)
```

Use AskUserQuestion:
- Header: "KB Organize"
- Question: "Here's the proposed reorganization. Proceed?"
- Options: "Apply all" | "Let me adjust" | "Cancel"

If "Let me adjust", let the user change individual file destinations via free-text. Re-display the updated plan and confirm again.

### Step 5: Execute Reorganization

For each approved move:

1. **Create the target subfolder** if it doesn't exist.
2. **Move the file** from `docs/kb/{file}.md` to `docs/kb/{category}/{file}.md`.
3. **Update CLAUDE.md table**: Change the File column path from `docs/kb/{file}.md` to `docs/kb/{category}/{file}.md`.
4. **Refresh the "When to Load" column**: After updating the file path, also regenerate the "When to Load" value from the file's current frontmatter:
   - Read the file's `scope` field (handle both string and array forms) to get glob patterns.
   - Read the file's `tags` field to get keywords.
   - If `pinned: true`, set to `Always (pinned)`.
   - Otherwise, format as: `` `scope-glob1`, `scope-glob2` — tag1, tag2 ``.
   - This ensures the table uses the structured format after reorganization.
5. **DO NOT modify `[[wiki-links]]`** in frontmatter `related` fields or `## Related` body sections — Obsidian and KB commands resolve `[[filename]]` by name, not by path. Only the CLAUDE.md table paths and "When to Load" column need updating.
6. **Update `last-updated`** in frontmatter of moved files to the date resolved at the start of the write phase (moves count as a meaningful change; files not moved must not have their dates touched).

### Step 6: Update Index and Log

1. **Update `docs/kb/_index.md`**: If this file exists, update all file paths in the "All Pages" table. Reorganize the category sections to match the new folder structure. Update `last-updated`.
2. **Append to `docs/kb/_log.md`**: If this file exists, append:
   ```
   ## [YYYY-MM-DD] organize | Reorganized KB into folders
   - Moved {count} files into category folders
   - New folders: {list}
   - Files moved: {list of old → new paths}
   ```

### Step 7: Confirm

Display:
- Number of files moved
- New folders created
- CLAUDE.md table entries updated
- Reminder: `[[wiki-links]]` in cross-references were not changed (they resolve by name, not path)
