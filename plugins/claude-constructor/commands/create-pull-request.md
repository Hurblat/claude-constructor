---
name: create-pull-request
description: Commit changes and create pull request
argument-hint: [issue-key] [state-management-file-path]
model: claude-haiku-4-5
---

# Create Pull Request Command

## Purpose

Create pull request for increment implemented to satisfy the issue.
Add, commit, push code for the finished increment. Create Pull request in GitHub using the `gh` CLI.
This command is called by an orchestrating command, and is one of the steps in a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. List unstaged changes using `git status`

2. Read the specification linked in the state management file ($2) and compare with unstaged changes to understand how the increment has been implemented and which unstaged changes are relevant to the increment. Ignore the specifications and state_management folders.

3. Create a git commit using the guidelines in @docs/git-commit.md

4. Push the commit using `git push`

5. Read the Settings section in the state management file ($2)

6. **Check Silent Mode for Pull Request Creation**:
   - If `silentMode` is `false`:
     - Create a pull request using `gh pr create --title "feat: $1 [brief description from commit]" --base [default branch name] --head $(git branch --show-current)`
   - If `silentMode` is `true`:
     - Log: "Silent mode: Would have created PR with title 'feat: [issue key] [brief description]'"
     - Skip the actual PR creation

7. **Check Silent Mode for Issue Status Update**:
   - If `silentMode` is `false` AND `issueTrackingProvider` is NOT `"prompt"`:
     - Use the SlashCommand tool to execute `/update-issue $1 "Code Review" $2`
   - If `silentMode` is `true` OR `issueTrackingProvider` is `"prompt"`:
     - Log: "Silent mode: Would have updated issue $1 status to 'Code Review'"
     - Skip the issue update
