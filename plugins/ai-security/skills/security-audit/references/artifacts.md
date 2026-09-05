# Audit artifacts, schema 1.1

The coordinator writes two files in the **audited repository**, using the same run timestamp:

- `docs/security/YYYY-MM-DD-HHMMSS-security-audit.json`: authoritative structured record.
- `docs/security/YYYY-MM-DD-HHMMSS-security-audit.md`: readable rendering.

These paths are repository-relative, not filesystem `/docs/security`. Use a suffix if simultaneous runs collide. Do not overwrite historical reports. Record timestamps with timezone in provenance. Redact credentials and personal data from both files; retain evidence locations and reproducible safe commands.

The [JSON Schema](audit.schema.json) defines exact fields and allowed values. New runs use 1.1; existing 1.0 artifacts remain readable and keep their original, stricter completion rules. Do not upgrade a historical artifact or change its status without reassessing the work. All object fields are required and extra fields are rejected. Empty lists mean **none recorded**, never proof of absence. Use `unknown`, `not exposed`, `not run`, or `not applicable: <reason>` for unobservable textual provenance. Never infer hidden model routing. `init` produces a valid unfinished starting record, not a completed audit or a sample finding.

## CLI

Resolve `SKILL_DIR` to this skill's actual location. No dependencies beyond Python 3.9+ are needed:

```sh
python3 "$SKILL_DIR/scripts/audit_artifact.py" init docs/security/2026-09-05-120000-security-audit.json
python3 "$SKILL_DIR/scripts/audit_artifact.py" validate docs/security/2026-09-05-120000-security-audit.json
python3 "$SKILL_DIR/scripts/audit_artifact.py" render docs/security/2026-09-05-120000-security-audit.json --output docs/security/2026-09-05-120000-security-audit.md
```

Create the destination directory first. `init` refuses to overwrite files; `render` replaces its explicit Markdown output and refuses the input artifact as output. The default render is a concise reading copy linked to its JSON; `--detail full` is an optional exhaustive technical export, not the default audit report. Validation/render return exit code 1 on invalid JSON, schema errors, invariant failures, or I/O errors, and 0 on success. A partial or blocked artifact is a successful validation if its uncertainty is disclosed.

If Python is unavailable, produce the same JSON/Markdown contract manually, record that structural checks were not executed as an execution limitation, and label the audit partial. Do not claim automated validation passed.

## Human-readable report

Write for a developer deciding what to fix. Use a short phrase for each title and one
or two concise sentences for impact and next steps; briefly define necessary security
terms. Lead with the consequence and the qualification that changes the decision, not
technical background. Put detailed
technical traces, reproduction commands, controls, and provenance in the JSON fields
that own them. Avoid copying the same paragraph into multiple fields or inventing
candidates for every passed check: coverage records already document those checks.

The default Markdown is a reading copy, not a dump of the JSON:

- Start with status, confirmed severity totals, unresolved concerns, coverage counts,
  and the first few recorded priorities; then a linked table of contents.
- Put confirmed findings first, with a linked index and a short explanation of impact,
  location/access, evidence, counterevidence, severity, and next steps. Include every
  confirmed finding and every unresolved candidate; potentially serious uncertainty
  must stay visible. Priority and severity remain separate.
- Use compact tables for optional improvements and every previous-finding outcome,
  including changed severity and why an item disappeared. Keep rejected/duplicate
  evidence in JSON rather than expanding it into more finding sections.
- Summarize file activity and coverage status. Disclose blockers and open questions;
  group coverage by check type, showing unfinished counts and example gaps with IDs.
  Link the full gap list in JSON. Grouping does not merge review obligations or imply
  the displayed examples are the only gaps. Summarize material blockers in top-level
  `limitations` so the reading copy explains what remains without thousands of rows.
- Link the companion JSON for full evidence and commands. The renderer bounds prose
  excerpts and marks shortened text with `…`; these are previews, not rewritten
  conclusions. Record locators such as `candidates[4]` refer to that run's JSON;
  candidate IDs remain the stable identities across runs.

Do not append reviewer reports, the full surface inventory, raw logs, schema fields,
or an exhaustive appendix to the reading copy. Do not remove findings to meet a page
count. If an excerpt obscures an important qualification, tighten its source field
while retaining the complete trace in the appropriate JSON records, then render again.
The same presentation rules apply to manual rendering. Full technical Markdown is
available only when explicitly requested via `render --detail full`.

