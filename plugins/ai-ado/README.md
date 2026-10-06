# AI-ADO Plugin

**Azure DevOps work items from Claude Code.** Set up a project, create Features, User Stories and Tasks through the Azure DevOps MCP server, log hours to stories, and build weekly timesheets.

---

## What This Plugin Does

The skills work through Microsoft's official Azure DevOps MCP server. Run `/ado-init` first: the other skills, except `/ado-work-items`, read their settings from `CLAUDE.md` and stop if they're missing.

## Available Skills

### `/ado-init`

Initialize Azure DevOps configuration by creating or updating `CLAUDE.md` with your organization, project, team, default paths and naming convention.

**What it does:**

- Asks for your organization, project and team
- Sets the default Area Path and Iteration Path for work items
- Sets the naming convention (decimal notation or descriptive names)
- Optionally creates `.mcp.json` for the Azure DevOps MCP server, after asking which OS you use
- Points Claude Code to `/ado-work-items` for hierarchy, HTML formatting and estimation rules
- Stops without changes if `CLAUDE.md` already has an Azure DevOps section

**Naming conventions:**

- **Decimal notation** (recommended): Features `1: Feature One`, `2: Feature Two`; User Stories `1.1: Story One`, `1.2: Story Two`, `2.1: Story One`; Tasks get descriptive titles without numbering
- **Descriptive names**: Features are numbered for priority; User Stories and Tasks get descriptive titles

The three create skills below and `/ado-log-story-work` ask whether to use AI or Manual mode. In AI mode you describe the work, Claude drafts the fields using your naming convention, and you confirm or override each one. In Manual mode you type each field.

### `/ado-create-feature`

Create a Feature work item following your configured conventions.

**What it does:**

- Asks for the title and description, or drafts them in AI mode
- Creates the Feature with HTML formatting
- Sets Area Path, Iteration Path, and State automatically
- Shows the work item ID and its Azure DevOps link

### `/ado-create-story`

Create a User Story as a child of an existing Feature.

**What it does:**

- Asks for the parent Feature ID
- Asks for the title, persona statement ("As a... I want to... so that..."), background, and Given/When/Then acceptance criteria, or drafts them in AI mode
- Asks for Story Points (1, 2, 3, 5, 8, 13, etc.)
- Creates the User Story linked to the Feature, with HTML formatting
- Sets Area Path, Iteration Path, and State automatically

### `/ado-create-task`

Create a Task as a child of an existing User Story, with an hour estimate.

**What it does:**

- Asks for the parent User Story ID, the title (drafted in AI mode) and an hour estimate
- In AI mode, reads the parent User Story before drafting the title
- Sets Original Estimate and Remaining Work to same value
- Leaves Completed Work empty (to be filled during progress)
- Sets Area Path, Iteration Path, and State automatically
- Keeps task description lightweight (references parent story)

### `/ado-log-story-work`

Log completed work to a User Story by creating a Task with completed hours already set. Built for logging several times a day.

**What it does:**

- Asks for the parent User Story ID, the title and description (drafted in AI mode), and the completed hours
- Sets Original Estimate and Completed Work to the same value
- Leaves Remaining Work empty (work is already complete)
- Optionally subtracts hours from a placeholder task's Original Estimate and Remaining Work
- Shows the new task and any placeholder changes, with Azure DevOps links

**Git Commit Hash Detection:**

In AI mode, the skill looks for git commit hashes in your description:
- Supports both full SHA (40 characters) and short SHA (7+ characters)
- Common patterns: "commit abc1234", "see commit 1a2b3c4", "hash: def456789"
- Runs `git show` and adds the commit message and changed files to the task description
- If git lookup fails, continues without commit context (non-blocking)

**Placeholder Task Hour Subtraction:**

- Useful for tracking hours from a pre-allocated hour bucket
- Subtracts from both "Original Estimate" and "Remaining Work", never going below zero
- Shows before/after values and links to both tasks

### `/ado-work-items`

Reference guide for creating Azure DevOps work items with the ADO MCP tools. Covers the Feature → User Story → Task hierarchy, required HTML formatting for Description and Acceptance Criteria fields, naming conventions, and Story Points and hour estimation standards.

### `/ado-timesheet-report`

