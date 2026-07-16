# Claude Code Plugins for Developers

[![Version](https://img.shields.io/badge/version-2.7.1-blue.svg)](https://github.com/charlesjones-dev/claude-code-plugins-dev/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub Issues](https://img.shields.io/github/issues/charlesjones-dev/claude-code-plugins-dev.svg)](https://github.com/charlesjones-dev/claude-code-plugins-dev/issues)
[![GitHub Stars](https://img.shields.io/github/stars/charlesjones-dev/claude-code-plugins-dev.svg)](https://github.com/charlesjones-dev/claude-code-plugins-dev/stargazers)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/charlesjones-dev/claude-code-plugins-dev/graphs/commit-activity)

AI-powered plugins that streamline your entire development workflow in Claude Code.

## 🎯 Overview

This Claude Code plugin marketplace provides 14 plugins that extend Claude Code's capabilities, focusing on developer productivity and automation.

## 📦 Available Plugins

> **💡 Usage Note:** All skills are invoked as slash commands (e.g., `/accessibility-audit`). Interactive skills prompt you for any required information; non-interactive skills run directly on your codebase. A few accept optional flags (e.g., `/seo-fix --dry-run`, `/swift-verify --fix`) — see each plugin's README for details.

| Plugin | Description | Skills (Slash Commands) | Agents |
|--------|-------------|------------------------|--------|
| [ai-accessibility](plugins/ai-accessibility/) | AI-powered accessibility auditing with WCAG compliance | `/accessibility-audit` | `accessibility-auditor` |
| [ai-ado](plugins/ai-ado/) | AI-powered Azure DevOps integration with MCP support | `/ado-init`, `/ado-work-items`, `/ado-create-feature`, `/ado-create-story`, `/ado-create-task`, `/ado-log-story-work`, `/ado-timesheet-report` | - |
| [ai-compliance](plugins/ai-compliance/) | AI-powered license compliance auditing and attribution generation | `/compliance-license-audit`, `/compliance-notice-generate` | - |
| [ai-geo](plugins/ai-geo/) | Generative Engine Optimization (GEO) for AI answer engines — llms.txt, AI crawler policy, citation-worthiness | `/geo-audit`, `/geo-fix`, `/geo-llms-txt` | - |
| [ai-git](plugins/ai-git/) | AI-powered git automation and workflow streamlining | `/git-init`, `/git-commit-push`, `/git-commit-push-pr`, `/git-pr-codex-loop` | - |
| [ai-knowledge](plugins/ai-knowledge/) | Curated, git-versioned team knowledge base with Obsidian compatibility — complements Claude Code's native auto memory | `/kb-init`, `/kb-learn`, `/kb-add`, `/kb-query`, `/kb-import`, `/kb-ingest`, `/kb-harvest`, `/kb-discover`, `/kb-absorb`, `/kb-remove`, `/kb-load`, `/kb-list`, `/kb-search`, `/kb-prune`, `/kb-auto`, `/kb-organize`, `/kb-upgrade` | - |
| [ai-modernize](plugins/ai-modernize/) | AI-powered codebase modernization assessment for technical debt | `/modernize-audit`, `/modernize-scan` | `modernize-auditor` |
| [ai-performance](plugins/ai-performance/) | AI-powered performance optimization and bottleneck detection | `/performance-audit` | `performance-auditor` |
| [ai-security](plugins/ai-security/) | AI-powered security auditing — complements native `/security-review` with archived OWASP-mapped reports, deployed-site scanning, and settings/supply-chain hardening | `/security-init`, `/security-audit`, `/security-scan-dependencies`, `/security-supply-chain` | `security-auditor`, `security-dependency-scanner` |
| [ai-seo](plugins/ai-seo/) | AI-powered modern SEO auditing that catches deprecated patterns LLMs still generate | `/seo-audit`, `/seo-fix`, `/seo-schema` | - |
| [ai-statusline](plugins/ai-statusline/) | Enhances Claude Code's native `/statusline` with progress bars, rate-limit widgets, and an effort-level indicator | `/statusline-wizard`, `/statusline-edit` | - |
| [ai-swift](plugins/ai-swift/) | AI-powered Swift/iOS/macOS release-readiness — catches Xcode Cloud & TestFlight blockers before upload | `/swift-preflight`, `/swift-diagnose`, `/swift-ci-scaffold`, `/swift-verify`, `/swift-concurrency-review` | `swift-release-auditor` |
| [ai-workflow](plugins/ai-workflow/) | AI-powered development workflow automation — preflight quality gates, ship-it workflow, principles & behavior rules | `/workflow-preflight`, `/workflow-ship`, `/workflow-principles`, `/workflow-rules` | - |
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

## 🗄️ Deprecated & Removed

As Claude Code ships features natively, plugins and skills that duplicate them are retired here. Removed plugins and skills live on in git history.

| Item | Status | Superseded by | Details |
|------|--------|---------------|---------|
| ai-learn (`/learn`, `/learn-review`) | 🗑️ Removed (July 2026) | Native **Learning** output style — `/config` → "Output style" → "Learning" | Built-in collaborative mentor mode with `TODO(human)` markers; an **Explanatory** style also ships natively |
| ai-workflow `/workflow-plan-phases` | 🗑️ Removed (July 2026, v2.0.0) | Native **Dynamic Workflows** | JavaScript runtime orchestrating subagent fan-out with per-agent token budgets — replaces manual 30–50k-token phase sizing |
| ai-workflow `/workflow-implement-phases` | 🗑️ Removed (July 2026, v2.0.0) | Native **Dynamic Workflows** | Runtime-managed orchestration replaces manual `Task()` fan-out and phase-coordination bookkeeping |

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

[![Star History Chart](https://api.star-history.com/chart?repos=charlesjones-dev/claude-code-plugins-dev&type=date&legend=bottom-right&sealed_token=_0yv5MGXVJ1oD5GXaPNG5bkcHVoquKUyqcfEsy0s4G9DScPsO-0c-mdNKq9Azb5rK8laSJeQe1yfD0SbfA2OnhgIP3jkbS-_Ygm5B0vLqnAOQeC6dKQjZKh_y3h3X8azNaQLG8fOidK3SLPhlOB9MKSNrHg-kB1xDFDVtOsTypQ-ztjPzxdjM_t5yLiN)](https://www.star-history.com/?type=date&legend=bottom-right&repos=charlesjones-dev%2Fclaude-code-plugins-dev)

---

**Built with ❤️ for the Claude Code community**
