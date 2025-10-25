---
name: update-issue
description: Update issue status in tracking system
argument-hint: [issue-key] [status] [state-management-file-path]
model: claude-haiku-4-5
allowed-tools: Read, Bash(echo:*)
---

# Update Issue Command

## Purpose

Update the status of an issue in the configured issue tracking system.
This command is called by other orchestrating commands, and is one of the steps in a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

Expected status values: "In Progress", "Code Review"

## Arguments

- `$1`: Issue key (required)
- `$2`: Status to set (required)
- `$3`: Path to state management file (required)

## Workflow Steps

1. **Read Settings from State Management File**:
   - Read the Settings section from the state management file ($3)
   - Extract `issueTrackingProvider` and `silentMode` values
   - If Settings section is missing, fail with error: "Settings not found in state management file. Run /read-settings first."

2. **Validate Provider Configuration**:
   - If issueTrackingProvider is "linear":
     - Check that Linear MCP tools are available
     - If NOT available: **FAIL with error**: "Provider is 'linear' but Linear MCP tools are not configured. Please configure Linear MCP or update settings with /read-settings --provider=prompt"
   - If issueTrackingProvider is "jira":
     - Check that Jira MCP tools are available
     - If NOT available: **FAIL with error**: "Provider is 'jira' but Jira MCP tools are not configured. Please configure Jira MCP or update settings with /read-settings --provider=prompt"

3. **Check Silent Mode or Prompt Issue Provider**:
   - If silentMode is true OR issueTrackingProvider is "prompt":
     - Log the status update operation locally: "Silent mode: Would have updated $1 status to '$2'"
     - Skip the actual API calls (step 4)
     - Continue to step 5

4. **Execute Update Status Operation** (only if silentMode is false and issueTrackingProvider is not "prompt"):

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

5. **Output Results**: Display confirmation of the status update:
   - **Issue**: $1
   - **Previous Status**: [if available]
   - **New Status**: $2
   - **Result**: Success/Failure (or "Skipped - Silent Mode" if applicable)

6. **Error Handling**: If the issue operation fails, log the error but continue gracefully
