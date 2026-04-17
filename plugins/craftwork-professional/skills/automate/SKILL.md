---
name: automate
description: Build automation scripts and pipelines that use coding-agent CLIs (Claude Code, Codex, Gemini CLI, GitHub Copilot CLI) in headless/non-interactive mode as the AI engine, or delegate work to cloud agents (`gh agent-task`) that open pull requests asynchronously. Use this skill whenever the user wants to write a shell script, CI job, cron task, batch processor, webhook handler, or any automation that shells out to `claude`, `codex`, `gemini`, `copilot`, or `gh agent-task` — single-turn prompts, multi-turn agentic loops, parallel fan-out across files/folders, structured JSON outputs consumed by downstream tools, or cloud-delegated tasks that produce PRs. Trigger on phrases like "script that uses Claude", "automate with Claude Code", "headless Claude", "batch process files with an LLM", "pipeline with codex exec", "gemini -p", "copilot --autopilot", "gh agent-task create", "GitHub Action that calls Claude", "cron job to review PRs", "agent loop in bash", "dispatch an agent task to open a PR", "fleet-wide agent-task across repos", or any request to integrate a coding agent CLI into an automated workflow. Also trigger when the user describes the shape of a pipeline (fan-out, map-reduce, review-then-fix, extract-then-summarize, ticket-to-PR, scheduled fleet upgrade) and AI is the engine, even if they don't name the CLI explicitly.
---

# Coding-Agent CLI Automation

You are helping the user build automation that uses a coding-agent CLI as its AI engine. The work lives at the boundary between shell scripting and prompt engineering — the CLI does the intelligence, your script orchestrates.

## Two categories of automation

Automation with coding agents comes in two shapes. Pick the category before you pick the tool:

1. **Local execution** — the agent runs on your machine or CI runner, against files in cwd. Synchronous, output streams to stdout, you decide what happens with the result. Use for: everything that produces artifacts other than PRs (reports, JSON, edits committed by your own script, batch transforms).
2. **Delegated cloud execution** — you dispatch a task to a cloud-hosted agent, which works asynchronously and opens a pull request against the repo. Use for: "I want an agent to implement this and open a PR" workflows triggered by tickets, issues, scheduled runs, or webhooks.

Local-execution CLIs ship a non-interactive mode; the flags differ, the mental model is the same:

| CLI | Headless invocation | Key reference |
|-----|--------------------|---------------|
| Claude Code | `claude -p "<prompt>" ...` or `claude --bare -p ...` | `references/claude-code.md` |
| Codex | `codex exec "<prompt>" ...` | `references/codex.md` |
| Gemini CLI | `gemini -p "<prompt>" ...` | `references/gemini.md` |
| GitHub Copilot CLI | `copilot -p "<prompt>" --allow-all-tools --autopilot ...` | `references/copilot.md` |

For delegated cloud execution on GitHub:

| Tool | Dispatch invocation | Key reference |
|------|--------------------|---------------|
| `gh agent-task` (GitHub Copilot coding agent) | `gh agent-task create "<description>" [--base main] [--custom-agent <name>]` | `references/github-agent-task.md` |

The two can be combined — `gh agent-task` opens the PR, a local-execution CLI reviews it. See the cookbook.

**Default to Claude Code** unless the user names a different CLI or the task explicitly benefits from one of the others. Load the relevant reference file when you commit to a CLI — it contains the full flag list, output formats, and gotchas.

## Decide the pipeline shape first

Before writing any code, answer these four questions. They determine every flag choice downstream.

1. **Single-turn or agentic?** Single-turn = one prompt → one answer. Agentic = the model executes tools, reads files, makes edits, iterates. Agentic needs tool permissions and a larger time/token budget.
2. **What does the output feed?** Human eyeballs → plain text. Another shell step → JSON + `jq`. A structured downstream system → JSON Schema–validated output.
3. **One task or many?** Many → fan out in parallel (GNU parallel, xargs -P, background jobs) and collect results. Watch the combined token spend.
4. **Does it need the codebase?** Yes → point the CLI at the working directory (`cd` or `--add-dir` / `-C`) and grant the tools it needs. No → strip context for speed and determinism.

