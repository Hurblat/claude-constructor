# Code Review Command

## Purpose

Review code changes for the active increment and give a verdict of NEEDS_CHANGES or APPROVED.
This command is called by an orchestrating command, and is one of the steps in a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

When this command is run with a state management file as $ARGUMENTS.

1. Read state management file to understand the context for what you need to review

2. Update issue status to "Code Review" - run the .claude/commands/ticket-update-issue.md command, passing the issue key and new status as arguments to it

Get the issue key from the state management file in $ARGUMENTS.

Format the arguments as:
```
Ticket Number: [issue key from state management file]
New Status: Code Review
```

3. Read the specification linked in the state management file

4. Analyze current codebase against the specification requirements

5. Verify completion criteria:
   - [ ] Single behavior is fully implemented
   - [ ] All quality gates pass (see below)
   - [ ] No breaking changes introduced
   - [ ] Feature works in both development and build modes
   - [ ] Business rules are enforced consistently

6. Ultrathink about your findings and provide detailed feedback:
   - What's implemented correctly
   - What's missing or incomplete
   - Any issues found
   - Specific next steps if changes needed

7. Final verdict: APPROVED or NEEDS_CHANGES with clear reasons

8. Once APPROVED, add code review comment - run the .claude/commands/ticket-create-comment.md command, passing the issue key and findings as arguments to it

Format the arguments as:
```
Ticket Number: [issue key from state management file]
Comment Text: [code review findings and verdict]
```

9. Report DONE to the orchestrating command.

## Review Process

### Specification Alignment
- Compare implemented behavior vs. specified behavior
- Verify no scope creep beyond the minimal increment
- Check adherence to domain principles

### Code Quality
- Review test coverage and quality
- Check domain model consistency
- Verify error handling
- Assess code organization

### Integration
- Verify frontend/backend integration if applicable
- Check build pipeline success
- Validate development/production compatibility

### Quality Gates

Run all quality gates and verify that they pass.

## Output Format

Provide structured feedback:
- **Summary**: Brief status
- **Completed**: What works correctly
- **Issues Found**: Specific problems
- **Missing**: What still needs implementation
- **Next Steps**: Actionable items
- **Decision**: APPROVED or NEEDS_CHANGES

**Update issue status based on decision**:
- If APPROVED: run the .claude/commands/ticket-update-issue.md command with status "Ready For Human Review"
- If NEEDS_CHANGES: run the .claude/commands/ticket-update-issue.md command with status "In Progress" and run the .claude/commands/ticket-create-comment.md command with required changes

Format the arguments as:
```
Ticket Number: [issue key from state management file]
New Status: Ready For Human Review
```
or
```
Ticket Number: [issue key from state management file]
New Status: In Progress
```
and
```
Ticket Number: [issue key from state management file]
Comment Text: [required changes description]
```