## Field contract

| Record | Required contents |
| --- | --- |
| Top level | `schema_version: "1.1"` (legacy `1.0` accepted), stable `run_id`, `status: complete\|partial\|blocked`, `provenance`, `scope`, `surfaces`, `coverage`, `files`, `candidates`, `validations`, `baseline`, `reconciliation`, `unresolved_questions`, `limitations` |
| `provenance` | `repository`, `revision`, `dirty_state`, `skill_version`, `plugin_version`, `plugin_hash`, `skill_hash`, `methodology_hash`, `model`, `reasoning`, `host`, `reviewers[]`, `runtime`, `tools[]`, `dependency_scan`, `budget`, `started_at`, `ended_at` |
| `dependency_scan` | `time`, `source` (advisory database), `tool` including version, `scope`, `result`, `lockfile_hash`; distinguish an unavailable or failed scan from a clean result |
| `scope` | `included[]`, `excluded[]`, `discovery_methods[]`, `discovery_gaps[]`; methods name framework registry inspection, build/generator checks, and discovery limitations where applicable |
| `surfaces[]` | Stable `id`, `description`, `locations[]`, `required_checks[]`; check identifiers reference pinned ASVS requirements or stable application-specific checks from the methodology |
| `coverage[]` | Unique `id`, `surface_id`, `check_id`, `applicability: applicable\|not_applicable\|unknown`, `status: reviewed\|partially_reviewed\|not_reviewed\|not_applicable`, `locations[]`, `checked`, `evidence[]`, `gaps[]`, `rationale` |
| `files[]` | Unique repository-relative `path`; independent Boolean `discovered`, `pattern_screened`, `manually_traced`, `behaviorally_tested`; categories overlap and screening is not tracing |
| `candidates[]` | Stable `id`, `root_cause_key`, `title`, `surface_ids[]`, `locations[]`, `attacker_access`, `prerequisites[]`, `trace[]`, `impact`, `protections[]`, `evidence[]`, `counterevidence[]`, `assumptions[]`, `validation_ids[]`, `disposition`, `rationale`, `confidence`, `confidence_rationale`, `evidence_strength`, `severity`, `priority`, `priority_rationale`, `duplicate_of`, `remediation` |
| `validations[]` | Unique `id`, `candidate_ids[]`, `method`, `commands[]`, `environment[]`, `expected`, `observed`, `result: supports\|refutes\|inconclusive`, `limitations[]` |
| `baseline` | `mode: none\|reconcile\|blind`, `reports[]` |
| `baseline.reports[]` | Unique `id`, repository-relative or explicitly supplied `path`, content `hash`, `findings[]` |
| `baseline.reports[].findings[]` | Prior report's `id`, canonical `stable_id` or null for legacy reports, original `title`, original `locations[]` |
| `reconciliation[]` | `report_id`, `prior_id`, nullable `current_candidate_id`, `related_current_candidate_ids[]`, `previous_severity: critical\|high\|medium\|low\|none\|unknown`, `status`, `evidence[]`, `rationale` |

Locations are explicit `relative/path:line` or line ranges when available; identify generated or external code as such. Evidence strings name the control or observation and its location. Do not put tokens, keys, full customer records, or dangerous executable payloads into artifacts.

`dirty_state` records relevant tracked changes and relevant untracked files, plus a sanitized diff/content fingerprint when available. A commit hash alone cannot reproduce a dirty audit target. `plugin_hash` is SHA-256 of the plugin manifest bytes; `skill_hash` is SHA-256 of the invoked SKILL.md bytes. The methodology bundle hash covers the implementation files actually used. For `methodology_hash`, sort the relative POSIX paths of the skill, agent, applicable reference files, schema, and scripts actually used; hash each path as UTF-8 followed by NUL and that file's bytes followed by NUL into one SHA-256 digest. Record the included path list alongside the digest in this text field; unrelated evaluation answer keys must not be loaded in blind runs. Include exposed reviewer/model identity in each `reviewers[]` entry. Record runtime/tool versions actually queried, budget, safety limits, and stopping conditions; do not fabricate them.

`skill_version` uses this skill’s plugin release version (there is no independent skill release counter). Read `../../.claude-plugin/plugin.json` relative to the skill directory; do not label an uninspected manifest missing. If that file is unavailable, record the actual failed lookup or access limitation.

## Decisions and uncertainty

