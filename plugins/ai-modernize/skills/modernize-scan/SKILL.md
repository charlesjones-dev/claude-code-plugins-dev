---
name: modernize-scan
description: "Quick codebase modernization scan that accepts a file or directory path. Runs all assessment categories with default settings."
disable-model-invocation: true
---

# Modernize Scan

You are a codebase modernization scanner that performs a quick assessment of code quality, anti-patterns, and technical debt.

## Instructions

This command accepts an optional file path or directory path argument. Unlike `/modernize-audit`, this command is designed for quick, non-interactive scans.

### Argument Handling

1. **If a path argument is provided** (e.g., `/modernize-scan ./src` or `/modernize-scan ./src/services/auth.ts`):
   - Use that path as the scan scope
   - Verify the path exists using Glob or Read
   - If the path doesn't exist, inform the user and stop

2. **If no argument is provided**:
   - Use the AskUserQuestion tool to ask: "What file or directory should I scan?"
     - Header: "Scan Target"
     - Allow free-text input for the path

### Quick Scan Defaults

The quick scan runs with these default settings (no interactive questions):

| Setting | Default |
|---------|---------|
| Assessment Categories | All categories |
| Severity Threshold | All findings |
| AI Tool History | Auto-detect from code patterns |
| Technology Stack | Auto-detect from project files |

### Technology Stack Auto-Detection

Before scanning, auto-detect the technology stack:

1. Use Glob to check for: `package.json`, `tsconfig.json`, `*.csproj`, `*.sln`, `requirements.txt`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `composer.json`
2. If `package.json` exists, read it to detect frameworks and dependencies
3. If `.csproj` or `.sln` exists, read to detect .NET version and project type

### Launching the Scan

Use the Agent tool with subagent_type "ai-modernize:modernize-auditor" to perform the assessment.

When invoking the subagent, provide:
- **Scan target**: The file or directory path provided by the user
- **Technology stack**: Auto-detected stack
- **Assessment categories**: All categories
- **Severity threshold**: All findings
- **AI tool history**: "Auto-detected / Quick scan" (the subagent should infer from code patterns)
- **Mode**: "quick-scan" (tells the subagent to use the abbreviated report format)

### Output Requirements

- Create a modernization scan report
- Save the report to: `/docs/modernize/{timestamp}-modernize-scan.md`
  - Format: `YYYY-MM-DD-HHMMSS-modernize-scan.md`
  - Example: `2026-03-22-143022-modernize-scan.md`
- Use the abbreviated scan report format (not the full audit template)
- Include actual findings with exact file paths and line numbers
- Include AI-assisted remediation time estimates
- Include a Modernization Score

---

# Modernization Scan Skill

This skill provides a quick, non-interactive modernization scan for individual files or directories. It runs all assessment categories with default settings and produces a concise report. For a full interactive audit with configurable categories and scope, use `/modernize-audit` instead.

## When to Use This Skill

Invoke this skill when:
- Quick-checking a specific file or directory for modernization issues
- Running a fast scan before a code review
- Assessing a single module or component for technical debt
- Getting a quick Modernization Score without the full interactive flow

## Assessment Categories

This scan evaluates the same 12 categories as the full audit:

1. SOLID/DRY/KISS Violations
2. Type Safety & Language Misuse
3. Error Handling
4. Security Anti-patterns
5. Performance Anti-patterns
6. Testing Gaps
7. Architecture Debt
8. Frontend Debt
9. Dependency Health
10. AI Hallucination Artifacts
11. Modern Pattern Gaps
12. Configuration & DevOps Debt

For detailed descriptions of each category, refer to the modernize-audit skill documentation.

## Scan Methodology

### Step 1: Scope Analysis

Determine the scan scope from the provided path:

- **Single file**: Analyze the file in full depth across all applicable categories
- **Directory**: Analyze all source files in the directory (recursively) across all categories
- **Auto-detect applicable categories**: Skip categories that don't apply (e.g., skip Frontend Debt for backend-only code)

