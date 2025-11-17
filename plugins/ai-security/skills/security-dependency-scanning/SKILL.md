---
name: security-dependency-scanning
description: Guide for conducting comprehensive web dependency security scans to identify outdated libraries, CVEs, and security misconfigurations. Use when analyzing deployed websites for dependency vulnerabilities.
---

# Web Dependency Security Scanning Skill

This skill provides expert guidance for scanning deployed websites to identify outdated dependencies, known vulnerabilities (CVEs), insecure configurations, and missing security controls.

## When to Use This Skill

Invoke this skill when:
- Scanning a deployed website for outdated libraries and frameworks
- Identifying CVEs in frontend dependencies (jQuery, React, Vue, Bootstrap, etc.)
- Detecting CMS versions and known vulnerabilities (WordPress, Drupal, Umbraco, Sitecore, etc.)
- Auditing HTTP security headers and configurations
- Performing third-party website security assessments
- Conducting pre-acquisition technical due diligence
- Analyzing supply chain security risks in web applications
- Evaluating client-side dependency security without source code access

## Required Tools

**🚨 CRITICAL: Tool Requirements for Website Scanning 🚨**

You MUST use ONLY these tools to fetch and analyze websites:
- ✅ **WebFetch tool** - Primary method for fetching HTML and HTTP headers
- ✅ **curl** (via Bash tool) - Alternative method: `curl -i https://example.com`

You MUST NOT use these tools:
- ❌ **Playwright** or any MCP browser automation tools
- ❌ **Any browser-based tools** (mcp__playwright__browser_navigate, etc.)
- ❌ **Any other MCP web browsing tools**

**Why This Matters**:
- HTTP security headers (Content-Security-Policy, HSTS, X-Frame-Options, etc.) are ONLY available via raw HTTP responses
- Playwright and browser tools **cannot access** these critical security headers
- Using browser tools will result in **incomplete and inaccurate security header analysis**
- WebFetch and curl provide the raw HTTP response headers required for comprehensive security auditing

**If you use Playwright or browser tools, the security scan will be incomplete and the report will be invalid.**

## Core Web Security Expertise

### 1. Frontend Library Detection

To identify JavaScript and CSS libraries, analyze:
- **CDN URL Patterns**: Extract library names and versions from CDN URLs
  - jsDelivr: `cdn.jsdelivr.net/npm/{package}@{version}/{file}`
  - unpkg: `unpkg.com/{package}@{version}/{file}`
  - cdnjs: `cdnjs.cloudflare.com/ajax/libs/{library}/{version}/{file}`
  - Google Hosted: `ajax.googleapis.com/ajax/libs/{library}/{version}/{file}`
- **Script/Link Tag Analysis**: Parse `<script src>` and `<link href>` for versioned filenames
  - Examples: `jquery-3.6.0.min.js`, `react.production.min.js`, `bootstrap.min.css`
- **File Content Inspection**: Look for version comments in fetched files
  - Examples: `/*! jQuery v3.6.0 */`, `/*! Bootstrap v4.3.1 */`
- **Meta Tag Detection**: Extract version info from HTML meta tags
  - Examples: `<meta name="generator" content="Next.js 13.4.0">`
- **Global Variables**: Document detection of version-exposing globals
  - Examples: `jQuery.fn.jquery`, `React.version`, `Vue.version`

**Common Libraries to Detect**:
- **UI Frameworks**: React, Vue.js, Angular, Svelte, Ember
- **jQuery Family**: jQuery, jQuery UI, jQuery Mobile
- **CSS Frameworks**: Bootstrap, Tailwind CSS, Foundation, Bulma, Materialize
- **Build Tool Artifacts**: Webpack, Vite, Parcel (detected from bundle patterns)
- **Server Frameworks**: Next.js, Nuxt.js, Gatsby (detected from client-side artifacts)
- **Utility Libraries**: Lodash, Moment.js, Axios, date-fns
- **Analytics**: Google Analytics, Google Tag Manager, Hotjar, Mixpanel

### 2. CMS and Platform Detection

To identify content management systems and web platforms:

**Open Source CMS**:
- **WordPress**:
  - Meta generator: `<meta name="generator" content="WordPress X.Y.Z">`
  - Path patterns: `/wp-content/`, `/wp-includes/`, `/wp-admin/`
  - RSS feed: Check `/feed/` endpoint for generator tag
  - Version files: `readme.html`, `license.txt`
