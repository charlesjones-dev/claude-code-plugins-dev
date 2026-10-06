# AI Modernize Plugin

Codebase modernization assessment that finds technical debt, anti-patterns and quality issues in older AI-generated or legacy code.

## Overview

Codebases built with older AI tools (Claude 3-era models, early Cursor, GPT-4 in 2024) or through "vibe coding" sessions can contain patterns that newer models avoid. This plugin finds those issues and produces a prioritized remediation roadmap with time estimates that assume AI-assisted work.

## Skills

### `/modernize-audit`: Full Interactive Assessment

**Usage:**
```bash
/modernize-audit
```

The skill will interactively ask about:
1. AI tools and models used to build the codebase
2. When the codebase was written
3. Technology stack confirmation (auto-detected first)
4. Which of the 12 assessment categories to run
5. Audit scope (entire solution or a specific directory)
6. Severity threshold for the report

### `/modernize-scan`: Quick Scan

Fast, non-interactive scan that accepts a file or directory path. Runs all categories with default settings and produces a concise report.

**Usage:**
```bash
/modernize-scan ./src
/modernize-scan ./src/services/auth.ts
/modernize-scan ./packages/api
```

If you don't give a path, it asks for one.

## Agents

### `modernize-auditor`

Both skills hand the assessment to this agent, which runs it in a fresh context. You can also use it for unattended or scheduled audits.

## Assessment Categories

| # | Category | What It Checks |
|---|----------|---------------|
| 1 | SOLID/DRY/KISS Violations | God classes, duplicated logic, over-engineering, mixed paradigms, YAGNI |
| 2 | Type Safety & Language Misuse | `any` overuse, missing type guards, loose typing, language idiom violations |
| 3 | Error Handling | Empty catch blocks, swallowed errors, missing error boundaries, console.log debugging |
| 4 | Security Anti-patterns | Hardcoded secrets, missing validation, injection risks, insecure defaults |
| 5 | Performance Anti-patterns | N+1 queries, sync bottlenecks, missing pagination, full library imports |
| 6 | Testing Gaps | Implementation-coupled tests, over-mocking, missing edge cases, no integration tests |
| 7 | Architecture Debt | Tight coupling, circular deps, business logic in UI, missing abstraction layers |
| 8 | Frontend Debt | Prop drilling, state mismanagement, useEffect misuse, inline styles, missing a11y |
| 9 | Dependency Health | Deprecated packages, vulnerable versions, unnecessary imports, missing lock files |
| 10 | AI Hallucination Artifacts | Non-existent APIs, wrong signatures, hallucinated packages, deprecated methods |
| 11 | Modern Pattern Gaps | Missing modern syntax, outdated patterns, old CSS, legacy build tools |
| 12 | Configuration & DevOps Debt | Hardcoded config, missing env validation, no health checks, poor Docker practices |

## Report Output

Reports are saved to `/docs/modernize/` with timestamped filenames:

- **Full audit**: `YYYY-MM-DD-HHMMSS-modernize-audit.md`
- **Quick scan**: `YYYY-MM-DD-HHMMSS-modernize-scan.md`

### Report Includes

- Modernization Score (0-100) with category breakdown
- Findings grouped by severity (Critical, High, Medium, Low)
- Exact file paths and line numbers for every finding
- Before/after code examples for remediation
- Time estimates that assume AI-assisted work
- Phased modernization roadmap with prioritized checklist
- A "Why Older AI Models Did This" note on each finding

## Supported Technology Stacks

The plugin auto-detects the stack and adds language-specific checks for:

- **JavaScript/TypeScript**: React, Vue, Nuxt, Next.js, Angular, Svelte, Express, Fastify, Node.js
- **C#/.NET**: nullable reference types, async I/O, records, pattern matching, minimal APIs
- **Python**: type hints, f-strings, context managers, match statements, dataclasses

## Plugin Details

| Field | Value |
|-------|-------|
| Version | 1.1.1 |
| Author | [Charles Jones](https://charlesjones.dev) |
| License | MIT |
| Repository | [claude-code-plugins-dev](https://github.com/charlesjones-dev/claude-code-plugins-dev) |

## Contributing

Bug reports and fixes are welcome. See [CONTRIBUTING.md](../../CONTRIBUTING.md).
