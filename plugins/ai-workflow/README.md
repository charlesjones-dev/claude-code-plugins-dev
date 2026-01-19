# AI-Workflow Plugin

**AI-powered development workflow automation for Claude Code.** Phase-based planning, implementation orchestration, and preflight code quality checks for efficient sub-agent execution.

---

## What This Plugin Does

Provides tools for managing complex development workflows including breaking features into context-efficient phases, orchestrating multi-phase implementations via sub-agents, and running comprehensive code quality checks before commits or deployments.

### Key Capabilities

- **Phase Planning**: Break large features into properly-sized phases (30-50k tokens each) optimized for sub-agent execution
- **Implementation Orchestration**: Analyze dependencies and execute phases with optimal parallel/sequential strategies
- **Preflight Checks**: Auto-detect and run type checking, linting, formatting, security scanning, and tests across multiple ecosystems

---

## Available Commands

### `/workflow-plan-phases`

Create structured implementation plans from feature descriptions, optimized for context-efficient sub-agent execution.

**What it does:**

- Asks clarifying questions to understand scope and requirements
- Breaks features into right-sized phases (30-50k tokens each)
- Uses whole number phases only (no sub-phases like 1.1, 1.2)
- Defines clear acceptance criteria per phase
- Maps dependencies between phases
- Recommends execution strategy (parallel/sequential/mixed)
- Outputs structured markdown to `docs/plans/`

**Usage:**

```
/workflow-plan-phases "Build a user authentication system with OAuth, MFA, and session management"
/workflow-plan-phases --output=docs/plans/auth-system.md "Build authentication system..."
```

**Before (manual planning):**

```
# Manually break down feature into tasks
# Guess at task sizes and dependencies
# Hope sub-agents don't run out of context
# Lose track of what depends on what
```

**After (with ai-workflow plugin):**

```
/workflow-plan-phases "Build user authentication"
# Answers clarifying questions
# AI creates optimally-sized phases
# Dependencies clearly mapped
# Execution strategy recommended
# Plan saved to docs/plans/
```

### `/workflow-implement-phases`

Orchestrate multi-phase implementation from a plan document using intelligent parallel/sequential execution.

**What it does:**

- Parses plan documents and extracts phase definitions
- Analyzes dependencies (explicit and implicit)
- Determines optimal execution strategy
- Presents execution plan for user confirmation
- Executes via Task() sub-agents with coordination directory
- Handles failures gracefully (skips dependent phases, continues independent ones)
- Aggregates results and provides comprehensive summary

**Usage:**

```
/workflow-implement-phases @docs/plans/user-authentication.md
/workflow-implement-phases @docs/plans/feature.md --phases=1,2,3
/workflow-implement-phases @docs/plans/feature.md --strategy=parallel
```

**Execution Strategies:**

| Strategy | When Used | Benefits |
|----------|-----------|----------|
| **Parallel** | No dependencies between phases | Fastest execution, maximum context isolation |
| **Sequential** | Linear dependency chain | Safest execution, full context from prior phases |
| **Mixed** | Some independent, some dependent | Best of both worlds |

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

## Available Skills

### `plan-phases`

Methodology for creating implementation plans optimized for sub-agent execution. Provides:

- Question categories for gathering requirements
- Phase sizing guidelines (30-50k tokens target)
- Dependency planning strategies
- Plan document template
- Phase writing guidelines with examples
- Anti-patterns to avoid

**Auto-loads when:** Creating implementation plans, phase planning documents, or breaking features into phases.

### `implement-phases`

Methodology for analyzing plan documents and coordinating phase implementation. Provides:

- Plan document parsing heuristics
- Dependency detection algorithms (explicit and implicit)
- Execution strategy selection criteria
- Sub-agent prompt templates
- Error handling patterns
- Results aggregation templates

**Auto-loads when:** Implementing phases from a plan, orchestrating sub-agents, or when `/workflow-implement-phases` is invoked.

### `preflight-checks`

Comprehensive reference for code quality tools across ecosystems. Provides:

- Quick reference tables for all ecosystems
- Discovery strategy (project type, configured scripts, CI alignment)
- Best practices (execution order, monorepos, caching)
- Common error messages and solutions
- Pre-commit hook integration examples

**Auto-loads when:** Running quality checks, preparing commits, or when user mentions preflight, verify, lint, typecheck, or test commands.

---

## Quick Start

### Installation

```
/plugin install ai-workflow@claude-code-plugins-dev
```

### Usage

```
# Plan a new feature
/workflow-plan-phases "Add user profile editing with avatar upload"

# Review the generated plan
# Located at: docs/plans/user-profile-editing.md

# Implement the phases
/workflow-implement-phases @docs/plans/user-profile-editing.md

# Run preflight checks before committing
/workflow-preflight
```

---

## How It Works

### Phase Planning Flow

```
User Description
      |
      v
Clarifying Questions  <-- Never skipped
      |
      v
Requirements Analysis
      |
      v
Phase Sizing (30-50k tokens each)
      |
      v
Dependency Mapping
      |
      v
Execution Strategy
      |
      v
Plan Document (docs/plans/)
```

### Phase Implementation Flow

```
Plan Document
      |
      v
Parse Phases & Extract Specs
      |
      v
Analyze Dependencies
      |
      v
Build Execution Graph
      |
      v
Present Plan to User
      |
      v
Execute via Sub-Agents
      |
      v
Aggregate Results
      |
      v
Summary Report
```

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

### When to Use Phase Planning

- Large features that would exceed a single context window
- Complex implementations with multiple dependencies
- Team projects where different phases could be assigned to different people
- Features requiring careful dependency management

### Phase Sizing Guidelines

| Phase Size | Tokens | Files | Recommendation |
|------------|--------|-------|----------------|
| Too Small | <15k | 1 | Combine with related work |
| Right-Sized | 30-50k | 2-5 | Ideal for sub-agents |
| Too Large | >60k | 6+ | Split by layer, entity, or concern |

### Preflight Integration

- Run `/workflow-preflight` before every commit
- Use `--fix` in CI for automated formatting
- Use `--check-only` in CI for validation gates
- Align local checks with CI configuration

---

## Time Savings

**Per feature implementation:**

- Manual planning: ~1-2 hours (for complex features)
- With plan-phases: ~10-15 minutes

**Per preflight check:**

- Manual checks: ~5-10 minutes (remembering commands, running each tool)
- With preflight: ~1-2 minutes (automated discovery and execution)

**Estimated monthly savings:**

- Phase planning: Save ~4-8 hours
- Preflight checks: Save ~2-4 hours
- Total: Save ~6-12 hours/month

Plus improved code quality, fewer context overflows, and more efficient sub-agent execution.

---

## Plugin Details

- **Name:** AI-Workflow
- **Version:** 1.1.0
- **Type:** Development Workflow Automation
- **Features:**
  - Commands: `/workflow-plan-phases`, `/workflow-implement-phases`, `/workflow-preflight`
  - Skills: `plan-phases`, `implement-phases`, `preflight-checks`
  - Security scanning: pnpm/npm/yarn audit, eslint-plugin-security, Semgrep (CLI or Docker)
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
