# AI-Security Plugin

**Comprehensive AI-powered security toolkit for Claude Code.** Intelligent security scanning, vulnerability detection, threat analysis, and secure development guidance.

---

## 🎯 What This Plugin Does

Provides a complete suite of AI-powered security tools including commands, agents, and skills that help you build secure applications, detect vulnerabilities, analyze threats, and maintain security best practices throughout your development lifecycle.

### Why Not Just Use `/security-review`?

Claude Code ships with a native `/security-review` command that provides basic security analysis. However, it has limitations:

❌ **No custom scan templates** - You can't define what the report should include
❌ **No output file control** - Results appear in chat but aren't saved to a specific location
❌ **No reproducibility** - Each scan produces different output formats
❌ **No standardization** - Can't ensure consistent audit documentation across projects

This plugin enhances security scanning by providing:

✅ **Custom scan templates** - Define exactly what your audit should cover
✅ **Controlled output location** - Reports saved to `/docs/security/{timestamp}-security-audit.md` (timestamp prevents overwrites)
✅ **Reproducible audits** - Same comprehensive format every time
✅ **Standardized documentation** - Consistent audit reports across all projects
✅ **Timestamped tracking** - Easy to compare audits over time
✅ **Enterprise-ready** - Professional audit documents suitable for compliance

**Use `/security-review` for:** Quick ad-hoc security checks during development

**Use `/security-audit` for:** Formal security audits, compliance documentation, and repeatable security assessments

## 📋 Available Commands

### `/security-audit`

Perform comprehensive security analysis on your codebase and generate a detailed audit report with vulnerability findings and remediation guidance.

**Before (manual):**

```
# Manual security review process
- Review each file for SQL injection patterns
- Check for XSS vulnerabilities
- Analyze authentication/authorization logic
- Review dependency vulnerabilities
- Check for hardcoded secrets
- Assess OWASP Top 10 compliance
- Write detailed findings document
- Create remediation plan
```

**After (with ai-security plugin):**

```
/security-audit
# ✨ AI analyzes entire codebase for vulnerabilities
# ✨ Identifies security risks across OWASP Top 10 categories
# ✨ Generates comprehensive audit report
# ✨ Provides code examples and remediation steps
# ✅ Report saved to /docs/security with timestamp
```

## 🤖 Available Agents

### `security-auditor`

Specialized agent that performs deep security analysis and generates comprehensive audit reports. Automatically invoked by `/security-audit` command.

---

## 🚀 Quick Start

### Installation

```
/plugin install ai-security@claude-code-plugins-dev
```

### Usage

```
# Run a security audit
/security-audit

# Review the generated report
# Located at: /docs/security/{timestamp}-security-audit.md
# Example: /docs/security/2025-10-17-143022-security-audit.md
```

---

## 💡 Features

### `/security-audit` Command

#### Comprehensive Vulnerability Detection

- **SQL Injection**: Identifies unsafe query construction patterns
- **Cross-Site Scripting (XSS)**: Detects unencoded user input in views
- **Authentication Bypass**: Analyzes JWT token validation and session management
- **Authorization Issues**: Finds missing or improper access controls
- **Hardcoded Secrets**: Locates API keys, passwords, and sensitive data in code
- **Insecure Direct Object References**: Identifies missing ownership validation

#### OWASP Top 10 2021 Compliance

Automatically assesses your codebase against all OWASP Top 10 categories:

- A01 - Broken Access Control
- A02 - Cryptographic Failures
- A03 - Injection
- A04 - Insecure Design
- A05 - Security Misconfiguration
- A06 - Vulnerable Components
- A07 - Identity & Authentication Failures
- A08 - Data Integrity Failures
- A09 - Security Logging Failures
- A10 - Server-Side Request Forgery

#### Architecture Security Assessment

- **Authentication & Authorization Analysis**: Reviews identity management patterns
- **Data Protection Analysis**: Checks encryption, validation, and encoding
- **Dependency Security**: Identifies vulnerable packages and outdated dependencies
- **Configuration Review**: Analyzes security headers, error handling, and settings

#### Detailed Reporting

Each finding includes:

- **Location**: Exact file path and line number
- **Risk Score**: Numerical severity rating (0-10)
- **Pattern Detected**: What vulnerability was identified
- **Code Context**: The problematic code snippet
- **Impact**: What could happen if exploited
- **Recommendation**: How to fix it
- **Fix Priority**: When it should be addressed

#### Code Remediation Examples

Reports include before/after code examples showing:

- Vulnerable code patterns
- Secure replacement code
- Explanation of the fix
- Best practices applied

---

## 📊 Example Audit Results

### Executive Summary

```
Risk Assessment Summary:
┌──────────┬───────┬────────────┐
│ Critical │ High  │ Medium     │
├──────────┼───────┼────────────┤
│ 2        │ 3     │ 4          │
└──────────┴───────┴────────────┘

OWASP Compliance: 40% (4/10 categories)
Overall Security Score: 62/100
```

### Critical Finding Example

