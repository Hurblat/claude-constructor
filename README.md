# Claude Constructor

A systematic workflow engine for implementing functionality with Claude Code, designed with quality-driven development practices and planning at the center.

## Overview

This system orchestrates feature development through a structured 16-step workflow that covers complete implementation, comprehensive testing, and automated code review. Each command works together as part of a larger orchestrated process.
The goal has been to enable Claude Code to work for extended periods of time without deviating from the plan.

## Core Workflow

The main orchestrator (`feature.md`) follows this sequence:

### Planning
1. **Read configuration files** - Load development guidelines, quality gates, and other documentation
2. **Create state management file** - Used to track workflow progress
3. **Read settings** - Get issue tracker and other settings
4. **Read Linear issue** - Fetch issue details via Linear MCP
5. **Define requirements** - Create detailed requirements specification covering business value, user journey, acceptance criteria, and technical constraints (using specialized agent)
6. **Validate requirements** - Quality assurance check to ensure requirements are complete, clear, and testable
7. **Get requirements sign-off** - Iterate on the requirements definition until it's ready *(Human Required)*
8. **Write specification** - Technical spec with parallelization plan (using specialized agent)
9. **Validate specification** - Technical validation to ensure implementation plan is actionable and properly parallelized
10. **Get specification sign-off** - Iterate on the specification until it's ready *(Human Required)*

### Implementation
11. **Check out new branch** - Create feature branch
12. **Implement increment** - Execute with parallel subagents if possible
13. **Write end-to-end tests** - Cover user behavior

### Review
14. **Perform code review** - Self-review, addressing findings automatically
15. **Create pull request** - Creating a pull request on GitHub, describing the work
16. **Review pull request** - Monitor and respond to feedback *(Human Required)*

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

Configuration in Claude Constructor works with schema defaults and optional local overrides.

The defaults are defined in `.claude/settings.claude-constructor.schema.json`. You can override these defaults by creating `.claude/settings.claude-constructor.local.json`. If no local settings file exists, the schema defaults will be used automatically.

An example configuration is provided in `.claude/settings.claude-constructor.example.json` for reference.

```json
# .claude/settings.claude-constructor.example.json
{
  "issue-tracking-provider": "linear",
  "default-branch": "main",
  "silent-mode": false
}
```

#### Supported Providers

**Linear (Default)**
```json
# .claude/settings.claude-constructor.example.json
{
  "issue-tracking-provider": "linear"
}
```

- Requires Linear MCP integration configured
- Uses `linear:get_issue`, `linear:update_issue`, `linear:create_comment`, `linear:list_issue_statuses`
- Supports fuzzy matching for status names

**Jira**
```json
# .claude/settings.claude-constructor.example.json
{
  "issue-tracking-provider": "jira"
}
```
- Requires Jira MCP integration configured
- Uses `jira:get_issue`, `jira:add_comment_to_issue`, `jira:get_transitions_for_issue`, `jira:transition_issue`
- Supports fuzzy matching for status names

**Prompt Issue (No External Integration)**
```json
# .claude/settings.claude-constructor.json
{
  "issue-tracking-provider": "prompt"
}
```
- No external issue tracking system required
- Prompts user for issue title and description during workflow
- Automatically skips all external API calls (same as silent mode)
- Perfect for local development and experimentation

#### Silent Mode

Silent mode allows you to run the workflow without making external API calls to issue tracking systems or creating GitHub pull requests. This is useful for:
- Testing workflows locally without side effects
- Dry-run scenarios to verify changes
- Development environments where external integrations are not available

To enable silent mode, set `"silent-mode": true` in your configuration:

```json
# .claude/settings.claude-constructor.example.json
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

**Note**: The `"prompt"` provider automatically behaves like silent mode, so you don't need to set both.

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

### 1. Requirements Sign-off (Step 7)
- **Process**: Claude Constructor presents assumptions and detailed understanding of requirements after validation
- **Human Required**: Must approve definition of requirements

### 2. Specification Sign-off (Step 10)
- **Process**: Claude Constructor presents assumptions and detailed specification for review after validation
- **Human Required**: Must approve technical specification before implementation begins

### 3. Pull Request Review (Step 16)
- **Human Required**: Reviewing and approving pull request on GitHub
- **Process**: Human adds comments/feedback directly in GitHub PR interface as part of a Review
- **Workflow**: Claude Constructor monitors for new comments but must be asked to check for updates, and the Review needs to be submitted

### 4. Merging Pull Request (After Step 16)
- **Human Required**: Must merge the pull request manually

These gates ensure human oversight of decisions and final code quality before delivery.

I also recommend checking in on the work as it is happening, to gauge if anything was missed in the specification or otherwise not going according to plan.

## Prerequisites

### Technical Requirements
- Python (python3)
- Issue tracking system MCP integration configured (see Issue Tracking System Integration section)
- GitHub CLI (`gh`) authenticated
- Git repository
- Quality gate tools available

### Required Configuration Files
- `/CLAUDE.md` - General principles, quality gates, and development workflow
- `docs/git-commit.md` - Git commit guidelines (example available in `docs/git-commit.md` in Claude Constructor)
- `.claude/settings.claude-constructor.example.json` - Example configuration file showing available settings

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
├── agents/
│   ├── requirements-definer.md               # Specialized agent for defining requirements
│   ├── requirements-validator.md             # Quality assurance for requirements completeness
│   ├── specification-writer.md               # Specialized agent for writing specifications
│   └── specification-validator.md            # Technical validation of implementation plans
├── commands/
│   ├── feature.md                            # Main orchestrator
│   ├── create-state-management-file.md
│   ├── read-settings.md
│   ├── requirements-sign-off.md
│   ├── specification-sign-off.md
│   ├── git-checkout.md
│   ├── implement-increment.md
│   ├── implement-sub-increment.md
│   ├── write-end-to-end-tests.md
│   ├── code-review.md
│   ├── create-pull-request.md
│   ├── review-pull-request.md
│   └── issue/
│       ├── get-issue.md                      # Issue tracking system: Get issue details
│       ├── read-issue.md                     # Issue tracking system: Read issue details
│       ├── update-issue.md                   # Issue tracking system: Update issue status
│       └── create-comment.md                 # Issue tracking system: Add comments to issue
├── settings.claude-constructor.example.json  # Example configuration file
├── settings.claude-constructor.local.json    # Configuration file (local Claude Constructor settings, gitignored)
├── settings.claude-constructor.schema.json   # Configuration schema with defaults
├── settings.json                             # General Claude settings
└── settings.local.json                       # Local Claude settings (gitignored)

docs/
└── git-commit.md
```

In the target repository:

```
state_management/                             # Generated during workflow
└── {issue_key}.md

specifications/                               # Generated during workflow
└── {issue_key}_specification_{timestamp}.md
```
