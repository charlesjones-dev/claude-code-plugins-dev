# AI-Statusline Plugin

**AI-powered status line customization for Claude Code.** Interactive setup and edit wizards for configuring a custom status line with progress bars and customizable display options.

> **How this relates to the native `/statusline` command:** Claude Code ships a built-in `/statusline` command that covers baseline setup (describe what you want, or auto-configure from your shell prompt). This plugin goes further with richer, opinionated widgets: a Unicode progress bar with color thresholds, 5-hour/7-day rate-limit percentages with color coding, a month-to-date spend budget for Enterprise/API seats that have no rate limits, a reasoning-effort indicator with `/effort`-matched colors (including ultracode detection), session cost and duration segments, granular per-segment toggles, and a matching `/statusline-edit` flow for reconfiguring later without regenerating the script.

---

## What This Plugin Does

Provides interactive commands to configure Claude Code's status line with visual elements like progress bars, token counts, git branch info, and more. The plugin generates cross-platform scripts (Bash for Mac/Linux, PowerShell for Windows) that dynamically display real-time session information.

### Example Status Line

```
Claude Opus 4.8 · high · 42k/100k ▓▓▓▓░░░░░░ 42% · 5h:12% 7d:4% · my-project · main · 5m 23s · 2:45pm · v2.1.80
```

On an Enterprise or API seat with a monthly spend cap (no 5h/7d rate limits), with the optional spend budget enabled:

