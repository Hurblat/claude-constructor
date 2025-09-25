---
name: read-settings
description: Read settings and add to state management file
argument-hint: [state-management-file-path]
model: claude-3-5-haiku-latest
allowed-tools: Bash($(command -v python3 || command -v python) ./scripts/load_settings.py)
---

# Read Settings Command

## Purpose

Read Claude Constructor settings and add them to the state management file.
These instructions are read and followed as part of a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. Read settings by running `$(command -v python3 || command -v python) ./scripts/load_settings.py`.

2. Add the settings to the state management file ($1), in a new section called `## Settings`, on this format
    - key: value