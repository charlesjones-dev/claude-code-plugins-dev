# Scaffold Plugin

AI-powered plugin scaffolding tool that generates a complete Claude Code plugin structure based on user requirements.

## Instructions

When this command is executed, follow these steps to create a new plugin:

### 1. Gather Plugin Requirements

Use the AskUserQuestion tool to collect the following information:

**Question 1 - Plugin Basics:**
- header: "Plugin Info"
- question: "What is the name of your plugin? (use kebab-case, e.g., 'my-awesome-plugin')"
- This should be a text input

**Question 2 - Plugin Description:**
- header: "Description"
- question: "Provide a brief description of what your plugin does:"
- This should be a text input

**Question 3 - Plugin Category:**
- header: "Category"
- question: "What category best describes your plugin?"
- options:
  - "AI & Automation" - AI-powered tools and automation workflows
  - "Productivity" - Tools that enhance developer productivity
  - "Code Quality" - Testing, linting, and code quality tools
  - "DevOps & Deployment" - CI/CD, deployment, and infrastructure tools
  - "Development Tools" - General development utilities
  - "Security" - Security scanning and compliance tools

**Question 4 - Initial Commands:**
- header: "Commands"
- question: "Which commands would you like to include? (You can select multiple)"
- multiSelect: true
- options:
  - "Main command" - A primary command for the plugin's core functionality
  - "Helper command" - A utility or helper command
  - "Custom commands" - I'll specify custom command names

**Question 5 - Additional Features:**
- header: "Features"
- question: "Would you like to include any of these additional features?"
- multiSelect: true
- options:
  - "README with examples" - Generate a comprehensive README file
  - "LICENSE file" - Add an MIT license file
  - "Test command" - Include a test/validation command

### 2. Create Plugin Directory Structure

Based on the gathered information, create the following structure:

```
plugins/{plugin-name}/
  .claude-plugin/
    plugin.json
  commands/
    {command-name}.md
  README.md (if selected)
  LICENSE (if selected)
```

Execute:
```bash
mkdir -p "plugins/{plugin-name}/.claude-plugin"
mkdir -p "plugins/{plugin-name}/commands"
```

### 3. Generate plugin.json

Create the plugin metadata file with:
- name: The plugin name provided by the user
- version: Start at "1.0.0"
- description: The description provided by the user
- author: Use the marketplace owner information from `.claude-plugin/marketplace.json`
- repository: Use the same repository as other plugins
- license: "MIT"
- keywords: Generate relevant keywords based on the plugin name, description, and category

### 4. Generate Commands

For each command the user wants to create:

1. Ask for the command name (if "Custom commands" was selected)
2. Ask for a brief description of what the command should do
3. Create a markdown file in the `commands/` directory with:
   - A clear title (# Command Name)
   - A description of what the command does
   - An "## Instructions" section with step-by-step guidance for Claude Code
   - Any important notes or constraints

Command template:
```markdown
# {Command Name}

{Brief description of what this command does}

## Instructions

When this command is executed:

1. {Step 1 description}
2. {Step 2 description}
3. {Step 3 description}
...

IMPORTANT: {Any important constraints or requirements}
```

### 5. Generate README.md (if selected)

Create a comprehensive README with:
- Plugin name and description
- Installation instructions
- Available commands with examples
- Usage guidelines
- Author and license information

### 6. Generate LICENSE (if selected)

Create an MIT license file with:
- Current year
- Author name from marketplace owner

### 7. Register Plugin in Marketplace

Read the `.claude-plugin/marketplace.json` file and add the new plugin to the `plugins` array:

```json
{
  "name": "{plugin-name}",
  "source": "./plugins/{plugin-name}",
  "description": "{plugin-description}",
  "version": "1.0.0",
  "keywords": [...],
  "author": {
    "name": "{author-name}",
    "url": "{author-url}"
  },
  "repository": "{repository-url}"
}
```

### 8. Verify and Report

After scaffolding is complete:

1. List all created files
2. Display the plugin structure
3. Provide next steps:
   - Review and customize the generated commands
   - Test the plugin with Claude Code
   - Update the README with specific usage examples
   - Commit the changes

## Important Notes

- Always use kebab-case for plugin names (e.g., "ai-security", not "AiSecurity")
- Ensure consistency between the plugin's `plugin.json` and marketplace `marketplace.json` entry
- Follow the existing plugin patterns in the repository
- Generate meaningful, actionable commands that provide clear instructions to Claude Code
- Do NOT include Claude Code attribution or co-author tags in any generated content

## Example Flow

```
User runs: /scaffold-plugin

1. Ask questions about the plugin
2. User answers:
   - Name: "code-analyzer"
   - Description: "AI-powered code analysis and insights"
   - Category: "Code Quality"
   - Commands: ["Main command", "Custom commands"]
   - Features: ["README with examples", "LICENSE file"]

3. Create directory structure
4. Generate plugin.json
5. Ask about custom commands and generate them
6. Generate README and LICENSE
7. Register in marketplace.json
8. Report success with file listing
```
