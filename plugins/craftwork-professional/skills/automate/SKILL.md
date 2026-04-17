---
name: automate
description: Build automation scripts and pipelines that use coding-agent CLIs (Claude Code, Codex, Gemini CLI, GitHub Copilot CLI) in headless/non-interactive mode as the AI engine, or delegate work to cloud agents (`gh agent-task`) that open pull requests asynchronously. Use this skill whenever the user wants to write a shell script, CI job, cron task, batch processor, webhook handler, or any automation that shells out to `claude`, `codex`, `gemini`, `copilot`, or `gh agent-task` — single-turn prompts, multi-turn agentic loops, parallel fan-out across files/folders, structured JSON outputs consumed by downstream tools, or cloud-delegated tasks that produce PRs. Trigger on phrases like "script that uses Claude", "automate with Claude Code", "headless Claude", "batch process files with an LLM", "pipeline with codex exec", "gemini -p", "copilot --autopilot", "gh agent-task create", "GitHub Action that calls Claude", "cron job to review PRs", "agent loop in bash", "dispatch an agent task to open a PR", "fleet-wide agent-task across repos", or any request to integrate a coding agent CLI into an automated workflow. Also trigger when the user describes the shape of a pipeline (fan-out, map-reduce, review-then-fix, extract-then-summarize, ticket-to-PR, scheduled fleet upgrade) and AI is the engine, even if they don't name the CLI explicitly.
---

# Coding-Agent CLI Automation

## Two categories

Pick the category before the tool:

1. **Local execution** — agent runs on your machine or CI runner against cwd. Synchronous, output to stdout, you decide what happens. For anything that produces artifacts other than PRs (reports, JSON, edits, batch transforms).
2. **Delegated cloud execution** — dispatch to a cloud agent that works asynchronously and opens a PR. For ticket/issue/webhook-triggered "implement this and open a PR" workflows.

| CLI | Headless invocation | Reference |
|-----|--------------------|-----------|
| Claude Code | `claude -p "<prompt>"` / `claude --bare -p ...` | `references/claude-code.md` |
| Codex | `codex exec "<prompt>"` | `references/codex.md` |
| Gemini CLI | `gemini -p "<prompt>"` | `references/gemini.md` |
| GitHub Copilot CLI | `copilot -p "<prompt>" --allow-all-tools --autopilot` | `references/copilot.md` |
| `gh agent-task` (cloud) | `gh agent-task create "<description>" --base main` | `references/github-agent-task.md` |

The two can be combined — `gh agent-task` opens the PR, a local CLI reviews it (see cookbook). **Default to Claude Code** unless the user names another. Load the relevant reference when you commit to a CLI.

## Non-negotiable flags (the checklist)

Every script must explicitly set these. CLI defaults are wrong for automation — stating them is the point.

**Local execution (`claude` / `codex` / `gemini` / `copilot`):**

- [ ] **Non-interactive permission mode.** `-p` alone doesn't pick a mode. Claude: `plan` / `acceptEdits` / `dontAsk` / `bypassPermissions`. Codex: `--sandbox <mode>`. Gemini: `--approval-mode <mode>`. Copilot: `--autopilot` (or `--plan`) + `--allow-all-tools` + `--no-ask-user`. No mode ⇒ "default" ⇒ silent block/deny.
- [ ] **Per-call budget cap.** `--max-budget-usd` for Claude; `timeout <N>s` wrapper for Codex/Gemini. **Also per worker inside parallel fan-outs** — one runaway file burns the whole job otherwise.
- [ ] **`--output-format json`** when the next step is a shell pipeline. Never parse `text` with regex/grep/sed.
- [ ] **Structured-output constraint** (`--json-schema` for Claude, `--output-schema` for Codex) when output feeds downstream code. Stops the model from drifting into prose / invalid enums so your `jq` pipeline can't silently break.
- [ ] **`--allowedTools` narrow allowlist** paired with the permission mode. Auto-mode ≠ blanket authority; list exactly what the task needs (e.g. `"Read,Grep,Glob"` for review, `"Read,Edit,Bash(npm test*)"` for dev).
- [ ] **Verify success in the JSON** (`is_error`, `subtype`, `errors[]`, `permission_denials[]`), not just exit code. All four CLIs can exit 0 on recoverable failures.

