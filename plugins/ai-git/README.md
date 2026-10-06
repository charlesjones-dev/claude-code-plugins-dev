# AI-Git Plugin

**Git skills for Claude Code.** Generate a .gitignore, commit and push with a message in your repo's style, open a PR, and loop a PR through Codex review.

---

## Available Skills

### `/git-init`

Create or update `.gitignore` with patterns for your project's technology stack.

**What it does:**

- Detects technologies in your project (Node.js, Python, .NET, Go, Rust, PHP, Ruby, Java, Docker, etc.)
- Adds ignore patterns for each detected technology
- Handles environment files, build artifacts, dependencies, OS files, and IDE files
- Merges with an existing .gitignore, keeping your custom patterns and comments
- Groups patterns into commented sections
- Shows a preview and asks before writing

**Usage:**

```
/git-init
```

### `/git-commit-push-pr`

Commit, push, and create a pull request in one interactive flow. It doesn't run preflight checks.

**What it does:**

- Prompts for branch selection (prevents direct commits to main/master)
- Stages and commits with an auto-generated message
- Pushes to remote with automatic upstream tracking
- Creates a PR against the branch you pick (offers staging when it exists on origin)
- PR includes summary bullets, test plan, and Claude Code attribution

**Usage:**

```
/git-commit-push-pr
```

### `/git-pr-codex-loop`

Open a PR for the current branch, then loop on Codex Code Review until it comes back clean. You make the final merge decision. This skill never merges.

> **Note:** Claude Code's native `/code-review` (with `--fix`, `--comment`, and cloud "ultra" mode) now covers automated review-and-fix loops without external dependencies. This skill is specifically for repositories standardized on OpenAI's Codex Code Review bot, where it remains the right tool for that cross-tool workflow.

**What it does:**

- Opens or finds the PR for the current branch (refuses to run on main/master)
- Waits for CI to go green before involving Codex, then waits for the `chatgpt-codex-connector` bot's review to settle. Codex acknowledges with a 👀 reaction ("received," not "done"), then trickles findings in as several comments seconds apart, so the loop never acts on the first comment alone
- Handles Codex's no-comment "all clear": when nothing is found, Codex may post no review and add a 👍 reaction to the PR description instead, which the skill treats as a clean pass
- Resolves every finding worst-priority-first (P0 → P1 → P2): fixes, commits, pushes, and replies per thread (no `@codex` tag), then posts one `@codex review` comment after the whole pass to re-request a single review
- Reads and resolves review threads via the GitHub GraphQL API (the REST endpoint can't mark threads resolved)
- Loops until a pass comes back clean (summary verdict or a 👍 on the PR description) and every thread is resolved, then hands back the PR URL and a summary
- Makes every fix locally with Claude and never delegates fixes to Codex (the only mention it posts is one `@codex review` per pass). If Codex never picks the PR up, it stops and tells you to enable Automatic reviews
- Never merges, never force pushes, and pushes back with a reasoned reply when Codex is wrong

**Usage:**

```
/git-pr-codex-loop
```

### `/git-commit-push`

Stages the files you changed by name, writes a message in the style of your last three commits, and pushes. See [How It Works](#how-it-works) for each step.

**Usage:**

```
/git-commit-push
```

---

## Quick Start

### Installation

```
/plugin install ai-git@claude-code-plugins-dev
```

---

## Example Commits

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

## How It Works

`/git-commit-push` runs these steps:

1. **Analyze**: Runs `git status`, `git diff`, and `git log -3` to see your changes and your recent commit style. Stops early if there's nothing to commit.
2. **Branch check**: Stops on main or master and suggests a feature branch or `/git-commit-push-pr`.
3. **Stage**: Stages the changed files by name, skipping secrets (`.env`, `credentials.*`, `*.key`, `*.pem`, etc.).
4. **Commit**: Writes a concise message that says what changed and why, with conventional commit prefixes (`feat:`, `fix:`, `docs:`) if your repo uses them. It doesn't add Claude attribution.
5. **Push**: Pushes to origin, setting upstream with `-u` if needed. It never force pushes.
6. **Confirm**: Shows the commit hash.

---

## Best Practices

Write the commit message yourself for:

- Major releases or version bumps
- Breaking changes that need a detailed explanation
- Merge commits with conflicts
- Commits that need specific issue references

---

## Configuration

There's nothing to configure.

---

## Plugin Details

- **Name:** AI-Git Plugin
- **Type:** AI Instruction Plugin (Skills)
- **Version:** 1.3.2
- **Skills:** `/git-init`, `/git-commit-push`, `/git-commit-push-pr`, `/git-pr-codex-loop`
- **License:** [MIT](LICENSE)
- **Author:** Charles Jones

---

## Contributing

Bug reports and fixes are welcome. See [CONTRIBUTING.md](../../CONTRIBUTING.md).
