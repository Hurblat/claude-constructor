# Update Issue Command

## Purpose

Update the status of an issue in the configured issue tracking system.
This command is called by other orchestrating commands, and is one of the steps in a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Arguments

This command expects $ARGUMENTS in the following format:

```
Issue key: [issue_key]
New Status: [status_name]
```

Expected status values: "In Progress", "Code Review"

## Workflow Steps

1. **Parse Arguments**: Extract the issue key and new status from $ARGUMENTS

2. **Load Settings**: Read the Settings section in $ARGUMENTS to get the silent mode setting

3. **Check Silent Mode**:
   - If `silent-mode` is `true` in the configuration:
     - Log the status update operation locally: "Silent mode: Would have updated [issue_key] status to '[new_status]'"
     - Skip the actual API calls (step 4)
     - Continue to step 5

4. **Execute Update Status Operation** (only if silent mode is false):

### For Linear Provider (`"linear"`)
- First, use `linear:list_issue_statuses` to get all available statuses for the issue
- Find the best match for the new status from $ARGUMENTS (handles typos/variations)
- Use `linear:update_issue` to set the issue to the matched status
- If no exact match is found, use the closest matching status name

### For Jira Provider (`"jira"`)
- First, use `jira:get_transitions_for_issue` to get all available columns for the issue
- Find the best match for the new status from $ARGUMENTS (handles typos/variations)
- Use `jira:transition_issue` to move the issue to the matched transition
- If no exact match is found, use the closest matching status name

5. **Output Results**: Display confirmation of the status update:
   - **Issue**: [issue_key]
   - **Previous Status**: [if available]
   - **New Status**: [updated_status]
   - **Result**: Success/Failure (or "Skipped - Silent Mode" if applicable)

6. **Error Handling**: If the issue operation fails, log the error but continue gracefully

7. **Report DONE** to the orchestrating command

## Usage Example

From other commands, call this command with:

```markdown
run the .claude/commands/issue/update_issue.md command, passing these arguments:
Issue Key: ABC-123
New Status: Code Review
```