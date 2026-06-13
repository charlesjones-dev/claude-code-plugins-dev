# AI-Git Plugin

**AI-powered git automation for Claude Code.** A collection of intelligent git commands and agents that streamline your version control workflow.

---

## 🎯 What This Plugin Does

Provides a suite of AI-powered git commands that automate common git workflows, from .gitignore generation to commit automation and beyond.

## 📋 Available Skills

### `/git-init`

Initialize or update `.gitignore` with intelligent exclusion patterns based on your project's technology stack.

**What it does:**

- Detects technologies in your project (Node.js, Python, .NET, Go, Rust, PHP, Ruby, Java, Docker, etc.)
- Generates comprehensive .gitignore patterns for detected technologies
- Handles environment files, build artifacts, dependencies, OS files, and IDE files
- Smart merge with existing .gitignore (preserves custom patterns and comments)
- Organized sections with helpful comments

**Usage:**

```
/git-init
# ✨ AI detects your tech stack
# ✨ Generates appropriate .gitignore patterns
# ✨ Previews changes and asks for confirmation
# ✨ Creates or updates .gitignore
# ✅ Done!
```

### `/git-commit-push-pr`

Commit, push, and create a pull request in one interactive flow. A lightweight shipping workflow without preflight checks.

**What it does:**

- Prompts for branch selection (prevents direct commits to main/master)
- Stages and commits with an auto-generated message
- Pushes to remote with automatic upstream tracking
- Creates a PR with dynamic target branch selection (detects staging/main)
- PR includes summary bullets, test plan, and Claude Code attribution

**Usage:**

```
/git-commit-push-pr
# ✨ AI analyzes your changes
# ✨ Prompts for branch selection
# ✨ Commits with proper message
# ✨ Pushes to remote
# ✨ Prompts for PR target branch
# ✨ Creates PR with summary and test plan
# ✅ Done! PR URL returned
```

### `/git-pr-codex-loop`

Open a PR for the current branch, then loop on Codex Code Review until it comes back clean. The human always makes the final merge decision — this skill never merges.

**What it does:**

- Opens or finds the PR for the current branch (refuses to run on main/master)
- Waits for CI to go green before involving Codex, then waits for the `chatgpt-codex-connector` bot's review to fully settle — Codex acknowledges with a 👀 reaction ("received," not "done") then trickles findings in as several comments seconds apart, so the loop never acts on just the first comment
- Handles Codex's no-comment "all clear": when nothing is found, Codex may post no review and just add a 👍 reaction to the PR description, which the skill treats as a clean pass
- Resolves every finding worst-priority-first (P0 → P1 → P2): fixes, commits, pushes, and replies per thread (no `@codex` tag), then posts one `@codex review` comment after the whole pass to re-request a single review
- Reads and resolves review threads via the GitHub GraphQL API (the REST endpoint cannot mark threads resolved)
- Loops until a pass comes back clean (summary verdict or a 👍 on the PR description) and every thread is resolved, then hands back the PR URL and a summary
- Makes every fix locally with Claude — never delegates fixes to Codex (the only mention it posts is one `@codex review` per pass); if Codex never picks the PR up, it stops and tells you to enable Automatic reviews
- Never merges, never force pushes, and pushes back with a reasoned reply when Codex is wrong

**Usage:**

```
/git-pr-codex-loop
# ✨ Opens or finds the PR for the current branch
# ✨ Waits for CI, then for Codex Code Review
# ✨ Resolves each finding and re-requests review (@codex)
# ✨ Loops until the review is clean
# ✅ Hands back the PR URL — you decide when to merge
```

### `/git-commit-push`

Analyze changes, generate intelligent commit messages, and push to origin - all in one command.

**Before (manual):**

```
git status
git diff
git log # check commit message style
git add .
git commit -m "fix: updated user authentication"
git push
```

**After (with ai-git plugin):**

```
/git-commit-push
# ✨ AI analyzes your changes
# ✨ Generates commit message matching your repo's style
# ✨ Stages, commits, and pushes automatically
# ✅ Done!
```