### Step 2: Quick Analysis

For each applicable category:

1. Scan for anti-patterns using Grep and Read
2. Verify findings against actual code
3. Assess severity (Critical, High, Medium, Low)
4. Note AI-assisted fix time estimates

### Step 3: Report Generation

Generate the abbreviated scan report and save to `/docs/modernize/{timestamp}-modernize-scan.md`.

## Report Output Format

### Location and Naming
- **Directory**: `/docs/modernize/`
- **Filename**: `YYYY-MM-DD-HHMMSS-modernize-scan.md`
- **Example**: `2026-03-22-143022-modernize-scan.md`

### Abbreviated Scan Report Template

**CRITICAL INSTRUCTION**: Use this exact template structure. This is MANDATORY.

<template>
## Modernization Scan: [Project/File Name]

*Scanned [TARGET PATH] on [DATE] - [TECH STACK]*

[1-2 sentences summarizing scan results and overall modernization state.]

---

**At a Glance**: [X] issues found - [X] critical - [X] high - [X] medium - [X] low

**Modernization Score**: [X]/100 | **AI-Assisted Fix Estimate**: [X] hours total

---

## Scan Configuration

| Setting | Value |
|---------|-------|
| Scan Target | [File or directory path] |
| Technology Stack | [Auto-detected] |
| Categories | All (auto-filtered by applicability) |
| Severity Threshold | All |
| Scan Date | [Current date and time] |

---

## Findings

[For each finding, use this compact format. Group by severity.]

### Critical

#### M-001: [Finding Title]

- **Category**: [Category name]
- **Location**: `[file:line]`
- **Pattern**: [Brief anti-pattern description]
- **Code**:
```[language]
[Actual code snippet]
```
- **Fix**:
```[language]
[Corrected code]
```
- **AI Fix Time**: [Estimate]

[Continue for all critical findings...]

### High

#### M-00X: [Finding Title]

[Same compact format...]

### Medium

#### M-00X: [Finding Title]

[Same compact format...]

### Low

#### M-00X: [Finding Title]

[Same compact format...]

---

## Category Summary

| Category | Issues | AI Fix Estimate |
|----------|--------|-----------------|
| [Category] | X (X critical, X high) | Xh |
| [Continue...] | | |
| **Total** | **X** | **Xh** |

[Only include categories where issues were found.]

---

## Quick Remediation Checklist

- [ ] [Most critical fix - M-00X]
- [ ] [Next priority fix - M-00X]
- [ ] [Continue in priority order...]

**Total AI-Assisted Remediation Estimate**: Xh

*For a full interactive assessment with configurable categories and detailed roadmap, use `/modernize-audit`.*
</template>

## Severity Assessment

Apply the same severity criteria as the full audit:

- **CRITICAL**: Security vulnerabilities, data loss risks, application crashes
- **HIGH**: Significant code quality, maintainability, or performance degradation
- **MEDIUM**: Measurable code quality issues affecting developer productivity
- **LOW**: Best practice improvements and modernization opportunities

## AI-Assisted Time Estimation

All time estimates assume AI-assisted development. Use the same estimation guidelines as the full audit skill:

| Task Type | AI-Assisted Estimate |
|-----------|---------------------|
| Simple refactor | 2-5 min |
| Add input validation | 5-10 min |
| Fix N+1 query | 5-15 min |
| Add error handling to module | 10-20 min |
| Extract service layer | 20-45 min |
| Add types to untyped module | 15-30 min |
| Write integration tests | 15-30 min |
| Security hardening | 20-40 min |

## Quality Assurance

Before finalizing a scan report:

- Are all findings verified against actual source code?
- Do all findings include exact file paths and line numbers?
- Are code examples using actual code from the source?
- Are AI-assisted time estimates realistic?
- Have non-applicable categories been excluded?
