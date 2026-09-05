# Audit methodology

Read this before discovery and verification. The coordinator workflow lives in
[SKILL.md](../SKILL.md); field names and validation rules live in
[artifacts.md](artifacts.md). This is a verification method, not certification.

## Scope, provenance, and inventory

Record the root, revision (`git rev-parse HEAD` if available), branch, relevant dirty
paths and diff hashes without secret contents, start/end times with timezone, scope,
exclusions, and stopping conditions. Identify the plugin version from its manifest
and hash the skill plus supporting methodology/schema/scripts using the artifact
contract's hash convention. Hashing only SKILL.md misses changes in its references.
Record exposed model and reasoning setting, host/runtime/tool versions, reviewer
identities, and dependency scan source and time. Never infer hidden model routing
from a product label. Missing tools, credentials, budgets, or settings are operational
context, not vulnerabilities; only unfinished in-scope work belongs in top-level limitations.

The default is repository review with bounded local verification where practical.
Checked-in deployment configuration and client/provider integration paths are in scope;
live deployment inspection, vendor dashboards, provisioning databases/queues, and a full
end-to-end environment are not prerequisites unless requested. Describe those boundaries
at scope establishment and record external questions when they matter. Review third-party
code on relevant registration and enforcement paths, not every dependency's internals.

Start with `git ls-files` or `rg --files` (including relevant hidden configuration),
manifests, lockfiles, build definitions, framework registration, and package boundaries.
Record discovery commands and their exclusions. Compare file discovery against router
registries, framework route listings/build manifests when safely available, middleware
mounts, scheduler/queue registries, and dispatch tables. Trace dynamic registrations,
plugins, catch-all routes, reflection, generated code and their generators; unsupported
languages or unavailable generated artifacts leave explicit inventory gaps. Do not
execute project startup or builds blindly if they connect to live services.

Use a stable semantic surface ID such as `http:POST:/api/invites:accept`,
`queue:feed-refresh:producer:web`, or `script:deploy:publish`. Keep line locations
separate so IDs survive movement. For each surface, enumerate required checks from
the categories below, applicable ASVS requirements, and application-specific invariants.
For an absent category, retain a not-applicable coverage record with discovery evidence;
do not omit categories merely because initial searches returned nothing.

Each **surface/check pair** needs a stable identity, applicability, one status
(`reviewed`, `partially_reviewed`, `not_reviewed`, `not_applicable`), locations, what
was checked, evidence, and remaining gaps or rationale. A reviewed check can discover
a vulnerability; it does not mean secure. Discovery uncertainty is not not-applicable.
Equivalent surfaces may share a review only with a trace to the shared enforcement
and explicit exception analysis for every member, including alternate mounts and bypasses.

`gaps` means **unfinished review**, not a missing application control. Put a discovered
vulnerability or hardening suggestion in the candidate ledger; that check can be reviewed.
For completed source tracing, record an unavailable optional runtime test in the validation
record's limitations, not as incomplete coverage. A check can finish by establishing what
the repository enforces and exactly which external fact remains unknown. Retain that fact
as an open question or unconfirmed candidate. Incomplete local traces and explicitly
requested but unperformed tests remain gaps. Reviewer-local gaps resolved by another
reviewer's evidence must be reconciled before reporting repository-wide coverage.

Track individual files as discovered, pattern-screened, manually traced, and
behaviorally tested; these are different kinds of work, not interchangeable totals.
Where behavior is exercised through an integration test, record the actual boundary
and implementation files exercised, not every file in the test dependency tree.

## Verification foundation and check catalog

