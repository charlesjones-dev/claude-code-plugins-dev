# Web Dependency Security Scan

Scan a deployed website for outdated dependencies, known CVEs, and security misconfigurations without requiring source code access.

## Instructions

**CRITICAL**: This command MUST NOT accept any arguments. If the user provided any text, URLs, or paths after this command (e.g., `/security-scan-dependencies https://example.com`), you MUST COMPLETELY IGNORE them. Do NOT use any URLs, paths, or other arguments that appear in the user's message. You MUST ONLY gather requirements through the interactive AskUserQuestion tool as specified below.

**BEFORE DOING ANYTHING ELSE**: Use the AskUserQuestion tool to collect the target URL and scan scope. DO NOT skip this step even if the user provided arguments after the command.

### Phase 1: Get Target URL

Use the **AskUserQuestion tool** to collect the target website URL:

```
Question: "What is the URL of the website you want to scan?"
Header: "Target URL"
Options:
  - Provide text input field for URL entry
```

**URL Validation**:
- Ensure URL includes protocol (http:// or https://)
- Accept both HTTP and HTTPS URLs
- If user provides URL without protocol, prepend https://

### Phase 2: Configure Scan Scope

Use the **AskUserQuestion tool** to determine scan scope:

```
Question: "What would you like to scan for?"
Header: "Scan Scope"
multiSelect: true
Options:
  1. "Frontend libraries" - "jQuery, React, Vue, Angular, Bootstrap, Tailwind, etc."
  2. "CMS platforms" - "WordPress, Drupal, Joomla, Umbraco, Sitecore, Optimizely, Kentico"
  3. "Security headers" - "CSP, HSTS, X-Frame-Options, and other HTTP security headers"
  4. "All of the above" - "Comprehensive scan covering all categories"
```

**Scope Interpretation**:
- If user selects "All of the above", perform comprehensive scan across all categories
- If user selects multiple specific options, scan only those categories
- If user selects only one option, focus the scan on that specific area

### Phase 3: Invoke Dependency Scanner Agent

Use the **Task tool** with subagent_type "ai-security:security-dependency-scanner" to perform the security scan.

**Important**: Pass the target URL and scan scope in the prompt to the agent.

**🚨 CRITICAL TOOL REQUIREMENT 🚨**:
- The agent MUST use ONLY the **WebFetch tool** or **curl** (via Bash tool) to fetch websites
- DO NOT use Playwright, browser automation, or any other MCP tools for website scanning
- **Reason**: HTTP security headers (especially Content-Security-Policy) can ONLY be retrieved via HTTP requests using WebFetch or curl. Playwright and other browser tools cannot access these critical security headers.
- Using the wrong tool will result in incomplete security header analysis

**Example Task Tool Invocation**:
```
Task tool:
  subagent_type: "ai-security:security-dependency-scanner"
  description: "Scan website for dependencies"
  prompt: "
    Please scan the following website for security vulnerabilities:

    Target URL: [user-provided URL]
    Scan Scope: [user-selected scope]

    Perform a comprehensive security dependency scan including:
    - [Based on scope: Frontend library detection and version analysis]
    - [Based on scope: CMS platform detection and version checking]
    - [Based on scope: HTTP security headers audit]
    - Context7 integration for latest version verification
    - Known CVE identification for detected libraries
    - Security risk assessment with CVSS scoring

    Generate a detailed security report following the security-dependency-scanning
    skill's mandatory template and save it to /docs/security/{timestamp}-dependency-scan.md
  "
```

**Agent Responsibilities**:
The ai-security:security-dependency-scanner agent will:
1. Load the security-dependency-scanning skill
2. Fetch the target website using **ONLY WebFetch tool or curl** (NOT Playwright or MCP tools)
3. Parse HTML and detect dependencies based on scope
4. Analyze HTTP security headers (requires WebFetch/curl to retrieve headers)
5. Use Context7 to check for latest versions
6. Identify known CVEs in detected versions
7. Generate comprehensive security report with findings
8. Save report to `/docs/security/YYYY-MM-DD-HHMMSS-dependency-scan.md`

### Phase 4: Report Completion

After the agent completes its analysis, inform the user:

```
✅ Web dependency security scan completed!

📄 Report saved to: /docs/security/{timestamp}-dependency-scan.md

Summary:
- Libraries Detected: X
- CMS Platform: [Detected CMS or "None"]
- Vulnerabilities Found: X (Y critical, Z high)
- Security Headers: X/8 configured

Please review the detailed report for:
- Complete list of detected dependencies and versions
- Known CVEs with CVSS scores and remediation steps
- Security header analysis and recommendations
- Prioritized risk mitigation roadmap

Next steps:
1. Review critical and high-severity findings first
2. Plan remediation based on the prioritized roadmap
3. Test updates in staging environment before production
4. Schedule follow-up scan after remediation
```

### Important Notes

**Scan Capabilities**:
- ✅ Detects frontend libraries from HTML, scripts, and CDN URLs
- ✅ Identifies CMS platforms from meta tags, paths, cookies, and headers
- ✅ Analyzes HTTP security headers and configurations
- ✅ Checks for known CVEs in detected library versions
- ✅ Uses Context7 to verify latest versions

**Scan Limitations**:
- ❌ Cannot detect server-side vulnerabilities without source code access
- ❌ Cannot assess authentication or authorization mechanisms
- ❌ Cannot detect business logic flaws
- ❌ Cannot scan password-protected or authenticated areas
- ❌ Limited to publicly accessible client-side information

**Use Cases**:
- Third-party website security assessment
- Pre-acquisition technical due diligence
- Client-side dependency auditing
- Supply chain security analysis
- Comparison with client's internal security scan tools

**Ethical Considerations**:
- Only scan websites you have permission to analyze
- This tool performs passive analysis of publicly accessible information
- No intrusive testing or exploitation attempts are performed
- Suitable for authorized security assessments and pentesting engagements

**Comparison with /security-audit**:
- `/security-audit`: Analyzes source code in current directory for vulnerabilities
- `/security-scan-dependencies`: Scans deployed website URL without source code access
- Use `/security-audit` for your own codebases
- Use `/security-scan-dependencies` for analyzing deployed websites
