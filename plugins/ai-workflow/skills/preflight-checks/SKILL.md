---
name: preflight-checks
description: Comprehensive code quality verification system for running type checking, linting, and tests. Use when validating code quality, preparing commits, running CI checks locally, or when the user mentions preflight, verify, lint, typecheck, or test commands.
---

# Preflight Code Quality Checks

This skill provides comprehensive guidance for discovering and running code quality checks across different project types.

## Overview

Preflight checks are the quality gates that verify code before commits, PRs, or deployments. They typically include:

1. **Type Checking** - Static type verification (TypeScript, MyPy, etc.)
2. **Linting** - Code quality and style enforcement
3. **Formatting** - Consistent code style
4. **Security Scanning** - Dependency audits and static analysis (SAST)
5. **Testing** - Unit, integration, and e2e tests

## Quick Reference

### Node.js / TypeScript Projects

| Check | Command | Auto-fix |
|-------|---------|----------|
| TypeScript | `npx tsc --noEmit` | N/A (manual) |
| ESLint | `npx eslint .` | `npx eslint . --fix` |
| Biome | `npx biome check .` | `npx biome check . --write` |
| Prettier | `npx prettier --check .` | `npx prettier --write .` |
| Jest | `npx jest` | N/A |
| Vitest | `npx vitest run` | N/A |

**Prefer npm scripts when available:**
```bash
# Check package.json scripts first
npm run lint        # if exists
npm run typecheck   # if exists
npm run test        # if exists
npm run check       # often runs all checks
```

### Python Projects

| Check | Command | Auto-fix |
|-------|---------|----------|
| MyPy | `mypy .` | N/A (manual) |
| Ruff lint | `ruff check .` | `ruff check . --fix` |
| Ruff format | `ruff format --check .` | `ruff format .` |
| Black | `black --check .` | `black .` |
| isort | `isort --check .` | `isort .` |
| Pytest | `pytest` | N/A |

**With pyproject.toml (modern Python):**
```bash
# Check for [tool.X] sections
ruff check . && ruff format --check .  # Ruff (fast, recommended)
mypy src/                               # Type checking
pytest                                  # Tests
```

### .NET Projects

| Check | Command | Auto-fix |
|-------|---------|----------|
| Build | `dotnet build` | N/A |
| Build strict | `dotnet build --warnaserror` | N/A |
| Format check | `dotnet format --verify-no-changes` | `dotnet format` |
| Tests | `dotnet test` | N/A |
| Analyzers | Configured in `.editorconfig` | N/A |

**.NET specific considerations:**
- Warnings as errors: Add `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>` to `.csproj`
- Enable nullable: `<Nullable>enable</Nullable>` for null safety
- Analyzers run during build automatically

### Go Projects

| Check | Command | Auto-fix |
|-------|---------|----------|
| Build | `go build ./...` | N/A |
| Vet | `go vet ./...` | N/A |
| golangci-lint | `golangci-lint run` | `golangci-lint run --fix` |
| gofmt | `gofmt -l .` | `gofmt -w .` |
| Tests | `go test ./...` | N/A |

### Rust Projects

| Check | Command | Auto-fix |
|-------|---------|----------|
| Check | `cargo check` | N/A |
| Clippy | `cargo clippy -- -D warnings` | `cargo clippy --fix` |
| Format | `cargo fmt --check` | `cargo fmt` |
| Tests | `cargo test` | N/A |

### Security Scanning (Cross-Platform)

| Tool | Purpose | Command |
|------|---------|---------|
| pnpm audit | Dependency CVE scan | `pnpm audit` or `pnpm audit:check` |
| npm audit | Dependency CVE scan | `npm audit` |
| yarn audit | Dependency CVE scan | `yarn audit` |
| eslint-plugin-security | JS/TS security patterns | Runs with ESLint |
| Semgrep | SAST scanning | `semgrep scan --config auto` |
| Semgrep (Docker) | SAST scanning | See platform-specific commands below |
| pip-audit | Python dependency scan | `pip-audit` |
| cargo-audit | Rust dependency scan | `cargo audit` |

**IMPORTANT: If Semgrep is detected in CI workflows or config files, you MUST run it as part of preflight checks. Do not skip it.**

**Semgrep Detection Priority:**
1. Package.json scripts (e.g., `pnpm run semgrep`)
2. Config files: `.semgreprc.yml`, `.semgrep.yml`, `semgrep.yml`, `.semgrep/`
3. CI workflows: `.github/workflows/*.yml` (extract `--config` flags)
4. **README.md documentation** - ALWAYS check this before trying generic Docker commands
5. Local CLI: `semgrep --version`
6. Docker fallback (see platform-specific commands below)

**Semgrep Docker Commands (AUTOMATIC PLATFORM DETECTION):**

CRITICAL: Detect the platform from environment context and use the correct command automatically.

- **Windows (`win32`):** ALWAYS use `MSYS_NO_PATHCONV=1` prefix:
  ```bash
  MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd):/src" semgrep/semgrep semgrep scan --config auto /src
  ```
