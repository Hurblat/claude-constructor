# Code Review Command

## Purpose

Review code changes for the active increment and give a verdict of NEEDS_CHANGES or APPROVED.
$ARGUMENTS contains the path to the state management file.
These instructions are read and followed as part of a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. Read state management file (path in $ARGUMENTS) to understand the context for what you need to review

2. Read the specification linked in the state management file

3. Analyze current codebase against the specification requirements

4. Verify completion criteria:
    - [ ] Single behavior is fully implemented
    - [ ] All quality gates pass (see below)
    - [ ] No breaking changes introduced
    - [ ] Feature works in both development and build modes
    - [ ] Business rules are enforced consistently
    - [ ] No stubs or TODOs, all functionality should be completed

5. Ultrathink about your findings and provide detailed feedback:
    - What's implemented correctly
    - What's missing or incomplete
    - Any issues found
    - Specific next steps if changes needed

6. Final verdict: APPROVED or NEEDS_CHANGES with clear reasons

7. Once APPROVED, add code review comment - read .claude/commands/issue/create-comment.md and follow the instructions

Format the arguments as:
```
Issue Key: [issue key from state management file]
Comment Text: [code review findings and verdict]
```

8. Report DONE and continue with the next workflow step.

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
