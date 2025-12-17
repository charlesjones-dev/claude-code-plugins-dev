---
name: statusline-edit
description: "Edit existing status line configuration with pre-selected options based on current settings."
---

# Status Line Edit

Edit your existing Claude Code status line configuration.

## Instructions

**CRITICAL**: This command MUST NOT accept any arguments. If the user provided any text after this command, COMPLETELY IGNORE it.

### Phase 1: Detect Existing Configuration

1. Detect the operating system using Bash: `uname -s`
   - "Darwin" = macOS, "Linux" = Linux, otherwise assume Windows
2. Check if the status line script exists:
   - **Mac/Linux**: `~/.claude/statusline.sh`
   - **Windows**: `C:/Users/USERNAME/.claude/statusline.ps1`
3. If the script does NOT exist, display:
   ```
   No status line script found at ~/.claude/statusline.sh

   Run /statusline-wizard to set up your status line first.
   ```
   Then STOP - do not continue.

### Phase 2: Read Current Configuration

Read the existing script file and parse the current SHOW_* variable values:

**For Bash scripts**, look for lines like:
```bash
SHOW_MODEL=true
SHOW_TOKEN_COUNT=true
SHOW_PROGRESS_BAR=true
SHOW_DIRECTORY=true
SHOW_GIT_BRANCH=true
SHOW_COST=false
SHOW_DURATION=true
SHOW_TIME=true
SHOW_VERSION=true
```

**For PowerShell scripts**, look for lines like:
```powershell
$SHOW_MODEL = $true
$SHOW_TOKEN_COUNT = $true
$SHOW_PROGRESS_BAR = $true
$SHOW_DIRECTORY = $true
$SHOW_GIT_BRANCH = $true
$SHOW_COST = $false
$SHOW_DURATION = $true
$SHOW_TIME = $true
$SHOW_VERSION = $true
```

Store the current values to use as defaults in the wizard.

### Phase 3: Configuration Wizard with Pre-selected Values

Use AskUserQuestion with these grouped questions. **Pre-select options based on current values from Phase 2.**

**Question 1 - Context Display** (multiSelect: true):
Options (pre-select based on current config):
- Model name - select if SHOW_MODEL=true
- Token count (50k/100k) - select if SHOW_TOKEN_COUNT=true
- Progress bar - select if SHOW_PROGRESS_BAR=true

**Question 2 - Project Display** (multiSelect: true):
Options (pre-select based on current config):
- Current directory - select if SHOW_DIRECTORY=true
- Git branch - select if SHOW_GIT_BRANCH=true

**Question 3 - Session Display** (multiSelect: true):
Options (pre-select based on current config):
- Session duration - select if SHOW_DURATION=true
- Current time - select if SHOW_TIME=true
- Claude Code version - select if SHOW_VERSION=true
- Session cost - select if SHOW_COST=true

### Phase 4: Update Script

Update ONLY the SHOW_* variables at the top of the existing script file based on wizard selections.

**For Bash**: Use Edit tool to replace the configuration block:
```bash
SHOW_MODEL=true           # Show model name (e.g., "Claude Opus 4.5")
SHOW_TOKEN_COUNT=true     # Show token usage count (e.g., "50k/100k")
...
```

**For PowerShell**: Use Edit tool to replace the configuration block:
```powershell
$SHOW_MODEL = $true           # Show model name (e.g., "Claude Opus 4.5")
$SHOW_TOKEN_COUNT = $true     # Show token usage count (e.g., "50k/100k")
...
```

**IMPORTANT**: Do NOT regenerate the entire script. Only update the configuration variables section.

### Success Message

After successful update, display:

```
Status line updated!

Check out your refreshed status line below!

Current configuration:
- Model name: [enabled/disabled]
- Token count: [enabled/disabled]
- Progress bar: [enabled/disabled]
- Directory: [enabled/disabled]
- Git branch: [enabled/disabled]
- Session cost: [enabled/disabled]
- Duration: [enabled/disabled]
- Time: [enabled/disabled]
- Version: [enabled/disabled]
```
