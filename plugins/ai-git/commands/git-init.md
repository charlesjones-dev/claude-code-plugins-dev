# Git Init

Initialize Git ignore patterns by creating or updating `.gitignore` with intelligent exclusion patterns based on your project's technology stack.

## Instructions

**CRITICAL**: This command MUST NOT accept any arguments. If the user provided any text, URLs, or paths after this command (e.g., `/git-init ./project` or `/git-init --force`), you MUST COMPLETELY IGNORE them. Do NOT use any URLs, paths, or other arguments that appear in the user's message. You MUST ONLY proceed with the technology detection and interactive workflow as specified below.

**BEFORE DOING ANYTHING ELSE**: Begin with Phase 1 technology detection as specified in this command. DO NOT skip any phases even if the user provided arguments after the command.

Set up comprehensive .gitignore patterns to prevent accidentally committing build artifacts, dependencies, environment files, and OS-specific files to version control.

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

**Next.js/React Detection:**
- Use Glob to search for: `next.config.js`, `next.config.ts`, `next.config.mjs`

**Vue Detection:**
- Use Glob to search for: `vue.config.js`, `nuxt.config.js`, `nuxt.config.ts`

**Terraform Detection:**
- Use Glob to search for: `*.tf`, `terraform.tfvars`

**IMPORTANT**:
- Use **Glob tool only** for file detection - DO NOT use bash test commands or any bash commands
- Only check for file existence - DO NOT read the contents of any files during detection
- Glob returns matching files or empty array if none found

### Phase 2: Build Ignore Patterns

Create a comprehensive .gitignore combining:

#### Base Patterns (Always Include)

**Environment & Secrets:**
```
# Environment variables
.env
.env.*
.env.local
.env.development
.env.production
.env.test
!.env.example

# Secrets
credentials.json
secrets.yml
*.secret
*.pem
*.key
*.p12
*.jks
*.pfx
*.keystore
```

**Operating System Files:**
```
# macOS
.DS_Store
.AppleDouble
.LSOverride
._*

# Windows
Thumbs.db
Thumbs.db:encryptable
ehthumbs.db
ehthumbs_vista.db
Desktop.ini
$RECYCLE.BIN/

# Linux
*~
.directory
.Trash-*
```

**IDE & Editor Files:**
```
# Visual Studio Code
.vscode/*
!.vscode/settings.json
!.vscode/tasks.json
!.vscode/launch.json
!.vscode/extensions.json
*.code-workspace

# JetBrains IDEs
.idea/
*.iml
*.iws
*.ipr
.idea_modules/

# Vim
*.swp
*.swo
*~

# Emacs
*~
\#*\#
/.emacs.desktop
/.emacs.desktop.lock

# Sublime Text
*.sublime-workspace
*.sublime-project
```

#### Technology-Specific Patterns

**Node.js (if detected):**
```
# Dependencies
node_modules/
jspm_packages/

# Build outputs
dist/
build/
.next/
.nuxt/
out/

# Testing
coverage/
.nyc_output/

# Caching
.cache/
.turbo/
.parcel-cache/
.webpack/

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*
lerna-debug.log*
pnpm-debug.log*

# Lock files (optional - ask user)
# Uncomment if you want to ignore lock files
# package-lock.json
# yarn.lock
# pnpm-lock.yaml
```

**Python (if detected):**
```
# Byte-compiled / optimized
__pycache__/
*.py[cod]
*$py.class
*.so

# Virtual environments
.venv/
venv/
ENV/
env/
.python-version

# Distribution / packaging
dist/
build/
*.egg-info/
*.egg
.eggs/
wheels/

# Testing
.pytest_cache/
.tox/
.coverage
htmlcov/
.hypothesis/

# Type checking
.mypy_cache/
.dmypy.json
dmypy.json
.pytype/

# Linting
.ruff_cache/

# Jupyter Notebook
.ipynb_checkpoints
*.ipynb
```

