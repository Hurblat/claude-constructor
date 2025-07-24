# Ticket Update Issue Command

## Purpose

Update the status of a ticket in the configured ticket system.
This command is called by other orchestrating commands, and is one of the steps in a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Arguments

This command expects $ARGUMENTS in the following format:

```
Ticket Number: [ticket_key_or_id]
New Status: [status_name]
```

Expected status values: "In Progress", "Code Review", "Ready For Human Review"

## Workflow Steps

1. **Parse Arguments**: Extract the ticket number and new status from $ARGUMENTS

2. **Load Configuration**: Read `.claude/settings.claude-constructor.json` to determine the ticket provider

3. **Execute Update Status Operation**:

### For Linear Provider (`"linear"`)
- First, use `linear:list_issue_statuses` to get all available statuses for the ticket
- Find the best match for the new status from $ARGUMENTS (handles typos/variations)
- Use `linear:update_issue` to set the ticket to the matched status
- If no exact match is found, use the closest matching status name

4. **Output Results**: Display confirmation of the status update:
   - **Ticket**: [ticket_number]
   - **Previous Status**: [if available]
   - **New Status**: [updated_status]
   - **Result**: Success/Failure

5. **Error Handling**: If the ticket operation fails, log the error but continue gracefully

6. **Report DONE** to the orchestrating command

## Usage Example

From other commands, call this command with:

```markdown
run the .claude/commands/ticket_update_issue.md command, passing these arguments:
Ticket Number: ABC-123
New Status: Code Review
```