# AI-Workflow Plugin

**Development workflow skills for Claude Code.** Preflight code quality checks, ship-it workflow, development principles generator, and curated CLAUDE.md behavior rules.

> **Removed skills (July 2026):** `/workflow-plan-phases` and `/workflow-implement-phases` were removed because Claude Code ships **Dynamic Workflows** natively (a JavaScript runtime that orchestrates subagent fan-out with per-agent token budgets), which supersedes manual phase planning/orchestration. They're still available in git history.

---

## Available Skills

### `/workflow-principles`

Generate a context-aware Development Principles section for your CLAUDE.md, tailored to your project's structure and tech stack.

**What it does:**

- Auto-discovers project structure (monorepo vs single, workspace packages, shared modules)
- Detects tech stack (languages, frameworks, validation libs, state management, testing tools)
- Asks which principle categories to include
- Generates principles using real package names, paths, and library names from your project
- Supports monorepo-specific rules (shared package conventions, dependency direction, cross-package contracts)
- Supports frontend component architecture rules (isolation, composition, state management)
- Appends to an existing CLAUDE.md, or replaces or merges an existing principles section
- Writes to project CLAUDE.md or user-level ~/.claude/CLAUDE.md

**Usage:**

```
/workflow-principles
```

**Principle Categories Available:**

| Category | What It Covers |
|----------|---------------|
| SOLID Principles | SRP, OCP, LSP, ISP, DIP - tailored to your stack |
| DRY / Code Reuse | No duplication, shared code rules, import-first |
| KISS / Simplicity | Simplest correct solution, avoid premature abstraction |
| YAGNI / Scope Discipline | Only build what's requested, ask before extras |
| Modularity & Coupling | Package boundaries, dependency direction, loose coupling |
| Component Architecture | Component isolation, composition, prop/state rules |
| Type Safety & Contracts | Strict typing, shared types, API contracts |
| Error Handling | Error boundaries, structured errors, graceful degradation |
| Testing Philosophy | Test behavior, integration over mocking, edge cases |
| Git Workflow | Commit consent, doc review before commits, branch conventions |

### `/workflow-rules`

Add, remove, or list curated **behavior rules** in CLAUDE.md: short instructions that correct repeated Claude Code annoyances (PR padding, fabricated test plans, "Generated with Claude Code" footers, internal-deliberation narration).

> **Rules vs. Principles:** `/workflow-rules` controls **how Claude behaves** (communication style, PR/commit hygiene, scope discipline) and is cross-project, picked from a curated library. `/workflow-principles` controls **how code is written in this project** (SOLID, DRY, testing philosophy) and is generated from project discovery. Use `/workflow-rules` when you keep correcting Claude on the same thing across every project; use `/workflow-principles` when you want project-specific coding standards.

**What it does:**

- Reads the curated rule library shipped with the plugin
- Picks target file: user `~/.claude/CLAUDE.md` (default, applies everywhere) or project `./CLAUDE.md`
- Cross-platform path resolution (Windows `%USERPROFILE%\.claude\CLAUDE.md` and POSIX `~/.claude/CLAUDE.md`)
- Multi-select picker grouped by section, with already-installed rules filtered out
- Wraps each installed rule in HTML comment markers (`<!-- workflow-rules:id=... -->`) so adds are idempotent and removes are precise, even if you edit the rule's title later
- Shows a unified diff before any write and requires explicit confirmation

**Usage:**

```
/workflow-rules
```

**Modes (chosen interactively):**

- **Add**: install one or more curated rules into the chosen CLAUDE.md
- **Remove**: uninstall previously-installed rules (matched by ID, not title)
- **List**: show what's currently installed and where

**Rule library:**

| Section | Rules |
|---------|-------|
| PR and Commit Hygiene | Scope to current session, no fabricated test plans, no speculative deploy steps, short PR bodies, scoped commit messages, no "Generated with Claude Code" footers |
| Scope Discipline | No unrequested features, confirm before risky/shared-state actions |
| Communication Style | No internal-deliberation narration, match response length to task |

