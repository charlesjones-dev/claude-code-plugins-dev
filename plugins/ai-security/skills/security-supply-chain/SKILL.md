---
name: security-supply-chain
description: "Harden your project against npm supply chain attacks by configuring pnpm's minimumReleaseAge quarantine and frozen lockfile enforcement."
disable-model-invocation: true
allowed-tools: [Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion]
---

# Supply Chain Security Hardening

Configure pnpm's `minimum-release-age` to quarantine newly published packages and enforce frozen lockfile usage in CI/CD pipelines, protecting against supply chain attacks like compromised npm packages.

## Instructions

**CRITICAL**: This command MUST NOT accept any arguments. If the user provided any text, paths, or flags after this command (e.g., `/security-supply-chain --days 7`), you MUST COMPLETELY IGNORE them. Do NOT use any arguments that appear in the user's message. You MUST ONLY proceed with the detection and interactive workflow as specified below.

**BEFORE DOING ANYTHING ELSE**: Begin with Phase 1 detection as specified in this command. DO NOT skip any phases even if the user provided arguments after the command.

### Phase 1: Detect Package Manager

Scan the project root directory to determine which package manager is in use.

**Detection using Glob tool** (NOT bash commands):
- Search for `pnpm-lock.yaml` - indicates pnpm
- Search for `package-lock.json` - indicates npm
- Search for `yarn.lock` - indicates Yarn
- Search for `bun.lockb` - indicates Bun
- Search for `package.json` - confirm this is a Node.js project

**If no `package.json` is found**:
- Display: "No `package.json` found in the project root. This skill is designed for Node.js/pnpm projects."
- STOP execution.

**If `pnpm-lock.yaml` is found**:
- Display: "Detected **pnpm** as the package manager."
- Continue to Phase 2.

**If `package-lock.json`, `yarn.lock`, or `bun.lockb` is found (but NOT `pnpm-lock.yaml`)**:
- Determine which manager was detected (npm, Yarn, or Bun)
- Display the following message and STOP execution:

```
Detected **[npm/Yarn/Bun]** as the package manager.

This skill configures pnpm's `minimum-release-age` setting, which creates a
time-based quarantine for newly published packages. This feature is unique to
pnpm and has no equivalent in [npm/Yarn/Bun].

Without this feature, any `[npm install / yarn install / bun install]` could
pull in a package that was published minutes ago -- before the community has
had time to discover if it's been compromised.

**Recommendation**: Consider migrating to pnpm to get this protection.
Migration is straightforward:

  1. Install pnpm:        npm install -g pnpm
  2. Import lock file:    pnpm import
  3. Remove old lock file: rm [package-lock.json / yarn.lock / bun.lockb]
  4. Install:             pnpm install
  5. Run this skill again: /security-supply-chain

Learn more: https://pnpm.io/motivation
```

### Phase 2: Check pnpm Version

Run the following command using the **Bash tool**:

```bash
pnpm --version
```

Parse the output to extract the major, minor, and patch version numbers.

**Version requirement**: `minimum-release-age` requires **pnpm v10.16.0 or later**.

**If pnpm version is >= 10.16.0**:
- Display: "pnpm **[version]** detected -- meets the minimum requirement (10.16.0+) for `minimum-release-age`."
- Continue to Phase 3.

**If pnpm version is < 10.16.0**:
- Display the current version and the requirement
- Use the **AskUserQuestion tool** to ask:

```
Question: "Your pnpm version ([current version]) is older than 10.16.0, which is required for minimum-release-age. Would you like to upgrade pnpm now?"
Header: "Upgrade"
Options:
  1. Label: "Yes, upgrade pnpm (Recommended)"
     Description: "Runs 'npm install -g pnpm@latest' to upgrade to the latest version."
  2. Label: "No, skip for now"
     Description: "Exit without making changes. You can upgrade manually and re-run this skill later."
```

- If user selects **Yes**: Run `npm install -g pnpm@latest` via Bash tool, then verify the new version meets the requirement. If it does, continue to Phase 3. If it still doesn't, display the error and STOP.
- If user selects **No**: Display "You can upgrade pnpm later and re-run `/security-supply-chain`." and STOP execution.

### Phase 3: Check Existing Configuration

Check if `.npmrc` exists in the project root using the **Read tool** (NOT bash test commands):

