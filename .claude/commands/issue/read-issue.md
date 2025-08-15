# Read Issue Command

## Purpose

Read issue from the configured issue tracking system for the issue key listed in $ARGUMENTS and note all information in $ARGUMENTS.
This command is called by an orchestrating command, and is one of the steps in a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. Read $ARGUMENTS and extract the issue key

2. Get issue details - run the .claude/commands/issue/get-issue.md command, passing the issue key as argument to it

The issue key is listed in $ARGUMENTS after `Issue Key:`

Format the argument as:
```
Issue Key: [issue key from $ARGUMENTS]
```

3. Note findings in $ARGUMENTS

Create a new section called `## Issue Information`, with information on this format:
- **Key**: Issue key
- **ID**: Issue ID
- **Title**: Issue title
- **Description**: Issue description

4. Report DONE to the orchestrating command
