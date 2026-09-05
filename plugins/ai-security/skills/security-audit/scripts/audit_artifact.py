#!/usr/bin/env python3
"""Validate and render security audit artifacts using Python's standard library."""
import argparse
from collections import Counter
import hashlib
import html
import os
import re
from urllib.parse import quote
import json
from pathlib import Path
import sys

SCHEMA_PATH = Path(__file__).resolve().parent.parent / 'references' / 'audit.schema.json'


def schema_errors(value, schema, path='$'):
    """Implement the exact JSON Schema subset used by the bundled schema.

    Unknown keywords fail closed, so evolving the schema cannot silently weaken checks.
    This is not a general-purpose JSON Schema implementation.
    """
    known = {'$schema', '$id', 'title', 'type', 'const', 'enum', 'minLength',
             'minItems', 'items', 'properties', 'required', 'additionalProperties'}
    errors = []
    if set(schema) - known:
        return [f'{path}: unsupported schema keywords {sorted(set(schema) - known)}']
    types = schema.get('type', [])
    types = [types] if isinstance(types, str) else types
    matches = {'object': isinstance(value, dict), 'array': isinstance(value, list),
               'string': isinstance(value, str), 'null': value is None,
               'boolean': isinstance(value, bool)}
    if types and not any(matches.get(t, False) for t in types):
        return [f'{path}: expected {types}']
    if 'const' in schema and value != schema['const']:
        errors.append(f'{path}: expected constant {schema["const"]!r}')
    if 'enum' in schema and value not in schema['enum']:
        errors.append(f'{path}: invalid value {value!r}')
    if isinstance(value, str) and len(value.strip()) < schema.get('minLength', 0):
        errors.append(f'{path}: empty text')
    if isinstance(value, list):
        if len(value) < schema.get('minItems', 0):
            errors.append(f'{path}: too few items')
        for i, item in enumerate(value):
            errors.extend(schema_errors(item, schema['items'], f'{path}[{i}]'))
    if isinstance(value, dict):
        props = schema['properties']
        for key in schema['required']:
            if key not in value:
                errors.append(f'{path}.{key}: required')
        for key, item in value.items():
            if key not in props:
                errors.append(f'{path}.{key}: unknown field')
            else:
                errors.extend(schema_errors(item, props[key], f'{path}.{key}'))
    return errors


