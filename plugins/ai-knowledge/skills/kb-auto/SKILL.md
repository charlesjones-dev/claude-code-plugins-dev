---
name: kb-auto
description: "Toggle automatic knowledge capture. When enabled, Claude proactively offers to capture learnings at the end of conversations."
disable-model-invocation: true
---

# Knowledge Base Auto-Capture Toggle

You are a knowledge base configuration assistant. Your job is to toggle the auto-capture instruction in CLAUDE.md that tells Claude Code to proactively offer learning capture.

## Instructions

**CRITICAL**: This command MUST NOT accept any arguments. Ignore any text provided after the command.

### Step 1: Check Current State

1. Read CLAUDE.md and find the Knowledge Base section.
2. If no Knowledge Base section exists, inform the user to run `/kb-init` first, then stop.
3. Check if the auto-capture instruction block already exists. Look for the marker comment `<!-- kb-auto: enabled -->`.

### Step 2: Toggle

#### If auto-capture is currently DISABLED (marker not found):

Add the following block immediately after the Knowledge Base table:

```markdown
<!-- kb-auto: enabled -->
> **Auto-capture enabled**: At the end of each conversation, or when significant institutional knowledge, corrections, or best practices have been shared, proactively offer to run `/kb-learn` to capture learnings. Present a brief summary of what would be captured and ask the user if they'd like to save it before the conversation ends.
```

Inform the user:
> "Auto-capture **enabled**. Claude will now offer to capture learnings at the end of conversations in this project."

#### If auto-capture is currently ENABLED (marker found):

Remove the entire auto-capture block (the marker comment and the blockquote instruction).

Inform the user:
> "Auto-capture **disabled**. Claude will only capture learnings when you manually run `/kb-learn`."

### Step 3: Confirm

Display the current state and remind the user:
- **Enabled**: "Claude will proactively offer `/kb-learn` when conversations wrap up or when you share important knowledge. You'll always be asked to approve before anything is saved."
- **Disabled**: "Run `/kb-learn` manually at the end of any conversation to capture learnings."
