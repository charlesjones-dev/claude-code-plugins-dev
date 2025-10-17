# Claude Code Plugins for Developers

A curated list of custom Claude Code plugins, agents, and skills for developers.

## 🎯 Overview

This Claude Code plugin marketplace provides plugins that extend Claude Code's capabilities, focusing on developer productivity and automation.

## 📦 Available Plugins

### ai-git

**AI-powered git automation** - Intelligent git commands and agents that streamline your version control workflow.

- **Version:** 1.0.0
- **Type:** AI Instruction Plugin (Slash Commands & Agents)
- **Keywords:** ai, git, commit, commits, automation, productivity, devops, version-control

**Current Commands:**

- `/commit-push` - Analyze changes, generate intelligent commit messages, and push to origin

**Features:**

- Automatically analyzes git status and diffs
- Generates context-aware commit messages following your repository's style
- Supports conventional commit prefixes (fix:, feat:, docs:, etc.)
- One-command commit and push workflow
- Clean commit messages (no AI attribution clutter)
- Extensible architecture for adding more git automation commands

### ai-security

**AI-powered security auditing** - Intelligent security scanning and vulnerability detection with comprehensive reporting.

> **Note:** While Claude Code includes the native `/security-review` command for quick security checks, this plugin provides **reproducible audit documentation** with custom templates, controlled output locations, and consistent formatting - essential for formal security audits and compliance requirements.

- **Version:** 1.0.0
- **Type:** AI Instruction Plugin (Slash Commands & Agents)
- **Keywords:** ai, security, compliance, auditing, auditor, vulnerability, owasp, scanning, defensive

**Current Commands:**

- `/security-audit` - Perform comprehensive security analysis and generate detailed audit reports

**Features:**

- Custom scan templates for reproducible audits
- Timestamped reports saved to `/docs/security/{timestamp}-security-audit.md` (prevents overwrites)
- Comprehensive vulnerability detection (SQL injection, XSS, authentication bypass, etc.)
- OWASP Top 10 2021 compliance assessment
- Architecture security analysis for authentication, authorization, and data protection
- Dependency vulnerability scanning
- Detailed findings with risk scores, code context, and remediation guidance
- Before/after code examples showing secure fixes
- Prioritized remediation roadmap
- Enterprise-ready documentation suitable for compliance

### ai-performance

**AI-powered performance optimization** - Intelligent performance analysis and bottleneck detection with comprehensive reporting.

- **Version:** 1.0.0
- **Type:** AI Instruction Plugin (Slash Commands & Agents)
- **Keywords:** ai, performance, optimization, analysis, bottleneck, scalability

**Current Commands:**

- `/performance-audit` - Perform comprehensive performance analysis and generate detailed optimization reports

**Features:**

- Custom analysis templates for reproducible audits
- Timestamped reports saved to `/docs/performance/{timestamp}-performance-audit.md` (prevents overwrites)
- Comprehensive performance pattern detection (N+1 queries, sync operations, memory issues, etc.)
- Performance best practices assessment across 10 key areas
- Architecture performance analysis for data access, application layer, and infrastructure
- Database optimization recommendations with missing index detection
- Detailed findings with impact scores, code context, and optimization guidance
- Before/after code examples showing performance improvements
- Prioritized optimization roadmap with expected performance gains
- Enterprise-ready documentation suitable for performance reviews

## 🚀 Quick Start

### Installation

1. Add this marketplace to Claude Code:

```bash
/plugin marketplace add charlesjones-dev/claude-code-plugins-dev
```

2. Install plugins:

```bash
# Install the ai-git plugin
/plugin install ai-git@claude-code-plugins-dev

# Install the ai-security plugin
/plugin install ai-security@claude-code-plugins-dev

# Install the ai-performance plugin
/plugin install ai-performance@claude-code-plugins-dev
```

### Usage

Once installed, you can use the slash commands directly in Claude Code:

#### Git Automation

```bash
/commit-push
```

This will:

1. Analyze all your changes
2. Review recent commit history to match your style
3. Generate an appropriate commit message
4. Stage all changes
5. Commit and push to origin

#### Security Auditing

```bash
/security-audit
```

This will:

1. Scan your codebase for security vulnerabilities
2. Analyze against OWASP Top 10 compliance
3. Review authentication, authorization, and data protection
4. Generate a comprehensive audit report in `/docs/security/{timestamp}-security-audit.md`
5. Provide prioritized remediation guidance with code examples

#### Performance Optimization

```bash
/performance-audit
```

This will:

1. Scan your codebase for performance bottlenecks and optimization opportunities
2. Analyze code patterns (N+1 queries, sync operations, memory issues)
3. Review database performance, caching strategies, and resource utilization
4. Generate a comprehensive performance report in `/docs/performance/{timestamp}-performance-audit.md`
5. Provide prioritized optimization roadmap with expected performance gains

_More commands coming soon to automate additional workflows..._

## 🏗️ Plugin Structure

This marketplace uses a structured plugin system:

```
plugins/
  {plugin-name}/
    .claude-plugin/
      plugins.json          # Plugin metadata
    commands/
      {command-name}.md     # Command implementations
```

All plugins include:

- Plugin metadata and versioning
- Detailed documentation
- MIT license

## 🤝 Contributing

Contributions are welcome! To add a new plugin:

1. Fork this repository
2. Create your plugin following the structure above
3. Add plugin metadata to `.claude-plugin/marketplace.json`
4. Submit a pull request

### Plugin Guidelines

- Follow the existing directory structure
- Include comprehensive metadata in `plugins.json`
- Provide clear documentation for each command
- Use descriptive keywords for discoverability
- Test thoroughly before submitting

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

## 👤 Author

**Charles Jones**

- Website: [charlesjones.dev](https://charlesjones.dev)
- GitHub: [@charlesjones-dev](https://github.com/charlesjones-dev)

## 🔗 Links

- [Repository](https://github.com/charlesjones-dev/claude-code-plugins-dev)
- [Claude Code Plugins Documentation](https://docs.claude.com/en/docs/claude-code/plugins)

---

**Built with ❤️ for the Claude Code community**
