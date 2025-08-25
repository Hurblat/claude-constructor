# Claude Constructor

A systematic workflow engine for implementing functionality with Claude Code, designed with quality-driven development practices and planning at the center.

## Overview

This system orchestrates feature development through a structured 13-step workflow that covers complete implementation, comprehensive testing, and automated code review. Each command works together as part of a larger orchestrated process.
The goal has been to enable Claude Code to work for extended periods of time without deviating from the plan.

## Core Workflow

The main orchestrator (`feature.md`) follows this sequence:

### Planning
1. **Read configuration files** - Load development guidelines, quality gates, and other documentation
2. **Create state management file** - Used to track workflow progress
3. **Read Linear issue** - Fetch issue details via Linear MCP
4. **Define requirements** - Create detailed requirements specification covering business value, user journey, acceptance criteria, and technical constraints
5. **Get requirements sign-off** - Iterate on the requirements definition until it's ready *(Human Required)*
6. **Write specification** - Technical spec with parallelization plan
7. **Get specification sign-off** - Iterate on the specification until it's ready *(Human Required)*

### Implementation
8. **Check out new branch** - Create feature branch
9. **Implement increment** - Execute with parallel subagents if possible
10. **Write end-to-end tests** - Cover user behavior

### Review
11. **Perform code review** - Self-review, addressing findings automatically
12. **Create pull request** - Creating a pull request on GitHub, describing the work
13. **Review pull request** - Monitor and respond to feedback *(Human Required)*

## Usage

There are two ways of using this workflow.

1. Put the command files in your `.claude/commands` folder (either in your project or your home directory), and docs/ in the root of your project.
Then run the following:

```bash
> claude
> /feature ABC-123
```

2. Run the workflow from this directory, to make changes in a different code base.
This enables you to reuse this workflow with any repository without copying/moving files.

```bash
> claude
> /add-dir $path_to_target_repository
> /feature ABC-123
```