- **macOS (`darwin`) / Linux:** Standard command:
  ```bash
  docker run --rm -v "$(pwd):/src" semgrep/semgrep semgrep scan --config auto /src
  ```

**Why `MSYS_NO_PATHCONV=1` is required on Windows:** Git Bash/MSYS2 auto-converts POSIX paths to Windows paths. Without this prefix, `/src` becomes `C:/Program Files/Git/src`, causing "Invalid scanning root" error. DO NOT try without the prefix first on Windows.

## Discovery Strategy

### Step 1: Identify Project Type(s)

Check for presence of key files:

```
# JavaScript/TypeScript
package.json, tsconfig.json, deno.json

# Python
pyproject.toml, setup.py, requirements.txt, Pipfile

# .NET
*.csproj, *.sln, *.fsproj

# Go
go.mod

# Rust
Cargo.toml
```

### Step 2: Check for Configured Scripts/Tasks

**package.json scripts (Node.js):**
```json
{
  "scripts": {
    "lint": "eslint .",
    "typecheck": "tsc --noEmit",
    "test": "vitest",
    "check": "npm run lint && npm run typecheck && npm run test"
  }
}
```

**pyproject.toml (Python):**
```toml
[tool.ruff]
line-length = 100

[tool.mypy]
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
```

**Makefile targets:**
```makefile
lint:
    ruff check .

test:
    pytest

check: lint test
```

### Step 3: Detect CI Configuration

Check for CI files to align local checks with CI:
- `.github/workflows/*.yml` - GitHub Actions (also check for semgrep jobs)
- `.gitlab-ci.yml` - GitLab CI
- `azure-pipelines.yml` - Azure DevOps
- `Jenkinsfile` - Jenkins
- `.circleci/config.yml` - CircleCI

### Step 4: Detect Security Tools

Check for security scanning configuration:
- `package.json` devDependencies for `eslint-plugin-security`
- `package.json` scripts containing `audit` or `semgrep`
- Semgrep config files: `.semgreprc.yml`, `.semgrep.yml`, `semgrep.yml`
- CI workflows for semgrep jobs (extract `--config` flags for local replication)
- `README.md` for documented security commands (often in Security sections)
- Lock files (`pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`) for audit support

## Best Practices

### Execution Order

Run checks in order of speed and feedback value:
1. **Format check** (fastest, catches style issues)
2. **Type checking** (fast, catches type errors)
3. **Linting** (medium, catches quality issues)
4. **Security scanning** (medium, catches vulnerabilities)
5. **Tests** (slowest, catches logic errors)

This order provides fastest feedback on failures.

### Handling Monorepos

For monorepos, check for workspace configuration:
- `pnpm-workspace.yaml`
- `lerna.json`
- `package.json` with `workspaces` field
- `Cargo.toml` with `[workspace]`

Run checks at workspace root or iterate through packages.

### CI Alignment

Ensure local preflight matches CI:
```bash
# Good: Use same commands as CI
npm run lint    # Same as CI step

# Avoid: Different commands locally vs CI
eslint . --max-warnings=0  # If CI uses npm run lint
```

### Exit Codes

Respect exit codes for CI integration:
- `0` - Success, no issues
- `1` - Failure, issues found
- `2` - Configuration error

### Caching

For faster subsequent runs:
- ESLint: Uses `.eslintcache` with `--cache` flag
- TypeScript: Uses `tsconfig.tsbuildinfo` with `incremental: true`
- Pytest: Uses `.pytest_cache`
- Rust: Uses `target/` directory

## Error Messages Reference

### TypeScript Common Errors

```
TS2339: Property 'x' does not exist on type 'Y'
-> Add property to interface or use type assertion

TS2322: Type 'X' is not assignable to type 'Y'
-> Check type definitions, may need union type

TS7006: Parameter 'x' implicitly has an 'any' type
-> Add explicit type annotation
```

### ESLint Common Errors

```
@typescript-eslint/no-unused-vars
-> Remove unused variable or prefix with _

@typescript-eslint/no-explicit-any
-> Replace 'any' with specific type

import/order
-> Auto-fixable: eslint --fix
```

### Python Common Errors

```
mypy: Incompatible return value type
-> Check return type annotation matches actual return

ruff: E501 Line too long
-> Auto-fixable or configure line-length

ruff: F401 Module imported but unused
-> Remove unused import
```

## Integration with Pre-commit Hooks

Preflight checks can be configured as pre-commit hooks:

**.pre-commit-config.yaml:**
```yaml
repos:
  - repo: local
    hooks:
      - id: preflight
        name: Preflight Checks
        entry: npm run check
        language: system
        pass_filenames: false
```

**Husky (Node.js):**
```bash
# .husky/pre-commit
npm run lint
npm run typecheck
```

## When to Skip Checks

Some scenarios where partial checks are acceptable:
- `--no-verify` for emergency fixes (use sparingly)
- WIP commits on feature branches
- Exploratory/spike work

Always run full preflight before:
- Opening PRs
- Merging to main/master
- Deploying to production
