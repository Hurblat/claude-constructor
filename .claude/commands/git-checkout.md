# Git Checkout Command

## Purpose

Check out a new git branch to be ready for implementation start.
$ARGUMENTS contains the path to the state management file.
These instructions are read and followed as part of a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. Read the Settings section in the state management file (path in $ARGUMENTS) to get the default branch name and issue key

2. Run `git checkout [default branch name]`

3. Ensure that you have the latest changes, using `git pull`

4. Check out a new branch, using `git checkout -b feat/{issue key}`

5. Report DONE and continue with the next workflow step
