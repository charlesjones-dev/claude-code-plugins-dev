# AI Plugins

AI-powered plugin development tools for Claude Code. This plugin provides intelligent scaffolding and generation capabilities to help you quickly create new Claude Code plugins with proper structure, metadata, and commands.

## Features

- **Interactive Scaffolding**: Ask questions to gather plugin requirements
- **Automatic Structure Generation**: Create proper directory structure and metadata files
- **Smart Command Generation**: Generate command templates with clear instructions
- **Marketplace Integration**: Automatically register new plugins in marketplace.json
- **Best Practices**: Follow Claude Code plugin conventions and patterns

## Available Commands

### `/scaffold-plugin`

Interactively scaffold a new Claude Code plugin with AI assistance.

**What it does:**
- Asks questions about your plugin (name, description, category, commands)
- Creates the complete plugin directory structure
- Generates metadata files (plugin.json)
- Creates command templates with instructions
- Optionally generates README and LICENSE files
- Registers the plugin in the marketplace

**Example usage:**

```bash
/scaffold-plugin
```

**Interactive flow:**

1. **Plugin Name**: Enter the plugin name in kebab-case (e.g., "my-awesome-plugin")
2. **Description**: Provide a brief description of your plugin's purpose
3. **Category**: Choose from AI & Automation, Productivity, Code Quality, DevOps, Development Tools, or Security
4. **Commands**: Select which commands to include (main, helper, or custom)
5. **Features**: Choose additional features (README, LICENSE, test command)

The command will then:
- Create the plugin directory structure
- Generate all necessary files
- Register the plugin in the marketplace
- Provide next steps for customization

**Generated structure:**

```
plugins/your-plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── commands/
│   └── your-command.md       # Command implementation
├── README.md                 # Plugin documentation
└── LICENSE                   # MIT license
```

## Installation

This plugin is part of the claude-code-plugins-dev marketplace. To use it:

1. Clone the marketplace repository
2. The ai-plugins plugin will be available in your Claude Code instance
3. Run `/scaffold-plugin` to create new plugins

## Creating Your First Plugin

1. Run the scaffold command:
   ```bash
   /scaffold-plugin
   ```

2. Answer the interactive questions:
   - Plugin name: `hello-world`
   - Description: `A simple hello world plugin`
   - Category: `Development Tools`
   - Commands: Select "Main command"
   - Features: Select "README with examples" and "LICENSE file"

3. The plugin structure will be generated automatically

4. Customize the generated command in `plugins/hello-world/commands/`

5. Test your plugin with Claude Code

## Plugin Development Best Practices

When creating plugins with this tool:

- **Use kebab-case** for plugin and command names
- **Write clear command instructions** that Claude Code can follow
- **Include examples** in your command documentation
- **Test commands** before committing to ensure they work as expected
- **Keep commands focused** on a single responsibility
- **Document constraints** and important requirements in command files

## Command Development Tips

Commands are markdown files that provide instructions to Claude Code. They should:

- Have a clear title and description
- Include a step-by-step "Instructions" section
- Specify any important constraints or requirements
- Use the AskUserQuestion tool when user input is needed
- Follow the existing command patterns in the repository

## Examples

### Simple Utility Plugin

```bash
/scaffold-plugin

Name: file-organizer
Description: AI-powered file organization and cleanup
Category: Productivity
Commands: Main command
Features: README with examples
```

### Multi-Command Development Plugin

```bash
/scaffold-plugin

Name: api-tools
Description: REST API development utilities
Category: Development Tools
Commands: Main command, Helper command, Custom commands
Features: README with examples, LICENSE file, Test command
```
---

## 📦 Plugin Details

- **Name:** AI-Plugins
- **Version:** 1.0.0
- **Features:**
  - Commands: `/scaffold-plugin`
- **License:** MIT
- **Author:** Charles Jones

## Troubleshooting

**Issue**: Plugin not appearing in Claude Code

**Solution**: Ensure the plugin is properly registered in `.claude-plugin/marketplace.json`

**Issue**: Command not working as expected

**Solution**: Review the command markdown file and ensure instructions are clear and follow Claude Code conventions

## Contributing

To improve this plugin:

1. Review the command implementation in `commands/scaffold-plugin.md`
2. Suggest improvements or additional features
3. Test with various plugin configurations
4. Submit feedback or contributions

## License

MIT License - See LICENSE file for details

## Author

Charles Jones - [charlesjones.dev](https://charlesjones.dev)

## Repository

[claude-code-plugins-dev](https://github.com/charlesjones-dev/claude-code-plugins-dev)
