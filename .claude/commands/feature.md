---
argument-hint: [issue key or prompt]
description: Implement feature from issue tracking system or user prompt
allowed-tools: Bash($(command -v python3 || command -v python) ./scripts/load_settings.py)
---

# Feature Implementation Command

## Purpose

This command guides the implementation of new functionality using **minimal iteration cycles**. Each workflow run should implement the smallest possible increment that provides measurable value while maintaining the system's quality standards.

You are responsible for making sure all steps are done according to the workflow steps description below.
All steps MUST complete, and they must be completed in the order described below.
You are only allowed to move to the next step after the previous step has reported DONE.

The issue key or prompt for the feature to implement is in $ARGUMENTS.

IMPORTANT: The workflow steps will report to you when they're done, and only then can the next step start. Do not stop until the workflow is completed.
Create a TODO list for the workflow steps, and follow it.

## Pre-Processing

Before starting the workflow for user prompts, create an issue key based on $ARGUMENTS:
- List the contents of `state_management` in the additional directories
- If there are no filenames using the format `prompt-{number}`, use issue key `prompt-1`
- If there is at least one filename using the format `prompt-{number}`, use issue key `prompt-{number+1}`

## Workflow Steps

1. Read @CLAUDE.md: General principles, quality gates, and development workflow. If the @CLAUDE.md refers to other @CLAUDE.md files, read those as well.
2. Create a state management file for this increment - read .claude/commands/create-state-management-file.md and follow the instructions, passing $ARGUMENTS as argument to it if the workflow was started from an issue, or the issue key if it was started from a prompt
3. Read settings - read .claude/commands/read-settings.md and follow the instructions
4. Read issue - check the issue-tracking-provider in the Settings section of the state management file. If not "prompt", read .claude/commands/issue/read-issue.md and follow the instructions. If "prompt", skip this step as there is no external issue to read.
5. Define requirements - use the Task tool to launch the requirements-definer agent with the state management file path as the prompt
6. Validate requirements - use the Task tool to launch the requirements-validator agent with the state management file path as the prompt. If validation fails with critical issues, return to step 5 to address them.
7. Get sign-off on requirements. You are not allowed to go to step 8 until the user has signed off on the requirements. Read .claude/commands/requirements-sign-off.md and follow the instructions
8. Write specification - use the Task tool to launch the specification-writer agent with the state management file path as the prompt
9. Validate specification - use the Task tool to launch the specification-validator agent with the state management file path as the prompt. If validation fails with critical issues, return to step 8 to address them.
10. Get sign-off on specification. You are not allowed to go to step 11 until the user has signed off on the specification. Read .claude/commands/specification-sign-off.md and follow the instructions
11. Check out new branch - read .claude/commands/git-checkout.md and follow the instructions
12. Implement increment - read .claude/commands/implement-increment.md and follow the instructions
13. Write end-to-end tests for the increment - read .claude/commands/write-end-to-end-tests.md and follow the instructions
14. Perform code review - read .claude/commands/code-review.md and follow the instructions. If the verdict of the code review is NEEDS_CHANGES, address comments and then repeat the implement increment step. Repeat as needed.
15. Create pull request - read .claude/commands/create-pull-request.md and follow the instructions
16. Review pull request - read .claude/commands/review-pull-request.md and follow the instructions

**If issue tracking system operations fail**:
- Continue with local specification files
- Log issue tracking system errors but don't block development
- Manually update issue status if needed
