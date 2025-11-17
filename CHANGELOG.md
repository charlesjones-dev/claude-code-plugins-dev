# Changelog

All notable changes to the Claude Code Plugins will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.5.4] - 2025-01-17

### Fixed

#### AI-Security Plugin (v1.3.2)

- **Fixed `/security-scan-dependencies` to require WebFetch or curl for HTTP header retrieval**
  - Updated command and skill documentation to explicitly prohibit Playwright or MCP browser tools
  - Added critical tool requirement section explaining that HTTP security headers (especially Content-Security-Policy) can ONLY be retrieved via WebFetch or curl
  - Browser automation tools cannot access raw HTTP response headers needed for security header analysis
  - Added "Required Tools" section to `security-dependency-scanning` skill with approved/prohibited tool lists
  - Enhanced scanning methodology with explicit WebFetch/curl usage examples
  - Updated quality assurance checklist to verify correct tool usage
  - Prevents incomplete security scans due to missing HTTP header analysis

## [1.5.3] - 2025-01-04

### Fixed

#### Marketplace

- Updated plugin versions in `marketplace.json` to match the versions in each `plugin.json` manifest

#### AI-Accessibility Plugin (v1.1.1)

- Accessibility scanning command `/accessibility-audit` now properly checks to see if Playwright MCP is installed before proceeding with an accessibility audit

## [1.5.2] - 2025-01-04

### Changed

#### AI-Accessibility Plugin (v1.1.0)

- **Added URL Accessibility Scanning** with optional Playwright MCP integration
  - New "a URL" option in scope selection for scanning live websites
  - Interactive Playwright MCP setup with automatic `.mcp.json` configuration
  - OS detection for Windows vs Linux/Mac Playwright configuration
  - Visual accessibility testing when Playwright MCP is available:
    - Real-time color contrast measurements of rendered elements
    - Visual verification of focus indicators
    - Accessibility tree analysis as perceived by assistive technologies
    - Keyboard navigation testing on live pages
    - Touch target size verification with actual pixel measurements
    - Screenshot-based visual accessibility assessment
  - Enhanced audit reports with screenshot evidence for visual findings
  - Screenshots saved to `/docs/accessibility/screenshots/` directory
- Updated `/accessibility-audit` command to support URL scanning with Question 4 for Playwright MCP preference
- Enhanced `accessibility-auditor` agent with dual analysis approach (codebase vs URL with Playwright)
- Enhanced `accessibility-auditing` skill with Playwright MCP expertise and visual testing methodology

#### All Plugins

- **Improved Command Usage Documentation** to prevent erroneous argument passing
  - Added prominent command usage note in README.md clarifying that all commands are invoked without arguments
  - Added explicit "no arguments" instruction to all 13 command files across all plugins
  - Commands now explicitly state they will ignore any passed arguments and prompt interactively for all necessary information
  - Affected plugins:
    - AI-Accessibility (v1.1.0): `/accessibility-audit`
    - AI-Security (v1.3.1): `/security-audit`, `/security-init`, `/security-scan-dependencies`
    - AI-Performance (v1.1.2): `/performance-audit`
    - AI-Git (v1.1.1): `/git-init`, `/git-commit-push`
    - AI-Plugins (v1.2.2): `/plugins-scaffold`
    - AI-ADO (v1.2.2): `/ado-init`, `/ado-create-feature`, `/ado-create-story`, `/ado-create-task`, `/ado-log-story-work`, `/ado-timesheet-report`

## [1.5.1] - 2025-11-01

### Added

#### AI-Security Plugin (v1.3.0)

- `/security-scan-dependencies` command for scanning deployed websites
  - Web dependency security scanning without source code access
  - Interactive URL input and configurable scan scope (libraries, CMS, security headers, or comprehensive)
  - Frontend library detection: jQuery, React, Vue, Angular, Bootstrap, Tailwind, and more via CDN pattern matching
  - CMS platform detection with version identification:
    - Open source: WordPress, Drupal, Joomla
    - Enterprise .NET: Umbraco, Sitecore, Optimizely, Kentico
  - HTTP security headers analysis (CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy)
  - Context7 MCP integration for latest version verification
  - Known CVE identification with CVSS v3.1 severity scoring
  - Timestamped reports with severity-based findings (C-001, H-001, M-001, L-001 format)
  - Hybrid Agent + Skill architecture with `security-dependency-scanner` agent and `security-dependency-scanning` skill
- Use cases: Third-party website assessment, pre-acquisition due diligence, supply chain security analysis

