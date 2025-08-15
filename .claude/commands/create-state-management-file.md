# Create State Management File Command

## Purpose

Create a state management file called `state_management/{issue_key}.md`.
This command is called by an orchestrating command, and is one of the steps in a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. Write the following at the top of the empty state management file:
`Linear Issue Key: {issue_key}` (replace {issue_key} with $ARGUMENTS)
2. Report DONE to the orchestrating command