Pin **OWASP ASVS 5.0.0**, using the
[versioned release](https://github.com/OWASP/ASVS/tree/v5.0.0) and
[versioned requirement identifiers](https://owasp.org/www-project-application-security-verification-standard/)
(`v5.0.0-<chapter>.<section>.<requirement>`). Select applicable requirements and record
why others are inapplicable; verify IDs/text against the pinned release, not memory.
If the reference is unavailable, retain the pin, mark mapping unverified, and continue
application-specific review with that gap disclosed. Do not invent requirement IDs.
ASVS is a foundation for checks, not an ASVS certification or a promise to verify
every level. OWASP Top 10 can label themes; category coverage is never compliance.

| Surface category | Required targeted checks when applicable |
| --- | --- |
| HTTP/API routes and middleware | Method/path and public/authenticated access; middleware mount order and exceptions; auth, ownership and tenant checks; input-to-query/command/template/file sinks; CSRF, CORS, browser output contexts, errors and sensitive outputs. Verify framework defaults before alleging a missing control. Include GraphQL resolvers, batching/cost, RPC and alternate API versions. |
| Public entry points | Trace requests that enqueue jobs, persist writes, send email, invalidate caches or start expensive work. Verify admission before side effects; distinguish recipient, sender, tenant and aggregate limits, trusted identity sources, retries and key rotation by an attacker. |
| Background jobs and queues | Trace producers through admission, dedup key/lifetime, retries and completion to consumers. Execution concurrency does not bound admission/backlog. Check backlog growth, queue priority/fairness, distributed atomicity, failure recovery and whether one caller can starve others. Include schedules, dead-letter/retry paths and privileged payloads. |
| SSE, WebSocket and persistent connections | Initial auth plus per-event/message authorization, connection lifetime, per-client work/concurrency, backpressure, cleanup, expiry, revocation and tenant changes. Test hostile clients that ignore disconnect notices; consider missed events and connect/revoke races. |
| Auth, sessions and tokens | Login, recovery, MFA, OAuth/OIDC/SAML and native callbacks; issuer/audience/signature/algorithm and framework/library defaults; state/nonce/PKCE where relevant; session fixation, refresh/reuse, revocation, one-time atomic consumption and sensitive token outputs. Trace actual protocols and trust boundaries before prescribing mechanisms. |
| Payment, entitlement, invitation and business state | Signature validity versus current authorization; replay, old grants after revocation, reordered/duplicate events, ownership binding, capacity enforcement, atomic compare-and-update/transactions, concurrent consumers, idempotency retention and recovery. Verify both ingress and downstream state writes. |
| Uploads, imports, parsers and expensive computation | Content/type/path and size limits, decompression, malformed/deep inputs, regex/parser complexity independent of size and request frequency, cancellation and isolation. Timeouts may not interrupt synchronous CPU work; measure actual cancellation. |
| External requests and redirects | Destination and scheme policy, DNS/IP validation, redirect hops, connection-time enforcement, proxy paths, response size/decompression and timeout bounds. Include image/proxy/webhook/import and worker fetches; see SSRF below. |
| Data, tenants, storage and sensitive outputs | Read/write/delete ownership and tenant scope, bulk/export/search paths, caches and object keys, mass assignment, serialization, output encoding, logs and secret exposure; cryptographic purpose, integrity, key handling and operational assumptions. Distinguish a nonsecurity checksum from credential hashing. |
| Privileged scripts, deployment, CI and dependencies | Untrusted inputs to shell/build steps; permissions and secret boundaries; image/install provenance, lockfiles and dependency advisory reachability/version; deployment exposure, ingress trust, storage and logging configuration. Record scan registry/database version or retrieval time, command, lockfile hash, dev/prod scope, failures and offline/stale results. |

Extend these checks to the actual stack, including mobile, desktop, CLI and library
projects. HTTP controls are inapplicable to some projects; local file, IPC, update,
deserialization and privilege boundaries may matter more. Identify trust boundaries
and assets before treating a pattern as a vulnerability. Preserve application-specific
checks even when no ASVS requirement maps neatly.

## Candidate ledger and distinct verification pass

Allocate severity-independent IDs (`SEC-0001` or a stable semantic key) once; reviewers
use disjoint provisional namespaces. Store title, surface refs, source locations,
attacker access/privileges/prerequisites, input-to-operation or state-transition trace,
claimed impact, existing protections, evidence, counterevidence, assumptions, validation
method/results, disposition and rationale. Every substantive rejected or unresolved
candidate remains in the ledger, not just in private reasoning.

After discovery, explicitly challenge each candidate:

1. Follow the actual entry point through authentication, middleware, ownership and
   tenant enforcement to the sensitive operation, including downstream controls.
2. Inspect exact library/framework versions and relevant defaults; use primary
   documentation or installed source. Scanner hits and grep absence are leads, not proof.
3. Attempt a concrete disproof: unreachable path, enforced invariant, atomic operation,
   bounds, sanitization at the actual sink, invalid prerequisites, or insufficient impact.
4. Separate observed source/local behavior from assumed production exposure. Missing
   application controls and unknown edge controls are different facts. Record what
   deployment evidence would settle the question; do not silently assume either outcome.
5. Exercise actual repository functions and integration boundaries where practical for
   races, replay, revocation, parser complexity and resource amplification. Use temporary
   state, bounded workloads and subprocess timeouts. A reimplementation or a mock that
   removes the disputed middleware, database atomicity or provider check cannot prove
   repository behavior. Label any model of behavior illustrative and state its limits.
6. Record exact commands/reproduction files, environment and versions, expected versus
   observed outcomes, bounds/timeouts, exit status and limitations. Preserve enough
   sanitized input/state to rerun. Passing existing tests does not cover a new abuse
sequence unless those tests actually exercise it. No production stress, real email,
   live billing or unrelated targets without specific authorization.

Source reasoning can confirm a vulnerability when the reachable path, violated invariant,
controls and impact are established even without runtime access. Do not require dangerous
exploitation to confirm it. Conversely, neither an isolated scanner alert nor a speculative
worst-case impact can establish a confirmed finding.

| Disposition | Decision |
| --- | --- |
| `confirmed` | Supported reachable security violation; verification addressed relevant controls and no unresolved decisive assumption remains. |
| `needs_validation` | Plausible violation with a decisive missing fact or disputed control; state potential severity, next validation step and why unresolved. Surface potentially High/Critical issues prominently. |
| `hardening` | Useful defense in depth without an established exploit/security violation in scope; excluded from vulnerability totals. |
| `rejected` | Evidence disproves the candidate or its claimed security impact; retain evidence and explanation. |
| `duplicate` | Same root cause as another ledger ID; link the canonical record and preserve distinct paths/impacts there. |

**Confidence** is the reviewer's qualitative certainty in the disposition (`high`,
`medium`, `low`), with rationale. **Evidence strength** describes the basis:
`behavioral` (actual relevant path exercised), `source` (complete source/control trace),
or `indicative` (incomplete trace or tool signal). These are independent of impact
severity; behavioral evidence still has environmental limits. Negative evidence must
say which protections were sought and found or not found. If none was found, explain
the search/trace performed; an empty assertion is insufficient.

Consolidate root causes, not merely similar titles. Preserve distinct entry points,
actors and materially different impacts in the canonical record; keep separate findings
when controls or fixes differ materially. Explain disagreements with code, environment,
coverage or assumptions rather than voting. Do not tune decisions for finding count.

## Qualitative severity and remediation priority

Assess confidentiality (which data/who), integrity (which state/authority), availability
(which resources/how long), affected scope, practical impact and attacker prerequisites
together. Explain the rating and the nearest plausible alternative; uncertainty belongs
in confidence/assumptions and disposition, not a quietly reduced severity. For unresolved
candidates, severity is explicitly **potential**, conditional on named assumptions.

| Severity | Evidence-based consequence in the actual context |
| --- | --- |
| Critical | Practical path to catastrophic, broad compromise: system-wide privileged control, highly sensitive bulk disclosure/destruction, or sustained failure of a critical service. Explain scope and feasibility; remote execution alone does not establish full-system impact. |
| High | Practical substantial breach of confidentiality/integrity or major service disruption beyond a narrowly bounded effect. Establish sensitive assets, affected population, durable privilege or resource consequences and realistic preconditions. |
| Medium | Demonstrated meaningful but bounded breach or disruption, such as limited unauthorized state/data access, constrained entitlement abuse or recoverable resource interference. Explain the bounds and what would change the rating. |
| Low | Demonstrated small security impact with constrained reach/consequence. Mere preference or defense in depth is hardening, not automatically Low. |

Authentication never fixes a rating by itself: an authenticated actor can cause Critical
impact, while a public path may have little impact. Do not extrapolate a local slowdown
to a production outage without capacity/exposure evidence. Do not require proof of
actual attacker exploitation to assess a demonstrated feasible path.

An unmeasured production ceiling does not by itself make a demonstrated violation
unconfirmed. Rate the impact the evidence supports and state its bounds; keep
`needs_validation` when the missing fact decides whether the violation is reachable
or exists, rather than only whether its worst-case magnitude is larger.

Track **remediation priority** separately (`urgent`, `scheduled`, `backlog`,
`investigate`, `none`) with context: exposure, active exploitation if evidenced,
business criticality, compensating controls, dependencies and cost of delay. An
unresolved potentially serious issue can need urgent investigation without being a
confirmed High vulnerability.

Artifact v1 uses qualitative severity only. Do not output overall scores, compliance
percentages, invented decimal risk scores or numerical CVSS. If a future schema adds
CVSS, it must require an explicit version, complete vector, metric-by-metric rationale,
a score calculated by a verified implementation (tool/version/command/result recorded),
and a base versus environmental/threat label. Never hand-calculate a score.

## Baseline reconciliation and identity

Freeze fresh discovery before reading prior findings where practical. Record when prior
exposure was unavoidable. Select the latest relevant baseline for the same scope/revision
lineage, or all explicitly supplied reports; record the choice and excluded histories.
Do not automatically ingest every historical audit. Blind benchmarks use no baseline
and no expected answers; their later evaluation belongs to a separate evaluator.

Inventory **every** prior finding into a baseline manifest before matching. Preserve
source report path/hash, original identifier/title/location, and original severity.
For legacy Markdown without IDs, assign a namespaced key from report SHA-256 plus
finding ordinal; include heading and location as human anchors. Old `H-001`/`M-001`
IDs are report-local, not globally unique. Match by root cause, boundary and operation,
using symbol/file history to follow movement. Keep mappings and explain ambiguous
matches rather than forcing them. Once mapped, keep the canonical current ID through
severity changes. Record old/new severity and the evidence for any change.

Disposition each baseline entry as `still_present`, `fixed` (trace the effective fix),
`rejected` (counterevidence), `duplicate_merged` (canonical ID), `not_reassessed`, or
`unresolved`, or `out_of_scope` (artifact 1.1). Link current candidates where appropriate
and document evidence/rationale.
For a split, keep the primary `current_candidate_id` and list the other canonical
IDs in `related_current_candidate_ids`; explain scope/impact differences. For a
merge, map each prior entry to the surviving canonical ID using `duplicate_merged`.
Use `out_of_scope` only for findings outside the declared review boundaries, with an
exclusion rationale and no current candidate mapping; it never implies fixed. Findings
within scope that were not examined remain `not_reassessed`. Differences can reflect
code, dependencies, environment, severity rationale,
new evidence, incomplete review or error; make the actual reason explicit.

## Technical guidance and reporting limits

Replace miniature “secure” snippets with control-specific evidence and proposed fixes.
For SSRF, trace parsing/canonicalization, allowed destinations/schemes, all resolved
IPv4/IPv6 addresses (including mapped/private/reserved/loopback/link-local ranges),
redirect validation at every hop, and the actual connection destination. DNS checking
followed by a fresh unpinned resolution leaves a rebinding gap; ensure the client
connects only to the validated address while preserving correct TLS/SNI/Host handling.
Consider proxies and alternate transports. Use maintained implementation primitives
and test their integration. The [OWASP SSRF guidance](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)
is a review reference, not proof that a hostname allowlist alone protects a fetch.

Evaluate headers, GraphQL introspection, action pinning, encryption, password hashing
costs and token rotation against actual assets and threats. Their absence is not a
universal vulnerability. For example, a library may constrain JWT algorithms by key
type by default; inspect the version and verification options before alleging algorithm
confusion. Output escaping differs by context; template use or JSON parsing is not
intrinsically injection. Host-specific assistant settings do not secure the application.

Render from validated structured data. Derive totals from dispositions, visibly separate
hardening and unresolved candidates, show coverage gaps and baseline outcomes, and link
reproduction evidence. Include remediation examples only when useful; label untested
snippets **proposed, untested** and identify missing integration work. No fixed number of
findings, repetitive sections or remediation examples is required. Partial reports are
useful: disclose stopping conditions and what remains. Structural validation checks
consistency; it cannot establish the truth of a security conclusion or discover omitted
surfaces. Even a complete audit means its declared review obligations were completed,
not that the repository is vulnerability-free.
