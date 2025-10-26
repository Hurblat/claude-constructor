---
name: feature
description: Implement feature from issue tracking system or user prompt
argument-hint: [issue-key-or-prompt] [--provider=<linear|jira|prompt>] [--silent=<true|false>]
model: claude-sonnet-4-5
---

# Feature Implementation Command

## Purpose

This command guides the implementation of new functionality using **minimal iteration cycles**. Each workflow run should implement the smallest possible increment that provides measurable value while maintaining the system's quality standards.

You are responsible for making sure all steps are done according to the workflow steps description below.

IMPORTANT: All steps MUST complete, and they must be completed in the order described below.
You are only allowed to move to the next step after the previous step has completed.

The issue key or prompt for the feature to implement is $1.

Create a TODO list for the workflow steps, and follow it.

## Arguments

- `$1`: Issue key or feature prompt (required)
- `$2+`: Optional settings in format `--provider=<value>` or `--silent=<value>`
  - `--provider`: Override issue tracking provider (`linear`, `jira`, or `prompt`)
  - `--silent`: Override silent mode (`true` or `false`)

## Pre-Processing

Before starting the workflow for user prompts, create an issue key based on $1:

- List the contents of `state_management` in the additional directories
- If there are no filenames using the format `prompt-{number}`, use issue key `prompt-1-{short-description}`
- If there is at least one filename using the format `prompt-{number}`, use issue key `prompt-{number+1}-{short-description}`
- The short description should be a kebab-case summary of the prompt (e.g., `prompt-1-implement-cli`, `prompt-2-add-auth`)

Parse optional settings arguments ($2, $3, etc.) to extract provider and silent overrides for passing to `/read-settings`.

## Workflow Steps

1. Read @CLAUDE.md: General principles, quality gates, and development workflow. If the @CLAUDE.md refers to other @CLAUDE.md files, read those as well.
2. Create a state management file for this increment - use the SlashCommand tool to execute `/create-state-management-file $1` if the workflow was started from an issue, or the issue key if it was started from a prompt
3. Read settings - use the SlashCommand tool to execute `/read-settings [state-management-file-path]` with any optional settings arguments from $2+ (e.g., `/read-settings [path] --provider=prompt --silent=true`)
4. Read issue - check the issueTrackingProvider in the Settings section of the state management file. If not "prompt", use the SlashCommand tool to execute `/read-issue [issue-key] [state-management-file-path]`. If "prompt", skip this step as there is no external issue to read.
5. Define requirements - Use the requirements-definer subagent to define requirements for [state-management-file-path]
6. Audit requirements - Use the requirements-definer-auditor subagent to audit requirements in [state-management-file-path]. If audit fails with critical issues, return to step 5 to address them.
7. Get sign-off on requirements. You are not allowed to go to step 8 until the user has signed off on the requirements. Use the SlashCommand tool to execute `/requirements-sign-off [state-management-file-path]`
8. Write specification - Use the specification-writer subagent to write specification for [state-management-file-path]
9. Audit specification - Use the specification-writer-auditor subagent to audit specification in [state-management-file-path]. If audit fails with critical issues, return to step 8 to address them.
10. Get sign-off on specification. You are not allowed to go to step 11 until the user has signed off on the specification. Use the SlashCommand tool to execute `/specification-sign-off [state-management-file-path]`
11. Check out new branch - use the SlashCommand tool to execute `/git-checkout [issue-key] [state-management-file-path]`
12. Implement increment - use the SlashCommand tool to execute `/implement-increment [issue-key] [state-management-file-path]`
13. Perform security review:
    - Use the security-reviewer subagent to analyze the implementation at [state-management-file-path]
    - Parse the verdict from the subagent's output (look for "**Decision**: APPROVED" or "**Decision**: NEEDS_CHANGES")
    - If APPROVED: proceed to next step
    - If NEEDS_CHANGES:
      a. Inform user that security vulnerabilities were found
      b. Return to step 12 (implement increment) where agents will read security_reviews/{issue-key}.md to understand what needs to be fixed
      c. Continue through steps 12-13 until APPROVED
14. Write end-to-end tests for the increment - use the SlashCommand tool to execute `/write-end-to-end-tests [state-management-file-path]`
15. Perform code review:
    - Use the code-reviewer subagent to review the implementation for [state-management-file-path]
    - Parse the verdict from the agent's output (look for "**Decision**: APPROVED" or "**Decision**: NEEDS_CHANGES")
    - If APPROVED:
      a. Extract issue key from state management file
      b. Extract code review summary from agent output:
         - Look for the section starting with "## Code Review Summary"
         - Extract everything from that heading through the end of the output
         - This section must include Decision, Summary, Completed, and other details
         - Format contract: The agent outputs this in a specific format (see code-reviewer.md section 9)
      c. Use SlashCommand tool to execute `/issue:create-comment [issue-key] "[code review summary]" [state-management-file-path]`
      d. Proceed to next step
    - If NEEDS_CHANGES:
      a. Inform the user that code review returned NEEDS_CHANGES and implementation will be revised
      b. Return to step 12 (implement increment) where implementation agents will read code_reviews/{issue-key}.md and address the issues
      c. Continue through steps 12-15 again until APPROVED
16. Create pull request - use the SlashCommand tool to execute `/create-pull-request [issue-key] [state-management-file-path]`
17. Review pull request - use the SlashCommand tool to execute `/review-pull-request [issue-key] [state-management-file-path]`

**If issue tracking system operations fail**:

- Continue with local specification files
- Log issue tracking system errors but don't block development
- Manually update issue status if needed
