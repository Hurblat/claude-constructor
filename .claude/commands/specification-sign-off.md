# Specification Sign-Off Command

## Purpose

Get sign-off on the specification for the increment to be implemented for the issue described in $ARGUMENTS.
This command is called by an orchestrating command, and is one of the steps in a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. **Read State Management File**:
   - Read the state management file provided in $ARGUMENTS
   - Locate the specification file path
   - Present the Implementation Plan section to the user for review

2. **Get User Feedback**:
   - Ask the user to read and provide feedback on the Implementation Plan
   - If user has feedback:
     a. Re-invoke the specification-writer agent with prompt:
        ```
        State management file: [path from $ARGUMENTS]
        User feedback to address: [user's feedback verbatim]
        ```
     b. The agent will detect the feedback and revise accordingly
     c. Return to step 1 for re-review
   - If user provides explicit sign-off, proceed to step 3

3. **Add Issue Comment**:
   - Did you get explicit approval on the specification? If not, go back to step 2.
   - Add specification comment - run the .claude/commands/issue/create-comment.md command, passing the issue key and specification details as arguments to it

    Get the issue key from the state management file in $ARGUMENTS.

    Format the arguments as:
    ```
    Issue Key: [issue key from state management file]
    Comment Text: [specification details and assumptions]
    ```

4. **Report Completion**:
   - Report DONE to the orchestrating command