```
Opus 5 (1M context) · high · 71k/1000k ░░░░░░░░░░ 7% · mo:$47.20/$2000 2.4% · my-project · main · 7m 48s · 4:52pm · v2.1.267
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
   - Model name (e.g., "Claude Opus 4.8")
   - Effort level (e.g., "high", with `/effort`-matched colors)

2. **Project Display** (what to show about your project)
   - Current directory name
   - Git branch name

3. **Session Display** (what to show about timing/costs)
   - Session duration
   - Current time
   - Claude Code version
   - Session cost (disabled by default)

4. **Usage Limits** (how close you are to your plan's limits)
   - Rate limit usage - 5h and 7d windows (Pro/Max plans)
   - Monthly spend budget - month-to-date spend across sessions on this machine (disabled by default; prompts for your monthly cap in USD and when it resets)

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
| Model name | On | Display model name (e.g., "Claude Opus 4.8") |
| Effort level | On | Display reasoning effort level with `/effort`-matched colors |
| Token count | On | Display token usage (e.g., "50k/100k") |
| Progress bar | On | Display visual progress bar with percentage |
| Current directory | On | Display current working directory name |
| Git branch | On | Display current git branch |
| Session duration | On | Display how long the session has been running |
| Current time | On | Display current time |
| Claude Code version | On | Display Claude Code version number |
| Session cost | Off | Display session cost in USD |
| Rate limit usage | On | Display 5-hour and 7-day rate limit percentages (hidden on accounts without rolling windows) |
| Monthly spend budget | Off | Display month-to-date spend across all sessions on this machine, e.g. `mo:$47.20/$2000 2.4%` |
| Monthly spend cap | 0 (none) | USD cap used for the spend budget percentage and colors; `0` shows the bare total |
| Spend cap reset | 1st, 00:00 UTC | Day of month (1-28) and time (UTC) the cap resets; the wizard converts what the console shows into UTC |

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

### Rate Limit Display

Shows your 5-hour and 7-day rate limit usage with color coding:

```
5h:12% 7d:4%    (Green - under 50%)
5h:65% 7d:42%   (Yellow - 50-79%)
5h:92% 7d:85%   (Red - 80%+)
```

Color changes automatically so you can see at a glance how close you are to either rate-limit window.

**Not on every plan:** Claude Code only sends `rate_limits` for plans with rolling usage windows (Pro/Max). Enterprise seats and API-billed accounts on a monthly spend cap receive no rate-limit data at all, so this segment stays hidden even when enabled. Use the Monthly Spend Budget segment below instead.

### Monthly Spend Budget

For accounts with no rolling rate limits, the optional spend segment shows month-to-date spend across all Claude Code sessions on this machine, colored on the same thresholds as the rate-limit segment:

```
mo:$47.20/$2000 2.4%    (Green - under 50% of cap)
mo:$1240.00/$2000 62.0% (Yellow - 50-79%)
mo:$1700.00/$2000 85.0% (Red - 80%+)
mo:$47.20               (No cap configured - bare total)
```

Enable it with `SHOW_SPEND_BUDGET=true` and set `SPEND_LIMIT_USD` to your seat's monthly cap (the "$0.96 of $2,000.00 spent" figure on the Anthropic console usage page). Leave the cap at `0` to show the bare total.

**Reset day and time:** the payload doesn't tell us when your cap resets, so you provide it. `SPEND_RESET_DAY` (1-28) and `SPEND_RESET_TIME` (HH:MM, 24-hour) are both in UTC and default to the 1st at 00:00 UTC, which is what the Anthropic console uses. The console shows that same instant in your local time ("Resets Wed, Sep 30, 8:00 PM EDT" is Oct 1 00:00 UTC), and the wizard does the conversion when you paste it. Invalid values fall back to the default rather than breaking the status line.

**How it works:** Claude Code only reports the current session's cost, so each render writes it to `~/.claude/statusline-spend/<period-start>/<session_id>` and the segment sums every file for the current billing period, where the period starts at the most recent reset day/time. One file per session means concurrent sessions never contend for a shared file. Previous periods are pruned automatically. If the directory can't be created or written (read-only home, missing `HOME`), the segment silently falls back to the current session's cost.

**Caveats to know before relying on it:**

- **It is a local estimate, not your bill.** The figure is Claude Code's own `cost.total_cost_usd` estimate and will not match the Anthropic console (in one observed case the console showed $0.96 spent while a single live session already reported $1.11). The authoritative sources are the console usage page and the Admin API cost report, which needs an org admin key most seat users don't have.
- **No historical backfill.** Only sessions rendered after you enable the segment are counted.
- **This machine only.** It doesn't include claude.ai web/desktop usage or sessions on other machines.

### Effort Level Display

Shows the session's reasoning effort level, colored to match Claude Code's `/effort` picker:

| Level | Color |
|-------|-------|
| `low` | Yellow |
| `medium` | Green |
| `high` | Light purple |
| `xhigh` | Dark purple |
| `max` | Per-character rainbow |
| `ultracode` | Purple explosion (`✦ultracode✦`, cycling purple shades) |

The segment reflects live `/effort` changes and is hidden entirely when the current model doesn't support the effort parameter.

**Ultracode detection:** Claude Code reports ultracode as plain `xhigh` in the status line payload, so the scripts scan the session transcript for the most recent `/effort` command output to tell them apart. If a session never ran `/effort`, the payload value is shown as-is.

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
SHOW_EFFORT=true          # Show reasoning effort level
SHOW_TOKEN_COUNT=true     # Show token usage count
SHOW_PROGRESS_BAR=true    # Show visual progress bar
SHOW_DIRECTORY=true       # Show current directory name
SHOW_GIT_BRANCH=true      # Show current git branch
SHOW_COST=false           # Show session cost
SHOW_DURATION=true        # Show session duration
SHOW_TIME=true            # Show current time
SHOW_VERSION=true         # Show Claude Code version
SHOW_RATE_LIMITS=true     # Show rate limit usage (5h/7d windows)
SHOW_SPEND_BUDGET=false   # Show month-to-date spend across sessions on this machine
SPEND_LIMIT_USD=0         # Monthly spend cap in USD (0 = no cap, show bare total)
SPEND_RESET_DAY=1         # Day of the month (1-28) the cap resets, UTC
SPEND_RESET_TIME=00:00    # Time (HH:MM, 24h, UTC) the cap resets
```

**PowerShell (`~/.claude/statusline.ps1`):**
```powershell
$SHOW_MODEL = $true
$SHOW_EFFORT = $true
$SHOW_TOKEN_COUNT = $true
$SHOW_PROGRESS_BAR = $true
$SHOW_DIRECTORY = $true
$SHOW_GIT_BRANCH = $true
$SHOW_COST = $false
$SHOW_DURATION = $true
$SHOW_TIME = $true
$SHOW_VERSION = $true
$SHOW_RATE_LIMITS = $true
$SHOW_SPEND_BUDGET = $false
$SPEND_LIMIT_USD = 0
$SPEND_RESET_DAY = 1
$SPEND_RESET_TIME = '00:00'
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

### Rate limits (5h/7d) never appear

Your account has no rolling rate-limit windows, so Claude Code doesn't send `rate_limits` in the status line payload. This is expected for Enterprise seats and API-billed accounts on a monthly spend cap. Enable the Monthly Spend Budget segment (`SHOW_SPEND_BUDGET=true`) for a comparable month-to-date view.

### Spend budget only shows the current session

The script couldn't write to `~/.claude/statusline-spend/` (read-only home directory or `HOME` not set), so it fell back to the current session's cost. Make that directory writable to restore cross-session totals.

---

## Plugin Details

- **Name:** AI-Statusline
- **Version:** 1.4.0
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
