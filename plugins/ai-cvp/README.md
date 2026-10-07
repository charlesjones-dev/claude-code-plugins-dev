# AI-CVP Plugin

Plans a sandboxed security audit, so the strongest model you can use spends its time finding and proving bugs instead of learning the repo. Use it only on code you own or are authorized to test.

---

## What This Plugin Does

`/cvp-defense-audit` is phase 1 of a three-phase audit. It reads the repo without changing it, then writes two prompts and a checklist:

- **An audit prompt** to paste into a new, sandboxed Claude Code session. It names this repo's attacker goals, files, banned commands, secret paths, production hosts and test commands.
- **A launch checklist** for that session: dependencies, an audit branch, auto mode, strict sandbox mode, and a probe that confirms the sandbox is on.
- **A fix prompt** for phase 3, which verifies each finding and fixes the ones you pick.

CVP refers to [Anthropic's Cyber Verification Program](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet), which gives qualifying security teams, open-source maintainers and researchers advanced cyber capabilities with fewer blocked requests. You don't need to be enrolled. The skill asks what authorizes the audit and writes only that into the prompt.

### The three phases

| Phase | Where it runs | Model tier | Sandboxed? | Network? | Output |
|---|---|---|---|---|---|
| 1. Plan (`/cvp-defense-audit`) | A normal Claude Code session in the repo | Planning model: Opus-class | No | Only optional `gh` reads of GitHub alerts | Audit prompt, launch checklist and fix prompt, saved to `~/.claude/cvp-audit-prompts/` |
| 2. Audit | A new session in the repo, in auto mode with `/sandbox` in strict mode | Audit model: the strongest security-capable model you can use | Yes, strict | None. Third-party services are mocked | One failing proof test per finding and a report, on an audit branch. Nothing is fixed |
| 3. Fix | A normal session in the repo | Fixing model: Opus-class | No | Yes, for GitHub, CI and deploys, plus read-only provider checks you approve | Verified findings, a fix per change you pick with its proof test kept as the regression test, and an updated report |

Opus-class means the current Opus model or one at least as capable (as of October 2026, Claude Opus 5.5). The audit model can be any model your account offers; some with stronger security capabilities require enrollment in the Cyber Verification Program.

## Available Skills

### `/cvp-defense-audit`

**How it works:**

1. Classifies the project (web app or API, Apple app, library, CLI or Claude Code plugin, Home Assistant integration, static site) and works out the owner from LICENSE, the manifest and the remote
2. Asks what authorizes the audit: enrollment in the Cyber Verification Program, ownership or maintenance of the code, or an authorized third-party engagement. It never claims enrollment you didn't state
3. Does read-only recon: entry points, auth and tenancy, untrusted-input sinks, billing, secrets (names only), integrations, CI and supply chain, deploy config, the test harness and earlier audits. With `gh` signed in, it also reads open Dependabot and code-scanning alerts. On a large repo, a read-only Explore subagent does the breadth sweep while the skill reads the auth, tenancy, webhook and encryption code itself
4. Picks 5 to 9 attacker goals from [`attack-catalog.md`](skills/cvp-defense-audit/attack-catalog.md) and rewrites each in the repo's own actors, assets and files
5. Fills in [`prompt-template.md`](skills/cvp-defense-audit/prompt-template.md): the rules for this repo, up to 8 files to read first, the goals, a retest section for earlier findings, open alerts, and how to prove each finding. That means the test framework, a file name with a `cvp` marker placed by the repo's convention, an existing test whose mocking to copy, the libraries to mock, and the single-file run command for each package. It checks that every path it cites exists
6. Fills in [`fix-prompt-template.md`](skills/cvp-defense-audit/fix-prompt-template.md) for phase 3
7. Saves both prompts outside the repo, copies the audit prompt to the clipboard, and replies with the prompt, the filled-in launch checklist and any warnings, such as a stale workspace build or tests that bind localhost ports

**Usage:**

```
/cvp-defense-audit
/cvp-defense-audit billing
/cvp-defense-audit src/auth --model <audit-model-id>
```

The focus is optional: an area or a path. Most goals then land there, with enough of the surrounding map to find paths in. `--model` fills in the launch line. Without it, the checklist says `claude --model <audit-model>`, and you pick the strongest model your account offers for security work (`/model` lists them).

### Phase 2: run the audit

Follow the printed checklist. In short:

1. Outside the sandbox, install dependencies and create an audit branch
2. Start `claude --model <audit-model-id>` in the repo, and check that the status bar shows `⏵⏵ auto mode on` (Shift+Tab cycles modes)
3. Run `/sandbox`, choose auto-allow on the Mode tab, then turn on Strict sandbox mode on the Overrides tab
4. Ask Claude to run `touch ~/sandbox-probe`. It should fail with `Operation not permitted` on macOS, or `Read-only file system` on Linux and WSL2
5. Paste the prompt, and deny any network access you can't explain

The audit model maps the attack surface, hunts each goal, writes one failing test per finding as proof, and writes a report. It doesn't fix anything or commit.

### Phase 3: verify and fix

Once the report is written, open a normal, unsandboxed session on an Opus-class model and paste the fix prompt (`<repo>-<date>-fix.md`). It:

- re-runs each Confirmed proof test outside the sandbox and downgrades any that don't fail for the reason the report gives;
- proposes exact checks for what code alone couldn't settle (dashboards, CLIs, provider settings), and runs read-only ones only with your OK;
- shows a triage table (ID, severity, verified, effort, proposed grouping) and asks which to fix;
- fixes each pick on a branch from your integration branch, keeps the proof test as the regression test, and runs the full test suite, lint and typecheck;
- never merges the audit branch, whose tests fail by design, and updates the report with each finding's status, date, commits or PR, and how it was verified.

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

- **Claude Code with `/sandbox` and auto mode.** The sandbox runs on macOS, Linux and WSL2. Linux and WSL2 also need `bubblewrap` and `socat`. On native Windows, Claude Code runs commands unsandboxed, so run the audit in WSL2. Auto mode needs a supported model, and an organization admin can turn it off. If your audit model doesn't offer auto mode, use accept-edits mode; the sandbox's auto-allow still runs sandboxed commands without prompts.
- **Access to a strong audit model.** Some require enrollment, such as models offered through the Cyber Verification Program.
- **`gh`, optionally,** signed in, to include open Dependabot and code-scanning alerts.
- **Dependencies installed before launch,** so the sandboxed session doesn't need the network.

## What it writes

| File | Contents |
|---|---|
| `~/.claude/cvp-audit-prompts/<repo>-<date>.md` | The audit prompt. Repos with more than about three independent deployables get one prompt per surface, with a suffix |
| `~/.claude/cvp-audit-prompts/<repo>-<date>-fix.md` | The fix prompt for phase 3 |

Phase 1 writes nothing inside the repo. Claude Code protects `~/.claude/`, so expect an approval prompt for these writes (in auto mode, the classifier reviews them instead).

These files are sensitive. They map your attack surface: entry points, weak spots to try, where secrets live and which hosts are production. Keep them out of the repo, and don't post them in issues, chats or gists.

Phase 2 adds the proof tests (with `cvp` in their file names) and the report to the repo, on the audit branch.

## Authorization and safety

- Use this only on code you own or are authorized to test. The skill asks what authorizes the audit and writes only that into the prompt. It doesn't claim Cyber Verification Program enrollment unless you say you're enrolled, and it stops if you have no authorization.
- The audit prompt limits scope to this repository, bans network requests to production and third parties, requires every third-party service to be mocked, and forbids changing application code, committing and switching branches.
- Recon in phase 1 is read-only. It doesn't run the app, tests, builds, installs or anything that loads secrets, and it cites a committed secret by path and line, never by value.
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
- **Version:** 1.0.0
- **License:** MIT
- **Author:** Charles Jones

---

## Contributing

Bug reports and fixes are welcome. See [CONTRIBUTING.md](../../CONTRIBUTING.md).

---

## License

MIT License. See [LICENSE](LICENSE).
