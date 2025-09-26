# Claude Constructor

A workflow automation system that helps Claude Code implement features systematically in your codebase with built-in planning, validation, and review steps.

## What It Does

Claude Constructor provides a `/feature` command that guides Claude Code through a complete feature development workflow - from understanding requirements to creating a pull request. Instead of giving Claude Code open-ended instructions, this system ensures it follows a structured process that includes planning, getting your approval, implementing, testing, and self-review.

The workflow prevents common issues like Claude Code losing focus, making unplanned changes, or implementing features differently than intended.

## Quickstart

> **Important:** Claude Constructor will work with you to define requirements and create specifications, but the more detail you provide upfront, the better the results. Whether providing a prompt directly or using issue tracking, include clear requirements, acceptance criteria, and technical constraints when possible. The workflow includes approval gates where you can refine requirements before implementation begins.

### Prerequisites

**Required:**
- Claude Code CLI installed and configured
- GitHub CLI (`gh`) authenticated
- Python 3 installed

**Optional:**
- Linear MCP or Jira MCP configured (for issue tracking integration)

### Quick Setup (No Configuration Required)

1. **Clone and start using immediately:**
   ```bash
   git clone https://github.com/Hurblat/claude-constructor.git
   cd claude-constructor
   claude
   > /add-dir /path/to/your/project
   > /feature Add dark mode toggle to settings page
   ```

   That's it! No configuration needed. Just describe your feature and Claude Constructor will guide you through the complete workflow - from requirements to pull request.

### Using with Issue Tracking (Optional)

If you use Linear or Jira for issue tracking:

1. **Create configuration file:**
   ```bash
   cp .claude/settings.claude-constructor.example.json .claude/settings.claude-constructor.local.json
   ```

2. **Edit the configuration:**
   ```json
   {
     "issue-tracking-provider": "linear"  // or "jira"
   }
   ```

3. **Run with issue key:**
   ```bash
   claude
   > /add-dir /path/to/your/project
   > /feature ABC-123
   ```

### Tips for Success

- **Be specific**: Whether using a feature description (`/feature Add dark mode`) or issue key (`/feature ABC-123`), provide clear requirements
- **Use silent mode** for testing: Add `"silent-mode": true` to skip issue tracker updates and PR creation
- **Monitor progress**: Claude Constructor will update you at each step and ask for approval at key points
- **Check the state file**: Find detailed progress in `state_management/{issue_key}.md` or `state_management/prompt-{number}.md`

## Core Workflow

The main orchestrator (`feature.md`) follows this sequence:

### Planning
1. **Read configuration files** - Load development guidelines, quality gates, and other documentation
2. **Create state management file** - Used to track workflow progress
3. **Read settings** - Get issue tracker and other settings
4. **Read issue/prompt** - Get feature details (from prompt or issue tracker)
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

### Alternative: Install directly in your project

If you prefer to have the workflow files in your project repository, you can copy the command files to your project's `.claude/commands` folder and `docs/` to your project root. Then run:

```bash
cd /your/project
claude
> /feature ABC-123
```

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

**Prompt Mode (No External Integration)**
```json
# .claude/settings.claude-constructor.json
{
  "issue-tracking-provider": "prompt"
}
```
- No external issue tracking system required
- Use with: `/feature Your feature description here`
- Creates local issue keys (prompt-1, prompt-2, etc.)
- Perfect for local development and experimentation
- Note: Automatically skips issue tracker API calls (but still creates PRs unless silent mode is also enabled)

#### Silent Mode

Silent mode prevents external API calls to issue trackers and GitHub, useful for testing and dry-runs. It works with any provider including prompt mode.

To enable silent mode, set `"silent-mode": true` in your configuration:

```json
# .claude/settings.claude-constructor.example.json
{
  "silent-mode": true,
  "issue-tracking-provider": "linear"  // or "jira" or "prompt"
}
```

When silent mode is enabled:
- **Issue comments**: Logged locally but not posted to issue tracker
- **Issue status updates**: Logged locally but not updated in the issue tracker
- **GitHub pull requests**: Code is committed and pushed, but PR creation is skipped
- **PR review comments**: Skipped entirely
- All other operations (git commits, code changes, tests) execute normally

**Note:** The `"prompt"` provider automatically skips issue tracker calls, but you still need `"silent-mode": true` if you want to skip GitHub PR creation.

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

### Input Requirements

Claude Constructor will help you refine and validate requirements during the workflow, but providing clear input upfront leads to better results.

**Helpful details to include (when known):**
- Clear problem definition and business context
- Detailed feature requirements and acceptance criteria
- Proposed solution approach or architecture direction
- Sufficient domain context for implementation decisions
- Any relevant technical constraints or considerations

The workflow includes human approval gates where you can iterate on requirements and specifications before implementation begins. For issue tracking systems, well-groomed issues will streamline this process.

### Example: Well-Defined Input

**Good Example (Issue or Prompt):**
```
Title: Add user preference for date format display

Description:
Currently, all dates in the application are displayed in US format (MM/DD/YYYY). International users have requested the ability to choose their preferred date format.

Requirements:
- Add a date format preference to user settings (options: US, ISO, European)
- Store preference in user profile database
- Apply format throughout the application (dashboard, reports, transaction history)
- Default to US format for existing users to maintain backward compatibility

Technical Notes:
- Use existing DateFormatter utility class
- Preference should persist across sessions
- Consider timezone handling for consistency

Acceptance Criteria:
- [ ] User can select date format in settings page
- [ ] Selected format applies immediately without page refresh
- [ ] Format persists after logout/login
- [ ] All date displays respect the preference
```

**Poor Example:**
```
Make dates better for international users
```

The workflow will help refine vague requirements, but starting with detail saves iteration cycles and produces better results.

### Optional Configuration Files
- `docs/requirements.md` - Domain principles and business rules (can be referenced during implementation planning and code review)
- ...and any additional context

## File Structure

When using Claude Constructor with `/add-dir` (recommended approach), the workflow files stay in the Claude Constructor repository - you don't need to copy any `.claude/` folders or command files to your project. The `/add-dir` command handles the connection between repositories.

The only files you may want to add to your target project are:
- `/CLAUDE.md` - Your project-specific development guidelines
- `docs/` folder - Any project-specific documentation referenced by the workflow

### Claude Constructor repository files:
These files remain in the Claude Constructor repository and define the workflow:

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

### Generated files in your target repository:
These files are automatically created in your project during the workflow:

```
state_management/                             # Tracks workflow progress
└── {issue_key}.md

specifications/                               # Technical specifications
└── {issue_key}_specification_{timestamp}.md
```