---

## 🚀 Quick Start

### Installation

```
/plugin install ai-git@claude-code-plugins-dev
```

### Usage

```
# Make your changes

# Commit and push everything
/git-commit-push

# That's it! AI handles the rest.
```

---

## 💡 Features

### `/git-commit-push` Command

#### Intelligent Analysis

- Analyzes `git status` to see all changes
- Reviews `git diff` to understand what changed
- Checks recent commit history to match your style
- Detects conventional commit patterns if used

#### Style Matching

- Automatically follows your repository's commit message conventions
- Detects and uses conventional commit prefixes (feat:, fix:, docs:, etc.)
- Matches tone and format of recent commits
- Respects your project's commit guidelines

#### Safety Guards

- Blocks commits directly to main/master (suggests feature branch or `/git-commit-push-pr`)
- Skips secret-like files (`.env`, `credentials.*`, `*.key`, `*.pem`, etc.)
- Never force pushes
- Detects empty state and stops early if nothing to commit

#### Complete Workflow

1. **Analyze**: Reviews all changes with `git status` and `git diff`
2. **Branch check**: Verifies you're not on main/master
3. **Stage**: Stages specific files by name (skips secrets)
4. **Generate**: Creates appropriate commit message using HEREDOC formatting
5. **Commit**: Commits with generated message
6. **Push**: Pushes to origin (auto-sets upstream tracking with `-u` if needed)
7. **Confirm**: Shows commit hash and success status

#### Clean Commits

- No AI attribution clutter in commit messages
- Professional, repository-appropriate messages
- Focus on what changed and why
- Concise and descriptive

---

## 📝 Example Commits

The plugin adapts to your repository's style:

**For repos using conventional commits:**

```
feat: add user authentication middleware
fix: resolve memory leak in websocket handler
docs: update API endpoint documentation
refactor: simplify error handling logic
```

**For repos with simple style:**

```
Add user authentication middleware
Fix memory leak in websocket handler
Update API endpoint documentation
Simplify error handling logic
```

---

## ⚙️ How It Works

1. **Context Gathering**
   - Runs `git status` to identify all changes
   - Runs `git diff` to see actual code modifications
   - Runs `git log -3` to learn your commit style

2. **Message Generation**
   - Analyzes the nature of changes (new feature, bug fix, refactor, etc.)
   - Drafts concise message describing what and why
   - Formats according to detected repository conventions

3. **Execution**
   - Stages all changes
   - Creates commit with generated message
   - Pushes to remote origin
   - Confirms success

---

## 🎓 Best Practices

### When to Use

- ✅ Regular feature development
- ✅ Bug fixes
- ✅ Documentation updates
- ✅ Refactoring work
- ✅ Quick updates and improvements

### When to Write Manually

- ⚠️ Major releases or version bumps
- ⚠️ Breaking changes requiring detailed explanation
- ⚠️ Merge commits with conflicts
- ⚠️ Commits requiring specific issue references

---

## ⏱️ Time Savings

**Per commit workflow:**

- Manual: ~2-3 minutes (review, write message, commit, push)
- With git-commit-push: ~10 seconds (one command)

**Estimated savings:**

- Per day (10 commits): Save ~25-30 minutes
- Per week: Save ~2-2.5 hours
- Per year: Save ~100+ hours

---

## 🔧 Configuration

No configuration needed! The plugin works out of the box and adapts to your repository automatically.

---

## 📦 Plugin Details

- **Name:** AI-Git Plugin
- **Type:** AI Instruction Plugin (Skills)
- **Version:** 1.3.0
- **Skills:** `/git-init`, `/git-commit-push`, `/git-commit-push-pr`, `/git-pr-codex-loop`
- **License:** MIT
- **Author:** Charles Jones

---

## 🤝 Contributing

Found a bug or have a suggestion? [Open an issue](https://github.com/charlesjones-dev/claude-code-plugins-dev/issues) or submit a pull request!

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for the Claude Code community**
