---
name: kb-init
description: "Initialize the Knowledge Base section in CLAUDE.md and create the docs/kb/ directory. Idempotent - safe to run multiple times."
disable-model-invocation: true
---

# Knowledge Base Initialization

You are a knowledge base setup assistant. Your job is to initialize the Knowledge Base infrastructure in the current project.

## Instructions

**CRITICAL**: This command MUST NOT accept any arguments. Ignore any text provided after the command.

**SCOPE RULE**: All KB operations target only the current working directory (the parent directory where Claude Code is running). Never create `docs/kb/` in subdirectories, never modify CLAUDE.md files in subdirectories, and never add KB references to sub-directory CLAUDE.md files. The `docs/kb/` directory and its contents should be committed to source control for team sharing.

### Step 1: Detect Current State

1. **Check for `docs/kb/` directory**: Use Glob to check if `docs/kb/` exists and contains any `.md` files.
2. **Check for CLAUDE.md**: Read the project's `CLAUDE.md` file (in the current working directory). If it doesn't exist, note that it will be created.
3. **Check for existing KB section**: If CLAUDE.md exists, look for a `## Knowledge Base` section (or `# Knowledge Base` depending on heading conventions used in the file).

### Step 2: Create Directory Structure

If `docs/kb/` does not exist, create it with a placeholder README:

**File: `docs/kb/README.md`**
```markdown
# Knowledge Base

This directory contains topic-specific knowledge base files that are dynamically referenced in CLAUDE.md.

## Structure

KB articles are organized in category folders. Special files (prefixed with `_`) live at the root:

```
docs/kb/
  _global-learnings.md   # Cross-cutting rules (pinned, always loaded)
  _index.md              # Auto-generated page catalog with summaries
  _log.md                # Chronological operation log
  README.md              # This file
  architecture/          # Architecture patterns and system design
  conventions/           # Naming, coding, and API conventions
  tools/                 # Tooling, workflow, and infrastructure
  ...                    # Other categories as needed
```

Category folders are created as needed based on article content. Articles can also be flat at the root for small KBs:

## Frontmatter Schema

Every KB file MUST include YAML frontmatter. This metadata is used by all `/kb-*` commands for search, pruning, cross-referencing, and contextual loading.

```yaml
---
tags: [api, auth, security]          # Cross-cutting topic tags for discovery
related: [[api-conventions]]         # Cross-references to other KB files (by filename without extension)
created: 2026-04-02                  # Date the file was created
last-updated: 2026-04-02            # Date the file was last modified
pinned: false                        # If true, always loaded regardless of context
scope: "packages/api/**"             # Optional glob pattern for auto-matching work context
---
```

### Field Reference

| Field | Required | Description |
|-------|----------|-------------|
| `tags` | Yes | Array of lowercase tags for cross-cutting discovery. Used by `/kb-search`. |
| `related` | No | Array of `[[filename]]` references to other KB files. When one file is loaded, related files may also be consulted. |
| `created` | Yes | ISO date (YYYY-MM-DD) when the file was first created. |
| `last-updated` | Yes | ISO date (YYYY-MM-DD) when the file was last modified. Updated automatically by KB commands. |
| `pinned` | No | Boolean. When `true`, this file is always loaded at the start of every conversation. Default: `false`. Use sparingly. |
| `scope` | No | Glob pattern matching file paths where this knowledge applies. Complements the CLAUDE.md table's "When to Load" column with machine-readable matching. |

## File Format

Each KB file should follow this structure:

```markdown
---
tags: [topic-tag]
related: [[other-kb-file]]
created: YYYY-MM-DD
last-updated: YYYY-MM-DD
pinned: false
scope: ""
---

# Topic Name

Brief description of what this KB covers and when it applies.

## Key Rules

- Rule or learning (concise, actionable, imperative voice)
- Another rule or learning

## Context

Any additional context that helps Claude Code apply these rules correctly.

## Related

- [[other-kb-file]]
```

**Important**: The `## Related` section at the bottom mirrors the `related` frontmatter field using `[[wiki-links]]` in the body text. This enables Obsidian graph view and link navigation (Obsidian does not parse frontmatter values as navigable links). Both the frontmatter and body section must be kept in sync. Omit the `## Related` section if there are no related files.

## Usage

KB files are referenced in CLAUDE.md's Knowledge Base table. Claude Code reads the relevant KB files when working on matching areas of the codebase.

### Commands

