---
name: kb-learn
description: "Analyze the current conversation to extract learnings, institutional knowledge, and best practices. Saves findings to topic-specific KB files and updates CLAUDE.md references."
disable-model-invocation: true
---

# Knowledge Base Learning Capture

You are a knowledge extraction specialist. Your job is to analyze the current conversation, identify valuable learnings, and persist them so future Claude Code sessions benefit from this institutional knowledge.

## Frontmatter Schema

Every KB file you create or update MUST have valid YAML frontmatter. When creating a new file, include all required fields. When updating an existing file, always update the `last-updated` field to today's date.

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

When a KB file has `related` entries in its frontmatter, you MUST also include a `## Related` section at the **end** of the file body with the same references as `[[wiki-links]]`. This enables Obsidian graph view and link navigation (frontmatter values are not parsed as navigable links by Obsidian). Always keep the `related` frontmatter AND the body `## Related` section in sync. If there are no related files, omit the `## Related` section entirely.

Example body section (placed at the very end of the file):
```markdown
## Related

- [[api-conventions]]
- [[auth-patterns]]
```

## Instructions

**CRITICAL**: This command MUST NOT accept any arguments. Ignore any text provided after the command.

### Phase 1: Conversation Analysis

Review the **entire** conversation from start to finish. Extract learnings in these categories:

1. **Mistakes or anti-patterns**: Things that were tried and failed, approaches the user corrected, or patterns explicitly called out as wrong for this project.
2. **Best practices discovered**: Approaches that worked well, patterns the user confirmed as correct, or conventions specific to this codebase.
3. **Institutional knowledge**: Information the user shared about external systems, team conventions, client requirements, or domain-specific rules that aren't evident from the code alone.
4. **Tool/workflow preferences**: Specific ways the user prefers to work (e.g., "always use pnpm, not npm", "run tests before committing", "this project uses a specific branching strategy").
5. **Codebase-specific rules**: Things learned about the codebase structure, gotchas, or non-obvious behaviors (e.g., "the auth middleware must be loaded before route handlers", "this legacy module uses a different naming convention").

**SECURITY**: Never store secrets, API keys, tokens, passwords, connection strings, or any sensitive credentials in KB files or CLAUDE.md — even if they were referenced in the conversation. Instead, record the *pattern* or *rule* about how secrets should be handled (e.g., "API keys for service X must come from environment variables, never hardcoded" rather than the actual key value). If a learning involves a specific service or endpoint URL that could be sensitive, describe it generically (e.g., "the internal staging API" rather than the full URL).

For each learning, determine:
- **Scope**: Is this a global learning (applies everywhere in this project) or topic-specific (applies only when working in a particular area)?
- **Topic**: If topic-specific, what topic/area does it relate to? (e.g., "API", "frontend", "database", "deployment", "testing", a specific package name, etc.)
- **Tags**: What cross-cutting tags apply? (e.g., a learning about API auth might be tagged `[api, auth, security]`)
- **Related**: Does this learning relate to content in existing KB files? If so, cross-reference them.

### Phase 2: Check Existing KB State

1. **Read CLAUDE.md**: Check for the Knowledge Base section. If it doesn't exist, inform the user to run `/kb-init` first, then stop.
2. **Read existing KB files**: For any topics that match extracted learnings, read the existing KB files to avoid duplication. Parse their frontmatter for tags and related references.
3. **Parse the KB reference table**: Know what's already registered so you can update or add entries.

### Phase 3: Propose Changes

Present the extracted learnings to the user in a clear summary, organized by destination:

```
Proposed Knowledge Base Updates:

## New/Updated KB Files

1. docs/kb/{topic}.md (NEW)
   Tags: [tag1, tag2]
   Related: [[existing-file]]
   - Learning: "Brief description of what will be captured"
   - Learning: "Another thing to capture"
   - Context: "When working on/in {area}"

2. docs/kb/{existing-topic}.md (UPDATE - appending)
   - Learning: "New thing to add to existing file"
   - Will update last-updated date

## Global Learnings (CLAUDE.md)
- "Cross-cutting learning that applies everywhere"
- "Another global insight"

## CLAUDE.md Table Updates
- New row: {Topic} | docs/kb/{file}.md | {when to load}

## Cross-References
- docs/kb/{file1}.md now references [[{file2}]]
```

**Wait for user approval before making any changes.** Use AskUserQuestion:
- Question: "Here are the learnings I extracted from this conversation. Should I save these to the knowledge base?"
- Options: "Save all" | "Let me pick which ones" | "Cancel"
- Header: "Knowledge Base Update"

If "Let me pick which ones", present each learning individually and ask whether to include it.

### Phase 4: Write Changes

After approval:

#### 4a: Create/Update KB Files

For each topic-specific learning:

1. **New KB file**: Create it under `docs/kb/` with frontmatter, content, and related links:
   ```markdown
   ---
   tags: [{inferred tags}]
   related: [{cross-references if any}]
   created: {today's date}
   last-updated: {today's date}
   pinned: false
   scope: ["{glob patterns if applicable}"]   # String or array of glob patterns
   ---

   # {Topic Name}

   {Brief description of what this KB covers and when it applies.}

   ## Key Rules

   - {Learning 1 - concise, actionable}
   - {Learning 2}

   ## Related

   - [[{related-kb-file}]]
   ```

   Only include the `## Related` section if there are related files. It must be the last section in the file.

2. **Existing KB file**: Read the file, append new learnings under the appropriate section. Do not duplicate existing entries. If a learning contradicts an existing one, replace the old entry with the new one (the latest conversation has the most current information). **Always update `last-updated` in the frontmatter to today's date.** Add any new tags or related references to the frontmatter.

**KB file writing rules:**
- **Prefer subfolder organization**: When creating new KB files, place them in a category folder (e.g., `docs/kb/architecture/`, `docs/kb/conventions/`, `docs/kb/testing/`). Use existing folder structure as a guide. If the KB is still small (< 5 files) or flat, placing files at the root is fine.
- Keep entries concise - enough context for future Claude Code sessions to understand and apply, not verbose explanations.
- Use imperative voice: "Use X", "Never do Y", "Prefer X over Y".
- Include just enough "why" so the rule isn't blindly followed without understanding.
- Use nested directories when a topic naturally belongs under a category (e.g., `docs/kb/packages/api.md` for a monorepo package).

#### 4b: Update Cross-References

After creating/updating KB files:
1. For any new KB file that relates to existing KB files, add `[[new-file]]` to the existing files' `related` frontmatter.
2. For any existing KB file referenced by new content, add the reverse reference.
3. Update the `## Related` body section on any file whose `related` frontmatter was modified (keep them in sync).
4. Update `last-updated` on any file whose frontmatter was modified.

#### 4c: Update Global Learnings

Global learnings are stored in `docs/kb/_global-learnings.md` (a pinned KB file), NOT inline in CLAUDE.md.

1. **Read `docs/kb/_global-learnings.md`**. If it doesn't exist, create it with frontmatter (`tags: [global, cross-cutting]`, `pinned: true`, today's dates) and a `# Global Learnings` heading.
2. Remove placeholder text if present ("_No global learnings captured yet..._").
3. Append new learnings as bullet points under `## Key Rules`.
4. Deduplicate: if a learning is substantially similar to an existing one, update the existing entry rather than adding a duplicate.
5. If a new learning contradicts an existing one, replace the old one.
6. Update `last-updated` in frontmatter to today's date.
7. Ensure `_global-learnings.md` is registered in the CLAUDE.md Knowledge Base table as: `| Global Learnings | docs/kb/_global-learnings.md | Always (pinned) |`

#### 4d: Update CLAUDE.md Reference Table

1. Remove the placeholder row if present ("_No entries yet_").
2. Add new rows for any new KB files created.
3. Update existing rows if the "When to Load" context changed.
4. For pinned KB files, set "When to Load" to "Always (pinned)".
5. **Deduplicate**: If multiple rows point to the same file, merge them.
6. **Keep the table sorted** alphabetically by Topic.
7. **Format the "When to Load" column** using the structured format: scope glob patterns (backtick-wrapped, comma-separated) followed by an em dash (`—`) and topic keywords from tags. Example: `` `src/api/**`, `*.controller.ts` — api, rest, middleware ``. If the KB file has no scope patterns, use keywords only: `— api, rest, middleware`. Pinned files always use `Always (pinned)`.

### Phase 5: Update Index and Log

After all KB changes:

1. **Update `docs/kb/_index.md`**: If this file exists, update it to reflect new/updated articles — add entries with one-line summaries for new files, update summaries if content changed significantly, and remove entries for deleted files. Keep categories organized by topic. Update `last-updated` in its frontmatter.
2. **Append to `docs/kb/_log.md`**: If this file exists, append an entry:
   ```
   ## [YYYY-MM-DD] learn | Conversation learnings captured
   - Created: {list of new files}
   - Updated: {list of updated files}
   - Global learnings: {count added}
   ```

### Phase 6: Confirmation

After writing all changes, display a summary:
- Number of KB files created/updated
- Number of global learnings added
- Number of table entries added/updated
- Cross-references added
- Reminder: "These learnings will be available in future Claude Code sessions."

## Quality Rules

- **Conciseness over completeness**: A future Claude Code session should gain the insight in minimal tokens. Don't write paragraphs when a sentence will do.
- **No duplication**: Always check existing KB files and global learnings before adding.
- **Actionable entries only**: Don't capture vague observations. Every entry should change behavior in future sessions.
- **Freshest knowledge wins**: If the conversation revealed that a previous learning was wrong, update or replace it.
- **Organize naturally**: Use nesting when there's a clear hierarchy (e.g., monorepo packages), keep flat when topics are independent.
- **Maintain frontmatter**: Every KB file write must include valid, complete frontmatter. Always update `last-updated`. Always add relevant tags.
