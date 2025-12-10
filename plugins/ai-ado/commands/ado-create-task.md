---
name: ado-create-task
description: "Interactively create a new Task work item as a child of an existing User Story in Azure DevOps."
---

# Create Azure DevOps Task

Interactively create a new Task work item as a child of an existing User Story in Azure DevOps using the organization's configured conventions and guidelines.

## Instructions

**CRITICAL**: This command MUST NOT accept any arguments. If the user provided any text, task titles, descriptions, IDs, or other arguments after this command (e.g., `/ado-create-task "My Task"` or `/ado-create-task 123`), you MUST COMPLETELY IGNORE them. Do NOT use any task titles, descriptions, IDs, or other arguments that appear in the user's message. You MUST ONLY gather requirements through the interactive prompts as specified below.

**BEFORE DOING ANYTHING ELSE**: Validate Azure DevOps configuration in CLAUDE.md, then begin gathering task information. DO NOT skip these steps even if the user provided arguments after the command.

This command creates a Task work item following the organization's Azure DevOps conventions defined in CLAUDE.md.

### Phase 1: Validate Azure DevOps Configuration

Before proceeding with task creation, verify that Azure DevOps configuration exists:

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
   - Store these values for use in task creation
   - Proceed to Phase 2

**IMPORTANT**:
- Use **Read tool** to check CLAUDE.md - DO NOT use bash commands
- The entire command should STOP if Azure DevOps configuration is not found
- Do not prompt the user for configuration values - they must run /ado-init first

### Phase 2: Gather Task Information

Collect task details from the user. The user can choose between AI-powered generation or manual input.

**Step 0 - Choose Input Method:**

Simply output the following text as your response message and STOP (DO NOT call any tools):

"Would you like to use AI to generate the Task title, or provide it manually?

Options:
1. AI-powered: Provide a description and let AI generate an appropriate task title
2. Manual: Provide the task title yourself

Please respond with 'AI' or 'Manual'."

Wait for the user's response before proceeding.

**If user chooses 'AI' (or similar affirmative response):**

**Step AI-0 - Get Parent User Story ID:**

Simply output the following text as your response message and STOP (DO NOT call any tools):

"What is the ID of the parent User Story for this Task?

(This is the numeric ID of the User Story work item that will contain this task. You can find this in Azure DevOps or from the output of /ado-create-story)"

Wait for the user's next message with the parent story ID before proceeding.

**Step AI-1 - Get Description Prompt:**

Simply output the following text as your response message and STOP:

"Please provide a description of what this Task should accomplish. I'll use this to generate an appropriate task title.

(Describe the specific work to be done. Examples: 'implement the login API endpoint', 'test authentication flows', 'create database migration for users table')"

Wait for the user's description, then:

1. Retrieve the parent User Story details to understand context
2. Generate a professional Task title that is:
   - Simple and descriptive
   - Focused on the work to be done
   - Follows common patterns like: 'Development for [feature]', 'QA testing for [feature]', 'Deploy [component]'
   - Clear and actionable

**Step AI-2 - Confirm Generated Title:**

Display the generated title and ask for confirmation:

"I've generated the following title based on your description:

**Title:** [GENERATED_TITLE]

Would you like to use this title, or would you prefer to provide your own?
(Type 'yes' to use this title, or provide an alternative title)"

Wait for response:
- If user approves (says "yes", "ok", "looks good", etc.), store the generated title
- If user provides alternative text, use that as the title instead

**Step AI-3 - Hour Estimate:**

Simply output the following text as your response message and STOP:

"What is the hour estimate for this Task?

(This value will be set for both 'Original Estimate' and 'Remaining Work' fields. Provide a numeric value in hours.)"

Wait for the user's next message with the hour estimate before proceeding to Phase 3.

**If user chooses 'Manual':**

**Step 1 - Parent User Story ID:**

Simply output the following text as your response message and STOP (DO NOT call any tools):

"What is the ID of the parent User Story for this Task?

(This is the numeric ID of the User Story work item that will contain this task. You can find this in Azure DevOps or from the output of /ado-create-story)"

Wait for the user's next message with the parent story ID before proceeding.

**Step 2 - Task Title:**

After receiving the parent story ID, simply output the following text as your response message and STOP (DO NOT call any tools):

"What is the title for this Task?

(Use a simple, descriptive title focused on the work to be done.
Examples: 'Development for user login functionality', 'QA testing for authentication', 'Deploy to staging environment')"

Wait for the user's next message with the task title before proceeding.

**Step 3 - Hour Estimate:**

After receiving the task title, simply output the following text as your response message and STOP (DO NOT call any tools):

"What is the hour estimate for this Task?

(This value will be set for both 'Original Estimate' and 'Remaining Work' fields. Provide a numeric value in hours.)"

Wait for the user's next message with the hour estimate before proceeding.