**.NET (if detected):**
```
# Build results
bin/
obj/
out/

# User-specific files
*.user
*.suo
*.userosscache
*.sln.docstates
*.userprefs

# Visual Studio
.vs/
*.DotSettings.user

# Test results
TestResults/
[Tt]est[Rr]esult*/
*.trx

# NuGet
packages/
*.nupkg
*.snupkg
project.lock.json
project.fragment.lock.json
```

**Go (if detected):**
```
# Binaries
*.exe
*.exe~
*.dll
*.so
*.dylib

# Test binary
*.test

# Output of the go coverage tool
*.out

# Dependency directories
vendor/

# Go workspace file
go.work
```

**Rust (if detected):**
```
# Compilation outputs
target/
Cargo.lock

# Backup files
**/*.rs.bk
*.pdb
```

**PHP (if detected):**
```
# Composer
vendor/
composer.lock
composer.phar

# Laravel
.env
.env.backup
.phpunit.result.cache
Homestead.json
Homestead.yaml
npm-debug.log
yarn-error.log

# Symfony
/var/
/vendor/
```

**Ruby (if detected):**
```
# Bundler
vendor/bundle/
.bundle/

# RVM
.rvmrc

# rbenv
.ruby-version

# RSpec
.rspec_status

# Coverage
coverage/
```

**Java (if detected):**
```
# Compiled class files
*.class

# Log files
*.log

# Package Files
*.jar
*.war
*.nar
*.ear
*.zip
*.tar.gz
*.rar

# Maven
target/
pom.xml.tag
pom.xml.releaseBackup
pom.xml.versionsBackup
pom.xml.next
release.properties

# Gradle
.gradle/
build/
gradle-app.setting
!gradle-wrapper.jar
```

**Docker (if detected):**
```
# Docker override files
docker-compose.override.yml
docker-compose.override.yaml
```

**Terraform (if detected):**
```
# Terraform
.terraform/
*.tfstate
*.tfstate.*
*.tfvars
crash.log
override.tf
override.tf.json
*_override.tf
*_override.tf.json
```

### Phase 3: Check Existing .gitignore

Check if `.gitignore` already exists using the **Read tool** (NOT bash test commands):

1. Try to read `.gitignore` using the Read tool
2. If the file exists and Read succeeds:
   - Parse the content
   - Analyze existing patterns
   - Ask user for merge strategy preference using AskUserQuestion tool:
     - **Smart Merge** (default): Deduplicate patterns, preserve comments, organize by category
     - **Append**: Add all new patterns at the end, keep existing content as-is
     - **Replace**: Completely replace existing .gitignore with new patterns
3. If the file doesn't exist (Read returns error):
   - Proceed to create new file with ignore patterns
   - Use "Smart Merge" as the default strategy

**IMPORTANT**:
- Use **Read tool** to check file existence - DO NOT use bash test commands
- The Read tool will gracefully handle non-existent files by returning an error
- Preserve existing comments and custom patterns during merge
- Detect and remove duplicate patterns

### Phase 4: Show Preview & Get Confirmation

Display a comprehensive preview showing:

1. **Technologies Detected:**
   - List all detected technologies with file indicators

2. **Current .gitignore (if exists):**
   - Show line count
   - Show sample of existing patterns (first 10 lines)
   - Identify any duplicate or redundant patterns

3. **Proposed .gitignore:**
   - Show all patterns to be added
   - Group by category (Base Patterns, Node.js, Python, etc.)
   - Show total pattern count
   - Highlight any custom patterns that will be preserved

4. **After Merge:**
   - Show estimated total line count
   - Show merge strategy being used
   - List categories included

Ask for user confirmation before proceeding.

### Phase 5: Write .gitignore

After user confirms:

1. Build the complete .gitignore content with proper formatting:
   - Add header comment with generation info
   - Group patterns by category with section headers
   - Include blank lines between sections for readability
   - Preserve existing custom patterns if merging
   - Sort patterns within categories alphabetically

