# AI-ADO Plugin

**AI-powered Azure DevOps integration for Claude Code.** Intelligent configuration, work item management, and automation that streamlines your Azure DevOps workflows.

---

## 🎯 What This Plugin Does

Provides AI-powered Azure DevOps integration through the official Microsoft Azure DevOps MCP server, with intelligent configuration management, work item creation guidelines, and automated workflows that ensure consistency across your team.

## 📋 Available Skills

### `/ado-init`

Initialize Azure DevOps configuration by creating or updating `CLAUDE.md` with organization-specific guidelines for work item creation, naming conventions, and MCP tool usage.

### `/ado-create-feature`

Interactively create a new Feature work item in Azure DevOps following your organization's configured conventions. Supports both AI-powered generation and manual input modes.

### `/ado-create-story`

Interactively create a new User Story work item as a child of an existing Feature, with guided prompts for persona statements, background, and acceptance criteria. Supports both AI-powered generation and manual input modes.

### `/ado-create-task`

Interactively create a new Task work item as a child of an existing User Story, with hour estimation and lightweight task tracking. Supports both AI-powered generation and manual input modes.

### `/ado-log-story-work`

Rapidly log completed work to a User Story by creating a Task work item with completed hours already set. Designed for quick logging multiple times per day. Supports AI-powered generation with automatic git commit hash detection and optional placeholder task hour subtraction.

### `/ado-timesheet-report`

Generate a summarized report of hours logged from work items during a specified week, with flexible filtering for closed, worked on, or both types of tasks. Creates a hierarchical tree structure (Feature > User Story > Task) showing rolled-up hours for weekly timesheet purposes.

**What it does:**

- Collects your Azure DevOps organization, project, and team settings
- Configures default Area Path and Iteration Path for work items
- Sets up naming conventions (decimal notation or descriptive names)
- Optionally creates `.mcp.json` for Azure DevOps MCP server configuration (OS-aware for Windows/Linux/Mac)
- Generates comprehensive work item creation guidelines
- Defines Feature, User Story, and Task hierarchy and requirements
- Configures hour estimation and Story Points standards

**Usage:**

```
/ado-init
# ✨ AI asks for your Azure DevOps settings
# ✨ You provide org, project, team, paths, and preferences
# ✨ Generates CLAUDE.md configuration section
# ✨ Creates work item guidelines and conventions
# ✅ Done!
```

### `/ado-create-feature` Command Details

**What it does:**

- Validates Azure DevOps configuration exists in CLAUDE.md
- Offers choice between AI-powered generation or manual input
- **AI Mode**: Generate professional title and description from a simple prompt
- **Manual Mode**: Provide title and description yourself
- Creates Feature work item with proper HTML formatting
- Sets Area Path, Iteration Path, and State automatically
- Displays success message with work item ID and Azure DevOps link

**Usage (AI Mode):**

```
/ado-create-feature

# Choose: AI
# Provide a description of what the feature should accomplish
# ✨ AI generates professional title following naming conventions
# ✨ AI generates comprehensive feature description
# ✨ Review and confirm or override each generated field
# ✨ Creates Feature with ID and hierarchy link
# ✅ Done!
```

**Usage (Manual Mode):**

```
/ado-create-feature

# Choose: Manual
# You'll be prompted for:
# - Feature title (e.g., "1: User Authentication System")
# - Feature description (high-level overview)

# ✨ Creates Feature with ID and hierarchy link
# ✨ Shows Azure DevOps URL for immediate viewing
# ✅ Done!
```

**Requirements:**
- Must run `/ado-init` first to configure Azure DevOps settings
- Azure DevOps MCP server must be configured and running

### `/ado-create-story` Command Details

**What it does:**

- Validates Azure DevOps configuration exists in CLAUDE.md
- Prompts for parent Feature ID to create hierarchy
- Offers choice between AI-powered generation or manual input
- **AI Mode**: Generate professional title, persona statement, background, and acceptance criteria from a simple description
- **Manual Mode**: Provide each field yourself through guided prompts
- Creates User Story as child of Feature with proper linking
- Applies HTML formatting for readability
- Sets Area Path, Iteration Path, and State automatically

**Usage (AI Mode):**

