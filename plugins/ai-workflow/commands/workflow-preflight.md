---
name: workflow-preflight
description: "Run code quality checks (typecheck, lint, tests) - auto-detects configured tools and offers to fix issues."
argument-hint: [--fix | --check-only | --verbose]
allowed-tools: Bash, Read, Glob, Grep
---

# Preflight Code Quality Checks

You are running a comprehensive preflight check on this codebase. This command discovers and runs configured quality checks including type checking, linting, and tests.

## Arguments

- `--fix` - Automatically attempt to fix issues without prompting
- `--check-only` - Only report issues, never prompt to fix
- `--verbose` - Show detailed output from all commands
- No arguments - Interactive mode (default): prompt before fixing

User provided: $ARGUMENTS

## Step 1: Discovery Phase

First, analyze the project to discover configured quality tools. Check for:

### Package Manager & Config Files
- `package.json` - Check for scripts: `lint`, `typecheck`, `type-check`, `tsc`, `test`, `check`, `validate`
- `tsconfig.json` / `jsconfig.json` - TypeScript/JavaScript configuration
- `.eslintrc*`, `eslint.config.*` - ESLint configuration
- `biome.json`, `biome.jsonc` - Biome configuration
- `.prettierrc*`, `prettier.config.*` - Prettier configuration
- `deno.json` / `deno.jsonc` - Deno configuration
- `.stylelintrc*` - Stylelint configuration

### Python Projects
- `pyproject.toml` - Check for ruff, mypy, pytest, black, isort configs
- `setup.py` / `setup.cfg` - Legacy Python config
- `requirements.txt` / `requirements-dev.txt` - Dependencies
- `mypy.ini` / `.mypy.ini` - MyPy configuration
- `ruff.toml` / `.ruff.toml` - Ruff configuration
- `pytest.ini` / `pyproject.toml [tool.pytest]` - Pytest configuration
- `tox.ini` - Tox configuration

### .NET Projects
- `*.csproj` / `*.fsproj` / `*.vbproj` - .NET project files
- `*.sln` - Solution files
- `.editorconfig` - Editor configuration with .NET analyzers
- `Directory.Build.props` - MSBuild properties

### Go Projects
- `go.mod` - Go module
- `.golangci.yml` / `.golangci.yaml` - GolangCI-Lint configuration

### Rust Projects
- `Cargo.toml` - Check for clippy, rustfmt
- `rustfmt.toml` / `.rustfmt.toml` - Rustfmt configuration
- `clippy.toml` / `.clippy.toml` - Clippy configuration

### Security Scanning
- `pnpm-lock.yaml` / `package-lock.json` / `yarn.lock` - Dependency audit support
- `.semgreprc.yml` / `.semgrep.yml` / `semgrep.yml` / `.semgrep/` - Semgrep configuration
- `.github/workflows/*.yml` - Check for semgrep CI jobs (extract config flags)
- `eslint-plugin-security` in devDependencies - ESLint security rules
- `package.json` scripts containing `audit` or `semgrep` - Custom security scripts
- `README.md` / `CONTRIBUTING.md` - Check for documented security scanning commands

### Other
- `Makefile` / `makefile` - Check for lint/test/check targets
- `.pre-commit-config.yaml` - Pre-commit hooks
- `justfile` - Just command runner

## Step 2: Report Discovery

Present a summary of what was discovered:

```
Preflight Discovery Summary

Project Type: [Node.js / Python / .NET / Go / Rust / Multi-language]

Type Checking: [tool name] via [config file]
Linting: [tool name] via [config file]
Testing: [tool name] via [config file]
Formatting: [tool name] via [config file]
Security Scanning: [tool name(s)] via [config file/method]
Not configured: [any missing categories]

Ready to run checks?
```

## Step 3: Execute Checks

