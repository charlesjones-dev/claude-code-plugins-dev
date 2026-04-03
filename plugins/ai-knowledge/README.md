# AI Knowledge Plugin

AI-powered knowledge base management for Claude Code. Capture conversation learnings, maintain topic-specific KB files, and dynamically reference institutional knowledge in CLAUDE.md.

## Overview

Over time, you accumulate project-specific knowledge during Claude Code conversations: things that didn't work, best practices, client requirements, and codebase gotchas. This plugin captures that knowledge so future sessions benefit from it automatically.

Knowledge is stored in two layers:
- **KB files** (`docs/kb/*.md`): Topic-specific knowledge loaded contextually when working in relevant areas
- **Global Learnings** (in CLAUDE.md): Cross-cutting rules that apply everywhere

## Commands

| Command | Description |
|---------|-------------|
| `/kb-init` | Initialize the KB section in CLAUDE.md and create `docs/kb/` directory |
| `/kb-learn` | Analyze the current conversation and extract learnings to KB files |
| `/kb-add` | Quickly add a learning or rule with interactive location picker |
| `/kb-import` | Register existing KB files in CLAUDE.md (adds missing frontmatter) |
| `/kb-absorb` | Migrate existing CLAUDE.md sections and docs/ content into the KB |
| `/kb-remove` | Remove a KB file and its CLAUDE.md reference |
| `/kb-list` | List all registered KB files with status, tags, dates, and cross-references |
| `/kb-search` | Search across KB files by keyword, topic, or tag (`tag:security`) |
| `/kb-prune` | Interactive cleanup: stale refs, duplicates, merges, frontmatter health |
| `/kb-auto` | Toggle automatic knowledge capture at end of conversations |

## Getting Started

1. Run `/kb-init` in your project to set up the Knowledge Base section in CLAUDE.md and create the `docs/kb/` directory.

2. If you have existing documentation in CLAUDE.md or `docs/`, run `/kb-absorb` to organize it into the KB.

3. Optionally run `/kb-auto` to enable automatic learning capture -- Claude will offer to save learnings when conversations wrap up.

4. At the end of productive conversations, run `/kb-learn` to capture learnings (or let auto-capture prompt you).

5. Use `/kb-add` to quickly save a one-off rule or note without full conversation analysis.

6. Periodically run `/kb-prune` to keep the knowledge base organized.

## How It Works

The Knowledge Base table in CLAUDE.md tells Claude Code which KB files to read based on what you're working on:

```markdown
## Knowledge Base

| Topic | File | When to Load |
|-------|------|--------------|
| API Conventions | docs/kb/api-conventions.md | When working in packages/api/ |
| Auth Rules | docs/kb/auth.md | Always (pinned) |
| React Patterns | docs/kb/frontend/react-patterns.md | When working in packages/web/ |
```

When Claude Code starts a conversation and reads CLAUDE.md, it knows to load the relevant KB files based on the task context. Pinned files are always loaded.

## KB File Frontmatter

Every KB file uses YAML frontmatter for metadata, search, and cross-referencing:

```yaml
---
tags: [api, auth, security]          # Cross-cutting topic tags for discovery
related: [[api-conventions]]         # Cross-references to other KB files
created: 2026-04-02                  # Date the file was created
last-updated: 2026-04-02            # Date the file was last modified
pinned: false                        # If true, always loaded regardless of context
scope: "packages/api/**"             # Optional glob pattern for auto-matching
---
```

Cross-references (`related`) create a knowledge graph -- when Claude loads one KB file and sees related references, it knows to also consult the linked files for full context.

## Plugin Details

- **Version**: 1.0.0
- **Author**: [Charles Jones](https://charlesjones.dev)
- **License**: MIT
