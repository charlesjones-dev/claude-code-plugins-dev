# AI-Workflow Plugin

**AI-powered development workflow automation for Claude Code.** Preflight code quality checks, ship-it workflow, development principles generator, and curated CLAUDE.md behavior rules.

> **Removed skills (July 2026):** `/workflow-plan-phases` and `/workflow-implement-phases` were removed as of July 2026 — Claude Code now ships **Dynamic Workflows** natively (a JavaScript runtime that orchestrates subagent fan-out with per-agent token budgets), which supersedes manual phase planning/orchestration. They remain available in git history. This plugin now provides `/workflow-preflight`, `/workflow-ship`, `/workflow-principles`, and `/workflow-rules`.

---

## What This Plugin Does

Provides tools for day-to-day development workflows: running comprehensive code quality checks, shipping code with a single command, generating project-aware development principles, and managing curated CLAUDE.md behavior rules.

### Key Capabilities

- **Preflight Checks**: Auto-detect and run type checking, linting, formatting, security scanning, and tests across multiple ecosystems
- **Ship It**: Run preflight checks, commit, push, and create a PR in one streamlined flow
- **Development Principles**: Generate a context-aware Development Principles section for CLAUDE.md from project discovery
- **Behavior Rules**: Install curated, marker-wrapped behavior rules into user or project CLAUDE.md

---

## Available Skills

### `/workflow-principles`

Generate a context-aware Development Principles section for your CLAUDE.md, tailored to your project's actual structure and tech stack.

**What it does:**

- Auto-discovers project structure (monorepo vs single, workspace packages, shared modules)
- Detects tech stack (languages, frameworks, validation libs, state management, testing tools)
- Interactively configures which principle categories to include
- Generates principles using real package names, paths, and library names from your project
- Supports monorepo-specific rules (shared package conventions, dependency direction, cross-package contracts)
- Supports frontend component architecture rules (isolation, composition, state management)
- Smart merge with existing CLAUDE.md (append, replace section, or merge)
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

**Before (manual setup):**

```
# Copy principles from another project
# Manually edit package names and paths
# Forget to update when adding new packages
# Inconsistent principles across projects
```

**After (with workflow-principles):**

```
/workflow-principles
# AI discovers your project structure
# You select which principles matter
# Principles generated with real package names
# Written directly to CLAUDE.md
```

### `/workflow-rules`

Add, remove, or list curated **behavior rules** in CLAUDE.md — short instructions that correct repeated Claude Code annoyances (PR padding, fabricated test plans, "Generated with Claude Code" footers, internal-deliberation narration).

> **Rules vs. Principles:** `/workflow-rules` controls **how Claude behaves** (communication style, PR/commit hygiene, scope discipline) and is cross-project, picked from a curated library. `/workflow-principles` controls **how code is written in this project** (SOLID, DRY, testing philosophy) and is generated from project discovery. Use `/workflow-rules` when you keep correcting Claude on the same thing across every project; use `/workflow-principles` when you want project-specific coding standards.

**What it does:**

- Reads the curated rule library shipped with the plugin
- Picks target file: user `~/.claude/CLAUDE.md` (default, applies everywhere) or project `./CLAUDE.md`
- Cross-platform path resolution (Windows `%USERPROFILE%\.claude\CLAUDE.md` and POSIX `~/.claude/CLAUDE.md`)
- Multi-select picker grouped by section, with already-installed rules filtered out
- Wraps each installed rule in HTML comment markers (`<!-- workflow-rules:id=... -->`) so adds are idempotent and removes are precise — even if you edit the rule's title later
- Shows a unified diff before any write and requires explicit confirmation
- Sync across machines via `/plugin update` — pull the latest library, then re-run to install new rules

**Usage:**

```
/workflow-rules
```

**Modes (chosen interactively):**

- **Add** — install one or more curated rules into the chosen CLAUDE.md
- **Remove** — uninstall previously-installed rules (matched by ID, not title)
- **List** — show what's currently installed and where

**Rule library (curated, lean):**

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
# Drift between machines
```

**After (with workflow-rules):**

```
/workflow-rules
# Pick "Add rules to CLAUDE.md"
# Pick user-level (applies everywhere) or project-level
# Multi-select the rules you want
# Review diff, confirm
# /plugin update on another machine to sync the library
```

### `/workflow-preflight`

Run comprehensive code quality checks before commits, PRs, or deployments.

**What it does:**

- Auto-detects configured quality tools across ecosystems
- Runs checks in optimal order: format -> typecheck -> lint -> security -> tests
- Detects security tools: pnpm/npm/yarn audit, eslint-plugin-security, Semgrep
- Universal Semgrep detection via config files, CI workflows, README docs, or Docker fallback
- Reports results with clear pass/fail/warning indicators
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

**Before (manual checks):**

```
# Remember which tools are configured
# Run each check manually in the right order
# Parse output to find issues
# Decide whether to fix or not
# Run checks again to verify
```

**After (with ai-workflow plugin):**

```
/workflow-preflight
# AI discovers configured tools
# Runs all checks in optimal order
# Shows clear summary
# Offers to fix issues
# Re-verifies after fixes
```

---

## Quick Start

### Installation

```
/plugin install ai-workflow@claude-code-plugins-dev
```

### Usage

```
# Run preflight checks before committing
/workflow-preflight

# Or ship everything in one go (preflight + commit + push + PR)
/workflow-ship

# Generate project-aware development principles for CLAUDE.md
/workflow-principles

# Manage curated behavior rules in CLAUDE.md
/workflow-rules
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
Run Checks (format -> type -> lint -> security -> test)
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

- Run `/workflow-preflight` before every commit
- Use `--fix` in CI for automated formatting
- Use `--check-only` in CI for validation gates
- Align local checks with CI configuration

---

## Time Savings

**Per preflight check:**

- Manual checks: ~5-10 minutes (remembering commands, running each tool)
- With preflight: ~1-2 minutes (automated discovery and execution)

**Estimated monthly savings:**

- Preflight checks: Save ~2-4 hours

Plus improved code quality and a streamlined commit-to-PR flow.

---

## Plugin Details

- **Name:** AI-Workflow
- **Version:** 2.0.0
- **Type:** Development Workflow Automation
- **Features:**
  - Skills: `/workflow-preflight`, `/workflow-ship`, `/workflow-principles`, `/workflow-rules`
  - Security scanning: pnpm/npm/yarn audit, eslint-plugin-security, Semgrep (CLI or Docker)
  - Development principles: Context-aware CLAUDE.md generation with project discovery
  - Behavior rules: Curated, marker-wrapped rule library for user/project CLAUDE.md (cross-project sync via `/plugin update`)
- **License:** MIT
- **Author:** Charles Jones

---

## Contributing

Found a bug or have a suggestion? [Open an issue](https://github.com/charlesjones-dev/claude-code-plugins-dev/issues) or submit a pull request!

---

## License

MIT License - See [LICENSE](LICENSE) file for details.

---

**Built with love for the Claude Code community**
