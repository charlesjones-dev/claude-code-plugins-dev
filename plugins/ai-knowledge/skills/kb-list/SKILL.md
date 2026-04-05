---
name: kb-list
description: "List all registered KB files from CLAUDE.md, show their status (exists/missing), tags, dates, and pinned status."
disable-model-invocation: true
---

# Knowledge Base Listing

You are a knowledge base inventory assistant. Your job is to display the current state of the project's knowledge base. This is a read-only operation - no files are modified.

## Instructions

**CRITICAL**: This command MUST NOT accept any arguments. Ignore any text provided after the command.

### Step 1: Read CLAUDE.md

1. Read the project's `CLAUDE.md` file.
2. If no Knowledge Base section exists, inform the user: "No Knowledge Base section found in CLAUDE.md. Run `/kb-init` to set one up." and stop.
3. Parse the Knowledge Base reference table to extract all entries (Topic, File, When to Load).
4. Read `docs/kb/_global-learnings.md` if it exists for global learnings count. Also check for a legacy `### Global Learnings` inline section in CLAUDE.md (older setups may still have this — if found, suggest running `/kb-obsidian` to migrate).

### Step 2: Verify File Status and Read Frontmatter

For each entry in the table:
1. Check if the referenced file actually exists using Glob or Read.
2. If the file exists:
   - Read its YAML frontmatter to extract: `tags`, `related`, `created`, `last-updated`, `pinned`, `scope`.
   - Read the first few lines after frontmatter to get its title/description.
   - Mark as **OK**.
   - Flag if frontmatter is missing or incomplete (**NEEDS FRONTMATTER**).
3. If the file doesn't exist, mark as **MISSING**.

### Step 3: Scan for Orphaned Files

1. Glob for all `.md` files under `docs/kb/` (excluding `docs/kb/README.md`).
2. Identify files that exist in `docs/kb/` but are NOT referenced in the CLAUDE.md table.
3. Mark these as **UNREGISTERED**. Read their frontmatter if present.

### Step 4: Display Summary

Present the results in a clear format:

```
Knowledge Base Status
=====================

Registered KB Files:
| Status | Topic | File | Tags | Last Updated | Pinned | When to Load |
|--------|-------|------|------|-------------|--------|--------------|
| OK | API Conventions | docs/kb/api-conventions.md | api, rest | 2026-04-01 | No | When working in packages/api/ |
| OK | Auth Rules | docs/kb/auth.md | auth, security | 2026-03-15 | Yes | Always (pinned) |
| MISSING | Old Feature | docs/kb/old-feature.md | - | - | - | When working on feature X |
| NEEDS FM | Deployment | docs/kb/deployment.md | (no frontmatter) | - | - | When deploying |

Cross-References:
- docs/kb/api-conventions.md → [[auth]]
- docs/kb/auth.md → [[api-conventions]]

Unregistered Files (in docs/kb/ but not in CLAUDE.md):
- docs/kb/new-topic.md (tags: misc, workflow)

Global Learnings: {count} entries

Summary: {ok_count} registered, {missing_count} missing, {unregistered_count} unregistered, {no_frontmatter_count} missing frontmatter
```

If there are issues, suggest:
- Missing files: "Run `/kb-prune` to clean up stale references."
- Unregistered files: "Run `/kb-import` to register these files in CLAUDE.md."
- Missing frontmatter: "Run `/kb-import` on these files to add frontmatter."
