---
name: implement-increment
description: Orchestrate implementation of feature increment
argument-hint: [issue-key] [state-management-file-path]
model: claude-sonnet-4-5
---

# Implement Increment Command

## Purpose

Implement the increment using the specification in the state management file.
These instructions are read and followed as part of a larger workflow.
You MUST follow all workflow steps below, not skipping any step and doing all steps in order.

## Workflow Steps

1. Ensure that the specification was explicitly signed off by the user. If not, go back to the specification signoff step in the larger workflow.

2. Update issue status to "In Progress":
   - Use the SlashCommand tool to execute `/update-issue $1 "In Progress"`

3. Add implementation comment:
   - Read the state management file ($2) to get the specification file name
   - Use the SlashCommand tool to execute `/create-comment $1 "Claude Code implementation started for [specification-file-name]"`

4. Understand the division of work and implement tasks:
    - Read specification to identify agent_ids and Dependency Graph from the Implementation Plan
    - Check for code review feedback:
      - Determine code-review file path: `code_reviews/{issue-key}.md` (where issue-key is $1)
      - If file exists: Read the latest review (most recent "Review #N" section) to understand what needs fixing
      - If this is a revision (code-review file exists), prioritize addressing review issues over spec additions
      - Note: Subagents will automatically check for and read code_reviews/{issue-key}.md if it exists - no need to pass review content explicitly
    - Create "Implementation Agents Status" section in state management file to track progress:

      ```markdown
      ## Implementation Agents Status
      - agent-1: pending (revision: 0)
      - agent-2: pending (revision: 0)
      ```

    - Process agents in dependency order:
      a. Identify agents with no dependencies or whose dependencies are complete
      b. Update their status to "in_progress" in Implementation Agents Status
      c. Spawn those agents in parallel using the increment-implementer subagent via Task tool
      d. Pass to each subagent: the agent_id and state management file path
      e. Monitor for completion signals ("AGENT_COMPLETE: [agent_id]")
      f. When an agent reports completion, invoke increment-implementer-auditor subagent via Task tool
      g. Pass to auditor: the agent_id and state management file path
      h. Wait for audit result (AUDIT_PASSED/AUDIT_FAILED)
      i. If audit passes, update status to "completed" in Implementation Agents Status
      j. If audit fails:
         - Update status to "needs_revision" in Implementation Agents Status
         - Extract specific feedback from audit report
         - Re-spawn the increment-implementer subagent with the feedback
         - Pass: agent_id, state management file path, and "Validator/Auditor feedback: [specific issues]"
         - Increment revision counter for tracking
         - Repeat audit cycle until pass or max revisions reached (3 attempts)
         - If max revisions reached, mark as "failed" and handle as agent failure
      k. Repeat until all agents are complete
    - Handle agent failures:
      - If an agent reports failure, mark it as "failed" in Implementation Agents Status
      - Do not spawn agents that depend on failed agents
      - Report the failure chain to the user
    - When all agent_ids are complete, implementation is finished

## This part of the workflow is done when

- [ ] All subagents are complete and have passed their audits
- [ ] All audit feedback has been addressed through the revision process
- [ ] Single behavior is fully implemented, both on the backend and the frontend
- [ ] All unit and integration tests pass
- [ ] All quality gates pass (see @CLAUDE.md for commands)
- [ ] No breaking changes introduced
- [ ] No test failures introduced in areas of the code unrelated to this increment
- [ ] Feature works in both development and build modes
- [ ] Business rules are enforced consistently
- [ ] Implementation strictly adheres to specification without scope creep
- [ ] No unnecessary code or over-engineering detected in audits
