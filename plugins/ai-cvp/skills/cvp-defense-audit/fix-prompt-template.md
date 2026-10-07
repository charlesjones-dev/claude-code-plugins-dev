# Fix prompt template

Phase 3. Fill every `{PLACEHOLDER}`, delete each `{IF_...}` line whose condition is false, and save the result next to the audit prompt as `<repo-name>-<date>-fix.md`. The user pastes it into a normal, unsandboxed session on an Opus-class model once the audit session has written its report.

## Placeholder notes

- `{REPORT_PATH}`, `{TEST_NAME_PATTERN}`, `{TEST_COMMAND}`, and `{INFRA}`: the same values as the audit prompt. For several surfaces, list every report and its test command.
- `{AUDIT_BRANCH}`: the branch from the launch checklist, such as `security/cvp-audit-<date>`.
- `{INTEGRATION_BRANCH}`: the branch PRs target, from recon item 13.
- `{CHECK_COMMANDS}`: the full test suite, lint, and typecheck, as the repo runs them (package scripts, Makefile, or CI workflow).
- `{CONVENTIONS}`: where the repo states its commit, PR, and review rules (CLAUDE.md, CONTRIBUTING.md, a PR template). If nothing is written down, use "the style of recent commits and PRs".
- `{TRACKING_RULES}`: the file or section holding the repo's security-tracking rules, if any.

---

```text
The security audit of {NAME} is done. The audit session wrote {REPORT_PATH}
and one failing proof test per Confirmed finding ({TEST_NAME_PATTERN}) on
branch {AUDIT_BRANCH}. This session isn't sandboxed. Verify the findings, help
me choose what to fix, and fix only what I pick.

## Rules
- Commit, push, or open a PR only after I say so. Follow {CONVENTIONS}.
- Run read-only checks against {INFRA} only after I OK each one. Don't change
  live settings or data.
- Never merge {AUDIT_BRANCH} as it is: its proof tests fail by design. The
  report lands as a docs-only change or with the first fix.
- Don't print secret values. Cite them by path and line.

## 1. Read
- Switch to {AUDIT_BRANCH} and run `git status`. The audit session couldn't
  commit, so the report and tests are probably uncommitted. Ask me before
  committing them to {AUDIT_BRANCH} as one local commit that's never pushed.
- Read {REPORT_PATH} and every proof test it cites.
{IF_TRACKING_RULES: "- Read {TRACKING_RULES} and follow them for every report update."}

## 2. Verify each Confirmed finding
Run each proof test here, outside the sandbox, with `{TEST_COMMAND}`. Check
that it fails for the reason the report gives, not because of a missing mock,
network access, or setup. If it passes, or fails for another reason, downgrade
the finding to Unconfirmed and say why. Read the code path yourself before you
accept a severity.

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
- Branch from {INTEGRATION_BRANCH}, not {AUDIT_BRANCH}.
- Bring the finding's proof test along (`git checkout {AUDIT_BRANCH} -- <test
  file>`), run it, and confirm it fails. Then fix the code until it passes.
- Keep it as the regression test. Rename it if the repo's naming convention
  doesn't fit {TEST_NAME_PATTERN}.
- Run the full test suite, lint, and typecheck: {CHECK_COMMANDS}.
- Show me the diff, and wait for my OK before committing.

## 6. Update the report
For each finding, record its status, the date, the commits or PR, and how the
fix was verified. Keep "fixed on a branch", "merged", and "deployed" distinct.
Don't mark a finding deployed until I confirm it is.

## 7. When the fixes have merged
Tell me to run /cvp-defense-audit again. Its recon reads the updated report and
adds a retest section for the fixed IDs.
```