```
/ado-create-story

# Choose: AI
# Provide parent Feature ID
# Describe what the user story should accomplish
# ✨ AI generates professional title following naming conventions
# ✨ AI generates persona statement (As a... I want to... so that...)
# ✨ AI generates background information with technical details
# ✨ AI generates acceptance criteria in Given/When/Then format
# ✨ Review and confirm or override each generated field
# ✨ Provide Story Points estimation
# ✨ Creates User Story linked to Feature
# ✅ Done!
```

**Usage (Manual Mode):**

```
/ado-create-story

# Choose: Manual
# You'll be prompted for:
# - Parent Feature ID (e.g., 123)
# - Story title (e.g., "1.1: Implement user login functionality")
# - User persona statement
# - Background information
# - Acceptance criteria
# - Story Points (1, 2, 3, 5, 8, 13, etc.)

# ✨ Creates User Story linked to Feature
# ✨ Shows Azure DevOps URL for immediate viewing
# ✅ Done!
```

**Requirements:**
- Must run `/ado-init` first to configure Azure DevOps settings
- Must have an existing Feature work item (create with `/ado-create-feature`)
- Azure DevOps MCP server must be configured and running

### `/ado-create-task` Command Details

**What it does:**

- Validates Azure DevOps configuration exists in CLAUDE.md
- Prompts for parent User Story ID to create hierarchy
- Offers choice between AI-powered generation or manual input
- **AI Mode**: Generate professional task title from a simple description
- **Manual Mode**: Provide task title yourself
- Creates Task as child of User Story with proper linking
- Sets Original Estimate and Remaining Work to same value
- Leaves Completed Work empty (to be filled during progress)
- Sets Area Path, Iteration Path, and State automatically
- Keeps task description lightweight (references parent story)

**Usage (AI Mode):**

```
/ado-create-task

# Choose: AI
# Provide parent User Story ID
# Describe what the task should accomplish
# ✨ AI generates professional task title based on description
# ✨ Review and confirm or override generated title
# ✨ Provide hour estimate
# ✨ Creates Task linked to User Story
# ✅ Done!
```

**Usage (Manual Mode):**

```
/ado-create-task

# Choose: Manual
# You'll be prompted for:
# - Parent User Story ID (e.g., 124)
# - Task title (e.g., "Development for user login functionality")
# - Hour estimate (e.g., 8)

# ✨ Creates Task linked to User Story
# ✨ Sets hour tracking fields for time estimation
# ✨ Shows Azure DevOps URL for immediate viewing
# ✅ Done!
```

**Requirements:**
- Must run `/ado-init` first to configure Azure DevOps settings
- Must have an existing User Story work item (create with `/ado-create-story`)
- Azure DevOps MCP server must be configured and running

### `/ado-log-story-work` Command Details

**What it does:**

- Validates Azure DevOps configuration exists in CLAUDE.md
- Prompts for parent User Story ID to create hierarchy
- Offers choice between AI-powered generation or manual input
- **AI Mode**: Automatically detects git commit hashes in description and looks up commit details
- **AI Mode**: Generates professional task title and description based on prompt and commit context
- **Manual Mode**: Provide task title and description yourself
- Creates Task as child of User Story with proper linking
- Sets Original Estimate and Completed Work to the same value
- Leaves Remaining Work empty (work is already complete)
- Optionally subtracts hours from a placeholder task's Original Estimate and Remaining Work
- Displays comprehensive success message with task and optional placeholder task details

**Usage (AI Mode):**

```
/ado-log-story-work

# Provide parent User Story ID
# Choose: AI
# Describe the completed work (optionally include a git commit hash)
# ✨ AI automatically detects commit hash (full or short SHA)
# ✨ AI runs git show to retrieve commit details (message, files changed)
# ✨ AI generates professional task title based on description and commit
# ✨ AI generates task description with commit context (both full and short SHA)
# ✨ Review and confirm or override each generated field
# ✨ Provide completed hours
# ✨ Choose whether to subtract hours from placeholder task
#    - If yes, provide placeholder task ID
#    - AI retrieves current placeholder values
#    - AI calculates and updates new values
# ✨ Creates Task with completed work logged
# ✨ Shows success message with task and optional placeholder updates
# ✅ Done!
```

**Usage (Manual Mode):**

```
/ado-log-story-work

# Provide parent User Story ID
# Choose: Manual
# You'll be prompted for:
# - Task title (e.g., "Implement authentication endpoints")
# - Task description (e.g., "Added JWT token validation and refresh logic")
# - Completed hours (e.g., 3.5)
# - Subtract from placeholder? (yes/no)
#    - If yes: Placeholder task ID (e.g., 456)

# ✨ Creates Task with completed work logged
# ✨ Optionally updates placeholder task hours
# ✨ Shows Azure DevOps URLs for immediate viewing
# ✅ Done!
```

