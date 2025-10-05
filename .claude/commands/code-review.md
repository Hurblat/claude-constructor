---
name: code-review
description: Review implementation against specification
argument-hint: [issue-key] [state-management-file-path]
model: claude-sonnet-4-5
---

# Code Review Command

## Purpose

Review code changes for the active increment and give a verdict of NEEDS_CHANGES or APPROVED.
These instructions are read and followed as part of a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. Read state management file ($2) to understand the context for what you need to review

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

7. Write review findings to log file:
   - Check if `workflow_files/$1/review.md` exists using: `ls workflow_files/$1/review.md 2>/dev/null || echo "not found"`
   - Determine round number:
     - If review.md exists: Read it and count occurrences of "## Round" to determine next round number
     - If review.md doesn't exist: This is Round 1
   - Generate timestamp using: `date -u '+%Y-%m-%d %H:%M UTC'`
   - Create the review entry with your findings:
     ```
     ## Round {N}
     **Date**: {timestamp}
     **Verdict**: APPROVED or NEEDS_CHANGES

     ### Summary
     [Brief status]

     ### Completed
     [What works correctly]

     ### Issues Found
     [Specific problems]

     ### Missing
     [What still needs implementation]

     ### Next Steps
     [Actionable items if NEEDS_CHANGES, or "None - ready for PR" if APPROVED]
     ```
   - Write to file:
     - If review.md exists: Use Edit tool to append the new round at the end
     - If review.md doesn't exist: Use Write tool to create it with the round content

8. Once APPROVED, add code review comment:
   - Use the SlashCommand tool to execute `/create-comment $1 "[code review findings and verdict]"`

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
