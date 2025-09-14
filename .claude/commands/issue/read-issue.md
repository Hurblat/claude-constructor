# Read Issue Command

## Purpose

Read issue from the configured issue tracking system and add the information to the state management file.
$ARGUMENTS contains the path to the state management file.
These instructions are read and followed as part of a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. Read the state management file (path in $ARGUMENTS) and extract the issue key

2. Get issue details - read .claude/commands/issue/get-issue.md and follow the instructions

The issue key is listed in the state management file after `Issue Key:`

Format the argument as:
```
Issue Key: [issue key from state management file]
```

3. Note findings in the state management file

Create a new section called `## Issue Information`, with information on this format:
- **Key**: Issue key
- **ID**: Issue ID
- **Title**: Issue title
- **Description**: Issue description

4. Report DONE and continue with the next workflow step