def validate(data):
    errors = schema_errors(data, json.loads(SCHEMA_PATH.read_text()))
    if errors:
        return errors

    def require(condition, message):
        if not condition:
            errors.append(message)

    def index(items, label, key='id'):
        result = {}
        for item in items:
            require(item[key] not in result, f'{label}: duplicate {key} {item[key]}')
            result[item[key]] = item
        return result

    surfaces = index(data['surfaces'], 'surfaces')
    candidates = index(data['candidates'], 'candidates')
    validations = index(data['validations'], 'validations')
    reports = index(data['baseline']['reports'], 'baseline reports')
    index(data['coverage'], 'coverage')
    index(data['files'], 'files', 'path')
    for surface in surfaces.values():
        checks = surface['required_checks']
        require(len(checks) == len(set(checks)), f'{surface["id"]}: duplicate required check')
    pairs = set()
    for row in data['coverage']:
        pair = (row['surface_id'], row['check_id'])
        require(pair not in pairs, f'coverage: duplicate surface/check {pair}')
        pairs.add(pair)
        surface = surfaces.get(row['surface_id'])
        require(surface is not None, f'{row["id"]}: unknown surface')
        if surface:
            require(row['check_id'] in surface['required_checks'], f'{row["id"]}: undeclared check')
        na = row['status'] == 'not_applicable'
        require(na == (row['applicability'] == 'not_applicable'), f'{row["id"]}: inconsistent applicability')
        if row['status'] == 'reviewed':
            require(row['applicability'] == 'applicable' and not row['gaps'], f'{row["id"]}: reviewed requires applicable and no gaps')
        if row['status'] in ('partially_reviewed', 'not_reviewed'):
            require(bool(row['gaps']), f'{row["id"]}: unfinished coverage needs explicit gaps')
    expected = {(s['id'], c) for s in surfaces.values() for c in s['required_checks']}
    require(pairs == expected, f'coverage: missing or extra surface/check pairs {sorted(expected ^ pairs)}')
    for file in data['files']:
        require(file['discovered'], f'{file["path"]}: listed file must be discovered')
    root_causes = {}
    for c in candidates.values():
        cid = c['id']
        for sid in c['surface_ids']:
            require(sid in surfaces, f'{cid}: unknown surface {sid}')
        require(len(c['surface_ids']) == len(set(c['surface_ids'])), f'{cid}: duplicate surface reference')
        require(len(c['validation_ids']) == len(set(c['validation_ids'])), f'{cid}: duplicate validation reference')
        for vid in c['validation_ids']:
            require(vid in validations, f'{cid}: unknown validation {vid}')
            if vid in validations:
                require(cid in validations[vid]['candidate_ids'], f'{cid}: validation backlink missing')
        severity = c['severity']
        disposition = c['disposition']
        if disposition in ('confirmed', 'needs_validation'):
            require(severity['level'] != 'none', f'{cid}: vulnerability or potential impact needs severity')
            require(severity['assessment'] == ('confirmed' if disposition == 'confirmed' else 'potential'), f'{cid}: severity assessment conflicts with disposition')
        else:
            require(severity['level'] == 'none' and severity['assessment'] == 'not_applicable', f'{cid}: non-vulnerability must not carry vulnerability severity')
        if disposition != 'duplicate':
            require(c['duplicate_of'] is None, f'{cid}: duplicate_of only allowed for duplicates')
            require(c['root_cause_key'] not in root_causes, f'{cid}: root cause already represented; consolidate or mark duplicate')
            root_causes[c['root_cause_key']] = cid
        else:
            target = candidates.get(c['duplicate_of'])
            require(target is not None and target['id'] != cid and target['disposition'] != 'duplicate', f'{cid}: duplicate must reference another nonduplicate candidate')
            if target:
                require(target['root_cause_key'] == c['root_cause_key'], f'{cid}: duplicate root cause mismatch')
        require(bool(c['validation_ids']), f'{cid}: verification record required for every disposition (inconclusive permitted)')
        if disposition == 'needs_validation':
            require(bool(c['assumptions']), f'{cid}: unresolved candidate needs decisive gap in assumptions')
        if disposition == 'confirmed':
            require(c['evidence_strength'] != 'indicative', f'{cid}: indicative evidence cannot confirm vulnerability')
            require(any(validations.get(v, {}).get('result') == 'supports' for v in c['validation_ids']), f'{cid}: confirmed candidate needs supporting verification')
        if disposition == 'rejected':
            require(any(validations.get(v, {}).get('result') == 'refutes' for v in c['validation_ids']), f'{cid}: rejected candidate needs refuting verification')
    for v in validations.values():
        require(len(v['candidate_ids']) == len(set(v['candidate_ids'])), f'{v["id"]}: duplicate candidate reference')
        for cid in v['candidate_ids']:
            require(cid in candidates, f'{v["id"]}: unknown candidate {cid}')
            if cid in candidates:
                require(v['id'] in candidates[cid]['validation_ids'], f'{v["id"]}: candidate backlink missing')
    prior_pairs = set()
    for report in reports.values():
        prior = index(report['findings'], report['id'] + ' prior findings')
        prior_pairs.update((report['id'], fid) for fid in prior)
    reconciled = set()
    for r in data['reconciliation']:
        pair = (r['report_id'], r['prior_id'])
        if r['status'] == 'out_of_scope':
            require(data['schema_version'] == '1.1', f'{pair}: out_of_scope requires schema 1.1')
            require(bool(data['scope']['excluded']), f'{pair}: out_of_scope needs explicit scope exclusions')
            require(r['current_candidate_id'] is None and not r['related_current_candidate_ids'],
                    f'{pair}: out_of_scope must not also map to an in-scope candidate')
        require(pair in prior_pairs, f'reconciliation: unknown prior finding {pair}')
        require(pair not in reconciled, f'reconciliation: duplicate prior finding {pair}')
        reconciled.add(pair)
        current = candidates.get(r['current_candidate_id'])
        related = r['related_current_candidate_ids']
        require(len(related) == len(set(related)), f'{pair}: duplicate related candidate reference')
        require(r['current_candidate_id'] not in related, f'{pair}: primary candidate repeated in related references')
        require(not related or current is not None, f'{pair}: split mappings require a primary candidate')
        if related and current:
            require(current['disposition'] != 'duplicate', f'{pair}: split primary must be canonical')
        for cid in related:
            target = candidates.get(cid)
            require(target is not None, f'{pair}: unknown related candidate {cid}')
            if target:
                require(target['disposition'] != 'duplicate', f'{pair}: related reference must be canonical')
                if r['status'] == 'rejected':
                    require(target['disposition'] == 'rejected', f'{pair}: rejected baseline contradicts related candidate')
                if r['status'] == 'fixed':
                    require(target['disposition'] not in ('confirmed', 'needs_validation'), f'{pair}: fixed baseline contradicts related candidate')
        require(r['current_candidate_id'] is None or current is not None, f'{pair}: unknown current candidate')
        if r['status'] in ('still_present', 'duplicate_merged'):
            require(current is not None, f'{pair}: current candidate required')
        if r['status'] == 'duplicate_merged' and current:
            require(current['disposition'] != 'duplicate', f'{pair}: merged baseline must reference surviving canonical candidate')
        if r['status'] == 'still_present' and current:
            prior = next((f for f in reports.get(r['report_id'], {}).get('findings', []) if f['id'] == r['prior_id']), None)
            if prior and prior['stable_id'] is not None:
                require(current['id'] == prior['stable_id'], f'{pair}: still-present finding must preserve stable ID')
            require(current['disposition'] == 'confirmed', f'{pair}: still-present vulnerability requires confirmed disposition; use unresolved otherwise')
        if r['status'] == 'rejected' and current:
            require(current['disposition'] == 'rejected', f'{pair}: rejected baseline contradicts candidate')
        if r['status'] == 'fixed' and current:
            require(current['disposition'] not in ('confirmed', 'needs_validation', 'duplicate'), f'{pair}: fixed baseline contradicts candidate or references noncanonical duplicate')
    require(reconciled == prior_pairs, 'baseline: every prior finding needs explicit reconciliation, including not_reassessed')
    if data['baseline']['mode'] in ('none', 'blind'):
        require(not reports and not data['reconciliation'], 'none/blind baseline mode must not contain prior findings')
    else:
        require(bool(reports), 'reconcile baseline mode requires selected report manifest')
    if not surfaces:
        require(bool(data['scope']['discovery_gaps']), 'empty inventory requires explicit discovery gap')
    if data['status'] == 'complete':
        require(bool(surfaces), 'complete audit requires inventory')
        require(bool(data['scope']['discovery_methods']), 'complete audit requires discovery methods')
        require(not data['scope']['discovery_gaps'], 'complete audit has discovery gaps')
        require(not data['limitations'], 'complete audit has unfinished execution obligations')
        require(all(r['status'] in ('reviewed', 'not_applicable') and not r['gaps'] for r in data['coverage']), 'complete audit has unfinished coverage')
        if data['schema_version'] == '1.0':
            # Preserve the stricter meaning of complete in historical records.
            require(not data['unresolved_questions'], 'complete 1.0 audit has unresolved questions')
            require(all(c['disposition'] != 'needs_validation' for c in candidates.values()), 'complete 1.0 audit has unresolved candidates')
            require(all(r['status'] not in ('not_reassessed', 'unresolved') for r in data['reconciliation']), 'complete 1.0 audit has unfinished baseline')
        else:
            for c in candidates.values():
                if c['disposition'] == 'needs_validation':
                    require(bool(data['unresolved_questions']), f'{c["id"]}: complete review must disclose external follow-up questions')
                    require(any(validations.get(vid, {}).get('limitations') for vid in c['validation_ids']),
                            f'{c["id"]}: complete review needs a validation limitation explaining external follow-up')
            for r in data['reconciliation']:
                require(r['status'] != 'not_reassessed', 'complete review has an unperformed baseline reassessment')
                if r['status'] == 'unresolved':
                    current = candidates.get(r['current_candidate_id'])
                    require(current is not None and current['disposition'] == 'needs_validation',
                            'complete review: unresolved baseline must map to a reassessed, unconfirmed candidate')
    return errors