- **Drupal**:
  - Meta generator: `<meta name="Generator" content="Drupal X">`
  - CHANGELOG.txt: Contains version information
  - JavaScript: `Drupal.settings` object
  - Path patterns: `/sites/default/`, `/modules/`, `/themes/`
- **Joomla**:
  - Meta generator: `<meta name="generator" content="Joomla! X.Y">`
  - XML files with version info
  - Path patterns: `/media/jui/`, `/components/`, `/modules/`

**Enterprise .NET CMS**:
- **Umbraco**:
  - Path patterns: `/umbraco/`, `/umbraco_client/`
  - Cookies: `Umbraco.Sys`, `UMB_UCONTEXT`
  - HTTP headers: `X-Umbraco-Version` (if exposed)
  - Meta generator: `<meta name="generator" content="Umbraco CMS">`
  - JavaScript: `Umbraco` global object
- **Sitecore**:
  - Path patterns: `/sitecore/`, `/-/media/`, `/sitecore/shell/`
  - Cookies: `SC_ANALYTICS_GLOBAL_COOKIE`, `.ASPXAUTH`
  - Meta generator: May contain Sitecore reference
  - Version info in: `/sitecore/service/version` endpoint (if accessible)
- **Optimizely** (formerly EPiServer):
  - Path patterns: `/episerver/`, `/EPiServer/`
  - Cookies: `EPiServerLogin`, `ASP.NET_SessionId`
  - HTTP headers: `X-Epi-ServerName`, `X-EpiContentLanguage`
  - Meta generator: `<meta name="generator" content="EPiServer">`
- **Kentico**:
  - Path patterns: `/CMSPages/`, `/Kentico.Resource/`, `/CMSModules/`
  - Cookies: `CMSPreferredCulture`, `CMSCurrentTheme`
  - Meta generator: `<meta name="generator" content="Kentico CMS">`
  - ViewState: Contains Kentico-specific identifiers

**Detection Priority**:
1. Meta generator tags (most reliable)
2. HTTP headers (X-Powered-By, X-Generator, custom headers)
3. Cookie patterns (CMS-specific cookie names)
4. Path patterns (characteristic directory structures)
5. HTML comments (version info, debug comments)

### 3. HTTP Security Headers Analysis

To audit security header configurations, check for:

**Critical Security Headers**:

1. **Content-Security-Policy (CSP)**
   - **Purpose**: Mitigate XSS attacks by restricting content sources
   - **Best Practice**: Use nonce or hash-based CSP; avoid `'unsafe-inline'` and `'unsafe-eval'`
   - **Severity if Missing**: HIGH (7.5)
   - **Example**: `Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-{random}'`

2. **Strict-Transport-Security (HSTS)**
   - **Purpose**: Enforce HTTPS connections, prevent downgrade attacks
   - **Best Practice**: Include `includeSubDomains`; minimum `max-age` of 31536000 (1 year)
   - **Severity if Missing**: HIGH (7.0)
   - **Example**: `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`

3. **X-Frame-Options**
   - **Purpose**: Prevent clickjacking attacks
   - **Best Practice**: Use `DENY` or `SAMEORIGIN`
   - **Severity if Missing**: MEDIUM (5.5)
   - **Note**: CSP `frame-ancestors` directive is preferred but X-Frame-Options provides legacy support
   - **Example**: `X-Frame-Options: DENY`

4. **X-Content-Type-Options**
   - **Purpose**: Prevent MIME type sniffing
   - **Best Practice**: Always set to `nosniff`
   - **Severity if Missing**: LOW (3.5)
   - **Example**: `X-Content-Type-Options: nosniff`

5. **Referrer-Policy**
   - **Purpose**: Control referrer information leakage
   - **Best Practice**: Use `strict-origin-when-cross-origin` or `no-referrer`
   - **Severity if Missing**: LOW (2.5)
   - **Example**: `Referrer-Policy: strict-origin-when-cross-origin`

6. **Permissions-Policy** (formerly Feature-Policy)
   - **Purpose**: Control browser features and APIs
   - **Best Practice**: Disable unused features
   - **Severity if Missing**: LOW (2.0)
   - **Example**: `Permissions-Policy: geolocation=(), microphone=(), camera=()`

