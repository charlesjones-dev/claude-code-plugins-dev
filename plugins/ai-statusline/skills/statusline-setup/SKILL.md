---
name: statusline-setup
description: Guide for configuring Claude Code's status line with customizable display options and progress bars. This skill should be used when setting up or customizing the status line display.
---

# Status Line Setup Skill

This skill provides guidance for configuring Claude Code's status line with customizable display options, progress bars, and cross-platform support.

## When to Use This Skill

Invoke this skill when:
- Setting up a custom status line for Claude Code
- Configuring which elements to show/hide in the status line
- Adding a visual progress bar for context usage
- Setting up cross-platform status line scripts (bash/PowerShell)

## Setup Workflow

### Phase 1: Check Existing Configuration

1. Detect the operating system using Bash: `uname -s` (returns "Darwin" for macOS, "Linux" for Linux)
   - If command fails or returns "MINGW"/"MSYS"/"CYGWIN", assume Windows
2. Read the user's settings file:
   - **Mac/Linux**: `~/.claude/settings.json`
   - **Windows**: `C:/Users/USERNAME/.claude/settings.json` (get USERNAME from environment)
3. Check if `statusLine` section already exists
4. If exists, ask user using AskUserQuestion:
   - **Replace**: Back up existing file and create new configuration
   - **Cancel**: Stop the setup process

### Phase 2: Configuration Wizard

Use the AskUserQuestion tool to gather user preferences. Group questions logically:

**Question 1: Context Information**
- Show model name (default: yes)
- Show token count e.g. "50k/100k" (default: yes)
- Show progress bar (default: yes)

**Question 2: Project Information**
- Show current directory (default: yes)
- Show git branch (default: yes)

**Question 3: Session Information**
- Show session cost (default: no)
- Show session duration (default: yes)
- Show current time (default: yes)
- Show Claude Code version (default: yes)

### Phase 3: Create Script File

Based on OS, create the appropriate script file:

**Mac/Linux**: `~/.claude/statusline.sh`
**Windows**: `C:/Users/USERNAME/.claude/statusline.ps1`

If script file already exists, back it up first with `.backup` extension.

### Phase 4: Update Settings

Update the settings.json file with the statusLine configuration:

**Mac/Linux**:
```json
{
  "statusLine": {
    "type": "command",
    "command": "/Users/USERNAME/.claude/statusline.sh",
    "padding": 0
  }
}
```

**Windows**:
```json
{
  "statusLine": {
    "type": "command",
    "command": "powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:/Users/USERNAME/.claude/statusline.ps1",
    "padding": 0
  }
}
```

### Phase 5: Make Executable (Mac/Linux only)

Run `chmod +x ~/.claude/statusline.sh` to make the script executable.

## Script Templates

### Bash Script Template (Mac/Linux)