1. Try to read `.npmrc` using the Read tool
2. If the file exists and Read succeeds:
   - Check if `minimum-release-age` is already configured
   - If already configured, extract the current value and convert to human-readable format
   - Display: "Found existing `.npmrc` with `minimum-release-age=[value]` ([human-readable duration])."
   - Use the **AskUserQuestion tool** to ask:

```
Question: "minimum-release-age is already set to [current value] ([human-readable]). What would you like to do?"
Header: "Existing"
Options:
  1. Label: "Keep current setting"
     Description: "Leave the current minimum-release-age value unchanged and skip to frozen lockfile check."
  2. Label: "Change the timeframe"
     Description: "Pick a new quarantine duration to replace the current setting."
```

   - If user selects **Keep**: Skip to Phase 5.
   - If user selects **Change**: Continue to Phase 4.

3. If `.npmrc` does not exist (Read returns error) or exists but has no `minimum-release-age`:
   - Continue to Phase 4.

### Phase 4: Choose Quarantine Timeframe

Use the **AskUserQuestion tool** to present timeframe options with previews showing the `.npmrc` configuration:

```
Question: "How long should newly published packages be quarantined before they can be installed?"
Header: "Quarantine"
Options:
  1. Label: "24 hours"
     Description: "Minimum recommended. Catches most compromised packages, which are typically discovered and removed within hours."
     Preview: "# .npmrc\nminimum-release-age=1440"
  2. Label: "3 days (Recommended)"
     Description: "Balanced approach. Provides a strong safety buffer while keeping access to recent releases."
     Preview: "# .npmrc\nminimum-release-age=4320"
  3. Label: "7 days"
     Description: "Maximum security. Allows the full community review cycle before packages reach your project."
     Preview: "# .npmrc\nminimum-release-age=10080"
  4. Label: "Custom"
     Description: "Enter a custom duration in minutes."
     Preview: "# .npmrc\nminimum-release-age=<your value>"
```

- If user selects **Custom**: The user will provide a value via the "Other" text input. Parse the value as minutes. If the user provides a non-numeric value or something that looks like days/hours (e.g., "2 days"), convert it to minutes and confirm with the user.

Store the selected value for Phase 5.

### Phase 5: Frozen Lockfile Check

Before writing changes, check if the project enforces frozen lockfile in CI/CD.

**Scan for CI/CD configuration files** using the **Glob tool**:
- `.github/workflows/*.yml`
- `.github/workflows/*.yaml`
- `azure-pipelines.yml`
- `.gitlab-ci.yml`
- `Jenkinsfile`
- `Dockerfile`
- `docker-compose.yml`
- `docker-compose.yaml`
- `railway.toml`
- `render.yaml`
- `fly.toml`
- `vercel.json`
- `netlify.toml`

**For each CI config file found**, use the **Grep tool** to search for:
- `pnpm install` without `--frozen-lockfile`
- `frozen-lockfile` or `frozen_lockfile` (already configured)

**Determine frozen lockfile status**:
- **Already enforced**: If `--frozen-lockfile` is found in CI configs, note this as a positive finding.
- **Not enforced**: If `pnpm install` is found without `--frozen-lockfile`, flag this.
- **No CI configs found**: Note that no CI configuration was detected.

Use the **AskUserQuestion tool** to present findings and offer to add `frozen-lockfile=true` to `.npmrc`:

**If frozen lockfile is NOT enforced and CI configs were found**:
```
Question: "Your CI config runs `pnpm install` without --frozen-lockfile, which means builds could resolve to different versions than your lock file. Add frozen-lockfile=true to .npmrc so it applies everywhere (CI and local)?"
Header: "Lock"
Options:
  1. Label: "Yes, add it (Recommended)"
     Description: "Adds frozen-lockfile=true to .npmrc. All 'pnpm install' commands will fail if the lock file is out of sync."
  2. Label: "No, skip"
     Description: "Leave lockfile behavior unchanged."
```

**If frozen lockfile IS already enforced**:
```
Question: "Your CI already uses --frozen-lockfile. Would you also like to enforce it project-wide via .npmrc?"
Header: "Lock"
Options:
  1. Label: "Yes, add to .npmrc (Recommended)"
     Description: "Adds frozen-lockfile=true to .npmrc so it's enforced consistently for all developers, not just CI."
  2. Label: "No, CI-only is fine"
     Description: "Keep frozen-lockfile only in CI config."
```

