---
name: review-pull-request
description: Monitor and respond to PR feedback
argument-hint: [issue-key] [state-management-file-path]
---

# Review Pull Request Command

## Purpose

Review pull request for the increment implemented to satisfy the issue.
This command is called by an orchestrating command, and is one of the steps in a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. **Load Settings**: Read the Settings section in the state management file ($2)

2. **Check Silent Mode**:
   - If `silentMode` is `true`:
     - Log: "Silent mode: Skipping PR review monitoring and comments"
     - Skip to step 7
   - If `silentMode` is `false`:
     - Continue with normal PR review workflow (steps 3-6)

3. Monitor the pull request for comments and/or reviews. Use `gh api repos/{OWNER}/{REPO}/pulls/{PR_NUMBER}/comments --jq '.[] | {author: .user.login, body: .body, path: .path, line: .line}'`

4. For each unaddressed comment:
    - Implement the requested changes
    - Commit and push changes. Read @docs/git-commit.md for commit guidelines. Check that there are not unstaged changes you haven't considered.

5. Add a reply to each addressed comment explaining how the requested changes were addressed (or if it was a question, your response to the question): `gh api repos/{OWNER}/{REPO}/pulls/{PR_NUMBER}/comments --method POST --field body="Your message here" --field in_reply_to={COMMENT_ID_NUMBER}`
    - Do not edit existing comments
    - Reply to specific comments, do not make general PR comments

6. Repeat steps 3 through 5 until the user approves the pull request. You are not allowed to approve the pull request yourself.

7. **Add pull request feedback comment** (only if not silent mode and not prompt):
   - If `silentMode` is `false` AND `issueTrackingProvider` is NOT `"prompt"`:
     - Generate a concise feedback summary from steps 3-6:
       - List reviewer comments/feedback received
       - Describe changes made in response to each
       - Note any questions answered
       - Format as a brief markdown summary (e.g., "**PR Feedback Addressed:**\n- Fixed X per reviewer comment\n- Updated Y as requested")
     - Use the Skill tool to execute `/create-comment $1 "{generated-feedback-summary}" $2`
   - If `silentMode` is `true` OR `issueTrackingProvider` is `"prompt"`:
     - Log: "Skipping PR feedback comment (silent mode or prompt provider)"
