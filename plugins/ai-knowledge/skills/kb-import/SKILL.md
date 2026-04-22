---
name: kb-import
description: "Register a KB file in CLAUDE.md's Knowledge Base table. Accepts a file path argument, or scans docs/kb/ for unregistered files. Adds missing frontmatter."
disable-model-invocation: true
---

# Knowledge Base File Registration

You are a knowledge base registration assistant. Your job is to register KB files in CLAUDE.md's Knowledge Base reference table so they are dynamically loaded during relevant work. You also ensure all registered files have valid frontmatter.

## Frontmatter Schema

Every KB file MUST have valid YAML frontmatter. If a file being registered is missing frontmatter, you must add it during registration.

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

**Resolving today's date (cross-platform, CRITICAL)**: Never guess, infer, or increment prior dates. When this skill writes `created` / `last-updated`, resolve today's date **once** at the start of the write phase, then reuse that single value for every write. Try these commands in order and use the first that returns a `YYYY-MM-DD` string:

- **macOS / Linux / WSL / Git Bash** (bash, zsh, sh): `date +%Y-%m-%d`
- **Windows PowerShell / pwsh**: `Get-Date -Format 'yyyy-MM-dd'`
- **Windows cmd.exe**: `powershell -NoProfile -Command "Get-Date -Format 'yyyy-MM-dd'"`
- **Portable fallback** (Node or Python available): `node -e "console.log(new Date().toISOString().slice(0,10))"` or `python -c "import datetime; print(datetime.date.today().isoformat())"`

Only update `last-updated` when the file's content actually changed. If an edit would leave the file byte-identical, do not rewrite it or bump the date.

## Obsidian-Compatible Related Links

When a KB file has `related` entries in its frontmatter, it MUST also have a `## Related` section at the **end** of the file body with the same references as `[[wiki-links]]`. When fixing frontmatter, also check for and add this body section if `related` is non-empty. Always keep both in sync.

## Instructions

### Step 1: Determine Mode

Check if the user provided a file path argument after the command (e.g., `/kb-import docs/kb/api-conventions.md`).

- **If a path was provided**: Use that path. Verify the file exists. If it doesn't exist, inform the user and stop.
- **If no path was provided**: Scan mode - proceed to Step 2.

### Step 2: Scan for Unregistered Files (scan mode only)

1. **Read CLAUDE.md**: Parse the Knowledge Base table to get all currently registered file paths.
2. **Glob for KB files**: Find all `.md` files under `docs/kb/` (excluding `docs/kb/README.md`).
3. **Diff**: Identify files that exist in `docs/kb/` but are NOT in the CLAUDE.md table.
4. **If no unregistered files found**: Inform the user "All KB files are already registered in CLAUDE.md." and stop.
5. **If unregistered files found**: Present the list and ask the user which to register.

Use AskUserQuestion:
- Question: "I found these unregistered KB files. Which should I add to CLAUDE.md?"
- Show the list of unregistered files
- Options: "Register all" | "Let me pick" | "Cancel"
- Header: "Unregistered KB Files"

If "Let me pick", ask about each file individually.

### Step 3: Validate and Fix Frontmatter

For each file to register:

1. **Read the KB file** and check if it has valid YAML frontmatter.
2. **If frontmatter is missing entirely**: Add complete frontmatter based on the file content:
   - Infer `tags` from the file content and file path
   - Set `created` and `last-updated` to today's date (resolved once via the cross-platform command in the Frontmatter Schema section)
   - Set `pinned` to `false`
   - Infer `scope` from file path and content if possible
   - Leave `related` empty initially
3. **If frontmatter exists but is incomplete**: Add missing required fields with inferred values.
4. **If frontmatter is valid**: No changes needed.
5. Inform the user of any frontmatter additions/changes made.

### Step 4: Gather Registration Details

For each file to register, determine the Topic and "When to Load" context:

1. **Infer the Topic**: Use the file name, frontmatter tags, and content to suggest a topic name.
2. **Build the "When to Load" value** using the structured format:
   - If `pinned: true`, use `Always (pinned)`.
   - Otherwise, extract scope patterns from the `scope` frontmatter field (handle both string and array forms). Extract keywords from the `tags` frontmatter field.
   - Format as: `` `scope-glob1`, `scope-glob2` — tag1, tag2 ``
   - If the file has no `scope`, try to infer scope patterns from the file content and path. If none can be inferred, use keywords only: `— tag1, tag2`.
   - If the file has no `tags`, use scope patterns only: `` `scope-glob1` ``

Present the inferred details and ask the user to confirm or adjust:

Use AskUserQuestion:
- Question: "I'll register this file with the following details. Look correct?"
- Show: Topic, File path, When to Load, Tags, Pinned status
- Options: "Looks good" | "Let me adjust" | "Skip this file"
- Header: "Register: {filename}"

If "Let me adjust", ask a free-text follow-up for corrections.

### Step 5: Update CLAUDE.md

1. **Read CLAUDE.md** and find the Knowledge Base table.
2. **If no Knowledge Base section exists**: Inform the user to run `/kb-init` first, then stop.
3. **Remove placeholder row** if present ("_No entries yet_").
4. **Add new row(s)** to the table with the confirmed Topic, File path, and When to Load.
5. **Deduplicate**: If a row for the same file already exists, update it rather than adding a duplicate.
6. **Sort the table** alphabetically by Topic.

### Step 6: Update Index and Log

1. **Update `docs/kb/_index.md`**: If this file exists, add entries for newly registered files with one-line summaries. Update `last-updated` in its frontmatter.
2. **Append to `docs/kb/_log.md`**: If this file exists, append:
   ```
   ## [YYYY-MM-DD] import | Registered {count} KB files
   - Registered: {list of files}
   - Frontmatter fixes: {count}
   ```

### Step 7: Confirm

Display what was registered:
- File(s) added to the Knowledge Base table
- Frontmatter additions/fixes applied
- Reminder that Claude Code will now consult these files when working in the matching context