Documentation for [`/add-dir`](https://docs.anthropic.com/en/docs/claude-code/cli-reference).

Notes:
- If you want to skip the issue tracking system you could update the workflow to start with a prompt instead

## Configuration

### Issue Tracking System Integration

The workflow supports multiple issue tracking systems through an abstraction layer. This allows you to use Linear, Jira, GitHub Issues, or any other issue tracking system by configuring the provider.

#### Configuration File

Similar to `./claude/settings.json` and `.claude/settings.local.json`, there are two ways of using configuration in Claude Constructor.
`.claude/settings.claude-constructor.json` has default values, but you can override these by creating `.claude/settings.claude-constructor.local.json`.

```json
# .claude/settings.claude-constructor.json
{
  "issue-tracking-provider": "linear",
  "default-branch": "main",
  "silent-mode": false
}
```

#### Supported Providers

**Linear (Default)**
```json
# .claude/settings.claude-constructor.json
{
  "issue-tracking-provider": "linear"
}
```

- Requires Linear MCP integration configured
- Uses `linear:get_issue`, `linear:update_issue`, `linear:create_comment`, `linear:list_issue_statuses`
- Supports fuzzy matching for status names

**Jira**
```json
# .claude/settings.claude-constructor.json
{
  "issue-tracking-provider": "jira"
}
```
- Requires Jira MCP integration configured
- Uses `jira:get_issue`, `jira:add_comment_to_issue`, `jira:get_transitions_for_issue`, `jira:transition_issue`
- Supports fuzzy matching for status names

#### Silent Mode

Silent mode allows you to run the workflow without making external API calls to issue tracking systems or creating GitHub pull requests. This is useful for:
- Testing workflows locally without side effects
- Dry-run scenarios to verify changes
- Development environments where external integrations are not available

To enable silent mode, set `"silent-mode": true` in your configuration:

```json
# .claude/settings.claude-constructor.json
{
  "silent-mode": true
}
```

When silent mode is enabled:
- **Issue comments**: Logged locally but not posted to issue tracker
- **Issue status updates**: Logged locally but not updated in the issue tracker
- **GitHub pull requests**: Code is committed and pushed, but PR creation is skipped
- **PR review comments**: Skipped entirely
- All other operations (git commits, code changes, tests) execute normally

#### Issue Tracking System Requirements

The workflow expects issues to support these standard status transitions:
- **"In Progress"** - When implementation begins
- **"Code Review"** - When automated code review is done and pull request has been created

Your issue tracking system should have statuses that match or can be mapped to these workflow states.

#### Adding New Providers

To add support for additional issue tracking systems (GitHub Issues, etc.):

1. Update the issue command files (`get-issue.md`, `update-issue.md`, `create-comment.md` etc.)
2. Add provider-specific MCP command mappings
3. Add the new provider option to the configuration

### Other Customizations

This repository is a work in progress, and there are things you might want to change to fit your setup better:

- Using different status transitions within your issue tracking system
- Adding reference points for your specific way of doing things, e.g. adding documentation on your E2E test principles in `docs/` and then reference it in `commands/write-end-to-end-tests.md`
- Tweaking your technical guardrails (described in `CLAUDE.md`). I recommend using pre-commit hooks and/or Claude Code hooks and/or CI to make sure the technical guardrails are enforced. TDD is also a great instrument in my opinion.
- Adapting the git branch and commit guidelines to suit your preferences

## Key Features

### Extensive Planning
- Focus on creating a solid plan before starting any work
- Transparent description of Claude Code's understanding of the work to be done, and assumptions made

### Parallel Execution
- Specifications identify independent components (backend APIs, frontend components, database migrations)
- Agent IDs assigned for parallel work with dependency management

### State Management
- Persistent tracking across all workflow steps in `state_management/{issue_key}.md`
- TODO list maintenance and resumable workflows

### Issue Tracking Integration
- Issue status updates at each workflow stage
- Progress comments with implementation details

## Human-in-the-Loop Points

The workflow includes critical human approval gates:

### 1. Requirements Sign-off (Step 5)
- **Process**: Claude Constructor presents assumptions and detailed understanding of requirements
- **Human Required**: Must approve definition of requirements

### 2. Specification Sign-off (Step 7)
- **Process**: Claude Constructor presents assumptions and detailed specification for review
- **Human Required**: Must approve technical specification before implementation begins

### 3. Pull Request Review (Step 13)
- **Human Required**: Reviewing and approving pull request on GitHub
- **Process**: Human adds comments/feedback directly in GitHub PR interface as part of a Review
- **Workflow**: Claude Constructor monitors for new comments but must be asked to check for updates, and the Review needs to be submitted

### 4. Merging Pull Request (After Step 13)
- **Human Required**: Must merge the pull request manually

These gates ensure human oversight of decisions and final code quality before delivery.

I also recommend checking in on the work as it is happening, to gauge if anything was missed in the specification or otherwise not going according to plan.

## Prerequisites

### Technical Requirements
- Python (Python 2 or Python 3)
- Issue tracking system MCP integration configured (see Issue Tracking System Integration section)
- GitHub CLI (`gh`) authenticated
- Git repository
- Quality gate tools available

### Required Configuration Files
- `/CLAUDE.md` - General principles, quality gates, and development workflow
- `docs/git-commit.md` - Git commit guidelines (example available in `docs/git-commit.md` in Claude Constructor)
- `.claude/settings.claude-constructor.json` - Configuration of issue tracking provider, default git branch name, and silent mode

### Optional Configuration Files
- `docs/requirements.md` - Domain principles and business rules (can be referenced during implementation planning and code review)
- ...and any additional context

### Issue Requirements
**The workflow assumes well-groomed issues.** Users must ensure issues contain:
- Clear problem definition and business context
- Detailed feature requirements and acceptance criteria
- Proposed solution approach or architecture direction
- Sufficient domain context for implementation decisions
- Any relevant technical constraints or considerations

The quality of the implementation depends directly on the quality of the issue description and context provided.

## File Structure

In this repository:

```
.claude/
├── commands/
│   ├── feature.md                          # Main orchestrator
│   ├── create-state-management-file.md
│   ├── read-issue.md
│   ├── define-requirements.md
│   ├── requirements-sign-off.md
│   ├── write-specification.md
│   ├── specification-sign-off.md
│   ├── git-checkout.md
│   ├── implement-increment.md
│   ├── implement-sub-increment.md
│   ├── write-end-to-end-tests.md
│   ├── code-review.md
│   ├── create-pull-request.md
│   ├── review-pull-request.md
│   ├── issue/
│   │   ├── get-issue.md                    # Issue tracking system: Get issue details
│   │   ├── update-issue.md                 # Issue tracking system: Update issue status
│   │   ├── create-comment.md               # Issue tracking system: Add comments to issue
├── settings.claude-constructor.json        # Configuration settings (project level, checked in)
└── settings.claude-constructor.local.json  # Configuration settings (local, gitignored)

docs/
└── git-commit.md
```

In the target repository:

```
state_management/                   # Generated during workflow
└── {issue_key}.md

specifications/                     # Generated during workflow
└── {issue_key}_specification_{timestamp}.md
```
