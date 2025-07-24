# Specification Sign-Off Command

## Purpose

Get sign-off on the specification for the increment to be implemented for the issue described in $ARGUMENTS.
This command is called by an orchestrating command, and is one of the steps in a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. **Present Assumptions**: Before showing the specification, clearly state your key assumptions about:
   - **Scope boundaries**: What is included/excluded in this increment
   - **Business rules**: Domain-specific rules or constraints to enforce
   - **User interactions**: Expected UX flow and user types involved
   - **Data requirements**: What data needs to be stored, validated, or transformed
   - **Integration points**: How this integrates with existing systems/components
   - **Error handling**: How errors and edge cases should be handled
   - **Performance expectations**: Any specific performance or scalability requirements

2. Ask the user to confirm these assumptions or provide corrections

3. Ask the user to read and provide feedback on the specification file linked in $ARGUMENTS

4. Iterate on the specification until the user gives their sign-off

5. Add specification comment - run the .claude/commands/ticket-create-comment.md command, passing the issue key and specification details as arguments to it

Get the issue key from the state management file in $ARGUMENTS.

Format the arguments as:
```
Ticket Number: [issue key from state management file]
Comment Text: [specification details and assumptions]
```

6. Report DONE to the orchestrating command
