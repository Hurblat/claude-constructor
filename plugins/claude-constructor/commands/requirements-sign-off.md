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
   - Read the specification file to get the Requirements Definition section

2. **Parse Open Questions**:
   - Find `### Open Questions` section in Requirements Definition
   - Extract questions with their type tags: `[STRUCTURED]` or `[OPEN-ENDED]`
   - For STRUCTURED questions, extract options using these rules:

     **Canonical format** (from requirements-definer):

     ```markdown
     - **Option A**: Description text
     - **Option B**: Description text
     ```

     **Also accept these variants** (normalize to canonical):

     - `- **Option A**: text` (canonical)
     - `- Option A: text`
     - `- A. text`
     - `- A) text`
     - `- A: text`

     Extract: label (A/B/C/D) and description text.

     **Validation**:

     - STRUCTURED questions must have at least 2 options
     - If no options found: log warning "No options found for STRUCTURED question: [title]", treat as OPEN-ENDED
     - If only 1 option found: log warning "Only 1 option found for STRUCTURED question: [title]", treat as OPEN-ENDED

3. **Resolve Structured Questions Interactively**:
   - If STRUCTURED questions exist:
     a. Collect all STRUCTURED questions into a list (preserving original order)
     b. Process in sequential batches of up to 4 questions each:
        - While unprocessed STRUCTURED questions remain:
          1. Take the next batch (up to 4 questions)
          2. Call AskUserQuestion tool with the batch:
             - question: The question text
             - options: Array with label and description for each option
          3. Await and collect user responses for all questions in batch
          4. Continue to next batch
     c. After all batches complete, update specification file:
        - Move all answered questions to `### Resolved Questions` section (create if needed)
        - Format: Question title + "**Answer:** [selected option with description]"
        - Remove the `[STRUCTURED]` tag from resolved questions

4. **Handle Open-Ended Questions**:
   - If only OPEN-ENDED questions remain:
     - Rename section to `### Open Questions (Requires Discussion)`
   - These will be presented in review for user to address in feedback

5. **Present Requirements for Review**:
   - Present the Requirements Definition section to the user for review
   - Tell the user where to find the full specification: "You can review the full specification at: `{specification-file-path}`"

6. **Get User Feedback**:
   - Ask the user to read and provide feedback on the Requirements Definition
   - If user has feedback:
     a. Use the requirements-definer subagent to revise requirements:

        ```text
        State management file: $1
        User feedback to address: [user's feedback verbatim]
        ```

     b. The subagent will detect the feedback and revise accordingly
     c. Return to step 1 for re-review
   - If user provides explicit sign-off, proceed to step 7

7. **Update Workflow Progress**:
   - Read the state management file ($1)
   - Update `requirementsApproved: false` to `requirementsApproved: true` in the Workflow Progress section
   - Requirements sign-off is complete
