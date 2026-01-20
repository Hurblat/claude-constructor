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
   - Read the specification file to get the Implementation Plan section

2. **Parse Technical Questions**:
   - Find `### Technical Questions` section in Implementation Plan (if exists)
   - Extract questions with their type tags: `[STRUCTURED]` or `[OPEN-ENDED]`
   - For STRUCTURED questions, extract options

3. **Resolve Structured Questions Interactively**:
   - If STRUCTURED questions exist:
     a. Group into batches of up to 4 questions (AskUserQuestion tool limit)
     b. Use AskUserQuestion tool for each batch:
        - question: The question text
        - options: Array with label and description for each option
     c. Update specification file:
        - Move answered questions to `### Resolved Technical Questions` section (create if needed)
        - Format: Question title + "**Answer:** [selected option with description]"
        - Remove the `[STRUCTURED]` tag from resolved questions

4. **Handle Open-Ended Questions**:
   - If only OPEN-ENDED questions remain:
     - Rename section to `### Technical Questions (Requires Discussion)`
   - These will be presented in review for user to address in feedback

5. **Present Implementation Plan for Review**:
   - Present the Implementation Plan section to the user for review
   - Tell the user where to find the full specification: "You can review the full specification at: `{specification-file-path}`"

6. **Get User Feedback**:
   - Ask the user to read and provide feedback on the Implementation Plan
   - If user has feedback:
     a. Use the specification-writer subagent to revise specification:

        ```text
        State management file: $1
        User feedback to address: [user's feedback verbatim]
        ```

     b. The subagent will detect the feedback and revise accordingly
     c. Return to step 1 for re-review
   - If user provides explicit sign-off, proceed to step 7

7. **Update Workflow Progress**:
   - Read the state management file ($1)
   - Update `specificationApproved: false` to `specificationApproved: true` in the Workflow Progress section

8. **Add Issue Comment**:
   - Did you get explicit approval on the specification? If not, go back to step 2.
   - Read the state management file to get the issue key
   - Use the SlashCommand tool to execute `/create-comment [issue-key] "[specification details and assumptions]"`
