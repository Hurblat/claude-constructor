---
name: update-issue
description: Update issue status in tracking system
argument-hint: [issue-key] [status]
model: claude-3-5-haiku-latest
allowed-tools: Bash(echo:*)
---

# Update Issue Command

## Purpose

Update the status of an issue in the configured issue tracking system.
This command is called by other orchestrating commands, and is one of the steps in a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

Expected status values: "In Progress", "Code Review"

## Workflow Steps

1. **Determine Settings**:

   **Silent Mode:**
   - Check `CLAUDE_CONSTRUCTOR_SILENT_MODE` environment variable
   - If not set or "false" → silent mode is false
   - If "true" or "1" → silent mode is true

   **Issue Tracking Provider:**
   - Check `CLAUDE_CONSTRUCTOR_PROVIDER` environment variable
   - Validate it's one of: "linear", "jira", "prompt"
   - If not set or invalid, auto-detect:
     - If Linear MCP tools are available → use "linear"
     - If Jira MCP tools are available → use "jira"
     - Otherwise → use "prompt"

2. **Check Silent Mode or Prompt Issue Provider**:
   - If silent mode is true OR provider is "prompt":
     - Log the status update operation locally: "Silent mode: Would have updated $1 status to '$2'"
     - Skip the actual API calls (step 3)
     - Continue to step 4

3. **Execute Update Status Operation** (only if silent mode is false):

### For Linear Provider (`"linear"`)
- First, use `linear:list_issue_statuses` to get all available statuses for $1
- Find the best match for $2 (handles typos/variations)
- Use `linear:update_issue` with $1 to set the issue to the matched status
- If no exact match is found, use the closest matching status name

### For Jira Provider (`"jira"`)
- First, use `jira:get_transitions_for_issue` with $1 to get all available columns
- Find the best match for $2 (handles typos/variations)
- Use `jira:transition_issue` with $1 to move the issue to the matched transition
- If no exact match is found, use the closest matching status name

4. **Output Results**: Display confirmation of the status update:
   - **Issue**: $1
   - **Previous Status**: [if available]
   - **New Status**: $2
   - **Result**: Success/Failure (or "Skipped - Silent Mode" if applicable)

5. **Error Handling**: If the issue operation fails, log the error but continue gracefully