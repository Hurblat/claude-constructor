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

3. **Read Review Files**:
   - Check if `claude_constructor/$1/review.md` exists:
     - If exists: Read for code review history, count review iterations, extract final verdict
     - If missing: Set code review iterations to 0, final verdict to "N/A", include "No code review performed" in summary
   - Check if `claude_constructor/$1/security_review.md` exists:
     - If exists: Read for security review history, count iterations, extract final verdict
     - If missing: Set security review iterations to 0, final verdict to "N/A", include "No security review performed" in summary

4. **Get PR Information** (if not silent mode):
   - Run `gh pr view --json url,number,title,baseRefName` to get PR details including base branch
   - Extract `baseRefName` from the response (e.g., "main", "develop")
   - If command fails (no PR), note that PR was not created and set `baseRefName` to null

5. **Gather Git Information**:
   - Run `git branch --show-current` to get current branch name
   - Determine comparison base:
     - If `baseRefName` was extracted from PR: use `origin/{baseRefName}` as the base
     - If no PR context (silent mode or no PR): fall back to `origin/HEAD` and note in summary that commit/diff info may be incomplete
   - Run `git log --oneline {base}..HEAD` to get commits made (where `{base}` is the determined comparison base)
   - Run `git diff --stat {base}..HEAD` to get files changed summary

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

   For each acceptance criterion from the Requirements Definition section:
   - Read the specification and implementation to determine if criterion was met
   - Mark with `[x]` if criterion is verifiably completed (code exists, tests pass)
   - Mark with `[ ]` if criterion was not implemented or cannot be verified
   - Mark with `[~]` if partially implemented

   - [{status}] {criterion 1}
   - [{status}] {criterion 2}
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
   - **Final Status**: {APPROVED/NEEDS_CHANGES/N/A}

   ### Code Review

   - **Iterations**: {count}
   - **Final Status**: {APPROVED/N/A}

   ## Deliverables

   - **Pull Request**: {PR_URL or "Not created (silent mode)"}
   - **Branch**: `{branch_name}`

   ## Commits

   {git log --oneline output}
   ```

7. **Output Summary to User**:
   - Display the key sections of the summary to the user
   - Inform them where the full summary file is located
