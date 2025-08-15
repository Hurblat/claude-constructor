# Review Pull Request Command

## Purpose

Review pull request for the increment implemented to satisfy the issue described in $ARGUMENTS.
This command is called by an orchestrating command, and is one of the steps in a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. Monitor the pull request for comments and/or reviews. Use `gh api repos/{OWNER}/{REPO}/pulls/{PR_NUMBER}/comments --jq '.[] | {author: .user.login, body: .body, path: .path, line: .line}'`

2. For each unaddressed comment:
  - Implement the requested changes
  - Commit and push changes. Read `docs/git-commit.md` for commit guidelines. Check that there are not unstaged changes you haven't considered.

3. Add a reply to each addressed comment explaining how the requested changes were addressed (or if it was a question, your response to the question):
  `gh api repos/{OWNER}/{REPO}/pulls/{PR_NUMBER}/comments --method POST --field body="Your message here" --field in_reply_to={COMMENT_ID_NUMBER}`
  - Do not edit existing comments
  - Do not make general PR comments

4. Repeat steps 1 through 3 until the user approves the pull request. You are not allowed to approve the pull request yourself.

5. Add pull request feedback comment - run the .claude/commands/issue/create-comment.md command, passing the issue key and feedback summary as arguments to it

Get the issue key from the state management file in $ARGUMENTS.

Format the arguments as:
```
Issue Key: [issue key from state management file]
Comment Text: [user feedback summary and changes made in response]
```

6. Report DONE to the orchestrating command
