---
name: get-issue
description: Retrieve issue details from tracking system
argument-hint: [issue-key]
model: claude-3-5-haiku-latest
allowed-tools: Bash(echo:*)
---

# Get Issue Command

## Purpose

Retrieve issue details from the configured issue tracking system for a given issue key.
This command is called by other orchestrating commands, and is one of the steps in a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. **Determine Issue Tracking Provider**:
   - Check `CLAUDE_CONSTRUCTOR_PROVIDER` environment variable
   - Validate it's one of: "linear", "jira", "prompt"
   - If not set or invalid, auto-detect:
     - If Linear MCP tools are available → use "linear"
     - If Jira MCP tools are available → use "jira"
     - Otherwise → use "prompt"

2. **Execute Get Issue Operation**:

### For Linear Provider (`"linear"`)

- Use `linear:get_issue` with $1 (issue key)
- Retrieve issue key, ID, title, and description

### For Jira Provider (`"jira"`)

- Use `jira:get_issue` with $1 (issue key)
- Retrieve issue key, ID, title, and description

3. **Output Results**: Display the issue information in this format:
   - **Key**: $1
   - **ID**: Issue ID
   - **Title**: Issue title
   - **Description**: Issue description

4. **Error Handling**: If the issue operation fails, log the error but continue gracefully
