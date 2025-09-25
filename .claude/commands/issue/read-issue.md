---
name: read-issue
description: Fetch issue details from tracking system
argument-hint: [issue-key] [state-management-file-path]
model: claude-3-5-haiku-latest
---

# Read Issue Command

## Purpose

Read issue from the configured issue tracking system and add the information to the state management file.
These instructions are read and followed as part of a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. Get issue details:
   - Use the SlashCommand tool to execute `/get-issue $1`

2. Note findings in the state management file ($2)

Create a new section called `## Issue Information`, with information on this format:
- **Key**: $1
- **ID**: Issue ID (from get-issue response)
- **Title**: Issue title (from get-issue response)
- **Description**: Issue description (from get-issue response)