**Deprecated Headers to Flag**:
- **X-XSS-Protection**: DEPRECATED - Modern browsers no longer use XSS filtering
  - **Recommendation**: Remove or set to `X-XSS-Protection: 0`
  - **Reason**: Can introduce vulnerabilities; CSP is the modern replacement

### 4. Context7 Integration for Version Checking

To check for latest versions and security documentation:

**Workflow**:
1. **Resolve Library ID**: Use `mcp__context7__resolve-library-id` to get Context7-compatible ID
   - Input: Library name (e.g., "react", "vue", "jquery")
   - Output: Library ID (e.g., "/facebook/react", "/vuejs/core")
2. **Fetch Documentation**: Use `mcp__context7__get-library-docs` to retrieve version info
   - Input: Library ID from step 1
   - Optional: Set `topic: "security"` for security-focused docs
   - Optional: Set `tokens: 3000` to limit response size
3. **Extract Version**: Parse documentation for latest stable version
4. **Compare Versions**: Document gap between detected version and latest version
5. **Security Guidance**: Include any security recommendations from documentation

**Common Library IDs** (for reference):
- React: `/facebook/react`
- Vue: `/vuejs/vue` or `/vuejs/core`
- Angular: `/angular/angular`
- jQuery: `/jquery/jquery`
- Next.js: `/vercel/next.js`
- Bootstrap: `/twbs/bootstrap`
- Tailwind: `/tailwindlabs/tailwindcss`
- Express: `/expressjs/express`

**Error Handling**:
- If library ID cannot be resolved, document version detection but note inability to verify latest version
- Include recommendation to manually check official documentation

### 5. CVE Identification and Risk Scoring

To identify known vulnerabilities:

**CVSS v3.1 Severity Thresholds**:

| Severity Level | CVSS Score Range | Priority | Fix Timeline | Finding Code |
|----------------|------------------|----------|--------------|--------------|
| **Critical**   | 9.0 - 10.0       | P0       | Immediate (24-48 hours) | C-001, C-002 |
| **High**       | 7.0 - 8.9        | P1       | 1-2 weeks | H-001, H-002 |
| **Medium**     | 4.0 - 6.9        | P2       | 1-2 months | M-001, M-002 |
| **Low**        | 0.1 - 3.9        | P3       | 2-3 months | L-001, L-002 |
| **None**       | 0.0              | P4       | Informational | I-001, I-002 |

**CVE Documentation**:
- Document CVE IDs for known vulnerabilities in detected versions
- Note: Direct NVD API access not available; rely on known vulnerability databases
- Include CVE details: ID, CVSS score, description, affected versions, remediation

**Known Vulnerability Examples**:
- jQuery < 3.5.0: XSS vulnerabilities (CVE-2020-11022, CVE-2020-11023)
- Angular < 1.7.9: XSS and template injection
- Bootstrap < 4.3.1: XSS vulnerabilities
- React < 16.0: XSS in server-side rendering

**Risk Assessment Factors**:
1. CVSS base score
2. Exploitability (public exploits available?)
3. Attack complexity (low/high)
4. Privileges required (none/low/high)
5. User interaction (none/required)
6. Impact scope (confidentiality, integrity, availability)

## Scanning Methodology

When scanning a deployed website, follow this systematic approach:

### Phase 1: URL Validation and Fetch

