# Claude Code Plugins for Developers

[![Version](https://img.shields.io/badge/version-2.4.2-blue.svg)](https://github.com/charlesjones-dev/claude-code-plugins-dev/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub Issues](https://img.shields.io/github/issues/charlesjones-dev/claude-code-plugins-dev.svg)](https://github.com/charlesjones-dev/claude-code-plugins-dev/issues)
[![GitHub Stars](https://img.shields.io/github/stars/charlesjones-dev/claude-code-plugins-dev.svg)](https://github.com/charlesjones-dev/claude-code-plugins-dev/stargazers)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/charlesjones-dev/claude-code-plugins-dev/graphs/commit-activity)

AI-powered plugins that streamline your entire development workflow in Claude Code.

## 🎯 Overview

This Claude Code plugin marketplace provides plugins that extend Claude Code's capabilities, focusing on developer productivity and automation.

## 📦 Available Plugins

> **💡 Usage Note:** All skills are invoked as slash commands without arguments (e.g., `/accessibility-audit`). Interactive skills will prompt you for any required information; non-interactive skills run directly on your codebase.

| Plugin | Description | Skills (Slash Commands) | Agents |
|--------|-------------|------------------------|--------|
| [ai-accessibility](plugins/ai-accessibility/) | AI-powered accessibility auditing with WCAG compliance | `/accessibility-audit` | `accessibility-auditor` |
| [ai-ado](plugins/ai-ado/) | AI-powered Azure DevOps integration with MCP support | `/ado-init`, `/ado-create-feature`, `/ado-create-story`, `/ado-create-task`, `/ado-log-story-work`, `/ado-timesheet-report` | - |
| [ai-git](plugins/ai-git/) | AI-powered git automation and workflow streamlining | `/git-init`, `/git-commit-push`, `/git-commit-push-pr` | - |
| [ai-learn](plugins/ai-learn/) | AI-powered Socratic learning mode for guided problem-solving | `/learn`, `/learn-review` | - |
| [ai-performance](plugins/ai-performance/) | AI-powered performance optimization and bottleneck detection | `/performance-audit` | `performance-auditor` |
| [ai-security](plugins/ai-security/) | AI-powered security auditing with reproducible reports | `/security-init`, `/security-audit`, `/security-scan-dependencies`, `/security-supply-chain` | `security-auditor`, `security-dependency-scanner` |
| [ai-statusline](plugins/ai-statusline/) | AI-powered status line customization with progress bars | `/statusline-wizard`, `/statusline-edit` | - |
| [ai-workflow](plugins/ai-workflow/) | AI-powered development workflow automation | `/workflow-plan-phases`, `/workflow-implement-phases`, `/workflow-preflight`, `/workflow-ship`, `/workflow-principles` | - |
| [ai-compliance](plugins/ai-compliance/) | AI-powered license compliance auditing and attribution generation | `/compliance-license-audit`, `/compliance-notice-generate` | - |
| [ai-knowledge](plugins/ai-knowledge/) | AI-powered knowledge base management with Obsidian compatibility | `/kb-init`, `/kb-learn`, `/kb-add`, `/kb-query`, `/kb-import`, `/kb-ingest`, `/kb-harvest`, `/kb-discover`, `/kb-absorb`, `/kb-remove`, `/kb-load`, `/kb-list`, `/kb-search`, `/kb-prune`, `/kb-auto`, `/kb-organize`, `/kb-upgrade` | - |
| [ai-modernize](plugins/ai-modernize/) | AI-powered codebase modernization assessment for technical debt | `/modernize-audit`, `/modernize-scan` | `modernize-auditor` |
| [ai-seo](plugins/ai-seo/) | AI-powered modern SEO auditing that catches deprecated patterns LLMs still generate | `/seo-audit`, `/seo-fix`, `/seo-schema` | - |
| [ai-geo](plugins/ai-geo/) | Generative Engine Optimization (GEO) for AI answer engines — llms.txt, AI crawler policy, citation-worthiness | `/geo-audit`, `/geo-fix`, `/geo-llms-txt` | - |
| [ai-writing](plugins/ai-writing/) | AI-powered writing quality tools for natural-sounding text | `/writing-humanize` | - |

> **📝 Note on Audit Plugins:** The `ai-accessibility`, `ai-security`, and `ai-performance` plugins are developer-focused analysis tools designed to identify issues during development. They perform static code analysis, with `ai-accessibility` and `ai-security` also offering URL scanning capabilities (`/accessibility-audit` with Playwright MCP and `/security-scan-dependencies` respectively). These plugins are meant to **complement** (not replace) runtime testing tools, professional services, and manual testing. Use these plugins to catch issues early in the development phase, then validate with specialized testing tools and services appropriate to your domain.

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
