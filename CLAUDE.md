# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a marketplace for custom Claude Code plugins, skills, and other extensions. The repository follows a structured plugin system where each plugin is self-contained with its own metadata and commands.

## Official Documentation

For detailed information about Claude Code plugins, refer to these official documentation resources:

1. **[Plugins](https://docs.claude.com/en/docs/claude-code/plugins)**: Core concepts and guide for creating and using Claude Code plugins
2. **[Plugins Reference](https://docs.claude.com/en/docs/claude-code/plugins-reference)**: Technical reference for plugin structure, metadata schemas, and command formats
3. **[Plugin Marketplaces](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)**: Guide for creating and managing plugin marketplaces like this repository

These documentation resources provide authoritative information on plugin development best practices, metadata schemas, and marketplace structure that should be consulted when developing new plugins.

## Architecture

### Marketplace Structure

The repository uses a two-level metadata system:

1. **Root marketplace manifest** (`.claude-plugin/marketplace.json`): Central registry that defines:
   - Marketplace owner and metadata
   - List of all available plugins with their source paths, descriptions, and categories
   - Plugin root directory location (`./plugins`)

2. **Individual plugin manifests** (`plugins/{plugin-name}/.claude-plugin/plugin.json`): Each plugin has its own metadata including name, version, description, author, and license.

### Plugin Organization

Plugins are organized under the `plugins/` directory:
```
plugins/
  {plugin-name}/
    .claude-plugin/
      plugin.json          # Plugin metadata
    commands/
      {command-name}.md     # Command implementations
```

### Plugin Types

Plugins can include:
- **Slash commands**: Markdown files in `commands/` directory that define executable commands
- Each command is a markdown file with instructions for Claude Code to execute

## Development Workflow

### Adding a New Plugin

You can create a new plugin either manually or using the ai-plugins scaffolding tool:

#### Option 1: Using the AI-Plugins Scaffolding Tool (Recommended)

The ai-plugins plugin provides a `/scaffold-plugin` command that interactively creates a complete plugin structure:

```bash
/scaffold-plugin
```

This will:
1. Ask interactive questions about your plugin (name, description, category, commands)
2. Create the complete directory structure under `plugins/{plugin-name}/`
3. Generate plugin.json with proper metadata
4. Create command templates with instructions
5. Optionally generate README and LICENSE files
6. Automatically register the plugin in `.claude-plugin/marketplace.json`

#### Option 2: Manual Plugin Creation

1. Create the plugin directory structure under `plugins/{plugin-name}/`
2. Add plugin metadata in `.claude-plugin/plugin.json` with:
   - name, version, description
   - author information
   - keywords for discoverability
   - repository and license
3. Implement commands in the `commands/` directory as markdown files
4. Register the plugin in the root `.claude-plugin/marketplace.json`

### Command Development

Commands are markdown files that provide instructions to Claude Code. They should:
- Have a clear title and description
- Include step-by-step instructions under an "## Instructions" section
- Specify any important constraints or requirements (e.g., what NOT to include in outputs)

Example from commit-push command (plugins/productivity/commit-push/commands/commit-push.md:22-24):
```
IMPORTANT: Do not include the following in commit messages:
- 🤖 Generated with [Claude Code](https://claude.com/claude-code)
- Co-Authored-By: Claude <noreply@anthropic.com>
```

## Key Conventions

### Git Commit Messages

This repository has specific requirements for git commit messages:
- Follow the repository's existing commit message style (check recent commits with `git log`)
- Use conventional commit prefixes if the repository uses them (fix:, feat:, docs:, etc.)
- Do NOT include Claude Code attribution or co-author tags

### Plugin Metadata

When creating or updating plugins, ensure consistency between:
1. The plugin's own `plugin.json` file
2. The marketplace's root `marketplace.json` registry entry

Both should have matching:
- name
- version
- description
- author information
