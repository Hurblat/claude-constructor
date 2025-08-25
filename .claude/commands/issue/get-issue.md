# Get Issue Command

## Purpose

Retrieve issue details from the configured issue tracking system for a given issue key.
This command is called by other orchestrating commands, and is one of the steps in a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Arguments

This command expects $ARGUMENTS in the following format:

```
Issue Key: [issue_key]
```

## Workflow Steps

1. **Parse Arguments**: Extract the issue key from $ARGUMENTS

1. **Load Settings**: Read the Settings section in $ARGUMENTS to get the issue tracking provider setting

3. **Execute Get Issue Operation**:

### For Linear Provider (`"linear"`)
- Use `linear:get_issue` with the issue key from $ARGUMENTS
- Retrieve issue key, ID, title, and description

### For Jira Provider (`"jira"`)
- Use `jira:get_issue` with the issue key from $ARGUMENTS
- Retrieve issue key, ID, title, and description

4. **Output Results**: Display the issue information in this format:
   - **Key**: Issue key
   - **ID**: Issue ID
   - **Title**: Issue title
   - **Description**: Issue description

5. **Error Handling**: If the issue operation fails, log the error but continue gracefully

6. **Report DONE** to the orchestrating command

## Usage Example

From other commands, call this command with:

```markdown
run the .claude/commands/issue/get_issue.md command, passing these arguments:
Issue Key: ABC-123
```