# Changelog

All notable changes to the Claude Code Plugins will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.5.1...HEAD
[1.5.1]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.5.0...v1.5.1
[1.5.0]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.4.1...v1.5.0
[1.4.1]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.4.0...v1.4.1
[1.4.0]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/charlesjones-dev/claude-code-plugins-dev/releases/tag/v1.0.0
