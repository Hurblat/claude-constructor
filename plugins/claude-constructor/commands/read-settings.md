---
name: read-settings
description: Read settings and add to state management file
argument-hint: [state-management-file-path] [--provider=<linear|jira|prompt>] [--silent=<true|false>]
model: claude-haiku-4-5
allowed-tools: Read, Edit, Bash(git symbolic-ref:*), Bash(git rev-parse:*)
---

# Read Settings Command

## Purpose

Read Claude Constructor settings and add them to the state management file.
Settings are determined by command arguments or auto-detection.
These instructions are read and followed as part of a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Arguments

- `$1`: Path to state management file (required)
- `$2+`: Optional settings in format `--provider=<value>` or `--silent=<value>`

## Workflow Steps

1. Parse optional arguments ($2, $3, etc.) to extract settings overrides:
   - Look for `--provider=<value>` (valid: "linear", "jira", "prompt")
   - Look for `--silent=<value>` (valid: "true", "false")

2. Determine settings in this priority order:

   **Issue Tracking Provider:**
   - If `--provider=<value>` argument provided:
     - Validate it's one of: "linear", "jira", "prompt"
     - If "linear": Check that Linear MCP tools are available (try calling `linear:list_teams` or similar)
       - If NOT available: **FAIL with error**: "Provider set to 'linear' but Linear MCP tools are not configured. Please configure Linear MCP or use --provider=prompt"
     - If "jira": Check that Jira MCP tools are available (try calling `jira:get_projects` or similar)
       - If NOT available: **FAIL with error**: "Provider set to 'jira' but Jira MCP tools are not configured. Please configure Jira MCP or use --provider=prompt"
     - If "prompt": No validation needed
     - Use the validated provider value
   - Otherwise, auto-detect:
     - If Linear MCP tools are available → "linear"
     - If Jira MCP tools are available → "jira"
     - Otherwise → "prompt"

   **Default Branch:**
   - Auto-detect by running: `git symbolic-ref refs/remotes/origin/HEAD --short`
   - Parse the output to extract the branch name after "origin/" (e.g., "origin/main" → "main")
   - If that fails, try: `git rev-parse --abbrev-ref origin/HEAD` and parse similarly
   - If both fail, default to "main"

   **Silent Mode:**
   - If `--silent=<value>` argument provided, use it
   - Otherwise, default to "false"

3. Read the state management file ($1) to check if Settings section already exists

4. If Settings section exists:
   - Update the existing Settings section with the determined values
   - Use Edit tool to replace the Settings section

5. If Settings section does not exist:
   - Add a new Settings section to the state management file using Edit tool
   - Format:

     ```markdown
     ## Settings
     - issueTrackingProvider: [value]
     - defaultBranch: [value]
     - silentMode: [value]
     ```
