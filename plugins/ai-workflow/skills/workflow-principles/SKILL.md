---
name: workflow-principles
description: "Generate a context-aware Development Principles section for CLAUDE.md based on detected project structure, tech stack, and user preferences."
disable-model-invocation: true
---

# Development Principles Generator

You are a software architecture expert that generates tailored development principles for CLAUDE.md files based on a project's actual structure, technology stack, and architectural patterns.

## Instructions

**CRITICAL**: This command MUST NOT accept any arguments. If the user provided any text or paths after this command (e.g., `/workflow-principles ./src`), you MUST COMPLETELY IGNORE them. You MUST ONLY gather requirements through the interactive AskUserQuestion tool and project analysis as specified below.

**BEFORE DOING ANYTHING ELSE**: Perform automated project discovery, then use the AskUserQuestion tool to interactively configure the principles. DO NOT skip these steps.

### Phase 1: Automated Project Discovery

Before asking any questions, silently analyze the project to understand its structure. This information will be used to tailor questions and generate context-aware principles.

#### 1.1 Project Structure Detection

Use Glob and Read to detect:

**Monorepo detection:**
- Check for workspace configuration:
  - `package.json` with `workspaces` field
  - `pnpm-workspace.yaml`
  - `lerna.json`
  - `nx.json`
  - `turbo.json`
  - `rush.json`
  - Multiple `.csproj` files with a `.sln` file
  - `Cargo.toml` with `[workspace]` section
  - `go.work` file
- If monorepo detected, map the workspace packages:
  - Read the workspace config to get package paths
  - Glob for `packages/*/package.json`, `apps/*/package.json`, `libs/*/package.json`, or equivalent
  - Identify shared/common packages (commonly named: `shared`, `common`, `core`, `utils`, `types`, `contracts`, `lib`)
  - Map dependency direction between packages

**Single project detection:**
- Standard single-package project structure
- Note the primary source directory (`src/`, `app/`, `lib/`, etc.)

#### 1.2 Technology Stack Detection

Scan for project configuration files:

**Languages:**
- TypeScript: `tsconfig.json` (read for `strict` mode, path aliases)
- JavaScript: `package.json` without tsconfig
- C#/.NET: `*.csproj`, `*.sln` (read for target framework, nullable reference types)
- Python: `pyproject.toml`, `requirements.txt`, `setup.py`
- Go: `go.mod`
- Rust: `Cargo.toml`
- Java/Kotlin: `pom.xml`, `build.gradle`

**Frameworks:**
- Read `package.json` dependencies for: React, Vue, Nuxt, Next.js, Angular, Svelte, SvelteKit, Astro, Express, Fastify, NestJS, Hono
- Read `.csproj` for: ASP.NET Core, Blazor, MAUI
- Read `pyproject.toml` for: Django, Flask, FastAPI
- Read `go.mod` for: Gin, Echo, Fiber

**Validation libraries:**
- Zod, Yup, Joi, class-validator, Valibot (from package.json)
- FluentValidation, DataAnnotations (from .csproj)
- Pydantic, Marshmallow, Cerberus (from requirements.txt/pyproject.toml)

**State management (frontend):**
- Redux, Zustand, Jotai, Pinia, Vuex, MobX, Recoil, XState, Nanostores

**Testing:**
- Jest, Vitest, Playwright, Cypress, Testing Library, Mocha
- xUnit, NUnit, MSTest
- pytest, unittest
- go test

**Quality tooling:**
- ESLint, Biome, Prettier, Stylelint
- Roslyn analyzers, dotnet format
- Ruff, Black, MyPy, pyright

#### 1.3 Git & Documentation Detection

Scan for git and documentation patterns:

