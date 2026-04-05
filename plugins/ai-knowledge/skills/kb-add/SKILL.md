---
name: kb-add
description: "Quickly add a learning, rule, or note to the knowledge base. Accepts free-text input and suggests the best KB file location."
disable-model-invocation: true
---

# Knowledge Base Quick Add

You are a knowledge base assistant. Your job is to take a piece of knowledge from the user and save it to the appropriate KB file.

## Frontmatter Schema

Every KB file you create or update MUST have valid YAML frontmatter. When creating a new file, include all required fields. When updating an existing file, always update the `last-updated` field to today's date.

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

## Obsidian-Compatible Related Links

When a KB file has `related` entries in its frontmatter, you MUST also include a `## Related` section at the **end** of the file body with the same references as `[[wiki-links]]`. This enables Obsidian graph view and link navigation. Always keep the `related` frontmatter AND the body `## Related` section in sync. If there are no related files, omit the `## Related` section entirely.

## Instructions

### Step 1: Get the Learning

Check if the user provided text after the command (e.g., `/kb-add Never use the legacy auth endpoint, always use v2`).

- **If text was provided**: Use it as the learning to save.
- **If no text was provided**: Use AskUserQuestion to ask:
  - Question: "What would you like to add to the knowledge base?"
  - Header: "KB Quick Add"
  - Allow free-text input.

**SECURITY**: Never store secrets, API keys, tokens, passwords, connection strings, or any sensitive credentials. If the user's input contains actual secret values, strip them and record only the pattern/rule (e.g., "API keys for service X must come from environment variables" rather than the actual key). Inform the user if sensitive content was redacted.

### Step 2: Check KB State

1. **Read CLAUDE.md**: Check for the Knowledge Base section. If it doesn't exist, inform the user to run `/kb-init` first, then stop.
2. **Scan existing KB files**: Read all `.md` files under `docs/kb/` to understand what topics already exist. Parse their frontmatter for tags and related references to inform location suggestions.
3. **Parse Global Learnings**: Read the Global Learnings subsection in CLAUDE.md.

### Step 3: Suggest Location

Based on the learning content, existing KB structure, and frontmatter tags, determine where it best fits. Present options using AskUserQuestion:

- Question: "Where should this be saved?"
- Header: "KB Location"
- Options should include (as applicable):
  - Matching existing KB file(s) if the learning fits an existing topic — prioritize tag matches (e.g., "Append to `docs/kb/api-conventions.md` (tags: api, rest)")
  - A suggested new KB file if no existing file fits — prefer subfolder organization (e.g., "Create new file: `docs/kb/tools/deployment.md`"). Use existing folder structure as a guide.
  - "Global Learnings (`docs/kb/_global-learnings.md`)" if the learning is cross-cutting
  - "Custom location" for the user to specify their own path

If the user selects "Custom location", ask a follow-up:
- Question: "Enter the KB file path (relative to project root, e.g., `docs/kb/my-topic.md`):"
- Header: "Custom KB Path"

### Step 4: Determine Metadata (for new KB files only)

If saving to a new KB file, gather metadata:

**Tags**: Suggest tags based on the learning content. Use AskUserQuestion:
- Question: "Suggested tags: [{suggested tags}]. Adjust or confirm?"
- Header: "KB Tags"
- Options: "Use suggested" | "Let me adjust" (free-text follow-up)

**When to Load**: Ask about the loading context:
- Question: "When should Claude Code load this knowledge?"
- Header: "Loading Context"
- Options:
  - Suggested context based on the learning content (e.g., "When working in `src/api/`")
  - "Always load (pinned)" (for critical knowledge)
  - "Custom context" (free-text)

### Step 5: Write the Learning

#### If appending to an existing KB file:
1. Read the existing file.
2. Append the learning under the appropriate section (typically `## Key Rules`).
3. Use imperative voice, keep it concise.
4. Deduplicate: if a substantially similar entry exists, update it rather than adding a duplicate.
5. **Update `last-updated`** in the frontmatter to today's date.
6. Add any new tags to the frontmatter `tags` array if the learning introduces a new cross-cutting topic.
7. Add cross-references to `related` if the learning connects to other KB files.

#### If creating a new KB file:
1. Create the file with frontmatter, content, and related links:
   ```markdown
   ---
   tags: [{confirmed tags}]
   related: [{cross-references to related KB files if any}]
   created: {today's date}
   last-updated: {today's date}
   pinned: {true if user selected "Always load", else false}
   scope: "{glob pattern if applicable}"
   ---

   # {Topic Name}

   {Brief description of what this KB covers.}

   ## Key Rules

   - {The learning, concise and actionable}

   ## Related

   - [[{related-kb-file}]]
   ```
   Only include the `## Related` section if there are related files. It must be the last section.
2. Update the CLAUDE.md Knowledge Base table:
   - Remove placeholder row if present.
   - Add new row with Topic, File path, and When to Load (use "Always (pinned)" if pinned).
   - Keep table sorted alphabetically by Topic.
3. Add reverse cross-references: if the new file relates to existing KB files, add `[[new-file]]` to those files' `related` frontmatter, update their `## Related` body section to match, and update their `last-updated`.

#### If adding to Global Learnings:
1. Read `docs/kb/_global-learnings.md`. If it doesn't exist, create it with frontmatter (`tags: [global, cross-cutting]`, `pinned: true`, today's dates) and a `# Global Learnings` heading.
2. Append as a bullet point under `## Key Rules`.
3. Remove placeholder text if present ("_No global learnings captured yet..._").
4. Deduplicate against existing entries.
5. Update `last-updated` in frontmatter to today's date.
6. Ensure `_global-learnings.md` is registered in the CLAUDE.md Knowledge Base table as: `| Global Learnings | docs/kb/_global-learnings.md | Always (pinned) |`

### Step 6: Update Index and Log

1. **Update `docs/kb/_index.md`**: If this file exists, add or update the entry for the modified file with a one-line summary. Update `last-updated` in its frontmatter.
2. **Append to `docs/kb/_log.md`**: If this file exists, append:
   ```
   ## [YYYY-MM-DD] add | Quick add to {destination}
   - Added: "{brief learning text}"
   ```

### Step 7: Confirm

Display:
- What was saved and where
- The formatted entry as written
- Tags applied (if KB file)
- Cross-references added (if any)