Run the discovered checks in this order:
1. **Type checking** (fastest feedback on type errors)
2. **Linting** (code quality issues)
3. **Formatting check** (style consistency - check only, don't auto-fix yet)
4. **Security scanning** - MANDATORY if any security tools detected:
   - Dependency audit (npm audit, pnpm audit, etc.)
   - **Semgrep SAST** - MUST run if detected in CI workflows or config files
5. **Tests** (run last as they take longest)

**CRITICAL: If Semgrep was detected in discovery (CI workflows, config files, or README), you MUST run it. Do NOT skip Semgrep and report "All checks passed" without running it.**

For each check, report:
- Pass - no issues found
- Warnings - non-blocking issues
- Fail - blocking issues found

### Common Commands by Ecosystem

**Node.js/TypeScript:**
- TypeScript: `npx tsc --noEmit` or `npm run typecheck`
- ESLint: `npx eslint . --max-warnings=0` or `npm run lint`
- Biome: `npx biome check .`
- Tests: `npm test` or `npx jest` or `npx vitest run`

**Python:**
- MyPy: `mypy .` or `mypy src/`
- Ruff: `ruff check .`
- Pytest: `pytest` or `python -m pytest`
- Black check: `black --check .`

**.NET:**
- Build with warnings: `dotnet build --warnaserror`
- Format check: `dotnet format --verify-no-changes`
- Tests: `dotnet test`

**Go:**
- Type check: `go build ./...`
- Lint: `golangci-lint run`
- Tests: `go test ./...`

**Rust:**
- Check: `cargo check`
- Clippy: `cargo clippy -- -D warnings`
- Tests: `cargo test`
- Format check: `cargo fmt --check`

### Security Scanning Commands

**Dependency Audits (run based on detected package manager):**
- pnpm: `pnpm audit` or `pnpm audit:check` (if script exists in package.json)
- npm: `npm audit`
- yarn: `yarn audit`
- pip: `pip-audit` (if installed) or `safety check` (if installed)
- cargo: `cargo audit` (if installed)

**Semgrep (static analysis - MUST run if detected in CI or config):**

IMPORTANT: If Semgrep is detected in CI workflows or config files, you MUST run it as part of preflight checks. Do not skip it.

Detection order:
1. Check for custom script in package.json (e.g., `pnpm run semgrep` or `npm run semgrep`)
2. Check for semgrep config files: `.semgreprc.yml`, `.semgrep.yml`, `semgrep.yml`, or `.semgrep/` directory
3. Check `.github/workflows/*.yml` for semgrep jobs - extract `--config` flags used in CI
4. **Check `README.md` for documented semgrep commands** - ALWAYS check this before trying generic Docker commands, as projects often document the exact command needed for their setup
5. Check if `semgrep` CLI is available locally: `semgrep --version`
6. Check if Docker is available: `docker --version`
7. If Docker available but no semgrep CLI, use Docker (see platform-specific commands below)

**Semgrep execution:**
- With config file: `semgrep scan --config .semgreprc.yml` (or detected config)
- Without config (auto rules): `semgrep scan --config auto`
- With language-specific rules: `semgrep scan --config auto --config p/javascript --config p/typescript`

**Docker execution (AUTOMATIC PLATFORM DETECTION):**

CRITICAL: You MUST detect the platform and use the correct command automatically. Check the platform from the environment context.

- **If platform is `win32` (Windows):** ALWAYS use `MSYS_NO_PATHCONV=1` prefix for Docker commands:
  ```bash
  MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd):/src" semgrep/semgrep semgrep scan --config auto /src
  ```

- **If platform is `darwin` (macOS) or `linux`:** Use standard Docker command:
  ```bash
  docker run --rm -v "$(pwd):/src" semgrep/semgrep semgrep scan --config auto /src
  ```

**Why this matters on Windows:** Git Bash/MSYS2 performs automatic POSIX-to-Windows path conversion. Without `MSYS_NO_PATHCONV=1`, the Docker volume mount `/src` gets incorrectly converted to `C:/Program Files/Git/src`, causing Semgrep to fail with "Invalid scanning root" error.

DO NOT try the command without the prefix first on Windows - use the correct platform-specific command immediately.

**ESLint Security Plugin:**
- If `eslint-plugin-security` is detected in devDependencies, security rules are already included in the linting step
- No separate command needed, but note in discovery output that security linting is active

## Step 4: Results Summary

Present results in a clear summary:

```
Preflight Results

Type Checking     Passed
Linting           3 errors, 2 warnings
Formatting        5 files need formatting
Security Audit    2 vulnerabilities found
Security SAST     Passed (semgrep)
Tests             42 passed, 0 failed

Overall: Issues found
```

## Step 5: Fix Prompt (Interactive Mode)

If issues were found AND user didn't pass `--check-only`:

**If `--fix` was passed:** Proceed directly to fixing without prompting.

**Otherwise, ask:**

```
Would you like me to attempt fixes?

[1] Fix all auto-fixable issues (lint --fix, format, etc.)
[2] Fix only linting issues
[3] Fix only formatting issues
[4] Show me the specific issues first
[5] Skip fixes - I'll handle it manually

Enter choice (1-5):
```

Wait for user input before proceeding.

## Step 6: Apply Fixes (if requested)

When fixing:
1. Run auto-fix commands (e.g., `eslint --fix`, `ruff --fix`, `prettier --write`)
2. Re-run the checks to verify fixes
3. Report what was fixed and what still needs manual attention

```
Fix Results

Auto-fixed:
  3 linting errors resolved
  5 files formatted

Still needs attention:
  1 type error in src/utils.ts:42
     Property 'foo' does not exist on type 'Bar'
```

## Important Guidelines

1. **Never run fix commands without user consent** unless `--fix` was explicitly passed
2. **Preserve user's working state** - don't modify files unexpectedly
3. **Respect existing configuration** - use project's own scripts when available (e.g., `npm run lint` over raw `eslint`)
4. **Handle missing tools gracefully** - if a tool isn't installed, note it and continue
5. **Provide actionable feedback** - include file paths and line numbers for manual fixes
6. **Consider CI alignment** - mention if checks match CI configuration

## Error Handling

If a tool fails to run:
```
Could not run [tool]: [error message]
   Suggestion: [how to install or configure]
```

If no quality tools are configured:
```
No quality tools detected in this project.

Would you like me to help set up:
[1] TypeScript type checking
[2] ESLint for linting
[3] Prettier for formatting
[4] A testing framework
[5] Skip setup
```
