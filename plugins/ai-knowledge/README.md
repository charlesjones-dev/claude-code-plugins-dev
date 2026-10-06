# AI Knowledge Plugin

Knowledge base management for Claude Code. Capture conversation learnings, maintain topic-specific KB files, and list them in CLAUDE.md so Claude knows when to read them.

## Overview

Claude Code's auto memory saves learnings to a per-project memory folder on your machine. That covers personal recall. This plugin adds a curated knowledge base for the project itself: things that didn't work, best practices, client requirements, and codebase gotchas, organized into topic files that live in git and travel with the repository so your whole team (and every machine) gets them.

The knowledge base has three layers:
- **KB articles** (`docs/kb/{category}/*.md`): Topic-specific knowledge organized in category folders, loaded contextually
- **Global Learnings** (`docs/kb/_global-learnings.md`): Cross-cutting rules that apply everywhere (pinned, always loaded)
- **Index & Log** (`docs/kb/_index.md`, `docs/kb/_log.md`): Auto-generated catalog and chronological activity record

Inspired by Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern, where the LLM does the filing and cross-referencing.

## How This Differs from Claude Code's Auto Memory

| | Auto memory | AI Knowledge KB (`docs/kb/`) |
|---|---|---|
| **Curation** | Automatic: Claude decides what to write | Deliberate: you review and file learnings |
| **Location** | Per-machine, outside the repo | Checked into git, versioned with the code |
| **Sharing** | Personal, single machine | Shared with your whole team via the repository |
| **Structure** | A `MEMORY.md` index plus topic files | Categorized topic files with frontmatter, tags, and cross-references |
| **Loading** | First 200 lines (or 25KB) of `MEMORY.md` at session start; topic files on demand | Pinned files at session start; others when scope globs or keywords match the task |
| **Tooling** | `/memory` to browse, edit, or turn it off | Query, search, synthesis, pruning, and import/harvest commands |
| **Browsing** | Plain markdown | Obsidian-compatible knowledge graph with wiki-links |

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
| `/kb-load` | Manually load a KB file into context by name, topic, or tag |
| `/kb-list` | List all registered KB files with status, tags, dates, and cross-references |
| `/kb-search` | Search across KB files by keyword, topic, or tag (`tag:security`) |
| `/kb-prune` | Interactive cleanup: stale refs, duplicates, merges, frontmatter health |
| `/kb-query` | Query the KB and synthesize answers (optionally filed back as articles) |
| `/kb-auto` | Toggle automatic knowledge capture at end of conversations |
| `/kb-organize` | Reorganize flat KB files into category folders |
| `/kb-upgrade` | Upgrade the KB to the current plugin format: Obsidian compat, structured loading, preamble, index |

## Getting Started

1. Run `/kb-init` in your project to set up the Knowledge Base section in CLAUDE.md and create the `docs/kb/` directory.

2. If you have existing documentation in CLAUDE.md or `docs/`, run `/kb-absorb` to organize it into the KB.

3. Optionally run `/kb-auto` to enable automatic learning capture. Claude will offer to save learnings when conversations wrap up.

4. At the end of productive conversations, run `/kb-learn` to capture learnings (or let auto-capture prompt you).

5. Use `/kb-add` to quickly save a one-off rule or note without full conversation analysis.

6. Periodically run `/kb-prune` to keep the knowledge base organized.

7. Run `/kb-upgrade` to bring your KB up to the current plugin format (Obsidian compatibility, structured loading, etc.).

## How It Works

The Knowledge Base table in CLAUDE.md tells Claude Code which KB files to read based on what you're working on:

```markdown
## Knowledge Base

| Topic | File | When to Load |
|-------|------|--------------|
| API Conventions | docs/kb/conventions/api-conventions.md | `packages/api/**`, `*.controller.ts` — api, rest |
| Auth Rules | docs/kb/security/auth.md | Always (pinned) |
| React Patterns | docs/kb/frontend/react-patterns.md | `packages/web/**` — react, frontend, components |
```

`/kb-init` adds instructions above the table telling Claude to read pinned files at the start of each conversation and other files when the files you're editing match their scope globs or the task matches their keywords. They're instructions, not enforced rules, so if Claude misses a file you need, load it with `/kb-load`.

## KB File Frontmatter

Every KB file uses YAML frontmatter for metadata, search, and cross-referencing:

```yaml
---
tags: [api, auth, security]          # Cross-cutting topic tags for discovery
related: [[api-conventions]]         # Cross-references to other KB files
created: 2026-04-02                  # Date the file was created
last-updated: 2026-04-02            # Date the file was last modified
pinned: false                        # If true, always loaded regardless of context
scope:                               # Optional glob pattern(s) for auto-matching
  - "packages/api/**"
  - "*.controller.ts"
---
```

Cross-references (`related`) link KB files into a graph. When Claude loads one file, it may also read the files it links to.

### Obsidian Compatibility

Open `docs/kb/` as an Obsidian vault to browse it. KB files also include a `## Related` section at the bottom of the file body with `[[wiki-links]]` mirroring the frontmatter:

```markdown
## Related

- [[api-conventions]]
- [[auth-patterns]]
```

This is required because Obsidian doesn't parse frontmatter values as navigable links. The body `[[wiki-links]]` enable Obsidian's graph view edges and click-to-navigate between related topics. All `/kb-*` commands maintain this section automatically.

## Plugin Details

- **Version**: 1.5.2
- **Author**: [Charles Jones](https://charlesjones.dev)
- **License**: MIT

## Contributing

Bug reports and fixes are welcome. See [CONTRIBUTING.md](../../CONTRIBUTING.md).