**Git Commit Hash Detection:**

The command automatically detects git commit hashes in your description:
- Supports both full SHA (40 characters) and short SHA (7+ characters)
- Common patterns: "commit abc123", "see commit 1a2b3c4", "hash: def456789"
- Runs `git show` to retrieve commit message and file changes
- Includes commit details in generated task description
- If git lookup fails, continues without commit context (non-blocking)

**Placeholder Task Hour Subtraction:**

When logging completed work, you can optionally subtract hours from a placeholder task:
- Useful for tracking hours from a pre-allocated hour bucket
- Subtracts from both "Original Estimate" and "Remaining Work" fields
- Calculates new values automatically (prevents negative values)
- Shows before/after comparison in success message
- Displays both task and placeholder task Azure DevOps links

**Requirements:**
- Must run `/ado-init` first to configure Azure DevOps settings
- Must have an existing User Story work item (create with `/ado-create-story`)
- Azure DevOps MCP server must be configured and running
- Git repository accessible (optional, for commit hash lookup)

### `/ado-timesheet-report` Command Details

**What it does:**

- Validates Azure DevOps configuration exists in CLAUDE.md
- Prompts for week definition (Monday-Sunday or Sunday-Saturday)
- Asks for time period (current week, last week, or specific week)
- **Offers flexible task filtering**:
  - Only closed tasks (best for completed work)
  - Only worked on tasks (best for in-progress work)
  - Both closed and worked on tasks (comprehensive view)
- **Supports multiple date fields**:
  - Closed Date (when task was marked as closed)
  - Changed Date (when task was last updated)
- Offers verbosity options (ID & Hours, ID/Title/Hours, or ID/Title/Description/Hours)
- Prompts for user selection (current user or specific team member)
- Queries Azure DevOps for work items matching the specified criteria
- Filters by "Completed Work" hours logged on work items
- Builds hierarchical tree structure (Feature > User Story > Task)
- Displays rolled-up hours at each parent level
- Handles orphaned work items under "No Parent" section

**Usage:**

```
/ado-timesheet-report

# Step 1: Configure report (4 questions asked together)
#   - Week definition: Monday-Sunday or Sunday-Saturday
#   - Time period: Current week, Last week, or Specific week
#   - Task filter type: Closed only, Worked on only, or Both
#   - Date field: Closed Date or Changed Date
# Step 1a: If you chose "Specific week", provide end date (YYYY-MM-DD)

# Step 2: Display options (3 questions asked together)
#   - Verbosity level: Level 1, 2, or 3
#   - Grouping mode: By hierarchy, By date, or By date with hierarchy
#   - User: Current user or Specific team member
# Step 2a: If you chose "Specific team member", provide their name

# ✨ Queries Azure DevOps with dynamic filters based on your selections
# ✨ Filters by user assignment and "Completed Work" hours
# ✨ Builds hierarchical tree structure with rolled-up totals
# ✨ Displays comprehensive report with summary statistics
# ✅ Done!
```

**Report Features:**

- **Flexible Task Filtering**: Choose between closed only, worked on only, or both types of tasks
- **Multiple Date Fields**: Use Closed Date for final work or Changed Date for recent updates
- **Three Grouping Modes**: Organize your report in the way that works best for you
  - **By hierarchy**: Traditional tree structure (Feature > User Story > Task) with rolled-up hours
  - **By date**: Flat list grouped by day of the week for daily time tracking
  - **By date with hierarchy**: Combine both - see the hierarchy within each day of the week
- **Multiple Verbosity Levels**: Choose the level of detail you need for your timesheet
- **Flexible Date Ranges**: Current week, last week, or any specific week
- **User Filtering**: Report on yourself or any team member
- **Orphaned Items**: Handles work items without parents gracefully
- **All Work Item Types**: Includes Tasks, Bugs, Issues, and any other types with logged hours
- **Supports Multiple Workflows**: Works whether your team closes tasks daily or logs hours incrementally

**Example Report (Verbosity Level 2, By Hierarchy):**

