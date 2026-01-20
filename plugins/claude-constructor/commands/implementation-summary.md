---
name: implementation-summary
description: Generate final summary of implemented feature
argument-hint: [issue-key] [state-management-file-path]
model: claude-haiku-4-5
---

# Implementation Summary Command

## Purpose

Generate a comprehensive summary of the completed feature implementation.
This command is called at the end of the workflow to provide a clear record of what was built.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. **Read State Management File**:
   - Read the state management file ($2)
   - Extract: issue key, specification file path, settings, implementation agents status

2. **Read Specification File**:
   - Read the specification file referenced in state management
   - Extract: Requirements Definition summary, Implementation Plan summary

3. **Read Review Files** (if they exist):
   - Read `claude_constructor/$1/review.md` for code review history
   - Read `claude_constructor/$1/security_review.md` for security review history
   - Count review iterations and extract final verdicts

4. **Gather Git Information**:
   - Run `git log --oneline origin/HEAD..HEAD` to get commits made
   - Run `git diff --stat origin/HEAD..HEAD` to get files changed summary
   - Run `git branch --show-current` to get branch name

5. **Get PR Information** (if not silent mode):
   - Run `gh pr view --json url,number,title` to get PR details
   - If command fails (no PR), note that PR was not created

6. **Generate Summary**:
   Write a summary to `claude_constructor/$1/implementation_summary.md` with the following structure:

   ```markdown
   # Implementation Summary

   **Issue**: {issue_key}
   **Title**: {issue_title}
   **Completed**: {timestamp}

   ## What Was Requested

   {Brief summary from issue description and requirements}

   ## What Was Built

   {Summary of implementation from specification}

   ### Acceptance Criteria Status

   - [x] {criterion 1}
   - [x] {criterion 2}
   ...

   ## Implementation Details

   **Branch**: `{branch_name}`
   **Commits**: {number of commits}

   ### Files Changed

   {git diff --stat output}

   ### Implementation Agents

   | Agent | Status | Revisions |
   |-------|--------|-----------|
   | {agent-id} | {status} | {count} |

   ## Quality Assurance

   ### Security Review

   - **Iterations**: {count}
   - **Final Status**: {APPROVED/NEEDS_CHANGES}

   ### Code Review

   - **Iterations**: {count}
   - **Final Status**: {APPROVED}
   - **Quality Gates**: All passed

   ## Deliverables

   - **Pull Request**: {PR_URL or "Not created (silent mode)"}
   - **Branch**: `{branch_name}`

   ## Commits

   {git log --oneline output}
   ```

7. **Output Summary to User**:
   - Display the key sections of the summary to the user
   - Inform them where the full summary file is located
