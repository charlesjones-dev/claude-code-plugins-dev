# Changelog

All notable changes to the Claude Code Plugins will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2025-10-17

### Added

#### AI-Plugins Plugin (v1.0.0)

- Initial release of AI-Plugins plugin for managing Claude Code plugins
- Plugin management and discovery capabilities

## [1.0.0] - 2025-10-17

### Added

#### Marketplace

- Initial release of Claude Code Plugins marketplace
- Marketplace metadata system with `.claude-plugin/marketplace.json`
- Flat plugin directory structure for easy management
- Support for slash commands, agents, and skills

#### AI-Git Plugin (v1.0.0)

- `/commit-push` command for automated git commit and push workflow
- Intelligent commit message generation following repository conventions
- Git status analysis and file staging
- Automatic detection of conventional commit patterns
- Push to remote with branch tracking
- Clean commit messages without AI attribution

#### AI-Security Plugin (v1.0.0)

- `/security-audit` command for comprehensive security analysis
- `security-auditor` agent with deep security expertise
- OWASP Top 10 2021 compliance checking
- Vulnerability detection for SQL injection, XSS, authentication issues, and more
- Timestamped security audit reports in `/docs/security/` directory
- Architecture security assessment capabilities
- Code remediation examples with before/after comparisons
- Risk scoring and prioritized remediation guidance
- Reproducible audit documentation for compliance requirements

#### AI-Performance Plugin (v1.0.0)

- `/performance-audit` command for comprehensive performance analysis
- `performance-optimizer` agent with deep performance optimization expertise
- Performance anti-pattern detection (N+1 queries, synchronous operations, memory issues)
- Database optimization recommendations with missing index detection
- Timestamped performance audit reports in `/docs/performance/` directory
- Architecture performance assessment (data access, application layer, infrastructure)
- Code optimization examples with before/after comparisons
- Impact scoring and prioritized optimization roadmap
- Expected performance improvement estimates

### Documentation

- README.md for marketplace overview and installation instructions
- CLAUDE.md for repository development guidelines
- Individual plugin README files with comprehensive documentation
- Plugin installation and usage instructions
- License information (MIT)

[Unreleased]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/charlesjones-dev/claude-code-plugins-dev/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/charlesjones-dev/claude-code-plugins-dev/releases/tag/v1.0.0