```bash
#!/bin/bash

# =============================================================================
# Claude Code Status Line
# =============================================================================
# Configuration - Set these to customize your status line
# =============================================================================

SHOW_MODEL=true           # Show model name (e.g., "Claude Opus 4.5")
SHOW_TOKEN_COUNT=true     # Show token usage count (e.g., "50k/100k")
SHOW_PROGRESS_BAR=true    # Show visual progress bar
SHOW_DIRECTORY=true       # Show current directory name
SHOW_GIT_BRANCH=true      # Show current git branch
SHOW_COST=false           # Show session cost (useful for API/Pro users)
SHOW_DURATION=true        # Show session duration
SHOW_TIME=true            # Show current time
SHOW_VERSION=true         # Show Claude Code version

# =============================================================================

input=$(cat)
model_name=$(echo "$input" | jq -r '.model.display_name')
current_dir=$(basename "$(echo "$input" | jq -r '.workspace.current_dir')")
version=$(echo "$input" | jq -r '.version')
usage=$(echo "$input" | jq '.context_window.current_usage')
cost=$(echo "$input" | jq -r '.cost.total_cost_usd')
duration_ms=$(echo "$input" | jq -r '.cost.total_duration_ms')
current_time=$(date +"%I:%M%p" | tr '[:upper:]' '[:lower:]')

# Format cost
if [ "$cost" != "null" ] && [ -n "$cost" ]; then
  cost_fmt=$(printf '$%.2f' "$cost")
else
  cost_fmt='$0.00'
fi

# Format duration (ms to human readable)
if [ "$duration_ms" != "null" ] && [ -n "$duration_ms" ]; then
  duration_s=$((duration_ms / 1000))
  if [ $duration_s -lt 60 ]; then
    duration_fmt="${duration_s}s"
  elif [ $duration_s -lt 3600 ]; then
    mins=$((duration_s / 60))
    secs=$((duration_s % 60))
    duration_fmt="${mins}m ${secs}s"
  else
    hours=$((duration_s / 3600))
    mins=$(((duration_s % 3600) / 60))
    duration_fmt="${hours}h ${mins}m"
  fi
else
  duration_fmt='0s'
fi

# Get git branch
git_branch=$(git -C "$(echo "$input" | jq -r '.workspace.current_dir')" branch --show-current 2>/dev/null)
if [ -z "$git_branch" ]; then
  git_branch='-'
fi

# Build progress bar
build_progress_bar() {
  local pct=$1
  local color=$2
  local bar_width=10
  local filled=$((pct * bar_width / 100))
  local empty=$((bar_width - filled))

  local bar=""
  for ((i=0; i<filled; i++)); do bar+="▓"; done
  for ((i=0; i<empty; i++)); do bar+="░"; done

  printf '\033[%sm%s %d%%\033[0m' "$color" "$bar" "$pct"
}

# ANSI color codes
reset='\033[0m'
white='\033[97m'
green='\033[32m'
yellow='\033[33m'
red='\033[31m'
blue='\033[94m'
magenta='\033[35m'
cyan='\033[36m'
gray='\033[90m'

# Build output segments
output=""

# Model name
if [ "$SHOW_MODEL" = true ]; then
  output="${white}${model_name}${reset}"
fi

# Token count and progress bar
if [ "$usage" != "null" ]; then
  current=$(echo "$usage" | jq '.input_tokens + .cache_creation_input_tokens + .cache_read_input_tokens')
  size=$(echo "$input" | jq '.context_window.context_window_size')
  pct=$((current * 100 / size))
  current_k=$((current / 1000))
  size_k=$((size / 1000))

  if [ $pct -lt 70 ]; then
    color='32'
  elif [ $pct -lt 80 ]; then
    color='33'
  else
    color='31'
  fi

  if [ "$SHOW_TOKEN_COUNT" = true ] || [ "$SHOW_PROGRESS_BAR" = true ]; then
    [ -n "$output" ] && output="$output · "

    if [ "$SHOW_TOKEN_COUNT" = true ]; then
      output="$output\033[${color}m${current_k}k/${size_k}k\033[0m"
    fi

    if [ "$SHOW_PROGRESS_BAR" = true ]; then
      progress_bar=$(build_progress_bar "$pct" "$color")
      [ "$SHOW_TOKEN_COUNT" = true ] && output="$output "
      output="$output${progress_bar}"
    fi
  fi
else
  if [ "$SHOW_TOKEN_COUNT" = true ] || [ "$SHOW_PROGRESS_BAR" = true ]; then
    [ -n "$output" ] && output="$output · "
    if [ "$SHOW_TOKEN_COUNT" = true ]; then
      output="$output${green}0k/0k${reset}"
    fi
    if [ "$SHOW_PROGRESS_BAR" = true ]; then
      progress_bar=$(build_progress_bar 0 '32')
      [ "$SHOW_TOKEN_COUNT" = true ] && output="$output "
      output="$output${progress_bar}"
    fi
  fi
fi

# Directory
if [ "$SHOW_DIRECTORY" = true ]; then
  [ -n "$output" ] && output="$output · "
  output="$output${blue}${current_dir}${reset}"
fi

# Git branch
if [ "$SHOW_GIT_BRANCH" = true ]; then
  [ -n "$output" ] && output="$output · "
  output="$output${magenta}${git_branch}${reset}"
fi

# Cost
if [ "$SHOW_COST" = true ]; then
  [ -n "$output" ] && output="$output · "
  output="$output${yellow}${cost_fmt}${reset}"
fi

# Duration
if [ "$SHOW_DURATION" = true ]; then
  [ -n "$output" ] && output="$output · "
  output="$output${cyan}${duration_fmt}${reset}"
fi

# Time
if [ "$SHOW_TIME" = true ]; then
  [ -n "$output" ] && output="$output · "
  output="$output${white}${current_time}${reset}"
fi

# Version
if [ "$SHOW_VERSION" = true ]; then
  [ -n "$output" ] && output="$output · "
  output="$output${gray}v${version}${reset}"
fi

printf '%b' "$output"
```

### PowerShell Script Template (Windows)