```
📊 Timesheet Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 Period: Jan 13, 2025 to Jan 19, 2025 (Monday-Sunday)
👤 User: John Smith
🔍 Filter: Both closed and worked on
📅 Date Field: Changed Date
⏱️  Total Hours: 38.5
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 Feature 101: User Authentication System (Total: 24.0h)
  📋 Story 102: Implement user login functionality (Total: 16.0h)
    ✓ Task 103: Implement JWT token validation - 8.0h
    ✓ Task 104: Add login API endpoint - 8.0h
  📋 Story 105: Password reset functionality (Total: 8.0h)
    ✓ Task 106: Email template for password reset - 4.0h
    ✓ Task 107: Reset token generation logic - 4.0h

📦 Feature 108: Dashboard Analytics (Total: 14.5h)
  📋 Story 109: User activity metrics (Total: 14.5h)
    ✓ Task 110: Database queries for metrics - 6.5h
    ✓ Task 111: Chart visualization components - 8.0h

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱️  Total Hours: 38.5
📊 Work Items: 9 (2 Features, 3 Stories, 4 Tasks)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Example Report (Verbosity Level 2, By Date):**

```
📊 Timesheet Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 Period: Jan 13, 2025 to Jan 19, 2025 (Monday-Sunday)
👤 User: John Smith
🔍 Filter: Both closed and worked on
📅 Date Field: Changed Date
⏱️  Total Hours: 38.5
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 Monday, Jan 13, 2025 (Total: 8.0h)
  • 103: Implement JWT token validation - 8.0h

📅 Tuesday, Jan 14, 2025 (Total: 12.0h)
  • 104: Add login API endpoint - 8.0h
  • 106: Email template for password reset - 4.0h

📅 Wednesday, Jan 15, 2025 (Total: 10.5h)
  • 107: Reset token generation logic - 4.0h
  • 110: Database queries for metrics - 6.5h

📅 Thursday, Jan 16, 2025 (Total: 8.0h)
  • 111: Chart visualization components - 8.0h

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱️  Total Hours: 38.5
📊 Work Items: 9 (2 Features, 3 Stories, 4 Tasks)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Requirements:**
- Must run `/ado-init` first to configure Azure DevOps settings
- Azure DevOps MCP server must be configured and running
- Work items must have "Completed Work" hours logged (state depends on filter choice)

**Use Cases:**

- **Daily Close & Log**: If your team creates and closes tasks daily, use "Closed only" filter with "Closed Date"
- **Incremental Logging**: If your team logs hours throughout the week on active tasks, use "Worked on only" or "Both" filter with "Changed Date"
- **Weekly Review**: For comprehensive timesheets, use "Both" filter to capture all work regardless of task state

---

## 🚀 Quick Start

### Prerequisites

1. **Node.js 20+**: Required for `npx` to run the Azure DevOps MCP server
   - Check your version: `node --version`
   - Download from: https://nodejs.org/

2. **Azure DevOps Access**: Ensure you have access to your Azure DevOps organization.

3. **MCP Configuration**: The `/ado-init` command can optionally create a `.mcp.json` file to configure the Microsoft Azure DevOps MCP server, which will use `npx` to run it automatically (no global installation required).

### Installation

```
/plugin install ai-ado@claude-code-plugins-dev
```

### Usage

```
# Step 1: Initialize Azure DevOps configuration
/ado-init

# Answer the prompts:
# - Organization: contoso
# - Project: MyProject
# - Team: Development Team
# - Area Path: MyProject\Team\Development
# - Iteration Path: MyProject\Sprint 1
# - Use decimal notation: Yes
# - Create .mcp.json: Yes
# - Operating System: Windows (or Linux)

# ✅ CLAUDE.md and .mcp.json are now configured!

# Restart Claude Code to apply settings

# Step 2: Create work items using the configured conventions
/ado-create-feature
# Creates a Feature work item

/ado-create-story
# Creates a User Story under a Feature

/ado-create-task
# Creates a Task under a User Story

# Step 3: Log completed work to user stories
/ado-log-story-work
# Rapidly log completed work with hours already set
```

---

## 💡 Features

### AI-Powered Work Item Generation

All work item creation commands (`/ado-create-feature`, `/ado-create-story`, `/ado-create-task`) now support **AI-powered generation mode**:

