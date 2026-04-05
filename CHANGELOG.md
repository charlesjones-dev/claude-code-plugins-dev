# Changelog

All notable changes to the Claude Code Plugins will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.3.3] - 2026-04-05

### Added

#### AI-Knowledge Plugin (v1.3.0)

- `/kb-query` - Query the knowledge base and synthesize answers from multiple KB files
  - Reads `_index.md` to find relevant pages, then drills into individual articles
  - Synthesizes comprehensive answers with `[[wiki-link]]` citations to source KB files
  - Flags contradictions between KB files and gaps in coverage
  - Offers to **file answers back as new KB articles** so explorations compound into the knowledge base
  - Filed answers include `type: synthesis`, `query`, and `sources` frontmatter fields for provenance
  - Inspired by Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern

- `/kb-obsidian` - One-time migration to upgrade and make an existing KB Obsidian-compatible
  - Adds `## Related` body sections with `[[wiki-links]]` for Obsidian graph view and link navigation
  - Migrates inline `### Global Learnings` from CLAUDE.md to `docs/kb/_global-learnings.md`
  - Generates `docs/kb/_index.md` — a categorized catalog of all KB articles with one-line summaries
  - Creates `docs/kb/_log.md` — a chronological record of KB operations
  - Offers to reorganize flat KB files into category folders (architecture/, conventions/, testing/, etc.)
  - Audits and fixes frontmatter health issues
  - Fully backwards-compatible — handles all older KB structures

- **`_index.md` — Knowledge Base Index** - Auto-generated, pinned catalog of all KB articles organized by category with one-line summaries. The LLM reads this first to find relevant pages before drilling into individual articles. Created by `/kb-init` and maintained by all `/kb-*` commands.

- **`_log.md` — Activity Log** - Append-only chronological record of KB operations (ingests, queries, prunes, etc.). Provides a timeline of how the knowledge base evolved. Created by `/kb-init` and appended to by all `/kb-*` commands.

- `/kb-organize` - Standalone folder reorganization for existing flat KB structures
  - Analyzes flat KB files and suggests category folders based on tags and content
  - Common categories: architecture/, conventions/, testing/, tools/, external/, domain/
  - Preview-first — shows all proposed moves before executing
  - Updates CLAUDE.md table paths and `_index.md` after reorganization
  - Does not modify `[[wiki-links]]` (they resolve by name, not path)

### Changed

#### AI-Knowledge Plugin (v1.3.0)

- **Subfolder organization** - All `/kb-*` commands that create new KB files now prefer placing them in category subfolders (e.g., `docs/kb/architecture/`, `docs/kb/conventions/`, `docs/kb/testing/`) instead of flat in the root. Existing flat structures continue to work. `/kb-obsidian` offers to reorganize flat files into folders.
- **Obsidian-compatible Related Links** - All `/kb-*` commands that create or update KB files now maintain a `## Related` section at the end of the file body with `[[wiki-links]]` mirroring the `related` frontmatter field. Obsidian does not parse frontmatter values as navigable links, so body links are required for graph view edges and link navigation to work.
- **Global Learnings as dedicated KB file** - Global learnings are now stored in `docs/kb/_global-learnings.md` (a pinned KB file) instead of inline in CLAUDE.md's `### Global Learnings` section. This makes global learnings visible in Obsidian, searchable as a regular KB file, and eliminates duplication. Affects `/kb-init`, `/kb-learn`, `/kb-add`, `/kb-search`, `/kb-list`, and `/kb-prune`. Existing inline global learnings are preserved and can be migrated with `/kb-obsidian`.
- **Index and log maintenance** - All `/kb-*` commands that modify KB files now update `_index.md` and append to `_log.md` (conditionally — only if the files exist, for backwards compatibility).
- **Cross-reference cleanup now includes body links** - `/kb-remove` and `/kb-prune` now update both `related` frontmatter AND `## Related` body sections when cleaning up cross-references.
- **kb-prune detects out-of-sync Related sections** - Cross-reference integrity checks now flag KB files where the `## Related` body section doesn't match the `related` frontmatter.
- **kb-list and kb-search detect legacy global learnings** - These commands now check for and flag legacy inline `### Global Learnings` sections in CLAUDE.md, suggesting `/kb-obsidian` for migration.

## [2.3.2] - 2026-04-03

### Added

#### AI-Knowledge Plugin (v1.2.0)

- `/kb-harvest` - Harvest knowledge from external sources into the KB system
  - Supports local directories, individual files, glob patterns, and web URLs as sources
  - Scans sibling git repos (e.g., `C:/Source/*/docs/**/*.md`) for cross-repo knowledge ingestion
  - Fetches and distills web pages (wikis, Confluence, internal docs) via URL
  - Auto-tags with `module:{name}` based on source directory structure for filtering by module
  - Tracks provenance via `source` frontmatter field (original path or URL) for future re-harvesting
  - Discovery report with pre-checked/unchecked sources and batch selection
  - Per-article content preview and approval before writing to disk
  - Distills content into concise, actionable KB format (not copy-paste)
  - Detects topic overlap with existing KB files and proposes appending
  - Registers entries in CLAUDE.md Knowledge Base table
  - Preserves all source files and URLs (never modifies originals)

- `/kb-discover` - Analyze source code to extract implicit knowledge into KB articles
  - Mines source code for architecture patterns, naming conventions, API contracts, error handling, config structures, data models, and testing patterns
  - Supports targeted analysis (specific directories), focus areas (topics), or full codebase scan with intelligent sampling
  - Auto-detects tech stack and prioritizes analysis targets accordingly
  - Groups findings into coherent KB articles (not raw category dumps)
  - Per-article draft preview and approval — user sees the full distilled content before any file is written
  - Tracks provenance via `discovered-from` frontmatter field for re-discovery when code evolves
  - Evidence-based only — requires observed repetition, never fabricates patterns from single occurrences
  - Right-sizes articles to 50-150 lines of distilled rules for context-friendly loading

## [2.3.1] - 2026-04-03

### Added

#### AI-Knowledge Plugin (v1.1.0)

- `/kb-ingest` - Ingest specific markdown files from anywhere in the project into the KB, as a targeted alternative to `/kb-absorb`
  - Accepts one or more file paths (e.g., `/kb-ingest docs/api-guide.md`)
  - Distills content into concise, actionable KB format with proper frontmatter
  - Detects overlap with existing KB files and proposes appending instead of creating duplicates
  - Registers new KB entries in the CLAUDE.md Knowledge Base table
  - Preserves source files (never modifies or deletes originals)

