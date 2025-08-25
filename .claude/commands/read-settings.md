---
allowed-tools: Bash(python scripts/load_settings.py)
description: Read configuration settings for the workflow
---

# Read Settings Command

## Purpose

Read Claude Constructor settings and put them in $ARGUMENTS.
This command is called by an orchestrating command, and is one of the steps in a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. Read settings by running !`python scripts/load_settings.py`

2. Add the settings in $ARGUMENTS, in a new section called `## Settings`, on this format
    - key: value

3. Report DONE to the orchestrating command