- **Intelligent Content Generation**: Describe what you want to build, and AI generates professional work item content
- **Naming Convention Compliance**: AI automatically follows your organization's naming conventions from CLAUDE.md
- **Review & Override**: Every AI-generated field is shown for confirmation before proceeding
- **Flexible Workflows**: Choose between AI generation or manual input for each work item
- **Context-Aware**: AI analyzes parent work items and project context for better quality

**What AI Generates:**

- **Features**: Professional titles and comprehensive descriptions
- **User Stories**: Titles, persona statements, background information, and acceptance criteria in Given/When/Then format
- **Tasks**: Descriptive titles focused on work to be done

### Core Skills

The plugin provides six slash commands for complete Azure DevOps work item lifecycle management:

1. **`/ado-init`**: Initialize Azure DevOps configuration with organization settings
2. **`/ado-create-feature`**: Create Feature work items with AI or manual input
3. **`/ado-create-story`**: Create User Story work items with AI-generated structured content
4. **`/ado-create-task`**: Create Task work items with AI-generated titles
5. **`/ado-log-story-work`**: Rapidly log completed work with git commit detection and placeholder hour tracking
6. **`/ado-timesheet-report`**: Generate weekly timesheet reports with hierarchical hour rollups

### `/ado-init` Command

#### Interactive Configuration

- Prompts for Azure DevOps organization name
- Collects project and team information
- Gathers default Area Path and Iteration Path
- Asks about naming convention preferences
- Optionally creates `.mcp.json` for MCP server configuration
- Detects operating system (Windows vs Linux/Mac) for correct MCP setup

#### Work Item Guidelines

Generates comprehensive guidelines for:

- **Three-level hierarchy**: Features → User Stories → Tasks
- **Feature requirements**: High-level descriptions summarizing contained stories
- **User Story format**: Persona statements, background, acceptance criteria
- **Task structure**: Lightweight containers for hour estimates
- **HTML formatting**: Proper formatting for all text fields

#### Naming Convention Standards

**With Decimal Notation** (recommended):

- Features: `1: Feature One`, `2: Feature Two`
- User Stories: `1.1: Story One`, `1.2: Story Two`, `2.1: Story One`
- Tasks: Descriptive titles without numbering

**Without Decimal Notation** (flexible):

- Features: Numbered for priority
- User Stories: Descriptive titles
- Tasks: Simple, descriptive titles

#### Hour Estimation & Tracking

Configures standards for:

- **Story Points**: Fibonacci sequence values on User Stories
- **Task estimates**: Identical values in "Original Estimate" and "Remaining Work"
- **Completed Work**: Left empty initially

#### MCP Integration

- Optionally creates `.mcp.json` configuration for automatic MCP server setup
- OS-aware: Uses correct command format for Windows (`cmd /c npx`) or Linux/Mac (`npx`)
- Uses `npx` to run `@azure-devops/mcp` without global installation
- Simple configuration with organization name
- Secure: Shows manual configuration snippet if `.mcp.json` already exists

---

## 📝 Work Item Creation Example

Once configured, Claude Code will create work items following your conventions:

**Feature:**
```
Title: 1: User Authentication System
Description: High-level overview of authentication features including login,
registration, password reset, and session management.
Area Path: MyProject\Team\Development
Iteration Path: MyProject\Sprint 1
State: New
```

**User Story:**
```
Title: 1.1: Implement user login functionality
Description:
As a website visitor, I want to log in with my email and password so that
I can access my personalized dashboard.

Background:
- System uses JWT tokens for authentication
- Session expires after 24 hours
- Failed login attempts are tracked

Acceptance Criteria:
Given a registered user with valid credentials
When they enter email and password on the login page
Then they should be authenticated and redirected to dashboard

Given a user with invalid credentials
When they attempt to login
Then they should see an error message
And their failed attempt should be logged

Story Points: 5
Area Path: MyProject\Team\Development
Iteration Path: MyProject\Sprint 1
State: New
```

**Task:**
```
Title: Development for user login functionality
Original Estimate: 8 hours
Remaining Work: 8 hours
Completed Work: (empty)
Area Path: MyProject\Team\Development
Iteration Path: MyProject\Sprint 1
State: New
```

---

## 🎓 Best Practices

### When to Use `/ado-init`

- ✅ Starting a new project or repository
- ✅ Standardizing work item conventions across team
- ✅ Onboarding new team members
- ✅ Switching to a new sprint or iteration
- ✅ Setting up consistent Azure DevOps workflows

### Configuration Tips

