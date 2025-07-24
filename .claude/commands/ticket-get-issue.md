# Ticket Get Issue Command

## Purpose

Retrieve issue details from the configured ticket system for a given ticket number.
This command is called by other orchestrating commands, and is one of the steps in a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Arguments

This command expects $ARGUMENTS in the following format:

```
Ticket Number: [ticket_key_or_id]
```

## Workflow Steps

1. **Parse Arguments**: Extract the ticket number from $ARGUMENTS

2. **Load Configuration**: Read `.claude/settings.claude-constructor.json` to determine the ticket provider

3. **Execute Get Issue Operation**:

### For Linear Provider (`"linear"`)
- Use `linear:get_issue` with the ticket number from $ARGUMENTS
- Retrieve issue key, ID, title, and description

4. **Output Results**: Display the issue information in this format:
   - **Key**: Issue key
   - **ID**: Issue ID  
   - **Title**: Issue title
   - **Description**: Issue description

5. **Error Handling**: If the ticket operation fails, log the error but continue gracefully

6. **Report DONE** to the orchestrating command

## Usage Example

From other commands, call this command with:

```markdown
run the .claude/commands/ticket_get_issue.md command, passing these arguments:
Ticket Number: ABC-123
```