## [1.5.0] - 2025-10-29

### Added

#### AI-Accessibility Plugin (v1.0.0)

- `/accessibility-audit` command with WCAG 2.1/2.2 compliance checking
  - Interactive configuration for WCAG version (2.1/2.2), conformance level (A/AA/AAA), and audit scope
  - Comprehensive pattern detection: semantic HTML, ARIA, keyboard navigation, color contrast, forms, images, screen readers
  - Timestamped reports with severity-based findings, WCAG compliance matrix, and code remediation examples
  - Hybrid Agent + Skill architecture with `accessibility-auditor` agent and `accessibility-auditing` skill

#### Marketplace Documentation

- Added "Note on Audit Plugins" section clarifying audit plugins are developer-focused static code analysis tools
- Emphasizes plugins complement (not replace) runtime testing tools and professional services

### Changed

#### AI-Security Plugin (v1.2.1)

- Standardized audit plugin structure
- Renamed skill from `security-audit` to `security-auditing`
- Reduced command file complexity: 402→80 lines
- Moved comprehensive report templates from command file to SKILL.md file (single source of truth)
- Renamed skill to use 'auditing' suffix

#### AI-Performance Plugin (v1.1.1)

- Standardized audit plugin structure
- Renamed agent from `performance-optimizer` to `performance-auditor`
- Renamed skill from `performance-audit` to `performance-auditing`
- Reduced command file complexity: 471→36 lines
- Moved comprehensive report templates from command file to SKILL.md file (single source of truth)
- Renamed skill to use 'auditing' suffix

## [1.4.1] - 2025-10-24

### Fixed

#### AI-ADO Plugin (v1.2.1)

- **Fixed `/ado-timesheet-report` command**
  - Migrated from non-existent `wit_query` to `wit_my_work_items` MCP tool with client-side filtering
  - Fixed date range filtering to use date-only comparison (prevents time-of-day issues)
  - Fixed day-of-week calculation using platform-specific system commands (PowerShell on Windows, `date` on Mac/Linux)
  - Prevents off-by-one errors in current week date range calculations

### Changed

- Condensed changelog entries across all versions for improved readability while maintaining essential information

## [1.4.0] - 2025-10-23

### Added

#### AI-ADO Plugin (v1.2.0)

- `/ado-timesheet-report` command for generating flexible weekly timesheet reports
  - Flexible task filtering (closed only, worked on only, or both)
  - Multiple date field support (Closed Date or Changed Date)
  - Three grouping modes (by hierarchy, by date, or by date with hierarchy)
  - Three verbosity levels (ID & hours, with titles, or with descriptions)
  - Flexible week definitions (Monday-Sunday or Sunday-Saturday)
  - User filtering (current user or specific team member)
  - Summary statistics and formatted reports with emoji icons

## [1.3.0] - 2025-10-21

### Added

#### AI-ADO Plugin (v1.1.0)

- **AI-Powered Work Item Generation** for `/ado-create-feature`, `/ado-create-story`, and `/ado-create-task` commands
  - AI generates titles, descriptions, persona statements, and acceptance criteria
  - Review and confirmation workflow with override options
  - Analyzes CLAUDE.md for naming conventions and standards
  - Context-aware generation using parent work item details

- `/ado-log-story-work` command for rapid work logging to User Stories
  - Creates tasks with completed hours pre-populated
  - AI-powered or manual task generation
  - Automatic git commit hash detection
  - Optional placeholder task hour subtraction

#### AI-Security Plugin (v1.2.0)

- **Hybrid Agent + Skill Architecture** with `security-audit` skill for optimal context efficiency
  - Progressive disclosure design: metadata loads first, full skill loads only when needed
  - Interactive security audits without consuming context until relevant

#### AI-Performance Plugin (v1.1.0)

- **Hybrid Agent + Skill Architecture** with `performance-audit` skill for optimal context efficiency
  - Progressive disclosure design: metadata loads first, full skill loads only when needed
  - Interactive performance analysis without consuming context until relevant

#### AI-Plugins Plugin (v1.2.0)

- **Plugin Development Skills** for interactive plugin and skill creation
  - New `plugins-scaffold` and `skills-scaffold` skills
  - Auto-loads when creating plugins, manifests, commands, agents, skills, or hooks

#### AI-ADO Plugin (v1.1.0)

- **Azure DevOps Work Items Skill** for MCP-powered work item management
  - New `ado-work-items` skill enforcing proper hierarchy and naming conventions
  - HTML formatting guidance and best practices
  - Auto-loads when using Azure DevOps MCP server tools