Report the "Completed Work" hours logged on work items during a given week, as a Feature > User Story > Task tree with rolled-up hours or grouped by day.

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
#   - Verbosity level: 1 (ID, hours), 2 (adds title), or 3 (adds description)
#   - Grouping mode: By hierarchy, By date, or By date with hierarchy
#   - User: Current user or Specific team member
# Step 2a: If you chose "Specific team member", provide their name
```

**Report Features:**

- **Date Fields**: Closed Date (when the task was closed) or Changed Date (when it was last updated)
- **Three Grouping Modes**:
  - **By hierarchy**: Feature > User Story > Task tree with rolled-up hours
  - **By date**: Flat list grouped by day of the week
  - **By date with hierarchy**: The hierarchy within each day of the week
- **All Work Item Types**: Includes Tasks, Bugs, Issues, and any other types with logged hours
- **Orphaned Items**: Work items without a parent go under a "No Parent" section

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
📊 Work Items: 11 (2 Features, 3 Stories, 6 Tasks)
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
📊 Work Items: 11 (2 Features, 3 Stories, 6 Tasks)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Use Cases:**

- **Daily Close & Log**: If your team creates and closes tasks daily, use "Closed only" filter with "Closed Date"
- **Incremental Logging**: If your team logs hours throughout the week on active tasks, use "Worked on only" or "Both" filter with "Changed Date"

---

## Quick Start

### Prerequisites

1. **Node.js 20+**: Required for `npx` to run the Azure DevOps MCP server
   - Check your version: `node --version`
   - Download from: https://nodejs.org/

2. **Azure DevOps Access**: Ensure you have access to your Azure DevOps organization.

3. **MCP Configuration**: `/ado-init` can create `.mcp.json` for you (see [MCP Server Setup](#mcp-server-setup)).

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

# CLAUDE.md and .mcp.json are now configured

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
# Logs completed work with hours already set
```

---

## Work Item Creation Example

Once configured, Claude Code creates work items following your conventions:

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

## Best Practices

- Use **decimal notation** for better organization and sorting in backlog
- Set **Area Path** to match your team structure
- Configure **Iteration Path** to your current sprint
- When sprints or teams change, edit the Azure DevOps section of `CLAUDE.md` (`/ado-init` won't overwrite it)
- Run `/ado-init` in each new project

---

## Configuration

### MCP Server Setup

`/ado-init` can optionally create a `.mcp.json` file to configure the Microsoft Azure DevOps MCP server.

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

- Asks whether you're on Windows or Linux/Mac to pick the command format
- If `.mcp.json` doesn't exist, it will be created with your organization name and OS-specific command
- If `.mcp.json` already exists, you'll get a manual configuration snippet to add (for security reasons, existing files aren't read or modified)
- Uses `npx` to run the MCP server without requiring global installation
- Windows needs the `cmd /c` prefix to run `npx`

**Security Note:**

For security reasons, the plugin won't read or modify existing `.mcp.json` files. If you already have this file, `/ado-init` shows you the OS-appropriate configuration snippet to add manually.

### Authentication

See the [Azure DevOps MCP server](https://github.com/microsoft/azure-devops-mcp) docs to set up authentication with your Azure DevOps account.

---

## Plugin Details

- **Name:** AI-ADO Plugin
- **Type:** AI Instruction Plugin (Skills)
- **Version:** 1.3.3
- **Skills:** `/ado-init`, `/ado-create-feature`, `/ado-create-story`, `/ado-create-task`, `/ado-log-story-work`, `/ado-work-items`, `/ado-timesheet-report`
- **MCP Integration:** Microsoft Azure DevOps MCP Server (optional, OS-aware configuration)
- **Requirements:** Node.js 20+
- **License:** MIT
- **Author:** Charles Jones

---

## Related Resources

- [Microsoft Azure DevOps MCP Server](https://github.com/microsoft/azure-devops-mcp)
- [Azure DevOps Documentation](https://learn.microsoft.com/en-us/azure/devops/)
- [Work Item Types](https://learn.microsoft.com/en-us/azure/devops/boards/work-items/about-work-items)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

## Contributing

Bug reports and fixes are welcome. See [CONTRIBUTING.md](../../CONTRIBUTING.md).

---

## License

MIT License - See [LICENSE](LICENSE) file for details.
