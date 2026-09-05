# AI-Security

Security tools for reviewing your code, checking a live website, and protecting your development setup.

## Quick start

Install from this marketplace:

```text
/plugin install ai-security@claude-code-plugins-dev
```

Then open the repository you want to review and run:

```text
/ai-security:security-audit
```

To review a smaller part of the project, describe the scope:

```text
/ai-security:security-audit ./server — exclude generated files
```

## Choose a command

| Command | Use it to… |
| --- | --- |
| `/ai-security:security-audit` | Review source code and save a report explaining possible problems, supporting evidence, and suggested fixes. |
| `/ai-security:security-scan-dependencies` | Check a live website for visible outdated libraries, known vulnerabilities, and browser protection settings; it asks for the URL and scope. |
| `/ai-security:security-init` | Set up Claude Code file-access rules for sensitive files such as credentials and environment files. |
| `/ai-security:security-supply-chain` | Configure a pnpm project to delay installing newly published packages and keep automated builds aligned with its lockfile. |

Some hosts also expose shorter aliases such as `/security-audit`.

The two setup commands show proposed configuration changes for approval. After using `security-init`, restart Claude Code for its settings to take effect; this step is optional and is not required to run an audit. The supply-chain command checks pnpm compatibility before making changes.

## What to expect from an audit

By default, the audit reviews the current repository, including application code, background jobs, configuration, and dependencies. It checks suspected problems against the code and uses small local tests where practical. Live infrastructure, vendor dashboards, and setting up a full test environment are not required unless you request that scope.

Reports are saved inside your repository:

```text
docs/security/YYYY-MM-DD-HHMMSS-security-audit.md
docs/security/YYYY-MM-DD-HHMMSS-security-audit.json
```

Start with the Markdown summary and table of contents, then jump to the findings you need. The matching JSON keeps the full evidence and commands for deeper review or automation. Reports explain:

- **What was reviewed** and which areas still need attention.
- **Confirmed problems**, their likely impact, and recommended next steps.
- **Uncertain concerns** separately from confirmed problems and optional improvements.
- **Changes since a previous audit**, when a previous report is selected or supplied.

The audit uses at most two reviewers at a time by default and closes its workers when they finish. If the host cannot manage workers reliably, the main assistant does the review itself. Reviewers contribute evidence to one final report, not separate reports for you to sort through.

You can ask the audit to compare against a specific report:

```text
/ai-security:security-audit compare against docs/security/<previous-report>.md
```

**Complete** means the agreed review work is finished. It can still say **follow-up remains** when a concern needs a production setting or vendor fact that the code cannot answer. Those concerns stay visible with next steps. **Partial** means actual review work is unfinished, such as unread routes or required tests that were skipped. Saving a report is not a reason to stop while useful, authorized checks remain.

A finding disappearing from a report does not mean it was fixed; the comparison should explain what happened to it. Suggested fixes still need review and testing.

Python 3.9+ is needed for automatic report checking and formatting. If it is unavailable, the assistant can produce a partial report and explain which checks were skipped.

## Limits

Results depend on the available code, tools, and review time. Audits can miss problems or make mistakes, and they do not certify compliance or guarantee an identical result on every run. Use them alongside your existing tests, dependency scanners, and security reviews.

A website scan sees what the site exposes publicly; it cannot establish the security of private server code or infrastructure.

## Updating and automation

Source edits do not update an installed plugin. Once a new version is available through your configured marketplace, refresh the marketplace, update the plugin, and reload plugins or start a new session as your host requires.

**Upgrading from 1.x:** Version 2.0 changes the audit report format. New reports use JSON schema 1.1; existing schema 1.0 reports keep their original completion rules. See the [report format guide](skills/security-audit/references/artifacts.md). Automations that previously launched the `security-auditor` helper directly should invoke `/ai-security:security-audit` for a complete audit.

## Detailed guidance

- [Audit workflow](skills/security-audit/SKILL.md) and [review methodology](skills/security-audit/references/methodology.md)
- [Report format and tools](skills/security-audit/references/artifacts.md)
- [Website scanning](skills/security-scan-dependencies/SKILL.md)
- [Claude Code file-access setup](skills/security-init/SKILL.md)
- [pnpm supply-chain setup](skills/security-supply-chain/SKILL.md)

**Version:** 2.0.0 · **Author:** Charles Jones · **License:** [MIT](../../LICENSE)
