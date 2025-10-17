# AI-Git Plugin

**AI-powered git automation for Claude Code.** A collection of intelligent git commands and agents that streamline your version control workflow.

---

## 🎯 What This Plugin Does

Provides a suite of AI-powered git commands that automate common git workflows, from commit generation to branch management and beyond.

## 📋 Available Commands

### `/commit-push`

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
/commit-push
# ✨ AI analyzes your changes
# ✨ Generates commit message matching your repo's style
# ✨ Stages, commits, and pushes automatically
# ✅ Done!
```

_More AI-powered git commands and agents coming soon..._

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
/commit-push

# That's it! AI handles the rest.
```

---

## 💡 Features

### `/commit-push` Command

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

#### Complete Workflow

1. **Analyze**: Reviews all staged and unstaged changes
2. **Generate**: Creates appropriate commit message
3. **Stage**: Adds all changes with `git add .`
4. **Commit**: Commits with generated message
5. **Push**: Pushes to origin automatically
6. **Confirm**: Shows commit hash and success status

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
- With commit-push: ~10 seconds (one command)

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
- **Version:** 1.0.0
- **Type:** AI Instruction Plugin (Slash Commands & Agents)
- **Commands:** `/commit-push` (more coming soon)
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