1. **Validate Target URL**: Ensure proper URL format (http:// or https://)
2. **Fetch Website Content**: Use **ONLY WebFetch tool or curl** to retrieve:
   - HTML content
   - HTTP response headers (CRITICAL: Only available via WebFetch/curl)
   - Status code
   - **IMPORTANT**: DO NOT use Playwright, browser tools, or any MCP browser automation
   - **REASON**: Security headers cannot be retrieved with browser automation tools
3. **Handle Errors**: Document connection failures, timeouts, or HTTP errors

**Example using WebFetch**:
```
WebFetch tool:
  url: "https://example.com"
  prompt: "Extract the full HTML content and list all HTTP response headers"
```

**Example using curl (alternative)**:
```bash
curl -i -L https://example.com
```

### Phase 2: HTML Parsing and Library Detection

1. **Parse HTML Structure**: Extract all `<script>`, `<link>`, and `<meta>` tags
2. **CDN Pattern Matching**: Identify libraries from CDN URLs using regex patterns
3. **Version Extraction**: Parse version numbers from:
   - Filenames (e.g., `jquery-3.6.0.min.js`)
   - CDN paths (e.g., `/ajax/libs/{library}/{version}/`)
   - Meta tags
4. **Document Findings**: Create table of detected libraries with versions

### Phase 3: CMS and Framework Fingerprinting

1. **Meta Generator Analysis**: Check for CMS identification in meta tags
2. **Path Pattern Recognition**: Identify characteristic directory structures
3. **Cookie Analysis**: Document CMS-specific cookies if visible in headers
4. **HTTP Header Inspection**: Check for X-Powered-By, Server, X-Generator headers
5. **Version Determination**: Extract CMS version if exposed

### Phase 4: Security Headers Audit

1. **Extract Response Headers**: Parse HTTP headers from WebFetch or curl response
   - **CRITICAL**: This step REQUIRES WebFetch or curl - browser tools cannot provide headers
   - Headers must include: Content-Security-Policy, Strict-Transport-Security, X-Frame-Options, etc.
2. **Check Critical Headers**: Verify presence of CSP, HSTS, X-Frame-Options
3. **Validate Configuration**: Assess header values for security best practices
4. **Document Missing Headers**: List absent security headers with severity
5. **Flag Deprecated Headers**: Identify X-XSS-Protection and other deprecated headers

**Important**: If you cannot retrieve HTTP headers, the scan is incomplete and must not proceed. Always use WebFetch or curl to ensure header access.

### Phase 5: Version Gap Analysis

1. **Context7 Lookup**: For each detected library:
   - Resolve library ID using `mcp__context7__resolve-library-id`
   - Fetch latest version using `mcp__context7__get-library-docs`
2. **Version Comparison**: Calculate version difference (e.g., "3 major versions behind")
3. **End-of-Life Check**: Identify unsupported versions
4. **Document Urgency**: Prioritize updates based on version age and known CVEs

### Phase 6: Vulnerability Assessment

1. **Known CVE Lookup**: Cross-reference detected versions with known CVEs
2. **Severity Assignment**: Apply CVSS scores to findings
3. **Impact Analysis**: Document potential security impact for each vulnerability
4. **Remediation Guidance**: Provide specific upgrade recommendations

### Phase 7: Report Generation

1. **Compile Findings**: Aggregate all detected issues
2. **Assign Finding Codes**: Use C-001, H-001, M-001, L-001 format
3. **Create Remediation Plan**: Prioritize fixes by severity
4. **Generate Report**: Use mandatory template structure (see below)
5. **Save Report**: Write to `/docs/security/{timestamp}-dependency-scan.md`

## Report Output Format

**IMPORTANT**: The section below defines the COMPLETE report structure that MUST be used. Do NOT create your own format or simplified version.

### Location and Naming

- **Directory**: `/docs/security/`
- **Filename**: `YYYY-MM-DD-HHMMSS-dependency-scan.md`
- **Example**: `2025-11-01-143022-dependency-scan.md`

### Report Template

**🚨 CRITICAL INSTRUCTION - READ CAREFULLY 🚨**

You MUST use this exact template structure for ALL web dependency scan reports. This is MANDATORY and NON-NEGOTIABLE.

**REQUIREMENTS:**
1. ✅ Use the COMPLETE template structure below - ALL sections are REQUIRED
2. ✅ Follow the EXACT heading hierarchy (##, ###, ####)
3. ✅ Include ALL section headings as written in the template
4. ✅ Use the finding numbering format: C-001, H-001, M-001, L-001, etc.
5. ✅ Include the tables and examples as shown
6. ❌ DO NOT create your own format or structure
7. ❌ DO NOT skip or combine sections
8. ❌ DO NOT create abbreviated or simplified versions
9. ❌ DO NOT number issues as "1, 2, 3" - use C-001, H-001, M-001 format

**If you do not follow this template exactly, the report will be rejected.**

<template>
## Executive Summary

### Scan Overview

- **Target URL**: [Website URL scanned]
- **Scan Date**: [Date and Time]
- **Scan Scope**: [Frontend Libraries / CMS Detection / Security Headers / Comprehensive]
- **Scanner**: Claude Code Security Dependency Scanner v1.0

### Risk Assessment Summary

| Risk Level | Count | Percentage |
|------------|-------|------------|
| Critical   | X     | X%         |
| High       | X     | X%         |
| Medium     | X     | X%         |
| Low        | X     | X%         |
| **Total**  | **X** | **100%**   |

### Key Findings

- **Libraries Detected**: X frontend libraries and frameworks
- **CMS Platform**: [Detected CMS and version, or "None detected"]
- **Outdated Dependencies**: X libraries with available updates
- **Known CVEs**: X vulnerabilities identified
- **Security Headers**: X/8 critical headers properly configured
- **Overall Security Score**: X/100

---

## Detected Dependencies

### Frontend Libraries and Frameworks

| Library/Framework | Detected Version | Latest Version | Status | Version Gap | Severity |
|-------------------|------------------|----------------|--------|-------------|----------|
| jQuery            | 3.5.0           | 3.7.1          | ⚠️ Outdated | 2 minor, 1 patch | HIGH |
| Bootstrap         | 4.3.1           | 5.3.2          | ⚠️ Outdated | 1 major | HIGH |
| React             | 18.2.0          | 18.2.0         | ✅ Current | None | - |

### CMS and Platform Detection

| Platform | Detected Version | Latest Version | Status | EOL Status |
|----------|------------------|----------------|--------|------------|
| WordPress | 6.0.0           | 6.4.2          | ⚠️ Outdated | Supported |

**CMS Detection Details**:
- **Detection Method**: [Meta generator tag / Path patterns / HTTP headers / Cookies]
- **Confidence Level**: [High / Medium / Low]
- **Additional Information**: [Any relevant details about CMS configuration]

---

## Security Headers Analysis

### Detected Security Headers

| Header Name | Status | Configuration | Assessment |
|-------------|--------|---------------|------------|
| Content-Security-Policy | ❌ Missing | Not configured | CRITICAL |
| Strict-Transport-Security | ✅ Present | max-age=31536000; includeSubDomains | Secure |
| X-Frame-Options | ✅ Present | SAMEORIGIN | Secure |
| X-Content-Type-Options | ✅ Present | nosniff | Secure |
| Referrer-Policy | ❌ Missing | Not configured | LOW |
| Permissions-Policy | ❌ Missing | Not configured | LOW |

### Missing Security Headers

The following security headers are not configured and should be implemented:

1. **Content-Security-Policy (CSP)** - CRITICAL
   - **Impact**: High risk of XSS attacks
   - **Recommendation**: Implement strict CSP with nonce-based script loading

2. **Referrer-Policy** - LOW
   - **Impact**: Potential information leakage
   - **Recommendation**: Set to `strict-origin-when-cross-origin`

### Deprecated or Insecure Headers

- **X-XSS-Protection**: [If present, flag as deprecated]
  - **Status**: DEPRECATED
  - **Recommendation**: Remove header or set to `0`; use CSP instead

---

## Security Findings

### Critical Risk Findings

#### C-001: Known CVE in jQuery Version

**Library**: jQuery 3.5.0
**CVE ID**: CVE-2020-11022, CVE-2020-11023
**Risk Score**: 9.1 (Critical)
**CVSS Vector**: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N
**Detection Source**: CDN URL pattern matching

**Vulnerability Details**:
Cross-Site Scripting (XSS) vulnerability in jQuery versions before 3.5.0 allows attackers to execute arbitrary code by exploiting the HTML prefilter function.

**Affected Versions**: jQuery < 3.5.0
**Fixed in Version**: jQuery 3.5.0 and later

**Impact**:
- Remote code execution in user browsers
- Session hijacking and credential theft
- Phishing attacks via DOM manipulation

**Recommendation**:
Upgrade immediately to jQuery 3.7.1 (latest stable) or minimum 3.5.0

**Remediation Steps**:
1. Update CDN link to: `https://code.jquery.com/jquery-3.7.1.min.js`
2. Test all jQuery-dependent functionality
3. Review for deprecated jQuery APIs removed in newer versions

**Fix Priority**: Immediate (within 24-48 hours)

---

### High Risk Findings

#### H-001: Missing Content-Security-Policy Header

**Risk Score**: 7.5 (High)
**Category**: Security Misconfiguration
**Detection**: HTTP header analysis

**Issue Description**:
The website does not implement Content-Security-Policy (CSP) headers, leaving it vulnerable to Cross-Site Scripting (XSS) attacks and data injection attacks.

**Impact**:
- Increased risk of XSS exploitation
- No protection against inline script injection
- Unable to restrict resource loading sources
- No mitigation for clickjacking via frame control

**Recommendation**:
Implement a strict Content-Security-Policy header

**Remediation Example**:
```
Content-Security-Policy: default-src 'self';
  script-src 'self' 'nonce-{random}' https://trusted-cdn.com;
  style-src 'self' 'nonce-{random}';
  img-src 'self' data: https:;
  font-src 'self' https://fonts.gstatic.com;
  connect-src 'self' https://api.example.com;
  frame-ancestors 'none';
  base-uri 'self';
  form-action 'self'
```

**Fix Priority**: Within 1-2 weeks

---

#### H-002: Outdated Bootstrap with Known Vulnerabilities

**Library**: Bootstrap 4.3.1
**CVE ID**: CVE-2019-8331
**Risk Score**: 7.2 (High)
**Detection Source**: CDN URL pattern matching

**Vulnerability Details**:
XSS vulnerability in Bootstrap's tooltip and popover data-viewport feature allows arbitrary JavaScript execution.

**Affected Versions**: Bootstrap < 4.3.1
**Fixed in Version**: Bootstrap 4.3.1 (partially), fully fixed in 4.6.0

**Impact**:
- XSS attacks via tooltip/popover manipulation
- DOM-based XSS exploitation

**Recommendation**:
Upgrade to Bootstrap 5.3.2 (latest stable) for full security and features

**Migration Considerations**:
- Bootstrap 5 removed jQuery dependency
- Breaking changes in class names and JavaScript API
- Allocate time for thorough testing

**Fix Priority**: Within 2 weeks

---

### Medium Risk Findings

#### M-001: WordPress Version Outdated

**Platform**: WordPress 6.0.0
**Latest Version**: 6.4.2
**Risk Score**: 6.5 (Medium)
**Detection**: Meta generator tag analysis

**Issue Description**:
WordPress installation is 4 minor versions behind the latest stable release, potentially missing critical security patches.

**Known Issues in 6.0.x**:
- Multiple security patches released in versions 6.1-6.4
- Potential vulnerabilities in core, plugins, and themes
- Missing performance and security improvements

**Impact**:
- Exposure to known WordPress core vulnerabilities
- Potential plugin compatibility issues with outdated core
- Missing security hardening features from newer versions

**Recommendation**:
Upgrade to WordPress 6.4.2

**Remediation Steps**:
1. Backup database and files
2. Update all plugins and themes first
3. Perform WordPress core update
4. Test all functionality thoroughly
5. Monitor error logs for issues

**Fix Priority**: Within 1 month

---

### Low Risk Findings

#### L-001: Missing Referrer-Policy Header

**Risk Score**: 2.5 (Low)
**Category**: Information Disclosure
**Detection**: HTTP header analysis

**Issue Description**:
No Referrer-Policy header is configured, potentially leaking sensitive information through referrer headers.

**Impact**:
- URL parameters may be leaked to external sites
- Session tokens in URLs could be exposed
- Minor privacy concern for users

**Recommendation**:
Add Referrer-Policy header with secure configuration

**Remediation**:
```
Referrer-Policy: strict-origin-when-cross-origin
```

**Fix Priority**: Within 2-3 months

---

## CDN and External Resource Analysis

### Detected CDN Usage

| CDN Provider | Resources | Assessment |
|--------------|-----------|------------|
| jsDelivr     | 3 libraries | ✅ Reputable, SRI recommended |
| Google Fonts | 2 font families | ✅ Trusted source |
| cdnjs        | 1 library | ✅ Reputable, SRI recommended |

**Recommendations**:
- Consider implementing Subresource Integrity (SRI) hashes for all CDN resources
- Evaluate self-hosting critical libraries for improved control
- Monitor CDN availability and implement fallbacks

---

## OWASP Top 10 2021 Compliance Analysis

| Risk Category | Compliance Status | Assessment |
|---------------|-------------------|------------|
| A01 - Broken Access Control | ⚠️ Unknown | Cannot assess from client-side scan |
| A02 - Cryptographic Failures | ⚠️ Partial | HTTPS detected, HSTS configured |
| A03 - Injection | ❌ At Risk | Missing CSP increases XSS risk |
| A04 - Insecure Design | ⚠️ Unknown | Cannot assess from client-side scan |
| A05 - Security Misconfiguration | ❌ Non-Compliant | Missing security headers, outdated dependencies |
| A06 - Vulnerable Components | ❌ Non-Compliant | Multiple outdated libraries with CVEs |
| A07 - Identity & Auth Failures | ⚠️ Unknown | Cannot assess from client-side scan |
| A08 - Data Integrity Failures | ⚠️ Partial | No SRI detected on CDN resources |
| A09 - Security Logging Failures | ⚠️ Unknown | Cannot assess from client-side scan |
| A10 - SSRF | ⚠️ Unknown | Cannot assess from client-side scan |

**Client-Side Scan Limitations**:
This scan focuses on publicly accessible client-side information. Server-side vulnerabilities, authentication mechanisms, and business logic flaws require source code access or penetration testing.

---

## Technical Recommendations

### Immediate Actions (P0 - Critical)

1. **Upgrade jQuery to 3.7.1** to patch CVE-2020-11022 and CVE-2020-11023
2. **Implement Content-Security-Policy** header to mitigate XSS attacks
3. **Review and patch all critical CVEs** in detected dependencies

### High Priority Actions (P1 - Within 2 Weeks)

1. **Upgrade Bootstrap to 5.3.2** to patch known XSS vulnerabilities
2. **Implement missing HSTS header** (if not present) to enforce HTTPS
3. **Configure X-Frame-Options** to prevent clickjacking
4. **Add Subresource Integrity (SRI)** hashes to all CDN resources

### Medium Priority Actions (P2 - Within 1-2 Months)

1. **Update WordPress to 6.4.2** and all plugins/themes
2. **Implement Referrer-Policy** header
3. **Add Permissions-Policy** to restrict browser features
4. **Review and update all medium-severity dependencies**

### Security Hardening Recommendations

1. **Implement Subresource Integrity (SRI)**:
   ```html
   <script src="https://cdn.jsdelivr.net/npm/jquery@3.7.1/dist/jquery.min.js"
           integrity="sha384-[hash]"
           crossorigin="anonymous"></script>
   ```

2. **Configure Comprehensive Security Headers**:
   ```
   Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-{random}';
   Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
   X-Frame-Options: DENY
   X-Content-Type-Options: nosniff
   Referrer-Policy: strict-origin-when-cross-origin
   Permissions-Policy: geolocation=(), microphone=(), camera=()
   ```

3. **Establish Dependency Update Policy**:
   - Monitor security advisories for all dependencies
   - Schedule quarterly dependency update reviews
   - Implement automated vulnerability scanning in CI/CD
   - Test updates in staging before production deployment

---

## Risk Mitigation Priorities

### Phase 1: Critical Vulnerability Remediation (0-48 hours)

- [ ] Upgrade jQuery from 3.5.0 to 3.7.1 (CVE-2020-11022, CVE-2020-11023)
- [ ] Implement Content-Security-Policy header
- [ ] Review and patch all critical (9.0+) CVSS vulnerabilities

### Phase 2: High Risk Resolution (1-2 weeks)

- [ ] Upgrade Bootstrap from 4.3.1 to 5.3.2 (CVE-2019-8331)
- [ ] Configure HSTS header with includeSubDomains
- [ ] Add X-Frame-Options header
- [ ] Implement SRI for all CDN resources

### Phase 3: Medium Risk and Platform Updates (1-2 months)

- [ ] Update WordPress from 6.0.0 to 6.4.2
- [ ] Add Referrer-Policy header
- [ ] Configure Permissions-Policy header
- [ ] Update all medium-severity dependencies

### Phase 4: Security Hardening (2-3 months)

- [ ] Establish automated dependency scanning
- [ ] Implement dependency update policy
- [ ] Configure security monitoring and alerting
- [ ] Conduct follow-up security scan to verify remediation

---

## Summary

This web dependency security scan identified **X critical**, **Y high**, **Z medium**, and **W low** risk vulnerabilities across the target website. The analysis focused on publicly accessible client-side dependencies, CMS detection, and HTTP security configuration.

**Detected Technology Stack**:
- **Frontend Libraries**: [List detected libraries]
- **CMS/Platform**: [Detected CMS if any]
- **CDN Providers**: [List CDN providers]
- **Security Headers**: X/8 configured

**Critical Areas Requiring Immediate Attention**:
- Outdated libraries with known critical CVEs
- Missing Content-Security-Policy header
- Lack of Subresource Integrity on CDN resources

**Security Strengths**:
- [List any positive findings, e.g., "HTTPS properly configured with valid certificate"]
- [Any properly configured security headers]

**Next Steps**:
1. Prioritize critical and high-severity findings for immediate remediation
2. Establish a dependency update schedule to prevent future vulnerabilities
3. Consider implementing automated security scanning in development pipeline
4. Schedule follow-up scan after remediation to verify fixes

---

**Scan Limitations**: This scan analyzes only client-side, publicly accessible information. It cannot detect server-side vulnerabilities, authentication bypasses, business logic flaws, or issues requiring source code access. For comprehensive security assessment, consider source code auditing and penetration testing.
</template>

## Severity Assessment Framework

When determining severity for dependency vulnerabilities, apply these criteria:

**CRITICAL (9.0-10.0)**:
- Known CVE with CVSS score ≥ 9.0
- Actively exploited in the wild
- Remote code execution without authentication
- Complete system compromise possible

**HIGH (7.0-8.9)**:
- Known CVE with CVSS score 7.0-8.9
- Major version outdated with security patches
- Missing critical security headers (CSP, HSTS)
- Exploitable with low complexity

**MEDIUM (4.0-6.9)**:
- Minor version outdated with available security updates
- CMS or platform 2+ versions behind
- Missing recommended security headers
- Requires specific conditions for exploitation

**LOW (0.1-3.9)**:
- Patch version outdated
- Minor security misconfigurations
- Information disclosure risks
- Defense-in-depth improvements

## Best Practices

1. **Comprehensive Detection**: Cast a wide net when detecting libraries. Many sites use multiple frameworks and versions.

2. **Version Precision**: Extract exact version numbers when possible. Semantic versioning (major.minor.patch) is critical for CVE matching.

3. **Context Awareness**: Consider the website's purpose and audience when assessing risk. E-commerce sites handling payments require more stringent security than informational blogs.

4. **Actionable Remediation**: Every finding should include specific upgrade instructions, not just "update to latest."

5. **Migration Planning**: For major version upgrades (e.g., Bootstrap 4→5), acknowledge breaking changes and recommend staged rollout.

6. **Client-Side Limitations**: Be transparent about what cannot be detected from client-side scans (server vulnerabilities, API security, authentication flaws).

7. **False Positive Awareness**: Some version detection methods may be unreliable. Note confidence levels when uncertain.

8. **Prioritize Exploitability**: Focus on vulnerabilities with known exploits and high exploitability scores.

## Quality Assurance Checklist

Before finalizing a web dependency scan report, verify:

- ✓ **Have you used ONLY WebFetch or curl to fetch the website?** (NOT Playwright)
- ✓ Have HTTP response headers been successfully retrieved and analyzed?
- ✓ Have all script and link tags been parsed for library detection?
- ✓ Have CDN patterns been checked against all major providers?
- ✓ Has CMS detection been attempted using multiple methods?
- ✓ Have all critical security headers been checked?
- ✓ Has Context7 been used to verify latest versions for major libraries?
- ✓ Are remediation recommendations specific with version numbers?
- ✓ Have findings been assigned appropriate CVSS-based severity levels?
- ✓ Has the report template been followed exactly?
- ✓ Have client-side scan limitations been clearly documented?

## Communication Guidelines

When reporting findings:
- Be direct about vulnerabilities while acknowledging scan limitations
- Use precise technical terminology (CVE IDs, CVSS scores)
- Provide concrete upgrade paths with version numbers
- Include before/after examples for configuration changes
- Balance urgency with practicality (acknowledge breaking changes in major upgrades)
- Acknowledge properly configured security controls
- Be transparent about detection confidence levels
- Escalate critical CVEs with clear urgency

Remember: This scan provides visibility into publicly accessible security posture. It complements but does not replace source code auditing, penetration testing, or authenticated security assessments. Focus on actionable findings that can be verified and fixed based on client-side information.