**Delegated cloud execution (`gh agent-task`):**

- [ ] **Explicit `--base <branch>`.** A PR opened against `develop` when you meant `main` wastes a review cycle.
- [ ] **`create` exit 0 = "dispatched," not "succeeded" and not "merged."** The agent runs after the command returns. Pair dispatch with a completion watcher (`gh pr list`, `pull_request.opened` webhook, or `--follow` in the foreground).
- [ ] **`--repo <owner/name>`** when targeting another repo. One dispatcher can address any repo you have access to without cloning.
- [ ] **Long ticket bodies via `-F <file>` / stdin**, never inlined as argv. Avoids quoting bugs and arg-length limits.

## The five canonical shapes

Shapes 1-4 are local execution; shape 5 is cloud delegation.

### 1. Single-turn, extract to JSON

Classification, extraction, summarization, triage. Script gets a structured answer it can parse.

```bash
result=$(claude --bare -p "Classify the severity of this error: $(cat error.log)" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"severity":{"type":"string","enum":["low","medium","high","critical"]},"reason":{"type":"string"}},"required":["severity","reason"]}' \
  --max-budget-usd 0.10)

severity=$(echo "$result" | jq -r '.structured_output.severity')
```

`--bare` skips hooks/skills/MCP/CLAUDE.md — right for a classifier with no repo context. Drop it if the task benefits from project context.

### 2. Agentic loop on a codebase

"Review and fix," "refactor," "add tests." Model needs file access + command execution.

```bash
cd /path/to/repo
claude -p "Run the test suite and fix any failures. Report which tests you changed." \
  --allowedTools "Bash,Read,Edit" \
  --permission-mode acceptEdits \
  --max-budget-usd 2.00 \
  --output-format json > run.json
```

`acceptEdits` auto-approves writes. `dontAsk` is stricter (deny-by-default) — better for locked-down CI.

### 3. Multi-turn agentic (chained calls sharing state)

Discrete steps with checkpoints — review, decide, act — each seeing prior context.

```bash
session_id=$(claude -p "Audit the auth module for security issues" \
  --output-format json --allowedTools "Read,Grep,Glob" | jq -r '.session_id')

claude -p "Now prioritize the issues you found by severity" \
  --resume "$session_id" --output-format json > prioritized.json

claude -p "Fix the critical issues only" \
  --resume "$session_id" --allowedTools "Read,Edit" --permission-mode acceptEdits
```

`--resume <id>` is explicit and parallel-safe; `--continue` (most-recent-in-cwd) races.

### 4. Parallel fan-out

Same operation against N files/PRs/tickets. Fan out via `xargs -P` or background jobs; collect into a directory, then reduce.

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

Bound parallelism (`-P 4`) to dodge rate limits. Per-call budget prevents a runaway task from burning the batch.

### 5. Delegate to a cloud agent (async PR)

Output = a pull request, no synchronous control needed. Local CLI is a dispatcher.

```bash
# Dispatch into current repo
gh agent-task create "Implement the spec in docs/rfc-042.md" --base main

# Dispatch into ANOTHER repo from outside it — no clone
gh agent-task create -F ticket.md --repo my-org/payments-service --base main

# Fan out across a fleet
gh repo list my-org --topic services --json nameWithOwner --jq '.[].nameWithOwner' | \
  while read -r repo; do
    gh agent-task create -F upgrade.md --repo "$repo" --base main
    sleep 2
  done

# Dispatch and follow logs in the foreground
gh agent-task create -F ticket.md --base main --follow
```

`--repo` is the orchestration lever — one dispatcher addresses any accessible repo. Pair with a local-execution CLI for review-gating: agent opens the PR, Claude/Codex/Gemini/Copilot reviews before merge. See `references/github-agent-task.md` for preview-status, PR-number-ambiguity, and no-JSON-from-create pitfalls.

## Principles that save you later

The checklist covers the must-set flags. These are the gotchas and cross-CLI details it assumes.

