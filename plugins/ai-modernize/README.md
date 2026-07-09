# AI Modernize Plugin

AI-powered codebase modernization assessment for identifying technical debt, anti-patterns, and quality issues from older AI-generated or legacy code.

## Overview

Codebases built with older AI models (Claude Sonnet 2/3, early Cursor, GPT-4 2024) or through "vibe coding" sessions often contain patterns that newer frontier models handle correctly. This plugin provides comprehensive assessment tools to identify these issues and produce prioritized remediation roadmaps with AI-assisted time estimates.

## Skills

### `/modernize-audit` - Full Interactive Assessment

Comprehensive, interactive modernization audit with configurable scope and categories.

**Features:**
- Interactive configuration via guided questions
- AI tool history awareness (adjusts assessment based on which tools generated the code)
- Auto-detects technology stack with user confirmation
- 12 assessment categories (selectable or run all)
- Configurable scan scope (entire solution or specific directory)
- Severity threshold filtering
- Detailed report with Modernization Score (0-100)
- AI-assisted remediation time estimates
- Phased modernization roadmap

**Usage:**
```bash
/modernize-audit
```

The skill will interactively ask about:
1. AI tools and models used to build the codebase
2. When the codebase was written
3. Technology stack confirmation
4. Which assessment categories to run
5. Audit scope
6. Severity threshold for the report

### `/modernize-scan` - Quick Scan

Fast, non-interactive scan that accepts a file or directory path. Runs all categories with default settings and produces a concise report.

**Usage:**
```bash
/modernize-scan ./src
/modernize-scan ./src/services/auth.ts
/modernize-scan ./packages/api
```

If no path is provided, it will ask for one.

## Agents

### `modernize-auditor`

Specialized agent that conducts automated codebase modernization audits in fresh context using the modernize-audit skill's methodology (12-category assessment, Modernization Score, phased roadmap). Automatically invoked by the `/modernize-audit` and `/modernize-scan` commands.

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
- AI-assisted remediation time estimates (not manual effort)
- Phased modernization roadmap with prioritized checklist
- "Why Older AI Models Did This" context for educational value

## Supported Technology Stacks

The plugin auto-detects and provides stack-specific analysis for:

- **JavaScript/TypeScript**: React, Vue, Nuxt, Next.js, Angular, Svelte, Express, Fastify, Node.js
- **C#/.NET**: ASP.NET Core, Blazor, Entity Framework, minimal APIs
- **Python**: Django, Flask, FastAPI, SQLAlchemy
- **Go**: Standard library, Gin, Echo, GORM
- **And more**: Analysis adapts to detected project configuration

## Plugin Details

| Field | Value |
|-------|-------|
| Version | 1.1.0 |
| Author | [Charles Jones](https://charlesjones.dev) |
| License | MIT |
| Repository | [claude-code-plugins-dev](https://github.com/charlesjones-dev/claude-code-plugins-dev) |
