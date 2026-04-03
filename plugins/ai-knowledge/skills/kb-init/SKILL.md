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

Files can be flat or nested:
- `docs/kb/api-conventions.md` - Flat topic file
- `docs/kb/frontend/react-patterns.md` - Nested under a category

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
related: []
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
```

## Usage

KB files are referenced in CLAUDE.md's Knowledge Base table. Claude Code reads the relevant KB files when working on matching areas of the codebase.

### Commands

- `/kb-learn` - Capture learnings from a conversation
- `/kb-add` - Quickly add a single learning or rule
- `/kb-import` - Register an existing KB file in CLAUDE.md
- `/kb-absorb` - Migrate existing docs and CLAUDE.md content into the KB
- `/kb-list` - View all registered KB files and their status
- `/kb-search` - Search across KB files by keyword or tag
- `/kb-prune` - Clean up and consolidate the knowledge base
- `/kb-auto` - Toggle automatic learning capture
```

If `docs/kb/` already exists, skip this step.

### Step 3: Initialize CLAUDE.md Knowledge Base Section

If a Knowledge Base section already exists in CLAUDE.md, inform the user:
> "Knowledge Base section already exists in CLAUDE.md. No changes needed."

If no Knowledge Base section exists, append the following section to CLAUDE.md (or create the file if it doesn't exist). Match the heading level convention used in the existing file (default to `##` for sections, `###` for subsections).

**Section to add:**

```markdown
## Knowledge Base

Topic-specific knowledge is stored in `docs/kb/` and loaded contextually. Consult the relevant KB file(s) when working in the matching area of the codebase. Files with `pinned: true` in frontmatter should always be loaded.

When a KB file's frontmatter contains `related: [[other-file]]` cross-references, also read the related file(s) for full context.

| Topic | File | When to Load |
|-------|------|--------------|
| _No entries yet_ | - | _Run `/kb-learn` to capture learnings or `/kb-add` to register KB files_ |

### Global Learnings

_No global learnings captured yet. Run `/kb-learn` at the end of a conversation to save cross-cutting insights._
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
  - `/kb-import` - Register an existing KB file in CLAUDE.md
  - `/kb-absorb` - Migrate existing docs and CLAUDE.md content into the KB
  - `/kb-list` - View all registered KB files and their status
  - `/kb-search <keyword>` - Search across KB files
  - `/kb-prune` - Clean up and consolidate the knowledge base
  - `/kb-auto` - Toggle automatic learning capture
