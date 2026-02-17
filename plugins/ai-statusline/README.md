# AI-Statusline Plugin

**AI-powered status line customization for Claude Code.** Interactive setup and edit wizards for configuring a custom status line with progress bars and customizable display options.

---

## What This Plugin Does

Provides interactive commands to configure Claude Code's status line with visual elements like progress bars, token counts, git branch info, and more. The plugin generates cross-platform scripts (Bash for Mac/Linux, PowerShell for Windows) that dynamically display real-time session information.

### Example Status Line

```
Claude Opus 4.5 · 42k/100k ▓▓▓▓░░░░░░ 42% · my-project · main · 5m 23s · 2:45pm · v1.0.24
```

---

## Available Skills

### `/statusline-wizard`

Interactive setup wizard for configuring Claude Code's custom status line from scratch.

**What it does:**

- Detects your operating system (Mac/Linux/Windows)
- Checks for existing configuration and offers to back up if present
- Runs an interactive wizard using grouped questions
- Creates the appropriate script file (`statusline.sh` or `statusline.ps1`)
- Updates `~/.claude/settings.json` with the statusLine configuration
- Makes the script executable on Mac/Linux

**Usage:**

```
/statusline-wizard
```

**Wizard Questions:**

The wizard asks about three categories of display options:

1. **Context Display** (what to show about your Claude session)
   - Token count (e.g., "50k/100k")
   - Progress bar (visual percentage indicator)
   - Model name (e.g., "Claude Opus 4.5")

2. **Project Display** (what to show about your project)
   - Current directory name
   - Git branch name

3. **Session Display** (what to show about timing/costs)
   - Session duration
   - Current time
   - Claude Code version
   - Session cost (disabled by default)

### `/statusline-edit`

Edit your existing status line configuration.

**What it does:**

- Detects your OS and locates the existing script file
- Reads current configuration values from the script
- Presents the same questions as wizard command
- Updates only the configuration variables (preserves the rest of the script)

**Usage:**

```
/statusline-edit
```

**Note:** If no status line script exists, you'll be prompted to run `/statusline-wizard` first.

---

## Quick Start

### Installation

```
/plugin install ai-statusline@claude-code-plugins-dev
```

### Usage

```
# Step 1: Run the setup wizard
/statusline-wizard

# Step 2: Answer the interactive questions
# Select which elements you want displayed

# Step 3: Your new status line appears immediately!

# Later: Edit your configuration
/statusline-edit
```

---

## Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| Model name | On | Display model name (e.g., "Claude Opus 4.5") |
| Token count | On | Display token usage (e.g., "50k/100k") |
| Progress bar | On | Display visual progress bar with percentage |
| Current directory | On | Display current working directory name |
| Git branch | On | Display current git branch |
| Session duration | On | Display how long the session has been running |
| Current time | On | Display current time |
| Claude Code version | On | Display Claude Code version number |
| Session cost | Off | Display session cost in USD |

---

## Features

### Visual Progress Bar

The progress bar uses Unicode block characters to show context usage:

```
▓▓▓▓░░░░░░ 42%  (Green - under 70%)
▓▓▓▓▓▓▓░░░ 74%  (Yellow - 70-79%)
▓▓▓▓▓▓▓▓░░ 85%  (Red - 80%+)
```

Color changes automatically based on usage level to help you monitor context consumption.

### Cross-Platform Support

- **Mac/Linux**: Generates `~/.claude/statusline.sh` (Bash script)
- **Windows**: Generates `~/.claude/statusline.ps1` (PowerShell script)

Both scripts are automatically configured in your `~/.claude/settings.json`.

### Smart Configuration

- **Backup existing configs**: Automatically backs up existing scripts before overwriting
- **Pre-selected defaults**: Edit command shows your current configuration
- **Minimal updates**: Edit command only modifies configuration variables, preserving any customizations

### Real-Time Information

The status line displays live data from Claude Code including:

- Current context window usage (input tokens + cache tokens)
- Context window size
- Session cost tracking
- Session duration in human-readable format (5s, 3m 45s, 1h 23m)
- Current git branch (with fallback to '-' if not in a repo)

---

## How It Works

1. **Script Generation**: The wizard creates a shell script that reads JSON input from stdin (provided by Claude Code)

2. **JSON Parsing**:
   - Mac/Linux: Uses `jq` to parse the JSON data
   - Windows: Uses PowerShell's `ConvertFrom-Json`

3. **Dynamic Output**: The script builds output segments based on enabled options, joining them with separators

4. **ANSI Colors**: Uses standard ANSI escape codes for cross-terminal color support

### Script Location

| OS | Script Path | Settings Path |
|----|-------------|---------------|
| Mac/Linux | `~/.claude/statusline.sh` | `~/.claude/settings.json` |
| Windows | `C:/Users/USERNAME/.claude/statusline.ps1` | `C:/Users/USERNAME/.claude/settings.json` |

---

## Requirements

### Mac/Linux

- **jq**: Required for JSON parsing
  ```bash
  # macOS
  brew install jq

  # Ubuntu/Debian
  sudo apt install jq

  # Fedora
  sudo dnf install jq
  ```

### Windows

- PowerShell 5.1+ (included with Windows 10/11) or PowerShell Core 7+
- No additional dependencies required

### Terminal Support

- Unicode support for progress bar characters (`▓` and `░`)
- ANSI color code support (most modern terminals)

---

## Customization

### Manual Configuration

After running the wizard, you can manually edit the configuration variables at the top of the script file:

**Bash (`~/.claude/statusline.sh`):**
```bash
SHOW_MODEL=true           # Show model name
SHOW_TOKEN_COUNT=true     # Show token usage count
SHOW_PROGRESS_BAR=true    # Show visual progress bar
SHOW_DIRECTORY=true       # Show current directory name
SHOW_GIT_BRANCH=true      # Show current git branch
SHOW_COST=false           # Show session cost
SHOW_DURATION=true        # Show session duration
SHOW_TIME=true            # Show current time
SHOW_VERSION=true         # Show Claude Code version
```

**PowerShell (`~/.claude/statusline.ps1`):**
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

---

## Troubleshooting

### Status line not appearing

1. Verify the script exists at the expected location
2. Check that `~/.claude/settings.json` contains the `statusLine` configuration
3. Restart Claude Code after making changes

### Colors not displaying

- Ensure your terminal supports ANSI escape codes
- Try a different terminal emulator if colors don't appear

### Progress bar characters look wrong

- Ensure your terminal font supports Unicode block characters
- Try a font like "Fira Code", "JetBrains Mono", or "Cascadia Code"

### jq not found (Mac/Linux)

Install jq using your package manager (see Requirements section above).

---

## Plugin Details

- **Name:** AI-Statusline
- **Version:** 1.2.1
- **Type:** UI Customization
- **Features:**
  - Skills: `/statusline-wizard`, `/statusline-edit`
- **License:** MIT
- **Author:** Charles Jones

---

## Contributing

Found a bug or have a suggestion? [Open an issue](https://github.com/charlesjones-dev/claude-code-plugins-dev/issues) or submit a pull request!

---

## License

MIT License - See [LICENSE](LICENSE) file for details.

---

**Built for the Claude Code community**
