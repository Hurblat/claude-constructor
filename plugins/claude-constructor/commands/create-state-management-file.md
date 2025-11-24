---
name: create-state-management-file
description: Create state management file for feature workflow
argument-hint: [issue-key]
model: claude-haiku-4-5
---

# Create State Management File Command

## Purpose

Create a state management file and add the issue key.
These instructions are read and followed as part of a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. Create the workflow directory for this issue using `mkdir -p claude_constructor/$1`

2. Create a state management file called `claude_constructor/$1/state_management.md`.

3. Write the following content to the newly created state management file:
`Issue Key: {$1}`
