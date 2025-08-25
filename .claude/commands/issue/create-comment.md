# Create Issue Comment Command

## Purpose

Add a comment to an issue in the configured issue tracking system.
This command is called by other orchestrating commands, and is one of the steps in a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Arguments

This command expects $ARGUMENTS in the following format:

```
Issue Key: [issue_key]
Comment Text: [comment_content]
```

## Workflow Steps

1. **Parse Arguments**: Extract the issue key and comment text from $ARGUMENTS

2. **Load Settings**: Read the Settings section in $ARGUMENTS to get the silent mode setting

3. **Check Silent Mode**: 
   - If `silent-mode` is `true` in the configuration:
     - Log the comment operation locally: "Silent mode: Would have added comment to [issue_key]: [comment_preview]"
     - Skip the actual API call (step 4)
     - Continue to step 5

4. **Execute Create Comment Operation** (only if silent mode is false):

### For Linear Provider (`"linear"`)
- Use `linear:create_comment` with the issue ID and comment text from $ARGUMENTS
- Add the comment to the specified issue

### For Jira Provider (`"jira"`)
- Use `jira:add_comment_to_issue` with the issue key and comment text from $ARGUMENTS
- Add the comment to the specified issue

5. **Output Results**: Display confirmation of the comment creation:
   - **Issue**: [issue_key]
   - **Comment Added**: [comment_preview - first 100 characters] 
   - **Result**: Success/Failure (or "Skipped - Silent Mode" if applicable)

6. **Error Handling**: If the issue operation fails, log the error but continue gracefully

7. **Report DONE** to the orchestrating command

## Usage Example

From other commands, call this command with:

```markdown
run the .claude/commands/issue/create_comment.md command, passing these arguments:
Issue Key: ABC-123
Comment Text: Claude Code implementation started for specification_ABC-123_20240101.md
```