def initial():
    return {'schema_version': '1.1', 'run_id': 'pending', 'status': 'partial',
            'provenance': {**{k: 'unknown' for k in ('repository', 'revision', 'dirty_state', 'skill_version', 'plugin_version', 'plugin_hash', 'skill_hash', 'model', 'reasoning', 'host', 'runtime', 'budget', 'started_at', 'ended_at', 'methodology_hash')}, 'reviewers': [], 'tools': [], 'dependency_scan': {'time': 'unknown', 'source': 'not run', 'tool': 'not run', 'scope': 'not run', 'result': 'not run', 'lockfile_hash': 'unknown'}},
            'scope': {'included': ['Repository scope pending'], 'excluded': [], 'discovery_methods': [], 'discovery_gaps': ['Inventory has not started.']},
            'surfaces': [], 'coverage': [], 'files': [], 'candidates': [], 'validations': [],
            'baseline': {'mode': 'none', 'reports': []}, 'reconciliation': [], 'unresolved_questions': [], 'limitations': ['Audit has not started.']}


def completion_note(data):
    if data['schema_version'] == '1.1' and data['status'] == 'complete':
        follow_up = bool(data['unresolved_questions']) or any(c['disposition'] == 'needs_validation' for c in data['candidates'])
        return ('**Declared review complete; follow-up remains.** External questions and unconfirmed concerns remain visible below. '
                'Completion does not mean they were resolved or that production was verified.' if follow_up else
                'The declared review work is complete. This does not certify production security or rule out unknown vulnerabilities.')
    return ''


