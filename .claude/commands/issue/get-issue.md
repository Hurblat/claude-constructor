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

2. **Load Configuration**: Read `.claude/settings.claude-constructor.json` to determine the issue tracking provider

3. **Execute Get Issue Operation**:

### For Prompt Issue Provider (`"prompt-issue"`)
- Prompt the user: "Please provide the following details for your feature/task:"
- Ask for:
  - **Title**: What feature or task are you implementing?
  - **Description**: Provide detailed description of requirements, acceptance criteria, and any technical constraints
- Use the provided issue key from $ARGUMENTS as both key and ID
- Continue to step 4 with the user-provided information

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