- **Budget caps overshoot.** `--max-budget-usd` is checked *post-turn* — one expensive call overshoots 2-3× before stopping. Verify `total_cost_usd` in the JSON. Codex/Gemini have no native flag; use `timeout <N>s` + post-run spend check.

- **Per-CLI permission-mode menu** (pick one from each row per task):

  | CLI | Read-only | Agentic edits | Sandboxed-only | Never use |
  |-----|-----------|---------------|----------------|-----------|
  | Claude | `plan` | `acceptEdits` / `dontAsk` | `bypassPermissions` | `default` / `auto` |
  | Codex | `--sandbox read-only` | `--full-auto` / `--sandbox workspace-write` | `--sandbox danger-full-access` | — (flag IS the posture) |
  | Gemini | `--approval-mode plan` | `--approval-mode auto_edit` | `--approval-mode yolo` | `default` (silent-denies `ask_user`) |
  | Copilot | `--plan` | `--autopilot` + `--allow-all-tools` + `--no-ask-user` | `--yolo` / `--allow-all` | `--mode interactive` |

- **Context posture is per-task.** Each CLI auto-loads a stack (Claude: `CLAUDE.md`/hooks/plugins/skills/MCP; Codex: `AGENTS.md` + `~/.codex/config.toml`; Gemini: extensions/skills/hooks/policies; Copilot: `AGENTS.md` + skills + built-in GitHub MCP). That context is often *why* the agent is competent on this codebase, so for agentic work on the repo, keep it loaded. Strip it for single-file classification, CI reproducibility, or adversarial-input runs: Claude `--bare`; Codex `-c` overrides + `--ephemeral`; Gemini `-e` + explicit `--policy`; Copilot `--no-custom-instructions` + `--disable-builtin-mcps`.

- **Capture session IDs for chained calls.** Claude/Gemini: `.session_id`; Codex: `.thread_id` (in `thread.started` when `--json` is on). Stash it early — `--continue` / `--last` / `-r latest` break under shared cwd or parallelism.

- **Stream for progress, JSON to parse.** `--output-format stream-json --verbose --include-partial-messages` for live feedback; plain `json` for `jq`.

- **Don't mix stdout channels.** If the CLI writes JSON to stdout, send progress to stderr (`>&2`). Gemini writes `[WARN]` to stderr on unreadable subdirs — don't `2>&1` into a pure-JSON pipe.

- **Quote prompts aggressively.** `$`, backticks, quotes, newlines. Heredocs (`<<'EOF'`) or `--append-system-prompt-file` avoid shell-expansion bugs.

- **Trap and clean up.** `trap 'git stash -u' ERR` is three lines that save a partial agentic run.

## Anti-patterns

- **Untrusted input straight into `-p`.** Prompt-injection surface. Wrap user-controlled content in clearly-delimited blocks (`<user_input>...</user_input>`) with instructions to treat it as data.
- **`--continue` in parallel jobs.** Races itself — resolves to "most recent session in this cwd." Use explicit session IDs.
- **One script targeting every CLI.** The headless models differ meaningfully. Pick one, commit to its idioms; only abstract if runtime provider choice is a real requirement.

## When to load what

| Scenario | Reference |
|---|---|
| Writing a Claude Code script (flags, output schemas, permissions) | `references/claude-code.md` |
| Writing a Codex script (sandbox modes, `--output-schema`, resume) | `references/codex.md` |
| Writing a Gemini script (approval modes, policy engine, sessions) | `references/gemini.md` |
| Writing a Copilot script (mode flags, `--allow-all-tools` / `--no-ask-user`, output formats) | `references/copilot.md` |
| Ticket/issue → PR pipelines, fleet dispatch, dispatch-then-review | `references/github-agent-task.md` |
| Detecting MCP / skills / models at runtime (fail-fast in CI) | `references/introspection.md` |
| A pipeline shape you haven't built (GH Action, cron PR review, batch translate, review-then-fix) | `references/cookbook.md` |

## Delivering the script

Include a header with: usage + required env vars; budget (typical cost + per-run cap); permission posture (read-only / edits / shell); tunable flags (model, dir, timeout).
