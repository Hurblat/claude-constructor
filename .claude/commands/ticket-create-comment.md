# Ticket Create Comment Command

## Purpose

Add a comment to a ticket in the configured ticket system.
This command is called by other orchestrating commands, and is one of the steps in a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Arguments

This command expects $ARGUMENTS in the following format:

```
Ticket Number: [ticket_key_or_id]
Comment Text: [comment_content]
```

## Workflow Steps

1. **Parse Arguments**: Extract the ticket number and comment text from $ARGUMENTS

2. **Load Configuration**: Read `.claude/settings.claude-constructor.json` to determine the ticket provider

3. **Execute Create Comment Operation**:

### For Linear Provider (`"linear"`)
- Use `linear:create_comment` with the ticket ID and comment text from $ARGUMENTS
- Add the comment to the specified ticket

4. **Output Results**: Display confirmation of the comment creation:
   - **Ticket**: [ticket_number]
   - **Comment Added**: [comment_preview - first 100 characters]
   - **Result**: Success/Failure

5. **Error Handling**: If the ticket operation fails, log the error but continue gracefully

6. **Report DONE** to the orchestrating command

## Usage Example

From other commands, call this command with:

```markdown
run the .claude/commands/ticket_create_comment.md command, passing these arguments:
Ticket Number: ABC-123
Comment Text: Claude Code implementation started for specification_ABC-123_20240101.md
```