---
name: specification-sign-off
description: Get user approval on implementation plan
argument-hint: [state-management-file-path]
model: claude-haiku-4-5
---

# Specification Sign-Off Command

## Purpose

Get sign-off on the specification for the increment to be implemented.
These instructions are read and followed as part of a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. **Read State Management File**:
   - Read the state management file (path in $1)
   - Locate the specification file path
   - Present the Implementation Plan section to the user for review

2. **Get User Feedback**:
   - Ask the user to read and provide feedback on the Implementation Plan
   - If user has feedback:
     a. Use the specification-writer subagent to revise specification:

        ```text
        State management file: $1
        User feedback to address: [user's feedback verbatim]
        ```

     b. The subagent will detect the feedback and revise accordingly
     c. Return to step 1 for re-review
   - If user provides explicit sign-off, proceed to step 3

3. **Add Issue Comment**:
   - Did you get explicit approval on the specification? If not, go back to step 2.
   - Read the state management file to get the issue key
   - Use the SlashCommand tool to execute `/create-comment [issue-key] "[specification details and assumptions]"`
