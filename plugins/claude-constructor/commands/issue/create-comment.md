---
name: create-comment
description: Add comment to issue in tracking system
argument-hint: [issue-key] "[comment-text]"
model: claude-3-5-haiku-latest
allowed-tools: Bash(echo:*)
---

# Create Issue Comment Command

## Purpose

Add a comment to an issue in the configured issue tracking system.
This command is called by other orchestrating commands, and is one of the steps in a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

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
     - Log the comment operation locally: "Silent mode: Would have added comment to $1: $2"
     - Skip the actual API call (step 3)
     - Continue to step 4

3. **Execute Create Comment Operation** (only if silent mode is false):

### For Linear Provider (`"linear"`)
- Use `linear:create_comment` with $1 (issue ID) and $2 (comment text)
- Add the comment to the specified issue

### For Jira Provider (`"jira"`)
- Use `jira:add_comment_to_issue` with $1 (issue key) and $2 (comment text)
- Add the comment to the specified issue

4. **Output Results**: Display confirmation of the comment creation:
   - **Issue**: $1
   - **Comment Added**: $2
   - **Result**: Success/Failure (or "Skipped - Silent Mode" if applicable)

5. **Error Handling**: If the issue operation fails, log the error but continue gracefully
