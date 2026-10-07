# Fix prompt template

Phase 3. Fill every `{PLACEHOLDER}`, delete each `{IF_...}` line whose condition is false, and save the result next to the audit prompt as `<repo-name>-<date>-fix.md`. The user pastes it into a normal, unsandboxed session on an Opus-class model once the audit session has written its report.

## Placeholder notes

- `{REPORT_PATH}`, `{TEST_NAME_PATTERN}`, `{TEST_COMMAND}`, and `{INFRA}`: the same values as the audit prompt. For several surfaces, list every report and its test command.
- `{INTEGRATION_BRANCH}`: the branch PRs target, from recon item 13.
- `{CHECK_COMMANDS}`: the full test suite, lint, and typecheck, as the repo runs them (package scripts, Makefile, or CI workflow).
- `{CONVENTIONS}`: where the repo states its commit, PR, and review rules (CLAUDE.md, CONTRIBUTING.md, a PR template). If nothing is written down, use "the style of recent commits and PRs".
- `{TRACKING_RULES}`: the file or section holding the repo's security-tracking rules, if any.

---

```text
The security audit of {NAME} is done. The audit session wrote {REPORT_PATH}
and archived one failing proof test per Confirmed finding ({TEST_NAME_PATTERN})
under docs/security/tests/, each at the repo-relative path it runs from with
`.disabled` appended. Git ignores docs/security/. This session isn't
sandboxed. Verify the findings, help me choose what to fix, and fix only what
I pick.

## Rules
- Commit, push, or open a PR only after I say so. Follow {CONVENTIONS}.
- Run read-only checks against {INFRA} only after I OK each one. Don't change
  live settings or data.
- Never commit anything under docs/security/, and never force-add it. The
  report and archived tests stay local. Proof tests fail by design, so one
  enters the source tree only together with its fix.
- Don't print secret values. Cite them by path and line.

## 1. Read
- Check that git ignores docs/security/, with
  `git check-ignore -q docs/security/probe`. If it exits non-zero, append
  `/docs/security/` to the file `git rev-parse --git-path info/exclude` prints,
  and tell me. Don't edit .gitignore.
- Run `git status`. It should list nothing. Move any cvp test or helper it
  lists into docs/security/tests/ the way the audit archives them. Show me any
  other change before doing anything else.
- Read {REPORT_PATH} and every archived proof test it cites.
{IF_TRACKING_RULES: "- Read {TRACKING_RULES} and follow them for every report update."}

## 2. Verify each Confirmed finding
Run each proof test here, outside the sandbox: copy it, and any archived
helper it imports, from docs/security/tests/ to its source path without
`.disabled`, run it with `{TEST_COMMAND}`, then delete the copies. Check that it fails for the reason the
report gives, not because of a missing mock, network access, or setup. If it
passes, or fails for another reason, downgrade the finding to Unconfirmed and
say why. Read the code path yourself before you accept a severity.

## 3. Settle what the code couldn't
For each item the report says to check in {INFRA}, propose the exact check: the
dashboard page, CLI command, or provider setting to look at, and which result
means the finding is real. Run read-only CLI checks only after I OK them. I'll
do the dashboard checks and tell you what I see.

## 4. Triage
Show a table: ID, severity, verified (yes, no, or downgraded), effort (S, M, or
L), and proposed grouping. Group related findings, such as ones that share a
root cause or a fix, into one change. Then ask which to fix. Fix nothing I
don't pick.

## 5. Fix
For each change I pick:
- Branch from {INTEGRATION_BRANCH}.
- Restore the proof test of each finding in the change, and any archived
  helper it imports: move it from docs/security/tests/ to its source path
  without `.disabled`, which also removes the archived copy:
  `mv docs/security/tests/<path>.disabled <path>`
  Run it and confirm it fails. Then fix the code until it passes.
- Keep it as the regression test. Rename it if the repo's naming convention
  doesn't fit {TEST_NAME_PATTERN}.
- Run the full test suite, lint, and typecheck: {CHECK_COMMANDS}.
- Before committing, check that `git status` lists no docs/security/ paths
  and no proof tests other than the ones this change fixes.
- Show me the diff, and wait for my OK before committing.

## 6. Update the report
For each finding, record its status, the date, the commits or PR, and how the
fix was verified. Keep "fixed on a branch", "merged", and "deployed" distinct.
Don't mark a finding deployed until I confirm it is.

## 7. When the fixes have merged
Tell me to run /cvp-defense-audit again. Its recon reads the updated report and
adds a retest section for the fixed IDs.
```