def render_full(data):
    """Render validated structured data; numbers are always derived from dispositions."""
    confirmed = [c for c in data['candidates'] if c['disposition'] == 'confirmed']
    hardening = [c for c in data['candidates'] if c['disposition'] == 'hardening']
    unresolved = [c for c in data['candidates'] if c['disposition'] == 'needs_validation']
    out = [f'# Security audit: {data["run_id"]}', '',
           f'Status: **{data["status"]}**. Confirmed vulnerabilities: **{len(confirmed)}**. Hardening recommendations: **{len(hardening)}**. Needs validation: **{len(unresolved)}**.', '',
           'Structural validation checks artifact consistency; it cannot establish the truth of security conclusions.', '']
    if completion_note(data):
        out.extend([completion_note(data), ''])

    def section(title):
        out.extend([f'## {title}', ''])

    def field(name, value):
        if isinstance(value, list):
            out.append(f'**{name}:**')
            out.append('')
            out.extend(f'- {item}' for item in value)
            if not value:
                out.append('- None recorded.')
        else:
            out.append(f'**{name}:** {value}')
        out.append('')

    section('Scope and provenance')
    for name, value in data['scope'].items():
        field(name.replace('_', ' ').capitalize(), value)
    out.extend(['```json', json.dumps(data['provenance'], indent=2), '```', ''])
    field('Execution limitations', data['limitations'])
    field('Unresolved questions', data['unresolved_questions'])
    if unresolved:
        section('Unresolved candidates — potential impact, not confirmed findings')
        for c in unresolved:
            field(f'{c["id"]}: {c["title"]}', f'Potential {c["severity"]["level"]}; {c["rationale"]} Assumptions: {"; ".join(c["assumptions"]) or "none recorded"}.')
    section('Coverage')
    counts = {k: sum(f[k] for f in data['files']) for k in ('discovered', 'pattern_screened', 'manually_traced', 'behaviorally_tested')}
    field('Files by activity (overlapping categories)', ', '.join(f'{k}: {v}' for k, v in counts.items()))
    for s in data['surfaces']:
        field(s['id'], f'{s["description"]} Locations: {"; ".join(s["locations"])}')
        for r in (r for r in data['coverage'] if r['surface_id'] == s['id']):
            field(f'{r["id"]} / {r["check_id"]}', f'{r["status"]} ({r["applicability"]}). {r["checked"]} {r["rationale"]}')
            field('Locations', r['locations'])
            field('Evidence', r['evidence'])
            field('Gaps', r['gaps'])
    section('Candidate ledger')
    for c in data['candidates']:
        out.extend([f'### {c["id"]}: {c["title"]}', ''])
        field('Decision', f'{c["disposition"]}; severity {c["severity"]["level"]} ({c["severity"]["assessment"]}); priority {c["priority"]}; confidence {c["confidence"]}; evidence strength {c["evidence_strength"]}. {c["rationale"]}')
        for key in ('root_cause_key', 'surface_ids', 'locations', 'attacker_access', 'prerequisites', 'trace', 'impact', 'protections', 'evidence', 'counterevidence', 'assumptions', 'validation_ids', 'confidence_rationale', 'priority_rationale', 'remediation'):
            field(key.replace('_', ' ').capitalize(), c[key])
        field('Severity rationale', '; '.join(f'{k}: {v}' for k, v in c['severity'].items() if k not in ('level', 'assessment')))
        if c['duplicate_of']:
            field('Duplicate of', c['duplicate_of'])
    section('Validation records')
    for v in data['validations']:
        field(v['id'], f'{v["method"]} — {v["result"]}; candidates: {", ".join(v["candidate_ids"])}')
        for key in ('commands', 'environment', 'expected', 'observed', 'limitations'):
            field(key.capitalize(), v[key])
    section('Previous findings')
    field('Baseline mode', data['baseline']['mode'])
    for report in data['baseline']['reports']:
        field(report['id'], f'{report["path"]}; hash: {report["hash"]}; prior IDs: {", ".join(f["id"] for f in report["findings"])}')
    candidates = {c['id']: c for c in data['candidates']}
    for r in data['reconciliation']:
        c = candidates.get(r['current_candidate_id'])
        change = f'; severity {r["previous_severity"]} → {c["severity"]["level"]}' if c else ''
        field(f'{r["report_id"]}/{r["prior_id"]}', f'{r["status"]}; current ID {r["current_candidate_id"] or "none"}{change}. {r["rationale"]}')
        for cid in r['related_current_candidate_ids']:
            related = candidates[cid]
            field('Related current candidate', f'{cid}: {related["title"]}; {related["disposition"]}; severity {related["severity"]["level"]} ({related["severity"]["assessment"]})')
        field('Evidence', r['evidence'])
    return '\n'.join(out).rstrip() + '\n'


