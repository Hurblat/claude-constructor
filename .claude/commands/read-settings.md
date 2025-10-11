---
name: read-settings
description: Read settings and add to state management file
argument-hint: [state-management-file-path]
model: claude-3-5-haiku-latest
allowed-tools: Read, Bash(git symbolic-ref:*), Bash(git rev-parse:*)
---

# Read Settings Command

## Purpose

Read Claude Constructor settings and add them to the state management file.
Settings are determined by environment variables (from .claude/settings.json env section) and auto-detection.
These instructions are read and followed as part of a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. Determine settings in this priority order:

   **Issue Tracking Provider:**
   - Check environment variable `CLAUDE_CONSTRUCTOR_PROVIDER`
   - If not set, auto-detect:
     - If Linear MCP tools are available → "linear"
     - If Jira MCP tools are available → "jira"
     - Otherwise → "prompt"

   **Default Branch:**
   - Auto-detect using: `git symbolic-ref refs/remotes/origin/HEAD --short | sed 's@^origin/@@'`
   - If that fails, try: `git rev-parse --abbrev-ref origin/HEAD | sed 's@^origin/@@'`
   - If both fail, default to "main"

   **Silent Mode:**
   - Check environment variable `CLAUDE_CONSTRUCTOR_SILENT_MODE`
   - If not set or "false" → false
   - If "true" or "1" → true

2. Add the settings to the state management file ($1), in a new section called `## Settings`, on this format:
   - issueTrackingProvider: [value]
   - defaultBranch: [value]
   - silentMode: [value]