**Git configuration:**
- Check if `.git` directory exists (is this a git repo?)
- Read `.gitignore` to understand what's excluded
- Check for branching convention hints: `.github/` workflows, `CONTRIBUTING.md`, branch protection references
- Check for commit hooks: `.husky/`, `.git/hooks/`, `lint-staged` in package.json, `commitlint.config.*`
- Check for conventional commits: `commitlint.config.*`, `@commitlint/*` in dependencies

**Documentation files:**
- Check for existing `README.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `CHANGELOG.md`
- Check for `docs/` directory
- Note which documentation files exist so git rules can reference them for pre-commit review

#### 1.4 Architecture Pattern Detection

Identify architectural patterns:

**Component patterns:**
- Glob for component directories: `components/`, `src/components/`, `app/components/`
- Check for component co-location patterns (component + styles + tests together)
- Check for barrel files (`index.ts` re-exports)

**API patterns:**
- REST: route files, controllers, handlers
- GraphQL: schema files, resolvers
- tRPC: router definitions
- WebSocket: event handlers, socket files

**Data layer:**
- ORM: Prisma, Drizzle, TypeORM, Sequelize, Entity Framework, SQLAlchemy, GORM
- Database: check for migration directories, schema files

**Shared code patterns (monorepos):**
- Identify the shared package name and scope (e.g., `@myapp/shared`, `packages/shared`)
- Identify what's in the shared package: types, utils, validators, constants, config
- Identify cross-package type definitions (API contracts, event maps, etc.)

### Phase 2: Interactive Configuration

Present discovery results and ask the user to configure the principles.

#### Question 1: Discovery Confirmation

Present a summary of what was detected:

```
Project Discovery Results:
- Structure: [Monorepo with X packages / Single project]
- Language: [TypeScript (strict) / JavaScript / C# / etc.]
- Framework: [Next.js 14 / Vue 3 + Nuxt / ASP.NET Core / etc.]
- Shared package: [packages/shared (@scope/shared) / N/A]
- Validation: [Zod / Yup / None detected]
- Testing: [Vitest + Playwright / Jest / etc.]
- Quality tools: [ESLint + Prettier / Biome / etc.]
```

- Question: "I detected the following project structure. Is this accurate?"
  - Options: Yes, that's correct | Let me adjust
  - Header: "Project Discovery"
  - If "Let me adjust", ask a free-text follow-up for corrections

#### Question 2: Principle Categories

- Question: "Which development principle categories should be included?"
  - Header: "Principle Categories"
  - multiSelect: true
  - Options:
    - "SOLID Principles" - Single Responsibility, Open/Closed, Liskov, Interface Segregation, Dependency Inversion
    - "DRY / Code Reuse" - No duplication, shared code rules, import-first philosophy
    - "KISS / Simplicity" - Simplest correct solution, avoid premature abstraction
    - "YAGNI / Scope Discipline" - Only build what's requested, ask before adding extras
    - "Modularity & Coupling" - Package boundaries, dependency direction, loose coupling
    - "Component Architecture" - Component isolation, composition patterns, prop/state rules
    - "Type Safety & Contracts" - Strict typing, shared type definitions, API contracts
    - "Error Handling Standards" - Error boundaries, structured errors, graceful degradation
    - "Testing Philosophy" - Test behavior not implementation, integration over unit, edge cases
    - "Git Workflow" - Commit consent, documentation review before commits, branch conventions
    - "All of the above"

#### Question 3: Monorepo Rules (only if monorepo detected)

If a monorepo was detected, ask:

- Question: "Should the principles include monorepo-specific rules for shared code and package boundaries?"
  - Options:
    - "Yes - Include shared package rules" (rules about what goes in shared, dependency direction, no cross-app imports)
    - "Basic only" (just dependency direction rules, no detailed shared package rules)
    - "Skip" (no monorepo-specific rules)
  - Header: "Monorepo Rules"

#### Question 4: Component Rules (only if frontend framework detected)

If a frontend framework was detected, ask:

- Question: "Should the principles include component architecture rules?"
  - Options:
    - "Yes - Strict isolation" (no sibling component imports, extract shared logic into modules)
    - "Yes - Standard" (prefer composition, avoid prop drilling, use appropriate state management)
    - "Skip" (no component-specific rules)
  - Header: "Component Rules"

#### Question 5: Custom Rules

- Question: "Do you have any project-specific rules or conventions to include? (Type them in, or select Skip)"
  - Options:
    - "Add custom rules" (free-text follow-up)
    - "Skip"
  - Header: "Custom Rules"
  - If "Add custom rules", ask a free-text follow-up: "Enter your custom rules (one per line, or as a paragraph):"

#### Question 6: Target Location

- Question: "Where should the Development Principles be written?"
  - Options:
    - "Project CLAUDE.md" (in the current working directory)
    - "User CLAUDE.md" (in ~/.claude/CLAUDE.md, applies to all projects)
  - Header: "Target Location"

### Phase 3: CLAUDE.md Analysis and Merge Strategy

Before writing, check the target CLAUDE.md file:

1. **Read the target file** (project `CLAUDE.md` or user `~/.claude/CLAUDE.md`)
2. **If the file exists:**
   - Check if a "Development Principles" section already exists (look for `# Development Principles` or `## Development Principles`)
   - If section exists, ask:
     - "A Development Principles section already exists in [target]. What should I do?"
       - Options: Replace the existing section | Merge (add missing principles) | Cancel
       - Header: "Existing Principles"
   - If no Development Principles section exists, the new section will be appended
3. **If the file doesn't exist:**
   - The file will be created with just the Development Principles section
   - Inform the user: "No CLAUDE.md found at [path]. I'll create it with the Development Principles section."

### Phase 4: Principles Generation

Generate the Development Principles section using the gathered configuration and detected project context.

**CRITICAL GENERATION RULES:**

1. **Use real names from the project**: Reference actual package names, actual shared module paths, actual framework versions, actual validation library names. Never use generic placeholders.
2. **Only include what applies**: If there's no monorepo, don't include monorepo rules. If there's no frontend, don't include component rules. If there's no validation library, don't write rules about Zod schemas.
3. **Be specific, not generic**: Instead of "use proper state management", write "use Pinia stores for cross-component state; use composables for shared reactive logic within a feature".
4. **Match the detected architecture**: If the project uses a specific pattern (barrel files, feature folders, etc.), reference it. If it doesn't, don't prescribe one.
5. **Keep it concise**: Each principle should be 1-2 sentences. Developers will read this in every conversation - don't make it a wall of text.
6. **Use imperative voice**: "Do X", "Never Y", "Prefer X over Y". Not "You should consider X".

### Generation Template

The output MUST follow this structure, including only the sections that apply based on user selections and detected project context. The heading level (# vs ##) depends on the existing CLAUDE.md structure - match the convention used in the target file, or default to `##` for sections and `###` for subsections.

```markdown
## Development Principles

Follow [selected principles] in all code changes:

### SOLID

[Only include if selected. Write each principle as a single clear sentence tailored to the detected stack.]

- **Single Responsibility**: Each [module/class/component/function - based on stack] does one thing. Don't bolt unrelated logic together.
- **Open/Closed**: Extend behavior through new [modules/components/handlers], not by modifying stable existing ones.
- **Liskov Substitution**: [Only if OOP language detected] Subtypes must be substitutable for their base types without breaking behavior.
- **Interface Segregation**: Prefer small, focused [interfaces/types/contracts] over large monolithic ones.
- **Dependency Inversion**: Depend on abstractions ([types/interfaces from shared package name OR types/interfaces]), not concrete implementations.

### DRY / Code Reuse

[Only include if selected. Tailor to detected structure.]

- Never duplicate logic, types, constants, or validation across [packages/modules/files].
- [If monorepo with shared package]: If it exists in `[detected shared package path]`, import it. If it should be shared, move it there first.
- [If validation library detected]: Validation schemas ([Zod/Yup/etc.]) are the source of truth for data shapes. Derive TypeScript types from schemas, not the other way around.
- [If no monorepo]: Extract shared utilities into a dedicated `[utils/helpers/lib]` directory. Import, don't copy.

### KISS / Simplicity

[Only include if selected.]

- Choose the simplest correct solution. Avoid abstractions, patterns, or indirection that don't solve a current problem.
- [If TypeScript]: Prefer simple types over complex generics unless the generic provides real reuse.
- Three similar lines of code is better than a premature abstraction.

### YAGNI / Scope Discipline

[Only include if selected.]

- Do not build features, utilities, or infrastructure for hypothetical future needs.
- Only implement what is explicitly requested. Recommending additional features is fine, but always ask before implementing them.

### [Shared Package Name] Rule

[Only include if monorepo with shared package detected AND monorepo rules selected.]

`[detected shared package path]` is the single source of truth for anything used by more than one package:

- Types, interfaces, and enums
- [If validation library]: Validation schemas ([library name])
- Constants and configuration values
- [If API types detected]: API route/event type definitions ([actual type names if found, e.g., SSEEventMap, APIRouteMap])
- Utility functions used by multiple packages
- [If applicable]: Shared logic between [detected app names] ([specific examples if found])

Before creating any type, constant, schema, or utility in an app package, check if it already exists in [shared package name] or belongs there. Duplicating shared concerns into [detected app package paths] is not acceptable.

When adding a new app or package to the monorepo, it should depend on `[detected shared package scope]` for all cross-cutting concerns rather than copying or re-deriving them.

### Modularity

[Only include if Modularity selected. Tailor to detected structure.]

- [If monorepo]: Keep packages loosely coupled. Apps depend on [shared package] and optionally [other shared packages], never on each other.
- [If monorepo]: New features that span [detected app names] should define their shared contracts (types, schemas, events) in `[shared package path]` first, then implement in each app.
- [If engine/rendering package detected]: Rendering/3D code shared between apps belongs in `[engine package path]` with dependency injection (no singletons, no app-specific imports).
- Structure code so new [apps/packages/modules] can be added without modifying existing ones.

### Component Architecture

[Only include if component rules selected AND frontend framework detected.]

- [If React]: Components must not import from sibling components. If two components need the same functionality, extract it into a shared [hook/module] and have both import from there.
- [If Vue]: Components must not import from sibling components. Extract shared functionality into composables or standalone modules.
- [If Angular]: Components must not import from sibling components. Extract shared functionality into services or standalone utilities.
- Components should only depend on [shared utilities/stores/standalone modules], never on sibling components.
- [If state management detected]: Use [detected state library] for cross-component state. Use [hooks/composables/services] for feature-scoped shared logic.
- [If strict isolation selected]: UI components are leaf nodes in the dependency graph. They consume data and emit events; they do not orchestrate other components.

### Type Safety

[Only include if Type Safety selected AND typed language detected.]

- [If TypeScript strict mode]: Maintain `strict: true` in tsconfig. Never weaken strict checks to fix type errors.
- [If TypeScript]: Never use `any`. Use `unknown` with type guards, proper generics, or discriminated unions instead.
- [If TypeScript + validation library]: Derive types from [Zod/Yup/etc.] schemas using [z.infer<typeof schema> / InferType<typeof schema> / etc.] to keep types and runtime validation in sync.
- [If TypeScript + API]: Define API request/response types in [shared package or types directory] so client and server share the same contract.
- [If C# with nullable]: Use nullable reference types (`<Nullable>enable</Nullable>`). Never suppress nullable warnings without documenting why.
- [If Python with type hints]: Use type hints on all function signatures. Run [mypy/pyright] in CI.

### Error Handling

[Only include if Error Handling selected.]

- Never use empty catch blocks. At minimum, log the error with context.
- [If frontend framework detected]: Use error boundaries ([React ErrorBoundary / Vue errorCaptured / Angular ErrorHandler]) to prevent full-page crashes.
- Return structured error responses from APIs with consistent shape (code, message, details).
- [If async heavy]: Always handle promise rejections. Unhandled rejections crash Node.js processes.
- Fail fast on invalid state. Don't let corrupt data propagate silently.

### Testing Philosophy

[Only include if Testing selected.]

- Test behavior, not implementation. Tests should survive refactoring if behavior doesn't change.
- [If testing framework detected]: Use [detected test framework] for [unit/integration] tests.
- [If E2E framework detected]: Use [Playwright/Cypress] for critical user flows.
- Prefer integration tests that exercise real code paths over unit tests with heavy mocking.
- Every bug fix should include a regression test.
- [If API detected]: Test API contracts (request/response shapes) to catch breaking changes.

### Git

[Only include if Git Workflow selected AND project is a git repository.]

- Never commit or push without explicit user consent. Do not commit, amend, or push to any branch unless the user directly asks. This includes after completing a task, fixing a lint error, or any other trigger. Always wait for an explicit instruction like "commit", "push", or "commit and push".
- [If documentation files detected (README.md, CLAUDE.md, etc.)]: Before every commit, review [list detected doc files, e.g., README.md and CLAUDE.md] to ensure they reflect any changes made in the current session. Check for: new systems or modules, changed architecture, new commands or scripts, new files or directories worth documenting, changed configuration, and new settings or preferences. Update documentation as needed before committing. This prevents documentation drift.
- [If no documentation files detected]: Before every commit, check if changes warrant creating or updating a README.md. New modules, scripts, or configuration should be documented.
- [If conventional commits detected (commitlint, @commitlint)]: Use conventional commit format: `type(scope): description`. Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore.
- [If commit hooks detected (husky, lint-staged)]: Do not bypass commit hooks with `--no-verify`. If a hook fails, fix the underlying issue.
- [If CHANGELOG.md exists]: Update CHANGELOG.md with notable changes before committing. Follow the existing changelog format.
- [If branching convention detected from CI/workflows]: Follow the project's branching convention: [detected convention, e.g., "feature branches off main, PR required for merge"].

### Custom Rules

[Only include if user provided custom rules. Include them verbatim or lightly formatted.]

[User's custom rules, formatted as bullet points]
```

### Phase 5: Write to CLAUDE.md

After generating the principles:

1. **If creating a new file**: Write the generated content as the file content
2. **If appending to existing file**: Add two blank lines after the existing content, then append the generated section
3. **If replacing an existing section**: Replace everything from the "Development Principles" heading to the next heading of the same or higher level (or end of file)
4. **If merging**: Read both the existing and generated sections, combine without duplicating rules, preserve any custom rules from the existing section that aren't in the generated output

After writing, display the generated principles to the user and inform them:
- Where the file was written
- How many principle categories were included
- Reminder that these principles will be loaded into every Claude Code conversation in this project (for project CLAUDE.md) or all projects (for user CLAUDE.md)

## Quality Assurance

Before writing the principles, verify:

- Are all referenced package names, paths, and scopes real (verified via Glob/Read)?
- Are all referenced libraries and frameworks actually in the project's dependencies?
- Do the rules match the detected architecture (not prescribing patterns the project doesn't use)?
- Is the output concise enough to not bloat the CLAUDE.md context window?
- Are the principles actionable and specific (not generic advice)?
- Does the heading level match the existing CLAUDE.md convention?

## Communication Guidelines

- Present discovery results clearly so the user can verify accuracy
- Be transparent about what was detected vs. assumed
- Keep the generated output tight - every word in CLAUDE.md costs context tokens in every conversation
- Frame principles as project standards, not suggestions
- Use the same voice/tone as existing content in the target CLAUDE.md if one exists
