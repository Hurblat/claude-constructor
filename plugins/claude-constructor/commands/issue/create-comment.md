---
name: create-comment
description: Add comment to issue in tracking system
argument-hint: [issue-key] "[comment-text]" [state-management-file-path]
model: claude-haiku-4-5
allowed-tools: Read, Bash(echo:*)
---

# Create Issue Comment Command

## Purpose

Add a comment to an issue in the configured issue tracking system.
This command is called by other orchestrating commands, and is one of the steps in a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Arguments

- `$1`: Issue key (required)
- `$2`: Comment text (required)
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
     - Log the comment operation locally: "Silent mode: Would have added comment to $1: $2"
     - Skip the actual API call (step 4)
     - Continue to step 5

4. **Execute Create Comment Operation** (only if silentMode is false and issueTrackingProvider is not "prompt"):

### For Linear Provider (`"linear"`)

- Use `linear:create_comment` with $1 (issue ID) and $2 (comment text)
- Add the comment to the specified issue

### For Jira Provider (`"jira"`)

- Use `jira:add_comment_to_issue` with $1 (issue key) and $2 (comment text)
- Add the comment to the specified issue

5. **Output Results**: Display confirmation of the comment creation:
   - **Issue**: $1
   - **Comment Added**: $2
   - **Result**: Success/Failure (or "Skipped - Silent Mode" if applicable)

6. **Error Handling**: If the issue operation fails, log the error but continue gracefully