### Fixed

#### AI-Knowledge Plugin (v1.1.0)

- **Fixed pinned file loading instruction in kb-init** - The CLAUDE.md template previously told Claude to check frontmatter of every KB file to find pinned entries, defeating the purpose of the dynamic loading table. Now correctly directs Claude to use the "When to Load" column ("Always (pinned)") as the source of truth

## [2.3.0] - 2026-04-02

### Added

#### AI-Knowledge Plugin (v1.0.0) - NEW PLUGIN

- **New plugin for knowledge base management** - Capture conversation learnings, maintain topic-specific KB files, and dynamically reference institutional knowledge in CLAUDE.md
- `/kb-init` - Initialize the Knowledge Base section in CLAUDE.md and create `docs/kb/` directory (idempotent)
- `/kb-learn` - Analyze conversation to extract learnings, best practices, and institutional knowledge into KB files
- `/kb-add` - Quickly add a learning or rule to the KB with interactive location picker
- `/kb-import` - Register existing KB files in CLAUDE.md (accepts file path or scans for unregistered files, adds missing frontmatter)
- `/kb-list` - List all registered KB files with status, tags, dates, pinned status, and cross-references
- `/kb-search` - Search across KB files by keyword, topic, or tag (`tag:security`)
- `/kb-prune` - Interactive cleanup: stale refs, duplicates, merges, frontmatter health, cross-reference integrity
- `/kb-auto` - Toggle automatic knowledge capture at end of conversations (per-project)
- `/kb-absorb` - Migrate existing CLAUDE.md sections and docs/ content into the KB system with interactive approval
- `/kb-remove` - Remove a KB file and its CLAUDE.md reference (accepts optional path or interactive selection)
- All KB files use YAML frontmatter with `tags`, `related`, `created`, `last-updated`, `pinned`, and `scope` fields
- Cross-references between KB files via `related: [[other-file]]` frontmatter for linked knowledge loading
- Pinned KB files (`pinned: true`) are always loaded regardless of work context

## [2.2.2] - 2026-03-31

### Fixed

#### AI-ADO Plugin (v1.3.1)