Candidate dispositions are `confirmed`, `needs_validation`, `hardening`, `rejected`, and `duplicate`. Confirmed findings and hardening recommendations are **views of the candidate ledger**, not additional editable arrays. Their IDs are candidate IDs, and every count in Markdown is derived from these dispositions. This avoids contradictory copies and prevents hardening or unresolved candidates inflating vulnerability totals. The required candidate `remediation` field describes a proposed action and its test status (or why no action is applicable); label proposals accurately and describe whether they were tested. Do not label untested remediation verified.

Every disposition has at least one verification record; inconclusive source inspection is acceptable when runtime access is unavailable. `commands[]` can be empty for manual source reasoning, but `method`, `environment`, `expected`, `observed`, and limitations still document exactly what was verified. Candidate and validation references are reciprocal. A supporting result is required for confirmation and a refuting result for rejection. A scanner hit alone is not confirmation.

`confidence` (`high`, `medium`, `low`) expresses how certain the decision is, with `confidence_rationale` explaining remaining uncertainty. `evidence_strength` names the strongest **relevant evidence basis**, independent of severity and confidence:

- `behavioral`: bounded observation exercises the disputed real path and control; limitations still matter.
- `source`: a traced, reachable input/transition-to-operation path with controls and versions examined; can establish a vulnerability without runtime reproduction.
- `indicative`: a search/scanner signal or incomplete path; cannot by itself establish a confirmed vulnerability.

Behavioral evidence is not inherently correct or stronger than a rigorous source proof: a mock that removes the disputed control does not qualify as behavioral evidence of that control. Counterevidence is required even if the entry says “No refuting control found after tracing X and Y.” Empty counterevidence or boilerplate “none” without investigation is not a substantive verification pass.

`severity` always contains `level`, `assessment`, `confidentiality`, `integrity`, `availability`, `prerequisites`, `scope`, `practical_impact`, and `rationale` explaining the selected level and nearest plausible alternative. Confirmed candidates use assessment `confirmed`; unresolved candidates use `potential`. Both require a qualitative level `critical|high|medium|low`. Hardening/rejected/duplicate entries use `level: none` and `assessment: not_applicable` (the canonical duplicate target carries impact). Keep unresolved High/Critical potential impacts visible. Unresolved candidates require nonempty `assumptions[]` identifying the decisive verification gap. `priority` is separately `urgent|scheduled|backlog|investigate|none`, with a context-based rationale.

Both supported schema versions use **qualitative severity only**. Numerical CVSS scores, vectors, overall scores, compliance percentages, and supplied finding counts are unknown fields and rejected. A future numeric extension would require versioned CVSS vectors, metric rationales, verified calculation, and base/environmental/threat identification; do not add ad hoc fields now.

A unique `root_cause_key` identifies each canonical candidate independently of severity. Consolidate shared root causes into one canonical candidate with all affected entry points and distinct impacts. Duplicate records must reference a nonduplicate candidate with the same root cause. Identity must not encode a severity rank or a finding's current list position.

## Previous findings and legacy reports

Fresh discovery precedes baseline reading. `reconcile` selects the latest relevant baseline or explicitly supplied reports; enumerate **every finding** in each selected report's manifest, including later rejected, merged, or unreviewed entries. `none` records no selected baseline; `blind` forbids loading expected answers or historical findings. Both modes require empty report and reconciliation arrays.

For legacy Markdown, assign a surrogate prior ID such as `legacy:<report-hash-prefix>:<original-label>`; preserve the report hash, original title and location. Set `stable_id` to null until a canonical current candidate identity is assigned. Match by root cause, trace, and affected surface rather than title or severity. Record the mapping and reasoning in reconciliation; future reports use the canonical candidate ID. Do not pretend old ordinal IDs were stable.

Each prior ID needs exactly one reconciliation: `still_present`, `fixed`, `rejected`, `duplicate_merged`, `not_reassessed`, `unresolved`, or (1.1 only) `out_of_scope`. `still_present` requires a confirmed current candidate and preserves known canonical stable IDs. Use `unresolved` if a prior claim remains uncertain. `duplicate_merged` points to the surviving candidate. A changed severity retains identity and explains the new evidence or rubric correction in `rationale`; the renderer shows previous and current severity. For a split, `current_candidate_id` is the primary canonical candidate (preserving a known stable ID when still present), and `related_current_candidate_ids[]` contains the other canonical candidates with distinct root causes. Explain why the old entry combined them; the renderer shows every related candidate and its severity. Related IDs must be unique, exist, and exclude the primary and duplicate records. For a merge, multiple prior reconciliation rows point to the same surviving canonical candidate using `duplicate_merged` where appropriate. Fixed/rejected entries require evidence; disappearance alone proves neither. A fixed entry cannot point directly to a duplicate or to a confirmed/unresolved primary or related candidate. An incomplete reassessment is still explicitly recorded, not omitted.