Once you can answer those, the script almost writes itself.

## The five canonical shapes

Most automation is one of these. Reach for the closest match, then adapt. Shapes 1-4 are local execution; shape 5 is cloud delegation.

### 1. Single-turn, extract to JSON

For classification, extraction, summarization, triage. The script gets a structured answer it can parse.

```bash
result=$(claude --bare -p "Classify the severity of this error: $(cat error.log)" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"severity":{"type":"string","enum":["low","medium","high","critical"]},"reason":{"type":"string"}},"required":["severity","reason"]}' \
  --max-budget-usd 0.10)

severity=$(echo "$result" | jq -r '.structured_output.severity')
```

`--bare` here skips auto-loaded hooks, skills, MCP, CLAUDE.md — right for a simple classifier that doesn't need repo context. Drop it if the task benefits from project context. Always set `--max-budget-usd` in scripts that run unattended.

### 2. Agentic loop on a codebase

For "review and fix", "refactor", "add tests". The model needs file access and the ability to run commands.

```bash
cd /path/to/repo
claude -p "Run the test suite and fix any failures. Report which tests you changed." \
  --allowedTools "Bash,Read,Edit" \
  --permission-mode acceptEdits \
  --max-budget-usd 2.00 \
  --output-format json > run.json
```

`--permission-mode acceptEdits` auto-approves filesystem writes. `dontAsk` is stricter (denies anything not explicitly allowed) and better for locked-down CI. See `references/claude-code.md` for the full permission model.

### 3. Multi-turn agentic (chained calls sharing state)

When you want discrete steps with checkpoints — review, then decide, then act — and each step should see the prior context.

```bash
session_id=$(claude -p "Audit the auth module for security issues" \
  --output-format json --allowedTools "Read,Grep,Glob" | jq -r '.session_id')

claude -p "Now prioritize the issues you found by severity" \
  --resume "$session_id" --output-format json > prioritized.json

claude -p "Fix the critical issues only" \
  --resume "$session_id" --allowedTools "Read,Edit" --permission-mode acceptEdits
```

Capture the session_id from the first call's JSON output. `--continue` works for the most-recent-in-cwd case; `--resume <id>` is explicit and parallel-safe.

### 4. Parallel fan-out over many inputs

When the same operation needs to run against N files/PRs/tickets. Use background jobs or `xargs -P`; collect into a directory, then reduce.

```bash
mkdir -p out
find . -name '*.py' -print0 | xargs -0 -P 4 -I {} bash -c '
  f="$1"
  claude --bare -p "Summarize $(cat "$f") in one sentence" \
    --output-format json --max-budget-usd 0.05 \
    > "out/$(basename "$f").json"
' _ {}

jq -s 'map({file: .session_id, summary: .result})' out/*.json > summary.json
```

Bound parallelism (`-P 4`) to avoid rate limits. Budget per call prevents a runaway single task from burning the whole job.

### 5. Delegate to a cloud agent (async PR)

When the output you want is a pull request and you don't need synchronous control. The local CLI is just a dispatcher; the agent runs in GitHub's cloud.

```bash
# Dispatch into the current repo; returns immediately
gh agent-task create "Implement the spec in docs/rfc-042.md" --base main

# Dispatch into ANOTHER repo from outside it — no clone needed
gh agent-task create -F ticket.md --repo my-org/payments-service --base main

# Fan out the same task across a fleet of repos
gh repo list my-org --topic services --json nameWithOwner --jq '.[].nameWithOwner' | \
  while read -r repo; do
    gh agent-task create -F upgrade.md --repo "$repo" --base main
    sleep 2
  done

# Dispatch and follow logs in the foreground
gh agent-task create -F ticket.md --base main --follow

# With a repo-configured custom agent (.github/agents/security-reviewer.md)
gh agent-task create "Audit the auth module" --custom-agent security-reviewer
```

