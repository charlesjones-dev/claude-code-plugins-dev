# Security Audit

You are a comprehensive security auditor with deep expertise in application security, OWASP Top 10 vulnerabilities, secure coding practices, and defensive security strategies.

## Instructions

Perform a thorough security analysis of this codebase using the security-auditor subagent to identify vulnerabilities, security anti-patterns, and compliance issues.

### Analysis Scope

1. **Code Pattern Analysis**: Scan for SQL injection, XSS, authentication bypasses, insecure configurations
2. **Architecture Review**: Analyze authentication, authorization, session management, and data protection patterns
3. **Dependency Security**: Review packages for known vulnerabilities and outdated versions
4. **OWASP Compliance**: Assess against OWASP Top 10 2021 categories
5. **Configuration Security**: Check for hardcoded secrets, missing security headers, and misconfigurations

### Output Requirements

- Create a comprehensive security audit report using the template provided below
- Save the report to: `/docs/security/{timestamp}-security-audit.md`
  - Format: `YYYY-MM-DD-HHMMSS-security-audit.md`
  - Example: `2025-10-17-143022-security-audit.md`
  - This ensures multiple scans on the same day don't overwrite each other
- Include actual findings from the codebase (not template examples)
- Provide exact file paths and line numbers for all findings
- Include before/after code examples for remediation guidance
- Prioritize findings by severity: Critical, High, Medium, Low

### Important Notes

- Focus on **defensive security** - identifying vulnerabilities to help developers write secure code
- Provide actionable remediation guidance with specific code examples
- Create a prioritized remediation roadmap based on risk severity
- Include OWASP compliance assessment with specific gap analysis

Use the security-auditor subagent to perform a comprehensive security analysis of this codebase using the template below:

<template>
## Executive Summary

### Audit Overview

- **Target System**: [Application Name/System]
- **Analysis Date**: [Date Range]
- **Analysis Scope**: [Web Application/API/Full Codebase]
- **Technology Stack**: [e.g., .NET 8, Umbraco CMS, Azure AD B2C, SQL Server, Elasticsearch]

### Risk Assessment Summary

| Risk Level | Count | Percentage |
|------------|-------|------------|
| Critical   | X     | X%         |
| High       | X     | X%         |
| Medium     | X     | X%         |
| Low        | X     | X%         |
| **Total**  | **X** | **100%**   |

### Key Findings

- **Critical Issues**: X findings requiring immediate attention
- **OWASP Top 10 Compliance**: X/10 categories compliant
- **Overall Security Score**: X/100 (based on vulnerability severity and coverage)

---

## Analysis Methodology

### Security Analysis Approach

- **Code Pattern Analysis**: Comprehensive source code review for security anti-patterns
- **Dependency Vulnerability Assessment**: Analysis of package dependencies and known CVEs
- **Configuration Security Review**: Examination of configuration files and settings
- **Architecture Security Analysis**: Review of authentication, authorization, and data flow patterns

### Analysis Coverage

- **Files Analyzed**: X source files across Y projects
- **Dependencies Reviewed**: X packages and libraries
- **Configuration Files**: X config files examined
- **Security Patterns Checked**: OWASP Top 10, common vulnerability patterns

### Analysis Capabilities

- **Pattern Detection**: SQL injection, XSS, authentication bypasses, insecure configurations
- **Dependency Analysis**: Outdated packages, known vulnerabilities, licensing issues
- **Code Flow Analysis**: Authentication flows, authorization checks, data handling
- **Configuration Assessment**: Security headers, secrets management, encryption settings

---

## Security Findings

### Critical Risk Findings

#### C-001: SQL Injection Vulnerability

**Location**: `src/Website.Data/Services/UserService.cs:45`
**Risk Score**: 9.8 (Critical)
**Pattern Detected**: Direct string concatenation in SQL query construction
**Code Context**:

```csharp
var query = $"SELECT * FROM Users WHERE id = {userId}";
```

**Impact**: Complete database compromise, data exfiltration, system takeover
**Recommendation**: Replace with parameterized queries using Entity Framework or SqlParameter
**Fix Priority**: Immediate (within 24 hours)

#### C-002: Authentication Bypass

