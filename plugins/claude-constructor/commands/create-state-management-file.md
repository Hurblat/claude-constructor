---
name: create-state-management-file
description: Create state management file for feature workflow
argument-hint: [issue-key]
model: claude-3-5-haiku-latest
---

# Create State Management File Command

## Purpose

Create a state management file and add the issue key.
These instructions are read and followed as part of a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. Create a state management file called `state_management/$1.md`.

2. Write the following at the top of the empty state management file:
`Issue Key: {$1}`
