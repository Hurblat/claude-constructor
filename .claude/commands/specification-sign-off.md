---
name: specification-sign-off
description: Get user approval on implementation plan
argument-hint: [state-management-file-path]
model: claude-3-5-haiku-latest
---

# Specification Sign-Off Command

## Purpose

Get sign-off on the specification for the increment to be implemented.
$ARGUMENTS contains the path to the state management file.
These instructions are read and followed as part of a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. **Read State Management File**:
   - Read the state management file (path in $ARGUMENTS)
   - Locate the specification file path
   - Present the Implementation Plan section to the user for review

2. **Get User Feedback**:
   - Ask the user to read and provide feedback on the Implementation Plan
   - If user has feedback:
     a. Re-invoke the specification-writer agent with prompt:
        ```
        State management file: $ARGUMENTS
        User feedback to address: [user's feedback verbatim]
        ```
     b. The agent will detect the feedback and revise accordingly
     c. Return to step 1 for re-review
   - If user provides explicit sign-off, proceed to step 3

3. **Add Issue Comment**:
   - Did you get explicit approval on the specification? If not, go back to step 2.
   - Read the state management file to get the issue key
   - Use the SlashCommand tool to execute `/create-comment [issue-key] "[specification details and assumptions]"`

4. **Report Completion**:
   - Report DONE and continue with the next workflow step
