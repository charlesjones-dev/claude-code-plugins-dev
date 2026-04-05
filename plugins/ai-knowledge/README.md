# AI Knowledge Plugin

AI-powered knowledge base management for Claude Code. Capture conversation learnings, maintain topic-specific KB files, and dynamically reference institutional knowledge in CLAUDE.md.

## Overview

Over time, you accumulate project-specific knowledge during Claude Code conversations: things that didn't work, best practices, client requirements, and codebase gotchas. This plugin captures that knowledge so future sessions benefit from it automatically.

The knowledge base is a persistent, compounding wiki maintained by the LLM. It has three layers:
- **KB articles** (`docs/kb/{category}/*.md`): Topic-specific knowledge organized in category folders, loaded contextually
- **Global Learnings** (`docs/kb/_global-learnings.md`): Cross-cutting rules that apply everywhere (pinned, always loaded)
- **Index & Log** (`docs/kb/_index.md`, `docs/kb/_log.md`): Auto-generated catalog and chronological activity record

The knowledge base is fully **Obsidian-compatible** — open `docs/kb/` as an Obsidian vault to browse your knowledge graph, navigate between related topics, and visualize connections.

Inspired by Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern — the LLM does all the summarizing, cross-referencing, filing, and bookkeeping that makes a knowledge base useful over time.

## Commands

| Command | Description |
|---------|-------------|
| `/kb-init` | Initialize the KB section in CLAUDE.md and create `docs/kb/` directory |
| `/kb-learn` | Analyze the current conversation and extract learnings to KB files |
| `/kb-add` | Quickly add a learning or rule with interactive location picker |
| `/kb-import` | Register existing KB files in CLAUDE.md (adds missing frontmatter) |
| `/kb-ingest` | Ingest specific markdown files from anywhere in the project into the KB |
| `/kb-harvest` | Harvest knowledge from external sources: sibling repos, directories, files, or web URLs |
| `/kb-discover` | Analyze source code to extract implicit knowledge into KB articles |
| `/kb-absorb` | Migrate existing CLAUDE.md sections and docs/ content into the KB |
| `/kb-remove` | Remove a KB file and its CLAUDE.md reference |
| `/kb-list` | List all registered KB files with status, tags, dates, and cross-references |
| `/kb-search` | Search across KB files by keyword, topic, or tag (`tag:security`) |
| `/kb-prune` | Interactive cleanup: stale refs, duplicates, merges, frontmatter health |
| `/kb-query` | Query the KB and synthesize answers (optionally filed back as articles) |
| `/kb-auto` | Toggle automatic knowledge capture at end of conversations |
| `/kb-organize` | Reorganize flat KB files into category folders |
| `/kb-obsidian` | One-time upgrade for Obsidian compatibility, index, log, and folders |

## Getting Started

1. Run `/kb-init` in your project to set up the Knowledge Base section in CLAUDE.md and create the `docs/kb/` directory.

2. If you have existing documentation in CLAUDE.md or `docs/`, run `/kb-absorb` to organize it into the KB.

3. Optionally run `/kb-auto` to enable automatic learning capture -- Claude will offer to save learnings when conversations wrap up.

4. At the end of productive conversations, run `/kb-learn` to capture learnings (or let auto-capture prompt you).

5. Use `/kb-add` to quickly save a one-off rule or note without full conversation analysis.

6. Periodically run `/kb-prune` to keep the knowledge base organized.

7. Run `/kb-obsidian` to make an existing KB Obsidian-compatible, then open `docs/kb/` as an Obsidian vault.

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

### Obsidian Compatibility

KB files also include a `## Related` section at the bottom of the file body with `[[wiki-links]]` mirroring the frontmatter:

```markdown
## Related

- [[api-conventions]]
- [[auth-patterns]]
```

This is required because Obsidian does not parse frontmatter values as navigable links. The body `[[wiki-links]]` enable Obsidian's graph view edges and click-to-navigate between related topics. All `/kb-*` commands maintain this section automatically.

## Plugin Details

- **Version**: 1.3.0
- **Author**: [Charles Jones](https://charlesjones.dev)
- **License**: MIT
