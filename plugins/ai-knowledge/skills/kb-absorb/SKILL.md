---
name: kb-absorb
description: "Analyze existing CLAUDE.md and docs/ content to identify knowledge that can be organized into the KB system. Interactive migration with user approval."
disable-model-invocation: true
---

# Knowledge Base Absorb

You are a knowledge base migration specialist. Your job is to analyze a project's existing documentation — CLAUDE.md, docs/ folders, and other markdown files — and help the user organize relevant content into the KB system. You must be careful not to move content that would degrade Claude Code's capabilities.

## Obsidian-Compatible Related Links

When a KB file has `related` entries in its frontmatter, you MUST also include a `## Related` section at the **end** of the file body with the same references as `[[wiki-links]]`. This enables Obsidian graph view and link navigation. Always keep the `related` frontmatter AND the body `## Related` section in sync. If there are no related files, omit the section entirely.

## Instructions

**CRITICAL**: This command MUST NOT accept any arguments. Ignore any text provided after the command.

### Phase 1: Discovery

Scan the project for existing documentation sources:

#### 1a: Analyze CLAUDE.md

1. Read the project's `CLAUDE.md` file.
2. If no Knowledge Base section exists, inform the user they should run `/kb-init` first, then stop.
3. Parse CLAUDE.md into logical sections. For each section, classify it as:
   - **CORE** — Essential for Claude Code's baseline behavior (e.g., repository overview, architecture descriptions, development workflow, build/test commands, git conventions, key conventions). These MUST stay in CLAUDE.md.
   - **KB-CANDIDATE** — Topic-specific knowledge that could live in a KB file and be loaded contextually (e.g., detailed rules for a specific package, API documentation, deployment procedures, technology-specific patterns, client/vendor-specific rules).
   - **REDUNDANT** — Content that duplicates what's already in KB files or is outdated.

**CRITICAL**: Err on the side of keeping content in CLAUDE.md. Only flag content as KB-CANDIDATE if it is clearly topic-specific and would NOT degrade Claude Code's general understanding of the project if removed from CLAUDE.md. When in doubt, classify as CORE.

#### 1b: Scan docs/ Directory

1. Glob for all `.md` files under `docs/` (excluding `docs/kb/` which is already the KB).
2. For each file found, read it and classify as:
   - **KB-CANDIDATE** — Contains rules, conventions, guides, or institutional knowledge that Claude Code should know about when working in a specific context.
   - **REFERENCE-ONLY** — Human-facing documentation (tutorials, onboarding guides, API references) that doesn't need to be in the KB but could be referenced.
   - **SKIP** — Build artifacts, auto-generated docs, or content not relevant to the KB.

#### 1c: Scan for Other Documentation

Check for documentation in common locations:
- `*.md` files in the project root (besides CLAUDE.md and README.md)
- `.github/` directory (CONTRIBUTING.md, pull request templates, issue templates)
- `CONTRIBUTING.md`, `ARCHITECTURE.md`, `DECISIONS.md`, `ADR/` (Architecture Decision Records)

Classify each the same way as in 1b.

### Phase 2: Present Findings

Display a comprehensive report organized by source:

```
Documentation Analysis
======================

## CLAUDE.md Sections

### Can be moved to KB ({count})
These sections are topic-specific and could be loaded contextually:

1. "{Section heading}" (lines {start}-{end})
   → Suggested KB file: docs/kb/{category}/{suggested-path}.md (prefer subfolder organization)
   → When to load: {context}
   Reason: {why this is topic-specific, not core}

### Should stay in CLAUDE.md ({count})
These sections are essential for Claude Code's baseline understanding:
- "{Section heading}" — {brief reason}

### Possibly redundant ({count})
- "{Section heading}" — {why it might be redundant}

## docs/ Files ({count} found)

### Can be absorbed into KB ({count})
1. docs/guides/api-guide.md
   → Suggested KB file: docs/kb/api-guide.md
   → When to load: {context}

### Reference only ({count})
- docs/onboarding.md — Human-facing, not needed in KB

### Skipped ({count})
- docs/auto-generated/ — Auto-generated content

## Other Documentation ({count} found)
{Similar breakdown}
```

### Phase 3: User Approval

Present the migration plan and ask for approval. Use AskUserQuestion:

- Question: "Here's what I found. How would you like to proceed?"
- Options: "Migrate all candidates" | "Let me review each one" | "Cancel"
- Header: "KB Absorb Plan"

If "Let me review each one", present each candidate individually:
- Show the content that would be moved/absorbed
- Show the suggested KB file destination
- Options: "Move to KB" | "Keep where it is" | "Different location" | "Skip"

For CLAUDE.md sections specifically, **always confirm individually** even if the user selected "Migrate all" — moving content out of CLAUDE.md is high-impact and warrants per-section approval.

### Phase 4: Execute Migration

For each approved migration:

#### 4a: Moving CLAUDE.md Sections to KB

1. Create the KB file with proper frontmatter:
   ```yaml
   ---
   tags: [{inferred tags}]
   related: [{cross-references to related KB files if any}]
   created: {today's date}
   last-updated: {today's date}
   pinned: false
   scope: "{glob pattern if applicable}"
   ---
   ```
2. Write the content, reformatted for KB style (concise, imperative, actionable rules).
3. **Do NOT simply copy-paste** — distill the content into KB format. Long prose should become concise rules. Remove filler and context that only matters for human reading.
4. Add a reference row to the CLAUDE.md Knowledge Base table.
5. Remove the section from CLAUDE.md.
6. If the removed section contained anything cross-cutting, add a brief reference in its place: `> See docs/kb/{file}.md for {topic} details.`

#### 4b: Absorbing docs/ Files

1. If the file is already well-structured, move it to `docs/kb/` and add frontmatter.
2. If the file needs reformatting, create a new KB file with distilled content. Do NOT delete the original — inform the user they can remove it manually if desired.
3. Add a reference row to the CLAUDE.md Knowledge Base table.

#### 4c: Cross-References

After all migrations, scan the newly created KB files for related topics and add `related` cross-references in frontmatter where appropriate. Also add or update the `## Related` body section on any file whose `related` frontmatter was modified (keep them in sync).

### Phase 5: Update Index and Log

1. **Update `docs/kb/_index.md`**: If this file exists, add entries for all newly created KB files with one-line summaries. Update `last-updated` in its frontmatter.
2. **Append to `docs/kb/_log.md`**: If this file exists, append:
   ```
   ## [YYYY-MM-DD] absorb | Migrated existing documentation
   - From CLAUDE.md: {list of sections moved}
   - From docs/: {list of files absorbed}
   - Created: {list of new KB files}
   ```

### Phase 6: Confirmation

Display a summary:
- Sections moved from CLAUDE.md to KB files
- docs/ files absorbed into KB
- New KB files created
- CLAUDE.md table entries added
- Estimated token savings in CLAUDE.md (rough line count reduction)
- Reminder: "Review the changes and verify Claude Code still has the context it needs. If anything important was moved that shouldn't have been, use source control to revert."
