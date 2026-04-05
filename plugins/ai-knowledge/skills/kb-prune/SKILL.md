---
name: kb-prune
description: "Interactive cleanup and consolidation of the knowledge base. Finds stale references, duplicates, orphaned files, frontmatter issues, and opportunities to merge related topics."
disable-model-invocation: true
---

# Knowledge Base Pruning

You are a knowledge base maintenance specialist. Your job is to clean up, consolidate, and organize the project's knowledge base. All changes require user approval.

## Obsidian-Compatible Related Links

When modifying KB files, you MUST keep the `related` frontmatter AND the `## Related` body section (at the end of the file) in sync. When merging files, fixing cross-references, or updating related links, always update both locations. If `related` becomes empty, remove the `## Related` body section entirely.

## Frontmatter Schema

When modifying KB files during pruning (merges, promotions, etc.), always maintain valid frontmatter and update `last-updated` to today's date.

```yaml
---
tags: [topic-tag-1, topic-tag-2]       # Required: lowercase tags for discovery
related: [[other-kb-file]]             # Optional: cross-references to related KB files
created: YYYY-MM-DD                    # Required: date created
last-updated: YYYY-MM-DD              # Required: date last modified (update on every write)
pinned: false                          # Optional: true = always loaded. Default false
scope: "src/api/**"                    # Optional: glob pattern for auto-matching
---
```

## Instructions

**CRITICAL**: This command MUST NOT accept any arguments. Ignore any text provided after the command.

### Phase 1: Full KB Audit

Perform a comprehensive audit of the knowledge base:

#### 1a: Parse CLAUDE.md

1. Read CLAUDE.md and find the Knowledge Base section.
2. If no Knowledge Base section exists, inform the user: "No Knowledge Base section found. Run `/kb-init` first." and stop.
3. Parse the reference table (Topic, File, When to Load).
4. Parse the Global Learnings subsection.

#### 1b: Verify File References

For each entry in the table:
1. Check if the referenced file exists.
2. Categorize as **OK** or **STALE** (file missing).

#### 1c: Find Orphaned Files

1. Glob all `.md` files under `docs/kb/` (excluding `docs/kb/README.md`).
2. Identify files not referenced in the CLAUDE.md table. Categorize as **ORPHANED**.

#### 1d: Frontmatter Health Check

For each existing KB file:
1. Check if YAML frontmatter exists.
2. Check if all required fields are present (`tags`, `created`, `last-updated`).
3. Categorize issues:
   - **NO FRONTMATTER** - File has no YAML frontmatter at all.
   - **INCOMPLETE FRONTMATTER** - Missing required fields.
   - **REVIEW SUGGESTED** - `last-updated` is older than 90 days. This doesn't mean the content is wrong — stable knowledge is fine — but it may be worth a quick review to confirm it's still accurate.

#### 1e: Detect Duplicates and Merge Candidates

1. Read all existing KB files.
2. Look for:
   - **Duplicate entries**: KB files with substantially overlapping content.
   - **Merge candidates**: KB files covering closely related topics that could be consolidated (e.g., `api-auth.md` and `api-tokens.md` could merge into `api-auth.md`). Use tags to identify overlap — files with highly overlapping tag sets are likely candidates.
   - **Contradictions**: Rules in different KB files or between KB files and Global Learnings that conflict.

#### 1f: Cross-Reference Integrity