- Use **decimal notation** for better organization and sorting in backlog
- Set **Area Path** to match your team structure
- Configure **Iteration Path** to your current sprint
- Update configuration when changing sprints or team structure
- Re-run `/ado-init` to update settings for new projects

---

## ⏱️ Time Savings

**Per work item set (Feature + 3 Stories + 9 Tasks):**

- Manual Azure DevOps: ~45-60 minutes (research format, create items, set fields, establish hierarchy)
- With ai-ado (Manual Mode): ~5-10 minutes (follows conventions automatically)
- **With ai-ado (AI Mode): ~2-4 minutes** (AI generates content, you just review and confirm)

**Estimated savings with AI Mode:**

- Per sprint (3 feature sets): Save ~2.5-3 hours
- Per quarter: Save ~30-36 hours
- Per year: Save ~120-144 hours

**Additional benefits:**

- **AI-Generated Quality**: Professional, well-structured work items every time
- **Consistent Standards**: AI follows your naming conventions and formatting rules
- **Reduced Mental Load**: Focus on what to build, not how to write work items
- **Better Acceptance Criteria**: AI generates comprehensive Given/When/Then scenarios
- **Faster Onboarding**: New team members get professional work items without training
- **Fewer Mistakes**: AI handles hierarchy, HTML formatting, and field requirements
- **Better Backlog**: Consistent organization and priority sorting

---

## 🔧 Configuration

### MCP Server Setup

The `/ado-init` command can optionally create a `.mcp.json` file to configure the Microsoft Azure DevOps MCP server.

**Windows Configuration:**

```json
{
  "mcpServers": {
    "ado": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@azure-devops/mcp", "YOUR_ORGANIZATION"]
    }
  }
}
```

**Linux/Mac Configuration:**

```json
{
  "mcpServers": {
    "ado": {
      "command": "npx",
      "args": ["-y", "@azure-devops/mcp", "YOUR_ORGANIZATION"]
    }
  }
}
```

**How it works:**

- Asks if you're using Windows or Linux/Mac for correct command format
- If `.mcp.json` doesn't exist, it will be created with your organization name and OS-specific command
- If `.mcp.json` already exists, you'll get a manual configuration snippet to add (for security reasons, existing files are not read or modified)
- Uses `npx` to run the MCP server without requiring global installation
- Windows requires `cmd /c` prefix for proper npx execution

**Requirements:**

- Node.js 20 or higher must be installed for `npx` to work
- Check your version: `node --version`

**Security Note:**

For security reasons, the plugin will not read or modify existing `.mcp.json` files. If you already have this file, the command will show you the OS-appropriate configuration snippet to manually add.

### Authentication

First-time use of Azure DevOps MCP tools will open a browser for Microsoft account authentication. Credentials must match your Azure DevOps organization access.

---

## 🔮 Roadmap

Future commands and features planned for this plugin:

- **`/ado-sprint-plan`**: Sprint planning assistant with capacity planning
- **`/ado-pipeline`**: Pipeline management and monitoring helpers
- **`/ado-pr-create`**: Pull request creation with automatic work item linking
- **`/ado-test-plan`**: Test plan and case management
- **`/ado-wiki-sync`**: Documentation sync to Azure DevOps wiki
- **`/ado-query`**: Custom work item queries and filtering
- **`/ado-bulk-update`**: Batch update multiple work items

---

## 📦 Plugin Details

- **Name:** AI-ADO Plugin
- **Type:** AI Instruction Plugin (Skills)
- **Version:** 1.3.0
- **Skills:** `/ado-init`, `/ado-create-feature`, `/ado-create-story`, `/ado-create-task`, `/ado-log-story-work`, `/ado-timesheet-report`
- **MCP Integration:** Microsoft Azure DevOps MCP Server (optional, OS-aware configuration)
- **Requirements:** Node.js 20+
- **License:** MIT
- **Author:** Charles Jones

---

## 🔗 Related Resources

- [Microsoft Azure DevOps MCP Server](https://github.com/microsoft/azure-devops-mcp)
- [Azure DevOps Documentation](https://learn.microsoft.com/en-us/azure/devops/)
- [Work Item Types](https://learn.microsoft.com/en-us/azure/devops/boards/work-items/about-work-items)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

## 🤝 Contributing

Found a bug or have a suggestion? [Open an issue](https://github.com/charlesjones-dev/claude-code-plugins-dev/issues) or submit a pull request!

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for the Claude Code community**
