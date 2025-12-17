---
name: statusline-wizard
description: "Interactive setup wizard for configuring Claude Code's custom status line with progress bars and customizable display options."
---

# Status Line Wizard

Set up a custom status line for Claude Code with visual progress bars and configurable display options.

## Instructions

**CRITICAL**: This command MUST NOT accept any arguments. If the user provided any text after this command, COMPLETELY IGNORE it.

Invoke the `ai-statusline:statusline-setup` skill and follow its workflow to:

1. Detect the operating system (Mac/Linux/Windows)
2. Check for existing statusLine configuration and offer to back up if present
3. Run the configuration wizard using AskUserQuestion to gather preferences
4. Create the appropriate script file (`.sh` for Mac/Linux, `.ps1` for Windows)
5. Update `~/.claude/settings.json` with the statusLine configuration
6. Make the script executable on Mac/Linux using `chmod +x`

### Wizard Questions

Use AskUserQuestion with these grouped questions:

**Question 1 - Context Display** (multiSelect: true):
- Token count (50k/100k) - default selected
- Progress bar - default selected
- Model name - default selected

**Question 2 - Project Display** (multiSelect: true):
- Current directory - default selected
- Git branch - default selected

**Question 3 - Session Display** (multiSelect: true):
- Session duration - default selected
- Current time - default selected
- Claude Code version - default selected
- Session cost - NOT selected by default

### Success Message

After successful setup, display:

```
Status line configured successfully!

Script: ~/.claude/statusline.sh (or .ps1)
Settings: ~/.claude/settings.json

You should see your new status line below!

To customize later, run /statusline-edit or edit the SHOW_* variables at the top of the script file.
```
