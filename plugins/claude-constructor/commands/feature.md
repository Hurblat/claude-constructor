---
name: feature
description: Implement feature from issue tracking system or user prompt
argument-hint: [issue-key-or-prompt]
model: claude-sonnet-4-5
---

# Feature Implementation Command

## Purpose

This command guides the implementation of new functionality using **minimal iteration cycles**. Each workflow run should implement the smallest possible increment that provides measurable value while maintaining the system's quality standards.

You are responsible for making sure all steps are done according to the workflow steps description below.
All steps MUST complete, and they must be completed in the order described below.
You are only allowed to move to the next step after the previous step has reported DONE.

The issue key or prompt for the feature to implement is $1.

IMPORTANT: The workflow steps will report to you when they're done, and only then can the next step start. Do not stop until the workflow is completed.
Create a TODO list for the workflow steps, and follow it.

## Pre-Processing

Before starting the workflow for user prompts, create an issue key based on $1:
- List the contents of `state_management` in the additional directories
- If there are no filenames using the format `prompt-{number}`, use issue key `prompt-1-{short-description}`
- If there is at least one filename using the format `prompt-{number}`, use issue key `prompt-{number+1}-{short-description}`
- The short description should be a kebab-case summary of the prompt (e.g., `prompt-1-implement-cli`, `prompt-2-add-auth`)

## Workflow Steps

1. Read @CLAUDE.md: General principles, quality gates, and development workflow. If the @CLAUDE.md refers to other @CLAUDE.md files, read those as well.
2. Create a state management file for this increment - use the SlashCommand tool to execute `/create-state-management-file $1` if the workflow was started from an issue, or the issue key if it was started from a prompt
3. Read settings - use the SlashCommand tool to execute `/read-settings [state-management-file-path]`
4. Read issue - check the issue-tracking-provider in the Settings section of the state management file. If not "prompt", use the SlashCommand tool to execute `/read-issue [issue-key] [state-management-file-path]`. If "prompt", skip this step as there is no external issue to read.
5. Define requirements - Use the requirements-definer subagent to define requirements for [state-management-file-path]
6. Validate requirements - Use the requirements-validator subagent to validate requirements in [state-management-file-path]. If validation fails with critical issues, return to step 5 to address them.
7. Get sign-off on requirements. You are not allowed to go to step 8 until the user has signed off on the requirements. Use the SlashCommand tool to execute `/requirements-sign-off [state-management-file-path]`
8. Write specification - Use the specification-writer subagent to write specification for [state-management-file-path]
9. Validate specification - Use the specification-validator subagent to validate specification in [state-management-file-path]. If validation fails with critical issues, return to step 8 to address them.
10. Get sign-off on specification. You are not allowed to go to step 11 until the user has signed off on the specification. Use the SlashCommand tool to execute `/specification-sign-off [state-management-file-path]`
11. Check out new branch - use the SlashCommand tool to execute `/git-checkout [issue-key] [state-management-file-path]`
12. Implement increment - use the SlashCommand tool to execute `/implement-increment [issue-key] [state-management-file-path]`
13. Perform security review - use the SlashCommand tool to execute `/security-review`. If security vulnerabilities are found, address them and repeat the implement increment step as needed.
14. Write end-to-end tests for the increment - use the SlashCommand tool to execute `/write-end-to-end-tests [state-management-file-path]`
15. Perform code review - use the SlashCommand tool to execute `/code-review [state-management-file-path]`. If the verdict of the code review is NEEDS_CHANGES, address comments and then repeat the implement increment step. Repeat as needed.
16. Create pull request - use the SlashCommand tool to execute `/create-pull-request [issue-key] [state-management-file-path]`
17. Review pull request - use the SlashCommand tool to execute `/review-pull-request [issue-key] [state-management-file-path]`

**If issue tracking system operations fail**:
- Continue with local specification files
- Log issue tracking system errors but don't block development
- Manually update issue status if needed
