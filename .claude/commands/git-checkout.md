---
allowed-tools: Bash(git checkout:*), Bash(git pull:*)
description: Check out a new git branch for implementation
---

# Git Checkout Command

## Purpose

Check out a new git branch to be ready for implementation start, for the issue described in $ARGUMENTS.
This command is called by an orchestrating command, and is one of the steps in a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. Read the Settings section in $ARGUMENTS to get the default branch name

2. Run !`git checkout [default branch name]`

3. Ensure that you have the latest changes, using !`git pull`

4. Check out a new branch, using !`git checkout -b feat/{issue key}`

5. Report DONE to the orchestrating command