def preview(value, limit=220):
    """One-line, escaped excerpt; full text remains in the linked JSON record."""
    text = ' '.join(str(value).split())
    if len(text) > limit:
        text = text[:limit].rsplit(' ', 1)[0] + '…'
    return re.sub(r'([\\`*_\[\]|])', r'\\\1', html.escape(text, quote=False))


def render(data, artifact_link=None, detail='summary'):
    """Human report by default; preserve exhaustive records in JSON or opt-in full mode."""
    if detail == 'full':
        return render_full(data)
    severity_order = {s: i for i, s in enumerate(('critical', 'high', 'medium', 'low', 'none'))}
    priority_order = {s: i for i, s in enumerate(('urgent', 'investigate', 'scheduled', 'backlog', 'none'))}
    candidates = {c['id']: c for c in data['candidates']}
    positions = {c['id']: i for i, c in enumerate(data['candidates'])}
    anchors = {cid: 'candidate-' + hashlib.sha256(cid.encode()).hexdigest()[:16] for cid in candidates}
    groups = {d: sorted((c for c in candidates.values() if c['disposition'] == d),
                       key=lambda c: (severity_order[c['severity']['level']], priority_order[c['priority']], c['id']))
              for d in ('confirmed', 'needs_validation', 'hardening', 'rejected', 'duplicate')}
    confirmed, unresolved, hardening = (groups[d] for d in ('confirmed', 'needs_validation', 'hardening'))
    counts = Counter(c['severity']['level'] for c in confirmed)
    coverage_counts = Counter(r['status'] for r in data['coverage'])
    json_link = f'[companion JSON]({artifact_link})' if artifact_link else 'the companion JSON'
    out = ['# Security audit', '', '## Summary', '',
           f'**{data["status"].capitalize()} review · {len(confirmed)} confirmed problems · '
           f'{len(unresolved)} need investigation · {len(hardening)} optional improvements.**', '',
           'Confirmed severity: ' + ', '.join(f'{counts[s]} {s.title()}' for s in ('critical', 'high', 'medium', 'low')) + '.', '',
           f'Reviewed {coverage_counts["reviewed"]} of {len(data["coverage"])} recorded checks; '
           f'{coverage_counts["partially_reviewed"]} partly reviewed, {coverage_counts["not_reviewed"]} not reviewed, '
           f'{coverage_counts["not_applicable"]} not applicable. These are review activities, not a security score.', '']
    if data['status'] != 'complete':
        out += ['**Work remains.** See [coverage and limits](#coverage-and-limits) for blockers and next steps. '
                'An unfinished review cannot rule out further problems.', '']
    else:
        if completion_note(data):
            out += [completion_note(data), '']
    if data['status'] == 'complete' and not confirmed:
        out += ['No confirmed problems were recorded in the declared scope; this does not prove the application is secure.', '']
    serious = [c for c in unresolved if c['severity']['level'] in ('critical', 'high')]
    if serious:
        out += [f'**{len(serious)} unresolved concern(s) have potential High/Critical impact.** '
                'They are not confirmed vulnerabilities; see [needs investigation](#needs-investigation).', '']
    actions = sorted(confirmed + unresolved, key=lambda c: (priority_order[c['priority']], severity_order[c['severity']['level']], c['id']))[:3]
    if actions:
        out += ['**Start here** (highest recorded priorities; all items follow):', '']
        for c in actions:
            action = 'Investigate' if c['disposition'] == 'needs_validation' else 'Address'
            out.append(f'- {action} [{preview(c["id"])}](#{anchors[c["id"]]}): {preview(c["title"], 120)}')
        out.append('')
    out += ['**Contents:** [Findings](#findings) · [Needs investigation](#needs-investigation) · '
            '[Optional improvements](#optional-improvements) · [Coverage and limits](#coverage-and-limits) · '
            '[Previous findings](#previous-findings) · [Audit details](#audit-details)', '',
            f'This is the reading copy. Excerpts end with …; full evidence, commands, and records are in {json_link}. '
            'Suggested fixes remain proposals unless their test status says otherwise.', '']

    def section(title):
        out.extend([f'## {title}', ''])

    def field(title, value, limit=260):
        if value:
            out.extend([f'**{title}:** {preview(value, limit)}', ''])

    def table(headers, rows):
        out.append('| ' + ' | '.join(headers) + ' |')
        out.append('| ' + ' | '.join('---' for _ in headers) + ' |')
        out.extend('| ' + ' | '.join(row) + ' |' for row in rows)
        out.append('')

    def record_ref(c):
        return f'`candidates[{positions[c["id"]]}]` in {json_link}'

    def candidate_details(c, potential=False):
        out.extend([f'<a id="{anchors[c["id"]]}"></a>', '',
                    f'### {preview(c["id"])} — {preview(c["title"], 110)}', ''])
        field('Assessment', f'{"Potential " if potential else ""}{c["severity"]["level"].title()}; '
              f'priority: {c["priority"]}; confidence in decision: {c["confidence"]}')
        field('Impact', c['impact'], 180)
        field('Where', '; '.join(c['locations'][:2]), 160)
        field('Access needed', c['attacker_access'] + '; ' + '; '.join(c['prerequisites']), 140)
        field('Evidence', '; '.join(c['evidence']), 160)
        field('Controls checked', '; '.join(c['counterevidence']), 140)
        if potential:
            field('What is still unknown', '; '.join(c['assumptions']), 180)
        field('Next step / fix status', c['remediation'], 180)
        out.extend([f'Details: {record_ref(c)}.', ''])

    section('Findings')
    if confirmed:
        table(['ID', 'Severity', 'Priority', 'Problem'],
              [[f'[{preview(c["id"])}](#{anchors[c["id"]]})', c['severity']['level'].title(),
                c['priority'], preview(c['title'], 110)] for c in confirmed])
        for c in confirmed:
            candidate_details(c)
    else:
        out += ['No confirmed vulnerabilities recorded.', '']
    section('Needs investigation')
    out += ['These concerns are unconfirmed. Severity describes the potential impact if the missing facts support the concern.', '']
    if unresolved:
        for c in unresolved:
            candidate_details(c, potential=True)
    else:
        out += ['None recorded.', '']
    section('Optional improvements')
    out += ['These are additional precautions (hardening), not confirmed vulnerabilities.', '']
    if hardening:
        table(['ID / JSON record', 'Priority', 'Suggestion (full action in JSON)'],
              [[preview(c['id']) + f' · `candidates[{positions[c["id"]]}]`', c['priority'],
                preview(c['title'], 100)] for c in hardening])
    else:
        out += ['None recorded.', '']
    section('Coverage and limits')
    field('Included', '; '.join(data['scope']['included']), 420)
    field('Excluded', '; '.join(data['scope']['excluded']), 420)
    activities = [('discovered', 'discovered'), ('pattern_screened', 'pattern-screened'),
                  ('manually_traced', 'manually traced'), ('behaviorally_tested', 'behaviorally tested')]
    out += ['Files: ' + '; '.join(f'{sum(f[k] for f in data["files"])} {label}' for k, label in activities) +
            '. These groups overlap; finding a file is different from tracing or testing it.', '']
    for label, items in [('Discovery gaps', data['scope']['discovery_gaps']),
                         ('Execution blockers / limits', data['limitations']),
                         ('Open questions', data['unresolved_questions'])]:
        if items:
            out += [f'**{label}:**', '']
            out.extend('- ' + preview(item, 180) for item in items)
            out.append('')
    check_groups = {}
    for row in data['coverage']:
        check_groups.setdefault(row['check_id'], []).append(row)
    if check_groups:
        rows = []
        for check_id, checks in sorted(check_groups.items()):
            states = Counter(r['status'] for r in checks)
            unfinished = [r for r in checks if r['gaps']]
            example = (preview(unfinished[0]['gaps'][0], 120) + ' · ' + preview(unfinished[0]['id'])) if unfinished else 'No recorded gap'
            rows.append([preview(check_id), str(states['reviewed']), str(states['partially_reviewed'] + states['not_reviewed']),
                         str(states['not_applicable']), example])
        out += [f'Coverage grouped by check type below; **every individual check and gap** remains in the `coverage` array in {json_link}. '
                'Gap examples are excerpts, not the full list. Grouping does not merge review obligations.', '']
        table(['Check type', 'Reviewed', 'Unfinished', 'Not applicable', 'Example gap / coverage ID'], rows)
    section('Previous findings')
    if not data['baseline']['reports']:
        out += [f'No previous findings compared (baseline mode: {data["baseline"]["mode"]}). Absence does not mean fixed.', '']
    else:
        results = Counter(r['status'] for r in data['reconciliation'])
        out += [', '.join(f'{n} {s.replace("_", " ")}' for s, n in sorted(results.items())) + '. Absence never implies fixed.', '']
        for report in data['baseline']['reports']:
            field('Baseline ' + preview(report['id']), report['path'])
        rows = []
        for i, r in enumerate(data['reconciliation']):
            current_ids = ([r['current_candidate_id']] if r['current_candidate_id'] else []) + r['related_current_candidate_ids']
            mapped = []
            for cid in current_ids:
                c = candidates[cid]
                label = f'{preview(cid)} ({"potential " if c["disposition"] == "needs_validation" else ""}{c["severity"]["level"]})'
                mapped.append(f'[{label}](#{anchors[cid]})' if c['disposition'] in ('confirmed', 'needs_validation') else label)
            rows.append([preview(r['report_id'] + '/' + r['prior_id']), r['status'].replace('_', ' '),
                         r['previous_severity'] + ' → ' + ('; '.join(mapped) or 'no current finding'),
                         preview(r['rationale'], 90) + f' (`reconciliation[{i}]`)'])
        table(['Prior ID', 'Outcome', 'Previous severity → current', 'Why / JSON record'], rows)
    section('Audit details')
    for label, key in [('Repository', 'repository'), ('Revision', 'revision'), ('Finished', 'ended_at'),
                       ('Model / host identity as recorded', 'model')]:
        field(label, data['provenance'][key])
    field('Host', data['provenance']['host'])
    scan = data['provenance']['dependency_scan']
    field('Dependency scan', f'{scan["result"]} · source: {scan["source"]} · time: {scan["time"]}', 320)
    out += [f'{len(groups["rejected"])} rejected candidates and {len(groups["duplicate"])} duplicates remain in {json_link}, '
            'with their reasons and evidence. They do not count as confirmed problems.', '',
            'Confidence describes certainty in a decision; severity describes impact. '
            'The JSON also retains full provenance, file activity, review coverage, commands, and previous-finding evidence.', '',
            'Structural validation checks consistency, not the truth of security conclusions. '
            'This audit is not a certification or a guarantee that the application is secure.', '']
    return '\n'.join(out).rstrip() + '\n'


