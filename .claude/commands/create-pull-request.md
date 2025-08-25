---
allowed-tools: Bash(git status:*), Bash(git push:*), Bash(gh pr create:*), Bash(git branch:*)
description: Create pull request for implemented increment
---

# Create Pull Request Command

## Purpose

Create pull request for increment implemented to satisfy the issue described in $ARGUMENTS.
Add, commit, push code for the finished increment. Create Pull request in GitHub using the `gh` CLI.
This command is called by an orchestrating command, and is one of the steps in a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. List unstaged changes using !`git status`

2. Read the specification linked in $ARGUMENTS to and compare with unstaged changes to understand how the increment has been implemented and which unstaged changes are relevant to the increment. Ignore the specifications and state_management folders.

3. Create a git commit using the guidelines in @docs/git-commit.md

4. Push the commit using !`git push`

5. Read the Settings section in $ARGUMENTS to get the following:
   - The default branch name from the "default-branch" field
   - The silent mode setting from the "silent-mode" field

6. **Check Silent Mode for Pull Request Creation**:
   - If `silent-mode` is `false`:
     - Create a pull request using !`gh pr create --title "feat: [issue key] [brief description from commit]" --base [default branch name] --head $(!git branch --show-current)`
   - If `silent-mode` is `true`:
     - Log: "Silent mode: Would have created PR with title 'feat: [issue key] [brief description]'"
     - Skip the actual PR creation

7. **Check Silent Mode for Issue Status Update**:
   - If `silent-mode` is `false`:
     - Update issue status to "Code Review" - run the .claude/commands/issue/update-issue.md command, passing the issue key and new status as arguments to it
     
     Get the issue key from the state management file in $ARGUMENTS.
     
     Format the arguments as:
     ```
     Issue Key: [issue key from state management file]
     New Status: Code Review
     ```
   - If `silent-mode` is `true`:
     - Log: "Silent mode: Would have updated issue [issue key] status to 'Code Review'"
     - Skip the issue update

8. **Legacy Linear Update** (if applicable and silent mode is false):
   - Update Linear issue status to "Code Review" using `linear:update_issue`
   - Skip if silent mode is true

9. Report DONE to the orchestrating command
