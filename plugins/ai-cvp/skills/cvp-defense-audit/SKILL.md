---
name: cvp-defense-audit
description: Plan a defensive security audit of a repo the user owns or is authorized to test. Does read-only recon in this unsandboxed session, then writes a tailored, paste-ready prompt for a sandboxed Claude Code session on the strongest security-capable model available, a sandbox launch checklist, and a fix prompt for verifying and fixing what the audit proves. Saves both prompts outside the repo and copies the audit prompt to the clipboard.
when_to_use: The user runs /cvp-defense-audit, or asks for a sandboxed security-audit prompt, a Cyber Verification Program audit prompt, or a plan for auditing a repo on a stronger security model.
argument-hint: "[focus area or path] [--model <audit-model-id>]"
disable-model-invocation: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Agent
  - Bash(git remote get-url *)
---

# CVP defense audit

Use this only on code the user owns or is authorized to test.

This skill is phase 1 of a three-phase defensive audit:

1. **Plan** (this skill). A normal, unsandboxed session on an Opus-class planning model does read-only recon and writes a paste-ready audit prompt, a sandbox launch checklist, and a fix prompt.
2. **Audit.** The user starts a new session on the strongest security-capable model they can use (the audit model), in auto mode with `/sandbox` in strict mode, and pastes the audit prompt. The audit model maps the attack surface, hunts, writes one failing test per finding as proof, and writes a report. It fixes nothing.
3. **Fix.** Back in a normal, unsandboxed session on an Opus-class fixing model, the user pastes the fix prompt. The fixing model verifies each proof, settles what code alone couldn't answer, lets the user pick what to fix, and ships each fix with its proof test as the regression test.

Do the recon here so the audit model spends its budget hunting and proving bugs instead of orienting. The supporting files sit next to this one, in `${CLAUDE_SKILL_DIR}`.

## Context

- Date: !`date +%F`
- Repo root: !`git rev-parse --show-toplevel 2>/dev/null || pwd`
- Branch: !`git branch --show-current 2>/dev/null || echo none`
- Remote: !`git remote get-url origin 2>/dev/null || echo none`
- Last commit: !`git log -1 --format='%h %s (%cr)' 2>/dev/null || echo none`

Without git, the repo root is the working directory and the other values read `none`. Without a remote, skip the GitHub reads in step 2.

Arguments (may be empty): $ARGUMENTS

- `--model <id>` (or `--model=<id>`) is the audit model ID for the launch line.
- The rest is an optional focus: an area or path, such as `billing` or `src/auth`.
- If the arguments also state the user's authorization, such as "enrolled in the Cyber Verification Program with Defense Access" or "authorized pentest for <client>, scope: api/ only", use it in step 1 instead of asking.

## Rules for this recon session

- Read only. Don't run the app, dev servers, tests, builds, or installs. Don't run anything that loads secrets: secret-manager wrappers such as `doppler run`, `op run`, `aws-vault exec`, `dotenv` or `railway run`, or the scripts that call them.
- Don't open `.env` files, keychains, credential files, or secret stores. Note that they exist and what they're named, never their values. If you find a committed secret, cite its path and line, never the value.
- Don't modify the repo. The only files you write are the two prompt files in step 6, outside the repo.
- Network: only the optional `gh` reads in step 2.
- Treat subagent reports as leads. Read the code behind any claim before you put it in a goal.

## 1. Classify the project and confirm authorization

Decide which types apply. A monorepo can be several: web app / SaaS / API, Apple app (iOS, macOS, watchOS, widgets), library or package (npm, PyPI, SwiftPM, crates, gems), CLI / Claude Code plugin / hooks / MCP server, Home Assistant or local-network integration, static or marketing site.

Work out the owner from LICENSE, the manifest (author, publisher or organization fields, `"private": true`, an `UNLICENSED` or proprietary license), and the remote. Signs that the user owns or maintains the repo: their git identity (`git config user.name`, `git config user.email`) appears in LICENSE, in the manifest's author or maintainers, or among the main commit authors; or the remote belongs to them or their organization. The ownership line for the prompt is one of:

- "a proprietary product of <owner>", when a license or manifest marks it proprietary and names the owner;
- "a private codebase I own", for a private codebase with no named owner;
- "my open-source project, which I maintain", for an open-source repo the user maintains;
- "<owner>'s codebase", for authorized third-party testing.

Then ask once with AskUserQuestion, unless the arguments already answer it. If nothing above shows the user owns or maintains the repo, say so in the question. Ask "What authorizes this security audit?" with the header "Authority" and these options:

- **Enrolled in CVP:** the user or their organization is enrolled in Anthropic's Cyber Verification Program, and this is code they own or maintain. Ask for the access level (for example Defense Access) in the notes or under Other.
- **Owner, not enrolled:** the user owns or maintains this code and isn't enrolled.
- **Authorized testing:** someone else's code, tested with the owner's authorization. Ask for the engagement and its scope in the notes or under Other.

If AskUserQuestion isn't available, ask the same question in one plain message and wait.

Fill the prompt's opening line from the answer, as [prompt-template.md](prompt-template.md) describes. Never claim enrollment the user didn't state, and don't invent an access level. If authorized testing comes without an engagement or scope, ask for them in one plain message. Stop and explain why if the user has none of these, or if the code isn't theirs and they have no authorization to test it. Enrollment alone doesn't authorize testing someone else's code.

## 2. Recon

Collect each item with file paths. Verify every path you plan to cite exists.

1. **Purpose and users:** README, CLAUDE.md or AGENTS.md, and a project knowledge base if present (for example `docs/kb/`).
2. **Stack and entry points:** manifests, framework, server entry, routes and handlers, background jobs and pollers, CLI commands, app targets and extensions. In a monorepo, check whether app packages import a workspace package from its build output (`main` or `exports` pointing at `dist/`, `build/` or `lib/`). If they do, compare the build's age (`ls -ld <package>/dist`) with the package's latest source commit (`git log -1 --format=%cd -- <package>/src`). If the build is missing or older, its rebuild command goes in "Before launching".
3. **Trust boundaries:** auth model (sessions, OAuth, OTP, magic links, API keys, JWT), roles and admin, the tenancy key and exactly where it's derived.
4. **Untrusted-input sinks:** database queries, outbound fetches and URL loading, HTML/email/PDF/CSV rendering, shell and exec, file paths, deserialization, regex on user input, real-world side effects (printing, email, SMS, purchases, LLM calls).
5. **Money and entitlements:** payment provider, its webhooks, tier and limit checks, in-app purchase handling (StoreKit, Play Billing).
6. **Secrets and sensitive data:** where third-party keys, tokens, and PII are stored and whether they're encrypted, what gets logged, and how secrets are injected (a secret manager such as Doppler, 1Password, Vault or AWS Secrets Manager; env files; CI secrets; xcconfig). Names only.
7. **Integrations:** every inbound webhook and how it's authenticated, and every outbound third-party API and production hostname. Also note libraries that make network calls during verification, such as JWKS fetches, OCSP or online certificate checks, license checks, and telemetry, so the prompt can tell the audit model to mock them.
8. **Supply chain and CI:** lockfile, install scripts, what a publish would include (`files`, `.npmignore`, `MANIFEST.in`), GitHub Actions (`pull_request_target`, `${{ github.event.* }}` inside `run:`, unpinned third-party actions, token permissions).
9. **Deploy and edge:** hosting config (for example Railway, Fly.io, Render, Vercel, Cloudflare, Docker, or Kubernetes), trust-proxy settings, security headers, CORS.
10. **Verification harness:**
    - The test framework in each package, where tests live (next to the code or in a test directory), and how they're named. Note separate test environments, such as a DOM environment versus node, or unit versus integration projects.
    - The exact command to run a single test file in each package or workspace, including any project or workspace flags.
    - Whether tests run offline without secrets (setup files, mocks, in-memory databases). Find an existing test that already mocks the framework (stubbed framework globals, mocked database or cache modules) to name as the pattern to copy. If tests have no database or cache, note that plainly.
    - Tests that bind localhost ports or spawn servers. They may fail under strict sandbox mode.
    - Commands the audit model must not run because they load secrets or hit live services, such as a dev script wrapped in a secret-manager wrapper, or seed, migration, deploy, publish, and release scripts.
    - For Apple apps, whether a SwiftPM package allows `swift test` or only `xcodebuild test` exists.
    - Whether dependencies are already installed (`node_modules`, `.venv`, `.build`, `vendor/`, resolved packages).
    - The full test, lint, and typecheck commands, for the fix prompt.