2. Write `.gitignore` using the **Write tool** (NOT bash echo or heredoc)

3. Show success message with:
   - File path: `.gitignore`
   - Total patterns configured
   - Technologies covered
   - Next steps (review, git status, commit)

**IMPORTANT**:
- Use **Write tool** to create/update the .gitignore file
- DO NOT use bash commands for writing the file
- Ensure proper formatting with blank lines between sections
- Include helpful comments for each section

### Important Constraints

**DO NOT:**
- Read the contents of any sensitive files during scanning
- Include actual file paths from the project in .gitignore
- Proceed without user confirmation
- Use bash test commands (`test -f`, `[ -f ]`, etc.)
- Use any bash commands for file detection or checking
- Remove existing custom patterns without user consent

**DO:**
- Use **Glob tool** for technology detection (file pattern matching)
- Use **Read tool** to check if `.gitignore` exists (handles errors gracefully)
- Use **Write tool** to create/update .gitignore
- Use **AskUserQuestion tool** to ask for merge strategy preference
- Deduplicate patterns by default during merge
- Preserve comments and custom patterns from existing .gitignore
- Show clear before/after comparison
- Maintain alphabetical ordering within categories for readability
- Use forward slashes in all patterns for cross-platform compatibility
- Add helpful section headers and comments

### Example Output Format

```
🔍 Detecting technologies in your project...

Technologies Detected:
✓ Node.js (package.json found)
✓ TypeScript (tsconfig.json found)
✓ Python (requirements.txt, pyproject.toml found)
✓ Docker (Dockerfile, docker-compose.yml found)

Current .gitignore:
📄 .gitignore exists (42 lines)
📊 Sample patterns:
  node_modules/
  .env
  dist/
  ...

Proposed .gitignore Structure:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Base Patterns:
  • Environment & Secrets (12 patterns)
  • Operating System Files (15 patterns)
  • IDE & Editor Files (18 patterns)

Node.js Patterns:
  • Dependencies (2 patterns)
  • Build outputs (5 patterns)
  • Testing & Caching (6 patterns)
  • Logs (5 patterns)

Python Patterns:
  • Byte-compiled (5 patterns)
  • Virtual environments (5 patterns)
  • Distribution (7 patterns)
  • Testing (5 patterns)

Docker Patterns:
  • Docker overrides (2 patterns)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total patterns: 87
Estimated file size: ~150 lines (with comments)

Merge Strategy: Smart Merge (deduplicate, preserve comments, organize)

Would you like to proceed with this configuration? (yes/no)
```

### Success Message Format

```
✓ .gitignore successfully initialized!

Configuration Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 File: .gitignore
📊 Total patterns: 87 (organized in 7 categories)
🛡️ Technologies covered: Node.js, TypeScript, Python, Docker
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next Steps:
1. Review the generated .gitignore file
2. Run `git status` to see which files are now ignored
3. Remove any currently tracked files that should be ignored:
   git rm --cached <file>
4. Commit the .gitignore file:
   git add .gitignore
   git commit -m "Add comprehensive .gitignore for detected technologies"

💡 Tip: You can run this command again to update .gitignore when adding new technologies to your project.
```

### Additional Features

**Lock File Handling:**
When Node.js is detected, ask the user if they want to commit lock files (package-lock.json, yarn.lock, pnpm-lock.yaml):
- Most projects SHOULD commit lock files for reproducible builds
- Only ignore lock files if explicitly requested
- Add commented-out lock file patterns with explanation

**Custom Patterns:**
During Smart Merge, detect and preserve:
- User-added comments (lines starting with #)
- Custom patterns not in the standard template
- Negation patterns (lines starting with !)

**Pattern Validation:**
- Ensure patterns use forward slashes (/)
- Remove duplicate patterns across categories
- Warn about overly broad patterns (e.g., `*`, `*.txt`)
