---
name: kb-ingest
description: "Ingest specific markdown files into the Knowledge Base. Distills content into KB format, creates KB files with frontmatter, and registers them in CLAUDE.md."
disable-model-invocation: true
---

# Knowledge Base Ingest

You are a knowledge base ingestion assistant. Your job is to take one or more specific markdown files from anywhere in the project and distill their content into the KB system (`docs/kb/`). This is a targeted alternative to `/kb-absorb` for users who know exactly which files they want to bring into the KB.

## Frontmatter Schema

Every KB file MUST have valid YAML frontmatter:

```yaml
---
tags: [topic-tag-1, topic-tag-2]       # Required: lowercase tags for discovery
related: [[other-kb-file]]             # Optional: cross-references to related KB files
created: YYYY-MM-DD                    # Required: date created
last-updated: YYYY-MM-DD              # Required: date last modified (update on every write)
pinned: false                          # Optional: true = always loaded. Default false
scope: "src/api/**"                    # Optional: glob pattern(s) for auto-matching. String or array.
---
```

## Obsidian-Compatible Related Links

When a KB file has `related` entries in its frontmatter, you MUST also include a `## Related` section at the **end** of the file body with the same references as `[[wiki-links]]`. This enables Obsidian graph view and link navigation. Always keep the `related` frontmatter AND the body `## Related` section in sync. If there are no related files, omit the section entirely.

## Instructions

### Step 1: Determine Input Files

Check if the user provided file path(s) after the command (e.g., `/kb-ingest docs/api-guide.md` or `/kb-ingest docs/api-guide.md docs/auth-notes.md`).

- **If path(s) provided**: Verify each file exists and is a markdown file (`.md`). If any file doesn't exist, inform the user and skip that file.
- **If no path provided**: Ask the user which file(s) they want to ingest using AskUserQuestion with a free-text input. Header: "KB Ingest".

**Validation**:
- Files must be markdown (`.md`).
- Files already inside `docs/kb/` should be registered with `/kb-import` instead. Inform the user and stop for those files.
- If no valid files remain after validation, stop.

### Step 2: Prerequisite Check

1. **Check for KB section in CLAUDE.md**: Read the project's CLAUDE.md and look for the Knowledge Base table. If it doesn't exist, inform the user to run `/kb-init` first and stop.
2. **Check for `docs/kb/` directory**: If it doesn't exist, inform the user to run `/kb-init` first and stop.

### Step 3: Analyze Each File

For each input file:

1. **Read the file** and analyze its content.
2. **Classify the content**:
   - **Actionable knowledge**: Rules, conventions, patterns, constraints, decisions, gotchas that would change how Claude Code works in the project. This is what belongs in the KB.
   - **Reference material**: Human-facing documentation (tutorials, onboarding, API references) that doesn't contain actionable rules. Flag this for the user but still allow ingestion if they want it.
   - **Not suitable**: Binary files, auto-generated content, changelogs, or files with no extractable knowledge. Inform the user and skip.

3. **Propose a KB destination**: Suggest a file path under `docs/kb/` using subfolder organization based on the content topic (e.g., `docs/kb/conventions/api-conventions.md`, `docs/kb/architecture/auth-flow.md`). Use existing folder structure as a guide.

4. **Check for overlap**: Read the CLAUDE.md Knowledge Base table and check if an existing KB file covers the same topic. If so, propose appending to the existing file instead of creating a new one.

### Step 4: Present Plan

For each file, present the ingestion plan. Use AskUserQuestion:

- Header: "Ingest: {source filename}"
- Question: Show the following and ask for confirmation:
  - Source file path
  - Whether content is actionable knowledge or reference material
  - Destination KB file path (new file or append to existing)
  - Suggested topic name for the CLAUDE.md table
  - Suggested "When to Load" value (structured format: `` `scope-globs` — keywords ``)
  - Suggested tags
  - Whether it should be pinned
- Options: "Looks good" | "Let me adjust" | "Skip this file"

If "Let me adjust", ask a free-text follow-up for corrections.

### Step 5: Execute Ingestion

For each approved file:

#### 5a: Creating a New KB File

1. **Distill the content** into KB format:
   - Convert prose into concise, actionable rules in imperative voice.
   - Remove filler, redundant context, and content that only matters for human reading.
   - Organize under clear headings (`## Key Rules`, `## Context`, etc.).
   - Keep the distilled content focused. A KB file should be quick to scan.
2. **Add proper frontmatter** with the confirmed tags, scope, pinned status, today's date for `created` and `last-updated`, and any `related` cross-references to existing KB files.
3. **Write the file** to the confirmed `docs/kb/` path.

#### 5b: Appending to an Existing KB File

1. **Read the existing KB file**.
2. **Distill only new content** that isn't already covered.
3. **Append** new rules under the appropriate section. Do not duplicate existing entries.
4. **Update `last-updated`** in frontmatter to today's date.
5. **Add new tags** to frontmatter if the ingested content introduces new topics.

#### 5c: Update CLAUDE.md Table

1. **Remove placeholder row** if present ("_No entries yet_").
2. **Add or update the row** with the confirmed Topic, File path, and When to Load.
   - For pinned KB files, set "When to Load" to "Always (pinned)".
   - For non-pinned files, format the "When to Load" column using the structured format: `` `scope-glob1`, `scope-glob2` — tag1, tag2 ``. Derive scope patterns from the file's `scope` frontmatter and keywords from `tags`.
3. **Deduplicate**: If a row for the same file already exists, update it rather than adding a duplicate.
4. **Sort the table** alphabetically by Topic.

### Step 6: Update Index and Log

1. **Update `docs/kb/_index.md`**: If this file exists, add or update entries for ingested files with one-line summaries. Update `last-updated` in its frontmatter.
2. **Append to `docs/kb/_log.md`**: If this file exists, append:
   ```
   ## [YYYY-MM-DD] ingest | Ingested {count} files
   - Sources: {list of source files}
   - Created: {list of new KB files}
   - Updated: {list of updated KB files}
   ```

### Step 7: Confirm

Display a summary for each ingested file:
- Source file and destination KB file
- Whether a new KB file was created or an existing one was updated
- Key content that was captured (brief bullet points)
- CLAUDE.md table entry added/updated
- Reminder: the source file was NOT deleted or modified (the user can remove it manually if desired)

## Quality Rules

- **Distill, don't copy-paste**: The KB file should be a concise, actionable version of the source. Long documentation should become focused rules.
- **No secrets**: Never store API keys, tokens, passwords, or connection strings. Store patterns/rules instead (e.g., "API keys must come from environment variables").
- **No duplication**: Check existing KB files before writing. If content already exists, skip it.
- **Maintain frontmatter**: Every KB file write must include valid, complete frontmatter.
- **Preserve source**: Never modify or delete the source file. The user decides what to do with it.