## Invariants and limitations

Report status describes the evidence, not permission to stop. Apply the
[coordinator's stopping rule](../SKILL.md#continue-until-the-work-is-done-or-genuinely-blocked)
before final handoff. For each unfinished obligation, use the existing coverage `gaps`,
candidate validation `limitations`, or reconciliation `rationale` to record attempted
work, its blocker or reached limit, and the next action needed; summarize the stopping
reason in top-level `limitations`. A valid partial artifact may be an interim checkpoint.

The validator checks strict schema, unique IDs, cross-references, reciprocal validation links, a coverage row for every declared surface/check, explicit coverage gaps, duplicate root-cause handling, qualitative severity/disposition consistency, verification records, and complete accounting of selected prior findings. The renderer derives counts and highlights unresolved candidates, severity changes, counterevidence, and coverage gaps, linking the JSON for complete verification details.

## Completion and follow-up

In 1.1, status describes **completion of the declared review**, not whether every
security concern has been settled:

- `complete`: all in-scope discovery, source/control tracing, required validation, and
  selected baseline comparisons are finished. No discovery gaps, unfinished coverage,
  or top-level execution limitations remain. External questions and `needs_validation`
  candidates may remain after the repository-side work is finished; the report must
  say **review complete; follow-up remains** and retain potential severity and next steps.
- `partial`: in-scope work remains, such as unread handlers, incomplete ownership or
  middleware traces, unperformed requested tests, or a baseline entry not reassessed.
  Continue feasible work under the stopping rule. Missing access to an explicitly
  requested deployment review is also unfinished work, not an automatic exclusion.
- `blocked`: unfinished review cannot meaningfully advance with current access/tools.

For a completed review, every unresolved candidate needs its decisive assumptions,
next action in `remediation`, an explanation of the external limit in its validation
record, and disclosure in `unresolved_questions`. An `unresolved` baseline outcome
must map to such a reassessed candidate; a bare unexamined previous claim is still
`not_reassessed` and prevents completion. `out_of_scope` preserves a prior finding
outside the declared scope without implying fixed: cite the excluded boundary in
its evidence/rationale and use no current candidate links. The validator requires an
explicit scope exclusion. Do not shrink the scope after discovery to gain completion.

Place information according to what it means:

| Information | Where it belongs | Prevents completion? |
| --- | --- | --- |
| Untraced in-scope route, unresolved inventory, required test not run | Coverage/discovery gaps; top-level `limitations` for unfinished execution | Yes |
| Flaw or hardening suggestion found in a finished check | Candidate ledger; check remains reviewed | No |
| Optional runtime reproduction unavailable after complete source tracing | That validation record's `limitations`; retain evidence strength as source | No |
| Deployment/provider fact beyond the agreed repository review | Candidate assumptions, validation limitations, `unresolved_questions`, next action | No, but clearly flag follow-up |
| Recovered baseline, resolved disagreement, routine environment bounds | Baseline provenance, candidate rationale, provenance or validation record as appropriate | No |
| Missing evidence for a required local control trace | Coverage gap, even if the candidate also needs validation | Yes |

Version 1.0 keeps its prior rule: unresolved candidates/questions or unresolved baseline
outcomes also prevent `complete`. Do not relabel old runs automatically. Structural
checks cannot decide whether an external limit is genuine or a source trace is adequate;
review those judgments against scope and evidence. Even a completed review is not a
claim that the application has no unknown vulnerabilities.

Structural validation **cannot establish the truth of security conclusions**, detect omitted surfaces absent from the inventory, assess the adequacy of evidence prose, verify that a declared test actually ran, or discover dishonest completeness claims. Review the artifact semantically against the methodology and source code. The bundled validator implements only the exact documented JSON Schema subset (`type`, `const`, `enum`, `minLength`, `minItems`, `items`, `properties`, `required`, `additionalProperties`) and rejects unsupported keywords. The schema can also be consumed by a standards-compliant JSON Schema validator; semantic invariants still require the bundled CLI.