**Before (manual fixes every project):**

```
# Edit ~/.claude/CLAUDE.md by hand
# Copy-paste the same rules into every new project
# Forget which corrections you already wrote down
```

**After (with workflow-rules):**

```
/workflow-rules
# Pick "Add rules to CLAUDE.md"
# Pick user-level (applies everywhere) or project-level
# Multi-select the rules you want
# Review diff, confirm
```

### `/workflow-preflight`

Run code quality checks before commits, PRs, or deployments.

**What it does:**

- Auto-detects configured quality tools across ecosystems
- Runs checks in this order: typecheck -> lint -> format check -> security -> tests
- Detects security tools: pnpm/npm/yarn audit, eslint-plugin-security, Semgrep
- Finds Semgrep through package.json scripts, config files, CI workflows, or README docs, with a Docker fallback
- Reports each check as pass, warning, or fail
- Offers interactive fix mode (or use `--fix` for automatic)
- Respects existing project scripts (uses `npm run lint` over raw `eslint`)

**Usage:**

```
/workflow-preflight                  # Interactive mode (default)
/workflow-preflight --fix            # Auto-fix all fixable issues
/workflow-preflight --check-only     # Report only, no fixes
/workflow-preflight --verbose        # Show detailed output
```

**Supported Ecosystems:**

| Ecosystem | Type Check | Lint | Format | Security | Test |
|-----------|------------|------|--------|----------|------|
| **Node.js/TypeScript** | tsc | ESLint, Biome | Prettier | pnpm/npm/yarn audit, eslint-plugin-security, Semgrep | Jest, Vitest |
| **Python** | MyPy | Ruff | Black, Ruff | pip-audit, safety, Semgrep | Pytest |
| **.NET** | dotnet build | Analyzers | dotnet format | Semgrep | dotnet test |
| **Go** | go build | golangci-lint | gofmt | Semgrep | go test |
| **Rust** | cargo check | Clippy | cargo fmt | cargo audit, Semgrep | cargo test |

### `/workflow-ship`

Run preflight checks, then commit, push, and open a PR.

**What it does:**

- Runs `/workflow-preflight` first. If checks fail, it tries auto-fixes and re-runs them. If it applied fixes, it stops so you can review them before running `/workflow-ship` again. If issues can't be fixed automatically, it stops and reports them
- Asks whether to commit to the current branch or a new one (on main or master, it requires a new branch)
- Stages specific files and writes a commit message in the style of your recent commits, with no Claude attribution
- Pushes, setting upstream if needed, and never force pushes
- Asks for the PR target (staging first if it exists on origin, otherwise main), opens the PR with a summary, test plan, and Claude Code attribution footer, and returns the URL

**Usage:**

```
/workflow-ship
```

---

## Quick Start

### Installation

```
/plugin install ai-workflow@claude-code-plugins-dev
```

---

## How It Works

### Preflight Check Flow

```
Discovery Phase
      |
      v
Detect Project Type(s)
      |
      v
Find Configured Tools (including security scanners)
      |
      v
Run Checks (type -> lint -> format -> security -> test)
      |
      v
Present Results
      |
      v
Fix Prompt (if issues found)
      |
      v
Verify Fixes
```

---

## Best Practices

### Preflight Integration

- Run `/workflow-preflight` before you commit
- Use `--fix` locally and `--check-only` in CI.
- Align local checks with CI configuration

---

## Plugin Details

- **Name:** AI-Workflow
- **Version:** 2.0.1
- **Type:** Development Workflow Automation
- **Skills:** `/workflow-preflight`, `/workflow-ship`, `/workflow-principles`, `/workflow-rules`
- **License:** [MIT](LICENSE)
- **Author:** Charles Jones

---

## Contributing

Bug reports and fixes are welcome. See [CONTRIBUTING.md](../../CONTRIBUTING.md).
