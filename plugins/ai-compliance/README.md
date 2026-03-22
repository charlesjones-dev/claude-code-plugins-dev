# AI Compliance Plugin

AI-powered software compliance auditing for open-source license detection, risk assessment, and attribution file generation.

## Overview

Open-source license compliance is a legal obligation that many projects overlook. Using a GPL-licensed dependency in a proprietary project could require disclosing your source code. A dependency with no license at all is legally "all rights reserved" and can't be used without explicit permission. This plugin scans your dependency tree, identifies every license, flags incompatibilities with your project's license, and generates the attribution files required by licenses like MIT, BSD, and Apache 2.0.

## Skills

### `/compliance-license-audit` - License Compliance Audit

Interactive, comprehensive audit of all open-source licenses in your dependency tree.

**Features:**
- Auto-detects your project's license with confirmation
- Scans all dependency manifests (package.json, requirements.txt, .csproj, go.mod, Cargo.toml, etc.)
- Identifies direct and transitive dependency licenses
- Scans source code for license headers and vendored/copied code
- Classifies licenses: Permissive, Weak Copyleft, Strong Copyleft, Unknown
- Flags incompatibilities with your project's license
- Identifies dependencies with no license (highest legal risk)
- Produces a License Compliance Score (0-100)
- Lists all unfulfilled license obligations (missing NOTICE files, attribution, etc.)
- Provides specific alternatives for problematic dependencies

**Usage:**
```bash
/compliance-license-audit
```

The skill will interactively ask about:
1. Your project's license (auto-detected with confirmation)
2. Audit scope (full, dependencies only, or source code only)
3. Risk tolerance (strict, moderate, permissive only, or informational)
4. Whether to include transitive dependencies

**Report output:** `/docs/compliance/YYYY-MM-DD-HHMMSS-license-audit.md`

### `/compliance-notice-generate` - Generate NOTICE / Attribution File

Generates legally compliant NOTICE, ATTRIBUTION, or THIRD-PARTY-NOTICES files from your dependency tree.

**Features:**
- Four output formats: NOTICE, THIRD-PARTY-NOTICES.md, ATTRIBUTION.md, licenses.json
- Configurable scope (production only, all, or custom dependency groups)
- Optional full license text inclusion
- Extracts actual copyright notices from LICENSE files
- Handles dual-licensed packages
- Supports all major package ecosystems
- Detects and handles existing attribution files

**Usage:**
```bash
/compliance-notice-generate
```

The skill will interactively ask about:
1. Output format (NOTICE, THIRD-PARTY-NOTICES.md, ATTRIBUTION.md, or licenses.json)
2. Content scope (production only, all, or custom)
3. Whether to include full license texts
4. How to handle existing attribution files (if any)

**Output:** Generated file saved to project root directory.

## License Classifications

| Classification | Examples | Risk Level |
|---------------|----------|------------|
| Permissive | MIT, Apache-2.0, BSD-2, BSD-3, ISC, Unlicense | Low |
| Weak Copyleft | LGPL-2.1, LGPL-3.0, MPL-2.0, EPL-2.0 | Moderate |
| Strong Copyleft | GPL-2.0, GPL-3.0, AGPL-3.0, SSPL-1.0 | High-Critical |
| No License | All rights reserved by default | Critical |

## Supported Package Ecosystems

| Ecosystem | Manifest | Lock File |
|-----------|----------|-----------|
| Node.js | package.json | package-lock.json, yarn.lock, pnpm-lock.yaml |
| Python | requirements.txt, pyproject.toml, Pipfile | Pipfile.lock, poetry.lock |
| .NET | *.csproj, packages.config | packages.lock.json |
| Go | go.mod | go.sum |
| Rust | Cargo.toml | Cargo.lock |
| Ruby | Gemfile | Gemfile.lock |
| PHP | composer.json | composer.lock |
| Java/Kotlin | pom.xml, build.gradle | - |

## Why This Matters

- **MIT License** requires: "The above copyright notice and this permission notice shall be included in all copies"
- **Apache 2.0** requires: Reproducing the NOTICE file in any distribution
- **BSD 3-Clause** requires: "Redistributions in binary form must reproduce the above copyright notice"
- **No license** means: "All rights reserved" - you legally cannot use the code
- **GPL in proprietary code** means: You may be obligated to release your source code

A single overlooked AGPL dependency in a SaaS application could theoretically require you to open-source your entire application.

## Recommended Workflow

1. Run `/compliance-license-audit` to get a full picture of your license landscape
2. Address any critical findings (incompatible licenses, missing licenses)
3. Run `/compliance-notice-generate` to create attribution files fulfilling your obligations
4. Add attribution file maintenance to your release checklist

## Plugin Details

| Field | Value |
|-------|-------|
| Version | 1.0.0 |
| Author | [Charles Jones](https://charlesjones.dev) |
| License | MIT |
| Repository | [claude-code-plugins-dev](https://github.com/charlesjones-dev/claude-code-plugins-dev) |
