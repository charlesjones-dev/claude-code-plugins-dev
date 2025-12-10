---
name: ado-create-feature
description: "Interactively create a new Feature work item in Azure DevOps using configured conventions."
---

# Create Azure DevOps Feature

Interactively create a new Feature work item in Azure DevOps using the organization's configured conventions and guidelines.

## Instructions

**CRITICAL**: This command MUST NOT accept any arguments. If the user provided any text, feature titles, descriptions, or IDs after this command (e.g., `/ado-create-feature "My Feature"` or `/ado-create-feature 123`), you MUST COMPLETELY IGNORE them. Do NOT use any feature titles, descriptions, or other arguments that appear in the user's message. You MUST ONLY gather requirements through the interactive prompts as specified below.

**BEFORE DOING ANYTHING ELSE**: Validate Azure DevOps configuration in CLAUDE.md, then begin gathering feature information. DO NOT skip these steps even if the user provided arguments after the command.

This command creates a Feature work item following the organization's Azure DevOps conventions defined in CLAUDE.md.

### Phase 1: Validate Azure DevOps Configuration

Before proceeding with feature creation, verify that Azure DevOps configuration exists:

1. Use the **Read tool** to read `CLAUDE.md` from the project root
2. If the file doesn't exist OR doesn't contain an "## Azure DevOps" section:
   - Display the following error message:
     ```
     ❌ Azure DevOps configuration not found

     CLAUDE.md does not contain Azure DevOps configuration.

     Please run /ado-init first to configure Azure DevOps settings for this project.

     The /ado-init command will:
     - Configure your organization, project, and team
     - Set up Area Path and Iteration Path defaults
     - Define naming conventions and work item guidelines
     - Optionally configure the Azure DevOps MCP server
     ```
   - **STOP** and do not proceed further

3. If Azure DevOps section exists:
   - Parse the CLAUDE.md content to extract configuration values:
     - Organization name (look for text after 'specify the organization as "')
     - Project name (look for text after 'the project as "')
     - Team name (look for text after 'the team as "')
     - Area Path (look for text after 'Area Path" set to "')
     - Iteration Path (look for text after 'Iteration Path" set to "')
     - Naming convention preference (check if "Use decimal notation" or "Use descriptive" appears in naming section)
   - Store these values for use in feature creation
   - Proceed to Phase 2

**IMPORTANT**:
- Use **Read tool** to check CLAUDE.md - DO NOT use bash commands
- The entire command should STOP if Azure DevOps configuration is not found
- Do not prompt the user for configuration values - they must run /ado-init first

### Phase 2: Gather Feature Information

Collect feature details from the user. The user can choose between AI-powered generation or manual input.

**Step 0 - Choose Input Method:**

Simply output the following text as your response message and STOP (DO NOT call any tools):

"Would you like to use AI to generate the Feature details, or provide them manually?

Options:
1. AI-powered: Provide a description and let AI generate the title and description
2. Manual: Provide title and description yourself

Please respond with 'AI' or 'Manual'."

Wait for the user's response before proceeding.

**If user chooses 'AI' (or similar affirmative response):**

**Step AI-1 - Get Description Prompt:**

Simply output the following text as your response message and STOP:

"Please provide a description or overview of what this Feature should accomplish. I'll use this to generate a professional title and detailed description.

