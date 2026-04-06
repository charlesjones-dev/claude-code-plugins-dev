---
name: kb-load
description: "Manually load one or more KB articles into the current conversation context. Accepts a filename, topic, or tag filter. Use when Claude hasn't automatically loaded a KB file you need."
disable-model-invocation: true
---

# Knowledge Base Manual Load

You are a knowledge base loading assistant. Your job is to load specific KB articles into the current conversation context when the user feels relevant knowledge wasn't automatically loaded. This is a quick, read-only operation — no files are modified.

## Instructions

### Step 1: Determine What to Load

Check if the user provided an argument after the command. Arguments can be:

- **Filename** (with or without path/extension): e.g., `/kb-load api-conventions` or `/kb-load docs/kb/conventions/api-conventions.md`
- **Topic name**: e.g., `/kb-load API Conventions` (matches against the Topic column in the CLAUDE.md table)
- **Tag filter**: e.g., `/kb-load tag:api` or `/kb-load tag:testing` (loads all KB files with the matching tag)
- **Multiple items**: e.g., `/kb-load api-conventions auth-patterns` (space-separated filenames)
- **`all`**: `/kb-load all` — loads every registered KB file (warn that this may use significant context)

**If no argument provided**: Proceed to Step 2 for interactive selection.

**If argument provided**: Skip to Step 3.

### Step 2: Interactive Selection (no argument)

1. **Read CLAUDE.md**: Parse the Knowledge Base table to get all registered entries.
2. **Read `docs/kb/_index.md`** if it exists for summaries.
3. **Present available KB files** using AskUserQuestion:

   - Header: "KB Load"
   - Question: Show the table of available KB files with their topics, tags (from frontmatter or index), and "When to Load" criteria. Ask: "Which KB file(s) would you like to load? Enter a topic name, filename, tag (e.g., `tag:api`), or number."
   - Number each entry for easy selection.
   - Allow free-text response.

### Step 3: Resolve Files

Based on the user's input, resolve to one or more file paths:

#### Filename match
1. If the input looks like a filename (contains no spaces, may have path segments):
   - Try exact path match first: `docs/kb/{input}`, `docs/kb/{input}.md`
   - Try recursive glob: `docs/kb/**/{input}.md`, `docs/kb/**/{input}`
   - If multiple matches, present them and ask the user to pick.
   - If no match, inform the user and suggest checking `/kb-list`.

#### Topic match
1. Read the CLAUDE.md Knowledge Base table.
2. Match the input (case-insensitive) against the Topic column.
3. If found, use the corresponding file path.
4. If no exact match, try partial/fuzzy matching and present candidates.

#### Tag filter
1. If input starts with `tag:`, extract the tag name.
2. Read all KB files under `docs/kb/` and parse their frontmatter `tags` arrays.
3. Collect all files that have the matching tag.
4. If no files match the tag, inform the user and suggest checking `/kb-search tag:{tag}`.

#### "all"
1. Read all registered files from the CLAUDE.md Knowledge Base table.
2. Warn: "Loading all {count} KB files. This may use significant context." Use AskUserQuestion:
   - Header: "KB Load All"
   - Question: "This will load {count} KB articles into context. Proceed?"
   - Options: "Load all" | "Cancel"

### Step 4: Load and Display

For each resolved file:

1. **Read the full file content** (frontmatter + body).
2. **Display the loading notification**: `📖 Loading KB: {filename}`
3. **Parse and internalize the content** — the knowledge is now available in this conversation.
4. **Check `related` cross-references**: If the file's frontmatter has `related: [[other-file]]` entries, inform the user:
   > "This article references related KB files: [[file1]], [[file2]]. Load them too?"
   
   Use AskUserQuestion:
   - Header: "Related KB Files"
   - Question: "Load related articles too?"
   - Options: "Load related" | "Skip"
   
   If "Load related", read and display those files with the same `📖 Loading KB:` notification.
   **Do not chain further** — only follow one level of related references to avoid loading the entire KB.

### Step 5: Summary

After loading all requested files, display a brief summary:

```
Loaded {count} KB article(s):
- {filename1} — {brief topic description from first heading}
- {filename2} — {brief topic description}

This knowledge is now available in the current conversation.
```

If any requested files were not found, list them:
```
Not found:
- {input} — no matching KB file. Check /kb-list for available files.
```