- **Fixed skill name parsing** - Changed `ado-work-items` skill name from `Azure DevOps Work Items` (with spaces) to `ado-work-items` so Claude Code can parse it correctly (fixes #8)

## [2.2.1] - 2026-03-31

### Fixed

#### AI-Statusline Plugin (v1.2.3)

- **Fixed rate limit percentage display** - Rate limit percentages now round to 2 decimal places instead of showing long floating-point numbers (e.g., `5h:12.35%` instead of `5h:12.345678%`)
  - Bash: uses jq `(. * 100 | round) / 100` for rounding, extracts integer part for color threshold comparisons
  - PowerShell: uses `[math]::Round($val, 2)` instead of `[int]` cast which truncated to whole numbers

## [2.2.0] - 2026-03-31

### Added

#### AI-Security Plugin (v1.5.0)

- `/security-supply-chain` new skill for hardening projects against npm supply chain attacks
  - Detects package manager (pnpm, npm, Yarn, Bun) and validates compatibility
  - Configures pnpm's `minimum-release-age` in `.npmrc` to quarantine newly published packages
  - Interactive timeframe selection with previews (24 hours, 3 days, 7 days, or custom)
  - Scans CI/CD configs for frozen lockfile usage and offers to add `frozen-lockfile=true`
  - Checks pnpm version and offers upgrade if below 10.16.0 minimum
  - Recommends pnpm migration for npm/Yarn/Bun users who lack quarantine protection
  - Creates two defense layers: time-based quarantine (local dev) + frozen lockfile (CI/CD)

## [2.1.0] - 2026-03-22

### Added

#### AI-Modernize Plugin (v1.0.0) - NEW PLUGIN

- **New plugin for codebase modernization assessment** - Identifies technical debt, anti-patterns, and quality issues from older AI-generated or legacy code

- `/modernize-audit` interactive skill for comprehensive modernization assessment
  - Guided configuration: AI tool history, codebase era, tech stack detection, category selection, scope, severity threshold
  - 12 assessment categories: SOLID/DRY/KISS violations, type safety, error handling, security, performance, testing, architecture, frontend debt, dependency health, AI hallucination artifacts, modern pattern gaps, configuration/DevOps
  - Modernization Score (0-100) with category breakdown
  - AI-assisted remediation time estimates (not manual development time)
  - Phased modernization roadmap with prioritized checklist
  - "Why Older AI Models Did This" educational context for each finding
  - Delegates to `ai-modernize:modernize-auditor` subagent for deep analysis

- `/modernize-scan` quick scan skill for fast, targeted assessments
  - Accepts file or directory path argument (e.g., `/modernize-scan ./src`)
  - Runs all categories with default settings, no interactive questions
  - Auto-detects technology stack
  - Produces abbreviated report with same scoring and estimate format

- Reports saved to `/docs/modernize/` with timestamped filenames

#### AI-Workflow Plugin (v1.4.0)

- `/workflow-principles` new skill for generating context-aware Development Principles in CLAUDE.md
  - Automated project discovery: detects monorepo structure, tech stack, frameworks, validation libraries, state management, testing tools
  - Interactive configuration: principle categories (SOLID, DRY, KISS, YAGNI, modularity, components, type safety, error handling, testing)
  - Monorepo-aware: detects shared packages, maps dependency direction, generates shared package rules with real package names
  - Frontend-aware: generates component architecture rules tailored to detected framework (React, Vue, Angular, Svelte)
  - Smart merge: appends, replaces, or merges with existing CLAUDE.md content
  - Supports both project CLAUDE.md and user-level ~/.claude/CLAUDE.md
  - Custom rules support for project-specific conventions
  - Uses real package names, paths, and library names from the detected project (never generic placeholders)

#### AI-Compliance Plugin (v1.0.0) - NEW PLUGIN

- **New plugin for software license compliance auditing** - Detects open-source licenses, flags legal risks, and generates attribution files

- `/compliance-license-audit` interactive skill for comprehensive license compliance audit
  - Auto-detects project license with confirmation
  - Scans all dependency manifests across 8 package ecosystems (npm, pip, NuGet, Go, Rust, Ruby, PHP, Java)
  - Classifies licenses: Permissive, Weak Copyleft, Strong Copyleft, Unknown/None
  - License compatibility analysis against the project's own license
  - Flags copyleft contamination risks with configurable risk tolerance
  - Optional transitive dependency analysis via lock files
  - Source code scanning for license headers and vendored/copied code
  - License Compliance Score (0-100)
  - Identifies unfulfilled license obligations (missing NOTICE files, attribution)
  - Provides alternative components for incompatible dependencies

- `/compliance-notice-generate` interactive skill for generating attribution files
  - Four output formats: NOTICE, THIRD-PARTY-NOTICES.md, ATTRIBUTION.md, licenses.json
  - Configurable scope: production only, all dependencies, or custom groups
  - Optional full license text inclusion
  - Extracts actual copyright notices from LICENSE files
  - Handles dual-licensed packages and license exceptions
  - Detects existing attribution files with replace/create-alongside options

- Reports saved to `/docs/compliance/` with timestamped filenames

## [2.0.2] - 2026-03-19

### Added

#### AI-Statusline Plugin (v1.2.2)

- **Added rate limit usage display** - Shows 5-hour and 7-day rate limit percentages with color-coded thresholds (green <50%, yellow 50-79%, red 80%+)
  - New `SHOW_RATE_LIMITS` configuration option (enabled by default)
  - Reads `rate_limits.five_hour.used_percentage` and `rate_limits.seven_day.used_percentage` from the statusline JSON input
  - Requires Claude Code 2.1.80+ (gracefully hidden on older versions where the field is absent)
  - Updated both Bash and PowerShell script templates
  - Added to `/statusline-wizard` and `/statusline-edit` question flows

## [2.0.1] - 2026-02-17

### Fixed

#### AI-Statusline Plugin (v1.2.1)

- **Fixed PowerShell script template bugs**
  - Fixed stdin reading using reserved `$input` automatic variable; replaced with `[System.Console]::In.ReadToEnd()` so the script actually receives JSON data when invoked via `-File`
  - Fixed progress bar using ASCII `+`/`-` instead of Unicode `▓`/`░` to match bash template and documentation
  - Fixed segment separator using `" | "` instead of `" · "` to match bash template and README examples
  - Fixed unquoted paths in `Split-Path` and `git -C` that would break on directories with spaces
  - Fixed confusing cost format string `'${0:F2}'` that resembles a variable reference; clarified with string concatenation
  - Fixed Unicode character encoding by setting `[Console]::OutputEncoding` to UTF-8 and using `[char]` codes instead of literal Unicode in source file

## [2.0.0] - 2026-02-16

### Added

#### AI-Writing Plugin (v1.0.0)

- **New plugin for writing quality tools**
  - Detect and remove signs of AI-generated writing from text
  - Based on Wikipedia's "Signs of AI writing" guide maintained by WikiProject AI Cleanup

- `/writing-humanize` skill for removing AI writing patterns
  - Identifies 24 documented AI writing patterns across 6 categories: content, language/grammar, style, communication, filler/hedging, and personality
  - Rewrites problematic sections with natural alternatives while preserving meaning
  - Detects inflated significance, promotional language, superficial -ing analyses, vague attributions, overused AI vocabulary, em dash overuse, rule of three, negative parallelisms, sycophantic tone, and more
  - Includes full before/after examples for each pattern category

#### AI-Workflow Plugin (v1.3.0)

- **Added `/workflow-ship` skill for end-to-end shipping workflow**
  - Runs preflight checks (typecheck, lint, tests) via `/workflow-preflight`
  - Auto-fixes linting and formatting issues, bails early if fixes were applied so user can review
  - Interactive branch selection with `AskUserQuestion` (prevents direct commits to main/master)
  - Commits with proper Co-Authored-By trailer and HEREDOC formatting
  - Pushes to remote with automatic upstream tracking setup
  - Creates PR with dynamic target branch selection (detects staging/main availability)
  - PR body includes summary bullets, test plan, and Claude Code attribution
  - Safety guards: never force pushes, never skips preflight, never commits secrets

### Changed

#### All Plugins

- **Migrated all commands to skills** - eliminated `commands/` directories across all 8 remaining plugins
  - All 21 slash commands now use the skills system exclusively, removing duplicate entries
  - Standalone commands converted to skill directories with `SKILL.md` files
  - Command+skill pairs merged into unified skill files (command workflow first, skill expertise below)
  - All skills include `disable-model-invocation: true` to prevent auto-invocation
  - Slash command names remain unchanged; no user-facing changes to invocation

#### AI-Accessibility Plugin (v1.4.0)

- Merged `/accessibility-audit` command into `accessibility-audit` skill
- **Overhauled accessibility audit skill for conciseness, WCAG 2.2 coverage, and pattern alignment with peer plugins**
  - Reduced SKILL.md from 1542 to 787 lines (~49% reduction) while preserving all functional content
  - Added WCAG 2.2 criteria to 4 expertise areas: Keyboard (SC 2.4.11, 2.4.13), Forms (SC 3.3.7, 3.3.8, 3.3.9), Interactive (SC 3.2.6), Responsive (SC 2.5.7, 2.5.8)
  - Added "WCAG 2.2 New Criteria" subsection with all 9 new success criteria and note on SC 4.1.1 Parsing removal
  - Removed standalone "Playwright MCP Visual Accessibility Testing" expertise area (area 9); Playwright workflow consolidated into Audit Methodology
  - Removed standalone "Code Remediation Examples" section (239 lines); findings already include remediation blocks
  - Removed "Component-Level Accessibility Assessment" from report template (duplicated findings section)
  - Reduced report template from 734 to ~186 lines with 2 format-demonstrating sample findings and clear placeholders
  - Consolidated Audit Methodology from 137 to ~48 lines with numbered checklists referencing expertise areas by name
  - Replaced "elite Accessibility Scanner" intro with professional, concise description
  - Tightened severity framework to criteria-only descriptions matching security-audit pattern
  - Added 3 concise before/after examples (Form Labels, Focus Indicators, ARIA Widget Pattern) replacing 6 verbose examples
  - Trimmed Best Practices (8 to 6), QA Checklist (10 to 8), Context-Aware (5 to 4), removed closing paragraph from Communication
- **Fixed agent skill reference**: `accessibility-auditing` to `accessibility-audit` in `accessibility-auditor` agent

#### AI-ADO Plugin (v1.3.0)

- Converted 6 commands to skills: `/ado-init`, `/ado-create-feature`, `/ado-create-story`, `/ado-create-task`, `/ado-log-story-work`, `/ado-timesheet-report`

#### AI-Git Plugin (v1.2.0)

- Converted 2 commands to skills: `/git-init`, `/git-commit-push`
- **Added `/git-commit-push-pr` skill for commit, push, and PR workflow**
  - Interactive branch selection with `AskUserQuestion` (prevents direct commits to main/master)
  - Commits with proper Co-Authored-By trailer and HEREDOC formatting
  - Pushes to remote with automatic upstream tracking setup
  - Creates PR with dynamic target branch selection (detects staging/main availability)
  - PR body includes summary bullets, test plan, and Claude Code attribution
  - Lightweight alternative to `/workflow-ship` without preflight checks
  - Safety guards: never force pushes, never commits secrets
- **Hardened `/git-commit-push` skill with safety improvements from `/git-commit-push-pr`**
  - Branch safety: blocks commits directly to main/master, suggests creating a feature branch
  - Smart file staging: prefers specific files by name over `git add .` or `git add -A`
  - Secrets detection: skips `.env`, `credentials.*`, `*.key`, `*.pem`, and other secret-like files
  - Upstream tracking: checks for remote tracking branch and uses `-u` flag when needed
  - HEREDOC formatting: uses HEREDOC for commit messages to ensure proper formatting
  - No-changes guard: detects empty state and stops early
  - Explicit safety rules: never force push, never use `git status -uall`
  - Structured step-by-step flow replacing flat numbered list
- **Improved `/git-init` skill with expanded technology support and lock file handling**
  - Added Swift/iOS detection (`Package.swift`, `*.xcodeproj`, `*.xcworkspace`) with Xcode, SPM, CocoaPods, Carthage, and Fastlane patterns
  - Added Flutter/Dart detection (`pubspec.yaml`) with platform-specific patterns for Android and iOS build artifacts
  - Added C/C++ detection (`CMakeLists.txt`, `Makefile`, `*.vcxproj`, `meson.build`) with compiled object and CMake patterns
  - Added Deno detection (`deno.json`, `deno.jsonc`, `deno.lock`)
  - Added Nuxt-specific build outputs (`.output/`, `.nitro/`, `.data/`) to Node.js patterns
  - Fixed Rust `Cargo.lock` handling: now commented out with guidance (commit for apps, ignore for libraries)
  - Fixed PHP `composer.lock` handling: now commented out with guidance (commit for apps, ignore for libraries)
  - Fixed Python `*.ipynb`: changed from default-ignore to commented out (many projects commit notebooks)
  - Fixed Go `go.work`: changed from default-ignore to commented out (some teams commit it)
  - Added `.env.template` and `.env.sample` negation patterns alongside `.env.example`
  - Updated lock file handling docs to cover Rust and PHP alongside Node.js

#### AI-Learn Plugin (v1.1.0)

- Converted 2 commands to skills: `/learn`, `/learn-review`

#### AI-Performance Plugin (v1.2.0)

- Merged `/performance-audit` command into `performance-audit` skill
- **Overhauled performance audit skill for technology-agnostic, modern analysis**
  - Replaced .NET-centric report template with stack-agnostic placeholders that adapt to any project
  - Removed pre-filled example findings (P-001 through P-007) from template; agent now discovers real findings only
  - Added Core Web Vitals (LCP, INP, CLS) as primary frontend metrics, replacing outdated FCP/TTI focus
  - Added severity scoring criteria with 1.0-10.0 scale, defined thresholds, and weighted scoring factors
  - Added framework-aware frontend guidance for React, Vue, Svelte, and Angular (previously React-only)
  - Added new "Concurrency and Thread Safety" section covering race conditions, deadlocks, connection pool exhaustion, and event loop blocking
  - Added new "Memory Performance" section with platform-specific patterns for JavaScript/Node.js and managed languages (.NET, Java, Go)
  - Added new "Observability" section covering metrics, logs, and distributed tracing (OpenTelemetry, Jaeger)
  - Added streaming/SSR performance guidance (React Server Components, Nuxt, SvelteKit, edge rendering)
  - Added GraphQL performance patterns (query depth limiting, DataLoader, persisted queries)
  - Added bundle analysis and tree-shaking to asset optimization guidance
  - Added Node.js event loop blocking example to skill examples
  - Enhanced asset loading example with modern formats (AVIF, WebP) and `<picture>` element
  - Added concurrency anti-patterns section (shared mutable state, deadlocks, connection pool exhaustion)
  - Expanded QA checklist with rollback planning, realistic data volume testing, and error path verification
  - Added template requirements for stack detection and instructions to tailor findings to project technology

#### AI-Security Plugin (v1.4.0)

- Converted `/security-init` command to skill
- Merged `/security-audit` command into `security-audit` skill
- Merged `/security-scan-dependencies` command into `security-scan-dependencies` skill
- **Overhauled security audit skill with modern attack coverage and placeholder-based templates**
  - Replaced hardcoded fake example data in report template (e.g., `src/Website.Data/Services/UserService.cs:45`) with placeholder guidance pattern (`[exact/file/path.ext:line_number]`) to prevent models from copying template examples verbatim
  - Added explicit template requirements: replace all bracketed placeholders, tailor code to detected stack, show "No [severity] issues identified" for empty severity levels
  - Added severity scoring table with 1.0-10.0 scale, defined thresholds, criteria, examples, and weighted scoring factors (exploitability, impact scope, data sensitivity, attack complexity, blast radius)
  - Added new "Supply Chain Security" section covering dependency confusion, typosquatting, lock file integrity, build pipeline secrets, Dockerfile security, and GitHub Actions injection
  - Added new "Modern API Attack Vectors" section covering GraphQL introspection/batching/depth attacks, WebSocket auth/rate limiting, SSRF cloud metadata endpoints, and API key leakage in client bundles
  - Added new "Modern Authentication Patterns" section covering passkeys/WebAuthn, OAuth 2.1/PKCE, JWT algorithm confusion, token lifecycle, and session fixation in SPAs
  - Added "Technology-Specific Security Considerations" section with language-specific vulnerabilities for Node.js (prototype pollution, ReDoS), Python (pickle, SSTI), .NET (XXE, BinaryFormatter), and Go (request smuggling, goroutine races)
  - Added 2 new examples: JWT algorithm confusion (JavaScript) and SSRF prevention (Python), bringing total to 5 multi-language examples
  - Added `allowed-tools` frontmatter to all 3 skills
- **Overhauled dependency scanning skill with expanded library detection and placeholder templates**
  - Replaced hardcoded findings (jQuery CVE, Bootstrap CVE, WordPress version, CSP header, Referrer-Policy examples) with placeholder guidance patterns
  - Fixed incorrect Context7 tool reference: `mcp__context7__get-library-docs` to `mcp__context7__query-docs`
  - Updated scanner version from v1.0 to v1.4.0 in report template
  - Expanded UI framework detection: added Solid.js, Lit, Alpine.js, HTMX, Qwik
  - Renamed "Server Frameworks" to "Meta-Frameworks" and added Remix, SvelteKit, Astro
  - Added meta-framework detection methods (Next.js `__NEXT_DATA__`, Nuxt `__NUXT__`, Remix `__remixContext`, SvelteKit `__sveltekit_`, Astro `astro-island`, Gatsby `___gatsby`)
  - Added headless CMS detection: Strapi, Sanity, Contentful, Payload CMS
  - Expanded build tool detection: added esbuild, SWC, Turbopack
  - Expanded analytics detection: added Plausible, PostHog
  - Added recent CVE examples: Lodash prototype pollution (CVE-2021-23337), Next.js SSRF (CVE-2024-34351), jsonwebtoken (CVE-2022-23529), Axios SSRF, Angular.js EOL
- **Enhanced security-init skill with expanded technology support**
  - Added Deno detection (`deno.json`, `deno.lock`) with `.deno/**` deny patterns
  - Added Swift/iOS detection (`Package.swift`, `*.xcodeproj`) with `.build/**`, `DerivedData/**`, `Pods/**` deny patterns
  - Added Kotlin/Android detection (`build.gradle.kts`, `AndroidManifest.xml`) with `build/**`, `.gradle/**`, `local.properties` deny patterns
  - Added Terraform/IaC detection (`*.tf`, `*.tfvars`) with `*.tfstate`, `.terraform/**` deny patterns
  - Added Kubernetes detection (`kustomization.yaml`, `Chart.yaml`) with `**/secrets.yaml` deny patterns
  - Added base security patterns: CI/CD secrets (`.github/secrets/**`), package manager auth (`.npmrc`, `.yarnrc.yml`), deployment configs (`.vercel/**`, `.netlify/**`)
  - Added post-install verification step to confirm settings were saved correctly
- **Fixed agent skill references**
  - `security-auditor` agent: `security-auditing` to `security-audit`, fixed `it's` to `its`, expanded focus areas with modern attack vectors
  - `security-dependency-scanner` agent: `security-dependency-scanning` to `security-scan-dependencies`, expanded focus areas with meta-frameworks, headless CMS, and build tools

#### AI-Statusline Plugin (v1.2.0)

- Merged `/statusline-wizard` command into `statusline-wizard` skill
- Converted `/statusline-edit` command to skill

#### AI-Workflow Plugin (v1.3.0)

- Merged `/workflow-plan-phases` command into `workflow-plan-phases` skill
- Merged `/workflow-implement-phases` command into `workflow-implement-phases` skill
- Merged `/workflow-preflight` command into `workflow-preflight` skill
- Renamed `/ship` skill to `/workflow-ship` for naming consistency

### Removed

#### AI-Plugins Plugin

- **Removed ai-plugins plugin entirely** - Claude Code handles plugin creation natively

## [1.9.1] - 2026-01-18

### Added

#### AI-Workflow Plugin (v1.1.0)

- **Added security scanning detection to `/workflow-preflight` command**
  - Detects and runs `pnpm audit`, `npm audit`, `yarn audit` for dependency vulnerability scanning
  - Detects `eslint-plugin-security` in devDependencies and notes when security linting is active
  - Universal Semgrep detection via multiple sources:
    - Package.json scripts (e.g., `pnpm run semgrep`)
    - Config files: `.semgreprc.yml`, `.semgrep.yml`, `semgrep.yml`, `.semgrep/`
    - CI workflows: `.github/workflows/*.yml` (extracts `--config` flags)
    - README.md documentation (Security sections)
    - Local CLI availability
    - Docker fallback when semgrep CLI not installed
  - Added Python (`pip-audit`, `safety`) and Rust (`cargo audit`) dependency scanning
  - Updated preflight skill with security scanning quick reference table

## [1.9.0] - 2026-01-14

### Added

#### AI-Learn Plugin (v1.0.0)

- **New plugin for Socratic learning mode**
  - Transforms Claude from code generator to patient coding mentor
  - Guides users through problem-solving without providing direct answers
  - Based on productive struggle methodology for retained knowledge

- `/learn` command for activating teaching mode
  - 5-phase teaching flow: Assessment, Foundation, Guided Implementation, Error Discovery, Reinforcement
  - Socratic questioning instead of direct answers
  - Hints and guidance rather than solutions
  - Escape hatch for users who explicitly request answers

- `/learn-review` command for Socratic code review
  - Reviews code through targeted questions
  - Helps users discover bugs by tracing through edge cases
  - Probes design decisions to deepen understanding
  - Question banks for logic, performance, readability, and security concerns

## [1.8.0] - 2025-12-18

### Added

#### AI-Accessibility Plugin (v1.3.0)

- **Added Section 508 / WCAG 2.0 AA option** to `/accessibility-audit` command
  - New "508 / WCAG 2.0 AA" option in WCAG version selection
  - Supports US federal accessibility requirements aligned with WCAG 2.0 Level AA

## [1.7.1] - 2025-12-17

### Fixed

#### AI-Statusline Plugin (v1.1.1)

- **Fixed PowerShell progress bar using incompatible Unicode characters**
  - Replaced `▓` and `░` with ASCII-compatible `#` and `-` characters
  - Ensures progress bar displays correctly on Windows environments

## [1.7.0] - 2025-12-16

### Added

#### AI-Statusline Plugin (v1.1.0)

- **New plugin for custom status line configuration**
  - Interactive setup wizard for configuring Claude Code's status line
  - Cross-platform support (bash for Mac/Linux, PowerShell for Windows)
  - Visual progress bar for context usage with color-coded thresholds
  - 9 configurable display options with sensible defaults

- `/statusline-wizard` command for interactive status line setup
  - Multi-step wizard using AskUserQuestion for configuration
  - Automatic OS detection for appropriate script selection
  - Backs up existing scripts and settings before overwriting
  - Makes scripts executable on Mac/Linux with `chmod +x`

- `/statusline-edit` command for editing existing configuration
  - Detects existing status line script and reads current settings
  - Pre-selects wizard options based on current configuration values
  - Updates only the configuration variables, preserving script logic
  - Directs users to `/statusline-wizard` if no script exists

- `statusline-setup` skill with complete script templates
  - Bash script template with all configurable variables
  - PowerShell script template with all configurable variables
  - Setup workflow documentation

- Configurable elements:
  - Model name (e.g., "Claude Opus 4.5")
  - Token count (e.g., "50k/100k")
  - Progress bar with percentage
  - Current directory
  - Git branch
  - Session cost (hidden by default)
  - Session duration
  - Current time
  - Claude Code version

## [1.6.3] - 2025-12-13

### Fixed

#### AI-Workflow Plugin (v1.0.3)

- **Fixed `/workflow-implement-phases` not using sub-agents for phase implementations**
  - Added explicit "Critical Requirements" section mandating Task() sub-agent usage for every phase
  - Added "CRITICAL: Mandatory Sub-Agent Requirement" section to implement-phases skill
  - Clarified orchestrator role: read plans, analyze dependencies, spawn sub-agents only
  - Added correct/wrong pattern examples showing Task() usage vs direct implementation
  - Updated parallel and sequential execution patterns with explicit Task() call examples
  - Prevents main agent from implementing phases directly, ensuring context isolation

## [1.6.2] - 2025-12-12

### Fixed

#### AI-Workflow Plugin (v1.0.2)

- **Fixed `/workflow-plan-phases` proceeding to implementation after creating plan**
  - Added explicit "Instructions" section with step-by-step workflow
  - Added "Important" section emphasizing planning-only scope
  - Command now stops after presenting the plan and directs users to `/workflow-implement-phases` for execution
  - Updated skill file with "IMPORTANT: Planning Only — Do Not Implement" section

- **Fixed `/workflow-implement-phases` not reading the plan file argument**
  - Added explicit "Instructions" section telling Claude to read the plan file
  - Added automatic plan discovery: if no file provided, searches `docs/plans/` and lets user pick
  - Plan file argument is now optional (defaults to searching `docs/plans/`)
  - Updated workflow step 1 to explicitly use Read tool for plan document

## [1.6.1] - 2025-12-10

### Changed

#### All Plugins

- **Added YAML frontmatter to all command files** with `name` and `description` attributes
  - Standardizes command metadata across all 17 commands in 7 plugins
  - Enables better command discovery and documentation
  - Follows the pattern established by ai-workflow plugin

#### AI-Workflow Plugin (v1.0.1)

- **Renamed commands to use `workflow-` prefix** for consistency with other plugins
  - `/plan-phases` → `/workflow-plan-phases`
  - `/implement-phases` → `/workflow-implement-phases`
  - `/preflight` → `/workflow-preflight`

## [1.6.0] - 2025-12-10

### Added

#### AI-Workflow Plugin (v1.0.0)

- **New plugin for development workflow automation**
  - Phase-based planning and implementation orchestration for efficient sub-agent execution
  - Preflight code quality verification system

- `/plan-phases` command for creating structured implementation plans
  - Breaks features into context-efficient phases (30-50k tokens each)
  - Whole number phases only (no sub-phases like 1.1, 1.2)
  - Clear acceptance criteria per phase
  - Dependency mapping with execution strategy recommendations
  - Outputs structured markdown to `docs/plans/`

- `/implement-phases` command for orchestrating multi-phase implementation
  - Parses plan documents and extracts phase definitions
  - Analyzes dependencies (explicit and implicit)
  - Determines optimal execution strategy (parallel/sequential/mixed)
  - Executes via Task() sub-agents with coordination directory
  - Aggregates results and provides comprehensive summary

- `/preflight` command for code quality checks
  - Auto-detects configured quality tools across ecosystems (Node.js, Python, .NET, Go, Rust)
  - Runs type checking, linting, formatting checks, and tests
  - Interactive fix mode with user consent
  - Supports `--fix`, `--check-only`, and `--verbose` arguments

- `plan-phases` skill with methodology for context-efficient phase sizing and dependency analysis
- `implement-phases` skill with dependency detection algorithms and execution patterns
- `preflight-checks` skill with comprehensive reference for quality tools across languages

### Changed

#### AI-Accessibility Plugin (v1.2.0)

- **Improved Playwright MCP detection flow** in `/accessibility-audit` command
  - Added "Skip visual testing" option when Playwright MCP tools are unavailable
  - Users can now proceed with code-based analysis without creating `.mcp.json`
  - Better handles cases where Playwright is installed globally via Claude Code `/mcp` command
- **Enhanced Accessibility Audit Skill with Improved Prompt Engineering**
  - Improvements for more accurate and actionable reports
  - Added **Code Context Accuracy** section with explicit guidance on when to include/omit code snippets
    - MUST show code when elements exist but lack attributes (e.g., missing alt, missing labels)
    - MUST omit code context when elements truly don't exist (e.g., no skip link present)
    - Prevents placeholder/guessed code in reports
  - Added **Specificity Requirements** section for precise element identification
    - Location field must enumerate specific elements, not generic descriptions
    - Code Context must show ALL affected elements (or first 3-5 if many)
    - Remediation examples must use actual values from the codebase, not placeholders
  - Enhanced **Severity Assessment Framework** with concrete examples for each level
  - Added clickable WCAG Understanding document links to compliance matrix
  - Standardized finding format with consistent bullet-point structure
  - Improved guidance on text readability with complex backgrounds (gradients, images, patterns)

## [1.5.4] - 2025-01-17

### Fixed

#### AI-Security Plugin (v1.3.2)

- **Fixed `/security-scan-dependencies` to require WebFetch or curl for HTTP header retrieval**
  - Updated command and skill documentation to explicitly prohibit Playwright or MCP browser tools
  - Added critical tool requirement section explaining that HTTP security headers (especially Content-Security-Policy) can ONLY be retrieved via WebFetch or curl
  - Browser automation tools cannot access raw HTTP response headers needed for security header analysis
  - Added "Required Tools" section to `security-dependency-scanning` skill with approved/prohibited tool lists
  - Enhanced scanning methodology with explicit WebFetch/curl usage examples
  - Updated quality assurance checklist to verify correct tool usage
  - Prevents incomplete security scans due to missing HTTP header analysis

## [1.5.3] - 2025-01-04

### Fixed

#### Marketplace

- Updated plugin versions in `marketplace.json` to match the versions in each `plugin.json` manifest

#### AI-Accessibility Plugin (v1.1.1)

- Accessibility scanning command `/accessibility-audit` now properly checks to see if Playwright MCP is installed before proceeding with an accessibility audit

## [1.5.2] - 2025-01-04

### Changed

#### AI-Accessibility Plugin (v1.1.0)

- **Added URL Accessibility Scanning** with optional Playwright MCP integration
  - New "a URL" option in scope selection for scanning live websites
  - Interactive Playwright MCP setup with automatic `.mcp.json` configuration
  - OS detection for Windows vs Linux/Mac Playwright configuration
  - Visual accessibility testing when Playwright MCP is available:
    - Real-time color contrast measurements of rendered elements
    - Visual verification of focus indicators
    - Accessibility tree analysis as perceived by assistive technologies
    - Keyboard navigation testing on live pages
    - Touch target size verification with actual pixel measurements
    - Screenshot-based visual accessibility assessment
  - Enhanced audit reports with screenshot evidence for visual findings
  - Screenshots saved to `/docs/accessibility/screenshots/` directory
- Updated `/accessibility-audit` command to support URL scanning with Question 4 for Playwright MCP preference
- Enhanced `accessibility-auditor` agent with dual analysis approach (codebase vs URL with Playwright)
- Enhanced `accessibility-audit` skill with Playwright MCP expertise and visual testing methodology

#### All Plugins

- **Improved Command Usage Documentation** to prevent erroneous argument passing
  - Added prominent command usage note in README.md clarifying that all commands are invoked without arguments
  - Added explicit "no arguments" instruction to all 13 command files across all plugins
  - Commands now explicitly state they will ignore any passed arguments and prompt interactively for all necessary information
  - Affected plugins:
    - AI-Accessibility (v1.1.0): `/accessibility-audit`
    - AI-Security (v1.3.1): `/security-audit`, `/security-init`, `/security-scan-dependencies`
    - AI-Performance (v1.1.2): `/performance-audit`
    - AI-Git (v1.1.1): `/git-init`, `/git-commit-push`
    - AI-Plugins (v1.2.2): `/plugins-scaffold`
    - AI-ADO (v1.2.2): `/ado-init`, `/ado-create-feature`, `/ado-create-story`, `/ado-create-task`, `/ado-log-story-work`, `/ado-timesheet-report`

## [1.5.1] - 2025-11-01

### Added

#### AI-Security Plugin (v1.3.0)

- `/security-scan-dependencies` command for scanning deployed websites
  - Web dependency security scanning without source code access
  - Interactive URL input and configurable scan scope (libraries, CMS, security headers, or comprehensive)
  - Frontend library detection: jQuery, React, Vue, Angular, Bootstrap, Tailwind, and more via CDN pattern matching
  - CMS platform detection with version identification:
    - Open source: WordPress, Drupal, Joomla
    - Enterprise .NET: Umbraco, Sitecore, Optimizely, Kentico
  - HTTP security headers analysis (CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy)
  - Context7 MCP integration for latest version verification
  - Known CVE identification with CVSS v3.1 severity scoring
  - Timestamped reports with severity-based findings (C-001, H-001, M-001, L-001 format)
  - Hybrid Agent + Skill architecture with `security-dependency-scanner` agent and `security-dependency-scanning` skill
- Use cases: Third-party website assessment, pre-acquisition due diligence, supply chain security analysis

## [1.5.0] - 2025-10-29

### Added

#### AI-Accessibility Plugin (v1.0.0)

- `/accessibility-audit` command with WCAG 2.1/2.2 compliance checking
  - Interactive configuration for WCAG version (2.1/2.2), conformance level (A/AA/AAA), and audit scope
  - Comprehensive pattern detection: semantic HTML, ARIA, keyboard navigation, color contrast, forms, images, screen readers
  - Timestamped reports with severity-based findings, WCAG compliance matrix, and code remediation examples
  - Hybrid Agent + Skill architecture with `accessibility-auditor` agent and `accessibility-auditing` skill

#### Marketplace Documentation

- Added "Note on Audit Plugins" section clarifying audit plugins are developer-focused static code analysis tools
- Emphasizes plugins complement (not replace) runtime testing tools and professional services

### Changed

#### AI-Security Plugin (v1.2.1)

- Standardized audit plugin structure
- Renamed skill from `security-audit` to `security-auditing`
- Reduced command file complexity: 402→80 lines
- Moved comprehensive report templates from command file to SKILL.md file (single source of truth)
- Renamed skill to use 'auditing' suffix

#### AI-Performance Plugin (v1.1.1)

- Standardized audit plugin structure
- Renamed agent from `performance-optimizer` to `performance-auditor`
- Renamed skill from `performance-audit` to `performance-auditing`
- Reduced command file complexity: 471→36 lines
- Moved comprehensive report templates from command file to SKILL.md file (single source of truth)
- Renamed skill to use 'auditing' suffix

## [1.4.1] - 2025-10-24

### Fixed

#### AI-ADO Plugin (v1.2.1)

- **Fixed `/ado-timesheet-report` command**
  - Migrated from non-existent `wit_query` to `wit_my_work_items` MCP tool with client-side filtering
  - Fixed date range filtering to use date-only comparison (prevents time-of-day issues)
  - Fixed day-of-week calculation using platform-specific system commands (PowerShell on Windows, `date` on Mac/Linux)
  - Prevents off-by-one errors in current week date range calculations

### Changed

- Condensed changelog entries across all versions for improved readability while maintaining essential information

## [1.4.0] - 2025-10-23

### Added

#### AI-ADO Plugin (v1.2.0)

- `/ado-timesheet-report` command for generating flexible weekly timesheet reports
  - Flexible task filtering (closed only, worked on only, or both)
  - Multiple date field support (Closed Date or Changed Date)
  - Three grouping modes (by hierarchy, by date, or by date with hierarchy)
  - Three verbosity levels (ID & hours, with titles, or with descriptions)
  - Flexible week definitions (Monday-Sunday or Sunday-Saturday)
  - User filtering (current user or specific team member)
  - Summary statistics and formatted reports with emoji icons

## [1.3.0] - 2025-10-21

### Added

#### AI-ADO Plugin (v1.1.0)

- **AI-Powered Work Item Generation** for `/ado-create-feature`, `/ado-create-story`, and `/ado-create-task` commands
  - AI generates titles, descriptions, persona statements, and acceptance criteria
  - Review and confirmation workflow with override options
  - Analyzes CLAUDE.md for naming conventions and standards
  - Context-aware generation using parent work item details

- `/ado-log-story-work` command for rapid work logging to User Stories
  - Creates tasks with completed hours pre-populated
  - AI-powered or manual task generation
  - Automatic git commit hash detection
  - Optional placeholder task hour subtraction

#### AI-Security Plugin (v1.2.0)

- **Hybrid Agent + Skill Architecture** with `security-audit` skill for optimal context efficiency
  - Progressive disclosure design: metadata loads first, full skill loads only when needed
  - Interactive security audits without consuming context until relevant

#### AI-Performance Plugin (v1.1.0)

- **Hybrid Agent + Skill Architecture** with `performance-audit` skill for optimal context efficiency
  - Progressive disclosure design: metadata loads first, full skill loads only when needed
  - Interactive performance analysis without consuming context until relevant

#### AI-Plugins Plugin (v1.2.0)

- **Plugin Development Skills** for interactive plugin and skill creation
  - New `plugins-scaffold` and `skills-scaffold` skills
  - Auto-loads when creating plugins, manifests, commands, agents, skills, or hooks

#### AI-ADO Plugin (v1.1.0)

- **Azure DevOps Work Items Skill** for MCP-powered work item management
  - New `ado-work-items` skill enforcing proper hierarchy and naming conventions
  - HTML formatting guidance and best practices
  - Auto-loads when using Azure DevOps MCP server tools

### Changed

#### AI-Security Plugin (v1.2.0)

- Converted `security-auditor` agent to lightweight wrapper that loads `security-audit` skill in fresh context

#### AI-Performance Plugin (v1.1.0)

- Converted `performance-optimizer` agent to lightweight wrapper that loads `performance-audit` skill in fresh context

### Fixed

#### AI-ADO Plugin (v1.1.0)

- Fixed `/ado-create-story` to properly set acceptance criteria in dedicated field instead of Description field

## [1.2.0] - 2025-10-20

### Added

#### AI-Git Plugin (v1.1.0)

- `/git-init` command for automated .gitignore generation
  - Intelligent technology detection (Node.js, Python, .NET, Go, Rust, PHP, Ruby, Java, Docker, React/Next.js, Vue, Terraform)
  - Comprehensive pattern generation (80+ patterns based on tech stack)
  - Smart merge strategies with preview and confirmation workflow

#### AI-ADO Plugin (v1.0.0)

- `/ado-init` command for Azure DevOps configuration and MCP server setup
  - Interactive configuration for organization, project, team, area path, and iteration path
  - Automatic CLAUDE.md configuration with work item hierarchy standards
  - Optional `.mcp.json` creation for MCP server integration
  - Cross-platform support with PAT authentication guidance

- `/ado-create-feature` command for creating Feature work items
  - Interactive prompts for title and description with HTML formatting
  - Returns Feature ID with Azure DevOps web link

- `/ado-create-story` command for creating User Story work items
  - Interactive prompts for parent Feature, title, persona statement, acceptance criteria, and story points
  - HTML formatted with Given-When-Then acceptance criteria

- `/ado-create-task` command for creating Task work items
  - Interactive prompts for parent User Story, title, and hour estimate
  - Hour tracking with Original Estimate and Remaining Work fields

### Changed

#### AI-Git Plugin (v1.1.0)

- Renamed `/commit-push` command to `/git-commit-push` for consistency with `/git-init` naming convention

#### AI-Plugins Plugin (v1.1.0)

- Renamed `/scaffold-plugin` command to `/plugins-scaffold` for consistency with plugin naming convention

## [1.1.0] - 2025-10-19

### Added

#### AI-Security Plugin (v1.1.0)

- `/security-init` command for automated security settings initialization
  - Intelligent technology detection with comprehensive file denial patterns (40-60+ based on tech stack)
  - Smart merge strategies with preview and confirmation workflow

### Changed

#### AI-Security Plugin (v1.1.0)

- Enhanced `/security-audit` with pre-audit configuration check recommending `/security-init` for users with fewer than 4 deny rules

## [1.0.1] - 2025-10-17

### Added

#### AI-Plugins Plugin (v1.0.0)

- Initial release with `/scaffold-plugin` command for interactive plugin scaffolding (later renamed to `/plugins-scaffold`)
  - AI-assisted plugin creation with automatic directory structure, metadata, and marketplace registration

## [1.0.0] - 2025-10-17

### Added

#### Marketplace

- Initial release of Claude Code Plugins marketplace with `.claude-plugin/marketplace.json` metadata system
- Support for slash commands, agents, and skills

#### AI-Git Plugin (v1.0.0)

- `/commit-push` command for automated git commit and push (later renamed to `/git-commit-push`)
  - Intelligent commit message generation following repository conventions
  - Clean commit messages without AI attribution

#### AI-Security Plugin (v1.0.0)

- `/security-audit` command with `security-auditor` agent
  - OWASP Top 10 2021 compliance checking and vulnerability detection
  - Timestamped audit reports with risk scoring and remediation guidance

#### AI-Performance Plugin (v1.0.0)

- `/performance-audit` command with `performance-optimizer` agent
  - Performance anti-pattern detection and database optimization recommendations
  - Timestamped audit reports with impact scoring and optimization roadmap

### Documentation

- README.md, CLAUDE.md, individual plugin READMEs, and MIT license

[Unreleased]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v2.2.2...HEAD
[2.2.2]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v2.2.1...v2.2.2
[2.2.1]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v2.2.0...v2.2.1
[2.2.0]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v2.0.1...v2.1.0
[2.0.1]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v2.0.0...v2.0.1
[2.0.0]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.9.1...v2.0.0
[1.9.1]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.9.0...v1.9.1
[1.9.0]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.8.0...v1.9.0
[1.8.0]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.7.1...v1.8.0
[1.7.1]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.7.0...v1.7.1
[1.7.0]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.6.3...v1.7.0
[1.6.3]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.6.2...v1.6.3
[1.6.2]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.6.1...v1.6.2
[1.6.1]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.6.0...v1.6.1
[1.6.0]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.5.4...v1.6.0
[1.5.4]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.5.3...v1.5.4
[1.5.3]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.5.2...v1.5.3
[1.5.2]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.5.1...v1.5.2
[1.5.1]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.5.0...v1.5.1
[1.5.0]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.4.1...v1.5.0
[1.4.1]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.4.0...v1.4.1
[1.4.0]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/charlesjones-dev/claude-code-plugins-dev/releases/tag/v1.0.0