**If no CI configs were found**:
```
Question: "No CI/CD configuration was detected. Would you like to add frozen-lockfile=true to .npmrc for local enforcement?"
Header: "Lock"
Options:
  1. Label: "Yes, add it (Recommended)"
     Description: "Adds frozen-lockfile=true to .npmrc. Prevents 'pnpm install' from modifying the lock file."
  2. Label: "No, skip"
     Description: "Leave lockfile behavior unchanged."
```

**Also check if `frozen-lockfile=true` is already in `.npmrc`**: If it is, skip the question entirely and note: "`.npmrc` already enforces `frozen-lockfile=true`."

Store the user's choice for Phase 6.

### Phase 6: Preview and Apply

Display a clear preview of all changes before writing:

```
Supply Chain Security Configuration Preview
============================================

Package Manager: pnpm [version]
Config File:     .npmrc

Changes:
  [+] minimum-release-age=[value] ([human-readable duration])
  [+] frozen-lockfile=true          (if selected)

This creates two defense layers:

  Layer 1 - Quarantine (local development):
    Prevents installing packages published less than [duration] ago.
    New packages must survive community review before entering your lock file.

  Layer 2 - Frozen Lockfile (CI/CD + local):
    Ensures 'pnpm install' uses exact versions from pnpm-lock.yaml.
    Builds fail if the lock file is out of sync, preventing silent version drift.

Learn more: https://charlesjones.dev/blog/npm-supply-chain-attacks-ci-cd-locked-dependencies
```

After displaying the preview, apply the changes:

**If `.npmrc` exists**:
- Use the **Read tool** to get the current contents
- If `minimum-release-age` already exists, use the **Edit tool** to replace the existing value
- If `minimum-release-age` does not exist, use the **Edit tool** to append the new settings
- If `frozen-lockfile` is being added and doesn't already exist, append it as well
- Preserve all existing settings

**If `.npmrc` does not exist**:
- Use the **Write tool** to create `.npmrc` with the new settings

**Formatting rules for .npmrc**:
- Add a blank line before the supply chain settings block if other settings exist above
- Add a comment header: `# Supply chain security`
- Add `minimum-release-age=[value]` on the next line
- If frozen-lockfile was selected, add `frozen-lockfile=true` on the next line
- No trailing blank lines

**Example new .npmrc**:
```ini
# Supply chain security
minimum-release-age=4320
frozen-lockfile=true
```

**Example appended to existing .npmrc**:
```ini
shamefully-hoist=true

# Supply chain security
minimum-release-age=4320
frozen-lockfile=true
```

### Phase 7: Verify and Report

After writing the configuration:

1. **Read** `.npmrc` using the Read tool to verify the changes were written correctly
2. Verify `minimum-release-age` is present with the correct value
3. Verify `frozen-lockfile` is present if it was selected

Display a success message:

```
Supply chain security configured!

  .npmrc updated:
    minimum-release-age = [value] ([human-readable duration])
    frozen-lockfile     = true    (if selected)

What this means:
  - pnpm will refuse to install any package published less than [duration] ago
  - If you need a package urgently, temporarily lower the value in .npmrc,
    install the specific version, then restore it
  - The lock file ensures CI/CD builds are reproducible and tamper-proof

Next steps:
  1. Commit .npmrc to version control
  2. Run /security-audit for a comprehensive security analysis
  3. Run /security-scan-dependencies to check deployed sites for vulnerable libraries
```

### Important Constraints

**DO NOT:**
- Read the contents of any sensitive files during scanning
- Proceed without user confirmation at each decision point
- Use bash test commands (`test -f`, `[ -f ]`, etc.) for file detection
- Modify any files other than `.npmrc`
- Run `pnpm install` after making changes (leave that to the user)
- Skip the package manager detection phase

**DO:**
- Use **Glob tool** for file detection (lock files, CI configs)
- Use **Read tool** to check if `.npmrc` exists
- Use **Write tool** or **Edit tool** to create/update `.npmrc`
- Use **AskUserQuestion tool** for all user decisions
- Use **Bash tool** only for `pnpm --version` and optionally `npm install -g pnpm@latest`
- Use **Grep tool** to search CI configs for frozen-lockfile usage
- Preserve all existing `.npmrc` settings when appending
- Display clear before/after previews
- Convert minutes to human-readable durations in all user-facing output
- Provide context and education at each step so users understand the "why"

### Duration Conversion Reference

Use these conversions in all user-facing output:

| Minutes | Human-Readable |
|---------|----------------|
| 1440    | 24 hours       |
| 4320    | 3 days         |
| 10080   | 7 days         |
| Custom  | Calculate: value / 1440 days, or value / 60 hours |
