# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a marketplace for custom Claude Code plugins, skills, and other extensions. The repository follows a structured plugin system where each plugin is self-contained with its own metadata and commands.

## Architecture

### Marketplace Structure

The repository uses a two-level metadata system:

1. **Root marketplace manifest** (`.claude-plugin/marketplace.json`): Central registry that defines:
   - Marketplace owner and metadata
   - List of all available plugins with their source paths, descriptions, and categories
   - Plugin root directory location (`./plugins`)

2. **Individual plugin manifests** (`plugins/{plugin-name}/.claude-plugin/plugins.json`): Each plugin has its own metadata including name, version, description, author, and license.

### Plugin Organization

Plugins are organized under the `plugins/` directory:
```
plugins/
  {plugin-name}/
    .claude-plugin/
      plugins.json          # Plugin metadata
    commands/
      {command-name}.md     # Command implementations
```

### Plugin Types

Plugins can include:
- **Slash commands**: Markdown files in `commands/` directory that define executable commands
- Each command is a markdown file with instructions for Claude Code to execute

## Development Workflow

### Adding a New Plugin

1. Create the plugin directory structure under `plugins/{plugin-name}/`
2. Add plugin metadata in `.claude-plugin/plugins.json` with:
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
1. The plugin's own `plugins.json` file
2. The marketplace's root `marketplace.json` registry entry

Both should have matching:
- name
- version
- description
- author information
