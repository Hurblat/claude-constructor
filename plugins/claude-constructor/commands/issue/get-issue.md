---
name: get-issue
description: Retrieve issue details from tracking system
argument-hint: [issue-key] [state-management-file-path]
model: claude-haiku-4-5
allowed-tools: Read, Bash(echo:*)
---

# Get Issue Command

## Purpose

Retrieve issue details from the configured issue tracking system for a given issue key.
This command is called by other orchestrating commands, and is one of the steps in a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Arguments

- `$1`: Issue key (required)
- `$2`: Path to state management file (required)

## Workflow Steps

1. **Read Settings from State Management File**:
   - Read the Settings section from the state management file ($2)
   - Extract `issueTrackingProvider` value
   - If Settings section is missing or issueTrackingProvider is not set, fail with error: "Settings not found in state management file. Run /read-settings first."

2. **Validate Provider Configuration**:
   - If issueTrackingProvider is "linear":
     - Check that Linear MCP tools are available
     - If NOT available: **FAIL with error**: "Provider is 'linear' but Linear MCP tools are not configured. Please configure Linear MCP or update settings with /read-settings --provider=prompt"
   - If issueTrackingProvider is "jira":
     - Check that Jira MCP tools are available
     - If NOT available: **FAIL with error**: "Provider is 'jira' but Jira MCP tools are not configured. Please configure Jira MCP or update settings with /read-settings --provider=prompt"
   - If issueTrackingProvider is "prompt":
     - Log error: "get-issue should not be called for prompt provider"
     - Skip to step 4

3. **Execute Get Issue Operation**:

   Based on the `issueTrackingProvider` value from the state management file:

   ### For Linear Provider (`"linear"`)

   - Use `linear:get_issue` with $1 (issue key)
   - Retrieve issue key, ID, title, and description

   ### For Jira Provider (`"jira"`)

   - Use `jira:get_issue` with $1 (issue key)
   - Retrieve issue key, ID, title, and description

4. **Output Results**: Display the issue information in this format:
   - **Key**: $1
   - **ID**: Issue ID
   - **Title**: Issue title
   - **Description**: Issue description

5. **Error Handling**: If the issue operation fails, log the error but continue gracefully
