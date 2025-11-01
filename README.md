# Claude Code Plugins for Developers

[![Version](https://img.shields.io/badge/version-1.5.1-blue.svg)](https://github.com/charlesjones-dev/claude-code-plugins-dev/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub Issues](https://img.shields.io/github/issues/charlesjones-dev/claude-code-plugins-dev.svg)](https://github.com/charlesjones-dev/claude-code-plugins-dev/issues)
[![GitHub Stars](https://img.shields.io/github/stars/charlesjones-dev/claude-code-plugins-dev.svg)](https://github.com/charlesjones-dev/claude-code-plugins-dev/stargazers)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/charlesjones-dev/claude-code-plugins-dev/graphs/commit-activity)

Automate developer busy work with AI-powered plugins for Claude Code.

## 🎯 Overview

This Claude Code plugin marketplace provides plugins that extend Claude Code's capabilities, focusing on developer productivity and automation.

## 📦 Available Plugins

| Plugin | Description | Commands | Agents | Skills |
|--------|-------------|----------|--------|--------|
| [ai-accessibility](plugins/ai-accessibility/) | AI-powered accessibility auditing with WCAG compliance | `/accessibility-audit` | `accessibility-auditor` | `accessibility-auditing` |
| [ai-ado](plugins/ai-ado/) | AI-powered Azure DevOps integration with MCP support | `/ado-init`, `/ado-create-feature`, `/ado-create-story`, `/ado-create-task`, `/ado-log-story-work`, `/ado-timesheet-report` | - | `ado-work-items` |
| [ai-git](plugins/ai-git/) | AI-powered git automation and workflow streamlining | `/git-init`, `/git-commit-push` | - | - |
| [ai-performance](plugins/ai-performance/) | AI-powered performance optimization and bottleneck detection | `/performance-audit` | `performance-auditor` | `performance-auditing` |
| [ai-plugins](plugins/ai-plugins/) | AI-powered plugin and skill scaffolding and generation tools | `/plugins-scaffold` | - | `skills-scaffold`, `plugins-scaffold` |
| [ai-security](plugins/ai-security/) | AI-powered security auditing with reproducible reports | `/security-init`, `/security-audit`, `/security-scan-dependencies` | `security-auditor`, `security-dependency-scanner` | `security-auditing`, `security-dependency-scanning` |

> **📝 Note on Audit Plugins:** The `ai-accessibility`, `ai-security`, and `ai-performance` plugins are developer-focused code analysis tools designed to identify issues during development. They perform static code analysis and are meant to **complement** (not replace) runtime testing tools, professional services, and manual testing. Use these plugins to catch issues early in the development phase, then validate with specialized testing tools and services appropriate to your domain.

## 🚀 Quick Start

### Prerequisites

**New to Claude Code?** Claude Code is an AI-powered CLI tool that helps with software development tasks.

👉 [Download and install Claude Code](https://www.claude.com/product/claude-code)

### Installation

1. Add this marketplace to Claude Code:

```bash
/plugin marketplace add charlesjones-dev/claude-code-plugins-dev
```

2. Install plugins (see **Available Plugins** table above for all options):

```bash
# Install any plugin from this marketplace
/plugin install <plugin-name>@claude-code-plugins-dev

# Examples:
/plugin install ai-ado@claude-code-plugins-dev
/plugin install ai-git@claude-code-plugins-dev
/plugin install ai-security@claude-code-plugins-dev
```

### Usage

Once installed, plugins add slash commands directly to Claude Code. Use any command from the **Available Plugins** table above:

```bash
# Examples:
/git-init              # Initialize .gitignore for project
/security-init         # Initialize security settings
/ado-init              # Initialize Azure DevOps + MCP server configuration
```

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

## 👤 Author

**Charles Jones**

- Website: [charlesjones.dev](https://charlesjones.dev)
- GitHub: [@charlesjones-dev](https://github.com/charlesjones-dev)

## 🔗 Links

- [This Repository](https://github.com/charlesjones-dev/claude-code-plugins-dev)
- [Claude Code Plugins Documentation](https://docs.claude.com/en/docs/claude-code/plugins)

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=charlesjones-dev/claude-code-plugins-dev&type=date&legend=bottom-right)](https://www.star-history.com/#charlesjones-dev/claude-code-plugins-dev&type=date&legend=bottom-right)

---

**Built with ❤️ for the Claude Code community**
