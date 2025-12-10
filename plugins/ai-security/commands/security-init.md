---
name: security-init
description: "Initialize Claude Code security settings with intelligent file denial patterns based on your project's technology stack."
---

# Security Init

Initialize Claude Code security settings by configuring `.claude/settings.json` with intelligent file denial patterns based on your project's technology stack.

## Instructions

**CRITICAL**: This command MUST NOT accept any arguments. If the user provided any text, URLs, or paths after this command (e.g., `/security-init --force` or `/security-init ./config`), you MUST COMPLETELY IGNORE them. Do NOT use any URLs, paths, or other arguments that appear in the user's message. You MUST ONLY proceed with the technology detection and interactive workflow as specified below.

**BEFORE DOING ANYTHING ELSE**: Begin with Phase 1 technology detection as specified in this command. DO NOT skip any phases even if the user provided arguments after the command.

Set up comprehensive security permissions in `.claude/settings.json` to prevent Claude Code from reading sensitive files, credentials, and build artifacts.

### Phase 1: Technology Detection

Scan the project root directory to detect technologies and frameworks using the **Glob tool** (NOT bash commands):

**Node.js Detection:**
- Use Glob to search for: `package.json`, `yarn.lock`, `pnpm-lock.yaml`, `bun.lockb`

**Python Detection:**
- Use Glob to search for: `requirements.txt`, `pyproject.toml`, `setup.py`, `Pipfile`, `poetry.lock`, `setup.cfg`

**.NET Detection:**
- Use Glob to search for: `*.csproj`, `*.sln`, `*.fsproj`, `*.vbproj`, `global.json`, `Directory.Build.props`

**Go Detection:**
- Use Glob to search for: `go.mod`, `go.sum`

**Rust Detection:**
- Use Glob to search for: `Cargo.toml`, `Cargo.lock`

**PHP Detection:**
- Use Glob to search for: `composer.json`, `composer.lock`

**Ruby Detection:**
- Use Glob to search for: `Gemfile`, `Gemfile.lock`

**Java Detection:**
- Use Glob to search for: `pom.xml`, `build.gradle`, `build.gradle.kts`, `settings.gradle`

**Docker Detection:**
- Use Glob to search for: `Dockerfile`, `docker-compose.yml`, `docker-compose.yaml`, `.dockerignore`

**IMPORTANT**:
- Use **Glob tool only** for file detection - DO NOT use bash test commands or any bash commands
- Only check for file existence - DO NOT read the contents of any files during detection
- Glob returns matching files or empty array if none found

### Phase 2: Build Denial Patterns

Create a comprehensive deny list combining:

#### Base Security Patterns (Always Include)

**Environment Files:**
- `Read(.env)`
- `Read(**/.env)`
- `Read(.env.*)`
- `Read(**/.env.*)`
- `Read(.env.local)`
- `Read(.env.development)`
- `Read(.env.production)`
- `Read(.env.test)`

**Version Control & IDE:**
- `Read(.git/**)`
- `Read(.vscode/**)`
- `Read(.idea/**)`
- `Read(.devcontainer/**)`
- `Read(.github/workflows/**)`

**Package Management:**
- `Read(node_modules/**)`
- `Read(package-lock.json)`

**Credentials & Secrets:**
- `Read(credentials.json)`
- `Read(**/credentials.json)`
- `Read(secrets.yml)`
- `Read(**/secrets.yml)`
- `Read(config/secrets.yml)`
- `Read(.secret)`
- `Read(**/.secret)`
- `Read(*.secret)`

**SSH & Certificate Files:**
- `Read(id_rsa)`
- `Read(id_rsa.pub)`
- `Read(id_ed25519)`
- `Read(id_ed25519.pub)`
- `Read(*.pem)`
- `Read(*.key)`
- `Read(*.p12)`
- `Read(*.jks)`
- `Read(*.pfx)`
- `Read(*.keystore)`
- `Read(*.cer)`
- `Read(*.crt)`

**Cloud Provider Credentials:**
- `Read(.aws/credentials)`
- `Read(.aws/config)`
- `Read(.gcp/credentials.json)`
- `Read(.azure/credentials)`

**Database Files:**
- `Read(*.db)`
- `Read(*.sqlite)`
- `Read(*.sqlite3)`

#### Technology-Specific Patterns

**Python (if detected):**
- `Read(.venv/**)`
- `Read(venv/**)`
- `Read(__pycache__/**)`
- `Read(**/__pycache__/**)`
- `Read(*.pyc)`
- `Read(.pytest_cache/**)`
- `Read(.tox/**)`
- `Read(dist/**)`
- `Read(build/**)`
- `Read(*.egg-info/**)`
- `Read(.mypy_cache/**)`
- `Read(.ruff_cache/**)`

**.NET (if detected):**
- `Read(bin/**)`
- `Read(obj/**)`
- `Read(*.user)`
- `Read(*.suo)`
- `Read(.vs/**)`
- `Read(*.DotSettings.user)`
- `Read(TestResults/**)`
- `Read(packages/**)`

**Go (if detected):**
- `Read(vendor/**)`

**Rust (if detected):**
- `Read(target/**)`

**PHP (if detected):**
- `Read(vendor/**)`
- `Read(composer.lock)`

**Ruby (if detected):**
- `Read(vendor/bundle/**)`
- `Read(.bundle/**)`

