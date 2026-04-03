---
name: kb-remove
description: "Remove a KB file and its CLAUDE.md reference. Accepts an optional file path or prompts the user to select which entry to remove."
disable-model-invocation: true
---

# Knowledge Base Remove

You are a knowledge base assistant. Your job is to cleanly remove a KB file and its corresponding CLAUDE.md reference table entry.

## Instructions

### Step 1: Determine Target

Check if the user provided a file path argument after the command (e.g., `/kb-remove docs/kb/old-topic.md`).

- **If a path was provided**: Use that path. Verify the file exists or at minimum has a CLAUDE.md table entry. If neither exists, inform the user and stop.
- **If no path was provided**: Proceed to selection mode.

#### Selection Mode

1. **Read CLAUDE.md**: Parse the Knowledge Base table to get all entries.
2. **If no Knowledge Base section exists**: Inform the user "No Knowledge Base section found. Nothing to remove." and stop.
3. **If no entries exist** (only placeholder row): Inform the user "No KB entries to remove." and stop.
4. Present the list of registered KB files and ask the user which to remove.

Use AskUserQuestion:
- Question: "Which KB entry would you like to remove?"
- Show the list of entries with their Topic, File, and When to Load
- Options: Each entry as a selectable option, plus "Cancel"
- Header: "KB Remove"

### Step 2: Confirm Removal

Show the user exactly what will happen. Use AskUserQuestion:
- Question: "This will remove the following. Confirm?"
- Show:
  - CLAUDE.md table row to be removed (Topic, File, When to Load)
  - Whether the KB file itself will be deleted (if it exists on disk)
  - Any other KB files that reference this file in their `related` frontmatter (these references will be cleaned up)
- Options: "Remove entry and delete file" | "Remove entry only (keep file)" | "Cancel"
- Header: "Confirm Removal"

If the file doesn't exist on disk, only show "Remove entry" and "Cancel".

### Step 3: Execute Removal

Based on user choice:

1. **Remove the CLAUDE.md table row** for this entry.
2. **Delete the KB file** from disk (only if user chose "Remove entry and delete file").
3. **Clean up cross-references**: For any other KB file that has this file in its `related` frontmatter, remove the reference and update `last-updated` to today's date.
4. If the table is now empty, restore the placeholder row: `| _No entries yet_ | - | _Run /kb-learn to capture learnings or /kb-add to register KB files_ |`
5. Re-sort the table alphabetically by Topic.

### Step 4: Confirm

Display:
- What was removed (table entry and/or file)
- Cross-references cleaned up (if any)
