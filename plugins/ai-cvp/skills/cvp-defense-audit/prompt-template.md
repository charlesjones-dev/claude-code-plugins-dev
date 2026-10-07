# Audit prompt template

Fill every `{PLACEHOLDER}`. Delete sections marked "optional" when they don't apply, and delete each `{IF_...}` line whose condition is false. Keep the wording of the rules, method, and report sections unless this repo needs a change. That wording was tuned against real runs.

## Opening line

`{OWNERSHIP}` is the ownership line from step 1 of SKILL.md. `{AUTHORIZATION}` comes from the user's answer, and states nothing beyond it:

| Answer | `{AUTHORIZATION}` |
|---|---|
| Enrolled in the Cyber Verification Program | `I'm in Anthropic's Cyber Verification Program with {ACCESS_LEVEL}, and this session is sandboxed.` Without an access level: `I'm in Anthropic's Cyber Verification Program, and this session is sandboxed.` |
| Owner or maintainer, not enrolled | `This session is sandboxed.` |
| Authorized third-party testing | `I'm authorized to test it under {ENGAGEMENT}, limited to {SCOPE}, and this session is sandboxed.` |

## Placeholder notes

- `{SCOPE_LIMIT}`: empty, or `, limited to {SCOPE}` for third-party testing.
- `{FORBIDDEN_COMMANDS}`: the exact dev, start, seed, migration, deploy, publish, and release scripts, secret-manager wrappers and the scripts that call them, and installs or builds that need the network.
- `{SECRET_FILES}`: only the ones that exist or apply, such as `.env*` (except `.env.example`), credential files, registry credentials (`~/.npmrc`, `~/.pypirc`), and the config directories of the secret manager, cloud CLIs, and `gh`.
- `{PROD_HOSTS}` and `{THIRD_PARTIES}`: from recon items 7 and 9. If the repo has neither (many libraries and CLIs), replace that bullet with "Make no network requests. If something truly needs network access, stop and ask me first."
- `{CODE_KIND}`: application, library, or app.
- `{TEST_PLACEMENT}`: where new tests go and how they're named, by the repo's convention, with the `cvp` marker. For example "named `*.cvp.test.ts` next to the code it targets" or "named `test_cvp_*.py` under tests/security/". When test environments differ, name the location for each.
- `{TEST_SETUP}`: one to four sentences, or delete it. The existing test to copy and how it mocks the framework, database, or cache. "There's no database or cache in tests," when true. The libraries to mock because they call the network during verification (JWKS fetches, OCSP, license checks, telemetry). "No new dependencies." When tests bind ports or spawn servers: "Tests that bind localhost ports or start servers may fail in this sandbox; call handlers in-process where you can."
- `{TEST_COMMAND}`: the exact single-file command. In a monorepo, give one per package or workspace with its project or workspace flags.
- `{INFRA}`: the hosting, provider, and store dashboards to check. For a library, the package registry and repository settings.

## Example

An invented Express + Vue multi-tenant invoicing SaaS that stores each tenant's payment-processor and SMS API keys, to show the level of specificity expected:

- Actors: "an admin or member of a paying tenant, a user on a free trial, an invoice recipient holding a public payment link, or an unauthenticated stranger"
- Goal: "Get another tenant's payment-processor or SMS API key in plaintext, or weaken the per-tenant encryption that protects them (key derivation, nonce reuse, plaintext fallbacks, the key-rotation script in server/scripts/rotate-keys.ts)."
- Forbidden: "Do NOT run `npm run dev` or `npm run db:seed` (both wrap `op run`), `docker compose up`, or anything that loads real secrets."
- Test setup: "Follow server/routes/invoices.test.ts, which stubs `req.tenant` and mocks server/db.ts. There's no database in tests. Mock the payment SDK and the JWKS fetch in server/auth/verify.ts. Component tests that need jsdom go in client/tests/. Run with `npx vitest run --project server <file>`, or `--project client` for client tests."

---

```text
This is {NAME}: {ONE_LINE_PURPOSE}. It's {OWNERSHIP}. {AUTHORIZATION} I want a
deep security review of this codebase that finds real, exploitable bugs and
proves each one.
{OPTIONAL_FOCUS_LINE: "Focus on {AREA}; cover the rest only as far as it leads into {AREA}."}

## Scope and rules
- In scope: this repository only{SCOPE_LIMIT}, exercised through {HARNESS} and
  local code.
- Do NOT run {FORBIDDEN_COMMANDS}, or anything that loads real secrets. Don't
  read {SECRET_FILES}.
- Make no network requests to production ({PROD_HOSTS}) or to {THIRD_PARTIES}.
  Mock every third-party service. If something truly needs network access, stop
  and ask me first.
- Don't change {CODE_KIND} code. Only add test files and the report below.
- No git commits, pushes, or branch changes.

## Read first
{READ_FIRST: bullet list, at most 8 paths, security-relevant only}
{IF_PRIOR_AUDIT: "- {PRIOR_AUDIT_PATH}. Don't re-report its open findings unless you find a worse variant or new impact."}

## Attacker goals to pursue
Think like {ACTORS} trying to:
1. {GOAL, in repo terms, naming real assets, features, and files}
2. ...
(5 to 9 goals, riskiest first)

## Retest the previous audit (optional)
- Try to bypass the fixes for {FIXED_IDS}.
- Settle the needs-investigation items {NEEDS_INVESTIGATION_IDS} as far as the
  code allows. For anything that depends on live {INFRA} setup, tell me exactly
  what to check and how.

## Open dependency alerts (optional)
{ALERT_LIST: severity, package, advisory ID, one-line summary}
For each one, decide whether the vulnerable code is reachable from this
codebase. Prove it's reachable with a test, or show the call path that makes it
unreachable.

## Method
1. Map the attack surface: every {SURFACE_UNIT: route / entry point / public
   API / command / URL handler}, what protects it, {TENANCY_LINE: "where
   tenantId comes from,"} and every place untrusted input reaches {SINKS}. Show
   me the map, then keep going.
2. Hunt each attacker goal against that map. Prefer depth on the riskiest paths
   over a broad checklist.
3. For every candidate, write a {FRAMEWORK} test {TEST_PLACEMENT} that fails on
   the current code and demonstrates the bug, with external services mocked.
   {TEST_SETUP}
   Run it with `{TEST_COMMAND}`. A finding counts as Confirmed only if its test
   fails for the right reason. Otherwise mark it Unconfirmed and say what
   evidence is missing.
4. Before reporting, try to disprove each Confirmed finding: look for upstream
   checks, {ORDERING: middleware ordering / call-site validation}, or deploy
   config that blocks it.

## Report
Write {REPORT_PATH} with:
- A summary table: ID (CVP-01, ...), severity, Confirmed or Unconfirmed,
  one-line problem, file:line.
- For each finding: attacker and access needed, step-by-step exploit path,
  impact, the test that proves it, and a specific fix.
{IF_RETEST: "- Retest results for the previous audit's items."}
{IF_ALERTS: "- A reachable or unreachable verdict for each dependency alert."}
- What you couldn't determine from code, and what I should check in {INFRA}.
Don't fix anything yet. I'll choose what to fix after reading the report.
```
