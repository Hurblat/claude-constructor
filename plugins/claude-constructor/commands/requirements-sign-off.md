---
name: requirements-sign-off
description: Get user approval on requirements
argument-hint: [state-management-file-path]
model: claude-haiku-4-5
---

# Requirements Sign-Off Command

## Purpose

Get sign-off on the requirements for the increment to be implemented.
These instructions are read and followed as part of a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. **Read State Management File**:
   - Read the state management file (path in $1)
   - Locate the specification file path
   - Present the Requirements Definition section to the user for review

2. **Get User Feedback**:
   - Ask the user to read and provide feedback on the Requirements Definition
   - If user has feedback:
     a. Use the requirements-definer subagent to revise requirements:

        ```text
        State management file: $1
        User feedback to address: [user's feedback verbatim]
        ```

     b. The subagent will detect the feedback and revise accordingly
     c. Return to step 1 for re-review
   - If user provides explicit sign-off, requirements sign-off is complete