```
C-001: SQL Injection Vulnerability
Location: src/Services/UserService.cs:45
Risk Score: 9.8 (Critical)

Vulnerable Code:
var query = $"SELECT * FROM Users WHERE id = {userId}";

Secure Fix:
var user = context.Users.FirstOrDefault(u => u.Id == userId);

Fix Priority: Immediate (within 24 hours)
```

---

## ⚙️ How It Works

The `/security-audit` command uses Claude Code's specialized **security-auditor agent** to perform comprehensive security analysis:

1. **Code Analysis**
   - Scans source files for security anti-patterns
   - Analyzes authentication and authorization flows
   - Reviews configuration files for misconfigurations
   - Checks dependency packages for known vulnerabilities

2. **Pattern Detection**
   - Identifies SQL injection vectors
   - Detects XSS vulnerabilities
   - Finds authentication bypass opportunities
   - Locates hardcoded secrets
   - Checks for missing authorization

3. **Report Generation**
   - Categorizes findings by severity (Critical, High, Medium, Low)
   - Provides exact locations with file paths and line numbers
   - Includes code examples and remediation guidance
   - Creates prioritized remediation roadmap
   - Saves timestamped report to /docs/security folder

The specialized agent brings deep security expertise and pattern recognition capabilities to identify vulnerabilities that might be missed by manual review.

---

## 🎓 Best Practices

### When to Run Security Audits

- ✅ Before production deployments
- ✅ After implementing authentication/authorization features
- ✅ When adding new API endpoints
- ✅ After integrating third-party libraries
- ✅ During security reviews and compliance checks
- ✅ As part of CI/CD pipeline (automated security gates)

### How to Use Audit Results

1. **Prioritize Critical & High findings** - Address these immediately
2. **Review code context** - Understand why each finding is a risk
3. **Apply remediation examples** - Use provided code fixes as templates
4. **Test fixes thoroughly** - Ensure security patches don't break functionality
5. **Re-audit after fixes** - Verify vulnerabilities are resolved

---

## ⏱️ Time Savings

**Per security audit:**

- Manual security review: ~4-8 hours (for medium-sized codebase)
- With security-audit: ~2-3 minutes (AI-powered analysis)

**Estimated savings:**

- Per comprehensive audit: Save ~4-8 hours
- Per month (2 audits): Save ~8-16 hours
- Per year: Save ~100+ hours

Plus reduced security incident risk and faster vulnerability remediation.

---

## 🔒 Security Expertise Built-In

This plugin embodies expert security knowledge across multiple domains:

### Vulnerability Detection

- OWASP Top 10 vulnerability patterns (2021 & 2025)
- Common authentication/authorization flaws
- SQL injection and XSS attack vectors
- API security vulnerabilities
- Cryptographic weaknesses

### Secure Development

- Secrets management best practices
- Secure coding standards (CERT, CWE)
- Input validation and sanitization
- Defense-in-depth strategies
- Security design patterns

### Threat Analysis

- Attack surface analysis
- Threat modeling methodologies (STRIDE, PASTA)
- Risk assessment frameworks
- Security architecture review

### Compliance & Standards

- OWASP ASVS (Application Security Verification Standard)
- CWE (Common Weakness Enumeration)
- NIST Cybersecurity Framework
- PCI-DSS, HIPAA, GDPR security requirements

---

## 🔧 Configuration

No configuration needed! The plugin works out of the box and generates comprehensive security reports automatically.

Reports are saved to: `/docs/security/{timestamp}-security-audit.md`

**Naming Format:** `YYYY-MM-DD-HHMMSS-security-audit.md` (e.g., `2025-10-17-143022-security-audit.md`)

This timestamp-based naming ensures multiple audits on the same day don't overwrite each other.

---

## 📦 Plugin Details

- **Name:** AI-Security
- **Version:** 1.0.0
- **Category:** Security
- **Type:** Comprehensive Security Toolkit
- **Features:**
  - Commands: `/security-audit`
  - Agents: `security-auditor`
- **License:** MIT
- **Author:** Charles Jones

---

## ⚠️ Important Notes

### What This Plugin Does

- ✅ Static code analysis and pattern detection
- ✅ Architecture and configuration security review
- ✅ Dependency vulnerability assessment
- ✅ Security best practices validation
- ✅ Threat modeling and risk analysis
- ✅ Compliance checking and reporting
- ✅ Secure development guidance
- ✅ AI-assisted security education

### What This Plugin Doesn't Do

- ❌ Runtime penetration testing
- ❌ Network security scanning
- ❌ Dynamic application security testing (DAST)
- ❌ Exploit development or offensive security
- ❌ Replace manual security testing by experts
- ❌ Credential harvesting or malicious code creation

### Security & Ethics

This plugin is designed exclusively for **defensive security** purposes:

- Helps developers write secure code
- Identifies vulnerabilities early in the development lifecycle
- Educates teams on security best practices
- Supports compliance and audit requirements
- Prevents security incidents before they occur

**NOT for offensive security, exploit development, or malicious purposes.**

---

## 🤝 Contributing

Found a bug or have a suggestion? [Open an issue](https://github.com/charlesjones-dev/claude-code-plugins-dev/issues) or submit a pull request!

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for the Claude Code community**
