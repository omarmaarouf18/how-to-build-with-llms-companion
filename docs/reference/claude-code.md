# Claude Code quick reference

Companion to Chapter 2 of *How to Build with LLMs*. The book keeps the concepts; this file keeps the
details that change from release to release. **Checked against the official documentation in
November 2026.** If something here doesn't match what you see, the official docs win, and a pull
request to fix this file is welcome.

Official docs: https://code.claude.com/docs

## Starting a session
| Command | What it does |
|---|---|
| claude | Start an interactive session in the current folder |
| claude "fix the build error" | Start a session with a first prompt |
| claude -c | Continue the most recent conversation in this folder |
| claude -r | Pick a previous conversation to resume |
| claude -p "explain this function" | Run once without the interactive screen, print the answer, and exit (more in 2.12) |

## Tools
Tool names matter: you use the same names in permission rules, sub-agent definitions, and hooks.

| Tool | What it does | Asks first? |
|---|---|---|
| Read | Reads a file with line numbers. Also reads images, PDFs, and Jupyter notebooks | No (inside the project) |
| Write | Creates a file or overwrites it completely | Yes |
| Edit | Replaces one exact piece of text in a file with another | Yes |
| NotebookEdit | Edits cells in a Jupyter notebook | Yes |
| Bash | Runs a shell command (PowerShell on Windows without Git Bash) | Yes, except read-only commands |
| Glob / Grep | Find files by name / search inside files. On macOS and Linux these searches usually run through Bash with built-in fast versions of find and grep | No |
| LSP | Code intelligence: jump to definitions, find references, see type errors | No |
| WebFetch / WebSearch | Fetch a URL / search the web | Yes |
| Agent | Starts a sub-agent with its own context window | No |
| Skill | Loads a skill into the conversation | Yes |
| AskUserQuestion | Asks you multiple-choice questions to clarify a task | No |
| EnterPlanMode / ExitPlanMode | Switch into planning; present a plan for your approval | No / Yes |
| TaskCreate, TaskUpdate, TaskList | Keep a checklist of steps for long tasks | No |
| Monitor | Runs a command in the background and feeds its output back as it arrives | No |
| EnterWorktree | Creates an isolated git worktree to work in | No |
| MCP tools | Any tools from MCP servers you connect, named mcp__server__tool | Yes |

The list keeps growing (scheduling, notifications, messaging between sessions). Ask Claude Code itself, or
check the tools reference, for the current list.

## Permission modes
Press Shift+Tab to cycle. Which mode a new session starts in depends on your version and settings.

| Mode | Behavior | Use it when |
|---|---|---|
| Manual | Asks before edits, commands, and other risky actions | You're learning, or the code is sensitive |
| acceptEdits | Edits files and runs basic file commands (mkdir, mv, cp) without asking; asks for other commands | You trust the direction and will review the diff |
| plan | Reads and explores, but doesn't edit your source files; ends with a plan for you to approve | Before any non-trivial change |
| auto | A separate classifier model reviews actions in the background and blocks risky ones instead of asking you | Longer tasks where approvals would interrupt you |
| dontAsk | Denies anything that isn't pre-approved | Unattended scripts with an explicit allow list |
| bypassPermissions | Skips permission prompts | Only in isolated environments like a throwaway container |

## Context commands
| Command | What it does | Use it when |
|---|---|---|
| /context | Shows what's using the context, as a colored grid | You want to know why a session feels slow or forgetful |
| /clear | Starts a fresh conversation | Between unrelated tasks, always |
| /compact [focus] | Summarizes the conversation to free space | A long task must continue; tell it what to keep |
| /btw | Asks a side question that never enters the history | Quick checks that shouldn't clutter the context |
| Sub-agents | Do research in a separate context and return a summary | Investigations that read many files |

## Everyday commands
Type `/` to see everything available.

| Command | Purpose |
|---|---|
| /init | Generate a starter CLAUDE.md |
| /model | Switch model (and adjust effort level) |
| /permissions | View and edit allow, ask, and deny rules |
| /mcp | Manage MCP server connections |
| /rewind | Restore code and/or conversation to a checkpoint |
| /resume | Continue a previous session |
| /usage (or /cost) | Session cost and plan limits |
| /memory | Edit CLAUDE.md files and auto memory |
| /hooks | See configured hooks |
| /doctor | Diagnose installation and configuration problems |

## Hook events
| Event | Runs | Example use |
|---|---|---|
| SessionStart | When a session starts or resumes | Load environment variables, print project status |
| UserPromptSubmit | When you send a prompt, before Claude sees it | Add context, block prompts containing secrets |
| PreToolUse | Before a tool runs; can block it | Refuse edits to migrations/, block dangerous commands |
| PostToolUse | After a tool succeeds | Run the formatter or linter after every edit |
| Stop | When Claude finishes its turn | Run the tests; refuse to stop until they pass |
| PreCompact | Before the context is compacted | Save a copy of the transcript |