`-R/--repo` is the key orchestration lever — one dispatcher script can address any repo you have access to, no local clones required. This is how "ops dashboard," "ticket router," and "fleet-wide upgrade" pipelines get built.

Exit 0 from `create` means "dispatched," not "agent succeeded." For completion detection, watch the PR state (via `gh pr list` / webhook) or use session ID + `gh agent-task view --follow`. Pair with a local-execution CLI for review-gating — agent opens the PR, Claude/Codex/Gemini/Copilot reviews it before merge. See `references/github-agent-task.md` for the full flag set and pitfalls (preview status, PR-number ambiguity, no JSON output from create).

## Principles that save you later

- **Always set a budget cap, but don't trust it as a hard ceiling.** `--max-budget-usd` on Claude aborts *after* exceeding (the check runs post-turn, so one expensive call can overshoot by 2-3x before stopping). Codex and Gemini have no native budget flag — wrap them with `timeout <N>s`. Check actual spend in the JSON output (`total_cost_usd` for Claude) rather than assuming the cap held. Unattended scripts without caps are how surprise bills happen.
- **Decide context posture deliberately — don't default to stripping or loading everything.** Each CLI auto-loads a stack of context when you invoke it: Claude pulls in `CLAUDE.md`, `~/.claude` hooks, plugins, skills, MCP servers from `.mcp.json`; Codex reads `AGENTS.md`, `~/.codex/config.toml` profiles, configured MCP servers; Gemini loads extensions, skills, hooks, policies; Copilot loads `AGENTS.md`, user skills, the built-in GitHub MCP server, and any configured MCPs. That context is often *why* the agent is competent on this codebase — it encodes conventions, architectural decisions, team-configured tools, and project-specific MCP integrations. **For agentic work on a codebase, you usually want that context loaded.** For classification/extraction on a single file, cross-machine CI reproducibility, or adversarial/untrusted-code runs, you want it stripped (Claude: `--bare`; Codex: explicit `-c` overrides + `--ephemeral`; Gemini: `-e` to restrict extensions, explicit `--policy`; Copilot: `--no-custom-instructions` + `--disable-builtin-mcps`). The choice is per-task, not a universal default.
- **Capture session IDs when you'll chain calls.** Claude uses `.session_id`, Gemini uses `.session_id`, Codex uses `.thread_id` (emitted in the `thread.started` event when `--json` is on). Stash it early; `--continue` / `--last` / `-r latest` shortcuts all break the moment two jobs share state.
- **Always pick a non-interactive permission mode.** Automation has no human at the keyboard, so any mode that prompts for approval either silently blocks or silently denies. Pick from the auto-family for each CLI and never fall back to `default`/`interactive`:
  - **Claude:** `plan` (read-only investigation), `acceptEdits` (agentic dev with writes), `dontAsk` (locked-down CI — deny unless explicitly allowed), `bypassPermissions` / `--dangerously-skip-permissions` (sandboxed envs only). Never use `default` or `auto` in scripts.
  - **Codex:** `--sandbox read-only` (investigation), `--full-auto` / `--sandbox workspace-write` (agentic edits), `--sandbox danger-full-access` (sandboxed envs only). Codex exec doesn't prompt; the sandbox flag IS the permission posture.
  - **Gemini:** `--approval-mode plan` (read-only), `--approval-mode auto_edit` (edits without prompts), `--approval-mode yolo` / `-y` (everything auto-approved). Never use `default` — in headless it turns every `ask_user` policy rule into a silent deny.
  - **Copilot:** `--plan` (read-only), `--autopilot` (autonomous agentic — the script default), paired with `--allow-all-tools` (required for `-p`) and `--no-ask-user` (so the agent can't pause for clarification). Never use `--mode interactive`. `--yolo` / `--allow-all` for sandboxed envs only.
- **Pair auto modes with tight tool/command allowlists.** Auto mode ≠ blanket authority. Claude's `--allowedTools "Read,Edit,Bash(npm test*)"` and Gemini's policy files narrow what "auto-approve" actually covers. A small allowlist + `acceptEdits`/`auto_edit` is safer AND more predictable than `bypassPermissions`/`yolo` alone.
- **Prefer `--allowedTools` over bypassing permissions.** Allowlist what the task actually needs: `"Read,Edit,Bash(git diff *)"`. Rule syntax in `references/claude-code.md`.
- **Stream when you want progress, JSON when you want to parse.** `--output-format stream-json --verbose --include-partial-messages` for live feedback; plain `json` for results you'll `jq`.
- **Don't mix stdout channels.** If the CLI is writing to stdout, don't `echo` script status to stdout too — it'll corrupt the JSON. Use stderr (`>&2`) for progress. Gemini in particular writes `[WARN]` lines to stderr when it scans unreadable subdirectories — don't merge `2>&1` into a pipe that expects pure JSON.
- **Verify success in the JSON, not just the exit code.** Codex returns exit 0 even on API failures (rate limits, quota exceeded). Claude can too on recoverable errors. Always parse `is_error` / `type: "error"` / `turn.failed` from the response.
- **Quote prompts aggressively.** Prompts contain `$`, backticks, quotes, newlines. Heredocs (`<<'EOF'`) or reading from a file (`--append-system-prompt-file`) avoid shell-expansion bugs.
- **Trap and clean up sessions.** On failure, a long agentic run may have left partial edits. `trap 'git stash -u' ERR` or an explicit rollback is worth the three lines.

## Anti-patterns

- **Piping untrusted input directly into `-p`.** If the prompt contains user-controlled data, you're one injection away from the model doing something you didn't intend. Wrap untrusted content in clearly-delimited blocks: `<user_input>...</user_input>` with instructions to treat it as data, not instructions.
- **Parsing `--output-format text` with regex.** The text format is for humans. If your next step is `grep`/`sed`/`awk`, you want `json` with `jq`, or `stream-json`.
- **Running agentic mode without `--max-budget-usd`.** An agent that mis-reads a task can loop for a long time. Budget it.
- **Using `--continue` in parallel jobs.** It resolves to "most recent session in this cwd" and races against itself. Use explicit session IDs.
- **Building the same script for every CLI.** Claude, codex, and gemini have meaningfully different headless models. Pick one, commit to its idioms, and only abstract if the user actually needs runtime provider choice.

## When to load what

- Starting a script for Claude Code → read `references/claude-code.md` for flags, output-format schemas, permission rules.
- Starting a script for Codex → read `references/codex.md` for sandbox modes, `--output-schema`, `--output-last-message`, resume semantics.
- Starting a script for Gemini → read `references/gemini.md` for approval modes, policy engine, resume/session handling.
- Starting a script for GitHub Copilot CLI → read `references/copilot.md` for mode flags (`--autopilot`, `--plan`), `--allow-all-tools` / `--no-ask-user` requirements, output formats, and session/resume handling.
- Building a ticket/issue → PR pipeline where the agent should open the PR → read `references/github-agent-task.md` for `gh agent-task` patterns (dispatch-and-forget, dispatch-and-watch, batch from queue, pair with local review).
- Needing to know what tools/MCP servers/skills/models the agent actually has available at runtime (e.g. fail fast in CI if a required MCP server didn't load) → read `references/introspection.md` for both static subcommands (`<cli> mcp list`, `skills list`, etc.) and runtime event-parsing recipes across all five tools.
- Writing a pipeline shape you haven't built before → read `references/cookbook.md` for longer worked examples (GitHub Action, cron PR reviewer, batch translator, review-then-fix loop).

## Delivering the script

When you hand the script back to the user, include:

1. A one-line usage: `./script.sh <arg>` with expected env vars.
2. The budget assumption (token/dollar ceiling per run, typical cost).
3. The permission posture (what the model can do — read-only? edit files? run commands?).
4. Any flags they should tune (model, directory, timeout).

Scripts grow; the person reading yours six months from now — possibly the user, possibly a colleague — will thank you for the three lines of header.