**IMPORTANT**:
- Simply output the question text in your response message and STOP - do NOT call ANY tools (except when generating AI content)
- DO NOT use the AskUserQuestion tool for any of these steps
- After outputting each question, wait for the user's next message before proceeding
- For AI mode: Generate task title based on user description and parent story context
- For AI mode: Always confirm generated content and allow user to override
- For AI mode: Parent User Story ID is still required before generating title
- Validate that required fields are provided (not empty)
- Parent User Story ID must be a valid number
- Hour estimate must be a valid number

### Phase 3: Create Task Work Item

Using the configuration from Phase 1 and the information from Phase 2, create the task work item:

1. Tasks should have minimal description as per Azure DevOps conventions:
   - Use a simple description: "Task for [STORY_TITLE]. See parent User Story for details."
   - Format as HTML: `<p>Task for [STORY_TITLE]. See parent User Story for details.</p>`

2. First, retrieve the parent User Story to get its title using **wit_get_work_item** MCP tool:
   - `id`: The parent story ID provided by user
   - `project`: Use the project name from Phase 1 configuration

3. Use the **wit_add_child_work_items** MCP tool with the following parameters:
   - `parentId`: The parent story ID provided by user (as number, not string)
   - `project`: Use the project name from Phase 1 configuration
   - `workItemType`: "Task"
   - `items`: Array containing a single item object with:
     - `title`: User-provided title
     - `description`: HTML-formatted description referencing parent story
     - `format`: "Html"
     - `areaPath`: Area Path from configuration
     - `iterationPath`: Iteration Path from configuration

4. After the task is created, use the **wit_update_work_item** MCP tool to set hour estimates:
   - `id`: The ID of the newly created task (from the response of wit_add_child_work_items)
   - `updates`: Array containing:
     - `{"op": "add", "path": "/fields/Microsoft.VSTS.Scheduling.OriginalEstimate", "value": "[HOUR_ESTIMATE]"}`
     - `{"op": "add", "path": "/fields/Microsoft.VSTS.Scheduling.RemainingWork", "value": "[HOUR_ESTIMATE]"}`

5. Wait for all MCP tool responses

**IMPORTANT**:
- Use the exact field names and paths shown above
- Retrieve parent story details first to reference in task description
- Ensure HTML formatting is applied to the description
- Parent ID must be converted to a number (not a string)
- Use configuration values from Phase 1, not hardcoded values
- Hour estimates must be set in a separate update operation after creation
- Both Original Estimate and Remaining Work should have identical values
- DO NOT set Completed Work field (leave empty initially)

### Phase 4: Display Success Message

After successful task creation, display a comprehensive success message:

```
✓ Task created successfully!

Task Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 ID: [TASK_ID]
📋 Title: [TASK_TITLE]
📖 Parent User Story: [PARENT_STORY_ID]
📂 Project: [PROJECT_NAME]
📍 Area Path: [AREA_PATH]
🔄 Iteration Path: [ITERATION_PATH]
⏱️  Original Estimate: [HOURS] hours
⏱️  Remaining Work: [HOURS] hours
✨ State: New
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next Steps:
1. Assign the task to a team member in Azure DevOps
2. Update progress and completed work as the task progresses
3. Create additional tasks for the story if needed

💡 To create another task for the same story:
   /ado-create-task
   (Parent User Story ID: [PARENT_STORY_ID])

🔗 View in Azure DevOps:
   https://dev.azure.com/[ORGANIZATION]/[PROJECT]/_workitems/edit/[TASK_ID]
```

Replace placeholders with actual values from the created task and configuration.

### Important Constraints

**DO NOT:**
- Proceed without Azure DevOps configuration in CLAUDE.md
- Use bash commands for file operations
- Create the task without user-provided information
- Use placeholder or empty values
- Call tools during Steps 1-3 (questions should be simple text output)
- Add detailed Description or Acceptance Criteria to tasks (tasks should reference parent story)
- Set different values for Original Estimate and Remaining Work
- Set Completed Work field (should remain empty initially)

**DO:**
- Use **Read tool** to check CLAUDE.md for Azure DevOps configuration
- Simply output question text and STOP for Steps 1-3 (no tool calls)
- Wait for user's response after each question before proceeding
- Use **wit_get_work_item** to retrieve parent story details
- Use **wit_add_child_work_items** MCP tool to create the task as a child of the story
- Use **wit_update_work_item** MCP tool to set hour estimates after creation
- Apply proper HTML formatting to description field
- Keep task descriptions lightweight and reference parent story
- Use configuration values from CLAUDE.md
- Show clear success message with task details
- Provide helpful next steps and links

### Error Handling

If the MCP tool returns an error:
- Display the error message to the user
- Suggest possible solutions:
  - Verify the parent User Story ID exists and is valid
  - Verify Azure DevOps MCP server is configured and running
  - Check that project and team names are correct
  - Ensure user has permissions to create work items
  - Verify Node.js 20+ is installed for MCP server
  - Check that hour estimate is a valid numeric value
- Recommend running /ado-init if configuration seems incorrect
- If parent ID is invalid, suggest using /ado-create-story first