### Changed

#### AI-Security Plugin (v1.2.0)

- Converted `security-auditor` agent to lightweight wrapper that loads `security-audit` skill in fresh context

#### AI-Performance Plugin (v1.1.0)

- Converted `performance-optimizer` agent to lightweight wrapper that loads `performance-audit` skill in fresh context

### Fixed

#### AI-ADO Plugin (v1.1.0)

- Fixed `/ado-create-story` to properly set acceptance criteria in dedicated field instead of Description field

## [1.2.0] - 2025-10-20

### Added

#### AI-Git Plugin (v1.1.0)

- `/git-init` command for automated .gitignore generation
  - Intelligent technology detection (Node.js, Python, .NET, Go, Rust, PHP, Ruby, Java, Docker, React/Next.js, Vue, Terraform)
  - Comprehensive pattern generation (80+ patterns based on tech stack)
  - Smart merge strategies with preview and confirmation workflow

#### AI-ADO Plugin (v1.0.0)

- `/ado-init` command for Azure DevOps configuration and MCP server setup
  - Interactive configuration for organization, project, team, area path, and iteration path
  - Automatic CLAUDE.md configuration with work item hierarchy standards
  - Optional `.mcp.json` creation for MCP server integration
  - Cross-platform support with PAT authentication guidance

- `/ado-create-feature` command for creating Feature work items
  - Interactive prompts for title and description with HTML formatting
  - Returns Feature ID with Azure DevOps web link

- `/ado-create-story` command for creating User Story work items
  - Interactive prompts for parent Feature, title, persona statement, acceptance criteria, and story points
  - HTML formatted with Given-When-Then acceptance criteria

- `/ado-create-task` command for creating Task work items
  - Interactive prompts for parent User Story, title, and hour estimate
  - Hour tracking with Original Estimate and Remaining Work fields

### Changed

#### AI-Git Plugin (v1.1.0)

- Renamed `/commit-push` command to `/git-commit-push` for consistency with `/git-init` naming convention

#### AI-Plugins Plugin (v1.1.0)

- Renamed `/scaffold-plugin` command to `/plugins-scaffold` for consistency with plugin naming convention

## [1.1.0] - 2025-10-19

### Added

#### AI-Security Plugin (v1.1.0)

- `/security-init` command for automated security settings initialization
  - Intelligent technology detection with comprehensive file denial patterns (40-60+ based on tech stack)
  - Smart merge strategies with preview and confirmation workflow

### Changed

#### AI-Security Plugin (v1.1.0)

- Enhanced `/security-audit` with pre-audit configuration check recommending `/security-init` for users with fewer than 4 deny rules

## [1.0.1] - 2025-10-17

### Added

#### AI-Plugins Plugin (v1.0.0)

- Initial release with `/scaffold-plugin` command for interactive plugin scaffolding (later renamed to `/plugins-scaffold`)
  - AI-assisted plugin creation with automatic directory structure, metadata, and marketplace registration

## [1.0.0] - 2025-10-17

### Added

#### Marketplace

- Initial release of Claude Code Plugins marketplace with `.claude-plugin/marketplace.json` metadata system
- Support for slash commands, agents, and skills

#### AI-Git Plugin (v1.0.0)

- `/commit-push` command for automated git commit and push (later renamed to `/git-commit-push`)
  - Intelligent commit message generation following repository conventions
  - Clean commit messages without AI attribution

#### AI-Security Plugin (v1.0.0)

- `/security-audit` command with `security-auditor` agent
  - OWASP Top 10 2021 compliance checking and vulnerability detection
  - Timestamped audit reports with risk scoring and remediation guidance

#### AI-Performance Plugin (v1.0.0)

- `/performance-audit` command with `performance-optimizer` agent
  - Performance anti-pattern detection and database optimization recommendations
  - Timestamped audit reports with impact scoring and optimization roadmap

### Documentation

- README.md, CLAUDE.md, individual plugin READMEs, and MIT license

[Unreleased]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.5.4...HEAD
[1.5.4]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.5.3...v1.5.4
[1.5.3]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.5.2...v1.5.3
[1.5.2]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.5.1...v1.5.2
[1.5.1]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.5.0...v1.5.1
[1.5.0]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.4.1...v1.5.0
[1.4.1]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.4.0...v1.4.1
[1.4.0]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/charlesjones-dev/claude-code-plugins-dev/releases/tag/v1.0.0