```powershell
# =============================================================================
# Claude Code Status Line (PowerShell)
# =============================================================================
# Configuration - Set these to customize your status line
# =============================================================================

$SHOW_MODEL = $true           # Show model name (e.g., "Claude Opus 4.5")
$SHOW_TOKEN_COUNT = $true     # Show token usage count (e.g., "50k/100k")
$SHOW_PROGRESS_BAR = $true    # Show visual progress bar
$SHOW_DIRECTORY = $true       # Show current directory name
$SHOW_GIT_BRANCH = $true      # Show current git branch
$SHOW_COST = $false           # Show session cost (useful for API/Pro users)
$SHOW_DURATION = $true        # Show session duration
$SHOW_TIME = $true            # Show current time
$SHOW_VERSION = $true         # Show Claude Code version

# =============================================================================

# Read JSON from stdin
$inputJson = $input | Out-String
$data = $inputJson | ConvertFrom-Json

$model_name = $data.model.display_name
$current_dir = Split-Path -Leaf $data.workspace.current_dir
$version = $data.version
$usage = $data.context_window.current_usage
$cost = $data.cost.total_cost_usd
$duration_ms = $data.cost.total_duration_ms
$current_time = (Get-Date -Format "h:mmtt").ToLower()

# Format cost
if ($null -ne $cost) {
    $cost_fmt = '${0:F2}' -f $cost
} else {
    $cost_fmt = '$0.00'
}

# Format duration (ms to human readable)
if ($null -ne $duration_ms) {
    $duration_s = [math]::Floor($duration_ms / 1000)
    if ($duration_s -lt 60) {
        $duration_fmt = "${duration_s}s"
    } elseif ($duration_s -lt 3600) {
        $mins = [math]::Floor($duration_s / 60)
        $secs = $duration_s % 60
        $duration_fmt = "${mins}m ${secs}s"
    } else {
        $hours = [math]::Floor($duration_s / 3600)
        $mins = [math]::Floor(($duration_s % 3600) / 60)
        $duration_fmt = "${hours}h ${mins}m"
    }
} else {
    $duration_fmt = '0s'
}

# Get git branch
$git_branch = try {
    git -C $data.workspace.current_dir branch --show-current 2>$null
} catch { $null }
if ([string]::IsNullOrEmpty($git_branch)) {
    $git_branch = '-'
}

# ANSI color codes
$esc = [char]27
$reset = "$esc[0m"
$white = "$esc[97m"
$cyan = "$esc[36m"
$green = "$esc[32m"
$yellow = "$esc[33m"
$red = "$esc[31m"
$blue = "$esc[94m"
$magenta = "$esc[35m"
$gray = "$esc[90m"

# Build progress bar
function Build-ProgressBar {
    param (
        [int]$Percent,
        [string]$Color
    )
    $bar_width = 10
    $filled = [math]::Floor($Percent * $bar_width / 100)
    $empty = $bar_width - $filled

    $bar = ("#" * $filled) + ("-" * $empty)
    return "$Color$bar $Percent%$reset"
}

# Build output segments
$segments = @()

# Model name
if ($SHOW_MODEL) {
    $segments += "$white$model_name$reset"
}

# Token count and progress bar
if ($null -ne $usage) {
    $current = $usage.input_tokens + $usage.cache_creation_input_tokens + $usage.cache_read_input_tokens
    $size = $data.context_window.context_window_size
    $pct = [math]::Floor($current * 100 / $size)
    $current_k = [math]::Floor($current / 1000)
    $size_k = [math]::Floor($size / 1000)

    if ($pct -lt 70) {
        $token_color = $green
    } elseif ($pct -lt 80) {
        $token_color = $yellow
    } else {
        $token_color = $red
    }

    $token_segment = ""
    if ($SHOW_TOKEN_COUNT) {
        $token_segment = "$token_color${current_k}k/${size_k}k$reset"
    }
    if ($SHOW_PROGRESS_BAR) {
        $progress_bar = Build-ProgressBar -Percent $pct -Color $token_color
        if ($SHOW_TOKEN_COUNT) {
            $token_segment += " $progress_bar"
        } else {
            $token_segment = $progress_bar
        }
    }
    if ($token_segment) {
        $segments += $token_segment
    }
} else {
    $token_segment = ""
    if ($SHOW_TOKEN_COUNT) {
        $token_segment = "${green}0k/0k$reset"
    }
    if ($SHOW_PROGRESS_BAR) {
        $progress_bar = Build-ProgressBar -Percent 0 -Color $green
        if ($SHOW_TOKEN_COUNT) {
            $token_segment += " $progress_bar"
        } else {
            $token_segment = $progress_bar
        }
    }
    if ($token_segment) {
        $segments += $token_segment
    }
}

# Directory
if ($SHOW_DIRECTORY) {
    $segments += "$blue$current_dir$reset"
}

# Git branch
if ($SHOW_GIT_BRANCH) {
    $segments += "$magenta$git_branch$reset"
}

# Cost
if ($SHOW_COST) {
    $segments += "$yellow$cost_fmt$reset"
}

# Duration
if ($SHOW_DURATION) {
    $segments += "$cyan$duration_fmt$reset"
}

# Time
if ($SHOW_TIME) {
    $segments += "$white$current_time$reset"
}

# Version
if ($SHOW_VERSION) {
    $segments += "${gray}v$version$reset"
}

Write-Host -NoNewline ($segments -join " - ")
```

## Configuration Variables

| Variable | Default | Description |
|----------|---------|-------------|
| SHOW_MODEL | true | Display model name (e.g., "Claude Opus 4.5") |
| SHOW_TOKEN_COUNT | true | Display token usage (e.g., "50k/100k") |
| SHOW_PROGRESS_BAR | true | Display visual progress bar with percentage |
| SHOW_DIRECTORY | true | Display current working directory name |
| SHOW_GIT_BRANCH | true | Display current git branch |
| SHOW_COST | false | Display session cost in USD |
| SHOW_DURATION | true | Display session duration |
| SHOW_TIME | true | Display current time |
| SHOW_VERSION | true | Display Claude Code version |

## Important Notes

- The scripts require `jq` to be installed on Mac/Linux for JSON parsing
- PowerShell scripts work on Windows PowerShell 5.1+ and PowerShell Core 7+
- Unicode progress bar characters (▓░) should work on modern terminals
- Colors use ANSI escape codes which work on most modern terminals
- Status line updates appear immediately after setup