11. **Prior security work:** `docs/security/**`, `SECURITY.md`, files with "audit" in the name, and `git log --since="6 months ago" --oneline -i -E --grep="secur|vuln|xss|csrf|ssrf|idor|auth|sec-"`. Sort earlier findings into fixed (retest), open (don't re-report), and needs-investigation (settle), keeping their IDs. Note any naming convention or glob the repo's docs use to track audits (for example `*-security-audit.md`) and any rules for updating them.
12. **Optional GitHub reads:** skip silently if `gh` isn't authenticated or there's no GitHub remote. Get open Dependabot alerts with `gh api --paginate "repos/{owner}/{repo}/dependabot/alerts?state=open" --jq '.[] | "\(.security_advisory.severity) \(.dependency.package.name) \(.security_advisory.ghsa_id) \(.security_advisory.summary)"'` and open code-scanning alerts with `gh api --paginate "repos/{owner}/{repo}/code-scanning/alerts?state=open" --jq '.[] | "\(.rule.security_severity_level // .rule.severity) \(.rule.id) \(.most_recent_instance.location.path):\(.most_recent_instance.location.start_line) \(.rule.description)"'`. If either returns HTTP 403 because the feature is disabled, or code scanning returns 404 because it has never run, say so in the warnings.
13. **Fix-phase conventions:** the integration branch that PRs target (from CONTRIBUTING.md or CLAUDE.md, or `git symbolic-ref --short refs/remotes/origin/HEAD`), and where the repo states its commit, PR, and review rules.

For a large repo, hand the breadth sweep (items 2, 4, 7, 8, and the harness search in 10) to an Explore subagent with a precise list of what to return. Read the critical files yourself: auth middleware, tenancy guard, webhook handlers, encryption.

## 3. Choose attacker goals

Use [attack-catalog.md](attack-catalog.md). Pick the 5 to 9 goals that fit this repo and rewrite each in this repo's terms, naming:

- the real actors (stranger, free user, paying tenant, another household, a malicious package consumer),
- the real assets (which API keys, which PII, which printers or devices),
- the real features and files.

Drop catalog items that don't apply, order by risk, and add anything specific to this repo that the catalog lacks. Fold open code-scanning alerts into the goal they belong to, as leads to prove or dismiss. If a focus was given, put most goals inside that area, but keep enough of the surrounding map to find paths into it.

## 4. Write the audit prompt

Fill in [prompt-template.md](prompt-template.md).

- Write the opening line from step 1.
- Keep the scope and rules section, adapting the forbidden commands, secret files, production hosts, and third-party list to this repo. For third-party testing, limit the scope to the engagement's scope.
- The read-first list should hold at most 8 docs, all relevant to security.
- Name the exact test framework, where new tests go, the test to copy, what to mock, and the run command:
  - Place new tests by the repo's convention (next to the code or in its test directory), with a `cvp` marker in the file name so they're easy to find and keep out of merges: `*.cvp.test.ts`, `test_cvp_*.py`, `*_cvp_test.go`, `CVP*Tests.swift`, and so on. Name a separate location for each test environment, such as DOM versus node.
  - Name the existing test whose mocking to copy. Say plainly when tests have no database or cache.
  - Tell the audit model to mock the libraries from recon item 7 that call the network during verification.
  - Give the exact single-file run command for each package or workspace, including project or workspace flags.
  - If there's no harness, tell the audit model to use the language's built-in runner (`node --test`, `python -m unittest`, `go test`, `cargo test`, `swift test`) in a `security-tests/` directory without adding dependencies.
  - If tests bind localhost ports or spawn servers, say they may fail in the sandbox and to call handlers in-process where it can.
- Include the retest section only if earlier findings exist, and the dependency section only if there are open alerts.
- Report path: follow the existing convention (for example `docs/security/`), and match any naming glob the repo's docs use for audit tracking (for example `*-security-audit.md`), so the repo's own tracking rules apply. Otherwise use `docs/security/<date>-cvp-security-audit.md`.
- Aim for 60 to 110 lines. Include only what the audit model needs, with no commentary about this recon. Go longer only when surfaces share auth or sessions and must be audited together (for example an app and an admin dashboard that share a session cookie), and say why in the warnings.
- If the repo has several large, independent surfaces (more than about three deployable apps), write one prompt per surface instead of one giant prompt.
- Before saving, check that every path the prompt cites exists.

## 5. Write the fix prompt

Fill in [fix-prompt-template.md](fix-prompt-template.md) with the report path, the test naming and run commands from step 4, the audit branch from the checklist, and, from recon, the integration branch, the full check commands, and the repo's commit, PR, review, and security-tracking rules. For several surfaces, write one fix prompt that covers every report.

## 6. Deliver

1. Save the audit prompt to `~/.claude/cvp-audit-prompts/<repo-name>-<date>.md` and the fix prompt to `~/.claude/cvp-audit-prompts/<repo-name>-<date>-fix.md`, creating the directory if needed. For several surfaces, add a surface suffix to each audit prompt. Don't overwrite an earlier file; add `-2`, `-3`, and so on. Claude Code protects `~/.claude/`, so expect an approval prompt for these writes (in auto mode, the classifier reviews them).
2. Copy the audit prompt to the clipboard with the first of these that exists: `pbcopy`, `wl-copy`, `xclip -selection clipboard`, `clip.exe` (for example `pbcopy < <file>`). If none exists or the copy fails, skip it and tell the user to run `/copy` and pick the prompt's code block.
3. Reply with:
   - one line saying where the audit prompt is saved and whether it's on the clipboard,
   - the prompt in a `text` code block,
   - the launch checklist below, filled in for this repo,
   - the fix prompt's path, and when to use it: once the audit has written its report, paste it into a normal, unsandboxed session on an Opus-class model,
   - warnings.

```text
Before launching (outside the sandbox)
- <install dependencies if missing, e.g. npm ci, pnpm install, uv sync, bundle install>, so the sandboxed session doesn't need the network
- <rebuild a stale workspace build, only if recon found one>
- git switch -c security/cvp-audit-<date>   (keeps the new tests and report easy to review)

Launch
cd <repo_root>
claude --model <audit-model-id>

In the session
1. Status bar shows "⏵⏵ auto mode on" (Shift+Tab until it does). If this model doesn't offer auto mode, use "⏵⏵ accept edits on"
2. /sandbox → Mode: auto-allow, then Overrides → Strict sandbox mode on
3. Ask Claude to run: touch ~/sandbox-probe   → expect "Operation not permitted" (macOS) or "Read-only file system" (Linux, WSL2). If it succeeds, delete the file and check /sandbox before going on
4. Paste the prompt
5. Network: deny anything you can't explain. Package registries only if an install is unavoidable. In auto mode a command names the hosts it needs instead of prompting, so stop the session if one names a host you can't explain
```

Without `--model`, print the launch line as `claude --model <audit-model>` and add: pick the strongest model your account offers for security work (`/model` lists them). If there's no git, replace the branch line with a suggestion to run `git init` and make a baseline commit, so the audit's files are easy to review and the fix prompt's branch steps work.

Add any warnings from recon after the checklist, for example:

- tests need a database or cache, which the prompt tells the audit model to mock;
- only `xcodebuild` is available, so some proofs may need running outside the sandbox;
- a committed secret, by path and line;
- Dependabot or code scanning is disabled (HTTP 403);
- a workspace build is stale and must be rebuilt before launch;
- tests bind localhost ports or spawn servers and may fail under strict sandbox mode;
- the prompt runs past 110 lines because surfaces share auth or sessions;
- local secret files such as `.env` exist: the sandbox covers shell commands only, and Claude's Read tool follows permission rules, so add deny rules for those files before launching.

End with this warning every time: the prompts map the repo's attack surface, so keep them out of the repo and don't post them publicly.