def load_json(path):
    def unique_keys(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'duplicate JSON key: {key}')
            result[key] = value
        return result
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=unique_keys,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f'invalid JSON constant: {value}')))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    for name in ('init', 'validate', 'render'):
        sub = commands.add_parser(name)
        sub.add_argument('artifact', type=Path)
        if name == 'render':
            sub.add_argument('--output', type=Path, required=True)
            sub.add_argument('--detail', choices=('summary', 'full'), default='summary',
                             help='summary: human reading copy (default); full: exhaustive technical export')
    args = parser.parse_args(argv)
    try:
        if args.command == 'init':
            with args.artifact.open('x', encoding='utf-8') as handle:
                json.dump(initial(), handle, indent=2)
                handle.write('\n')
            print(f'Created partial artifact: {args.artifact}')
            return 0
        data = load_json(args.artifact)
        errors = validate(data)
        if errors:
            for error in errors:
                print(error, file=sys.stderr)
            return 1
        if args.command == 'render':
            if args.output.resolve() == args.artifact.resolve():
                raise ValueError('report output must differ from input artifact')
            try:
                relative = os.path.relpath(args.artifact.resolve(), args.output.resolve().parent)
                artifact_link = quote(Path(relative).as_posix(), safe='/')
            except ValueError:  # Windows paths on different drives cannot be relative.
                artifact_link = args.artifact.resolve().as_uri()
            args.output.write_text(render(data, artifact_link, args.detail), encoding='utf-8')
        print(f'Valid artifact ({data["status"]}); structural checks do not verify security conclusions.')
        return 0
    except (OSError, ValueError) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