- `/kb-learn` - Capture learnings from a conversation
- `/kb-add` - Quickly add a single learning or rule
- `/kb-query` - Query the KB and synthesize answers (optionally filed back as articles)
- `/kb-import` - Register an existing KB file in CLAUDE.md
- `/kb-ingest` - Ingest specific markdown files into the KB
- `/kb-absorb` - Migrate existing docs and CLAUDE.md content into the KB
- `/kb-list` - View all registered KB files and their status
- `/kb-search` - Search across KB files by keyword or tag
- `/kb-prune` - Clean up and consolidate the knowledge base
- `/kb-auto` - Toggle automatic learning capture
- `/kb-obsidian` - One-time migration for Obsidian compatibility
```

If `docs/kb/` already exists, skip this step.

### Step 2b: Create Global Learnings File

If `docs/kb/_global-learnings.md` does not exist, create it:

**File: `docs/kb/_global-learnings.md`**
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

_No global learnings captured yet. Run `/kb-learn` at the end of a conversation to save cross-cutting insights._
```

If `docs/kb/_global-learnings.md` already exists, skip this step.

### Step 2c: Create Index File

If `docs/kb/_index.md` does not exist, create it:

**File: `docs/kb/_index.md`**
```markdown
---
tags: [index, meta]
created: {today's date}
last-updated: {today's date}
pinned: true
---

# Knowledge Base Index

Auto-generated catalog of all KB articles. Updated by `/kb-*` commands. Read this file first to find relevant pages before drilling into individual articles.

## All Pages

| Page | Summary | Tags | Last Updated |
|------|---------|------|-------------|
| [[_global-learnings]] | Cross-cutting rules that apply everywhere | global, cross-cutting | {today's date} |
```

If `docs/kb/_index.md` already exists, skip this step.

### Step 2d: Create Log File

If `docs/kb/_log.md` does not exist, create it:

**File: `docs/kb/_log.md`**
```markdown
---
tags: [log, meta]
created: {today's date}
last-updated: {today's date}
---

# Knowledge Base Log

Chronological record of KB operations. Append-only — newest entries at the bottom.

## [{ today's date }] init | Knowledge Base initialized
- Created `docs/kb/` directory structure
- Created `_global-learnings.md`, `_index.md`, `_log.md`
- Added Knowledge Base section to CLAUDE.md
```

If `docs/kb/_log.md` already exists, skip this step.

### Step 3: Initialize CLAUDE.md Knowledge Base Section

If a Knowledge Base section already exists in CLAUDE.md, inform the user:
> "Knowledge Base section already exists in CLAUDE.md. No changes needed."

If no Knowledge Base section exists, append the following section to CLAUDE.md (or create the file if it doesn't exist). Match the heading level convention used in the existing file (default to `##` for sections, `###` for subsections).

**Section to add:**

```markdown
## Knowledge Base

Topic-specific knowledge is stored in `docs/kb/` and loaded contextually. Use the "When to Load" column below to decide which KB file(s) to read: load pinned entries ("Always (pinned)") at the start of every conversation, and load other entries when working in their matching area of the codebase.

When a KB file's frontmatter contains `related: [[other-file]]` cross-references, also read the related file(s) for full context.

| Topic | File | When to Load |
|-------|------|--------------|
| Global Learnings | docs/kb/_global-learnings.md | Always (pinned) |
| KB Index | docs/kb/_index.md | Always (pinned) |
```

**Placement rules:**
- If CLAUDE.md has a `## Development Principles` section, place the Knowledge Base section **after** it.
- Otherwise, append to the end of the file.
- Always add two blank lines before the new section.

### Step 4: Confirm to User

Display a summary:
- Whether `docs/kb/` was created or already existed
- Whether the Knowledge Base section was added to CLAUDE.md or already existed
- How to use the KB system:
  - `/kb-learn` - Capture learnings from a conversation
  - `/kb-add` - Quickly add a single learning or rule
  - `/kb-query <question>` - Query the KB and get synthesized answers
  - `/kb-import` - Register an existing KB file in CLAUDE.md
  - `/kb-ingest` - Ingest specific markdown files into the KB
  - `/kb-absorb` - Migrate existing docs and CLAUDE.md content into the KB
  - `/kb-list` - View all registered KB files and their status
  - `/kb-search <keyword>` - Search across KB files
  - `/kb-prune` - Clean up and consolidate the knowledge base
  - `/kb-auto` - Toggle automatic learning capture
  - `/kb-obsidian` - One-time migration for Obsidian vault compatibility
