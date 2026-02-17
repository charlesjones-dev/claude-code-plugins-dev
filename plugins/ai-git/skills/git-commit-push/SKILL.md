---
name: git-commit-push
description: "Commit all changes to git with an auto-generated message and push to origin."
disable-model-invocation: true
---

# Commit and Push

Commit all changes to git and push to origin.

## Instructions

**CRITICAL**: This command MUST NOT accept any arguments. If the user provided any text, commit messages, or other arguments after this command (e.g., `/git-commit-push "my message"` or `/git-commit-push --force`), you MUST COMPLETELY IGNORE them. Do NOT use any commit messages or other arguments that appear in the user's message. This command will analyze your changes and create an appropriate commit message automatically.

**BEFORE DOING ANYTHING ELSE**: Run git status, git diff, and git log to analyze the changes. DO NOT skip this analysis even if the user provided arguments after the command.

When this command is executed:

### Step 1: Analyze Changes

1. Run `git status` (never use `-uall` flag) to see all changes
2. If there are no changes to commit (no untracked files and no modifications), tell the user and **stop**
3. Run `git diff` to see the actual changes
4. Run `git log -3 --format='%s'` to see recent commit message style

### Step 2: Branch Safety Check

1. Run `git branch --show-current` to determine the current branch
2. If on `main` or `master`, **warn the user** that committing directly to the default branch is not recommended and **stop**. Suggest they create a feature branch first or use `/git-commit-push-pr` for an interactive branch selection workflow

### Step 3: Stage Files

1. Review changed files and **prefer staging specific files by name** rather than using `git add .` or `git add -A`
2. Do NOT stage files that look like secrets (`.env`, `.env.*`, `credentials.*`, `*.key`, `*.pem`, `*.secret`, etc.). If secret-like files are detected, warn the user and skip them
3. Stage the appropriate files

### Step 4: Commit

1. Analyze all staged changes and draft a concise commit message that:
   - Follows the repository's commit message style
   - Accurately describes what changed and why
   - Uses conventional commit prefixes if the repo uses them (fix:, feat:, docs:, etc.)
2. Use a HEREDOC for the commit message to ensure proper formatting:
   ```bash
   git commit -m "$(cat <<'EOF'
   your commit message here
   EOF
   )"
   ```

### Step 5: Push

1. Check if the current branch tracks a remote: `git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null`
2. If no upstream is set, push with `-u` flag: `git push -u origin <branch>`
3. If upstream exists, push normally: `git push`
4. Confirm success and show the commit hash

## Important rules

- Never force push
- Never use `git status -uall` (can cause memory issues on large repos)
- Do not commit files that look like secrets (.env, credentials, etc.)
- Do not commit or push directly to main/master
- If there are no changes to commit, tell the user and stop

IMPORTANT: Do not include the following in commit messages:

- 🤖 Generated with [Claude Code](https://claude.com/claude-code)
- Co-Authored-By: Claude <noreply@anthropic.com>
