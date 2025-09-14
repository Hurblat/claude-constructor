# Read Settings Command

## Purpose

Read Claude Constructor settings and add them to the state management file.
$ARGUMENTS contains the path to the state management file.
These instructions are read and followed as part of a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. Read settings by running `python3 ./scripts/load_settings.py`.

2. Add the settings to the state management file (path in $ARGUMENTS), in a new section called `## Settings`, on this format
    - key: value

3. Report DONE and continue with the next workflow step