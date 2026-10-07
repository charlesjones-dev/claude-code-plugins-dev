# AI-CVP Plugin

Plans a sandboxed security audit, so the strongest model you can use spends its time finding and proving bugs instead of learning the repo. Use it only on code you own or are authorized to test.

---

## What This Plugin Does

`/cvp-defense-audit` is phase 1 of a three-phase audit. It reads the repo, makes sure git ignores `docs/security/`, and then writes two prompts and a checklist:

- **An audit prompt** to paste into a new, sandboxed Claude Code session. It names this repo's attacker goals, files, banned commands, secret paths, production hosts and test commands.
- **A launch checklist** for that session: dependencies, a clean working tree, a one-line launch that turns on auto mode and a strict sandbox, and a probe that confirms the sandbox is on.
- **A fix prompt** for phase 3, which verifies each finding and fixes the ones you pick.

CVP refers to [Anthropic's Cyber Verification Program](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet), which gives qualifying security teams, open-source maintainers and researchers advanced cyber capabilities with fewer blocked requests. You don't need to be enrolled. The skill asks what authorizes the audit and writes only that into the prompt.

### The three phases

| Phase | Where it runs | Model tier | Sandboxed? | Network? | Output |
|---|---|---|---|---|---|
| 1. Plan (`/cvp-defense-audit`) | A normal Claude Code session in the repo | Planning model: Opus-class | No | Only optional `gh` reads of GitHub alerts | Audit prompt, launch checklist and fix prompt, saved to `~/.claude/cvp-audit-prompts/`, plus a local ignore rule for `docs/security/` |
| 2. Audit | A new session in the repo, launched in auto mode with a strict sandbox | Audit model: the strongest security-capable model you can use | Yes, strict | None. Third-party services are mocked | A report in `docs/security/`, and one failing proof test per finding, archived as a `.disabled` file under `docs/security/tests/`. Nothing is fixed or committed |
| 3. Fix | A normal session in the repo | Fixing model: Opus-class | No | Yes, for GitHub, CI and deploys, plus read-only provider checks you approve | Verified findings, a fix per change you pick with its proof test restored as the regression test, and an updated report |

Opus-class means the current Opus model or one at least as capable (as of October 2026, Claude Opus 5.5). The audit model can be any model your account offers; some with stronger security capabilities require enrollment in the Cyber Verification Program.

## Available Skills

### `/cvp-defense-audit`

**How it works:**

1. Classifies the project (web app or API, Apple app, library, CLI or Claude Code plugin, Home Assistant integration, static site) and works out the owner from LICENSE, the manifest and the remote
2. Asks what authorizes the audit: enrollment in the Cyber Verification Program, ownership or maintenance of the code, or an authorized third-party engagement. It never claims enrollment you didn't state
3. Does read-only recon: entry points, auth and tenancy, untrusted-input sinks, billing, secrets (names only), integrations, CI and supply chain, deploy config, the test harness and earlier audits. With `gh` signed in, it also reads open Dependabot and code-scanning alerts. On a large repo, a read-only Explore subagent does the breadth sweep while the skill reads the auth, tenancy, webhook and encryption code itself
4. Picks 5 to 9 attacker goals from [`attack-catalog.md`](skills/cvp-defense-audit/attack-catalog.md) and rewrites each in the repo's own actors, assets and files
5. Fills in [`prompt-template.md`](skills/cvp-defense-audit/prompt-template.md): the rules for this repo, up to 8 files to read first, the goals, a retest section for earlier findings, open alerts, and how to prove each finding. That means the test framework, a file name with a `cvp` marker placed by the repo's convention, an existing test whose mocking to copy, the libraries to mock, the single-file run command for each package, and where to archive each test once it has run. It checks that every path it cites exists
6. Fills in [`fix-prompt-template.md`](skills/cvp-defense-audit/fix-prompt-template.md) for phase 3
7. Adds `/docs/security/` to `.git/info/exclude` unless git already ignores it, saves both prompts outside the repo, copies the audit prompt to the clipboard, and replies with the path to each prompt, a checklist for the audit session and one for the fix session, and any warnings, such as a stale workspace build or tests that bind localhost ports. It doesn't print the prompts; open the files to read or edit them

**Usage:**

```
/cvp-defense-audit
/cvp-defense-audit billing
/cvp-defense-audit src/auth --model <audit-model-id>
```

The focus is optional: an area or a path. Most goals then land there, with enough of the surrounding map to find paths in. `--model` fills in the launch line. Without it, the checklist says `claude --model <audit-model>`, and you pick the strongest model your account offers for security work (`/model` lists them).

### Phase 2: run the audit

Follow the printed checklist. In short:

1. Outside the sandbox, install dependencies and check that `git status` is clean
2. Start the audit session in the repo with the checklist's launch line:
   ```bash
   claude --model <audit-model-id> --permission-mode auto --settings '{"sandbox":{"enabled":true,"autoAllowBashIfSandboxed":true,"allowUnsandboxedCommands":false,"failIfUnavailable":true}}'
   ```
3. Check that the status bar shows `⏵⏵ auto mode on`, and that `/status` lists `Command line arguments` under setting sources
4. Ask Claude to run `touch ~/sandbox-probe`. It should fail with `Operation not permitted` on macOS, or `Read-only file system` on Linux and WSL2
5. Paste the prompt, and deny any network access you can't explain
6. When it finishes, check that `git status` lists nothing

The launch line replaces the `/sandbox` panel. Its settings last for that session only and write no file:

- `enabled` turns on the sandbox.
- `autoAllowBashIfSandboxed` runs sandboxed commands without prompts (auto-allow).
- `allowUnsandboxedCommands: false` turns on strict sandbox mode, so Claude can't retry a blocked command outside the sandbox. Set this way, it also makes the sandbox admin-required (Claude Code v2.1.285 or later): Claude Code ignores the repo's own `.claude/settings.json` and `.claude/settings.local.json` entries that would loosen it, such as `excludedCommands`, `allowWrite` and `allowedDomains`.
- `failIfUnavailable` makes Claude Code exit at startup if the sandbox can't start, instead of running commands unsandboxed.

`/sandbox` won't open in that session, because command-line settings outrank the file it saves to. If you use [ai-statusline](../ai-statusline/), turn on its sandbox indicator to see when your settings turn the sandbox on.

The audit model maps the attack surface, hunts each goal, proves each finding with a failing test, and writes a report. It runs each test where the repo keeps its tests, then moves it to `docs/security/tests/` with `.disabled` appended, so no failing test is left in the source tree. It doesn't fix anything or commit.

### Phase 3: verify and fix

Once the report is written, quit the audit session, start a normal, unsandboxed session on an Opus-class model (`claude --model opus`), and paste the fix prompt (`<repo>-<date>-fix.md`). The reply's fix checklist gives the command that copies it to the clipboard. The fix session:

- re-runs each Confirmed proof test outside the sandbox and downgrades any that don't fail for the reason the report gives;
- proposes exact checks for what code alone couldn't settle (dashboards, CLIs, provider settings), and runs read-only ones only with your OK;
- shows a triage table (ID, severity, verified, effort, proposed grouping) and asks which to fix;
- fixes each pick on a branch from your integration branch, moves its archived proof test back into place (dropping `.disabled`) as the regression test, and runs the full test suite, lint and typecheck;
- never commits anything under `docs/security/`, and updates the report with each finding's status, date, commits or PR, and how it was verified.

Commits, pushes and PRs wait for your consent. When the fixes have merged, run `/cvp-defense-audit` again. Its recon finds the updated report and adds a retest section for the fixed IDs.

## Why plan outside the sandbox

- **The audit model's budget goes to finding and proving bugs.** Orientation runs here, on a cheaper model plus a read-only subagent.
- **The guardrails are written before an unattended run starts.** Banned commands, secret paths and production hosts are set for this repo before the auto-mode session begins. You can read and edit them first, and the audit model doesn't set its own limits.
- **Steps that need network or credentials stay outside.** GitHub alert reads happen in phase 1, so the sandboxed session never needs your tokens.
- **Earlier audits arrive sorted.** Fixed findings become a retest list, open ones aren't re-reported, and needs-investigation items get settled, so the audit doesn't rediscover known findings.
- **The prompt is a saved file.** You can review it, edit it, rerun it and compare it across audits.
- **Finding and fixing happen in separate sessions.** The fixing session re-checks each finding before changing code, and only an unsandboxed session can push branches, open PRs and watch CI and deploys.

## Trade-offs

- The chosen goals can anchor the audit model on what recon noticed. The prompt's method still requires a full attack-surface map before hunting, which offsets this.
- The prompt goes stale as the code changes. If the code has moved since you generated it, run the skill again.
- If budget doesn't matter, a short prompt with only the rules may find more bugs off the map.

## Requirements

- **Claude Code v2.1.285 or later, with the sandbox and auto mode.** Earlier versions let the audited repo's own settings loosen a sandbox set on the command line. The sandbox runs on macOS, Linux and WSL2. Linux and WSL2 also need `bubblewrap` and `socat`. On native Windows, Claude Code runs commands unsandboxed, so run the audit in WSL2. Auto mode needs a supported model, and an organization admin can turn it off. If your audit model doesn't offer auto mode, launch with `--permission-mode acceptEdits` instead; auto-allow still runs sandboxed commands without prompts. Managed settings outrank `--settings`, so if your organization sets the sandbox keys, theirs apply.
- **Access to a strong audit model.** Some require enrollment, such as models offered through the Cyber Verification Program.
- **`gh`, optionally,** signed in, to include open Dependabot and code-scanning alerts.
- **Dependencies installed before launch,** so the sandboxed session doesn't need the network.

## What it writes

| File | Written in | Contents |
|---|---|---|
| `~/.claude/cvp-audit-prompts/<repo>-<date>.md` | Phase 1 | The audit prompt. Repos with more than about three independent deployables get one prompt per surface, with a suffix |
| `~/.claude/cvp-audit-prompts/<repo>-<date>-fix.md` | Phase 1 | The fix prompt for phase 3 |
| `.git/info/exclude` | Phase 1 | A `/docs/security/` line, unless git already ignores the folder |
| `docs/security/<date>-cvp-security-audit.md` | Phase 2 | The audit report |
| `docs/security/tests/<path>.disabled` | Phase 2 | One proof test per finding, stored under the repo-relative path it runs from, with `cvp` in its file name |

Phase 1 doesn't change any file git tracks. Claude Code protects `~/.claude/`, so expect an approval prompt for the prompt files (in auto mode, the classifier reviews them instead).

These files are sensitive. They map your attack surface: entry points, weak spots to try, where secrets live and which hosts are production. Don't commit them, and don't post them in issues, chats or gists.

Git ignores `docs/security/`, so the report and tests stay local, even in an open-source repo. The rule goes in `.git/info/exclude` rather than `.gitignore`, so it's never committed and nothing in the repo hints at the folder. It applies to this clone and all its worktrees. If you copy `docs/security/` into another clone, add the line there too. The rule also covers the reports ai-security's `/security-audit` and `/security-scan-dependencies` write there. Files git already tracks in `docs/security/` stay tracked, and the skill lists them in its warnings.

Proof tests fail by design, so the audit doesn't leave one in the source tree, where a commit would turn CI red. The `.disabled` suffix keeps the usual test, type-check and lint patterns from matching the archived copies. Each one keeps its original path, so the fix session restores it with a single `mv` once its fix is in.

## Authorization and safety

- Use this only on code you own or are authorized to test. The skill asks what authorizes the audit and writes only that into the prompt. It doesn't claim Cyber Verification Program enrollment unless you say you're enrolled, and it stops if you have no authorization.
- The audit prompt limits scope to this repository, bans network requests to production and third parties, requires every third-party service to be mocked, and forbids changing application code, committing and switching branches.
- Recon in phase 1 is read-only. It doesn't run the app, tests, builds, installs or anything that loads secrets, and it cites a committed secret by path and line, never by value. Phase 1 changes no file git tracks. Its one write inside the repo is the `docs/security/` line in `.git/info/exclude`.
- Strict sandbox mode stops Claude from retrying a blocked command outside the sandbox. The sandbox covers shell commands only: Claude's Read, Edit and Write tools follow your permission rules instead, and sandboxed commands can read most of your machine by default. Add deny rules for secret files before launching (`/security-init` in [ai-security](../ai-security/) writes them), and see `sandbox.credentials` in the [sandboxing docs](https://code.claude.com/docs/en/sandboxing).

### Related plugins

- `/security-audit` ([ai-security](../ai-security/)) runs an audit in the current session and keeps Markdown and JSON reports across runs.
- `/cvp-defense-audit` prepares a sandboxed run on a stronger model.
- Claude Code's built-in `/security-review` checks the pending changes on your branch.

---

## Quick Start

### Installation

```
/plugin install ai-cvp@claude-code-plugins-dev
```

Then run `/ai-cvp:cvp-defense-audit` from the repo you want to audit. The short form `/cvp-defense-audit` also works unless another command already uses that name.

---

## Plugin Details

- **Name:** AI-CVP Plugin
- **Type:** AI Instruction Plugin (Skills)
- **Skill:** `/cvp-defense-audit`
- **Version:** 1.0.2
- **License:** MIT
- **Author:** Charles Jones

---

## Contributing

Bug reports and fixes are welcome. See [CONTRIBUTING.md](../../CONTRIBUTING.md).

---

## License

MIT License. See [LICENSE](LICENSE).
