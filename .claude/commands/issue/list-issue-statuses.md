# List Issue Statuses Command

## Purpose

List all available statuses for an issue in the configured issue tracking system.
This command is called by other orchestrating commands, and is one of the steps in a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Arguments

This command expects $ARGUMENTS in the following format:

```
Issue Key: [issue_key]
```

## Workflow Steps

1. **Parse Arguments**: Extract the issue key from $ARGUMENTS

2. **Load Configuration**: Read `.claude/settings.claude-constructor.json` to determine the issue tracking provider

3. **Execute List Statuses Operation**:

### For Linear Provider (`"linear"`)
- Use `linear:list_issue_statuses` with the issue key from $ARGUMENTS
- Retrieve all available status names for the issue

4. **Output Results**: Display the available statuses:
   - **Issue**: [issue_key]
   - **Available Statuses**: 
     - [status_1]
     - [status_2]  
     - [status_3]
     - ...

5. **Error Handling**: If the issue operation fails, log the error but return default workflow statuses

6. **Report DONE** to the orchestrating command

## Usage Example

From other commands, call this command with:

```markdown
run the .claude/commands/issue/list_issue_statuses.md command, passing these arguments:
Issue Key: ABC-123
```