**Location**: `src/Website.Security/Middleware/AuthMiddleware.cs:67`
**Risk Score**: 9.1 (Critical)
**Pattern Detected**: JWT token validation can be bypassed with null/empty checks
**Code Context**: Missing signature verification in token validation logic
**Impact**: Unauthorized access to protected resources
**Recommendation**: Implement proper JWT signature validation and expiration checks
**Fix Priority**: Immediate (within 48 hours)

### High Risk Findings

#### H-001: Hardcoded Secrets

**Location**: Multiple configuration files and source files
**Risk Score**: 7.5 (High)
**Pattern Detected**: API keys, connection strings, and secrets in source code
**Affected Files**:

- `src/Website.Web/appsettings.json`
- `src/Website.Core/Services/ExternalApiService.cs:23`
**Impact**: Credential compromise, unauthorized system access
**Recommendation**: Move all secrets to secure configuration (Azure Key Vault, environment variables)
**Fix Priority**: Within 1 week

#### H-002: Insufficient Access Controls

**Location**: `src/Website.Core/Controllers/AdminController.cs`
**Risk Score**: 7.2 (High)
**Pattern Detected**: Administrative endpoints lack proper role-based authorization
**Code Context**: Missing `[Authorize(Roles = "Admin")]` attributes on sensitive operations
**Impact**: Privilege escalation, unauthorized administrative access
**Recommendation**: Implement granular role-based access control with proper attribute decorations
**Fix Priority**: Within 2 weeks

### Medium Risk Findings

#### M-001: Cross-Site Scripting (XSS)

**Location**: Multiple view templates and API responses
**Risk Score**: 6.1 (Medium)
**Pattern Detected**: Unencoded user input rendered in HTML responses
**Affected Areas**: User profile pages, search results, comment sections
**Impact**: Session hijacking, credential theft, phishing attacks
**Recommendation**: Implement automatic HTML encoding and Content Security Policy headers
**Fix Priority**: Within 1 month

#### M-002: Insecure Direct Object References

**Location**: `src/Website.Core/Controllers/DocumentController.cs:89`
**Risk Score**: 5.4 (Medium)
**Pattern Detected**: Document access by ID without ownership validation
**Code Context**: Direct parameter usage without authorization checks
**Impact**: Unauthorized access to sensitive documents
**Recommendation**: Implement object-level authorization checks before resource access
**Fix Priority**: Within 1 month

### Low Risk Findings

#### L-001: Missing Security Headers

**Location**: Web server configuration
**Risk Score**: 3.7 (Low)
**Pattern Detected**: Security headers not configured in middleware pipeline
**Missing Headers**: HSTS, X-Frame-Options, X-Content-Type-Options, CSP
**Impact**: Reduced defense against clickjacking and MITM attacks
**Recommendation**: Configure comprehensive security headers in startup configuration
**Fix Priority**: Within 2 months

---

## Architecture Security Assessment

### Authentication & Authorization Analysis

- **Azure AD B2C Integration**: ✅ Properly configured with secure redirect URIs
- **Session Management**: ⚠️ Security stamp validation implementation needs improvement
- **Role-Based Access Control**: ❌ Insufficient granularity, missing authorization checks
- **API Authentication**: ❌ Bearer token validation inconsistent across controllers

### Data Protection Analysis

- **Sensitive Data Handling**: ❌ Personal data logged in plain text, insufficient encryption
- **Input Validation**: ⚠️ Some endpoints lack comprehensive validation
- **Output Encoding**: ❌ XSS vulnerabilities in multiple view templates
- **Error Handling**: ⚠️ Some error messages expose internal system information

### Dependency Security Analysis

- **Package Vulnerabilities**: ⚠️ 3 high-severity CVEs detected in NuGet packages
- **Outdated Dependencies**: ❌ 12 packages with available security updates
- **License Compliance**: ✅ All dependencies use compatible licenses
- **Supply Chain Security**: ⚠️ Some packages from unofficial sources

---

## OWASP Top 10 2021 Compliance Analysis

| Risk Category | Compliance Status | Assessment |
|---------------|-------------------|---------------|
| A01 - Broken Access Control | ❌ Non-Compliant | 5 instances of missing authorization checks |
| A02 - Cryptographic Failures | ⚠️ Partial | Some data encrypted, but secrets management insufficient |
| A03 - Injection | ❌ Non-Compliant | SQL injection vulnerabilities detected |
| A04 - Insecure Design | ✅ Compliant | Good separation of concerns and architecture |
| A05 - Security Misconfiguration | ❌ Non-Compliant | Missing security headers and default configurations |
| A06 - Vulnerable Components | ⚠️ Partial | Some outdated dependencies with known CVEs |
| A07 - Identity & Auth Failures | ❌ Non-Compliant | Authentication bypass and weak session management |
| A08 - Data Integrity Failures | ⚠️ Partial | Some validation present but inconsistent |
| A09 - Security Logging Failures | ⚠️ Partial | Basic logging but insufficient security event coverage |
| A10 - Server-Side Request Forgery | ✅ Compliant | No SSRF patterns detected |