1. For each KB file with `related` references in frontmatter:
   - Check that referenced files exist.
   - Check for one-way references (A links to B but B doesn't link to A).
   - Check that the `## Related` body section matches the `related` frontmatter (flag **OUT OF SYNC** if they differ or if the body section is missing).
2. Categorize as **BROKEN LINK**, **ONE-WAY REFERENCE**, or **OUT OF SYNC**.

#### 1g: Review Global Learnings

Global learnings are stored in `docs/kb/_global-learnings.md`. If this file doesn't exist, check for a legacy `### Global Learnings` inline section in CLAUDE.md — if found, flag it as **NEEDS MIGRATION** and suggest running `/kb-obsidian`.

1. Read `docs/kb/_global-learnings.md` (or the legacy inline section if the file doesn't exist).
2. Check for entries that are:
   - **Outdated**: No longer relevant based on current codebase state (check if referenced files/patterns still exist).
   - **Duplicated**: Same information exists in a KB file AND in Global Learnings.
   - **Promotable**: A global learning that's actually topic-specific and should be moved to a KB file.

### Phase 2: Present Findings

Display a comprehensive audit report:

```
Knowledge Base Audit Report
============================

## Issues Found

### Stale References ({count})
These CLAUDE.md table entries point to files that no longer exist:
- {Topic} -> {file path} (MISSING)

### Orphaned Files ({count})
These KB files exist but aren't referenced in CLAUDE.md:
- {file path} (tags: {tags})

### Frontmatter Issues ({count})
- {file path} — NO FRONTMATTER
- {file path} — Missing fields: tags, created
- {file path} — Last updated 120 days ago (review suggested, may still be valid)

### Merge Candidates ({count})
These KB files have overlapping content and could be consolidated:
- {file1} + {file2} -> Suggested merge into {target}
  Overlapping tags: {shared tags}
  Reason: {brief explanation}

### Cross-Reference Issues ({count})
- {file1} references [[{file2}]] but {file2} doesn't reference [[{file1}]] (one-way)
- {file1} references [[{file2}]] but {file2} doesn't exist (broken)

### Duplicate/Redundant Entries ({count})
- Global learning "{entry}" duplicates content in {kb file}

### Contradictions ({count})
- {file1} says "{rule1}" but {file2} says "{rule2}"

### Promotable Global Learnings ({count})
- "{learning}" could move to {suggested kb file} (tags: {suggested tags})

## Summary
- {ok_count} healthy KB files
- {total_issues} issues found
```

If no issues found:
> "Knowledge base is clean. No issues found across {file_count} KB files and {learning_count} global learnings."

### Phase 3: Propose Actions

If issues were found, present a remediation plan:

Use AskUserQuestion:
- Question: "Here's my recommended cleanup plan. How would you like to proceed?"
- Show the proposed actions grouped by type
- Options: "Apply all recommendations" | "Let me review each one" | "Cancel"
- Header: "KB Cleanup Plan"

If "Let me review each one", present each proposed action individually:
- For stale references: "Remove row for '{Topic}' from CLAUDE.md table?"
- For orphaned files: "Register '{file}' in CLAUDE.md, or delete it?"
- For frontmatter issues: "Add/fix frontmatter for '{file}'?" (show proposed frontmatter)
- For merge candidates: "Merge '{file1}' and '{file2}' into '{target}'?"
- For cross-reference issues: "Add missing reverse reference? / Remove broken reference?"
- For duplicates: "Remove duplicate from Global Learnings (kept in KB file)?"
- For contradictions: "Which rule is correct: '{rule1}' or '{rule2}'?"
- For promotable learnings: "Move '{learning}' from Global Learnings to '{kb file}'?"

### Phase 4: Execute Approved Actions

Apply only the user-approved changes:

1. **Stale references**: Remove rows from the CLAUDE.md table.
2. **Orphaned files**: Either register them (add table row, fix frontmatter) or delete the file, per user choice.
3. **Frontmatter fixes**: Add/complete frontmatter on affected files. Update `last-updated`.
4. **Merges**: Combine content from source files into target file, merge tags and related references in frontmatter, remove source files, update CLAUDE.md table. Update `last-updated`.
5. **Cross-reference fixes**: Add missing reverse references or remove broken links. Sync the `## Related` body section with the `related` frontmatter on all modified files. Update `last-updated` on modified files.
6. **Duplicates**: Remove the redundant entry from whichever location the user chose.
7. **Contradictions**: Update the incorrect entry with the correct rule. Update `last-updated`.
8. **Promotions**: Move the learning from `docs/kb/_global-learnings.md` to the target KB file, add table reference if needed. Update `last-updated` on `_global-learnings.md`.
9. **Legacy migration**: If inline `### Global Learnings` content was found in CLAUDE.md, migrate it to `docs/kb/_global-learnings.md` and remove the inline section.

After all changes:
- Re-sort the CLAUDE.md reference table alphabetically by Topic.
- Remove any placeholder text if real entries now exist.
- Ensure no empty sections remain.

### Phase 5: Update Index and Log

1. **Update `docs/kb/_index.md`**: If this file exists, update it to reflect all changes — remove entries for deleted files, update summaries for merged files, add entries for newly registered orphans. Update `last-updated` in its frontmatter.
2. **Append to `docs/kb/_log.md`**: If this file exists, append:
   ```
   ## [YYYY-MM-DD] prune | KB cleanup and consolidation
   - Stale refs removed: {count}
   - Orphans registered/deleted: {count}
   - Frontmatter fixes: {count}
   - Merges: {count}
   - Cross-ref fixes: {count}
   ```

### Phase 6: Confirmation

Display a summary of all changes made:
- Files created/updated/deleted
- Frontmatter fixes applied
- Cross-references added/removed
- CLAUDE.md table rows added/removed/updated
- Global learnings added/removed/moved
- Final KB file count and health status
