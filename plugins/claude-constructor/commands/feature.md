---
name: feature
description: Implement feature from issue tracking system or user prompt
argument-hint: [issue-key-or-prompt] [--provider=<linear|jira|prompt>] [--silent=<true|false>]
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

- List the contents of the `claude_constructor` directory (if it exists)
- Check for existing directories named using the pattern `prompt-{number}` (e.g., `prompt-1`, `prompt-2`)
- Determine the next issue key:
  - If no `prompt-{number}` directories exist: use `prompt-1-{short-description}`
  - If at least one exists: find the maximum number and use `prompt-{maxNumber+1}-{short-description}`
- The short description should be a kebab-case summary of the prompt (e.g., `prompt-1-implement-cli`, `prompt-2-add-auth`)

Parse optional settings arguments ($2, $3, etc.) to extract provider and silent overrides for passing to `/read-settings`.

## Resume Detection

Before starting the workflow, check if a previous workflow exists for this issue and offer to resume.

### Detection Algorithm

Check if `claude_constructor/{issue-key}/state_management.md` exists. If it does, parse the file and determine the resume point using this algorithm (check in reverse order, first match wins):

| Check | Condition | Resume at |
|-------|-----------|-----------|
| 1 | `implementation_summary.md` exists | Complete - offer to start fresh |
| 2 | `pullRequestUrl` is set (not empty) | Step 16 (review PR) |
| 3 | `review.md` latest review has APPROVED | Step 15 (create PR) |
| 4 | `review.md` latest review has NEEDS_CHANGES | Step 11 (re-implement, code review loop) |
| 5 | `review.md` exists (any content) | Step 14 (code review - was interrupted) |
| 6 | `security_review.md` latest has APPROVED | Step 13 (write E2E tests) |
| 7 | `security_review.md` latest has NEEDS_CHANGES | Step 11 (re-implement, security loop) |
| 8 | `security_review.md` exists (any content) | Step 12 (security review - was interrupted) |
| 9 | Agent statuses all "completed" | Step 12 (security review) |
| 10 | Agent statuses exist with incomplete | Step 11 (continue implementation) |
| 11 | `workingBranch` is set, no agent statuses | Step 11 (start implementation) |
| 12 | `specificationApproved: true` | Step 10 (git checkout) |
| 13 | Implementation Plan section exists in specification | Step 9 (spec sign-off) |
| 14 | `requirementsApproved: true` | Step 7 (write spec) |
| 15 | Requirements Definition section exists in specification | Step 6 (req sign-off) |
| 16 | Settings section exists | Step 4 (define requirements) |
| 17 | State file exists only | Step 2 (read settings) |

### Implementation Progress Display

For implementation resume (check 10), show detailed agent progress:

```text
Implementation progress:
- agent-1: completed
- agent-2: in_progress (revision: 1) ← will continue
- agent-3: pending ← blocked by agent-2
```

### Resume UX Flow

1. Display progress summary:

   ```text
   Progress for {issue-key}:
   - [x] Requirements defined + approved
   - [x] Specification written + approved
   - [ ] Implementation ← Resume point
   ```

2. Use AskUserQuestion tool:
   - question: "Existing workflow found for {issue-key}. Resume from '{step-name}'?"
   - header: "Resume"
   - options:
     - label: "Resume (Recommended)"
       description: "Continue from {step-name}, preserving existing progress"
     - label: "Start Fresh"
       description: "Archive existing state and begin new workflow"

3. If user chooses "Start Fresh":
   - Rename `claude_constructor/{issue-key}/` → `claude_constructor/{issue-key}-archived-{timestamp}/`
     - Timestamp format: `YYYYMMDD-HHMMSS` (e.g., `ABC-123-archived-20240120-143052`)
   - Create fresh state file and start from step 1

4. If user chooses "Resume":
   - Skip to the detected resume step
   - For step 11 resume, `/implement-increment` will handle skipping completed agents

## Workflow Steps

1. Create a state management file for this increment - use the Skill tool to execute `/create-state-management-file $1` if the workflow was started from an issue, or the issue key if it was started from a prompt
2. Read settings - use the Skill tool to execute `/read-settings [state-management-file-path]` with any optional settings arguments from $2+ (e.g., `/read-settings [path] --provider=prompt --silent=true`)
3. Read issue - check the issueTrackingProvider in the Settings section of the state management file. If not "prompt", use the Skill tool to execute `/read-issue [issue-key] [state-management-file-path]`. If "prompt", skip this step as there is no external issue to read.
4. Define requirements - Use the requirements-definer subagent to define requirements for [state-management-file-path]
5. Audit requirements - Use the requirements-definer-auditor subagent to audit requirements in [state-management-file-path]. If audit fails with critical issues, return to step 4 to address them.
6. Get sign-off on requirements. You are not allowed to go to step 7 until the user has signed off on the requirements. Use the Skill tool to execute `/requirements-sign-off [state-management-file-path]`
7. Write specification - Use the specification-writer subagent to write specification for [state-management-file-path]
8. Audit specification - Use the specification-writer-auditor subagent to audit specification in [state-management-file-path]. If audit fails with critical issues, return to step 7 to address them.
9. Get sign-off on specification. You are not allowed to go to step 10 until the user has signed off on the specification. Use the Skill tool to execute `/specification-sign-off [state-management-file-path]`
10. Check out new branch - use the Skill tool to execute `/git-checkout [issue-key] [state-management-file-path]`
11. Implement increment - use the Skill tool to execute `/implement-increment [issue-key] [state-management-file-path]`
12. Perform security review:
    - Use the security-reviewer subagent to analyze the implementation at [state-management-file-path]
    - Parse the verdict from the subagent's output (look for "**Decision**: APPROVED" or "**Decision**: NEEDS_CHANGES")
    - If APPROVED: proceed to next step
    - If NEEDS_CHANGES:
      a. Inform user that security vulnerabilities were found
      b. Return to step 11 (implement increment) where agents will read claude_constructor/{issue-key}/security_review.md to understand what needs to be fixed
      c. Continue through steps 11-12 until APPROVED
13. Write end-to-end tests for the increment - use the Skill tool to execute `/write-end-to-end-tests [state-management-file-path]`
14. Perform code review:
    - Use the code-reviewer subagent to review the implementation for [state-management-file-path]
    - Parse the verdict from the agent's output (look for "**Decision**: APPROVED" or "**Decision**: NEEDS_CHANGES")
    - If APPROVED:
      a. Extract issue key from state management file
      b. Extract code review summary from agent output:
         - Look for the section starting with "## Code Review Summary"
         - Extract everything from that heading through the end of the output
         - This section must include Decision, Summary, Completed, and other details
         - Format contract: The agent outputs this in a specific format (see code-reviewer.md section 9)
      c. Use Skill tool to execute `/issue:create-comment [issue-key] "[code review summary]" [state-management-file-path]`
      d. Proceed to next step
    - If NEEDS_CHANGES:
      a. Inform the user that code review returned NEEDS_CHANGES and implementation will be revised
      b. Return to step 11 (implement increment) where implementation agents will read claude_constructor/{issue-key}/review.md and address the issues
      c. Continue through steps 11-14 again until APPROVED
15. Create pull request - use the Skill tool to execute `/create-pull-request [issue-key] [state-management-file-path]`
16. Review pull request - use the Skill tool to execute `/review-pull-request [issue-key] [state-management-file-path]`
17. Generate implementation summary - use the Skill tool to execute `/implementation-summary [issue-key] [state-management-file-path]`

**If issue tracking system operations fail**:

- Continue with local specification files
- Log issue tracking system errors but don't block development
- Manually update issue status if needed