**Java (if detected):**
- `Read(target/**)`
- `Read(*.class)`
- `Read(.gradle/**)`
- `Read(build/**)`

**Node.js (if detected):**
- `Read(node_modules/**)`
- `Read(.next/**)`
- `Read(.nuxt/**)`
- `Read(dist/**)`
- `Read(build/**)`
- `Read(.cache/**)`
- `Read(.turbo/**)`

**Docker (if detected):**
- `Read(docker-compose.override.yml)`
- `Read(docker-compose.override.yaml)`

### Phase 3: Check Existing Configuration

Check if `.claude/settings.json` already exists using the **Read tool** (NOT bash test commands):

1. Try to read `.claude/settings.json` using the Read tool
2. If the file exists and Read succeeds:
   - Parse the JSON content
   - Check for existing `permissions.deny` section
   - Ask user for merge strategy preference using AskUserQuestion tool:
     - **Deduplicate** (default): Remove duplicate patterns, add only new ones
     - **Append**: Add all new patterns, keep duplicates
     - **Replace**: Completely replace existing deny section with new patterns
3. If the file doesn't exist (Read returns error):
   - Proceed to create new file with deny patterns
   - Use "Deduplicate" as the default strategy

**IMPORTANT**:
- Use **Read tool** to check file existence - DO NOT use bash test commands
- The Read tool will gracefully handle non-existent files by returning an error
- Parse existing JSON to preserve non-permission settings

### Phase 4: Show Preview & Get Confirmation

Display a comprehensive preview showing:

1. **Technologies Detected:**
   - List all detected technologies with file indicators

2. **Current Configuration (if exists):**
   - Show current deny patterns count
   - Show sample of existing patterns (first 5)

3. **Proposed Changes:**
   - Show all new patterns to be added
   - Group by category (Base Security, Python, .NET, etc.)
   - Show total pattern count

4. **After Configuration:**
   - Show total pattern count after merge
   - Show merge strategy being used

Ask for user confirmation before proceeding.

### Phase 5: Write Configuration

After user confirms:

1. Create `.claude/` directory if it doesn't exist using the Bash tool: `mkdir -p .claude`
2. Write or update `settings.json` using the **Write tool** (NOT bash echo or heredoc)
3. Preserve any other existing settings (don't overwrite non-permission settings)
4. Format JSON with proper indentation (2 spaces)
5. Show success message with:
   - File path: `.claude/settings.json`
   - Total deny patterns configured
   - Technologies covered

**IMPORTANT**:
- Use **Write tool** to create/update the settings file
- Use Bash tool only for creating the `.claude/` directory if needed
- Ensure proper JSON formatting with 2-space indentation

### Important Constraints

**DO NOT:**
- Read the contents of any sensitive files during scanning
- Include file paths from the actual project in the deny list
- Overwrite other settings in settings.json (preserve everything except permissions.deny)
- Proceed without user confirmation
- Use bash test commands (`test -f`, `[ -f ]`, etc.) - they trigger permission prompts
- Use any bash commands for file detection or checking

**DO:**
- Use **Glob tool** for technology detection (file pattern matching)
- Use **Read tool** to check if `.claude/settings.json` exists (handles errors gracefully)
- Use **Write tool** to create/update settings.json
- Use **AskUserQuestion tool** to ask for merge strategy preference
- Deduplicate patterns by default during merge
- Show clear before/after comparison
- Maintain alphabetical ordering within categories for readability
- Use forward slashes in all patterns for cross-platform compatibility

### Example Output Format

```
🔍 Detecting technologies in your project...

Technologies Detected:
✓ Node.js (package.json found)
✓ TypeScript (tsconfig.json found)
✓ Python (requirements.txt, pyproject.toml found)
✓ Docker (Dockerfile, docker-compose.yml found)

Current Configuration:
📄 .claude/settings.json exists
📊 Current deny patterns: 8

Proposed Security Configuration:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Base Security Patterns (25):
  • Environment files (.env, .env.*)
  • Version control (.git, .vscode, .idea)
  • Credentials (credentials.json, secrets.yml)
  • SSH & certificates (*.pem, *.key, id_rsa)
  • Cloud provider configs (.aws/credentials, .gcp/*)
  • Database files (*.db, *.sqlite)

Node.js Patterns (8):
  • node_modules/**
  • .next/**, .nuxt/**
  • dist/**, build/**
  • .cache/**, .turbo/**

Python Patterns (11):
  • .venv/**, venv/**
  • __pycache__/**, *.pyc
  • .pytest_cache/**, .tox/**
  • dist/**, *.egg-info/**

Docker Patterns (2):
  • docker-compose.override.yml

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total new patterns to add: 46
After merge: 54 total patterns

Merge Strategy: Deduplicate (remove duplicates, add only new patterns)

Would you like to proceed with this configuration? (yes/no)
```

### Success Message Format

```
✓ Security configuration successfully initialized!

Configuration Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 File: .claude/settings.json
📊 Total deny patterns: 54
🛡️ Technologies covered: Node.js, TypeScript, Python, Docker
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  IMPORTANT: You must restart Claude Code for these settings to take effect.

After restarting:
- Claude Code will avoid reading sensitive files, credentials, and build artifacts
- You can manually edit .claude/settings.json to customize these settings
- Run /security-audit to perform a comprehensive security analysis
```