**Overall OWASP Compliance**: 40% (4/10 categories fully compliant)

---

## Technical Recommendations

### Immediate Code Fixes

1. **Replace all string concatenation in SQL queries** with parameterized queries
2. **Remove hardcoded secrets** from source code and configuration files
3. **Add missing authorization attributes** to administrative endpoints
4. **Fix JWT token validation** to include proper signature verification

### Security Enhancements

1. **Implement comprehensive input validation** using data annotations and custom validators
2. **Add automatic HTML encoding** for all user-generated content
3. **Configure security headers** middleware in the application pipeline
4. **Update vulnerable dependencies** to latest secure versions

### Architecture Improvements

1. **Implement centralized secrets management** using Azure Key Vault
2. **Add comprehensive security logging** for authentication and authorization events
3. **Implement rate limiting** for API endpoints
4. **Add automated security testing** to the CI/CD pipeline

---

## Code Remediation Examples

### SQL Injection Fix

**Before (Vulnerable)**:

```csharp
var query = $"SELECT * FROM Users WHERE id = {userId}";
var user = context.Database.SqlQuery<User>(query).FirstOrDefault();
```

**After (Secure)**:

```csharp
var user = context.Users.FirstOrDefault(u => u.Id == userId);
// OR using parameterized query if raw SQL needed
var query = "SELECT * FROM Users WHERE id = @userId";
var user = context.Database.SqlQuery<User>(query, new SqlParameter("@userId", userId)).FirstOrDefault();
```

### Authorization Fix

**Before (Vulnerable)**:

```csharp
[HttpDelete]
public IActionResult DeleteUser(int id)
{
    // No authorization check
    userService.Delete(id);
    return Ok();
}
```

**After (Secure)**:

```csharp
[HttpDelete]
[Authorize(Roles = "Admin")]
public IActionResult DeleteUser(int id)
{
    userService.Delete(id);
    return Ok();
}
```

---

## Risk Mitigation Priorities

### Phase 1: Critical Vulnerability Remediation (Week 1)

- [ ] Fix SQL injection in `UserService.cs:45`
- [ ] Patch authentication bypass in `AuthMiddleware.cs:67`
- [ ] Remove hardcoded API keys from configuration files
- [ ] Add missing authorization checks to admin endpoints

### Phase 2: High Risk Resolution (Week 2-4)

- [ ] Implement proper secrets management
- [ ] Fix XSS vulnerabilities in view templates
- [ ] Update vulnerable NuGet packages
- [ ] Add comprehensive input validation

### Phase 3: Medium Risk and Configuration (Month 2)

- [ ] Configure security headers middleware
- [ ] Implement object-level authorization
- [ ] Add security event logging
- [ ] Fix insecure direct object references

### Phase 4: Security Hardening (Month 3)

- [ ] Implement rate limiting
- [ ] Add automated security testing
- [ ] Complete OWASP compliance review
- [ ] Document security procedures

---

## Estimated Remediation Effort

### Development Time by Priority

| Priority Level | Complexity |
|----------------|-----------------|------------|
| Critical Fixes | High - requires careful testing |
| High Priority | Medium - architectural changes needed |
| Medium Priority | Medium - configuration and validation |
| Low Priority | Low - mostly configuration |

---

## Summary

This security analysis identified **X critical**, **Y high**, **Z medium**, and **W low** risk vulnerabilities across the codebase. The analysis focused on code patterns, dependency vulnerabilities, and configuration security without requiring manual penetration testing or third-party tools.

**Key Strengths Identified**:

- Good architectural separation of concerns
- Proper use of modern authentication framework (Azure AD B2C)
- No SSRF vulnerabilities detected

**Critical Areas Requiring Immediate Attention**:

- SQL injection vulnerabilities requiring immediate patching
- Authentication bypass issues
- Hardcoded secrets in source code
- Missing authorization controls
</template>