(Provide as much context as you'd like - the more detail you provide, the better the generated content will be.)"

Wait for the user's description, then:

1. Analyze the naming convention from Phase 1 configuration
2. Generate a professional Feature title following the naming convention (e.g., "1: Feature Name" for decimal notation)
3. Generate a comprehensive feature description that:
   - Summarizes the feature's purpose
   - Describes what user stories it will contain
   - Provides an overview without excessive fine details
   - Is clear and suitable for stakeholders

**Step AI-2 - Confirm Generated Title:**

Display the generated title and ask for confirmation:

"I've generated the following title based on your description:

**Title:** [GENERATED_TITLE]

Would you like to use this title, or would you prefer to provide your own?
(Type 'yes' to use this title, or provide an alternative title)"

Wait for response:
- If user approves (says "yes", "ok", "looks good", etc.), store the generated title
- If user provides alternative text, use that as the title instead

**Step AI-3 - Confirm Generated Description:**

Display the generated description and ask for confirmation:

"I've generated the following description:

**Description:**
[GENERATED_DESCRIPTION]

Would you like to use this description, or would you prefer to provide your own?
(Type 'yes' to use this description, or provide an alternative description)"

Wait for response:
- If user approves (says "yes", "ok", "looks good", etc.), store the generated description
- If user provides alternative text, use that as the description instead

Then proceed to Phase 3 with the final values.

**If user chooses 'Manual':**

**Step 1 - Feature Title:**

Simply output the following text as your response message and STOP (DO NOT call any tools):

"What is the title for this Feature?

(Based on your naming convention, use an appropriate format. For decimal notation, use: '1: Feature Name', '2: Feature Name', etc.)"

Wait for the user's next message with the feature title before proceeding.

**Step 2 - Feature Description:**

After receiving the feature title, simply output the following text as your response message and STOP (DO NOT call any tools):

"What is the high-level description for this Feature?

(Provide a summary of the feature's purpose and the user stories it will contain. This should be an overview without fine details.)"

Wait for the user's next message with the feature description before proceeding.

**IMPORTANT**:
- Simply output the question text in your response message and STOP - do NOT call ANY tools (except when generating AI content)
- DO NOT use the AskUserQuestion tool for any of these steps
- After outputting each question, wait for the user's next message before proceeding
- For AI mode: Generate content intelligently based on user's description and naming conventions
- For AI mode: Always confirm generated content and allow user to override
- Validate that title and description are provided (not empty)

### Phase 3: Create Feature Work Item

Using the configuration from Phase 1 and the information from Phase 2, create the feature work item:

1. Format the description as HTML for proper Azure DevOps display:
   - Wrap the description in `<p>` tags
   - Convert line breaks to `<br/>` tags
   - If the description contains bullet points (lines starting with `-` or `*`), wrap them in `<ul>` and `<li>` tags

2. Use the **wit_create_work_item** MCP tool with the following parameters:
   - `project`: Use the project name from Phase 1 configuration
   - `workItemType`: "Feature"
   - `fields`: Array containing these field objects:
     - Title field: `{"name": "System.Title", "value": "[USER_PROVIDED_TITLE]"}`
     - Description field: `{"name": "System.Description", "value": "[HTML_FORMATTED_DESCRIPTION]", "format": "Html"}`
     - Area Path field: `{"name": "System.AreaPath", "value": "[AREA_PATH_FROM_CONFIG]"}`
     - Iteration Path field: `{"name": "System.IterationPath", "value": "[ITERATION_PATH_FROM_CONFIG]"}`
     - State field: `{"name": "System.State", "value": "New"}`

3. Wait for the MCP tool response

**IMPORTANT**:
- Use the exact field names shown above (e.g., "System.Title", "System.Description")
- Ensure HTML formatting is applied to the description for readability
- Use configuration values from Phase 1, not hardcoded values
- The format parameter for Description must be "Html"

### Phase 4: Display Success Message

After successful feature creation, display a comprehensive success message:

```
✓ Feature created successfully!

Feature Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 ID: [FEATURE_ID]
📋 Title: [FEATURE_TITLE]
📂 Project: [PROJECT_NAME]
📍 Area Path: [AREA_PATH]
🔄 Iteration Path: [ITERATION_PATH]
✨ State: New
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next Steps:
1. Create User Stories under this Feature using /ado-create-story
2. Review the feature in Azure DevOps web interface
3. Add additional details or attachments as needed

💡 To create a user story for this feature:
   /ado-create-story
   (You'll be prompted for parent Feature ID: [FEATURE_ID])

🔗 View in Azure DevOps:
   https://dev.azure.com/[ORGANIZATION]/[PROJECT]/_workitems/edit/[FEATURE_ID]
```

Replace placeholders with actual values from the created feature and configuration.

### Important Constraints

**DO NOT:**
- Proceed without Azure DevOps configuration in CLAUDE.md
- Use bash commands for file operations
- Create the feature without user-provided title and description
- Use placeholder or empty values
- Call tools during Steps 1-2 (questions should be simple text output)

**DO:**
- Use **Read tool** to check CLAUDE.md for Azure DevOps configuration
- Simply output question text and STOP for Steps 1-2 (no tool calls)
- Wait for user's response after each question before proceeding
- Use **wit_create_work_item** MCP tool to create the feature
- Apply proper HTML formatting to description field
- Use configuration values from CLAUDE.md
- Show clear success message with feature details
- Provide helpful next steps and links

### Error Handling

If the MCP tool returns an error:
- Display the error message to the user
- Suggest possible solutions:
  - Verify Azure DevOps MCP server is configured and running
  - Check that project and team names are correct
  - Ensure user has permissions to create work items
  - Verify Node.js 20+ is installed for MCP server
- Recommend running /ado-init if configuration seems incorrect
